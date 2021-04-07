

import DSGRN
import sqlite3
import sys
import pickle

#XC_grabber creates a list of all parameters exhibiting a stable XC
#param_compare creates two lists containing the parameters with clb2 OFF and clb2 ON that exhibit a stable XC



def XC_grabber(db):
    c = sqlite3.connect(db)
    cursor = c.cursor()
    query = [ row[0] for row in cursor.execute('select ParameterIndex,Vertex from Signatures natural join ( select MorseGraphIndex,Vertex from MorseGraphAnnotations where label="XC {sbf, yhp1, sff, swi5/ace2}" except select MorseGraphIndex,Source from MorseGraphEdges);')]
    return query

def param_compare(net, query):
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
    with open('clb2_off_data.txt', 'wb') as fp:
        pickle.dump(low_clb2, fp)
    with open('clb2_on_data.txt', 'wb') as fp:
        pickle.dump(hi_clb2, fp)
if __name__=='__main__':
    db = sys.argv[2]
    query = XC_grabber(db)
    net = sys.argv[1]
    param_compare(net, query)


        