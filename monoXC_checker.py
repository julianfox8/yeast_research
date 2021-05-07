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
with open('monostable_query.json') as f:
    monostable_query_result = json.load(f)

def monoXC_FC_check(net):
    mono_FC = set(FC_query_result).intersection(set(monostable_query_result))
    mono_XC = set(XC_query).intersection(set(monostable_query_result))
    clb2_OFF = []
    clb2_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in mono_XC:
        param = pg.parameter(i)
        param_logic = param.logic()[3].hex()
        if param_logic == '00':
            clb2_OFF.append(i)
        elif param_logic == '3F':
            clb2_ON.append(i)

    #with open('ON_monostable_FC_XC_clb.txt', 'w') as f:
        #pickle.dump(clb2_ON_XC, f)
    #with open('OFF_monostable_FC_clb.txt', 'w') as f:
        #pickle.dump(clb2_OFF_XC, f)
    print("number of parameters that exhibit a monostable XC with clb2 ON:" + str(len(clb2_ON)))
    print("number of parameters that exhibit a monostable XC with clb2 OFF:" + str(len(clb2_OFF)))
    print("number of parameters that exhibit a monostable FC :" + str(len(mono_FC)))
    print("number of parameters that exhibit a monostable XC :" + str(len(mono_XC)))
if __name__ == '__main__':
    net = sys.argv[1]
    monoXC_FC_check(net)