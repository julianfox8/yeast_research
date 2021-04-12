import json
import sys
import DSGRN
import ast
from dsgrn_utilities.parameter_building import construct_parameter
import pickle


with open('FC_query.txt') as f:
    FC_query_result = json.load(f)
with open('XC_query.txt') as f:
    XC_query = json.load(f)
with open('bistable_query.txt') as f:
    bistable_query = json.load(f)

def bistableFC_bistableXC_checker(net):
    Bistable_FC = set(FC_query_result).intersection(set(bistable_query))
    Bistable_XC = set(XC_query).intersection(set(bistable_query))
    clb2_OFF = []
    clb2_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in Bistable_FC:
        param = pg.parameter(i)
        orders = []
        hex_code = []
        for j in range(network.size()):
            hex_code.append(param.logic()[j].hex())
            orders.append(ast.literal_eval(str(param.order()[j])))
        hex_code[3] = '00'
        new_param_OFF = construct_parameter(network, hex_code, orders)
        clb2_OFF.append(pg.index(new_param_OFF))
        hex_code[3] = '3F'
        new_param_ON = construct_parameter(network, hex_code, orders)
        clb2_ON.append(pg.index(new_param_ON))
    clb2_ON_XC = set(clb2_ON).intersection(Bistable_XC)
    #with open('bistable_FC_XC_clb2.txt', 'w') as f:
        #pickle.dump(clb2_ON_XC, f)
    clb2_OFF_XC = set(clb2_OFF).intersection(Bistable_XC)
    #with open('bistable_FC_XC_clb2.txt', 'w') as f:
        #pickle.dump(clb2_OFF_XC, f)
    print("number of parameters that exhibit a bistable FC to bistable XC with y ON:" + str(len(clb2_ON_XC)))
    print("number of parameters that exhibit a bistable FC to bistable XC with y OFF:" + str(len(clb2_OFF_XC)))

if __name__ == '__main__':
    net = sys.argv[1]
    bistableFC_bistableXC_checker(net)