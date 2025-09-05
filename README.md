# Artifact evaluation of KaDisRedu

In the following, we reproduce the artifacts of the paper[^1] obtained with the [KaDisRedu](https://github.com/jabo17/kadisredu)
However, we would like to address two difficulties regarding reproducibility in advance:

1. Our algorithms are designed for distributed-memory machines which typically requires access to a HPC cluster.
Although one can run our algorithms on a single compute node (single machine), this is not sufficient for investigating communication between processes (PEs) over a network and typically does not allow scaling to 1024 cores as in our experiments.
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
> If neither of those two is an option, you need to provide dependencies manually.
> On most HPC systems, many of them are pre-installed and can be loaded into the active software-stack.

In general, we assume that you have an internet connection to download and install software from the internet.
First, we need to clone this repository.
```bash
# At you machine where you want to run the experiments
git clone https://github.com/jabo17/kadisredu-reproducibility.git --recursive
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
4. Build the competitor [HtWIS](https://github.com/mwis-abc/mwis-source-code)
```bash
sh 04_build_htwis.sh
```

## Download instances

We provide a subset of the graphs as download. If you are interested in the data set, we can provide you the download link.
Moreover, if you are interested in the full data set, please contact us.
```bash
download_link="CONTACT_US"
wget $download_link
tar -xJf mini.tar.xz
mv mini instances
rm mini.tar.xz
```

## Run Experiments

We can now run the experimentes.
Therefore, change your working directory to `experiments/`.
```bash
cd experiments
```
The directory contains all the necessary scripts to run our experiments on your current machine.
We provide in `suites/` the experiment configurations of our experiments which are processed (and run) by [kaval](https://github.com/niklas-uhl/kaval).
kaval generates the `mpiexec` calls and calls them for us for all instances and algorithm configurations.

> [!NOTE]
> We configured the experiments in this repository to run on you local machine to support an easy reproducibility check.
> If you plan to run the experiments on a cluster (multiple machines), you most certainly need to adjust some settings depending on how MPI jobs are started and scheduled on your system.
> If you are unsure about the correct configuration, please don't hesitate to contact us -- we'll be glad to help.

### Run KaDisRedu For Strong Scaling

### Run KaDisRedu For Weak Scaling

Now, we can run our weak scaling experiments.
In the weak scaling experiments, we linearly increase the number of vertices and edges of the input graph with the number of cores.
We investigate three different graph families, using the graph generator [KaGen](https://github.com/KarlsruheGraphGeneration/KaGen).

To run the experiments, execute the following:
```bash
# in experiments/
sh 01_run_kadisredu_weak.sh
```

### Run HtWIS

To run the sequential reduce-and-peel algorithm HtWIS as competitor, run the following:
```bash
# in experiments/
sh 02_run_htwis.sh
```

## Artifacts

After all experiments were performed, we can obtain CSV file which with the most relavant data which were use to support our claims in the paper[^1].
Therefore, change your working directory to `artifacts`.
```bash
cd artifacts
```

### A1 KaDisRedu Srong Scaling

To gather all important metrics from the strong scaling experiments in a CSV, run the following:
```bash
cd strong
sh 00_kadisredu_strong_results_csv.sh # create kadisredu_strong_results.
```

### A2 HtWIS

To obtain the results on the same data set with HtWIS, run the following:
```bash
# in artifacts/strong
sh 01_htwis_results_csv.sh # creates htwis_results.csv
```

### A3 Weak Scaling

To gather all important metrics from the weak scaling experiment in a CSV, run the following:
```bash
cd weak
sh 00_kadisredu_weak_results_csv.sh
```

## References
[^1]: Paper is currently in the review process
