import sys
sys.path.append("../..")
from pathos.pools import ProcessPool
from cadCAD.engine import ExecutionMode
from model import run_experiments



exps = ["gateway_viability_sweep_ag1_1",
        "gateway_viability_sweep_ag1_2",
        "gateway_viability_sweep_ag1_3"]


def run_single_exp(exp):
    run_experiments([exp],
                    disable_postprocessing=True,
                    context=ExecutionMode().single_proc)


with ProcessPool() as p:
    p.map(run_single_exp, exps)
