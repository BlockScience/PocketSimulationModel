import numpy as np
import pandas as pd 

# TODO: import methods from other files for parameter grid updates. 


df = pd.read_csv("gateway_viability_sweep_ag1_.csv")

def read_data(filename: str = None) -> pd.DataFrame:
    """
    We are keeping this as a method in case another approach is used. 
    """
    return pd.read_csv(filename)    

def run_cadcad_sims(param_grid, data: pd.DataFrame, experiment_num):
    #########################################
    # NOTE: This is a placeholder method.  ##
    ## Currently we just take the next     ##
    ## step from a pre-loaded DataFrame.   ##
    ##  In reality we need to run the      ##
    ##  cadCAD process that generates the  ##
    ## real data.                          ##
    ## TODO: Replacement needed to run real cadCAD.  ##
    #########################################
    if not(data is None):
        raise ValueError("Do not try to use this method yet without a DataFrame input. It is just a mock.")
    else:
        return data[data['Experiment Name'] == f'gateway_viability_sweep_ag1_{experiment_num}']

def process_data_to_kpis(raw_data):
    #########################################
    # NOTE: This is a placeholder method.  ##
    ## Take raw data from experiment and   ##
    ## convert to KPIs.                    ##
    ## TODO: Replacement needed?           ##
    #########################################

    kpi_col_names = ['Net Minting Rate', 
                'KPI C', 
                'KPI E',
                'KPI 1',
                'KPI 3',
                'KPI 11', 
                'KPI 14', 
                'total_relays', 
                'processed_relays',
                'kpi_a', 
                'floating_supply', 
                'circulating_supply',
                'dao_value_capture', 
                'POKT_burned_cummulative', 
                'POKT_minted_cummulative', 
                'POKT_net_mint_cummulative',
                'burn_rate_cummulative', 
                'mint_rate_cummulative',
                'net_mint_rate_cummulative']

    kpi_info = raw_data_row[kpi_col_names]
    return kpi_info

def convert_to_threshold_vec(kpis, thresholds, num_kpi_thresholds):
    #########################################
    # NOTE: This is a placeholder method.  ##
    ## Currently we just return 
    ## Take kpis and turn into binary      ##
    ## variables based on thresholds.      ##
    ## TODO: Replacement needed.           ##
    #########################################
    
    threshold_vec = np.random.randint(0, 2, size=num_kpi_thresholds)
    
    return threshold_vec

def check_if_finished(kpis, thresh_ineq_vec):
    #########################################
    # NOTE: This is a placeholder method.  ##
    ## Currently we just return False.     ##
    ## In general, we need to see if any   ##
    ## stopping criteria, i.e.      ##
    ## TODO: Replacement needed?           ##
    #########################################
    return False

def provide_updated_param_grid(param_grid, kpis, thresh_ineq_vec, method_to_use):
    # TODO: Create logic that will provide an updated param_grid.
    return None

def add_to_history(history_data, raw_data, kpis, thresh_ineq_vec, time_taken):
    # TODO:  Add the current information to the history DataFrame.
    return None 

def write_history_to_csv(history_data, history_filename):
    # TODO: Write the current history to a .csv file. 
    return None 

def main_loop(init_param_grid, max_steps, data, 
              bounds_to_use, history_filename, kpi_vec_size,
              method):
    step = 0  # current step in simulation 
    history = pd.DataFrame() # begin with empty data frame
    param_grid = init_param_grid # The parameter grid object to update
    finished = False # Is simulation done? 
    
    while not(finished or step > max_steps):
        start_time = time.time
        raw_data = run_cadcad_sims(param_grid, data, step)
        kpis = process_data_to_kpis(raw_data)
        thresh_ineq_vec = convert_to_threshold_vec(kpis, bounds_to_use, kpi_vec_size)
        finished = check_if_finished(kpis, thresh_ineq_vec)
        add_to_history(history, raw_data, kpis, thresh_ineq_vec)

        if not(finished):
            param_grid = provide_updated_param_grid(param_grid, kpis, thresh_ineq_vec, method)
            step = step + 1
        else:
            if record_time: 
                write_history_to_csv(history, history_filename, time)
            else: 
                write_history_to_csv(history, history_filename)










# print(df['Experiment Name'].unique())





