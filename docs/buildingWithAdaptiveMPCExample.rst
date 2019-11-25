Building emulator controlled using the adaptive MPC example
===========================================================

How to run a building adaptive MPC example
------------------------------------------

For those who have access to the adaptive MPC repository, here are the steps to run an integrated building emulator and adaptive MPC case.

1. Download the Docker images
  - Building emulator Docker image at \inlineCode{laurmarinovici/building_control_emulator:latest}
  - Julia 1.2.0 on Ubuntu 18.04 image at \inlineCode{laurmarinovici/julia_1.2.0:ubuntu18}

2. Start 2 terminal windows

3. At one terminal, and in a folder of your choice, clone the building emulator repository at \href{https://github.com/SenHuang19/BuildingControlEmulator}{https://github.com/SenHuang19/BuildingControlEmulator}, which also includes the script \inlineCode{runBuildingEmulatorDocker.sh} that allows you to start the building emulator docker as root.

4. At the other terminal, and in a folder of your choice, clone the adaptive MPC repository at \href{https://stash.pnnl.gov/scm/~mari009/adaptive-control-with-julia-1.git}{https://stash.pnnl.gov/scm/~mari009/adaptive-control-with-julia-1.git}, which also includes the \inlineCode{runMPCDocker.sh} that allows you to start adaptive MPC part of the simulation.

5. In the building emulator terminal, switch to \inlineCode{/mnt/examples/} folder and run
    \begin{lstlisting}
      python startREST.py -p ./models/LargeBuilding.fmu -s 60
    \end{lstlisting}

6. In the Julia docker terminal, switch to \inlineCode{/mnt/mcp} folder and run
    \begin{lstlisting}
      julia simulate.jl
    \end{lstlisting}

7. \textcolor{red}{WARNING!} I believe that Sen changed the \inlineCode{wrapped.fmu} model in terms of signals being communicated and their names, whcih implies that the MPC code would have to be, once again, changed. Needs to be checked if we want to use that model.
\end{enumerate}