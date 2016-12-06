#! /usr/bin/env python
#
"""
@author: Adam Kniffen
@contact: akniffen@cisco.com
@copyright: Copyright 2016
@organization: Cisco Active Threat Analytics
@status: Development
"""

import argparse
import json
import sys

from netmon import netmon


def main():
    rp = argparse.ArgumentParser(prog='netmon',
                                 description="""A simple utility for pulling averages from /proc/net/dev""")
    rp.add_argument('--logpath', type=str, default=False, help="""the path where you want netmon.log to be written to""")
    rp.add_argument('--logappend', type=bool, default=False, help="Do you wish to append to the logfile, or simply overwrite it?")
    rp.add_argument('--eshost', type=str, default=False, help="the elasticsearch host you wish to log directly to")
    rp.add_argument('--esuser', type=str, default=False, help="The user for your authenticated ES instance")
    rp.add_argument('--espwd', type=str, default=False, help="The password to your authenticated ES instance")
    rp.add_argument('--esindex', type=str, default="netmon", help="the index you wish to write to. Defaults to netmon")
    rp.add_argument('--pprint', action="store_true", help="pretty print the output of your netmon collection task")
    args = rp.parse_args()

    # first, deal with empty calls to the client
    if len(sys.argv) == 1:
        rp.print_help()
        sys.exit(1)

    n = netmon(logpath=args.logpath, logappend=args.logappend, elasticsearchhost=args.eshost,
               elasticsearchindex=args.esindex, elasticsearchpwd=args.espwd, elasticsearchuser=args.esuser)
    out = n.collectall()

    if args.pprint:
        print json.dumps(out, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
