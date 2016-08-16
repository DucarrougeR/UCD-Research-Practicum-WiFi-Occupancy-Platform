adir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; type="audio"; filename=$adir$type$now$format 
printf "date,month,year,time,maxamp" >> $filename 
while true; do 
    arecord -d 30 temp.wav 
    printf "\n$(date '+%d,%m,%Y,%H:%M:%S'),$(sox temp.wav -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2 | tr -d '[[:space:]]')" >> $filename; 
done
