rdir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; type="rssi"; filename=$rdir$type$now$format 
printf "date,month,year,time,rssi" >> $filename 
while true; do
printf "\n$(date "+%d,%m,%Y,%H:%M:%S"),$( iwconfig wlan0 \
    | grep "Signal level" | cut -d '-' -f 2 | cut -d ' ' -f 1)" >> $filename; \
    sleep 30; 
done
