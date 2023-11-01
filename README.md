# Pocket Network Simulation Model

## Summary

The enclosed repository serves as a simulation model for testing economic scenarios related to the Pocket Network. It is built off cadCAD under the hood.

## Model Background

This model is the next step in the evolution from the [Pocket Math Spec](https://github.com/BlockScience/PocketMathSpec) which served as a foundational architecture document prior to development.

## Current Development

The current development updates are:

1. Majority of the core development for action chains are completed but there is still refinement needed in terms of constraints and non-basic behaviors.
2. Parameters are being filled in over time as all their relationships are filled in (sourced from the math spec for easily knowing where parameters need to be invoked).
3. Basic scenario creation tools implemented which allow for testing iteratively during development.
4. Lots of work in progress, all tracked through github issues and tagged for easier triage.

## Structure of the Model Repository

1. Exploratory Folder: All jupytyer notebooks being used to test and build the system
2. Model Folder
    A. Action Chains: The code that pieces together the boundary actions, policies, and mechanisms
    B. Boundary Actions, Policies, Mechanisms: All code which implements modular logic
    C. Classes: The class definitions for entities used in the model
    D. Spaces, Types: The annotations used for functions to make it more readable
    E. PSUBs: The partial state update blocks that mostly are used as pass throughs to action chains
    F. Config: The utility functions for setting up configurations as well as options for starting state + parameter sets

## Partial State Update Blocks

## Running Simulations

### run_experiments

To run pre-packaged simulations, import run_experiments and then pass a list of experiment keys like so:

    from model import run_experiments
    df = run_experiments(["test1"])

### auto_run_sets

This option allows for running sets in chunks, saving down the results as CSV files, and picking up where last started off. The chunk size determines how many simulations to run at a time

    from model import run_experiments
    df = auto_run_sets(["test1"], "Data", 10)

### Creating Simulation Configuration

Within model/config/experiment, the experimental_configs dictionary can be modified to add in different experiments. The structure of it is like so:

    experimental_setups = {
        "test1": {
            "config_option_state": "Test",
            "config_option_params": "Test",
            "monte_carlo_n": 1,
            "T": 365,
        }
    }

Where each key represents a set, the config_option_state refers to a specific starting state, config_option_params does the same for parameters, monte_carlo_n defines the number of monte carlo runs, and T defines the number of timesteps for the experiment.

Within model/config/params, the config_option_map is set up to handle the different options for creating parameter sweeps. More detail in the parameters section on specifics.

    config_option_map = {
        "Test": {"System": "Test", "Behaviors": "Test", "Functional": "Test"}
    }

Likewise, within model/config/state, there is a config_option_map for the specific types of starting state assumptions to implement.

    config_option_map = {
        "Test": {
            "Geozones": "Test",
            "Applications": "Test",
            "DAO": "Test",
            "Portals": "Test",
            "Services": "Test",
            "Servicers": "Test",
            "Validators": "Test",
        }
    }


## Parameters

## State
