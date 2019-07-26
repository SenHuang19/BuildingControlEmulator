JModelica Docker
================

Getting the JModelica emulator docker image
-------------------------------------------

**Note.** The following procedures are related to Mac OS and Ubuntu.

Once Docker desktop is installed on the host computer, to get access to the JModelica container, one could follow the steps below. Details on the Docker commands can be found on the `Docker documentation`_ page.

.. _Docker documentation: https://docs.docker.com

1. Open a terminal window.

2. At the terminal prompt type

.. code::

  docker pull laurmarinovici/building_control_emulator:latest

The docker image will be downloaded on the host computer.

3. To inspect the Docker images downloaded type

.. code::

  docker images

should return a list of Docker images, which should include something similar to

+-------------------------------------------+----------+------------------+----------------+--------------+
| REPOSITORY                                | TAG      | IMAGE ID         | CREATED        | SIZE         |
+===========================================+==========+==================+================+==============+
| blaurmarinovici/building_control_emulator | latest   | 04f1b11d5bd6     | 31 hours ago   | 1.69GB       |
+-------------------------------------------+----------+------------------+----------------+--------------+

4. To instantiate the Docker container, run

.. code::

  docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=<path to host computer folder to bind with container folder>,destination=<path to folder in the container bound to host folder> \
           --network=host --name=<container name> <image name> bash

  Normally, the host computer folder bound to a folder within the container would be the folder that contains the models and the running scripts (developed or downloaded from the github repository).

5. Once the container has been created, it should show up listed when running

.. code::

  docker ps -a

Inside the JModelica Docker container
-------------------------------------

.. _JModelica Docker container:

  .. figure:: images/emulatorDockerDiagram.png
    :scale: 50 %

    Figure 1. Emulator Docker diagram

`JModelica Docker container`_ is build on an Ubuntu distribution version *16.04.6 LTS (Xenial Xerus)*. It contains `JModelica`_ and the neccessary Python modules:

- `PyModelica`_ - for compiling Modelica models intu FMUs

.. _PyModelica: https://pypi.org/project/PyModelica/

- `PyFMI`_ - for loading and interacting with the FMU representing the building emulator

.. _PyFMI: https://pypi.org/project/PyFMI/


Inside the `JModelica Docker container`_, the building emulator is loaded and simulated/controlled using a `REST`_ (REpresentational State Transfer) API.

.. _REST: https://restfulapi.net

Class *emulatorSetup* has been implemented to define the REST API requests to perform functions such as advancing the simulation, retrieving test case information, and calculating and reporting results.

**Code documentation -** *emulatorSetup.py*

  .. automodule:: emulatorSetup

  - *Acquire the list of inputs the emulator accepts as control signals*

    The emulator inputs are pairs of 2 values for each control signal:

    - *<name>_activate* - that can take 0 or 1 values indicating that particular input is going to be used for control with the given value rather than the default value

    - *<name>_u* - that represents the actual input value that the control designer calculates

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_inputs

  - *Acquire the list of measurements exposed by the emulator*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_measurements

  - *Advance the emulator simulation one step further after providing a set of control inputs to it with*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: advance

  - *Obtain the name of the emulator*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_name

  - *Obtain the simulation time step in seconds*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_step

  - *Set the simulation time step in seconds*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: set_step

  - *Obtain full trajectories of measurements and control inputs*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_results

  - *Obtain key performance indicator (kpi)*

  .. autoclass:: emulatorSetup.emulatorSetup
    :members: get_kpis

Script *startREST* instantiate the building emulator by loading the desired FMU file and setting up the length of the time interval (in seconds) for which the emulator will run until finishing or being interrupted to receive an external control action. It also opens up the communication channels through which HTTP requests can be made to access the building emulator. The scripts should be called using:

.. code::

  python startREST.py -p ./models/wrapped.fmu -s 60

or

.. code::

  python startREST.py --fmuPath=./models/wrapped.fmu --fmuStep=60

**Code documentation -** *startREST.py*

  .. automodule:: startREST

  .. autoclass:: startREST.Advance
    :members:

  .. autoclass:: startREST.Inputs
    :members:
  
  .. autoclass:: startREST.Measurements
    :members:
  
  .. autoclass:: startREST.Results
    :members:
  
  .. autoclass:: startREST.KPI
    :members:
  
  .. autoclass:: startREST.Name
    :members: