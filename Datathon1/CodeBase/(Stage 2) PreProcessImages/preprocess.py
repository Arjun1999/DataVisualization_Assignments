import os
import shutil

org_fnames = []
data_source_dir = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/CD732-Datathon-1-20200828T160947Z-001/CD732-Datathon-1/SSS/"
for filename in os.listdir(data_source_dir):
    if(filename[-4:] == ".csv"):
        org_fnames.append(filename[:-4])

# print(org_fnames)
data_source_dir_temp = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/SSSImages/"
concatenated_path = "/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/SSS_Output/"
for filename in os.listdir(data_source_dir_temp):
    # print(filename)
    if(filename[-4:] == ".jpg"):
        for i in range(len(org_fnames)):
            # print("Org fname : ", org_fnames[i][4:15])
            # print("Filename : ", filename)
            if(org_fnames[i][4:15] == filename[:-4]):
                # print(str(int((org_fnames[i][:3]))))
                shutil.copyfile(os.path.join(data_source_dir_temp, filename), os.path.join(concatenated_path, (str(int(org_fnames[i][:3])) + ".jpg")))
