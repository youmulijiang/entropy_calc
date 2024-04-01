import collections
import math
import os
import queue
from concurrent.futures import ThreadPoolExecutor
import threading
queue = queue.Queue()
lock = threading.Lock()
# 合法软件熵值为 4.8 - 7.2 之间

# 恶意软件熵值大于 7.2 (用红色标识）

def entropy_calc(text):
    entropy = 0
    for key,value in collections.Counter(text).items():
        probability = value/len(text)
        entropy += (-probability)*math.log2(probability)
    return entropy

def file_entropy_calc(path):
    if not os.path.exists(path):
        raise FileNotFoundError("该文件路径不存在")
    if os.path.isfile(path):
        with lock:
            with open(path,'rb+') as file:
                file = file.read()
            entropy_num = entropy_calc(file)
            if entropy_num > 7.2:
                print(f"The entropy of {path} is "+f"\033[1;31;31m{str(entropy_num)}\033[0m")
            if 4.8 <= entropy_num <= 7.2:
                print(f"The entropy of {path} is "+f"\033[1;32;32m{str(entropy_num)}\033[0m")
            if entropy_num < 4.8:
                print(f"The entropy of {path} is "+f"\033[1;33;33m{str(entropy_num)}\033[0m")
            check_pe(path)
            print()
            return entropy_calc(file)
       
    
    if os.path.isdir(path):
        for root,dir,file in os.walk(path):
            for file in file:
                file_path = os.path.join(root,file)
                queue.put(file_path)
        with ThreadPoolExecutor() as pool:
            while not queue.empty():
                pool.submit(file_entropy_calc,queue.get())

def check_pe(filepath):
    with open(filepath,"rb") as file:
        flag1 = file.read(2) 

        file.seek(0x3c) 

        offset = ord(file.read(1))

        file.seek(offset)

        flag2 = file.read(4) 

        if flag1==b'MZ' and flag2==b'PE\x00\x00': 
            print(filepath + ' \033[1;31;31m is a PE file.\033[0m')
        else:
            print(filepath + '\033[1;34;34m is not a PE file.\033[0m')


if __name__ == '__main__':       
    import argparse

    logo = """ 
            _                                      _      
  ___ _ __ | |_ _ __ ___  _ __  _   _     ___ __ _| | ___ 
 / _ \ '_ \| __| '__/ _ \| '_ \| | | |   / __/ _` | |/ __|
|  __/ | | | |_| | | (_) | |_) | |_| |  | (_| (_| | | (__ 
 \___|_| |_|\__|_|  \___/| .__/ \__, |___\___\__,_|_|\___|
                         |_|    |___/_____|  

author: youmulijiang

# The entropy of legitimate software is between 4.8-7.2
# Malware entropy greater than 7.2 (marked in red)
 """
    
    print(logo)

    parse = argparse.ArgumentParser()
    parse.add_argument("-f",metavar="file_path",help="Specify folder path",type=str,required=True)
    args = parse.parse_args()

    if args.f:
        file_entropy_calc(args.f)

        
                


