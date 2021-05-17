import json
import sys, time, ast
import DSGRN
from dsgrn_utilities.parameter_building import construct_parameter



def param_constructer(param, network):
    orders = []
    hex_code = []
    for j in range(network.size()):
        hex_code.append(param.logic()[j].hex())
        orders.append(ast.literal_eval(str(param.order()[j])))
    hex_code[3] = '00'
    new_param_OFF = construct_parameter(network, hex_code, orders)
    hex_code[3] = '3F'
    new_param_ON = construct_parameter(network, hex_code, orders)
    return (new_param_OFF, new_param_ON)

def main(net, chunk=1000000):

    starttime = time.process_time()

    print("FC to XC transition starting")
    with open('FC_query.json', 'r') as f:
        FC_query = json.load(f)
    with open('XC_query.json', 'r') as f:
        XC_query = json.load(f)
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    clb2_off = []
    clb2_on = []
    #is this the proper method to iterate over the chunks and grab individual parameters?
    for k in range(0, len(FC_query), chunk):
        for i in FC_query[k:k+chunk-1]:
            param = pg.parameter(i)
            new_param_OFF, new_param_ON = param_constructer(param, network)
            clb2_off.append(pg.index(new_param_OFF))
            clb2_on.append(pg.index(new_param_ON))
    #print(len(clb2_off))
    #print(len(clb2_on))
    clb2_off_FC_XC = set()
    for k in range(0, len(clb2_off), chunk):
        clb2_off_FC_XC = clb2_off_FC_XC.union(set(clb2_off[k:k+chunk-1]).intersection(XC_query))
    clb2_off_FC_XC = list(clb2_off_FC_XC)
    clb2_on_FC_XC = set()
    for k in range(0,len(clb2_on), chunk):
        clb2_on_FC_XC = clb2_on_FC_XC.union(set(clb2_on[k:k+chunk-1]).intersection(XC_query))
    clb2_on_FC_XC = list(clb2_on_FC_XC)
    now = time.process_time()
    print("OFF clb2 FC to XC complete, {} mutant OFF params".format(len(clb2_off_FC_XC)))
    print("ON clb2 FC to XC complete, {} mutant ON params".format(len(clb2_on_FC_XC)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    del FC_query
    del XC_query
    del clb2_off_FC_XC
    del clb2_on_FC_XC
    del clb2_off
    del clb2_on

    print('mono FC to mono XC transition starting')
    with open('monostable_FC_query.json', 'r') as f:
        mono_FC = json.load(f)
    with open('monostable_XC_query.json', 'r') as f:
        mono_XC = json.load(f)
    starttime = now
    network = DSGRN.Network(net)
    pg = DSGRN.ParameterGraph(network)
    clb2_off = []
    clb2_on = []
    for k in range(0, len(mono_FC), chunk):
        for i in mono_FC[k:k+chunk-1]:
            param = pg.parameter(i)
            new_param_OFF, new_param_ON = param_constructer(param, network)
            clb2_off.append(pg.index(new_param_OFF))
            clb2_on.append(pg.index(new_param_ON))
    clb2_off_mono_FC_XC = set()
    for k in range(0, len(clb2_off), chunk):
        clb2_off_mono_FC_XC = clb2_off_mono_FC_XC.union(set(clb2_off[k:k+chunk-1]).intersection(mono_XC))
    clb2_off_mono_FC_XC = list(clb2_off_mono_FC_XC)
    clb2_on_mono_FC_XC = set()
    for k in range(0,len(clb2_on), chunk):
        clb2_on_mono_FC_XC = clb2_on_mono_FC_XC.union(set(clb2_on[k:k+chunk-1]).intersection(mono_XC))
    clb2_on_mono_FC_XC = list(clb2_on_mono_FC_XC)
    now = time.process_time()
    print("OFF clb2 mono FC to XC complete, {} mutant OFF params".format(len(clb2_off_mono_FC_XC)))
    print("ON clb2 mono FC to XC complete, {} mutant ON params".format(len(clb2_on_mono_FC_XC)))
    print("{:.02f} minutes\n".format((now - starttime)/60))
    sys.stdout.flush()
    # del clb2_off
    # del clb2_on
    # del clb2_off_mono_FC_XC
    # del clb2_on_mono_FC_XC
    # del clb2_off
    # del clb2_on


if __name__ == '__main__':
    net = sys.argv[1]
    main(net, chunk=100000)