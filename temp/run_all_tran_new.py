import json
from math import floor
import sys, time, ast
import DSGRN
from dsgrn_utilities.parameter_building import construct_parameter
import multiprocessing as mp
from functools import partial


def param_constructer(param, network):
    orders = []
    hex_code = []
    for j in range(network.size()):
        hex_code.append(param.logic()[j].hex())
        orders.append(ast.literal_eval(str(param.order()[j])))
    hex_code[3] = '00'
    new_param_OFF = construct_parameter(network, hex_code, orders)
    hex_code[3] = '3F'
    new_param_ON = construct_parameter(network, hex_code, orders)
    return (new_param_OFF, new_param_ON)


def make_intersection_double_count(xcs,network,pgraph,N,enum_fc):
    n, fc_list = enum_fc
    clb2_off = 0
    clb2_on = 0
    for k in fc_list:
        param = pgraph.parameter(k)
        new_param_OFF, new_param_ON = param_constructer(param, network)
        if pgraph.index(new_param_OFF) in xcs:
            clb2_off += 1
        if pgraph.index(new_param_ON) in xcs:
            clb2_on +=1
    print("{} of {}".format(n+1,N))
    sys.stdout.flush()
    return clb2_off,clb2_on


def main_FC_XC_double_count(net,num_divisions=100):

    print("FC to XC transition starting")
    with open('FC_query.json', 'r') as f:
        FC_query = json.load(f)
    with open('XC_query.json', 'r') as f:
        XC_query = json.load(f)
    # CLB ON/OFF can't have FCs, use that fact to make the XC list smaller
    XC_query = set(XC_query).difference(FC_query)
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)

    chunk = floor(len(FC_query)/num_divisions)
    workinglist = [FC_query[k:k + chunk] for k in range(0, len(FC_query), chunk)]
    working_func = partial(make_intersection_double_count,XC_query,network,pg,len(workinglist))
    pool = mp.Pool()
    output = list(pool.map(working_func, enumerate(workinglist)))
    clb2_off_FC_XC = sum([o[0] for o in output])
    clb2_on_FC_XC = sum([o[1] for o in output])
    print("OFF clb2 FC to XC complete, {} mutant OFF params".format(clb2_off_FC_XC))
    print("ON clb2 FC to XC complete, {} mutant ON params".format(clb2_on_FC_XC))

def main_monoFC_monoXC_double_count(net,num_divisions=100):
    print("Monostable FC to monostable XC transition starting")
    with open('monostable_FC_query.json', 'r') as f:
        mono_FC = json.load(f)
    with open('monostable_XC_query.json', 'r') as f:
        mono_XC = json.load(f)
    mono_XC = set(mono_XC).difference(mono_FC)
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)

    chunk = floor(len(mono_FC)/num_divisions)
    workinglist = [mono_FC[k:k + chunk] for k in range(0, len(mono_FC), chunk)]
    working_func = partial(make_intersection_double_count, mono_XC, network,pg, len(workinglist))
    pool = mp.Pool()
    output = list(pool.map(working_func, enumerate(workinglist)))
    clb2_off_mono_FC_XC = sum([o[0] for o in output])
    clb2_on_mono_FC_XC = sum([o[1] for o in output])
    print("OFF clb2 mono FC to XC complete, {} mutant OFF params".format(clb2_off_mono_FC_XC))
    print("ON clb2 mono FC to XC complete, {} mutant ON params".format(clb2_on_mono_FC_XC))

def main_biFC_biXC_double_count(net,num_divisions=100):
    print("Bistable FC/FP to Bistable XC/FP transition starting")
    with open('bistable_FC_FP_query.json', 'r') as f:
        bi_FC = json.load(f)
    with open('bistable_XC_FP_query.json', 'r') as f:
        bi_XC = json.load(f)
    bi_XC = set(bi_XC).difference(bi_FC)
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)

    chunk = floor(len(bi_FC)/num_divisions)
    workinglist = [bi_FC[k:k + chunk] for k in range(0, len(bi_FC), chunk)]
    working_func = partial(make_intersection_double_count, bi_XC, network,pg, len(workinglist))
    pool = mp.Pool()
    output = list(pool.map(working_func, enumerate(workinglist)))
    clb2_off_bi_FC_XC = sum([o[0] for o in output])
    clb2_on_bi_FC_XC = sum([o[1] for o in output])
    print("OFF clb2 bi FC/FP to XC/FP complete, {} mutant OFF params".format(clb2_off_bi_FC_XC))
    print("ON clb2 bi FC/FP to XC/FP complete, {} mutant ON params".format(clb2_on_bi_FC_XC))

if __name__ == '__main__':
    net = sys.argv[1]
    main_FC_XC_double_count(net,num_divisions=100)
    main_monoFC_monoXC_double_count(net,num_divisions=100)
    main_biFC_biXC_double_count(net, num_divisions=100)
