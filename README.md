f5-talker
=========
this tool is used to query BIGIP ltm f5 How to get all pools and members or VIP address port in CSV format

f5-talker.py usage
python f5-talker.py -u admin -p xyz -d lba01.lhr6 -t pool
python f5-talker.py -u admin -p xyz -d lba01.lhr6 -t vip_ip_comb
 
Usage: f5-talker.py [options]
 
Options:
  -h, --help            show this help message and exit
  -u USERNAME, --user=USERNAME
  -p PASSWORD, --pass=PASSWORD
  -d DEVICE, --device=DEVICE
  -t TYPE, --type=TYPE  vip_ip_comb or pool 

read more here:
http://www.techietek.com/2014/07/09/bigip-f5-get-pools-members-vip-address-port-csv-format/

any questions please get in touch
