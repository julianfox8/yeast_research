import json, sys, DSGRN, sqlite3, ast, pickle
from dsgrn_utilities.parameter_building import construct_parameter
from parameter_constructer import param_constructer
from bistableFC_bistableXC_checker import bistableFC_bistableXC_check
from FC_XC_checker import FC_XC_check
from monoFC_monoXC_checker import monoFC_monoXC_check
from CLB2_XC_query import param_compare
from bistableFC_bistableXC_FP_checker import bistableFC_bistableXC_FP_check
from CLB2_XC_FP_query import param_compare_XC_FP

def run_all_funct(net):
    param_compare(net)
    param_compare_XC_FP(net)
    FC_XC_check(net)
    monoFC_monoXC_check(net)
    bistableFC_bistableXC_check(net)
    bistableFC_bistableXC_FP_check(net)

if __name__ == '__main__':
    net = sys.argv[1]
    run_all_funct(net)
