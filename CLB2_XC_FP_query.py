import DSGRN
import sqlite3
import sys
import json


with open('XC_query.json') as f:
    XC_query = json.load(f)
with open('FP_query.json') as f:
    FP_results = json.load(f)
with open('bistable_query.json') as f:
    bistable_query = json.load(f)

    
def param_compare_XC_FP(net):
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    low_clb2 = []
    hi_clb2 = []
    for i in XC_query:
        param = pg.parameter(i)
        param_logic = param.logic()[3].hex()
        if param_logic == '00':
            low_clb2.append(i)
        elif param_logic == '3F':
            hi_clb2.append(i)
    low_biXC_results = set(low_clb2).intersection(set(bistable_query))
    low_XC_FP_keys = set(low_biXC_results).intersection(set(FP_results.keys()))
    low_XC_FP_result = {k:FP_results[k] for k in low_XC_FP_keys}


    high_biXC_results = set(hi_clb2).intersection(set(bistable_query))
    high_XC_FP_keys = set(high_biXC_results).intersection(set(FP_results.keys()))
    high_XC_FP_result = {k:FP_results[k] for k in high_XC_FP_keys}

    with open('../../low_XC_FP_result.txt', 'w') as f:
        json.dump(low_XC_FP_result, f)
    with open('../../high_XC_FP_result.txt', 'w') as f:
        json.dump(high_XC_FP_result, f)
    print("number of CLB2 ON parameters exhibiting a bistable XC:" + str(len(low_biXC_results)))
    print("number of CLB2 ON parameters exhibiting an XC w/ FP:" + str(len(low_XC_FP_result)))
    print("number of CLB2 OFF parameters exhibiting a bistable XC:" + str(len(high_biXC_results)))
    print("number of CLB2 OFF parameters exhibiting an XC x/ FP:" + str(len(high_XC_FP_result)))

if __name__=='__main__':
    net = sys.argv[1]
    param_compare_XC_FP(net)


        
