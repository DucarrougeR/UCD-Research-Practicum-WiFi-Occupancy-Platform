# Writes a CSV file containing RSSI readings from the wlan0 interface 
# and the maximum amplitude in a recorded wav file in 30-second intervals. 
# Takes 1 argument, which should be a room number, e.g., B002 
dir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; filename=$dir$1$now$format 
printf "room,date,month,year,time,maxamp,rssi" >> $filename
while true; do 
    arecord -d 30 temp.wav 
    printf "\n$1,$(date "+%d,%m,%Y,%H:%M:%S"),$(sox temp.wav -n stat 2>&1 | grep "Maximum amplitude" | cut -d ':' -f 2 | tr -d '[[:space:]]')" >> $filename; 
    printf "$( iwconfig wlan0 | grep "Signal level" | cut -d '-' -f 2 | cut -d ' ' -f 1)" >> $filename; 
done
