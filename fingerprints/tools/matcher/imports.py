import os
import platform
from config.settings import BASE_DIR
from ctypes import *


"""
    Если проект запускать под OS Windows, то нужна библиотека UFMatcher.dll
    Если проект запускать на Unix подобных системах: libNFIQ2.so, libUFMatcher.so
"""
current_os = platform.system()

if current_os == 'Windows':
    ufm_lib = CDLL(os.path.join(BASE_DIR, 'fingerprints/tools/matcher/UFMatcher.dll'))
else:
    CDLL('/lib/x86_64-linux-gnu/libusb-1.0.so', mode=RTLD_GLOBAL)
    ufm_lib = CDLL(os.path.join(BASE_DIR, 'fingerprints/tools/matcher/libUFMatcher.so'), mode=RTLD_GLOBAL)

