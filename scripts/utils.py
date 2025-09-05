#!/bin/env python

import numpy as np
import sys
import os
import json
import yaml
import argparse
from pathlib import Path
import re

def extract_iteration_from_filename(s):
    match = re.search(r"-s(\d+)_", s)
    if match:
        return int(match.group(1))
    return None  # or raise an error, or return a default value

def extract_config_idx_from_filename(s):
    match = re.search(r"-c(\d+)-", s)
    if match:
        return int(match.group(1))
    return None  # or raise an error, or return a default value

def shorten_filename_name(filename: str):
    return Path(filename).stem

def extract_instance_name(kagen_option_string: str, weak=False, cores=1) -> str:
    if ";" not in kagen_option_string:
        # plain filename
        return kagen_option_string

    def unpack_param_pair(param_pair: str, delimiter="="):
        assert delimiter in param_pair, param_pair
        return param_pair.split(delimiter)

    subcommand, remainder = kagen_option_string.split(";", 1)
    params = remainder.split(";")
    params = [unpack_param_pair(key_value_pair) for key_value_pair in params]
    params = {k:v for [k,v] in params}

    if subcommand == "file":
        assert "filename" in params.keys()
        return shorten_filename_name(params["filename"])
    elif subcommand.startswith("type"):
        subcommand = subcommand.split("=")[1]
        result=subcommand

        n = int(params["n"])
        m = int(params["m"])
        if weak:
            n = int(np.log2(n/cores))
            m = int(np.log2(m/cores))
            result += "-N%s-M%s" % (n, m)
        else:
            result += "-n%s-m%s" % (n, m)

        if subcommand == "rhg":
            result += '-g%s' % params["gamma"]
        return result
    else:
        assert False, "subcommand not supported yet"
        # graph generator

def extract_max_time(obj, query, default=0.0):
    if "." not in query:
        try:
            return obj[query]["statistics"]["max"][0]
        except KeyError:
            return default
    else:
        [field, remainder]  = query.split(".", 1)
        try:
            return extract_max_time(obj[field], remainder, default)
        except KeyError:
            return default


def extract_fields(obj: dict, time_limit, weak=False) -> dict:
    """
    Extract row from json object holding experimental results
    """

    ctx = obj["solver"]["context"]
    red_ctx = ctx["red_ctx"]
    last_red_phase = len(red_ctx)-1

    t_partition = sum([extract_max_time(obj, "timer.KaDisRedu.reduce.R"+str(i)+".build-distributed-dynamic-graph.partition") for i in range(len(red_ctx))])
    t_build_graph = sum([extract_max_time(obj, "timer.KaDisRedu.reduce.R"+str(i)+".build-distributed-dynamic-graph") for i in range(len(red_ctx))])

    if last_red_phase >= 0:
        cut = obj["solver"]["R0"]["graph"]["cut"]
        nodes = obj["solver"]["R0"]["graph"]["nodes"]
        edges = obj["solver"]["R0"]["graph"]["edges"]
        kernel_nodes = obj["solver"]["R"+str(last_red_phase)]["reducer"]["kernel_graph"]["nodes"]
        kernel_edges = obj["solver"]["R"+str(last_red_phase)]["reducer"]["kernel_graph"]["edges"]
        rel_kernel_nodes = kernel_nodes/nodes
        rel_kernel_edges = kernel_edges/edges
    else:
        # plain greedy
        cut = obj["solver"]["greedy"]["graph"]["cut"]
        nodes = obj["solver"]["greedy"]["graph"]["nodes"]
        edges = obj["solver"]["greedy"]["graph"]["edges"]
        kernel_nodes = nodes
        kernel_edges = edges
        rel_kernel_nodes = 1.0
        rel_kernel_edges = 1.0

    t = extract_max_time(obj, "timer.KaDisRedu")

    return {
            "graph": extract_instance_name(ctx["kagen_option_string"], weak=weak, cores=ctx["np"]),
            "p" : ctx["np"],
            "seed" : ctx["seed"],
            "solution_weight" : obj["solver"]["solution_weight"],
            # overall time used by KaDisRedu
            "t" : t,
            # reduce phase (including building and partitioning the graph)
            "t_reduce" : extract_max_time(obj, "timer.KaDisRedu.reduce"),
            # reduce phase (without graph partitioner)
            #"t_reduce_without_partition" : extract_max_time(obj, "timer.KaDisRedu.reduce") - t_partition, 
            #"t_partition" : t_partition,
            #"t_build_graph" : t_build_graph,
            #"t_greedy" : extract_max_time(obj, "timer.KaDisRedu.greedy"),
            "kernel_nodes": kernel_nodes,
            "rel_kernel_nodes": rel_kernel_nodes,
            "kernel_edges": kernel_edges,
            "rel_kernel_edges": rel_kernel_edges,
            "nodes": nodes,
            "edges": edges,
            "cut": cut,
            "failed": (t > time_limit)
    }
