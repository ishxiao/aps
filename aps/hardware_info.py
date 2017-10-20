#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:25:29 2017

@author: ishxiao
~Email~: me@ishxiao.com

"""

__all__ = ['hardware_info']

import os
import sys
import multiprocessing

def _mac_hardware_info():
    info = dict()
    results = dict()
    for l in [l.split(':') for l in os.popen('sysctl hw').readlines()[1:]]:
        info[l[0].strip(' "').replace(' ', '_').lower().strip('hw.')] = \
            l[1].strip('.\n ')
    results.update({'cpus': int(info['physicalcpu'])})
    results.update({'cpu_freq': int(float(os.popen('sysctl -n machdep.cpu.brand_string')
                                .readlines()[0].split('@')[1][:-4])*1000)})
    results.update({'memsize': int(int(info['memsize']) / (1024 ** 2))})
    # add OS information
    results.update({'os': 'Mac OSX'})
    return results


def _linux_hardware_info():
    results = {}
    # get cpu number
    cpu_info = dict()
    for l in [l.split(':') for l in os.popen('lscpu').readlines()]:
        cpu_info[l[0]] = l[1].strip('.\n ').strip('kB')
    sockets = int(cpu_info['Socket(s)'])
    cores_per_socket = int(cpu_info['Core(s) per socket'])
    results.update({'cpus': sockets * cores_per_socket})
    # get cpu frequency directly (bypasses freq scaling)
    try:
        file = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
        cpu_freq = open(file).readlines()[0]
        cpu_freq = float(cpu_freq.strip('\n'))
        results.update({'cpu_freq': cpu_freq / (1000. ** 2)})
    except:
        cpu_freq = float(cpu_info['CPU MHz']) / 1000.
        results.update({'cpu_freq': cpu_freq})

    # get total amount of memory
    mem_info = dict()
    for l in [l.split(':') for l in open("/proc/meminfo").readlines()]:
        mem_info[l[0]] = l[1].strip('.\n ').strip('kB')
    results.update({'memsize': int(mem_info['MemTotal']) / 1024})
    # add OS information
    results.update({'os': 'Linux'})
    return results


def _win_hardware_info():
    try:
        from comtypes.client import CoGetObject
        winmgmts_root = CoGetObject("winmgmts:root\cimv2")
        cpus = winmgmts_root.ExecQuery("Select * from Win32_Processor")
        ncpus = 0
        for cpu in cpus:
            ncpus += int(cpu.Properties_['NumberOfCores'].Value)
    except:
        ncpus = int(multiprocessing.cpu_count())
    return {'os': 'Windows', 'cpus': ncpus}


def hardware_info():
    """
    Returns basic hardware information about the computer.

    Gives actual number of CPU's in the machine, even when hyperthreading is
    turned on.

    Returns
    -------
    info : dict
        Dictionary containing cpu and memory information.

    """
    try:
        if sys.platform == 'darwin':
            out = _mac_hardware_info()
        elif sys.platform == 'win32':
            out = _win_hardware_info()
        elif sys.platform in ['linux', 'linux2']:
            out = _linux_hardware_info()
        else:
            out = {}
    except:
        return {}
    else:
        return out

if __name__ == '__main__':
    print(hardware_info())