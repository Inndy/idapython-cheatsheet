## Useful Enumeration Functions

Check this: https://github.com/nlitsme/idascripts/blob/master/enumerators.py

## Get Current Function Range

``` python
curr_range = xrange(GetFunctionAttr(ScreenEA(), FUNCATTR_START), GetFunctionAttr(ScreenEA(), FUNCATTR_END))
```

## Delete Struct

``` python
for i in range(999):
    DelStruc(GetStrucIdByName('sc%d' % i))
```

## Create Struct

Copy data from x64dbg dataview (pointer format), parse it and reconstruct import table structure

``` python
import clipboard # install package from pip

functions = [ line.split('!')[1].strip() for line in clipboard.paste().split('\n') ]

sid = AddStrucEx(0xffffffff, 'importable', 0)

for i, name in enumerate(functions):
    AddStrucMember(sid, name.encode('ascii'), i * 4, FF_DATA | FF_DWORD, -1, 4)
```

## Remove Function Call By Address

``` python
def patch_mov_eax(addr, v):
    PatchByte(addr, 0xb8)
    PatchDword(addr+1, v)

def nop(addr, size=5):
    for i in range(size):
        PatchByte(addr + i, 0x90)

def remove_call(addr, use_nop=True):
    if Byte(addr) in (0xe8, 0xe9):
        if use_nop:
            nop(addr, 5)
        else:
            patch_mov_eax(addr, 0)
    elif Byte(addr) in (0xff,) and Byte(addr+1) in range(0xd0, 0xd8):
        if use_nop:
            nop(addr, 2)
        else:
            PatchWord(addr, 0xc031) # xor eax, eax


def remove_all_call(addrs, use_nop=True):
    for i in addrs.split():
        remove_call(int(i, 16), use_nop)
```

## Smart MakeName

``` python
def tryMakeName(addr, name, i=0, suffix=''):
    n = name + suffix
    if LocByName(n) == addr:
        return
    while LocByName(n) != BADADDR:
        n = '%s_%d' % (name, i)
        i += 1
    MakeName(addr, n)
```

## Remove Disassembler Trap

**This script requires function from https://github.com/nlitsme/idascripts/blob/master/enumerators.py**

Replace following patterns with nop

```
jz $+3
jnz $+1
.db 0xe9 ; 0xe8
```

``` python
op_pairs = [ (0x70, 0x71), (0x72, 0x73), (0x74, 0x75), (0x76, 0x77), (0x78, 0x79), (0x7a, 0x7b), (0x7c, 0x7d), (0x7e, 0x7f) ]
for pair in op_pairs:
    patterns = [
        "%.2x 03 %.2x 01 %.2x" % (a, b, c)
        for (a, b) in [ pair, pair[::-1] ]
        for c in (0xe8, 0xe9)
    ]
    for p in patterns:
        for ea in Binaries((FirstSeg(), BADADDR), p):
            PatchDword(ea, 0x90909090); PatchByte(ea + 4, 0x90)
```
