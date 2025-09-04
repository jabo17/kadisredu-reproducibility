# Artifact evaluation of KaDisRedu

In the following, we reproduce the artifacts of the paper[^1] obtained with the implementation[^2].
However, we would like to address two difficulties regarding reproducibility in advance:

1. Our algorithms are designed for distributed-memory machines which typically requires access to a HPC cluster.
Although one can run our algorithms on a single compute node (single machine), this is not sufficient for investigating communication between processes (PEs) over a network and typically does not allow scaling to 1024 cores.
Morover, running distributed algorithms on an HPC cluster and evaluating their results with a "one-click"-script is typically impossible.
From our experience, HPC cluster jobs are failing from time to time with unknown reason for the callee.
Still, we aim to provide you a setup which comes close to a "one-click"-script.
2. Our set of benchmark instances (graphs) requires a lot of storage, and therefore cannot be made easily publicly available for download.
To that end, we provide only a subset of them. 

## Setup Experiment Environment

> [!NOTE]
We used the HPC cluster HoreKa for our experiments.
Each compute node is equipped with two Intel Xeon Platinum 8368 processors with 38 cores each and 256 GB of main memory.
Compute nodes are connected by a InfiniBand 4X HDR 200 GBit/s interconnect.
All algorithms are implemented in C++ and compiled using NGU GCC13.
For interprocess communication, we use IntelMPI 2021.11 and the MPI-wrapper KaMPIng.

> [!TIP]
> To simplify the installation process on a single machine we provide a docker container and for HoreKA a module environment, respectively.
> If neither of those two is an option, you need to provide dependencies yourself.
> On most HPC systems, many of them are pre-installed and can be loaded into the active software-stack.

In general, we assume that you have an internet connection to download and install software from the internet.
First, we need to clone this repository.
```bash
# At you machine where you want to run the experiments
git clone https://github.com/jabo17/kadisredu-reproducibility.git
```

Afterwards, follow one of the three options:
### 1. Method: Provide the dependencies manually

#### 1.1 Dependencies
- CMake 3.30 or higher
- GNU G++13 or higher
- IntelMPI 2021.11 or higher
- Intel TBB 2021.4.0 or higher
- libsparsehash (Google Sparsehash)
- GNU patch 2.7.6

#### 1.2 Evaluation Software-Stack
The following packages are required for evaluation
- Python and Pipenv
- Texlive
- AWK

### 2. Method: HoreKa
If you are using HoreKa, the dependencies to run the experiments can be provided via `module`.
```bash
# At HoreKa login node
cd kadisredu-reproducibility
cp horeka/modules_kadisredu.hk ~/.config/lmod/
# to load the software
module restore modules_kadisredu
```

We evaluate the experiments our local machine.
Therefore, the experiment output must be downloaded.

To evaluate the experiments, ensure that you have installed the software from [1.2 Evaluation Software-Stack](#12-evaluation-software-stack).
Rather than installing the evaluation software-stack manually, you can also run the docker image as described in [3. Method](#3-method-docker-single-machine).

### 3. Method: Docker (Single Machine)
1. Go into `kadisredu-reproducibility`
```bash
cd kadisredu-reproducibility
```
1. Pull the docker image
```bash
sh 00_pull_docker_image.sh
```
2. Run the docker image with the current directory as working directory
```bash
sh 01_run_docker_container.sh
```

## Build Benchmark
1. Fetch KaDisRedu and HtWIS
```bash
sh 02_fetch_algorithms.sh
```
3. Build KaDisRedu
```bash
sh 03_build_kadisredu.sh
```
4. Build HtWIS
```bash
sh 04_build_htwis.sh
```

## Run Experiments


### Run KaDisRedu For Strong Scaling

### Run KaDisRedu For Weak Scaling

### Run HtWIS

## Artifacts

### A1 Reduction Impact

### A2 Reduction Time

### A3 Comparison With HtWIS

### A4 Weak Scaling

## Evaluate Experiments To Obtain Artifacts


## References
[^1]: TODO Link to the paper
[^2]: TODO Link to repository
