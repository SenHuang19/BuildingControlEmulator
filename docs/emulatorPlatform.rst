Building Control Emulator platform
**********************************
The building emulator is given as a Functional Mock-up Unit (FMU) and simulated using `JModelica`_. JModelica, as the tool to simulate and analyze the building emulator behavior, has been packaged on a Ubuntu 16.04.5 LTS machine in a Docker container. Hence, in order to download, access and run the JModelica-specialized container, Docker needs to be installed on the host machine.

.. _JModelica: https://jmodelica.org

Docker Container
================
For Windows 10 and Mac OS, there are specific versions of `Docker desktop`_, that is `Docker desktop for Windows`_, and `Docker desktop for Mac`_. On Ubuntu (Linux), installing Docker is less straight forward, and the procedure coudl follow the details below.

.. _`Docker desktop`: https://www.docker.com/products/docker-desktop
.. _`Docker desktop for Windows`: https://hub.docker.com/editions/community/docker-ce-desktop-windows
.. _`Docker desktop for Mac`: https://hub.docker.com/editions/community/docker-ce-desktop-mac


File `Script to install Docker CE on Ubuntu`_, which presents what the docker installation site shows at `Docker installation`_, can be used as helper to download and install Docker CE on Ubuntu.

.. _Script to install Docker CE on Ubuntu: https://github.com/GRIDAPPSD/gridappsd-docker/blob/master/docker_install_ubuntu.sh
.. _Docker installation: https://docs.docker.com/install/linux/docker-ce/ubuntu/

.. code::

  #!/bin/bash

  # Environment variables you need to set so you don't have to edit the script below.
  DOCKER_CHANNEL=stable
  DOCKER_COMPOSE_VERSION=1.18.0

  # Update the apt package index.
  sudo apt-get update

  # Install packages to allow apt to use a repository over HTTPS.
  sudo apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      software-properties-common \
      vim

  # Add Docker's official GPG key.
  curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | sudo apt-key add -

  # Verify the fingerprint.
  sudo apt-key fingerprint 0EBFCD88

  # Pick the release channel.
  sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
    $(lsb_release -cs) \
    ${DOCKER_CHANNEL}"

  # Update the apt package index.
  sudo apt-get update

  # Install the latest version of Docker CE.
  sudo apt-get install -y docker-ce

  # Allow your user to access the Docker CLI without needing root.
  sudo /usr/sbin/usermod -aG docker $USER

  # Install Docker Compose.
  curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` -o /tmp/docker-compose
  sudo mv /tmp/docker-compose /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo chown root:root /usr/local/bin/docker-compose

The script also installs Docker Composer, used to define and run a multi-container Docker application. See `Compose overview`_.

.. _Compose overview: https://docs.docker.com/compose/overview/

**Warning.** To be able to run the Docker CLI without needing root, you need a reboot.