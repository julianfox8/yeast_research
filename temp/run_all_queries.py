import json
import sqlite3
import sys, time

def XC_grabber(db):
    c = sqlite3.connect(db)
    cursor = c.cursor()
    # could have bistable XCs, so get unique parameter indices
    XC_query = list(set([ row[0] for row in cursor.execute('select ParameterIndex from Signatures natural join ( select MorseGraphIndex,Vertex from MorseGraphAnnotations where label="XC {sbf, yhp1, sff, swi5/ace2}" except select MorseGraphIndex,Source from MorseGraphEdges);')]))
    with open('XC_query.json', 'w') as f:
        json.dump(XC_query,f)
    return XC_query


def FC_grabber(db):
    c = sqlite3.connect(db)
    cursor1 = c.cursor()
    # could have bistable FCs, so get unique parameter indices
    FC_result = list(set([row[0] for row in cursor1.execute('select ParameterIndex from Signatures natural join (select MorseGraphIndex,Vertex from (select MorseGraphIndex,Vertex from MorseGraphAnnotations where Label="FC" except select MorseGraphIndex,Source from MorseGraphEdges));')]))
    with open('FC_query.json', 'w') as f:
        json.dump(FC_result,f)
    return FC_result


def bistable_grabber(db):
    c = sqlite3.connect(db)
    cursor4 = c.cursor()
    # this should give unique parameter indices, but take unique parameter indices to be sure
    bistable_result = list(set([row[0] for row in cursor4.execute("select ParameterIndex from Signatures natural join (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=2;")]))
    with open('bistable_query.json', 'w') as f:
        json.dump(bistable_result,f)
    return bistable_result


def mono_grabber(db):
    c = sqlite3.connect(db)
    cursor3 = c.cursor()
    # this should give unique parameter indices, but take unique parameter indices to be sure
    monostable_result = list(set([row[0] for row in cursor3.execute("select ParameterIndex from Signatures natural join (select MorseGraphIndex, count(*) as StableCount from (select MorseGraphIndex,Vertex from MorseGraphVertices except select MorseGraphIndex,Source from MorseGraphEdges) group by MorseGraphIndex) where StableCount=1;")]))
    with open('monostable_query.json', 'w') as f:
        json.dump(monostable_result,f)
    return monostable_result


def FC_FP_grabber(db,bistable_FC_query):
    # bistable_FC_query must be a tuple of parameter indices
    c = sqlite3.connect(db)
    cursor2 = c.cursor()
    # could get multistable FC, FP, FP (in general), take unique parameter indices
    bistable_FC_FP_result = list(set([row[0] for row in cursor2.execute('select ParameterIndex from Signatures natural join ( select MorseGraphIndex, label from MorseGraphAnnotations where label like "FP%" except select MorseGraphIndex,Source from MorseGraphEdges) where ParameterIndex in {};'.format(bistable_FC_query))]))
    with open('bistable_FC_FP_query.json', 'w') as f:
        json.dump(bistable_FC_FP_result,f)
    return bistable_FC_FP_result


def XC_FP_grabber(db,bistable_XC_query):
    # bistable_XC_query must be a tuple of parameter indices
    c = sqlite3.connect(db)
    cursor2 = c.cursor()
    # could get multistable XC, FP, FP (in general), take unique parameter indices
    bistable_XC_FP_result = list(set([row[0] for row in cursor2.execute('select ParameterIndex from Signatures natural join ( select MorseGraphIndex, label from MorseGraphAnnotations where label like "FP%" except select MorseGraphIndex,Source from MorseGraphEdges) where ParameterIndex in {};'.format(bistable_XC_query))]))
    with open('bistable_XC_FP_query.json', 'w') as f:
        json.dump(bistable_XC_FP_result,f)
    return bistable_XC_FP_result


def main(db,chunk=1000000):
    # because of memory issues, we have to intersect one chunk at a time
    starttime = time.process_time()

    print("Monostable starting")
    monostable_query = mono_grabber(db)
    now = time.process_time()
    print("Monostable complete, {} WT params".format(len(monostable_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()

    print("FC starting")
    FC_query = FC_grabber(db)
    starttime = now
    now = time.process_time()
    print("FC complete, {} WT params".format(len(FC_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()

    print("Monostable FC starting")
    monostable_FC_query = set()
    for k in range(0,len(monostable_query),chunk):
        monostable_FC_query = monostable_FC_query.union(set(monostable_query[k:k+chunk]).intersection(FC_query))
    monostable_FC_query = list(monostable_FC_query)
    with open('monostable_FC_query.json', 'w') as f:
        json.dump(monostable_FC_query,f)
    starttime = now
    now = time.process_time()
    print("Monostable FC complete, {} WT params".format(len(monostable_FC_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)
    del monostable_FC_query #since memory is a problem, explicitly delete

    print("XC starting")
    XC_query = XC_grabber(db)
    now = time.process_time()
    print("XC complete, {} WT params".format(len(XC_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)

    print("Monostable XC starting")
    monostable_XC_query = set()
    for k in range(0,len(monostable_query),chunk):
        monostable_XC_query = monostable_XC_query.union(set(monostable_query[k:k+chunk]).intersection(XC_query))
    monostable_XC_query = list(monostable_XC_query)
    with open('monostable_XC_query.json', 'w') as f:
        json.dump(monostable_XC_query,f)
    starttime = now
    now = time.process_time()
    print("Monostable XC complete, {} WT params".format(len(monostable_XC_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)
    del monostable_XC_query #since memory is a problem, explicitly delete
    del monostable_query

    print("Bistable starting")
    bistable_query = bistable_grabber(db)
    starttime = now
    now = time.process_time()
    print("Bistable complete, {} WT params".format(len(bistable_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)

    print("Bistable FC starting")
    bistable_FC_query = set()
    for k in range(0,len(bistable_query),chunk):
        bistable_FC_query=bistable_FC_query.union(set(bistable_query[k:k+chunk]).intersection(FC_query))
    bistable_FC_query = list(bistable_FC_query)
    with open('bistable_FC_query.json', 'w') as f:
        json.dump(bistable_FC_query,f)
    starttime = now
    now = time.process_time()
    print("Bistable FC complete, {} WT params".format(len(bistable_FC_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)
    del FC_query

    print("Bistable FC/FP starting")
    bistable_FC_FP = FC_FP_grabber(db, tuple(bistable_FC_query))
    with open('bistable_FC_FP_query.json', 'w') as f:
        json.dump(bistable_FC_FP,f)
    starttime = now
    now = time.process_time()
    print("Bistable FC/FP complete, {} WT params".format(len(bistable_FC_FP)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)
    del bistable_FC_query
    del bistable_FC_FP

    print("Bistable XC starting")
    bistable_XC_query = set()
    for k in range(0,len(bistable_query),chunk):
        bistable_XC_query = bistable_XC_query.union(set(bistable_query[k:k+chunk]).intersection(XC_query))
    bistable_XC_query = list(bistable_XC_query)
    with open('bistable_XC_query.json', 'w') as f:
        json.dump(bistable_XC_query,f)
    starttime = now
    now = time.process_time()
    print("Bistable XC complete, {} WT params".format(len(bistable_XC_query)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # time.sleep(0.5)
    del bistable_query
    del XC_query

    print("Bistable XC/FP starting")
    bistable_XC_FP = XC_FP_grabber(db, tuple(bistable_XC_query))
    with open('bistable_XC_FP_query.json', 'w') as f:
        json.dump(bistable_XC_FP,f)
    starttime = now
    now = time.process_time()
    print("Bistable XC/FP complete, {} WT params".format(len(bistable_XC_FP)))
    print("{:.02f} minutes\n".format((now - starttime)/60))


if __name__ == '__main__':
    db = sys.argv[1]
    main(db,chunk=1000000)
