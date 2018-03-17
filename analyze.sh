#!/bin/bash

# Variables
client_dns=$1
server_dns=$2
server_ip=$3
key_path=$4
run=0

# Create params.txt locally
touch params.txt

# Create the results.txt on server/client

ssh -i $key_path ubuntu@$client_dns <<EOF

cd engg_533/
touch results.txt

exit
EOF

ssh -i $key_path ubuntu@$server_dns <<EOF

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
  period=$(echo "scale=5; 35/$sessions" | bc)

  echo "run ${run}: sessions=${sessions} period=${period}" >> params.txt

  # Sub loop (for averages)

  while [ $rerun -lt 2 ]
  do

    ssh -i $key_path ubuntu@$client_dns <<EOF
# ------------- Client ----------- #

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

# Pipe iperf times into results
echo "-- IPERF --" >> results.txt
iperf -c $server_ip >> results.txt
echo "-- END --" >> results.txt

echo "" >> results.txt

exit
# -------------------------------- #
EOF

  ssh -i $key_path ubuntu@$server_dns <<EOF
# ------------ Server ------------ #

cd engg_533/

echo "run ${run}-${rerun}" >> results.txt

echo "-- PERFDATA --" >> results.txt
cat collectl/perfdata.txt >> results.txt
echo "-- END --" >> results.txt

# Run utilization script
echo "-- UTILIZATION --" >> results.txt
./collectl/utilization.sh ./collectl/perfdata.txt >> results.txt
echo "-- END --" >> results.txt

# Pipe iperf times into results
echo "-- IPERF --" >> results.txt
iperf -s >> results.txt
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
sftp -i $key_path ubuntu@$client_dns <<EOF

cd engg_533/
get results.txt
rm results.txt

exit
EOF

mv ./results.txt ./client-results.txt

sftp -i $key_path ubuntu@$server_dns <<EOF

cd engg_533/
get results.txt
rm results.txt

exit
EOF

mv ./results.txt ./server-results.txt
