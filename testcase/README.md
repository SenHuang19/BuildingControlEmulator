Test Case 
===================
This test case is a large commercial office building emulator with built-up HVAC system.

Structure
---------

- ``doc/`` contains documentation of the test case: one SimBuild 2018 paper and  slides
- ``models/`` contains the emulation model files for the test case.


To interact, send RESTful requests to: http://127.0.0.1:5000/<request>

| Interaction                                                    | Request                                                   |
|----------------------------------------------------------------|-----------------------------------------------------------|
| Advance simulation with control input and receive measurements |  POST ``advance`` with json data "{<input_name>:<value>}" |
| Reset simulation to beginning                                  |  PUT ``reset`` with no data                               |
| Receive communication step in seconds                          |  GET ``step``                                             |
| Set communication step in seconds                              |  PUT ``step`` with data ``step=<value>``                  |
| Receive sensor signal names (y) and metadata                   |  GET ``measurements``                                     |
| Receive control signals names (u) and metadata                 |  GET ``inputs``                                           |
| Receive test result data                                       |  GET ``results``                                          |                              |
| Receive test case name                                         |  GET ``name``                                             |
