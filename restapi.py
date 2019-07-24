# -*- coding: utf-8 -*-
"""
This module implements the REST API used to interact with the test case.  
The API is implemented using the ``flask`` package.  
"""

# GENERAL PACKAGE IMPORT
# ----------------------
from flask import Flask
from flask_restful import Resource, Api, reqparse
# ----------------------

# TEST CASE IMPORT
# ----------------
from testcase import TestCase
# ----------------

# FLASK REQUIREMENTS
# ------------------
app = Flask(__name__)
api = Api(app)
# ------------------

# INSTANTIATE TEST CASE
# ---------------------
case = TestCase()
case_index=0
# ---------------------

# DEFINE ARGUMENT PARSERS
# -----------------------
# ``step`` interface
parser_step = reqparse.RequestParser()
parser_step.add_argument('step')

# ``select emulator`` interface
parser_name = reqparse.RequestParser()
parser_name.add_argument('name')

# ``advance`` interface
parser_advance=[]
for i in range(len(case.u)):
   temp = reqparse.RequestParser()
   for key in case.u[i].keys():
        temp.add_argument(key)
   parser_advance.append(temp)
# -----------------------

# DEFINE REST REQUESTS
# --------------------
class Advance(Resource):
    '''Interface to advance the test case simulation.'''    
    
    def post(self):
        '''POST request with input data to advance the simulation one step 
        and receive current measurements.'''
        u = parser_advance[case_index].parse_args()
        print u
        y = case.advance(u,case_index)
        return y

class Reset(Resource):
    '''Interface to test case simulation step size.'''
    
    def put(self):
        '''PUT request to reset the test.'''
        case.reset(case_index)
        return 'Testcase reset.'

        
class Step(Resource):
    '''Interface to test case simulation step size.'''
    
    def get(self):
        '''GET request to receive current simulation step in seconds.'''
        step = case.get_step(case_index)
        return step

    def put(self):
        '''PUT request to set simulation step in seconds.'''
        args = parser_step.parse_args()
        print args
        step = args['step']
        case.set_step(step,case_index)
        return step, 201
        
class Inputs(Resource):
    '''Interface to test case inputs.'''
    
    def get(self):
        '''GET request to receive list of available inputs.'''
        u_list = case.get_inputs(case_index)
        return u_list
        
class Measurements(Resource):
    '''Interface to test case measurements.'''
    
    def get(self):
        '''GET request to receive list of available measurements.'''
        y_list = case.get_measurements(case_index)
        return y_list
        
class Results(Resource):
    '''Interface to test case result data.'''
    
    def get(self):
        '''GET request to receive measurement data.'''
        Y = case.get_results(case_index)
        return Y
        
class KPI(Resource):
    '''Interface to test case KPIs.'''
    
    def get(self):
        '''GET request to receive KPI data.'''
        kpi = case.get_kpis(case_index)
        return kpi
        
class Name(Resource):
    '''Interface to test case name.'''
     
    def get(self):

        '''GET request to receive test case name.'''
        print case.get_name()
        print case_index
        name=case.get_name()[case_index]
        return name
   
    def put(self):
        '''PUT request to change the testcase.'''
        global case_index   
        args = parser_name.parse_args()
        print args
        name=args['name']
        i=0
        for fmu_name in case.get_name():
                if name == fmu_name:
                    case_index=i

                    break
                i=i+1
        print case_index
        return 'Testcase selected.'

class Emulator(Resource):
    '''Interface to test case name.'''
    
    def get(self):
        '''GET request to receive test case name.'''
        name=case.get_name()
        return name
   


# --------------------
        
# ADD REQUESTS TO API WITH URL EXTENSION
# --------------------------------------
api.add_resource(Advance, '/advance')
api.add_resource(Reset, '/reset')
api.add_resource(Step, '/step')
api.add_resource(Inputs, '/inputs')
api.add_resource(Measurements, '/measurements')
api.add_resource(Results, '/results')
api.add_resource(KPI, '/kpi')
api.add_resource(Name, '/name')
api.add_resource(Emulator, '/emulator')

# --------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')