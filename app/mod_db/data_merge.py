import zipfile, os, re

def merge_logs(path, outf):
    """ Takes a directory containing folders full of log files and merges the data therein
    into a single CSV file. """
    # Opens the outfile and writes the column names.
    fout = open(outf, "w")
    headings = "room,time,assocated,authenticated\n"
    fout.write(headings)

    # Loops through every CSV file in every folder in the data directory. 
    direc = "data/CSI WiFiLogs"
    for root, dirs, files in os.walk(direc):
        for name in files:
            with open((os.path.join(root, name)), encoding = "ISO-8859-1") as fin:
                # Finds the string "Key" and reads the remainder of the file to the outfile.
                for line in fin:
                    if "Key" in line:
                        fout.write(fin.read())
    
    fout.close()
        
unzip("data/CSI WiFiLogs.zip") 
merge_logs("data/CSI WiFiLogs", "data/logs_merged.csv")
