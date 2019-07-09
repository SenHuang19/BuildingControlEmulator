FROM michaelwetter/ubuntu-1604_jmodelica_trunk


ENV ROOT_DIR /usr/local
ENV JMODELICA_HOME $ROOT_DIR/JModelica
ENV IPOPT_HOME $ROOT_DIR/Ipopt-3.12.4
ENV SUNDIALS_HOME $JMODELICA_HOME/ThirdParty/Sundials
ENV SEPARATE_PROCESS_JVM /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV PYTHONPATH $PYTHONPATH:$JMODELICA_HOME/Python:$JMODELICA_HOME/Python/pymodelica

USER root

WORKDIR $HOME

RUN pip install --user flask-restful

COPY testcase /usr/testcases/testcase

COPY examples /usr/testcases/examples

COPY config.py /usr/testcases/config.py

COPY restapi.py /usr/testcases/restapi.py

COPY testcase.py /usr/testcases/testcase.py


