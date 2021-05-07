import json, sys, DSGRN, sqlite3, ast, pickle
from dsgrn_utilities.parameter_building import construct_parameter
from parameter_constructer import param_constructer
from CLB2_XC_FP_query import param_compare_XC_FP
from CLB2_XC_query import param_compare
from monoXC_checker import monoXC_FC_check

def run_all_cycle_check(net):
    param_compare(net)
    monoXC_FC_check(net)
    param_compare_XC_FP(net)

if __name__ == '__main__':
    net = sys.argv[1]
    run_all_cycle_check(net)
