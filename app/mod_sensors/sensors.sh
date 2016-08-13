dir="data/"; now=$(date "+%d-%m-%Y-%H:%M:%S"); format=".csv"; filename=$dir$now$format 
printf "date,month,year,time,maxamp,rssi"
while true; do
    arecord -d 30 temp.wav 
    printf "\n$(date "+%d,%m,%Y,%H:%M:%S"),$(sox temp.wav -n stat 2>&1 | grep "Maximum amplitude" | cut -d ':' -f 2 | tr -d '[[:space:]]')" >> $filename; 
    printf "$( iwconfig wlan0 | grep "Signal level" | cut -d '-' -f 2 | cut -d ' ' -f 1)" >> $filename; 
done
    
    

