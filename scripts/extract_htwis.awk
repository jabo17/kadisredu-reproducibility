#!/bin/env awk
# extract_htwis_experiment.awk
# extract htwis data for one graph (one log)

BEGIN{
	OFS=","
	# obtain graph name
	sub(".*/", "", file);
	split(file, g, "_nokey");
	graph=g[1];
	# iteration counter (repetitions of the experiment with the graph)
	i=0;
} 
# vertices in input graph
/n = /{
	gsub(/[ |\t]/, "", $0); 
	split($0, a, /[=|;]/); 
	result[i]["nodes"]=a[2]
} 
/Finished/{i+=1}
# vertices in kernel graph
/Kernel/{
	split($0, a, ":"); 
	result[i]["kernel_nodes"] = a[2]
} 
# solution weight and running time line
/total weight/{
	gsub(" ", "", $0); 
	split($0, a, /[:|,]/); 
	result[i]["solution"]=a[2]; 
	result[i]["t"]=a[6]/1000 # to seconds
} 


END {
	for(k=0;k<i;k++){
		if(result[k]["solution"] > 0){
			failed=0
			# check time limit
			if(time_limit < result[k]["t"]) {
				failed=1
			}
			# iteration  (starting with 1), nodes, kernel_nodes, rel_kernel_nodes, solution weight, running time (seconds), failed
			print "htwis",1,graph,k+1,0,result[k]["nodes"], result[k]["kernel_nodes"],result[k]["kernel_nodes"]/result[k]["nodes"],result[k]["solution"],result[k]["t"],failed
		}
	}
}
