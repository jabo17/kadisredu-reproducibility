#!/usr/bin/env sh

exp_dir=../../experiments/experiment_out/htwis/output
time_limit=7200 # seconds
echo "algo,p,graph,iteration,seed,nodes,kernel_nodes,rel_kernel_nodes,solution_weight,t,failed" > htwis_results.csv
ls $exp_dir/*log.txt |grep -v 'error'|xargs -i sh -c "awk -v f={} -v time_limit=$time_limit -f ../../scripts/extract_htwis.awk {}" >> htwis_results.csv
