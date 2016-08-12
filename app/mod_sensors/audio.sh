adir="data/"; now=$(date "+%d-%m-%Y-%H:%M:%S"); format=".csv"; type="audio"; afilename=$adir$type$now$format 
printf "date,month,year,time,maxamp" >> $afilename 
while true; do 
    arecord -d 1 temp.wav 
    printf "\n$(date "+%d,%m,%Y,%H:%M:%S"),$(sox temp.wav -n stat 2>&1 | grep "Maximum amplitude" | cut -d ':' -f 2 | tr -d '[[:space:]]')" >> $afilename; 
done
