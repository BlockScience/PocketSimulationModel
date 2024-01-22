KPIS = {
    'servicer_npv'                                : 'kpi_1',
    'gateway_npv'                                 : 'kpi_3',
    'circulating_supply'                          : 'kpi_4',
    'available_supply'                            : 'kpi_5',
    'servicer_slashing_cost'                      : 'kpi_8',
    'dao_value_capture'                           : 'kpi_10',
    'servicer_jailing_cost'                       : 'kpi_11',
    'servicer_capital_costs'                      : 'kpi_14',
    'network_load_balancing'                      : 'kpi_C',
    'net_inflation'                               : 'kpi_D',
    'circulating_supply_available_supply_ratio'   : ['kpi_4', 'kpi_5'],
    'net_inflation_dao_value_capture_elasticity'  : ['kpi_D', 'kpi_10'],
}

THRESHOLD_INEQUALITIES = {
    'servicer_npv'                               : lambda df, min, max, frac : threshold_mc_fraction(df, min, max, frac, 'servicer_npv'),
    'servicer_capital_costs'                     : lambda df, min, max       : threshold_average(df, min, max, 'servicer_capital_costs'),
    'servicer_slashing_cost'                     : lambda df, min, max, frac : threshold_mc_fraction(df, min, max, frac, 'servicer_slashing_cost'),
    'servicer_jailing_cost'                      : lambda df, min, max, frac : threshold_mc_fraction(df, min, max, frac, 'servicer_jailing_cost'),
    'gateway_npv'                                : lambda df, min, max, frac : threshold_mc_fraction(df, min, max, frac, 'gateway_npv'),
    'circulating_supply_available_supply_ratio'  : lambda df, min, max       : threshold_kpi_ratios(df, min, max, 'circulating_supply_available_supply_ratio'),
    'net_inflation'                              : lambda df, min, max       : threshold_average(df, min, max, 'net_inflation'),
    'dao_value_capture'                          : lambda df, min, max, frac : threshold_mc_fraction(df, min, max, frac, 'dao_value_capture'),
    'net_inflation_dao_value_capture_elasticity' : lambda df, min, max       : threshold_elasticity(df, min, max, 'net_inflation_dao_value_capture_elasticity'),
    'network_load_balancing'                     : lambda df, min, max, frac : threshold_load_balancing(df, min, max, frac, 'network_load_balancing'),
}


def threshold_mc_fraction(df, min, max, frac, entity):

    if entity not in ['servicer_npv', 'gateway_npv', 'dao_value_capture', 'servicer_slashing_cost', 'servicer_jailing_cost' ]:
        raise ValueError("Error: unsupported threshold inequality type")
    
    num_monte_carlo_sims = len(df.groupby(['run']))
    kpi = KPIS[entity]

    # find average over timesteps within run and simulation
    df_with_means = df.groupby(['simulation', 'run'], as_index = False).mean() 
    if min and max:
        df_with_means['inequality'] = df_with_means.groupby(['simulation'])[kpi].transform(lambda x: (x > min) and (x < max))
    elif min and not max:
        df_with_means['inequality'] = df_with_means.groupby(['simulation'])[kpi].transform(lambda x: (x > min))
    elif max and not min:
        df_with_means['inequality'] = df_with_means.groupby(['simulation'])[kpi].transform(lambda x: (x < max))
    else:
        raise ValueError("Error: must provide at least one maximum or minimum threshold value")

    # recast dataframe with one parameter constellation per simulation
    df_for_analysis = df_with_means[df_with_means['run'] == 1].reset_index()

    # add column with fraction of Monte Carlo runs satisfying inequality to the recast dataframe
    df_for_analysis[entity + '_threshold'] = df_with_means.groupby(['simulation'])['inequality'].sum()/num_monte_carlo_sims > frac

    # return the recast dataframe, which contains one row per simulation (i.e. one row per parameter constellation)
    return df_for_analysis


def threshold_average(df, min, max, entity):

    if entity not in ['servicer_capital_costs', 'net_inflation', 'circulating_supply_available_supply_ratio']:
        raise ValueError("Error: unsupported threshold inequality type")

    if 'ratio' in entity:
        kpi = 'ratio'
    else:
        kpi = KPIS[entity]

    # find average over timesteps within run and simulation
    df_with_means = df.groupby(['simulation', 'run'], as_index = False).mean()
    
    # find average over Monte Carlo runs
    df_with_means['kpi_mean'] = df_with_means.groupby(['simulation'])[kpi].transform('mean')

    # recast dataframe with one parameter constellation per simulation
    df_for_analysis = df_with_means[df_with_means['run'] == 1].reset_index()
    
    if min and max:
        df_for_analysis[entity + '_threshold'] = ((df_with_means[df_with_means['run'] == 1]['kpi_mean'] > min) and 
                                                  (df_with_means[df_with_means['run'] == 1]['kpi_mean'] < max)).values
    elif min and not max:
        df_for_analysis[entity + '_threshold'] = (df_with_means[df_with_means['run'] == 1]['kpi_mean'] > min).values
    elif max and not min:
        df_for_analysis[entity + '_threshold'] = (df_with_means[df_with_means['run'] == 1]['kpi_mean'] < max).values
    else:
        raise ValueError("Error: must provide at least one maximum or minimum threshold value")

    # return the recast dataframe, which contains one row per simulation (i.e. one row per parameter constellation)
    return df_for_analysis


def threshold_kpi_ratios(df, min, max, entity):
    
    if entity not in ['circulating_supply_available_supply_ratio']:
        raise ValueError("Error: unsupported threshold inequality type")

    # This must be a list with two KPI entries
    kpi = KPIS[entity]

    df['ratio'] = df[kpi[0]]/df[kpi[1]]

    return threshold_average(df, min, max, entity)


def threshold_elasticity(df, min, max, entity):
    
    if entity not in ['net_inflation_dao_value_capture_elasticity']:
        raise ValueError("Error: unsupported threshold inequality type")
    
    kpi = KPIS[entity]

    df_delta = df.pct_change()
    df_delta['elasticity'] = df_delta[kpi[0]]/df_delta[kpi[1]]
    df.drop(df.index[:1], inplace=True)
    df['elasticity'] = df_delta['elasticity']

    return threshold_average(df, min, max, entity)
    
# WIP
def threshold_load_balancing(df, min, max, frac, entity):
    
    if entity not in ['network_load_balancing']:
        raise ValueError("Error: unsupported threshold inequality type")
    
    kpi = KPIS[entity]

def drop_unnecessary_columns(df, control_params):
    
    cols = df.columns
    retained_columns = [name for name in cols if "threshold" in name]
    retained_columns.extend([*tuple(control_params)])

    reduced_df = df[retained_columns].set_index(['simulation'])

    return reduced_df





