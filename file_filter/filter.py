import os

if __name__ == "__main__":
    working_dir = os.getcwd()    # get working directory
    target_dir = os.path.join(working_dir, "test")  # dir needs to filter

    #os.chdir(target_dir)

    filenames = os.listdir(target_dir)  # rd file names from /data
    #print(filenames)
    map = {}
    for file in filenames:
        res = file.split('_')
        serial_num = res[0]
        date = res[1]

        if serial_num not in map:
            map[serial_num] = date
        else:
            if date < map[serial_num]:
                os.remove(os.path.join(target_dir, serial_num + "_" + date))
            elif date > map[serial_num]:
                os.remove(os.path.join(target_dir, serial_num + "_" + map[serial_num]))
                map[serial_num] = date
            else:
                continue


    #print(map)
