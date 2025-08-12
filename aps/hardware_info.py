#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:25:29 2017
Updated on Aug 12 2025 — Improved cross-platform CPU/memory detection.

@author: ishxiao
~Email~: me@ishxiao.com

"""

__all__ = ['hardware_info']

import os
import sys
import multiprocessing
import platform

def _mac_hardware_info():
    results = {}
    try:
        info = {}
        for l in [l.split(':') for l in os.popen('sysctl hw').readlines()[1:]]:
            info[l[0].strip(' "').replace(' ', '_').lower().strip('hw.')] = \
                l[1].strip('.\n ')
        results['cpus'] = int(info.get('physicalcpu', os.cpu_count() or 0))
        try:
            freq_str = os.popen('sysctl -n machdep.cpu.brand_string').read()
            if '@' in freq_str:
                mhz = float(freq_str.split('@')[1][:-4]) * 1000
                results['cpu_freq'] = mhz
        except:
            pass
        results['memsize'] = int(int(info.get('memsize', 0)) / (1024 ** 2))
        results['os'] = 'Mac OSX'
    except Exception:
        results['cpus'] = os.cpu_count() or 'Unknown'
    return results


def _linux_hardware_info():
    results = {}
    try:
        cpu_info = {}
        for l in [l.split(':') for l in os.popen('lscpu').readlines() if ':' in l]:
            cpu_info[l[0].strip()] = l[1].strip()
        sockets = int(cpu_info.get('Socket(s)', 1))
        cores_per_socket = int(cpu_info.get('Core(s) per socket', os.cpu_count() or 1))
        results['cpus'] = sockets * cores_per_socket or os.cpu_count() or 'Unknown'

        try:
            with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq") as f:
                cpu_freq = float(f.read().strip())
                results['cpu_freq'] = cpu_freq / 1e6
        except:
            mhz = float(cpu_info.get('CPU MHz', 0))
            results['cpu_freq'] = mhz / 1000 if mhz else 'Unknown'

        try:
            mem_info = {}
            for l in [l.split(':') for l in open("/proc/meminfo").readlines()]:
                mem_info[l[0]] = l[1].strip().strip('kB')
            results['memsize'] = int(mem_info.get('MemTotal', 0)) / 1024
        except:
            results['memsize'] = 'Unknown'

        results['os'] = 'Linux'
    except Exception:
        results['cpus'] = os.cpu_count() or 'Unknown'
    return results


def _win_hardware_info():
    results = {}
    try:
        from comtypes.client import CoGetObject
        winmgmts_root = CoGetObject(r"winmgmts:root\cimv2")
        cpus = winmgmts_root.ExecQuery("Select * from Win32_Processor")
        ncpus = sum(int(cpu.Properties_['NumberOfCores'].Value) for cpu in cpus)
        results['cpus'] = ncpus
    except:
        results['cpus'] = multiprocessing.cpu_count()
    results['os'] = 'Windows'
    return results


def hardware_info():
    """
    Returns basic hardware information (CPUs, frequency, memory, OS) in a dictionary.
    Cross-platform and robust against missing system commands or keys.
    """
    try:
        if sys.platform == 'darwin':
            out = _mac_hardware_info()
        elif sys.platform == 'win32':
            out = _win_hardware_info()
        elif sys.platform.startswith('linux'):
            out = _linux_hardware_info()
        else:
            out = {}
    except Exception:
        out = {}

    # Always ensure at least 'cpus' key exists
    if 'cpus' not in out:
        out['cpus'] = os.cpu_count() or 'Unknown'
    return out


if __name__ == '__main__':
    print(hardware_info())
