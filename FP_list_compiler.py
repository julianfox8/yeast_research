import json
import sqlite3
import sys

with open('bistable_query.json') as f:
    bistable_query = json.load(f)
with open('FC_query.json') as f:
    FC_query = json.load(f)
with open('XC_query.json') as f:
    XC_query = json.load(f)



def FP_lister(db):
    c = sqlite3.connect(db)
    cursor2 = c.cursor()
    cursor2.execute('select ParameterIndex, label from Signatures natural join ( select MorseGraphIndex, label from MorseGraphAnnotations where label like "FP%" except select MorseGraphIndex,Source from MorseGraphEdges);')
    FP_fetch = cursor2.fetchall()
    FP_result = {}
    for k, v in FP_fetch:
        if k in FP_result:
            FP_result[k].append(v)
        else:
            FP_result[k] = [v]

    bistable_FC_results = set(FC_query).intersection(set(bistable_query))
    FC_FP_keys = set(bistable_FC_results).intersection(set(FP_result.keys()))
    FC_FP_result = {k: FP_result[k] for k in FC_FP_keys}
    print('FC_FP_result: '+str(len(FC_FP_result)))

    bistable_XC_results = set(XC_query).intersection(set(bistable_query))
    XC_FP_keys = set(bistable_XC_results).intersection(set(FP_result.keys()))
    XC_FP_result = {k: FP_result[k] for k in XC_FP_keys}
    print('XC_FP_result: '+str(len(XC_FP_result)))

    with open('FC_FP_list.txt', 'w') as f:
        json.dump(FC_FP_result, f)
    with open('XC_FP_list.txt', 'w') as f:
        json.dump(XC_FP_result, f)

if __name__ == '__main__':
    db = sys.argv[1]
    FP_lister(db)
