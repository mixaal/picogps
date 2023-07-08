import time

start_time = time.time()
ticks_ms = time.ticks_ms()

# this method is here since I can't convince my rpi pico to
# output sub-second precision: time.time() returns seconds,
# time.time_ns() returns zeros on sub-second position, i.e.
# it's the same information value as time.time()
def time_ms():
    return start_time*1000 + time.ticks_ms() - ticks_ms

        
        
    