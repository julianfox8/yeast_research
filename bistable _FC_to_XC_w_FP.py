import DSGRN
import sqlite3
import sys
import pickle
import ast
from dsgrn_utilities.parameter_building import construct_parameter

def FC_FP_grabber(db):
    c = sqlite3.connect(db)
    cursor1 = c.cursor()
    FC_results = [ row[0] for row in cursor1.execute('select ParameterIndex from Signatures natural join (select MorseGraphIndex,vertex from (select MorseGraphIndex,vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));')]
    cursor3 = c.cursor()
    bistable_query = [row[0] for row in cursor3.execute("select MorseGraphIndex from (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=2;")]
    bistable_FC_results = set(FC_results).intersection(set(bistable_query))
    cursor2 = c.cursor()
    cursor2.execute('select ParameterIndex, label from Signatures natural join ( select MorseGraphIndex, label from MorseGraphAnnotations where label like "FP%" except select MorseGraphIndex,Source from MorseGraphEdges);')
    FP_fetch = cursor2.fetchall()
    FP_results = {}
    for row in FP_fetch:
        FP_results.setdefault(row[0], []).append(row[1])
    FC_FP_keys = set(bistable_FC_results).intersection(set(FP_results.keys()))
    FC_FP_result = {k:FP_results[k] for k in FC_FP_keys}
    with open('bistable_FC_FP_results.txt', 'wb') as fp:
        pickle.dump(FC_FP_result, fp)
    return FC_FP_result

def XC_FC_FP_grabber(net, result, db):
    c =sqlite3.connect(db)
    clb2_ON = {}
    clb2_OFF = {}
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for key in result:
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
    cursor3 = c.cursor()
    XC_results = [row[0] for row in cursor3.execute('select ParameterIndex from Signatures natural join ( select MorseGraphIndex,vertex from (select MorseGraphIndex,vertex from MorseGraphAnnotations where label="XC {sbf, yhp1, sff, swi5/ace2}" except select MorseGraphIndex,Source from MorseGraphEdges));')]
    clb2_ON_XC_keys = set(XC_results).intersection(set(clb2_ON.keys()))
    clb2_ON_XC = {k:clb2_ON[k] for k in clb2_ON_XC_keys}
    clb2_OFF_XC_keys = set(XC_results).intersection(set(clb2_OFF.keys()))
    clb2_OFF_XC = {k:clb2_OFF[k] for k in clb2_OFF_XC_keys}
    with open('bistable_FC_to_XC_FP_ON.txt', 'wb') as fp:
        pickle.dump(clb2_ON_XC, fp)

    with open('bistabale_FC_to_XC_FP_OFF.txt', 'wb') as fp:
        pickle.dump(clb2_OFF_XC, fp)

if __name__ == '__main__':
    db = sys.argv[1]
    result = FC_FP_grabber(db)
    net = sys.argv[2]
    XC_FC_FP_grabber(net, result,db)

