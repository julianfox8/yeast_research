import json
import sys
import DSGRN
import ast
from dsgrn_utilities.parameter_building import construct_parameter
import pickle

with open('bistable_query.txt') as f:
    bistable_query = json.load(f)
with open('FC_query.txt') as f:
    FC_query_result = json.load(f)
with open('XC_query.txt') as f:
    XC_query = json.load(f)
with open('FP_query.txt') as f:
    FP_results = json.load(f)

def bistableFC_bistableXC_FP_checker(net):
    bistable_FC_results = set(FC_query_result).intersection(set(bistable_query))
    FC_FP_keys = set(bistable_FC_results).intersection(set(FP_results.keys()))
    FC_FP_result = {k:FP_results[k] for k in FC_FP_keys}
    clb2_ON = {}
    clb2_OFF = {}
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for key in FC_FP_result:
        param = pg.parameter(key)
        orders = []
        hex_code = []
        for j in range(network.size()):
            hex_code.append(param.logic()[j].hex())
            orders.append(ast.literal_eval(str(param.order()[j])))
        hex_code[3] = '00'
        new_param_OFF = construct_parameter(network, hex_code, orders)
        clb2_OFF.update({pg.index(new_param_OFF): []})
        clb2_OFF[pg.index(new_param_OFF)].append(key)
        clb2_OFF[pg.index(new_param_OFF)].append(result[key])
        hex_code[3] = '3F'
        new_param_ON = construct_parameter(network, hex_code, orders)
        clb2_ON.update({pg.index(new_param_ON): []})
        clb2_ON[pg.index(new_param_ON)].append(key)
        clb2_ON[pg.index(new_param_ON)].append(result[key])
    bistable_XC_results = set(XC_query).intersection(set(bistable_query))
    clb2_ON_XC_keys = set(bistable_XC_results).intersection(set(clb2_ON.keys()))
    clb2_ON_XC = {k:clb2_ON[k] for k in clb2_ON_XC_keys}
    clb2_OFF_XC_keys = set(bistable_XC_results).intersection(set(clb2_OFF.keys()))
    clb2_OFF_XC = {k:clb2_OFF[k] for k in clb2_OFF_XC_keys}
    #with open('../../bistable_FC_to_XC_FP_ON.txt', 'w') as f:
        #pickle.dump(y_ON_XC, f)
    #with open('../../bistable_FC_to_XC_FP_OFF.txt', 'w') as f:
        #pickle.dump(y_OFF_XC, f)
    print("number of parameters that exhibit a bistable FC to bistable XC with FP where is y ON:" + str(len(clb2_ON_XC)))
    print("number of parameters that exhibit a bistable FC to bistable XC with FP where is y OFF:" + str(len(clb2_OFF_XC)))
    clb2_OFF_FP = {}
    clb2_ON_FP = {}
    OFF_matching_keys = set(clb2_OFF_XC.keys()).intersection(set(FP_results.keys()))
    for k in OFF_matching_keys:
        clb2_OFF_FP[k] = [FP_results[k],clb2_OFF[k]]
    clb2_OFF_XC_FC = []
    for key, val in clb2_OFF_FP.items():
        OFF_P = val[0]
        OFF_FC_P = val[1][1]
        if set(OFF_P) == set(OFF_FC_P):
            clb2_OFF_XC_FC.extend(OFF_P)
    #with open('test_OFF_XC_FP_FC.txt', 'w') as f:
        #json.dump(y_OFF_FP, f)
    ON_matching_keys = set(clb2_ON_XC.keys()).intersection(set(FP_results.keys()))
    for k in ON_matching_keys:
        clb2_ON_FP[k] = [FP_results[k],clb2_ON[k]]
    clb2_ON_XC_FC = []
    for key, val in clb2_ON_FP.items():
        ON_P = val[0]
        ON_FC_P = val[1][1]
        if set(ON_P) == set(ON_FC_P):
            clb2_ON_XC_FC.extend(ON_P)
    #with open('test_ON_XC_FP_FC.txt', 'w') as f:
        #json.dump(y_ON_FP, f)
    print("number of parameters that exhibit a bistable FC to bistable XC with the same FP where is y ON:" + str(len(clb2_ON_XC_FC)))
    print("number of parameters that exhibit a bistable FC to bistable XC with the same FP where is y OFF:" + str(len(clb2_OFF_XC_FC)))

if __name__ == '__main__':
    net = sys.argv[1]
    bistableFC_bistableXC_FP_checker(net)