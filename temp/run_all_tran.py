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


def make_intersection_original(xcs,network,pgraph,N,enum_fc):
    n, fc_list = enum_fc
    clb2_off = set([])
    clb2_on = set([])
    for k in fc_list:
        param = pgraph.parameter(k)
        new_param_OFF, new_param_ON = param_constructer(param, network)
        clb2_off.add(pgraph.index(new_param_OFF))
        clb2_on.add(pgraph.index(new_param_ON))
    off_params, on_params = clb2_off.intersection(xcs), clb2_on.intersection(xcs)
    print("{} of {}".format(n+1,N))
    sys.stdout.flush()
    return off_params,on_params


def main_FC_XC_original(net,num_divisions=100):

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
    working_func = partial(make_intersection_original,XC_query,network,pg,len(workinglist))
    pool = mp.Pool()
    output = list(pool.map(working_func, enumerate(workinglist)))
    clb2_off_FC_XC = set().union(*[o[0] for o in output])
    clb2_on_FC_XC = set().union(*[o[1] for o in output])
    print("OFF clb2 FC to XC complete, {} mutant OFF params".format(len(clb2_off_FC_XC)))
    print("ON clb2 FC to XC complete, {} mutant ON params".format(len(clb2_on_FC_XC)))


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


def main_monoFC_monoXC(net,num_divisions=100):
    print("Monostable FC to monostable XC transition starting")
    with open('monostable_FC_query.json', 'r') as f:
        mono_FC = json.load(f)
    with open('monostable_XC_query.json', 'r') as f:
        mono_XC = json.load(f)
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)


if __name__ == '__main__':
    net = sys.argv[1]
    # main_FC_XC_original(net,num_divisions=100)
    main_FC_XC_double_count(net,num_divisions=100)