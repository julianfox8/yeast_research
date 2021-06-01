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

def FP_check(k, pgraph):
    label = []
    p = pgraph.parameter(k)
    dg = DSGRN.DomainGraph(p)
    mg = DSGRN.MorseGraph(dg)
    for k in range(mg.poset().size()):
        a = ast.literal_eval(str(mg.annotation(k).stringify()))
        if a[0].startswith('FP '):
            label.append(a)
    return label



def make_intersection_label(xcs,network,pgraph,N,enum_fc):
    n, fc_list = enum_fc
    clb2_off = 0
    clb2_on = 0
    for k in fc_list:
        param = pgraph.parameter(k)
        fc_fp_label = FP_check(k,pgraph)
        new_param_OFF, new_param_ON = param_constructer(param, network)
        OFF_label = FP_check(pgraph.index(new_param_OFF), pgraph)
        ON_label = FP_check(pgraph.index(new_param_ON), pgraph)
        if pgraph.index(new_param_OFF) in xcs and OFF_label==fc_fp_label:
            clb2_off += 1
        if pgraph.index(new_param_ON) in xcs and ON_label==fc_fp_label:
            clb2_on +=1
    print("{} of {}".format(n+1,N))
    sys.stdout.flush()
    return clb2_off,clb2_on



def main_biFC_biXC_same_FP_label(net,num_divisions=100):
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
    working_func = partial(make_intersection_label, bi_XC, network,pg, len(workinglist))
    pool = mp.Pool()
    output = list(pool.map(working_func, enumerate(workinglist)))
    clb2_off_bi_FC_XC = sum([o[0] for o in output])
    clb2_on_bi_FC_XC = sum([o[1] for o in output])
    print("OFF clb2 bi FC/FP to XC/FP complete, {} mutant OFF params".format(clb2_off_bi_FC_XC))
    print("ON clb2 bi FC/FP to XC/FP complete, {} mutant ON params".format(clb2_on_bi_FC_XC))

if __name__ == '__main__':
    net = sys.argv[1]
    main_biFC_biXC_same_FP_label(net, num_divisions=100)