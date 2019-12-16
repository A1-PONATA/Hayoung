import os

file_path = "/home/pirl/Desktop/motion_fin_1215_shuffle_ver/fp"

# idx = 0
#
# for file in os.listdir(file_path):
#     os.rename(file_path+"/"+file, file_path+"/"+str(1000+idx)+"."+file.split(".")[1])
#     print(file_path+"/"+file)
#     print(file_path+"/"+str(1000+idx)+"."+file.split(".")[1])
#     idx+=1
#
for file in os.listdir(file_path):
    #print(file.split("jpg"))
    #print(file_path+"/"+file.split('jpg')[0]+".jpg")

    if len(file) <= 6:
        print(file.split("jpg"))
        os.rename(file_path+"/"+file, file_path+"/"+file.split('jpg')[0]+".jpg")