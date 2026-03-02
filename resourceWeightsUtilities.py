import copy
import pandas as pd


def append_assigned_numbers(data, resource_mapping):
    """
    Append a number to each record based on its resource label,
    using an explicitly provided mapping.

    Parameters
    ----------
    data : list
        Nested input list.
    resource_mapping : dict
        Dictionary mapping resource labels to assigned numbers.
        Example:
        {
            'R1': 10,
            'R2': 20,
            'R3': 30,
            'R4': 40,
            'R5': 50,
            'R6': 60,
            'R7': 70,
            'E':  0
        }

    Returns
    -------
    list
        New list with appended assigned numbers.
    """

    new_data = copy.deepcopy(data)

    for record in new_data:
        resource_label = record[5][0]  # e.g. 'R4'

        if resource_label not in resource_mapping:
            raise ValueError(f"Resource '{resource_label}' not found in mapping.")

        assigned_number = resource_mapping[resource_label]
        record.append(assigned_number)

    return new_data


def add_assigned_number_to_node_weights(
    records,
    node_intervals: dict,
    *,
    in_place=False,
    strict=None  # kept for backward compatibility
):
    """
    Add each record's assigned number (last element) to node_intervals[node_id].

    Only updates nodes that already exist in node_intervals.
    Nodes not present are silently skipped.

    Parameters
    ----------
    records : list
    node_intervals : dict
    in_place : bool
    strict : ignored (kept for compatibility)
    """

    updated = node_intervals if in_place else dict(node_intervals)

    for rec in records:
        node_id = rec[-2]
        add_val = rec[-1]
        key = str(node_id)

        if key not in updated:
            continue  # skip missing nodes

        updated[key] = float(updated[key]) + float(add_val)

    return updated



def append_number_from_resource_mapping(
    data,
    mapping_csv_path,
    Step_Number=1,
    date_column="Date",
    resource_column="ProviderID",
    weight_column="Available_Prob",
    default_for_E=0.0
):
    """
    Append weight to each record based on resource mapping
    derived from the specified Step_Number (day index).

    If Step_Number == 1 → use first (earliest) date.
    """

    # -----------------------
    # Load mapping CSV
    # -----------------------
    df = pd.read_csv(mapping_csv_path)

    df[date_column] = pd.to_datetime(df[date_column])
    df[resource_column] = df[resource_column].astype(str).str.strip()
    df[weight_column] = pd.to_numeric(df[weight_column], errors="raise")

    df = df.sort_values(by=date_column)

    unique_dates = sorted(df[date_column].unique())

    if Step_Number < 1 or Step_Number > len(unique_dates):
        raise ValueError("Step_Number out of range.")

    selected_date = unique_dates[Step_Number - 1]

    # Filter only selected date
    df_step = df[df[date_column] == selected_date]

    # Build mapping for that date
    resource_mapping = dict(zip(df_step[resource_column], df_step[weight_column]))

    # Ensure default for 'E'
    resource_mapping.setdefault("E", default_for_E)

    # -----------------------
    # Original logic (unchanged)
    # -----------------------
    new_data = copy.deepcopy(data)

    for record in new_data:
        resource_label = record[5][0]

        if resource_label not in resource_mapping:
            raise ValueError(
                f"Resource '{resource_label}' not found for date {selected_date}."
            )

        record.append(resource_mapping[resource_label])

    return new_data



def append_number_from_resource_mapping(
    data,
    mapping_csv_path: str,
    date_column: str = "Date",
    resource_column: str = "ProviderID",
    weight_column: str = "Available_Prob",
    Step_Number: int = 1,
    scale_factor: float = 1.0,
    default_for_E: float = 0.0
):
    """
    Append weight to each record based on resource mapping derived
    from a specific step (day).

    If Step_Number == 1:
        Use the first day (earliest date) in the CSV.

    Parameters
    ----------
    data : list
        Your nested graph node structure.
    mapping_csv_path : str
        Path to cleaned CSV file.
    date_column : str
        Name of date column in CSV.
    resource_column : str
        Column containing resource IDs (e.g., R1).
    weight_column : str
        Column containing weights.
    Step_Number : int
        Determines which day's mapping to use.
    scale_factor : float
        Multiply weights by this factor.
    default_for_E : float
        Default value for resource 'E'.

    Returns
    -------
    list
        Updated node list with appended weights.
    """

    # -----------------------------
    # Load and preprocess mapping
    # -----------------------------
    df = pd.read_csv(mapping_csv_path)

    df[date_column] = pd.to_datetime(df[date_column])
    df[resource_column] = df[resource_column].astype(str).str.strip()
    df[weight_column] = pd.to_numeric(df[weight_column], errors="raise")

    df = df.sort_values(by=date_column)

    unique_dates = sorted(df[date_column].unique())

    if Step_Number < 1 or Step_Number > len(unique_dates):
        raise ValueError("Step_Number out of range.")

    # Select date based on Step_Number
    selected_date = unique_dates[Step_Number - 1]

    df_step = df.loc[df[date_column] == selected_date].copy()

    # Scale weights
    df_step[weight_column] = df_step[weight_column] * scale_factor

    # Build mapping for that day
    resource_mapping = dict(zip(df_step[resource_column], df_step[weight_column]))

    resource_mapping.setdefault("E", default_for_E)

    # -----------------------------
    # Append weights to graph data
    # -----------------------------
    new_data = copy.deepcopy(data)

    for record in new_data:
        resource_label = record[5][0]

        if resource_label not in resource_mapping:
            raise ValueError(f"Resource '{resource_label}' not found for date {selected_date}.")

        record.append(resource_mapping[resource_label])

    return new_data



def preprocess_remove_pre_monday_and_weekends(
    input_filepath: str,
    output_filepath: str,
    date_column: str = "Date"
):
    """
    Preprocess CSV data by:
      1) Removing all rows before the first Monday
      2) Removing all weekend rows (Saturday, Sunday)
      3) Saving cleaned table to a new CSV

    Parameters
    ----------
    input_filepath : str
        Path to input CSV file.
    output_filepath : str
        Path to save processed CSV file.
    date_column : str
        Name of the date column.
    """

    # Load file
    df = pd.read_csv(input_filepath)

    # Validate date column
    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in CSV. Columns: {list(df.columns)}")

    # Convert to datetime
    df[date_column] = pd.to_datetime(df[date_column], errors="raise")

    # Sort by date (important for determining first Monday)
    df = df.sort_values(by=date_column)

    # Find first Monday
    first_monday = df.loc[df[date_column].dt.weekday == 0, date_column].min()

    if pd.isna(first_monday):
        raise ValueError("No Monday found in dataset.")

    # Remove rows before first Monday
    df = df[df[date_column] >= first_monday]

    # Remove weekends (Saturday=5, Sunday=6)
    df = df[df[date_column].dt.weekday < 5]

    # Save output
    df.to_csv(output_filepath, index=False)

    print(f"Preprocessing complete. Cleaned file saved to: {output_filepath}")

