import re
import objects
import logging
from string import Template

logger = logging.getLogger(__name__)

def tokenize_template(template):
    """Extract out the tokens from a yaml template

    :param template: The os-net-config template with tokens to be replaced
    :return list: Returns a list of the tokens in the template
    """
    token = re.compile('\$\{.*\}')
    token_match = token.findall(template)
    logger.debug('Tokens matched: %s' % token_match)
    return token_match

def process_template(template, replacements):
    """Perform string.template substitution based on the replacement dict.

    :param template: The raw template with tokens to be replaced.
    :param replacements: A dict of tokens with replacement values
    :return config: The raw os-net-config.yaml produced from the template.
    """
    template_obj = Template(template)
    return template_obj.safe_substitute(replacements)

def token_query(subnet, token_keys):
    if token_keys[1] == "address":
        return subnet.address(int(token_keys[2]))
    elif (token_keys[1] == "ip") and (token_keys[2] == "netmask"):
        return getattr(subnet, token_keys[1] + '_' + token_keys[2])
    else:
        return getattr(subnet, token_keys[1].strip())

def replace_token(subnets, token_keys):
    """Replace field tokens with values

    :param subnet: Subnet object to use for replacement
    :param token_keys: token keys in the form "<subnet>_<property>" or
                       "<subnet>_<method>_<parameter>"
    :return: replacement
    """
    token_processed = False
    token_keys_ip = False
    if len(token_keys) > 5:
        # Subnet referenced in the form IP10_0_0_0_8 rather than by name
        subnet_ref = token_keys[0].strip('IP') + '.'
        subnet_ref += '.'.join(token_keys[1:4]) + '/' + token_keys[4]
        token_keys_ip = token_keys
        token_keys = [subnet_ref]
        for token in token_keys_ip[5:]:
            token_keys.append(token)

    for subnet in subnets:
        if (token_keys[0] == subnet.name) or\
                (token_keys[0] == subnet.ip_netmask):
            return token_query(subnet, token_keys)
    if token_keys_ip:
        # Subnet referenced not found, create subnet and process query
        new_subnet = objects.Subnet(subnet_ref, name="")
        return token_query(new_subnet, token_keys)

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
