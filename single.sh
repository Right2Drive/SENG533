#!/bin/bash

# Variables
server_ip="ec2-52-11-10-86.us-west-2.compute.amazonaws.com"
client_ip="ec2-34-215-43-162.us-west-2.compute.amazonaws.com"
run=1

# Main Loop
while [ $run -lt 6 ]
do
  rerun=1

  while [ $rerun -lt 6 ]
  do
    ssh -i ~/Keys/seng533.pem ubuntu@$client_ip <<EOF
# ------------- Client ----------- #

# TODO: Run the HTTP Perf and collect any results in result.txt

cd engg_533/
bash test.sh

exit
# -------------------------------- #
EOF

ssh -i ~/Keys/seng533.pem ubuntu@$client_ip <<EOF
# ------------ Server ------------ #

# TODO: Run the various performance scripts and collect any results in result.txt

cd engg_533/

exit
# -------------------------------- #
EOF

  rerun=$(($rerun+1))
  done

run=$(($run+1))
done

# TODO: SFTP to server and retrieve results, delete when done
