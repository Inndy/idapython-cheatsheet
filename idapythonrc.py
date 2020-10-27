import binascii
import sys
from hexdump import hexdump as _hexdump
# https://github.com/nlitsme/idascripts/raw/master/enumerators.py
from enumerators import Texts, Code, NonFuncs, Undefs, ArrayItems, Addrs, NotTails, BytesThat, Heads, Funcs, FChunks, Names

if sys.version_info.major < 3:
    bytes = str

def hexdump(data, *args, **kwargs):
    if isinstance(data, bytearray): # hexdump do not accept bytearray
        data = bytes(data)
    return _hexdump(data, *args, **kwargs)

hd = hexdump

def xorb(data, b):
    return bytearray(i ^ b for i in bytearray(data))

def xor(a, b):
    if not a or not b:
        return bytearray(b'')
    if len(a) < len(b):
        a, b = b, a
    a = bytearray(a)
    b = bytearray(b) * (len(a) // len(b) + 1)
    return bytearray(i ^ j for i, j in zip(a, b))

# for ironstrings and shellcode
def set_vivsect_arch(arch='i386'):
    import vivisect
    vivisect.defconfig['viv']['parsers']['blob']['arch'] = arch
