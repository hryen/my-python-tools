# 将一个目录下的所有MP4文件和MOV文件以拍摄日期重命名,例如: 20150506_123423_0000.mov
# 2020.3.7

import os
from pymediainfo import MediaInfo
import random

path = input("Path: ")
path = path.replace("\\", "/")
if not path.endswith("/"):
    path = path + "/"

dir_list = os.listdir(path)

count = 0
pass_count = 0

for file in dir_list:
    if not file.lower().endswith('mp4') | file.lower().endswith('mov'):
        print("Pass: " + file)
        pass_count = pass_count + 1
        continue
        
    media_info = MediaInfo.parse(path + file)

    for track in media_info.tracks:
        if track.track_type == 'General':

            try:
                tagged_date = track.tagged_date[4:]
            except TypeError:
                print("Pass: " + file)
                pass_count = pass_count + 1
                continue

            tagged_date = tagged_date.replace("-", "").replace(" ", "_").replace(":", "")

            # hour + 8
            hour = tagged_date[9:11]
            hour = int(hour) + 8
            if hour < 10:
                hour = str("0" + str(hour))
            else:
                hour = str(hour)

            str_list = list(tagged_date)
            str_list[9] = hour[0]
            str_list[10] = hour[1]
            tagged_date = "".join(str_list)

            random_int = str(random.randint(1000, 9999))

            src_extension = os.path.splitext(file)[1].lower()

            dst_name = tagged_date + "_" + str(random_int) + src_extension

            while True:
                try:
                    os.rename(path + file, path + dst_name)
                    break
                except FileExistsError:
                    dst_name.replace(random_int, str(random.randint(1000, 9999)))
                    os.rename(path + file, path + dst_name)

            count = count + 1
            break

print("Renamed: " + str(count))
print("Passed: " + str(pass_count))
