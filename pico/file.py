import uos
import os
import time
import re
import gc

class FsHandler(object):
    def __init__(self):
        self.alarm = []
        self.free = -1
        self.total = -1
        
    def glob(self, pattern):
        res = []
        for fname in os.listdir():
            if re.match(pattern, fname):
                res.append(fname)
        return res
        

    
    def alarm(self, msg):
        self.alarm.append(msg)
        
    def filename(self):
        (year, month, day, hour, minute, sec, _, _) = time.localtime()
        return f"{year:04d}-{month:02d}-{day:02d}-{hour:02d}-{minute:02d}-{sec:02d}.csv"
    
    def clear_all(self):
        for fname in self.glob(".*csv$"):
            print(f"remove {fname}....\n")
            os.remove(fname)
            print("Done.")
            
    def remove_file(self, fname):
        try:
            print(f"remove {fname}....\n")
            os.remove(fname)
            print("Done.")
            return True
        except e:
            return False

    def save_data(self, data):
    
        (blk_sz, _, total, free, _, _, _, _, _, _) = uos.statvfs('/')

        total_bytes = blk_sz*total
        free_bytes = blk_sz*free
        
        self.free = free_bytes
        self.total= total_bytes

        free_mem = gc.mem_free()
        alloc_mem = gc.mem_alloc()
        
        print(f"Storage: total capacity : {total_bytes} bytes")
        print(f"Storage: free  capacity : {free_bytes} bytes")
        print(f"Memory free {free_mem} bytes, {alloc_mem} allocated bytes")
        
        data_to_write=""
        for gps_record in data:
            print(gps_record)
            data_to_write += str(gps_record['timestamp'])+", "+str(gps_record['lat'])+", "+str(gps_record['lon'])+", "+str(gps_record['fix'])+", "+str(gps_record['sats'])+", "+str(gps_record['alt'])+"\n"

        print(f"After: Memory free {free_mem} bytes, {alloc_mem} allocated bytes")
        
        space_needed = len(data_to_write)
        if free_bytes < space_needed:
            self.alarm(f"low disk space {free_bytes} need {space_needed}")
            return

        with open(self.filename(), "a") as f:
            f.write(data_to_write)
    

#with open('test.csv') as f:
#    lines = f.readlines()
    
#print(lines)

#uos.remove("test.csv")

#fh=open("test.csv", "a")
#fh.write("ahoj svete\n" * 1000)
#fh.close()