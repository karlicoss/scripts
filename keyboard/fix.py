#!/usr/bin/env python3
# ok, xmodmap/xinitrc/xsession/autostart/etc -- I could never make it work properly.

from subprocess import check_call, check_output

def bind(kc: int, value):
    check_call(f'DISPLAY=:0 xmodmap -e "keycode {kc} = {value}"', shell=True)

current_raw = check_output('DISPLAY=:0 xmodmap -pke', shell=True).decode('utf8').splitlines()

current = []
for c in current_raw:
    ll = [x.strip() for x in c.split('=')]
    kc = int(ll[0].split()[1])
    current.append((kc, ll[1]))


def find_key(pattern: str):
    for kc, l in current:
        if pattern in l:
            return kc, l
    raise RuntimeError

tilde = find_key(' asciitilde ')
minus = find_key(' minus ')
plus  = find_key(' plus ')

# make keyboard more like kinesis
# TODO err. there is some extra layout in panel. which is empty, so maybe it doesn't have to do with key fixing script..
needs_swap = minus[0] + 1 == plus[0]
if needs_swap:
    bind(tilde[0], plus[1])
    bind(plus[0] , tilde[1])
else:
    pass


# TODO not so sure about hotkeys...
