# -*- coding: utf-8 -*-
"""
This module defines the API to the test case used by the REST requests to 
perform functions such as advancing the simulation, retreiving test case 
information, and calculating and reporting results.
"""

from pyfmi import load_fmu
import numpy as np
import copy
import config

class TestCase(object):
    '''Class that implements the test case.
    
    '''
    
    def __init__(self):
        '''Constructor.
        
        '''
        
        # Get configuration information
        con = config.get_config()
        self.fmus=[]
        self.fmu_names=[]
        self.fmu_path=[]
        self.step=[]
        for key in con.keys():
        # Define simulation model
             fmupath = con[key]['fmupath']
        # Load fmu
             self.fmus.append(load_fmu(fmupath))
             self.fmu_path.append(fmupath)
             self.fmu_names.append(con[key]['name'])
             self.step.append(con[key]['step'])
        # Get version
        input_names=[]
        output_names=[]
        for fmu in self.fmus:
             fmu_version = fmu.get_version()
        # Get available control inputs and outputs
             if fmu_version == '2.0':
                   input_names.append(fmu.get_model_variables(causality = 2).keys())
                   output_names.append(fmu.get_model_variables(causality = 3).keys())
             else:
                   raise ValueError('FMU must be version 2.0.')
        # Define measurements
        self.y=[]
        self.y_store=[]
        self.u=[]
        self.u_store=[]
        self.start_time=[]
        self.final_time=[]
        self.initialize=[]
        self.options=[]
        for i in range(len(input_names)):
            y ={'time':[]}
            for key in output_names[i]:
                  y[key] = []
            y_store = copy.deepcopy(y)
        # Define inputs
            u = {'time':[]}
            for key in input_names[i]:
                  u[key] = []
            u_store = copy.deepcopy(u)
        # Set default options
            options = self.fmus[i].simulate_options()
            options['CVode_options']['rtol'] = 1e-6 
        # Set default communication step

        # Set initial simulation start
            start_time = 0
            initialize = True
            options['initialize'] = self.initialize
            self.y.append(y)
            self.y_store.append(y_store)
            self.u.append(u)
            self.u_store.append(u_store)
            self.start_time.append(start_time)
            self.final_time.append(start_time)
            self.initialize.append(initialize)
            self.options.append(options)





        
    def advance(self,u,i):
        '''Advances the test case model simulation forward one step.
        
        Parameters
        ----------
        u : dict
            Defines the control input data to be used for the step.
            {<input_name> : <input_value>}
            
        Returns
        -------
        y : dict
            Contains the measurement data at the end of the step.
            {<measurement_name> : <measurement_value>}
            
        '''

        # Set final time
        self.final_time[i] = self.start_time[i] + self.step[i]
        # Set control inputs if they exist
        if u.keys():
            u_list = []
            u_trajectory = self.start_time[i]
            for key in u.keys():
                
                if key != 'time' and u[key] is not None:
                    value = float(u[key])
                    u_list.append(key)
                    u_trajectory = np.vstack((u_trajectory, value))
            input_object = (u_list, np.transpose(u_trajectory))
        else:
            input_object = None
        # Simulate
        print input_object
        self.options[i]['initialize'] = self.initialize[i]
        res = self.fmus[i].simulate(start_time=self.start_time[i], 
                                final_time=self.final_time[i], 
                                options=self.options[i], 
                                input=input_object)
        # Get result and store measurement
        for key in self.y[i].keys():
            self.y[i][key] = res[key][-1]
            print self.y_store[i]
            self.y_store[i][key] = self.y_store[i][key] + res[key].tolist()[1:]
        # Store control inputs
        for key in self.u[i].keys():
            self.u_store[i][key] = self.u_store[i][key] + res[key].tolist()[1:] 
        # Advance start time
        self.start_time[i] = self.final_time[i]
        # Prevent inialize
        self.initialize[i] = False
        
        return self.y[i]

    def reset(self,i):
        '''Reset the test.
        
        '''
        # Load fmu
        self.fmus[i]=load_fmu(self.fmu_path[i])
        self.initialize[i] = True
        self.start_time[i]=0

    def get_step(self,i):
        '''Returns the current simulation step in seconds.'''

        return self.step[i]

    def set_step(self,step,i):
        '''Sets the simulation step in seconds.
        
        Parameters
        ----------
        step : int
            Simulation step in seconds.
            
        Returns
        -------
        None
        
        '''
        
        self.step[i] = float(step)
        
        return None
        
    def get_inputs(self,i):
        '''Returns a list of control input names.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        inputs : list
            List of control input names.
            
        '''

        inputs = self.u[i].keys()
        
        return inputs
        
    def get_measurements(self,i):
        '''Returns a list of measurement names.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        measurements : list
            List of measurement names.
            
        '''

        measurements = self.y[i].keys()
        
        return measurements
        
    def get_results(self,i):
        '''Returns measurement and control input trajectories.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        Y : dict
            Dictionary of measurement and control input names and their 
            trajectories as lists.
            {'y':{<measurement_name>:<measurement_trajectory>},
             'u':{<input_name>:<input_trajectory>}
            }
        
        '''
        
        Y = {'y':self.y_store[i], 'u':self.u_store[i]}
        
        return Y
        
    def get_kpis(self,i):
        '''Returns KPI data.
        
        Requires standard sensor signals.
        
        Parameters
        ----------
        None
        
        Returns
        kpi : dict
            Dictionary containing KPI names and values.
            {<kpi_name>:<kpi_value>}
        
        '''
        
        kpi = dict()
        # Energy
        kpi['Heating Energy'] = self.y_store[i]['ETotHea_y'][-1]
        # Comfort

        return kpi
        
    def get_name(self):
        '''Returns the name of the test case fmu.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        name : str
            Name of test case fmu.
            
        '''
        
        name = self.fmu_names
        
        return name