Running emulator simulation - Example
=====================================

.. _Simulation setup:

  .. figure:: images/simulationDockerDiagram.png
    :scale: 30 %

    Figure 2. Simulation setup diagram

1. Open the Ubuntu terminal on a distribution that has Docker installed.

2. Download the JModelica Docker

.. code::

  docker pull laurmarinovici/building_control_emulator:latest

3. Running

.. code::

  docker images



4. Create the JModelica Docker container by running

.. code::

  docker run -it --rm -p="127.0.0.1:5000:5000" \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker/jmodelica/,destination=/mnt/master \
           --mount type=bind,source=/Users/mari009/PNNL_Projects/GitHubRepositories/emulator_docker_fork/jmodelica/,destination=/mnt/fork \
           --network=host --name=jmodelica boptest_testcase3 bash

which will create a Docker container named *jmodelica* from *boptest_testcase3* image, and bind 2 host computer folders to 2 container folders, specifically, the master branch of the emulator GitHub repository to */mnt/master*  and a forked version to */mnt/fork/*. This way we have access to any file in the local host folders, including the emulator FMU, and any development done on any file of the binded local folders would automatically be available in the container.

5. After running the docker command from point 4, we get acces to the bash command inside the container. Navigate to one of the binded folders to access the configuration and the REST API files. In *config.py*, make sure line

.. code::

  'fmupath'  : './testcase3/models/wrapped.fmu', 

points to the correct location and name of the emulator FMU.

6. Back at the terminal prompt, launch the application by starting the REST API

.. code::

  python startREST.py

which will now wait for requests to access the emulator to update control actions or request measurements.


