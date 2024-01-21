import pandas as pd

#####################################
## Global values re-used across    ##
## various scenarios.              ##
#####################################

############################################
## Define constants outside the functions ##
## so they aren't defined every time the  ##
## function is called.                    ##
############################################

# Values for Gateway Viability
s1_val = 0
s2_val = 0.9

t1_val = -182_000
t2_val = 0.9

u1_val = 0.5  # Placeholder while we wait for actual value.
u2_val = 0.9

v1_val = 0.25  # Document suggests this may be revised upward

w1 = 0.9
w2 = 1.1

a1 = 0
a2 = 100


def calc_gvs_thresh_ineq_met(df: pd.DataFrame, num_gvs_ineq=4) -> float:
    ############################################
    ## Gateway Viability Scenarios            ##
    ############################################

    # Gateway Viability Scenario
    # Threshold Inequality 1
    # The average servicer cost per unit of reward
    # ust lie between a_1 and a_2, where a_1 < a_2.

    avg_servicer_cost_per_unit_of_reward = (df["KPI 14"] / df["KPI 1"]).mean()
    first_condition = avg_servicer_cost_per_unit_of_reward > a1
    second_condition = avg_servicer_cost_per_unit_of_reward < a2
    gvs_ineq_1_met = int(first_condition and second_condition)

    # Gateway Viability Scenario
    # Threshold Inequality 2
    # The  fraction of the Monte Carlo simulations
    # for which average (across Servicers) Servicer NPV
    # is greater than s1 must be at least  s2.

    gvs_ineq_2_met = int(
        (df["KPI 1"] > s1_val).mean() > s2_val
    )  # boolean: was this inequality met?

    # Gateway Viability Scenario
    # Threshold Inequality 3

    # The fraction of the Monte Carlo simulations
    # for which Gateway Cost NPV
    # is greater than t1 must be at least t2.

    gvs_ineq_3_met = int(
        (df["KPI 3"] > t1_val).mean() > t2_val
    )  # boolean: was this inequality met?

    # Network Viability Scenario
    # Threshold Inequality 4

    # The fraction of the Monte Carlo simulations
    # for which the average required Gateway NPV revenue t
    # hat equalizes average Gateway NPV and average Servicer NPV,
    # when expressed as a fraction $\mu$ of average Servicer NPV such that
    #  $\mu < \bar u_1,$ must be at least $\bar u_2$.

    gvs_ineq_4_met = int((df["KPI 1"] < u1_val).mean() >= u2_val)

    inequalities = [gvs_ineq_1_met, gvs_ineq_2_met, gvs_ineq_3_met, gvs_ineq_4_met]

    total_met = sum(inequalities)
    proportion_met = total_met / num_gvs_ineq

    return proportion_met
