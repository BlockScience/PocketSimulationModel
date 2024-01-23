# WIP
def threshold_load_balancing(df, min, max, frac, entity):
    if entity not in ["network_load_balancing"]:
        raise ValueError("Error: unsupported threshold inequality type")

    kpi = KPIS[entity]


def drop_unnecessary_columns(df, control_params):
    cols = df.columns
    retained_columns = [name for name in cols if "threshold" in name]
    retained_columns.extend([*tuple(control_params)])

    reduced_df = df[retained_columns].set_index(["simulation"])

    return reduced_df
