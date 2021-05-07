import json, sys, DSGRN, sqlite3, ast, pickle
from dsgrn_utilities.parameter_building import construct_parameter
from parameter_constructer import param_constructer
from FC_XC_checker import FC_XC_check
from monoFC_monoXC_checker import monoFC_monoXC_check
from bistableFC_bistableXC_FP_checker import bistableFC_bistableXC_FP_check

def run_all_transition(net):
    FC_XC_check(net)
    monoFC_monoXC_check(net)
    bistableFC_bistableXC_FP_check(net)

if __name__ == '__main__':
    net = sys.argv[1]
    run_all_transition(net)
