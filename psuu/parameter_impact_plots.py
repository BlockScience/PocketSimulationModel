import os
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#################################
## Begin  scenario dictionary  ##
#################################

scenarios_dict = dict()
scenarios_dict["gateway_viability_sweep_ag"] = dict()
scenarios_dict["gateway_viability_sweep_ag"]["sweep title"] = "Gateway Viability"
scenarios_dict["gateway_viability_sweep_ag"]["param_abbreviations"] = {
                                                             "param_session_token_bucket_coefficient" : "TTRM",
                                                             "param_gateway_fee_per_relay" : "GFPR",
                                                             "param_application_fee_per_relay": "AFPR",
                                                             "param_gateway_minimum_stake": "GMS",
                                                             "param_minimum_application_stake": "AMS"
                                                             }
scenarios_dict["gateway_viability_sweep_ag"]["KPIs"] = ["KPI 1", "KPI 3", "KPI 14"]

scenarios_dict["network_failures_service_ag"] = dict()
scenarios_dict["network_failures_service_ag"]["sweep title"] = "Network Failures Servicer"
scenarios_dict["network_failures_service_ag"]["param_abbreviations"] = {
                                              "param_slash_fraction_downtime" : "SFD",
                                              "param_max_chains_servicer" : "MCS",
                                              "param_downtime_jail_duration": "DJD"
                                           }
scenarios_dict["network_failures_service_ag"]["KPIs"] = ["KPI 11", "KPI C"]

scenarios_dict["servicer_viability_ag"] = dict()
scenarios_dict["servicer_viability_ag"]["sweep title"] = "Servicer Viability"
scenarios_dict["servicer_viability_ag"]["param_abbreviations"] = {
                                                             "param_relays_to_tokens_multiplier" : "TTRM",
                                                             "param_gateway_fee_per_relay" : "GFPR",
                                                             "param_application_fee_per_relay": "AFPR",
                                                             "param_gateway_minimum_stake": "GMS",
                                                             "param_minimum_application_stake": "AMS",
                                                             "param_dao_allocation": "DAL",
                                                             "param_validator_fee_percentage": "VFP"
                                                             }
scenarios_dict["servicer_viability_ag"]["KPIs"] = ["KPI 1", "KPI 3", "KPI 4", "KPI 5", "KPI D", "KPI 10", "KPI 14"]

#################################
## End scenario dictionary.    ##
#################################

#################################
## Begin KPI cleanup map.      ##
#################################

KPI_CLEANUP_MAP = {
    "circulating_supply": "KPI 4",
    "floating_supply": "KPI 5",
    "net_mint_rate_cummulative": "KPI D",
    "dao_value_capture": "KPI 10",
}

#################################
## End KPI cleanup map.      ##
#################################

#################################
## Begin functions.            ##
#################################

def read_and_format_data(directory: str = "simulation_data",
                        scenario_sweep_category: str = None,
                        ag_iter_col_name: str = "AG iteration",
                        start_iter: int = 1,
                        end_iter: int = 6):
    # Find all .csv files in the directory that begin with the given string
    matching_files = [
                    f"{scenario_sweep_category}{file_num}_.csv"
                    for file_num in range(start_iter, end_iter + 1)
                    ]

    # Load each matching file into a DataFrame
    data_frames = [pd.read_csv(os.path.join(directory, file)) for file in matching_files]
    for ag_num in range(len(data_frames)):
        data_frames[ag_num][ag_iter_col_name] = ag_num + 1

    # Assuming data_frames is the list of DataFrames to be merged
    merged_df = pd.concat(data_frames, ignore_index=True)

    # Rename KPI columns to final forms for reporting
    merged_df = merged_df.rename(columns=KPI_CLEANUP_MAP)
    
    return merged_df



def make_initial_vs_final_plot(df: pd.DataFrame,
                               scenario_sweep_category: str,
                               param_name: str,
                               param_abbr_to_use: str = None,
                               kpi_names_to_use: List[str] = None,
                               ag_iter_col_name: str = "AG iteration",
                               start_iter: int = 1,
                               end_iter: int = 6,
                               fig_height: float = 8,
                               fig_width: float = 10):

    scenario = scenarios_dict.get(scenario_sweep_category, None)

    # Set parameter abbreviation from master scenario dictionary.
    if param_abbr_to_use is None:
        param_name_abbr_dict = scenario.get("param_abbreviations")
        param_abbr = param_name_abbr_dict.get(param_name)
    else:
        param_abbr_to_use = param_abbr

    # Set KPIs from master scenario dictionary. 
    if kpi_names_to_use is None:
        kpi_names= scenario.get("KPIs")
    else:
        kpi_names_to_use = kpi_names

    # Define the custom color palette 
    custom_palette = ["#000000", "#FF0000"]  
    sns.set_palette(custom_palette)

    # Do some preprocessing to create a new DataFrame.
    # There is a duplicate column with a shorter name. 

    new_df = df.copy(deep = True)
    new_df[param_abbr] = new_df[param_name].copy()

    # Create a plot object with subplots. 
    fig, axs = plt.subplots(len(kpi_names), 2, 
                      figsize=(fig_height,  fig_width), 
                      sharex='row', sharey='row', 
                      gridspec_kw={'hspace': 0.5})
    fig.subplots_adjust(top=0.95)
    title_to_use = scenario.get("sweep title")
    fig.suptitle(f"{title_to_use}: \n Impact of {param_name} ({param_abbr}) \n on selected KPIs.")

    # Iterate over the rows, creating initial vs. final densities.

    for row_num, kpi_name in enumerate(kpi_names):
        sns.kdeplot(
            data = new_df[new_df[ag_iter_col_name] == start_iter] ,
            x = kpi_names[row_num],
            hue = param_abbr,
            ax = axs[row_num,0],
            palette = custom_palette)
        axs[row_num,0].set_title(f"Initial Iteration: {kpi_name}")

        sns.kdeplot(
            data = new_df[new_df[ag_iter_col_name] == end_iter] ,
            x = kpi_names[row_num],
            hue = param_abbr,
            ax = axs[row_num,1],
            palette = custom_palette)
        axs[row_num,1].set_title(f"Final Iteration: {kpi_name}")
        

    plt.show()
    return fig, axs

#################################
## End functions.              ##
#################################