import json
import sys
import DSGRN
import sqlite3
import ast
from dsgrn_utilities.parameter_building import construct_parameter
import pickle 

with open('FC_query_test.txt') as f:
    FC_query_result = json.load(f)
with open('XC_query_test.txt') as f:
    XC_query = json.load(f)
with open('monostable_query_test.txt') as f:
    monostable_query_result = json.load(f)
with open('bistable_query_test.txt') as f:
    bistable_query = json.load(f)
with open('FP_query_test.txt') as f:
    FP_results = json.load(f)

def FC_XC_checker(net):
    y_OFF = []
    y_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in FC_query_result:
        param = pg.parameter(i)
        orders = []
        hex_code = []
        for j in range(network.size()):
            hex_code.append(param.logic()[j].hex())
            orders.append(ast.literal_eval(str(param.order()[j])))
        hex_code[1] = '0'
        new_param_OFF = construct_parameter(network, hex_code, orders)
        y_OFF.append(pg.index(new_param_OFF))
        hex_code[1] = 'F'
        new_param_ON = construct_parameter(network, hex_code, orders)
        y_ON.append(pg.index(new_param_ON))
    y_ON_XC = set(y_ON).intersection(XC_query)
    #with open('ON_FC_to_XC_test.txt', 'w') as f:
        #pickle.dump(y_ON_XC, f)
    y_OFF_XC = set(y_OFF).intersection(XC_query)
    #with open('OFF_FC_to_XC_test.txt', 'w') as f:
        #pickle.dump(y_OFF_XC, f)
    print("number of parameters that exhibit a FC to XC with y OFF:" + str(len(y_OFF_XC)))
    print("number of parameters that exhibit a FC to XC with y ON:" + str(len(y_ON_XC)))
def monoFC_monoXC_checker(net):
    monostable_FC_results = set(FC_query_result).intersection(set(monostable_query_result))
    monostable_XC_results = set(XC_query).intersection(set(monostable_query_result))
    y_OFF = []
    y_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in monostable_FC_results:
        param = pg.parameter(i)
        orders = []
        hex_code = []
        for j in range(network.size()):
            hex_code.append(param.logic()[j].hex())
            orders.append(ast.literal_eval(str(param.order()[j])))
        hex_code[1] = '0'
        new_param_OFF = construct_parameter(network, hex_code, orders)
        y_OFF.append(pg.index(new_param_OFF))
        hex_code[1] = 'F'
        new_param_ON = construct_parameter(network, hex_code, orders)
        y_ON.append(pg.index(new_param_ON))
    y_ON_XC = set(y_ON).intersection(monostable_XC_results)
    #with open('ON_monostable_FC_XC_test.txt', 'w') as f:
        #pickle.dump(y_ON_XC, f)
    y_OFF_XC = set(y_OFF).intersection(monostable_XC_results)
    #with open('OFF_monostable_FC_test.txt', 'w') as f:
        #pickle.dump(y_OFF_XC, f)
    print("number of parameters that exhibit a monostable FC to monostable XC with y ON:" + str(len(y_ON_XC)))
    print("number of parameters that exhibit a monostable FC to monostable XC with y OFF:" + str(len(y_OFF_XC)))
def bistableFC_bistableXC_checker(net):
    Bistable_FC = set(FC_query_result).intersection(set(bistable_query))
    Bistable_XC = set(XC_query).intersection(set(bistable_query))
    y_OFF = []
    y_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in Bistable_FC:
        param = pg.parameter(i)
        orders = []
        hex_code = []
        for j in range(network.size()):
            hex_code.append(param.logic()[j].hex())
            orders.append(ast.literal_eval(str(param.order()[j])))
        hex_code[1] = '0'
        new_param_OFF = construct_parameter(network, hex_code, orders)
        y_OFF.append(pg.index(new_param_OFF))
        hex_code[1] = 'F'
        new_param_ON = construct_parameter(network, hex_code, orders)
        y_ON.append(pg.index(new_param_ON))
    y_ON_XC = set(y_ON).intersection(Bistable_XC)
    #with open('bistable_FC_XC_test.txt', 'w') as f:
        #pickle.dump(y_ON_XC, f)
    y_OFF_XC = set(y_OFF).intersection(Bistable_XC)
    #with open('bistable_FC_XC_test.txt', 'w') as f:
        #pickle.dump(y_OFF_XC, f)
    print("number of parameters that exhibit a bistable FC to bistable XC with y ON:" + str(len(y_ON_XC)))
    print("number of parameters that exhibit a bistable FC to bistable XC with y OFF:" + str(len(y_OFF_XC)))
def bistableFC_bistableXC_FP_checker(net):
    bistable_FC_results = set(FC_query_result).intersection(set(bistable_query))
    FC_FP_keys = set(bistable_FC_results).intersection(set(FP_results.keys()))
    FC_FP_result = {k:FP_results[k] for k in FC_FP_keys}
    y_ON = {}
    y_OFF = {}
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for key in FC_FP_result:
        param = pg.parameter(key)
        orders = []
        hex_code = []
        for j in range(network.size()):
            hex_code.append(param.logic()[j].hex())
            orders.append(ast.literal_eval(str(param.order()[j])))
        hex_code[1] = '0'
        new_param_OFF = construct_parameter(network, hex_code, orders)
        y_OFF.update({pg.index(new_param_OFF): []})
        y_OFF[pg.index(new_param_OFF)].append(key)
        y_OFF[pg.index(new_param_OFF)].append(result[key])
        hex_code[1] = 'F'
        new_param_ON = construct_parameter(network, hex_code, orders)
        y_ON.update({pg.index(new_param_ON): []})
        y_ON[pg.index(new_param_ON)].append(key)
        y_ON[pg.index(new_param_ON)].append(result[key])
    bistable_XC_results = set(XC_query).intersection(set(bistable_query))
    y_ON_XC_keys = set(bistable_XC_results).intersection(set(y_ON.keys()))
    y_ON_XC = {k:y_ON[k] for k in y_ON_XC_keys}
    y_OFF_XC_keys = set(bistable_XC_query).intersection(set(y_OFF.keys()))
    y_OFF_XC = {k:y_OFF[k] for k in y_OFF_XC_keys}
    #with open('../../bistable_FC_to_XC_FP_ON_test.txt', 'w') as f:
        #pickle.dump(y_ON_XC, f)
    #with open('../../bistable_FC_to_XC_FP_OFF_test.txt', 'w') as f:
        #pickle.dump(y_OFF_XC, f)
    print("number of parameters that exhibit a bistable FC to bistable XC with FP where is y ON:" + str(len(y_ON_XC)))
    print("number of parameters that exhibit a bistable FC to bistable XC with FP where is y OFF:" + str(len(y_OFF_XC)))
    y_OFF_FP = {}
    y_ON_FP = {}
    OFF_matching_keys = set(y_OFF_XC.keys()).intersection(set(FP_results.keys()))
    for k in OFF_matching_keys:
        y_OFF_FP[k] = [FP_results[k],y_OFF[k]]
    y_OFF_XC_FC = []
    for key, val in y_OFF_FP.items():
        OFF_P = val[0]
        OFF_FC_P = val[1][1]
        if set(OFF_P) == set(OFF_FC_P):
            y_OFF_XC_FC.extend(OFF_P)
    #with open('test_OFF_XC_FP_FC.txt', 'w') as f:
        #json.dump(y_OFF_XC_FC, f)
    ON_matching_keys = set(y_ON_XC.keys()).intersection(set(FP_results.keys()))
    for k in ON_matching_keys:
        y_ON_FP[k] = [FP_results[k],y_ON[k]]
    y_ON_XC_FC = []
    for key, val in y_ON_FP.items():
        ON_P = val[0]
        ON_FC_P = val[1][1]
        if set(ON_P) == set(ON_FC_P):
            y_ON_XC_FC.extend(ON_P)
    #with open('test_ON_XC_FP_FC.txt', 'w') as f:
        #json.dump(y_ON_XC_FC, f)
    print("number of parameters that exhibit a bistable FC to bistable XC with the same FP where is y ON:" + str(len(y_ON_XC_FC)))
    print("number of parameters that exhibit a bistable FC to bistable XC with the same FP where is y OFF:" + str(len(y_OFF_XC_FC)))

if __name__ == '__main__':
    net = sys.argv[1]
    FC_XC_checker(net)
    monoFC_monoXC_checker(net)
    bistableFC_bistableXC_checker(net)
    bistableFC_bistableXC_FP_checker(net)
