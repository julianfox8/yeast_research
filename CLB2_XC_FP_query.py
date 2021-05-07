import DSGRN
import sqlite3
import sys
import json

with open('FC_FP_list.json') as f:
    FC_FP_results = json.load(f)
with open('XC_FP_list.json') as f:
    XC_FP_results = json.load(f)
def param_compare_XC_FP(net):
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    ON_clb2 = []
    OFF_clb2 = []
    XC_FP_keys = [int(i) for i in XC_FP_results.keys()]
    for k in XC_FP_keys:
        param = pg.parameter(k)
        param_logic = param.logic()[3].hex()
        if param_logic == '00':
            OFF_clb2.append(k)
        elif param_logic == '3F':
            ON_clb2.append(k)

    OFF_biXC_results = {}
    for k in XC_FP_results.keys():
        if int(k) in OFF_clb2:
            OFF_biXC_results[k] = XC_FP_results[k]
    ON_biXC_results = {}
    for k in XC_FP_results.keys():
        if int(k) in ON_clb2:
            ON_biXC_results[k] = XC_FP_results[k]

    #with open('../../low_biXC_results.txt', 'w') as f:
        #json.dump(OFF_biXC_results, f)
    #with open('../../high_biXC_results.txt', 'w') as f:
        #json.dump(ON_biXC_results, f)

    print("number of CLB2 ON parameters exhibiting an XC w/ FP:" + str(len(OFF_biXC_results)))
    print("number of CLB2 OFF parameters exhibiting an XC x/ FP:" + str(len(ON_biXC_results)))
    print("number of parameters exhibiting a bistable FC and FP:" + str(len(FC_FP_results)))
    print("number of parameters exhibiting a bistable XC and FP:" + str(len(XC_FP_results)))

if __name__=='__main__':
    net = sys.argv[1]
    param_compare_XC_FP(net)


        