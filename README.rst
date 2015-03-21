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
unique IP addresses based on an index provided by Heat ResourceGroup. The
project consists of:

 * A CLI (os-net-configurator) which provides an interface to process a file
   containing subnets (/etc/os-net-config/subnets.yaml by default) and a
   template file (/etc/os-net-config/template.yaml by default) and replace the
   tokens in the template file with values based on the subnets file.

 * A python library which provides templating via an object model

YAML Config Examples
--------------------
 * Configure two interfaces, one with dhcp and one with a static IP

.. code-block:: yaml

  network_config:
