#!/usr/bin/env python3
from subprocess import check_output


def spl(line: str):
    [kcs, value] = line.split('=')
    key = kcs.split()[1]
    return (key, value)

def set(key, value):
    check_output(['xmodmap', '-e', f'keycode {key} = {value}'])


def swap(first, second):
    current = check_output('xmodmap -pke', shell=True).decode('utf-8').splitlines()
    [ff] = [x for x in current if first in x]
    [ss] = [x for x in current if second in x]
    kf, vf = spl(ff)
    ks, vs = spl(ss)
    print(kf, vf)
    print(ks, vs)
    set(kf, vs)
    set(ks, vf)



def main():
    # make keyboard more like Kinesis
    swap("equal plus", "grave asciitilde")

if __name__ == '__main__':
    main()
