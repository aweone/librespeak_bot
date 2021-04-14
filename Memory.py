# -*- coding: utf-8 -*-
def memory():
    with open("/proc/meminfo") as f:
        memoryfile = f.readlines()

    memorytotal = round(int(memoryfile[0].split()[1])/1024)
    memoryused = round(int(memoryfile[2].split()[1])/1024/2)
    memorystr = f'Занято памяти {memoryused}мб. из {memorytotal}мб.'
    return memorystr
#print(memory())
