from PIL import Image
import  numpy as np

image_frames = []

days = np.arange(1,148)

for i in days:
    new_frame =  Image.open("/home/arjun/Desktop/Semester_7/DataVisualization/Datathon1/SSS_Output/" + str(i) + ".jpg")
    image_frames.append(new_frame)

image_frames[0].save("NewSSS_timelapse.gif", format = 'GIF', append_images = image_frames[1: ], save_all = True, duration = 100, loop = 0)