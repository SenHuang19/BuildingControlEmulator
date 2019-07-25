"""
.. module:: startREST

  :platform: Unix, Windows

  :synopsis: This module implements the REST API used to interact with the test case. The API is implemented using the ``flask`` package. 

.. moduleauthor:: PNNL
"""
# -*- coding: utf-8 -*-
"""
This module implements the REST API used to interact with the test case.  
The API is implemented using the ``flask`` package.  
"""

# GENERAL PACKAGE IMPORT
# ----------------------
from flask import Flask
from flask_restful import Resource, Api, reqparse
import getopt		# for being able to supply input arguments to the script
# ----------------------

# SIMULATION SETUP IMPORT
# -----------------------
from emulatorSetup import emulatorSetup
# -----------------------

# DEFINE REST REQUESTS
# --------------------
class Advance(Resource):
  """Interface to advance the test case simulation."""

  def __init__(self, **kwargs):
    self.case = kwargs["case"]
    self.parser_advance = kwargs["parser_advance"]

  def post(self):
    """
    POST request with input data to advance the simulation one step 
    and receive current measurements.
    """
    u = self.parser_advance.parse_args()
    y = self.case.advance(u)
    return y

class Reset(Resource):
  """
  Interface to test case simulation step size.
  """
  
  def __init__(self, **kwargs):
      self.case = kwargs["case"]
      self.parser_reset = kwargs["parser_reset"]

  def put(self):
    """PUT request to reset the test."""
    u = self.parser_reset.parse_args()
    start = u['start']
    self.case.reset(start)
    return start

        
class Step(Resource):
  """Interface to test case simulation step size."""

  def __init__(self, **kwargs):
      self.case = kwargs["case"]
      self.parser_step = kwargs["parser_step"]

  def get(self):
    """GET request to receive current simulation step in seconds."""
    return self.case.get_step()

  def put(self):
    """PUT request to set simulation step in seconds."""
    args = self.parser_step.parse_args()
    step = args['step']
    self.case.set_step(step)
    return step, 201
        
class Inputs(Resource):
  """Interface to test case inputs."""

  def __init__(self, **kwargs):
      self.case = kwargs["case"]
    
  def get(self):
    """GET request to receive list of available inputs."""
    u_list = self.case.get_inputs()
    return u_list
        
class Measurements(Resource):
  """Interface to test case measurements."""

  def __init__(self, **kwargs):
      self.case = kwargs["case"]
    
  def get(self):
    """GET request to receive list of available measurements."""
    y_list = self.case.get_measurements()
    return y_list
        
class Results(Resource):
  """Interface to test case result data."""

  def __init__(self, **kwargs):
      self.case = kwargs["case"]

  def get(self):
    """GET request to receive measurement data."""
    
    Y = self.case.get_results()
    return Y
        
class KPI(Resource):
  """Interface to test case KPIs."""

  def __init__(self, **kwargs):
    self.case = kwargs["case"]
    
  def get(self):
    """GET request to receive KPI data."""
    kpi = self.case.get_kpis()
    return kpi
        
class Name(Resource):
  """Interface to test case name."""

  def __init__(self, **kwargs):
    self.case = kwargs["case"]
    
  def get(self):
    """GET request to receive test case name."""
    return self.case.get_name()
# --------------------

def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hp:s:", ["help", "fmuPath=", "fmuStep="])
    if not opts:
      print("ERROR: need options and arguments to run.")
      print("Usage: ./startREST.py -p <path to FMU file> -s <FMU step in seconds>")
      sys.exit()
  except getopt.GetoptError:
    print("Wrong option or no input argument! Usage: ./startREST.py -p <path to FMU file> -s <FMU step in seconds>")
    sys.exit(2)
  for opt, arg in opts:
    if  opt in ("-h", "--help"):
      print("Help prompt. Usage: ./startREST.py -p <path to FMU file> -s <FMU step in seconds>")
      sys.exit()
    elif opt in ("-p", "--fmuPath"):
      fmuPath = arg
    elif opt in ("-s", "--fmuStep"):
      fmuStep = int(arg)
  
  # FLASK REQUIREMENTS
  # ------------------
  app = Flask(__name__)
  api = Api(app)
  # ------------------

  # INSTANTIATE SIMULATION
  # ---------------------
  case = emulatorSetup(fmuPath, fmuStep)
  # ---------------------

  # DEFINE ARGUMENT PARSERS
  # -----------------------
  # ``step`` interface
  parser_step = reqparse.RequestParser()
  parser_step.add_argument('step')
  # ``reset`` interface
  parser_reset = reqparse.RequestParser()
  parser_reset.add_argument('start')
  # ``advance`` interface
  parser_advance = reqparse.RequestParser()
  for key in case.u.keys():
    parser_advance.add_argument(key)
  # -----------------------

  # ADD REQUESTS TO API WITH URL EXTENSION
  # --------------------------------------
  api.add_resource(Advance, '/advance', resource_class_kwargs = {"case": case, "parser_advance": parser_advance})
  api.add_resource(Reset, '/reset', resource_class_kwargs = {"case": case, "parser_reset": parser_reset})
  api.add_resource(Step, '/step', resource_class_kwargs = {"case": case, "parser_step": parser_step})
  api.add_resource(Inputs, '/inputs', resource_class_kwargs = {"case": case})
  api.add_resource(Measurements, '/measurements', resource_class_kwargs = {"case": case})
  api.add_resource(Results, '/results', resource_class_kwargs = {"case": case})
  api.add_resource(KPI, '/kpi', resource_class_kwargs = {"case": case})
  api.add_resource(Name, '/name', resource_class_kwargs = {"case": case})
  # --------------------------------------

  app.run(debug=False, host='0.0.0.0')

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])