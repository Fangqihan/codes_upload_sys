import os
total_num = 0
for root, dirs, files in os.walk(r'C:\Users\Administrator\Desktop\CodeUP\uploads\1f80cdab-3c0a-4ed5-b3c9-1770a130c4dd'):
    # print(dirs)
    # print(root)  # 文件夹的绝对路径
    for filename in files:
        line_count = 0
        file_path = os.path.join(root,filename)
        with open(file_path, 'rb') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(b'#'):
                    continue
                line_count+=1
        total_num += line_count

print(total_num)


