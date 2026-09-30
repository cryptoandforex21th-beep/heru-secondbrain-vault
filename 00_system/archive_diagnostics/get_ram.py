import ctypes

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ('dwLength', ctypes.c_ulong),
        ('dwMemoryLoad', ctypes.c_ulong),
        ('ullTotalPhys', ctypes.c_ulonglong),
        ('ullAvailPhys', ctypes.c_ulonglong),
        ('ullTotalPageFile', ctypes.c_ulonglong),
        ('ullAvailPageFile', ctypes.c_ulonglong),
        ('ullTotalVirtual', ctypes.c_ulonglong),
        ('ullAvailVirtual', ctypes.c_ulonglong),
        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
    ]

m = MEMORYSTATUSEX()
m.dwLength = ctypes.sizeof(m)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))

print(f"Total Physical RAM : {m.ullTotalPhys / (1024**2):.2f} MB")
print(f"Available RAM      : {m.ullAvailPhys / (1024**2):.2f} MB")
print(f"Memory Load        : {m.dwMemoryLoad}%")
