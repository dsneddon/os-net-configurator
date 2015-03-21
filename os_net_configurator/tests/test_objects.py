import os.path
import tempfile
import netaddr

from os_net_configurator import objects
from os_net_configurator.tests import base

class TestSubnet(base.TestCase):

    def test_Subnet(self):
        network = netaddr.IPNetwork("192.168.2.0/23")
        network_broadcast = "192.168.3.255"
        network_prefix = "23"
        subnet2 = objects.Subnet(network)
        self.assertEquals(netaddr.IPNetwork("192.168.2.0/23"),
                          subnet2.network)
        self.assertEquals(network_broadcast, str(subnet2.network.broadcast))
        self.assertEquals(23, subnet2.network.prefixlen)
        self.assertEquals(objects.IPv4Address("192.168.2.1"),
                          subnet2.get_address(0))
        self.assertEquals(objects.IPv4Address("192.168.3.254"),
                          subnet2.gateway)
        self.assertEquals(objects.IPv4Address("192.168.3.0"),
                          subnet2.get_address(255))
        self.assertRaises(ValueError, subnet2.get_address, 511)
        self.assertEquals(objects.IPv4Address("192.168.3.254"),
                          subnet2.get_address(-1))

    def test_Subnet_range(self):
        network = netaddr.IPNetwork("192.168.2.0/23")
        subnet2 = objects.Subnet(network, name="test",
                                 {"host_range":"192.168.2.10, 192.168.2.100"})
        self.assertEquals(netaddr.IPNetwork("192.168.2.0/23"),
                          subnet2.network)
        self.assertEquals(netaddr.IPAddress("192.168.2.10"),
                          subnet2.get_address(0))

    def test_IPv4Address(self):
        address = objects.IPv4Address("192.168.1.1")
        self.assertEquals(False, address.assigned)
        address.assign()
        self.assertEquals(True, address.assigned)