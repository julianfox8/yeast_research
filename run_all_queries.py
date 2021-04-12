import json
import sqlite3
import sys

def XC_grabber(db):
    c = sqlite3.connect(db)
    cursor = c.cursor()
    XC_query = [ row[0] for row in cursor.execute('select ParameterIndex,Vertex from Signatures natural join ( select MorseGraphIndex,Vertex from MorseGraphAnnotations where label="XC {sbf, yhp1, sff, swi5/ace2}" except select MorseGraphIndex,Source from MorseGraphEdges);')]
    with open('XC_query.txt', 'w') as f:
        json.dump(XC_query,f)

def FC_grabber(db):
    c = sqlite3.connect(db)
    cursor1 = c.cursor()
    FC_result = [row[0] for row in cursor1.execute('select ParameterIndex, Vertex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));')]
    with open('FC_query.txt', 'w') as f:
        json.dump(FC_result,f)

def FP_grabber(db):
    c =sqlite3.connect(db)
    cursor2 = c.cursor()
    cursor2.execute('select ParameterIndex, label from Signatures natural join ( select MorseGraphIndex, label from MorseGraphAnnotations where label like "FP%" except select MorseGraphIndex,Source from MorseGraphEdges);')
    FP_fetch = cursor2.fetchall()
    FP_result = {}
    for row in FP_fetch:
        FP_result.setdefault(row[0], []).append(row[1])
    with open('FP_query.txt', 'w') as f:
        json.dump(FP_result,f)

def mono_grabber(db):
    c = sqlite3.connect(db)
    cursor3 = c.cursor()
    monostable_result = [row[0] for row in cursor3.execute("select MorseGraphIndex from (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=1;")]
    with open('monostable_query.txt', 'w') as f:
        json.dump(monostable_result,f)

def bistable_grabber(db):
    c = sqlite3.connect(db)
    cursor4 = c.cursor()
    bistable_result = [row[0] for row in cursor4.execute("select MorseGraphIndex from (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=2;")]
    with open('bistable_query.txt', 'w') as f:
        json.dump(bistable_result,f)

if __name__ == '__main__':
    db = sys.argv[1]
    XC_grabber(db)
    FC_grabber(db)
    FP_grabber(db)
    mono_grabber(db)
    bistable_grabber(db)