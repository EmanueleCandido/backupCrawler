### ATTENTION: this script will delete your backup files.
### Use this tool carefully.

### Crawl the filesystem from target backup dir.
### Confont each file with the namesake in the original.
### Delete each file not present in the original dir
### that has the namesake stored in the backup dir older than the user specified.

import shutil as sh
import os
import argparse
from time import time as time_time
target_dir = "/home/target"
backup_dir = "/home/backup"

### Main recursive function 
def dir_cleaner(dir_crawled, empty_children = False):
    curr_dir=os.scandir(dir_crawled)
    
    ### Delete empty directories
    if next(os.scandir(dir_crawled), False) == False :
        os.rmdir(dir_crawled)
        return True

    ### Crawl and/or delete for each file in current dir
    for element in curr_dir :
        if os.path.isdir(element) :
            next_dir = dir_crawled + "/" + element.name
            dir_cleaner(next_dir)

            ### Check if directory became empty after deleting its children
            if next(os.scandir(dir_crawled), False) == False :
                os.rmdir(dir_crawled)
                return True

        elif os.path.isfile(element) :
            file_path = dir_crawled + "/" + element.name
            og_file = target_dir + file_path[len(backup_dir):]

            ### Check if file is no longer present in the original directory
            if os.path.exists(og_file) == False :
                file_mtime = os.path.getmtime(file_path)
                last_mod_occ = time_time() - os.path.getmtime(file_path)
                
                ### Check if file is old enough to be deleted
                if last_mod_occ > 24 * 60 * 60 * days_to_preserve :
                    os.remove(file_path)

        else :
            print("STRANGE %s" % element.name)

    return False

### Arguments Handling
parser = argparse.ArgumentParser(
        description = "This program delete files and directories in a backup"
        )

parser.add_argument("-d", "--days-to-preserve", required = True,
        help = "Specify since when backup files may be deleted",
        type = int )

days_to_preserve = parser.parse_args().days_to_preserve

### Main
dir_cleaner(backup_dir)
