from string import Template

def process_template(template, replacements):
    """Perform string.template substitution based on the replacement dict.

    :param template: The raw template with tokens to be replaced.
    :param replacements: A dict of tokens with replacement values
    :return config: The raw os-net-config.yaml produced from the template.
    """
    template_obj = Template(template)
    return template_obj.safe_substitute(replacements)

def replace_token(subnets, token_keys):
    """Replace field tokens with values

    :param subnet: Subnet object to use for replacement
    :param token_keys: token keys in the form "<subnet>_<property>" or
                       "<subnet>_<method>_<parameter>"
    :return: replacement
    """
    if len(token_keys) > 5:
        # Subnet referenced in the form 10_0_0_0_8 rather than by name
        subnet_ip_netmask = '.'.join(token_keys[0:4])
        print "Subnet ip_netmask: %s" % subnet_ip_netmask

    for subnet in subnets:
        token_subnet = token_keys[0]
        if token_subnet == subnet.name:
            if token_keys[1] == "getaddress":
                return subnet.get_address(int(token_keys[2]))
            if (token_keys[1] == "ip") and (token_keys[2] == "netmask"):
                return getattr(subnet, token_keys[1] + '_' + token_keys[2])
            else:
                return getattr(subnet, token_keys[1].strip())

def write_output_file(path, data):
    """Write the os-net-config configuration to a file specified by :path.

    :param path: The path to the file to be written
    :param data: The data to be written as a string
    """
    try:
        with open(path, 'w') as file:
            file.write(data)
    except IOError as e:
        print "Could not write to file %s: %s" % (path, e)
