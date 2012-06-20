import time,win32api,win32con
time.sleep(3)

for i in range(4):
    win32api.keybd_event(ord('X'), 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
    time.sleep(0.07)
    win32api.keybd_event(ord('X'), 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.03)
