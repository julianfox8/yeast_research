import pickle
import sys
import DSGRN
import sqlite3
import ast
from dsgrn_utilities.parameter_building import construct_parameter

def FC_XC_checker(db, net):
    c = sqlite3.connect(db)
    cursor1 = c.cursor()
    FC_query_result = [ row[0] for row in cursor1.execute('select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));')]
    cursor3 = c.cursor()
    monostable_query_result = [row[0] for row in cursor3.execute("select MorseGraphIndex from (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=1;")]
    cursor2 = c.cursor()
    monostable_FC_results = set(FC_query_result).intersection(set(monostable_query_result))
    XC_query = [ row[0] for row in cursor2.execute('select ParameterIndex,Vertex from Signatures natural join ( select MorseGraphIndex,Vertex from MorseGraphAnnotations where label="XC {sbf, yhp1, sff, swi5/ace2}" except select MorseGraphIndex,Source from MorseGraphEdges);')]
    monostable_XC_results = set(XC_query).intersection(set(monostable_query_result))
    clb2_OFF = []
    clb2_ON = []
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    for i in monostable_FC_results:
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

    clb2_ON_XC = set(clb2_ON).intersection(monostable_XC_results)
    with open('CLB2_ON_monostable_FC_XC.txt', 'wb') as fp:
        pickle.dump(clb2_ON_XC, fp)
    clb2_OFF_XC = set(clb2_OFF).intersection(monostable_XC_results)
    with open('CLB2_OFF_monostable_FC.txt_XC', 'wb') as fp:
        pickle.dump(clb2_OFF_XC, fp)

if __name__ == '__main__':
    net = sys.argv[2]
    db = sys.argv[1]
    FC_XC_checker(db, net)