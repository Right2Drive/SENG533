#!/bin/bash

# Variables
client_dns=$1
server_dns=$2
server_ip=$3
run=0

# Create the results.txt on server/client

ssh -i ~/Keys/seng533.pem ubuntu@$client_dns <<EOF

cd engg_533/
touch results.txt

exit
EOF

ssh -i ~/Keys/seng533.pem ubuntu@$server_dns <<EOF

cd engg_533/
touch results.txt

exit
EOF

# Main Loop
while [ $run -lt 2 ]
do
  rerun=0

  # calculate params
  sessions=$((500+$run*25))
  period=$((35/$sessions))

  # Sub loop (for averages)

  while [ $rerun -lt 2 ]
  do

    ssh -i ~/Keys/seng533.pem ubuntu@$client_dns <<EOF
# ------------- Client ----------- #

# TODO: Run the HTTP Perf and collect any results in result.txt

# Move to correct directory
cd engg_533/

# Set header for run
echo "run ${run}-${rerun}" >> results.txt

# Run the test script
bash test.sh $server_ip $sessions $period

# Pipe response times into results
echo "-- RESPONSE --" >> results.txt
cat responsetimes/output.txt >> results.txt
echo "-- END --" >> results.txt
echo "" >> results.txt

exit
# -------------------------------- #
EOF

  ssh -i ~/Keys/seng533.pem ubuntu@$server_dns <<EOF
# ------------ Server ------------ #

# TODO: Run the various performance scripts and collect any results in result.txt

cd engg_533/

echo "run ${run}-${rerun}" >> results.txt

echo "-- PERFDATA --" >> results.txt
cat collectl/perfdata.txt >> results.txt
echo "-- END --" >> results.txt

echo "-- UTILIZATION --" >> results.txt
./collectl/utilization.sh ./collectl/perfdata.txt >> results.txt
echo "-- END --" >> results.txt
echo "" >> results.txt

exit
# -------------------------------- #
EOF

  rerun=$(($rerun+1))
  done

run=$(($run+1))
done

# TODO: SFTP to server and retrieve results, delete when done
sftp -i ~/Keys/seng533.pem ubuntu@$client_dns <<EOF

cd engg_533/
get results.txt
rm results.txt

exit
EOF

mv ./results.txt ./client-results.txt

sftp -i ~/Keys/seng533.pem ubuntu@$server_dns <<EOF

cd engg_533/
get results.txt
rm results.txt

exit
EOF

mv ./results.txt ./server-results.txt
