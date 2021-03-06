#! /usr/bin/env python
#
"""
@author: Adam Kniffen
@contact: akniffen@cisco.com
@copyright: Copyright 2016
@organization: Cisco Active Threat Analytics
@status: Development
"""

import re
import ast
import json
import time
import socket
import os
import sys
from elasticsearch import Elasticsearch
from datetime import datetime as dt
import argparse


class netmon:

    def __init__(self, logpath=False, logappend=False, elasticsearchhost=False, elasticsearchindex=False,
                 elasticsearchuser=False,
                 elasticsearchpwd=False):
        self.logpath = logpath
        self.logappend = logappend
        self.elasticsearchhost = elasticsearchhost
        self.elasticsearchindex=  elasticsearchindex
        self.elasticsearchuser = elasticsearchuser
        self.elasticsearchpwd = elasticsearchpwd

    def collectall(self):
        """
        Executes time phased collection tasks and calculates an average units / second / interface statistic
        :return: dict
        """
        resp = {}
        # collect once to start and then sleep
        start = time.time()
        _start = self.collectonce()
        time.sleep(1)
        _end = self.collectonce()
        end = time.time()
        diff = end - start

        for iface in _start:
            resp[iface] = {}
            for key in _start[iface]:
                if key == "recv_bytes":
                    resp[iface]["recv_mbps"] = float(((_end[iface][key] - _start[iface][key]) / diff) << 20 )
                else:
                    resp[iface][key] = int((_end[iface][key] - _start[iface][key]) / diff)
        resp['host'] = socket.gethostname()
        if self.logpath is not False:
            self.log2file(resp)

        if self.elasticsearchhost is not False:
            self.log2es(resp)
        else:
            return resp

    def log2file(self, resp):
        """
        Log our output to file as JSON so it can be consume with your logforwarder of choice
        :return: Nada, zip, zilch. If this fails, we're going to sys.exit(1)
        """
        try:
            if not os.path.isdir(self.logpath):
                os.mkdir(self.logpath)
            fmode = "w"
            if self.logappend is True:
                fmode = "a"
            with open(os.path.join(self.logpath, "netmon.log"), fmode) as f:
                f.write(json.dumps(resp))
                f.write("\n")
        except Exception:
            sys.exit(1)

    def log2es(self, resp):
        """
        for a more direct logging chain, you can write the results directly to the elasticsearch node and index of
        your choice.
        :return:
        """
        try:
            if self.elasticsearchuser is not False:
                es = Elasticsearch([self.elasticsearchhost], http_auth=(self.elasticsearchuser, self.elasticsearchpwd))
            else:
                es = Elasticsearch(self.elasticsearchhost)
            resp['timestamp'] = dt.utcnow()
            es.index(index=self.elasticsearchindex, doc_type='netmon', body=resp)
        except Exception:
            sys.exit(1)

    def collectonce(self):
        """
        collects /proc/net/dev and reformats into a dict. All credit for this formatter goes to
        http://stackoverflow.com/users/6946/anurag-uniyal
        :return: dict of values.
        """
        lines = open("/proc/net/dev", "r").readlines()

        columnline = lines[1]
        _, receivecols, transmitcols = columnline.split("|")
        receivecols = map(lambda a: "recv_" + a.strip(), receivecols.split())
        transmitcols = map(lambda a: "trans_" + a.strip(), transmitcols.split())

        cols = receivecols + transmitcols

        resp = {}
        for line in lines[2:]:
            if line.find(":") < 0:
                continue
            iface, data = line.split(":")
            # remove whitespace around the iface value
            iface = re.sub("\s+", "", iface)
            facedata = dict(zip(cols, data.split()))
            # clean this up, they're not all strings after all
            for key in facedata:
                facedata[key] = ast.literal_eval(facedata[key])
            resp[iface] = facedata
        return resp

