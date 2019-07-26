Building emulator examples
==========================

How to run a simple example
---------------------------

On `Building Control Emulator`_ Github repository at *https://github.com/SenHuang19/BuildingControlEmulator*:

.. _Building Control Emulator: https://github.com/SenHuang19/BuildingControlEmulator

- folder *emulatorExamples* contains:

  - *emulatorSetup.py* - to implement the emulatorSetup class

  - *startREST.py* - to load the building emulator/FMU and start the REST server

  - folder *models* that includes the building emulators given as FMU files

  This folder needs to be bound to a folder inside the container to have access to the FMU to simulate.

- folder *simulationExamples* contains:

  - *runSimulation.py* - script to be run from the host computer to simulate the emulator inside the docker, control it if need be, get results, or whatever else the developer wants to add. This script is to be called (as seen later in the methodology) using

  .. code::

    python runSimulation.py -u "http://0.0.0.0:5000" -d 200 -o 0 -l 1200 -s 300

  or

  .. code::

    python runSimulation.py --url="http://0.0.0.0:5000" --dayOfYear=200 --dayOffset=0 --simDuration=1200 --fmuStep=300

  where

  - *-u*, *--url* represents the URL of the Docker that runs the REST server has. In this case it is *http://0.0.0.0:5000* because the emulator docker runs locally;

  - *-d*, *--dayOfYear* represents the day of year when the emulator simulation starts;

  - *-o*, *--dayOffset* represents the offset in seconds from second zero of the day when the simulation starts in the day previously set;

  - *-l*, *--simDuration* represents the entire simulation duration in seconds;

  - *-s*, *--fmuStep* represents the period for which the FMU is being simulated before stopping and/or waiting for external control; this value would actually overwrite the *fmuStep* given when instantiating the *emulatorSetup* class.
  
Methodology
-----------

**Disclaimer.** This procedure has been tested and worked well on a Mac or Linux machine with Docker installed as presented in `Docker Container`_.

1. On a computer with docker installed, open a terminal and pull the building cnotrol emulator image.

.. code::

  docker pull laurmarinovici/building_control_emulator:latest

2. To instantiate the Docker container, run

.. code::

  docker run -it --rm -p="127.0.0.1:5000:5000" \
          --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/BuildingControlEmulator/emulatorExamples/,destination=/mnt/examples \
          --name=jmodelica_docker laurmarinovici/building_control_emulator:latest bash

where */Users/mari009/PNNL_Projects/GitHubRepositories/BuildingControlEmulator/* represents the local folder where the building control emulator Github repository has been cloned to, and */mnt/examples* is just a folder on the already started *jmodelica_container*.

3. At the opened terminal inside the container:

.. code::

  cd /mnt/examples

4. Run

.. code::

  python startREST.py --fmuPath=./models/wrapped.fmu --fmuStep=60

The app should start showing

.. code::

  * Serving Flask app "startREST" (lazy loading)
  * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
  * Debug mode: off
  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

5. At a different terminal

.. code::

  cd /Users/mari009/PNNL_Projects/GitHubRepositories/BuildingControlEmulator/simulationExamples

  python runSimulation.py --url="http://0.0.0.0:5000" --dayOfYear=200 --dayOffset=0 --simDuration=1200 --fmuStep=300

6. After 4 300-second intervals, within which the building emulator is simulated, the simulation ends, and the user can observe the following output files:

  - in *<..>/BuildingControlEmulator/simulationExamples*: 

    - *results.csv* containing some sample measurements taken at the end of each 300-second interval

    - *measurementsList.csv* containing a list of all the measurements exposed for the building model

    - *controlInputsList.csv* containing a list of control signals that can be by an external control at the beginning of each 300-second interval to overwrite or not the default control signals that come with the building model:

      - *<control signal name>_activate* - flag that would signal to the emulator whether that control value should be overwrtten (when flag is set to 1) or disregarded (flag is set to 0)

      - *<control signal name>_u* - the actual value of the control signal for that particular time

  - in *<..>/BuildingControlEmulator/emulatorExamples*:

    - *<FMU name>_result.mat* - *THIS STILL NEED TO BE WORKED OUT*

List of examples
----------------

The following examples should be found in */emulatorExamples/models/*:

- *wrapped.fmu*

- *LargeOffice* - *NEED DESCRIPTION*

- *LargeOfficeFDD* - *NEED DESCRIPTION*