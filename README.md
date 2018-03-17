SENG 533
========

## Project B

`analyze.sh`

This script is intended to run the `test.sh` script on the client, targeting the server, and collect the results from both the client and server. These results will be placed in the current directory with the names `client-results.txt` and `server-results.txt`. This script is run with the following parameters:

`analyze.sh <client_dns> <server_dns> <server_ip> <key_path>`

- `client_dns` - DNS name for client
- `server_dns` - DNS name for server
- `server_ip` - IP Address for server
- `key_path` - Path to `.pem` access key

The script will also generate a `params.txt` file locally with the parameters (`session` and `period`) that each run occurred with
