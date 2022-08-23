import os
j = os.path.join
dirs = os.listdir()
for file_name in dirs:
    if not file_name.endswith('.py'):
        idx = file_name.rfind('.')
        new_name = file_name[:idx]+'-由博文-04931901'+file_name[idx:]
        os.rename(file_name, new_name)
