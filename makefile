IMG_NAME=boptest

COMMAND_RUN=docker run \
	  --name ${IMG_NAME} \
	  --detach=false \
	  --network host \
	  -e DISPLAY=${DISPLAY} \
	  -v /tmp/.X11-unix:/tmp/.X11-unix \
	  --rm \
	  -v `pwd`:/home/developer/test \
	  -i \
          -t \
	  ${IMG_NAME} /bin/bash -c

build:
	docker build --network host --no-cache --rm -t ${IMG_NAME} .
 
remove-image:
	docker rmi ${IMG_NAME}

run:
	$(COMMAND_RUN) \
            "bash"