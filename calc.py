# Calculating threshold inequalities

import pandas as pd

def calc_thresh_ineq_met(df: pd.DataFrame, 
                         scenario: str = "gvs", 
                         num_ineq = 7):
    """
    A wrapper function that passes to a function below based on scenarios.
    """ 

    if scenario == "gvs": #Gateway Viability 
        proportion_met, total_met = calc_gvs_thresh_ineq_met(df)

    elif scenario == "nvs": #Network Viability
        proportion_met, total_met = calc_nvs_thresh_ineq_met(df)

    elif scenario == "svs": #Servicer Viability
        raise Error("Servicer Viability not yet implemented.")

    elif scenario == "nfs": #Network Failure Viability
        raise Error("Network Failures Viability not yet implemented.")

    elif scenario == "nfo": #Network Failure Oracle
        raise Error("Network Failures Oracle not yet implemented.")
    
    return proportion_met, total_met


############################################
## Define constants outside the functions ##
## so they aren't defined every time the  ##
## function is called.                    ##
############################################

# Values for Network Viability
s1_val = 0 
s2_val = 0.9

t1_val = -182_000
t2_val = 0.9

u1_val = 0.5 # Placeholder while we wait for actual value.
u2_val = 0.9

v1_val = 0.25 # Document suggests this may be revised upward

w1 = 0.9
w2 = 1.1


############################################
## Network Viability Scenarios           ## 
############################################

def calc_nvs_thresh_ineq_met(df: pd.DataFrame, num_nvs_ineq = 7) -> float:
    # Network Viability Scenario
    # Threshold Inequality 1
    # The  fraction of the Monte Carlo simulations
    # for which average (across Servicers) Servicer NPV 
    # is greater than s1 must be at least  s2.   


    nvs_ineq_1_met = int((df['KPI 1'] > s1_val).mean() > s2_val) # boolean: was this inequality met? 

    # Network Viability Scenario
    # Threshold Inequality 2 
    # the Monte Carlo simulations for which average (across Gateways) Gateway Cost NPV
    # is greater than t1  must be at least t2.


    nvs_ineq_2_met = int((df['KPI 1'] > t1_val).mean() > t2_val) # boolean: was this inequality met? 
    
    # Network Viability Scenario
    # Threshold Inequality 3 
    # The fraction of the Monte Carlo simulations 
    # for which the average required Gateway NPV revenue t
    # hat equalizes average Gateway NPV and average Servicer NPV, 
    # when expressed as a fraction $\mu$ of average Servicer NPV such that
    #  $\mu < \bar u_1,$ must be at least $\bar u_2$. 
    

    nvs_ineq_3_met = int((df['KPI 1'] < u1_val).mean() >= u2_val)


    # Network Viability Scenario
    # Threshold Inequality 4 
    # The average ratio of circulating supply to available supply
    # should not be less than v1

    nvs_ineq_4_met = int((df['circulating_supply']/df['floating_supply']).mean() <= 0.25) # boolean: was this inequality met? 
    # NOTE: Is floating supply the same as available supply?

    # Network Viability Scenario
    # Threshold Inequality 5
    # The average ratio of the growth rate of circulating supply 
    # to the growth rate of DAO value capture 
    # should be between w_1 and w_2, with w_2 > w_1  

    # NOTE: 8 am not sure here about "growth rate", so I am just using column values for now.

    avg_growth_rate = (df['circulating_supply']/df['dao_value_capture']).mean() #TODO: check
    nvs_ineq_5_met = int((w2 > avg_growth_rate) and (avg_growth_rate > w1))

    # Network Viability Scenario
    # Threshold Inequality 6
    # The average elasticity of the inflation/deflation rate of POKT 
    # with respect to total fees should lie between x_1 and x_2, x_2 > x_1

    # TODO: How to find total fees in DataFrame? 
    # x1 = -1.0
    # x2 = -0.5 
    #  
    # TODO: Get total fees
    # TODO: Get inflation rate
    nv_ineq_6_met = 0 # Set to False for now

    # Network Viability Scenario
    # Threshold Inequality 7
    # The average inflation/deflation rate of POKT 
    # should fall between y1 and y2, where y2 > y1. 
    average_inflation = df["net_mint_rate"].mean()
    first_condition = (average_inflation > y1)
    second_condition = (average_inflation < y2)
    nv_ineq_7_met = int(first_condition and second_condition)

    # Network Viability Scenario
    # Threshold Inequality 8
    # The fraction of the Monte Carlo simulations 
    # for which DAO value capture 
    # lies between z1 and z2, where z1 < z2,
    #  must be at least z3.
 
    lies_between_bounds  = (df['dao_value_capture'] > z1) and (df['dao_value_capture']) < z2
    nv_ineq_8_met = int(lies_between_bounds.mean() >= z3)

    inequalities = [nv_ineq_1_met, nv_ineq_2_met, nv_ineq_3_met,
                   nv_ineq_4_met, nv_ineq_5_met, nv_ineq_6_met,
                    nv_ineq_7_met, nv_ineq_8_met]

     

    total_met = sum(inequalities)
    proportion_met = total_met/num_nvs_ineq

    return proportion_met, total_met

# Values for Gateway Viability

# s1, s2, t1, t2, u1, u2 as defined in Network Viability constants

a1 = 0
a2 = 100

def calc_gvs_thresh_ineq_met(df: pd.DataFrame,
                             num_gvs_ineq = 4) -> float:

    ############################################
    ## Gateway Viability Scenarios            ## 
    ############################################

    # Gateway Viability Scenario
    # Threshold Inequality 1
    # The average servicer cost per unit of reward 
    # ust lie between a_1 and a_2, where a_1 < a_2. 

    avg_servicer_cost_per_unit_of_reward = (df["KPI 14"]/df["KPI 1"]).mean()
    first_condition = avg_servicer_cost_per_unit_of_reward > a1
    second_condition = avg_servicer_cost_per_unit_of_reward < a2
    gvs_ineq_1_met = int(first_condition and second_condition)

    # Gateway Viability Scenario
    # Threshold Inequality 2
    # The  fraction of the Monte Carlo simulations
    # for which average (across Servicers) Servicer NPV 
    # is greater than s1 must be at least  s2.   

    gvs_ineq_2_met = int((df['KPI 1'] > s1_val).mean() > s2_val) # boolean: was this inequality met? 

    # Gateway Viability Scenario
    # Threshold Inequality 3

    # The fraction of the Monte Carlo simulations
    # for which Gateway Cost NPV 
    # is greater than t1 must be at least t2. 

    gvs_ineq_3_met = int((df['KPI 1'] > t1_val).mean() > t2_val) # boolean: was this inequality met? 

    # Network Viability Scenario
    # Threshold Inequality 3 
    # The fraction of the Monte Carlo simulations 
    # for which the average required Gateway NPV revenue t
    # hat equalizes average Gateway NPV and average Servicer NPV, 
    # when expressed as a fraction $\mu$ of average Servicer NPV such that
    #  $\mu < \bar u_1,$ must be at least $\bar u_2$. 
    
    gvs_ineq_4_met = int((df['KPI 1'] < u1_val).mean() >= u2_val)

    inequalities = [gvs_ineq_1_met, gvs_ineq_2_met, 
                    gvs_ineq_3_met, gvs_ineq_4_met]

    total_met = sum(inequalities)
    proportion_met = total_met/num_gvs_ineq

    return proportion_met, total_met






























