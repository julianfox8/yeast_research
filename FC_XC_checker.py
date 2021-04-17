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

def FC_XC_check(net):
    clb2_ON = []
    clb2_OFF = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in FC_query_result:
        param = pg.parameter(i)
        new_param_OFF, new_param_ON = param_constructer(param, network)
        clb2_OFF.append(pg.index(new_param_OFF))
        clb2_ON.append(pg.index(new_param_ON))
    clb2_ON_XC = set(clb2_ON).intersection(XC_query)
    #with open('ON_FC_to_XC_clb2.txt', 'w') as f:
        #pickle.dump(clb2_ON_XC, f)
    clb2_OFF_XC = set(clb2_OFF).intersection(XC_query)
    #with open('OFF_FC_to_XC_clb2.txt', 'w') as f:
        #pickle.dump(clb2_OFF_XC, f)
    print("number of parameters that exhibit a FC to XC with clb2 OFF:" + str(len(clb2_OFF_XC)))
    print("number of parameters that exhibit a FC to XC with clb2 ON:" + str(len(clb2_ON_XC)))

# if __name__ == '__main__':
#     net = sys.argv[1]
#     FC_XC_checker(net)