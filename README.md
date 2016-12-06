**What Is It**
A simple, python utility that samples /proc/net/dev for interface statistics, converts the output to JSON, computes 
averages in units / second, and provides simple methods to either log the JSON to file or directly insert it to ElasticSearch.

**Sample Output**


**Installation:**

sudo python setup.py install



**Usage with filebeat as a log forwarder**

In netmon/beats you'll find a sample filebeat.yml and filebeat.conf file to help with configuring Elastic FileBeats 
output to Logstash and then Elasticsearch. 



**Usage with the local forwarder agent**

Provide an elasticsearch host, index name (optional, default is netmon), and username/password (optional)

elasticsearch>=2.0.0