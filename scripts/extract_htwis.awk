#!/bin/env awk
# extract_htwis_experiment.awk
# extract htwis data for one graph (one log)

BEGIN{
	OFS=","
  split(f, b, /c0-s/); 
  split(b[2], b, /-log.txt/); 
	iteration=b[1];
} 
/Graph:/{
	split($0, g, "instances/")
  split(g[2], g2, ".gra")
  graph=g2[1]
}
# vertices in input graph
/n = /{
	gsub(/[ |\t]/, "", $0); 
	split($0, a, /[=|;]/); 
	nodes=a[2]
} 
/Finished/{i+=1}
# vertices in kernel graph
/Kernel/{
	split($0, a, ":"); 
	kernel_nodes = a[2]
} 
# solution weight and running time line
/total weight/{
	gsub(" ", "", $0); 
	split($0, a, /[:|,]/); 
	solution=a[2]; 
	t=a[6]/1000 # to seconds
} 

END {
		if(solution > 0){
			failed=0
			# check time limit
			if(time_limit < t) {
				failed=1
			}
			# htwis, seed (placeholder), graph, iteration  (starting with 1), nodes, kernel_nodes, rel_kernel_nodes, solution weight, running time (seconds), failed
			print "htwis",1,graph,iteration,0,nodes,kernel_nodes,kernel_nodes/nodes,solution,t,failed
		}
}
