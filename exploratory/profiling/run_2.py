import os, sys
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append("../..")
from model import run_experiments
from model.config.params import build_params
import numpy as np
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

df, simulation_kpis = run_experiments(["gateway_viability_sweep_ag1_1",
                                       "gateway_viability_sweep_ag1_2",
                                       "gateway_viability_sweep_ag1_3"],
                                       disable_postprocessing=True,
                                       disable_deepcopy=True,
                                       context=ExecutionMode().single_mode)