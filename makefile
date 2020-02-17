IMG_NAME=laurmarinovici/building_control_emulator
COMMAND_RUN=docker run \
	  --name test \
	  --rm \
	  -v `pwd`:/usr/testcases \
 	  -it \
	  -p 127.0.0.1:5000:5000

build:
	docker build --no-cache --rm -t ${IMG_NAME} .

remove-image:
	docker rmi ${IMG_NAME}

run:
	$(COMMAND_RUN) --detach=false ${IMG_NAME} /bin/bash -c "bash"

stop:
	docker stop ${IMG_NAME}

	
