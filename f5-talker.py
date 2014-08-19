__author__ = 'info@techietek.com'

import sys
try:
    import pycontrol.pycontrol as pc
except:
    print "please install pycontrol 'pip install pycontrol'"
    sys.exit()
from optparse import OptionParser
from urllib2 import URLError

def main():

    parser = OptionParser()
    parser.add_option("-u", "--user", dest="username", help="")
    parser.add_option("-p", "--pass", dest="password", help="")
    parser.add_option("-d", "--device", dest="device", help="")
    parser.add_option("-t", "--type", dest="type", help="vip_ip_comb or pool")

    (options, args) = parser.parse_args()

    if not options.username or not options.password or not options.device or not options.type:
        parser.print_help()
        sys.exit()
    # The constructor is similar to the original pyControl.
    # Note the change from wsdl_files to wsdls, which makes more sense.
    try:
        b = pc.BIGIP( hostname = options.device,
                      username = options.username,
                      password = options.password,
                      fromurl = True,
                      wsdls = ['LocalLB.VirtualServer','LocalLB.Pool','LocalLB.PoolMember'])

        v = b.LocalLB.VirtualServer
        p = b.LocalLB.Pool

        vs_list = v.get_list()
        vs_list_dest = v.get_destination(virtual_servers = vs_list)
        pool_list = v.get_default_pool_name(virtual_servers = vs_list)
        pool_members = p.get_member(pool_names = pool_list)

        pool_list_raw = p.get_list()
        pool_members_raw = p.get_member(pool_names = pool_list_raw)
        pool_monitor = p.get_monitor_association(pool_names = pool_list_raw)

        combined = zip(vs_list, vs_list_dest, pool_list, pool_members)

        resultFile = open("output-{0}-{1}.csv".format(options.type, options.device),'wb')

        if 'vip_ip_comb' in options.type:
            # write headings
            resultFile.write("vs-name :: vs-address:port :: pool :: poolmembers\n")

            for x in combined:
                members = []

                for vip in x[1]:
                    if 'address' in vip[:2][0]:
                        vsAddress = str(vip[:2][1])
                    if 'port' in vip[:2][0]:
                        vsPort = str(vip[1])

                # get pool members
                for y in x[3]:
                    members.append("{0}:{1}".format(str(y['address']),str(y['port'])))

                poolName = str(x[2])
                vsName = str(x[0])
                line = "{0} :: {1}:{2} :: {3} :: {4}\n".format(vsName, vsAddress, vsPort, poolName, ", ".join(members))
                resultFile.write(line)

        elif 'pool' in options.type:

            combined_pools = zip(pool_list_raw, pool_members_raw, pool_monitor)

            # write headings
            resultFile.write("pool_name :: pool_members\n")

            for x in combined_pools:

                members = []
                # print pool members
                for y in x[1]:
                    members.append("{0}:{1}".format(str(y['address']),str(y['port'])))

                resultFile.write("{0} :: {1}\n".format(str(x[0]), ", ".join(members)))

        print "output-{0}-{1}.csv".format(options.type, options.device)
        resultFile.close()

    except URLError as e:
        print "Unable to connect to ({0})".format(options.device)

if __name__ == '__main__':
    main()


