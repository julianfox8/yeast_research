import json
import sys
import DSGRN
import ast
from dsgrn_utilities.parameter_building import construct_parameter
import pickle
from parameter_constructer import param_constructer


with open('FC_query.json') as f:
    FC_query_result = json.load(f)
with open('XC_query.json') as f:
    XC_query = json.load(f)
with open('bistable_query.json') as f:
    bistable_query = json.load(f)

with open('XC_FP_list.json') as f:
    XC_FP_results = json.load(f)
with open('FC_FP_list.json') as f:
    FC_FP_results = json.load(f)

def bistableFC_bistableXC_check(net):
    FC_FP_keys = [int(i) for i in FC_FP_results.keys()]
    clb2_OFF = []
    clb2_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in FC_FP_keys:
        param = pg.parameter(i)
        new_param_OFF, new_param_ON = param_constructer(param, network)
        clb2_OFF.append(pg.index(new_param_OFF))
        clb2_ON.append(pg.index(new_param_ON))
    OFF_biXC_results = {}
    for k in XC_FP_results.keys():
        if int(k) in clb2_OFF:
            OFF_biXC_results[k] = XC_FP_results[k]
    ON_biXC_results = {}
    for k in XC_FP_results.keys():
        if int(k) in clb2_ON:
            ON_biXC_results[k] = XC_FP_results[k]
    print("number of parameters that exhibit a bistable FC to bistable XC with CLB2 ON:" + str(len(ON_biXC_results)))
    print("number of parameters that exhibit a bistable FC to bistable XC with CLB2 OFF:" + str(len(OFF_biXC_results)))

if __name__ == '__main__':
    net = sys.argv[1]
    bistableFC_bistableXC_check(net)