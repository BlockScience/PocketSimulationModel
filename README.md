# Pocket Network Simulation Model

## Summary

The enclosed repository serves as a simulation model for testing economic scenarios related to the Pocket Network. It utilizes cadCAD as the underlying simulation engine.

## Model Background

This model is the next step in the evolution from the [Pocket Math Spec](https://github.com/BlockScience/PocketMathSpec) which served as a foundational architecture document prior to development of the simulation model.

## Structure of the Model Repository

1. Exploratory Folder: All jupytyer notebooks being used to test and build the system
2. Model Folder
    A. Action Chains: The code that pieces together the boundary actions, policies, and mechanisms
    B. Boundary Actions, Policies, Mechanisms: All code which implements modular logic
    C. Classes: The class definitions for entities used in the model
    D. Spaces, Types: The annotations used for functions to make it more readable
    E. PSUBs: The partial state update blocks that mostly are used as pass throughs to action chains
    F. Config: The utility functions for setting up configurations, as well as options for starting state and parameter sets

## Partial State Update Blocks

The following are the partial state update blocks used in the model; each block represents one timestep in the system. The current timestep is one day, i.e. setting `T = 365` in the scenario running would correspond to a period of 365 days. 

1. Meta Update Block: updates the time in the system, the price (both true and oracle) for POKT in USD, simulates the number of transactions on the network, and sets certain timestep tracking variables to 0.
2. Join Block: contains all logic around servicers, services, gateways, and applications joining.
3. Stake Block: implements the logic for staking in the system.
4. Delegation and Service Linking Block: takes care of applications delegating to gateways and servicers linking to services.
5. Relay Request Block: simulates the process of requests being created and relayed, as well as recording of relays in different groups.
6. Jailing & Slashing Block: implements the steps for servicers or gateways being slashed or jailed, in addition to the inverse actions + penalties.
7. Block & Fee Rewards Block: logic for both the block rewards as well as the fee rewards.
8. Undelegation & Unservice Block: handles any gateways undelegating or any services being unlinked from.
9. Leave Block: all logic around servicers, services, gateways, and applications leaving. There is also a substep to check which nodes might be understaked and kick certain ones from the system depending on the policy.

## Running Simulations

### run_experiments

To run pre-packaged simulations, import run_experiments and then pass a list of experiment keys. For instance,

    from model import run_experiments
    df = run_experiments(["test1", "test2])

    would run predefined experiments corresponding to "test1" and "test2". 

### auto_run_sets

This option allows for running sets in chunks, saving down the results as CSV files, and picking up where the last run started off. The chunk size determines how many simulations to run at a time.

    from model import run_experiments
    df = auto_run_sets(["test1"], "Data", 10)

### Creating Simulation Configuration

Within `model`, `config`, and `experiment`: the experimental_configs dictionary can be modified to add in different experiments. The structure of it is like so:

    experimental_setups = {
        "test1": {
            "config_option_state": "Test",
            "config_option_params": "Test",
            "monte_carlo_n": 1,
            "T": 365,
        }
    }

Here 
* each key represents a set that can be run,
* the `config_option_state` refers to a specific starting state,
* ` config_option_params` does the same for parameters,
* `monte_carlo_n` defines the number of monte carlo runs, and
* `T` specifies the number of timesteps for the experiment.

Within `model`/`config`/`params`, the `config_option_map` is set up to handle the different options for creating parameter sweeps. More detail in the parameters section on specifics.

    config_option_map = {
        "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"}
    }

Likewise, within model/config/state, there is a `config_option_map` for the specific types of starting state assumptions to implement.

    config_option_map = {
        "Test": {
            "Geozones": "Test",
            "Applications": "Test",
            "DAO": "Test",
            "Gateways": "Test",
            "Services": "Test",
            "Servicers": "Test",
            "Validators": "Test",
        }
    }


## Parameters

Parameters can be divided into three distinct types:

1. System Parameters: All parameters that would be present in the actual implementation of the system
2. Behavior Parameters: All parameters used in the model for assumptions about user actions
3. Function Parameters: All parameters which influence functions for either:
    A. Behaviors: the functional parameters allow for experimenting with different classes of behavior i.e. pulling from a random distribution or feeding in a specific signal that is meant to represent the randomness
    B. Policies: structure that allows for A/B testing of different implementations of policies, i.e. to test and compare different schemes of reward disbursement based on quality of service or other factors.

## State

The state can be seeded with different starting state representations. For example, one might test the impact of *quantity of servicers* on the network by varying the number of servicers. 

## Cloud Running

- The container must be built with docker build . -t pocketsimulation --platform linux/x86_64
- To run one experiment locally do: docker run . -t pocketsimulation Base
- To run two or more for example: docker run . -t pocketsimulation Base test1
