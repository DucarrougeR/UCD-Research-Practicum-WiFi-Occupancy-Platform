import sys, os, time

def monitor(room):
    # Calls Bash to generate the CSV file and print headings. 
    """
    cmd = 'dir="data/"; now=$(date "+%d-%m-%Y-%H:%M:%S"); format=".csv"; filename=$dir$1$now$format; printf "room,date,month,year,time,face" >> $filename'
    os.system(cmd)
    """
    
    while True: 
        # For 30 seconds:
        loop_time = time.time() + 30
        while time.time() < loop_time:
            # Run face-detection algorithm. 

            # Writes to the outfile. 
            date = os.popen('date "+%d,%m,%Y,%H:%M:%S"').read().strip()
            print(date)

monitor("B002")
