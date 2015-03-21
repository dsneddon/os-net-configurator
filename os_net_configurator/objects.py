import logging
import netaddr


logger = logging.getLogger(__name__)

class IPIndexError(ValueError):
    pass

class Subnet(object):
    """Base class for Subnet objects."""

    def __init__(self, ip_netmask, name="", **kwargs):
        """Initialize the Subnet object.

        :param network: Network/mask ('10.0.0.0/8' or '10.0.0.0/255.0.0.0').
        :param name: The name of the subnet (used for template matching).
        :param gateway: IP of the subnet gateway, *defaults to last host IP*.
        :param host_range: Host IP range. Defaults to IPRange(first+1, last-1).
        """
        self.ip_netmask = ip_netmask
        self.network = netaddr.IPNetwork(ip_netmask)
        logger.debug('Name: %s' % name)
        if name:
            self.name = name
        else:
            net_name = str(self.network)
            net_name = net_name.replace(".", "_")
            net_name = net_name.replace("/", "_")
            self.name = net_name
        self.host_range = ""
        self.gateway = ""
        logger.info('Subnet "%s" created with network address/netmask: %s' %
                    (self.name, repr(self.network)))
        # TODO: Improve input parameter handling
        args = {}
        for key, value in kwargs.iteritems():
            args[key] = value
        if args["gateway"]:
            self.gateway = args["gateway"]
        else:
            self.gateway = str(self.network[-2])
        if "host_range" in args:
            begin, end = args["host_range"].split(',')
            self.host_range = netaddr.IPRange(begin.strip(), end.strip())
        else:
            self.host_range = netaddr.IPRange(str(self.network[1]),
                                              str(self.network[-2]))
        logger.info('Subnet created with host_range: %s' % repr(self.host_range))
        for key, value in kwargs.iteritems():
            self.key = value

    def network_ip(self):
        return str(self.network.ip)

    def get_address(self, index, type="compute"):
        """Returns the <index>th Subnet address, or None if out of range.

        :param index: the index position of the address to retrieve
        :returns: an IPv4Address object representing the IP address.
        """
        try:
            __retval = str(self.host_range[index]) + '/' + \
                       str(self.network.prefixlen)
            return __retval
        except Exception as e:
            print e
            raise IPIndexError('index out of range for address range size!')

class IPv4Address(netaddr.IPAddress):
    """Subclass for IPv4 Addresses"""

    def __init__(self, address, assigned=False):
        netaddr.IPAddress.__init__(self, address)
        self.assigned = assigned

    def assign(self, assigned=True):
        self.assigned = assigned
