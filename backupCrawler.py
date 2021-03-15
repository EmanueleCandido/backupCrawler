### Crawl the filesystem from target dir.
### Confont each file with the namesake in the backup dir.
### Copy each file not present in the backup dir
### or newer than the namesake stored in the backup dir.

import shutil as sh
import os.path as pth
from os import scandir
target_dir = "/home/target_dir"
backup_dir = "/home/backup"

### Main recursive function 
def dir_crawler(dir_crawled, backup_create=True):
    curr_dir=scandir(dir_crawled)

    ### Create backup dir based on the current analyzed one if not present
    if backup_create :
        bk_subdir = backup_dir + dir_crawled[len(target_dir):]
        if pth.isdir(bk_subdir) :
            # print("BACKUP %s already PRESENT" % bk_subdir)
            pass
        else :
            os.mkdir(bk_subdir)
            # print("CREATED subPath BACKUP %s" % bk_subdir)

    ### Crawl or copy for each file in current dir
    for element in curr_dir :
        if pth.isdir(element) :
            # print("DIR %s" % element.name)
            next_dir = dir_crawled + "/" + element.name
            dir_crawler(next_dir)
        elif pth.isfile(element) :
            # print("FILE %s" % element.name)
            file_path = dir_crawled + "/" + element.name
            file_mtime = pth.getmtime(file_path)
            bk_file = backup_dir + file_path[len(target_dir):]

            if pth.exists(bk_file) :
                bk_file_mtime = pth.getmtime(bk_file)
                # print("FILE to copy mtime %d while backup %d" % (file_mtime, bk_file_mtime))
                if file_mtime <= bk_file_mtime :
                    continue

            # print("FILE to copy %s into target %s" % (file_path, bk_file))
            sh.copy2(file_path, bk_file)
        else :
            print("STRANGE %s" % element.name)

### Main
dir_crawler(target_dir, False)
