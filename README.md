**What Is It**

A simple, python utility that samples /proc/net/dev for interface statistics, converts the output to JSON, computes 
averages in units / second, and provides simple methods to either log the JSON to file or directly insert it to ElasticSearch.

**Sample Output**
```
          "tap0": {
            "trans_packets": 0,
            "recv_compressed": 0,
            "recv_multicast": 0,
            "recv_bytes": 33,
            "recv_drop": 0,
            "recv_packets": 0,
            "trans_compressed": 0,
            "recv_frame": 0,
            "recv_fifo": 0,
            "trans_fifo": 0,
            "recv_errs": 0,
            "trans_drop": 0,
            "trans_colls": 0,
            "trans_carrier": 0,
            "trans_errs": 0,
            "trans_bytes": 33
          },
          "ppp0": {
            "trans_packets": 24,
            "recv_compressed": 0,
            "recv_multicast": 0,
            "recv_bytes": 7029,
            "recv_drop": 0,
            "recv_packets": 24,
            "trans_compressed": 0,
            "recv_frame": 0,
            "recv_fifo": 0,
            "trans_fifo": 0,
            "recv_errs": 0,
            "trans_drop": 0,
            "trans_colls": 0,
            "trans_carrier": 0,
            "trans_errs": 0,
            "trans_bytes": 1534
          },
          "lo": {
            "trans_packets": 48,
            "recv_compressed": 0,
            "recv_multicast": 0,
            "recv_bytes": 12032,
            "recv_drop": 0,
            "recv_packets": 48,
            "trans_compressed": 0,
            "recv_frame": 0,
            "recv_fifo": 0,
            "trans_fifo": 0,
            "recv_errs": 0,
            "trans_drop": 0,
            "trans_colls": 0,
            "trans_carrier": 0,
            "trans_errs": 0,
            "trans_bytes": 12032
          },
          "host": "<hostname>",
          "eth0": {
            "trans_packets": 18,
            "recv_compressed": 0,
            "recv_multicast": 0,
            "recv_bytes": 5267,
            "recv_drop": 0,
            "recv_packets": 11,
            "trans_compressed": 0,
            "recv_frame": 0,
            "recv_fifo": 0,
            "trans_fifo": 0,
            "recv_errs": 0,
            "trans_drop": 0,
            "trans_colls": 1,
            "trans_carrier": 0,
            "trans_errs": 0,
            "trans_bytes": 7723
          }
        }
```

**Installation:**

```
sudo python setup.py install 
```

OR 

```
pip install git+https://github.com/akniffe1/netmon
```

**CLI Usage**

```
usage: netmon [-h] [--logpath LOGPATH] [--logappend LOGAPPEND]
              [--eshost ESHOST] [--esuser ESUSER] [--espwd ESPWD]
              [--esindex ESINDEX] [--pprint]

A simple utility for pulling averages from /proc/net/dev

optional arguments:
  -h, --help            show this help message and exit
  --logpath LOGPATH     the path where you want netmon.log to be written to
  --logappend LOGAPPEND
                        Do you wish to append to the logfile, or simply
                        overwrite it?
  --eshost ESHOST       the elasticsearch host you wish to log directly to
  --esuser ESUSER       The user for your authenticated ES instance
  --espwd ESPWD         The password to your authenticated ES instance
  --esindex ESINDEX     the index you wish to write to. Defaults to netmon
  --pprint              pretty print the output of your netmon collection task
  
```

**Usage with a log forwarder**

Netmon can output its JSON to a local file that you can then consume with your logforwarder of choice. The default behavior
is to overwrite each entry, though if that's not ok with your logforwarding agent you can also add the --logappend flag.

*Default behavior: overwrites the logpath/netmon.log file each time the agent is invoked*
```
netmon --logpath /path/to/your/desired/logging/location/
```
*Optional Behavior: Appends to logpath/netmon.log each time the agent is invoked*
```
netmon --logpath /path/to/your/desired/logging/location/ --logappend
```

**Usage with the builtin ElasticSearch forwarder agent**

Provide an elasticsearch host, index name (optional, default is netmon), and username/password (optional)

When written directly to Elasticsearch we also add the hostname and a timestamp value, so you can filter on the originating host

*For a vanilla elasticsearch installation (no authentication or proxy), simply add the --eshost flag and the agent will 
post to eshost/netmon/*

```
netmon --eshost localhost:9200
```

*If you've got authentication, add the --esuser and --espwd flags*

```
netmon --eshost localhost:9200 --esuser user --espwd p@sSw0rD
```

*If you want to specify a different index than 'netmon'*

```
netmon --eshost localhost:9200 --esuser user --espwd p@sSw0rD --esindex notnetmon
```

**Schedule Me**

A decent application of netmon would be to invoke it via cron job on a reasonable reporting interval (say 5 minutes) like so:
```
5   *   *   *   * netmon --eshost localhost:9200 --esindex notnetmon
