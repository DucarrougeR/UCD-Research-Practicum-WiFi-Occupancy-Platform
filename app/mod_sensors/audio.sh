<<<<<<< HEAD
adir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; type="audio"; filename=$adir$type$now$format 
printf "date,month,year,time,maxamp" >> $filename 
while true; do 
    arecord -d 30 temp.wav 
    printf "\n$(date '+%d,%m,%Y,%H:%M:%S'),$(sox temp.wav -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2 | tr -d '[[:space:]]')" >> $filename; 
done
=======
adir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; type="audio"; filename=$adir$type$now$format 
printf "date,month,year,time,maxamp" >> $filename 
while true; do 
    arecord -d 30 temp.wav 
    printf "\n$(date '+%d,%m,%Y,%H:%M:%S'),$(sox temp.wav -n stat 2>&1 | grep 'Maximum amplitude' | cut -d ':' -f 2 | tr -d '[[:space:]]')" >> $filename; 
done
>>>>>>> 284673ca39815a91cdf0e263bb6712a8bf8cc1ca
