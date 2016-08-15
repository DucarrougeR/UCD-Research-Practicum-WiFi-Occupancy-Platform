rdir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; type="rssi"; rfilename=$rdir$type$now$format 
printf "date,month,year,time,rssi" >> $rfilename 
while true; do
printf "\n$(date "+%d,%m,%Y,%H:%M:%S"),$( iwconfig wlan0 \
    | grep "Signal level" | cut -d '-' -f 2 | cut -d ' ' -f 1)" >> $rfilename; \
    sleep 30; 
done
