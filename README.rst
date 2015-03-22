===============================
os-net-configurator
===============================

host network configuration tool

A templating engine for use with os-net-config. The intention is for this code
to eventually be integrated into the os-net-config project.

* Free software: Apache license

Features
--------

The core aim of this project is to produce a template for os-net-config with
unique IP addresses based on an index provided by a Heat ResourceGroup. The
project consists of:

 * A CLI (os-net-configurator) which provides an interface to process a file
   containing subnets (/etc/os-net-config/subnets.yaml by default) and a
   template file (/etc/os-net-config/template.yaml by default) and replace the
   tokens in the template file with values based on the subnets file.

 * A python library which provides templating via an object model

YAML Config Examples
--------------------
 * Configure two interfaces, one with dhcp and one with a static IP and a route.
 * This will result in a host config where the second NIC on the host will get
   an IP address of 172.21.5.10 (tenant_getaddress_0 will retrieve the first IP
   in the host_range) and the gateway of 172.21.5.254 for the static route.

.. code-block:: yaml

  network_config:
    -
      type: interface
      name: nic1
      use_dhcp: true
    -
      type: interface
      name: nic2
      addresses:
        -
          ip_netmask: ${tenant_getaddress_0}
      routes:
        -
          next_hop: ${tenant_gateway}
          ip_netmask: 10.0.1.0/24

.. code-block:: yaml

  subnets:
    -
      name: tenant
      ip_netmask: 172.21.5.0/24
      gateway: 172.21.5.254
      host_range: 172.21.5.10, 172.21.5.100
