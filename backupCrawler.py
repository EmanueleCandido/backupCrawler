### Crawl the filesystem from target dir.
### Confont each file with the namesake in the backup dir.
### Copy each file not present in the backup dir
### or newer than the namesake stored in the backup dir.

from shutil import copy2 as shcopy2
import os
target_dir = "/home/target"
backup_dir = "/home/backup"

### Main recursive function 
def dir_crawler(dir_crawled, backup_create=True):
    curr_dir=os.scandir(dir_crawled)

    ### Create backup dir based on the current analyzed one if not present
    if backup_create :
        bk_subdir = backup_dir + dir_crawled[len(target_dir):]
        if os.path.isdir(bk_subdir) :
            pass
        else :
            os.mkdir(bk_subdir)

    ### Crawl or copy for each file in current dir
    for element in curr_dir :
        if os.path.isdir(element) :
            next_dir = dir_crawled + "/" + element.name
            dir_crawler(next_dir)
        elif os.path.isfile(element) :
            file_path = dir_crawled + "/" + element.name
            file_mtime = os.path.getmtime(file_path)
            bk_file = backup_dir + file_path[len(target_dir):]

            ### Skip copy if file already backuped and mod time of
            ### the original file is not greater than the backuped one
            if os.path.exists(bk_file) :
                bk_file_mtime = os.path.getmtime(bk_file)
                if file_mtime <= bk_file_mtime :
                    continue

            shcopy2(file_path, bk_file)
        else :
            print("STRANGE %s" % element.name)

### Main
dir_crawler(target_dir, False)
