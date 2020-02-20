import ctypes

class Windows:
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001

    def __init__(self):
        pass

    def deny_shutdown(self):
        ctypes.windll.kernel32.SetThreadExecutionState(
            Windows.ES_CONTINUOUS | Windows.ES_SYSTEM_REQUIRED)

    def allow_shutdown(self):
        ctypes.windll.kernel32.SetThreadExecutionState(Windows.ES_CONTINUOUS)

Windows = Windows()