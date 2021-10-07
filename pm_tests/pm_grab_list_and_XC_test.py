import os

#the pm_grab_plist_test will print the all_match and res dictionaries to see if the parameters and corresponding parameter indices are properly being stored in the res dictionary

#the pm_XC_test will print out the res dictionary to see if Param_list contains any parameter indices (I am not sure whether there exist any partial patternmatches within this test but my code could have a bug in it)

def pm_grab_plist_test():
    print("Starting pm_grab_plist_test")
    #two differnt command objects defined depending on whether the CountPatternMatch script is saved within the ~/dsgrn_net_query/src/dsgrn_net_query/queries directory or the working directory
    command = "python ~/dsgrn_net_query/src/dsgrn_net_query/queries/CountPatternMatch_large_networks_grab_plist.py mpi_network_pm_ln.txt mpi_params_FCln.json"
    #command = "python CountPatternMatch_large_networks_grab_plist.py mpi_network_pm_ln.txt mpi_params_FCln.json"
    os.system(command)
    print("pm_grab_plist_test complete")

def pm_XC_test():
    print("\n Starting pm_XC_test")
    # two differnt command objects defined depending on whether the CountPatternMatch script is saved within the ~/dsgrn_net_query/src/dsgrn_net_query/queries directory or the working directory
    command = "python ~/dsgrn_net_query/src/dsgrn_net_query/queries/CountPatternMatch_large_networks_grab_plist_XC.py mpi_network_pm_ln_XC.txt mpi_params_XCln.json"
    #command = "python CountPatternMatch_large_networks_grab_plist_XC.py mpi_network_pm_ln_XC.txt mpi_params_XCln.json"
    os.system(command)
    print("pm_XC_test complete")

if __name__ == "__main__":
    pm_grab_plist_test()
    pm_XC_test()