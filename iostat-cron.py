#!/usr/bin/env python3
"""
Copyright (C) 2021  Glen Pitt-Pladdy

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


See: https://www.pitt-pladdy.com/blog/_20121016-200723_0100_iostat_on_Cacti_via_SNMP/

Version 20211109
"""

import sys
import os
import subprocess
import json


IOSTAT_COMMAND = [
    '/usr/bin/iostat',
    '-Ndkx',
    '-o', 'JSON',
    '300', '2',
]


def iostat_run():
    """Get iostat data for timeperiod"""
    proc = subprocess.run(
        IOSTAT_COMMAND,
        capture_output=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    # we only care about the stats for the timeperiod
    return data['sysstat']['hosts'][0]['statistics'][-1]['disk']

def get_mounts(devices):
    """Resolve iostat devices to mountpoints"""
    # get mounts
    mounts = {}
    with open('/proc/mounts', 'rt') as f_mounts:
        for line in f_mounts:
            device, mountpoint, _, _, _, _ = line.split(' ')
            if not device.startswith('/dev/'):
                continue
            while os.path.islink(device):
                mounts[device] = mountpoint
                device = os.path.abspath(os.path.join(os.path.dirname(device), os.readlink(device)))
            mounts[device] = mountpoint
    # resolve devices to mounts
    dev_mounts = {}
    for iostat_device in devices:
        alias_device = None
        if iostat_device.startswith('scd'):
            alias_device = 'sr' + iostat_device[3:]
        if os.path.exists(os.path.join('/dev/', iostat_device)):
            device = os.path.join('/dev/', iostat_device)
        elif os.path.exists(os.path.join('/dev/mapper/', iostat_device)):
            device = os.path.join('/dev/mapper/', iostat_device)
        elif alias_device and os.path.exists(os.path.join('/dev/', alias_device)):
            device = os.path.join('/dev/', alias_device)
        else:
            raise OSError("Can't find device: {}".format(iostat_device))
        while device not in mounts and os.path.islink(device):
            device = os.path.abspath(os.path.join(os.path.dirname(device), os.readlink(device)))
        if device in mounts:
            dev_mounts[iostat_device] = mounts[device]
        else:
            dev_mounts[iostat_device] = None
    return dev_mounts


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path to json output>")
        sys.exit(1)
    file_out = sys.argv[1]
    # get data
    iostat = iostat_run()
    mounts = get_mounts([dev['disk_device'] for dev in iostat])
    for stat in iostat:
        stat['_mountpoint'] = mounts.get(stat['disk_device'])
    # write file
    file_tmp = file_out + '_TMP{}'.format(os.getpid())
    with open(file_tmp, 'wt') as f_out:
        json.dump(iostat, f_out, sort_keys=True, indent=2)
    os.rename(file_tmp, file_out)


if __name__ == '__main__':
    main()
