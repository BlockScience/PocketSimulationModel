import pandas as pd

def prepare_quantiles(simulation_data_path):
    df = pd.read_csv(simulation_data_path, index_col = 0)

    columns = ['total_relays',
     'processed_relays',
     'pokt_price_oracle',
     'n_transactions',
     'floating_supply',
     'POKT_burned',
     'POKT_minted',
     'period_slashing_costs',
     'period_jailing_opportunity_cost',
     'relays_to_tokens_multiplier',
     'gateway_fee_per_relay',
     'application_fee_per_relay',
     'POKT_net_mint',
     'total_application_stake',
     'total_servicer_stake',
     'total_gateway_stake',
     'total_stake',
     'circulating_supply',
     'dao_value_capture',
     'POKT_burned_cummulative',
     'POKT_minted_cummulative',
     'POKT_net_mint_cummulative',
     'burn_rate',
     'mint_rate',
     'net_mint_rate',
     'burn_rate_cummulative',
     'mint_rate_cummulative',
     'net_mint_rate_cummulative',
     'n_understaked_servicers',
     'n_understaked_gateways',
     'n_understaked_applications']

    q = {}
    for column in columns:
        g = df.groupby("timestep")[column]
        q[column] = pd.concat([g.quantile(.25),
                              g.quantile(.5),
                              g.quantile(.75)], axis=1)
        
    return q