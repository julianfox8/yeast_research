import DSGRN
import sqlite3
import pickle
import ast
from dsgrn_utilities.parameter_building import construct_parameter
import sys

#net = '~/DSGRN/yeast_cc/networks/WT_clb2_nonE.txt'
#db = '~/DSGRN/yeast_cc/networks/WT_clb2_nonE.db'

def FC_XC_checker(db, net):
    c = sqlite3.connect(db)
    cursor1 = c.cursor()
    cursor3 = c.cursor()
    bistable_query = [ row[0] for row in cursor3.execute("select MorseGraphIndex from (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=2;")]
    FC_query_result = [ row[0] for row in cursor1.execute('select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));')]
    Bistable_FC = set(FC_query_result).intersection(set(bistable_query))
    cursor2 = c.cursor()
    XC_query = [ row[0] for row in cursor2.execute('select ParameterIndex,Vertex from Signatures natural join ( select MorseGraphIndex,Vertex from MorseGraphAnnotations where label="XC {sbf, yhp1, sff, swi5/ace2}" except select MorseGraphIndex,Source from MorseGraphEdges);')]
    Bistable_XC =set(XC_query).intersection(set(bistable_query))
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
    with open('CLB2_ON_bistable_FC_XC.txt', 'wb') as fp:
        pickle.dump(clb2_ON_XC, fp)
    clb2_OFF_XC = set(clb2_OFF).intersection(Bistable_XC)
    with open('CLB2_OFF_bistable_FC_XC.txt', 'wb') as fp:
        pickle.dump(clb2_OFF_XC, fp)

if __name__ == '__main__':
    net = sys.argv[2]
    db = sys.argv[1]
    FC_XC_checker(db, net)