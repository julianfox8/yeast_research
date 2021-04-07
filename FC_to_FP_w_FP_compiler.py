import pickle
import sys

#filename = 'CLB2_OFF_XC.txt'
#filename2 = 'FP_results.txt' (I had a pre-computed .txt file of all FPs for the network)
def FP_compiler(filename, filename2):
    with open(filename, 'rb') as f:
        CLB2_OFF = pickle.load(f)
    with open(filename2, 'rb') as f:
        FP_results = pickle.load(f)
    CLB2_OFF_FP = {}
    matching_keys = set(CLB2_OFF.keys()).intersection(set(FP_results.keys()))
    for k in matching_keys:
        CLB2_OFF_FP[k] = [FP_results[k],CLB2_OFF[k]]
    CLB2_OFF_XC_FC = []
    for key, val in CLB2_OFF_FP.items():
        OFF_P = val[0]
        OFF_FC_P = val[1][1]
        if set(OFF_P) == set(OFF_FC_P):
            CLB2_OFF_XC_FC.extend(OFF_P)
    with open('CLB2_OFF_XC_FP_FC_2.txt', 'wb') as f:
        pickle.dump(CLB2_OFF_FP, f)

if __name__ == '__main__':
    filename = sys.argv[1]
    filename2 = sys.argv[2]
    FP_compiler(filename, filename2)

