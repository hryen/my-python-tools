import os
import exifread
import random

# !!! 使用"/"结尾
# !!! Windows请使用"/"
# 将一个目录下的所有JPG和JPEG图片以拍摄日期重命名,例如: 20150506_123423_0000.jpg
path = "E:/backup/photos/jpg/"

dir_list = os.listdir(path)

count = 0
pass_count = 0

for file in dir_list:
    if file.lower().endswith('.jpg') | file.lower().endswith('.jpeg'):
        f = open(path + file, 'rb')
        tags = exifread.process_file(f, stop_tag='DateTimeOriginal', details=False)
        f.close()

        try:
            shooting_date = tags['EXIF DateTimeOriginal']
        except KeyError:
            print("Pass: " + file)
            pass_count = pass_count + 1
            continue

        dst_name = str(shooting_date).replace(":", "").replace(" ", "_")

        random_int = random.randint(1000, 9999)

        src_extension = os.path.splitext(file)[1].lower()

        dst_name = dst_name + "_" + str(random_int) + src_extension

        while True:
            try:
                os.rename(path + file, path + dst_name)
                break
            except FileExistsError:
                dst_name.replace(random_int, str(random.randint(1000, 9999)))
                os.rename(path + file, path + dst_name)

        count = count + 1
    else:
        print("Pass: " + file)
        pass_count = pass_count + 1
        continue

print("Renamed: " + str(count))
print("Passed: " + str(pass_count))
