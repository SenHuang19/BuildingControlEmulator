# -*- coding: utf-8 -*-
"""
This file is used to configure the test case.

"""

def get_config():
    '''Returns the configuration structure for the test case.
    
    Returns
    -------
    config : dict()
    Dictionary contatinin configuration information.
    {
    'fmupath'  : string, location of model fmu
    'step'     : int, default control step size in seconds
    }
    
    '''
        
    config = {
	'fmu1':{
    # Enter configuration information
    'fmupath'  : '/usr/testcases/testcase/models/fmu1/wrapped.fmu',
    'name'  : 'LargeOffice',
    'step'     : 60},
	'fmu2':{
    # Enter configuration information
    'fmupath'  : '/usr/testcases/testcase/models/fmu2/wrapped.fmu',   
    'name'  : 'LargeOfficeFDD',
    'step'     : 60}
    }
    
    return config