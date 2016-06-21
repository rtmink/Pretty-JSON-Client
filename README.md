# Pretty-JSON-Client
Parsing JSON data arriving over a bad protocol such that there is no delimiter between the JSON objects.

***

IMPORTANT:

I wrote "pretty_json_client.py" and "test.py", which interact with the "ugly_json_server.py".

***

The command "python3" is used below assuming that
it is the command name for python 3.

Client command-line:
python3 pretty_json_client.py

Test command-line:*
python3 test.py

To set the number of JSON objects that the client is tested with (default 100):
python3 test.py --limit 90

*: test.py executes commands in a subshell that include running the
server and the client using the command "python3" which as the 
name implies, refers to python 3. Change this command if needed.

Also, ugly_json_server.py, pretty_json_client.py, and test.py are assumed 
to be in the same directory. Thus, ugly_json_server.py is included in the
zip file for ease of testing.
