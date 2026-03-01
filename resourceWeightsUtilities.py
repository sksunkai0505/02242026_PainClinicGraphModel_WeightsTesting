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


def add_assigned_number_to_node_weights(records, node_intervals, *, in_place=False, strict=True):
    """
    Add the newly assigned number (last element of each record) to the existing
    node weights in node_intervals, matching by node index (second last element).

    Parameters
    ----------
    records : list
        Each record ends with [..., node_id, assigned_number]
        Example: [..., 0, 40]
    node_intervals : dict
        Existing weights keyed by string node ids, e.g. {'0': 4.36, '1': 1e-07, ...}
    in_place : bool, optional
        If True, modify node_intervals directly. If False (default), return a new dict.
    strict : bool, optional
        If True, raise an error if a node_id from records is missing in node_intervals.
        If False, create missing keys starting at 0.0.

    Returns
    -------
    dict
        Updated weights dict (same object if in_place=True).
    """
    updated = node_intervals if in_place else dict(node_intervals)

    for rec in records:
        if len(rec) < 2:
            raise ValueError(f"Record too short: {rec}")

        node_id = rec[-2]          # second last element
        add_val = rec[-1]          # last element (new assigned number)

        key = str(node_id)         # node_intervals uses string keys

        if strict and key not in updated:
            raise KeyError(f"Node '{key}' not found in node_intervals.")
        if key not in updated:
            updated[key] = 0.0

        updated[key] = float(updated[key]) + float(add_val)

    return updated



def load_resource_mapping_from_csv(
    filepath: str,
    resource_column: str = "ProviderID",
    weight_column: str = "Available_Prob",
    *,
    scale_factor: float = 10.0,
    default_for_E: float = 0.0,
    allow_duplicates: bool = False,
) -> dict:
    """
    Load resource->weight mapping from a CSV file and scale weights.

    Parameters
    ----------
    filepath : str
        Path to CSV file.
    resource_column : str
        Column containing resource labels.
    weight_column : str
        Column containing numeric weights.
    scale_factor : float
        Multiply weight_column values by this factor (default = 10).
    default_for_E : float
        Default value if 'E' is not present in CSV.
    allow_duplicates : bool
        If True, duplicates are averaged; otherwise error.

    Returns
    -------
    dict
        Mapping dictionary {resource: scaled_weight}
    """

    df = pd.read_csv(filepath)

    if resource_column not in df.columns or weight_column not in df.columns:
        raise ValueError(
            f"Columns not found. Need '{resource_column}' and '{weight_column}'. "
            f"CSV has: {list(df.columns)}"
        )

    df[resource_column] = df[resource_column].astype(str).str.strip()
    df[weight_column] = pd.to_numeric(df[weight_column], errors="raise")

    if df[resource_column].duplicated().any():
        if not allow_duplicates:
            duplicates = df.loc[df[resource_column].duplicated(), resource_column].tolist()
            raise ValueError(f"Duplicate ProviderIDs found: {duplicates}")
        df = df.groupby(resource_column, as_index=False)[weight_column].mean()

    # 🔹 Scale weights
    df[weight_column] = df[weight_column] * scale_factor

    df = df.dropna(subset=[weight_column])

    mapping = dict(zip(df[resource_column], df[weight_column]))

    # Ensure default for E
    mapping.setdefault("E", float(default_for_E))

    return mapping



def append_number_from_resource_mapping(data, resource_mapping):
    """
    Append weight to each record based on resource label.
    """

    new_data = copy.deepcopy(data)

    for record in new_data:
        resource_label = record[5][0]

        if resource_label not in resource_mapping:
            raise ValueError(f"Resource '{resource_label}' not found in mapping.")

        record.append(resource_mapping[resource_label])

    return new_data

