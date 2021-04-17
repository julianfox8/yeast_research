import DSGRN
import sqlite3
import sys
import json


with open('XC_query.txt') as f:
    XC_query = json.load(f)



def param_compare(net):
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    low_clb2 = []
    hi_clb2 = []
    for i in query:
        param = pg.parameter(i)
        param_logic = param.logic()[3].hex()
        if param_logic == '00':
            low_clb2.append(i)
        elif param_logic == '3F':
            hi_clb2.append(i)
    #with open('../../clb2_off_data.txt', 'w') as f:
        #json.dump(low_clb2, fp)
    #with open('../../clb2_on_data.txt', 'w') as f:
        #json.dump(hi_clb2, f)
    print("number of CLB2 ON parameters exhibiting an XC:" + str(len(hi_clb2)))
    print("number of CLB2 OFF parameters exhibiting an XC:" + str(len(low_clb2))


if __name__=='__main__':
    net = sys.argv[1]
    param_compare(net)


        
