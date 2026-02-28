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

    import copy
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


import pandas as pd

def load_resource_mapping_from_excel(filepath,
                                     resource_column='Resource',
                                     weight_column='Weight'):
    """
    Load resource mapping from Excel file.

    Parameters
    ----------
    filepath : str
        Path to Excel file.
    resource_column : str
        Column name containing resource labels (e.g., 'R1').
    weight_column : str
        Column name containing numeric weights.

    Returns
    -------
    dict
        Mapping dictionary like {'R1': 10, 'R2': 20, ...}
    """

    df = pd.read_excel(filepath)

    if resource_column not in df.columns or weight_column not in df.columns:
        raise ValueError("Specified columns not found in Excel file.")

    mapping = dict(zip(df[resource_column], df[weight_column]))

    return mapping

import copy

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

