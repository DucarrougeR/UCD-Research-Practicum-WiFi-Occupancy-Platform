import zipfile, os, re

def unzip(zip_path, room_path=None):
    """ Fully unzips a zipped folder full of zip files. """
    if zipfile.is_zipfile(zip_path):
        with zipfile.ZipFile(zip_path) as m_zip:
            if not room_path:
                folder_path = zip_path[0:zip_path.find(".zip")]
            else:
                folder_path = room_path

            # Iterates through items in the zip file.
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            print("extracting" + zip_path)

            zipfile.ZipFile(zip_path, "r").extractall(folder_path)

            for item in m_zip.namelist():
                if zipfile.is_zipfile(folder_path + "/" + item):
                    # Regex match to get room number.
                    room = re.match(r"Client_Count_CSCI_([A-Z]\-\d{2})", item)
                    room_dir_path = folder_path + "/" + room.groups()[0]

                    if not os.path.exists(room_dir_path):
                        os.makedirs(room_dir_path)

                    # Unzips this file.
                    unzip(folder_path + "/" + item, room_dir_path)
                    os.remove(folder_path + "/" + item)
                else:
                    print(folder_path + item + " is not a zip")

            m_zip.close()
    else:
        print(zip_path + " is not zip")


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
