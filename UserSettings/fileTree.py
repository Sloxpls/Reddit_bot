import os


def dir_exist():
    path_to_dirs = ["assets/backgrounds/audio","assets/backgrounds/video", "assets/temp", "assets/temp/mp3", "finishedVideo"]
    for dir in path_to_dirs:
     if os.path.exists(dir):
         pass
     else:
         try:
             os.mkdir(dir)
         except:
             print("*********************************"
                   "** Somting wrong with file tree **"
                   "**********************************")