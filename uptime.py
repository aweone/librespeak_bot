import time


def upTime(startTime):
    days = int((time.time() - startTime)//86400)
    hours = int((time.time() - startTime - days * 86400)//3600)
    minuts = int((time.time() - startTime - days * 86400 - hours * 3600)//60)
    seconds = int((time.time() - startTime - days *
                  86400 - hours * 3600 - minuts * 60))
    return(f"{days}д. {hours}ч. {minuts}м. {seconds}c.")
