MarathonPlayground
==================

Tiny server for judging marathon-style tasks

Execute run.bat/run.sh for starting a server. Server will be available at http://localhost:8051.

You should put tester from Topcoder, say, TopcoderTaskNameVis.jar, in folder 'testing'. Then edit 4th line of file judge.py accordingly.

If something is wrong with testing (you can look at the server window for error messages), take a look at the lines of judge.py which contain definition of variable run_jar_str and check if all needed parameters are specified.
