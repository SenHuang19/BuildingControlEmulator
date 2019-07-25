"""
.. module:: runSimulation

  :platform: Unix, Windows

  :synopsis: This module simply tests starting and running a simulation within the JModelica docker.

.. moduleauthor:: PNNL
"""
# -*- coding: utf-8 -*-
# GENERAL PACKAGE IMPORT
# ----------------------
import requests
import getopt
import os
import csv
# ----------------------

def ctrlInitialize(inputs):
  u = {}
  for ind in range(len(inputs)):
    if "_u" in inputs[ind]:
      u[inputs[ind]] = 1e-27
    elif "_activate" in inputs[ind]:
      u[inputs[ind]] = 0
  return u

def main(argv):
  # SETUP SIMULATION
  # ---------------

  try:
    opts, args = getopt.getopt(argv, "hu:d:o:l:s:", ["help", "url=", "dayOfYear=", "dayOffset=", "simDuration=", "fmuStep="])
    if not opts:
      print("ERROR: need options and arguments to run.")
      print("Usage: ./runSimulation.py -u <url of FMU machine> -d <day of year to start the simulation> -o <second of day to start the simulation> -l <simulation duration in seconds> -s <FMU step in seconds>")
      sys.exit()
  except getopt.GetoptError:
    print("Wrong option or no input argument! Usage: ./runSimulation.py -u <url of FMU machine> -d <day of year to start the simulation> -o <second of day to start the simulation> -l <simulation duration in seconds> -s <FMU step in seconds>")
    sys.exit(2)
  for opt, arg in opts:
    if  opt in ("-h", "--help"):
      print("Help prompt. Usage: ./runSimulation.py -u <url of FMU machine> -d <day of year to start the simulation> -o <second of day to start the simulation> -l <simulation duration in seconds> -s <FMU step in seconds>")
      sys.exit()
    # Set URL for emulator location
    elif opt in ("-u", "--url"):
      url = arg
    # Set simulation parameters
    elif opt in ("-l", "--simDuration"):
      simDuration = int(arg)
    elif opt in ("-s", "--fmuStep"):
      fmuStep = int(arg)
    elif opt in ("-d", "--dayOfYear"):
      dayOfYear = int(arg)
    elif opt in ("-o", "--dayOffset"):
      dayOffset = int(arg)

  # GET TEST INFORMATION
  # --------------------
  print('\nSIMULATION SETUP INFORMATION\n---------------------')
  # Test case name
  name = requests.get('{0}/name'.format(url)).json()
  print('Name:\t\t\t\t{0}'.format(name))
  # Inputs available
  inputs = requests.get('{0}/inputs'.format(url)).json()
  # print('Control Inputs:\t\t\t{0}'.format(inputs))
  inputFileName = "controlInputsList.csv"
  if os.path.exists(inputFileName):
    os.remove(inputFileName)
    with open(inputFileName, "w", newline = "") as outFile:
      writer = csv.writer(outFile)
      for line in sorted(inputs):
        writer.writerow([line])
  else:
    with open(inputFileName, "w", newline = "") as outFile:
      writer = csv.writer(outFile)
      for line in sorted(inputs):
        writer.writerow([line])
  # Measurements available
  measurements = requests.get('{0}/measurements'.format(url)).json()
  # print('Measurements:\t\t\t{0}'.format(sorted(measurements)))
  measFileName = "measurementsList.csv"
  if os.path.exists(measFileName):
    os.remove(measFileName)
    with open(measFileName, "w", newline = "") as outFile:
      writer = csv.writer(outFile)
      for line in sorted(measurements):
        writer.writerow([line])
  else:
    with open(measFileName, "w", newline = "") as outFile:
      writer = csv.writer(outFile)
      for line in measurements:
        writer.writerow([line])
  outFileName = "results.csv"
  if os.path.exists(outFileName):
    os.remove(outFileName)
    outFile = open(outFileName, "w", newline = "")
    writer = csv.DictWriter(outFile, fieldnames = sorted(measurements))
    writer.writeheader()
  else:
    outFile = open(outFileName, "w", newline = "")
    writer = csv.DictWriter(outFile, fieldnames = sorted(measurements))
    writer.writeheader()
  # Default simulation step
  step_def = requests.get('{0}/step'.format(url)).json()
  print('Default Simulation Step:\t{0}'.format(step_def))
  # --------------------

  # RUN SIMULATION
  # -------------
  # Reset simulation
  print('Resetting simulation to start in a certain day of year at a certain time in seconds.')
  res = requests.put('{0}/reset'.format(url), data = {'start': dayOffset + dayOfYear * 24 * 3600})
  # Set simulation step
  print('Setting simulation step to {0}.'.format(fmuStep))
  res = requests.put('{0}/step'.format(url), data = {'step': fmuStep})
  print('============ Started running simulation ============\n')
  timeStep = 1
  # Initialize u
  u = ctrlInitialize(inputs)
  # Simulation Loop
  while timeStep <= int(simDuration/fmuStep):
    # Advance simulation
    y = requests.post('{0}/advance'.format(url), data = u).json()
    # print(sorted(y.items(), key = lambda x: x[0]))
    # Compute next control signal
    # Here code to change control signals could be added
    # u = ins
    print("Simulated step {0}.".format(timeStep))
    timeStep += 1
    print("Current time {0} seconds.\n".format(y["time"]))
    writer.writerow(dict(sorted(y.items(), key = lambda x: x[0])))
  print('============= Simulation complete. =================\n')
  # -------------

if __name__ == "__main__":
  import sys
  main(sys.argv[1:])