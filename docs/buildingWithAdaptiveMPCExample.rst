Building emulator controlled using the adaptive MPC example
===========================================================

How to run a building adaptive MPC example
------------------------------------------

For those who have access to the adaptive MPC repository, here are the steps to run an integrated building emulator and adaptive MPC case.

1. Download the Docker images
  - Building emulator Docker image at *laurmarinovici/building_control_emulator:latest*
  - Julia 1.2.0 on Ubuntu 18.04 image at *laurmarinovici/julia_1.2.0:ubuntu18*

2. Start 2 terminal windows

3. At one terminal, and in a folder of your choice, clone the building emulator repository at `Building Control Emulator`_ , which also includes the script *runBuildingEmulatorDocker.sh* that allows you to start the building emulator docker as root.

.. _`Building Control Emulator`: https://github.com/SenHuang19/BuildingControlEmulator

4. At the other terminal, and in a folder of your choice, clone the adaptive MPC repository at `Adaptive MPC`_ , which also includes the *runMPCDocker.sh* that allows you to start adaptive MPC docker as root.

.. _Adaptive MPC: https://stash.pnnl.gov/scm/~mari009/adaptive-control-with-julia-1.git

5. In the building emulator terminal, switch to */mnt/examples/* folder and run

.. code::

  python startREST.py -p ./models/LargeBuilding.fmu -s 60

6. In the Julia docker terminal, switch to \inlineCode{/mnt/mcp} folder and run

.. code::

  julia simulate.jl

7. **WARNING!** I believe that Sen changed the *wrapped.fmu* model in terms of signals being communicated and their names, which implies that the MPC code would have to be, once again, changed. Needs to be checked if we want to use that model.