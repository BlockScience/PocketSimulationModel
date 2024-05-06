# Pocket Cloud Framework

## Introduction

The cloud framework for the Pocket Network Simulation Model was introduced to allow for parallel processing of a large number of monte carlo runs. Built on AWS enabled container runs, this architecture allows for scaling. The write up here is meant to detail the architecture for any future users.

## Model Outline

### model

- The model folder is defined [here](https://github.com/BlockScience/PocketSimulationModel/tree/main/model)

### requirements.txt

- Requirements are defined [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/requirements.txt) and are necessary for the docker container to be built

### AWS Credentials

- **DO NOT SWITCH THE GITIGNORE FROM IGNORING THESE! THESE HAVE GOT TO BE HIDDEN OR ELSE THEY CAN BE STOLEN!**
- These should be at the top level with the file name "aws-credentials.csv"

### The Dockerfile

The dockerfile is defined [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/Dockerfile).

A few notes on what the lines of code do:

<pre>FROM continuumio/miniconda3</pre>

- Creates the base enviroment as miniconda3

<pre>COPY requirements.txt .
RUN pip install -r requirements.txt</pre>

- Copy and install requirements into docker enviroment

<pre>RUN apt-get update
RUN apt-get install curl -y
RUN apt-get install unzip</pre>

- Install some utilities needed for the next step

<pre>RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install</pre>

- Download the AWS CLI into the docker container

<pre>COPY aws-credentials.csv .
COPY model model
COPY data data
COPY cloud_run.py .
COPY configuration_data configuration_data</pre>

- Copy over files

<pre>RUN aws configure import --csv file://aws-credentials.csv</pre>

- Configure the AWS credentials

<pre>ENTRYPOINT ["python", "cloud_run.py"]</pre>

- Set the entrypoint as running the python script "cloud_run.py"


### cloud_run.py

- The cloud_run.py file is defined [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/cloud_run.py)

A few notes on what some of the code does:

<pre>experiments = sys.argv[1:]
df, simulation_kpis = run_experiments(experiments, context=ExecutionMode().single_mode)</pre>
- sys.argv[1:] will grab all the experiments that were passed in (see running the docker container for more)
- The run_experiments takes care of running all experiments

<pre>for key in df["Experiment Name"].unique():
    file_name = open("data/{}.pkl".format(key), "ab")
    pickle.dump(df[df["Experiment Name"] == key], file_name)
    file_name.close()

    file_name = open("data/Simulation-{}.pkl".format(key), "ab")
    pickle.dump(simulation_kpis[simulation_kpis["Experiment Name"] == key], file_name)
    file_name.close()</pre>
    
- This command pickles the results and saves them to the local docker storage

<pre>session = boto3.Session(profile_name="sean")
s3 = session.client("s3")
for key in df["Experiment Name"].unique():
    s3.upload_file(
        "data/{}.pkl".format(key),
        "pocketsimulation",
        "data/{}.pkl".format(key),
    )
    s3.upload_file(
        "data/Simulation-{}.pkl".format(key),
        "pocketsimulation",
        "data/Simulation-{}.pkl".format(key),
    )</pre>
- The commands here upload the resulting files to AWS S3 storage

### Run Experiments Function

- Function is defined [here](https://github.com/BlockScience/PocketSimulationModel/blob/fa7329d7ae52bc514ff65c65f7a6b8b38e0dad76/model/run.py#L239)
- A few of the code blocks to explain in more detail....

<pre>    meta_data = []

    experimental_setup = experimental_setups[experiment_keys[0]]
    state = build_state(experimental_setup["config_option_state"])
    params = build_params(experimental_setup["config_option_params"])
    if params["servicer_service_density_starting"][0]:
        enforce_density_service_servicers(state, params)
    exp = load_config(
        experimental_setup["monte_carlo_n"], experimental_setup["T"], params, state
    )
    meta_data.append(
        [
            experiment_keys[0],
            experimental_setup["config_option_state"],
            experimental_setup["config_option_params"],
        ]
    )</pre>
    
- Build the first experiment with state, parameters, configuration and metadata

<pre>    for key in experiment_keys[1:]:
        experimental_setup = experimental_setups[key]
        state = build_state(experimental_setup["config_option_state"])
        params = build_params(experimental_setup["config_option_params"])
        if params["servicer_service_density_starting"][0]:
            enforce_density_service_servicers(state, params)

        add_config(
            exp,
            experimental_setup["monte_carlo_n"],
            experimental_setup["T"],
            params,
            state,
        )
        meta_data.append(
            [
                key,
                experimental_setup["config_option_state"],
                experimental_setup["config_option_params"],
            ]
        )</pre>
- Do the same for any further experiments, adding them into the configuration

<pre>    raw = run(exp, **kwargs)
    meta_data = pd.DataFrame(
        meta_data, columns=["Experiment Name", "State Set", "Params Set"]
    )

    if disable_postprocessing:
        return raw, None
    else:
        df, simulation_kpis = postprocessing(raw, meta_data)
        return df, simulation_kpis</pre>
- Run and post-process

## Docker Commands

### Building the Container

- For AWS, the container needs to be built like so from the command line in the repository which hosts the dockerfile:

```docker build . -t pocketsimulation --platform linux/x86_64```

- If you are just running locally, you can build like:

```docker build . -t pocketsimulation```

### Running the Container Locally

If we have definitions of runs to be made, the following is the format for running. Let's say we have one defined as "Base" and another as "test1".

-To run one experiment locally do

```docker run -t pocketsimulation Base```

To run two or more for example:

```docker run -t pocketsimulation Base test1```


## AWS Setup

### S3 Storage

- There is an S3 storage instance which will be used to upload simulation results

### Container Registry

- A container registry is in the workspace to hold the latest version of the docker container
- Every time you want to update it, first run the build command, then follow the instructions in the registry for pushing which will allow you to push the container up.

### Elastic Container Service

- An elastic container service is used for running the containers in the cloud
- The PocketRuns cluster is where containers are run out of
- Under task definitions there is Simulation-Run which has the task definition for running the docker container

## Cloud Running Utilities

- The notebook [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/cloud/Run%20Tasks.ipynb) gives a good overview of running the containers.
- The notebook [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/cloud/Download%20KPIs.ipynb) shows how to download the KPIs from the cloud
- The notebook [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/cloud/Download%20Monte%20Carlos.ipynb) shows how to download a given number of monte carlo runs for sanity checking
- The notebook [here](https://github.com/BlockScience/PocketSimulationModel/blob/main/cloud/Full%20Adaptive%20Grid%20Run.ipynb) shows how to do a full adaptive grid run

### create_expected_runs_dataframe_multi

- This function can take a given list of experiment names, populate what runs have not been executed yet (based on the S3 instance), and then return a dataframe of runs to be made.

### queue_and_launch

- This function takes expected runs and launches containers every X minutes (as defined in the parameters)

