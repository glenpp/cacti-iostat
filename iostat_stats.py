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

Thanks to:
    "Tim" - readlink error diagnosis in previous version
"""

import json
import sys


STATSFILE = '/var/local/snmp/iostat.json'


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <key>")
        sys.exit(1)
    key = sys.argv[1]
    # read data
    with open(STATSFILE, 'rt') as f_data:
        data = json.load(f_data)
    empty = 'U'
    if key == 'mountpoint':
        key = '_mountpoint'
        empty = 'Not mounted'
    elif key == 'devcount':
        print(len(data))
        return
    for stat in data:
        metric = stat.get(key)
        print(empty if metric is None else metric)


if __name__ == '__main__':
    main()
