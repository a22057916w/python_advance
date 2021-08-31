import os

if __name__ == "__main__":
    curr_dir = os.getcwd()    # get working directory
    filenames = os.listdir(os.path.join(curr_dir, "data"))  # rd file names from /data

    map = {}

    # iterate through list
    for file in filenames:
        res = file.split('_')
        serial_num = res[0]
        date = res[1]

        if serial_num not in map:
            map[serial_num] = date
        else:
            if date > map[serial_num]:
                map[serial_num] = date
    #print(map)

    out_dir = os.path.join(curr_dir, "output")
    os.makedirs(out_dir, 0o777, True)   # makedirs(name, mode(octal), exist_ok)

    # iterate therough dictionary
    for key in map:
        open(os.path.join(out_dir, key + "_" + map[key]), 'x').close()  # x for 'create'
