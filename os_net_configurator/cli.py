import argparse
import logging
import os
import sys
import yaml
import objects
import utils

logger = logging.getLogger(__name__)

def parse_opts(argv):
    parser = argparse.ArgumentParser(
        description='Configure host network interfaces using a JSON'
        ' config file format.')
    parser.add_argument('-s', '--subnets-file', metavar='SUBNETS_FILE',
                        help="""path to the subnets configuration file.""",
                        default='/etc/os-net-config/subnets.yaml')
    parser.add_argument('-t', '--template-file', metavar='TEMPLATE_FILE',
                        help="""path to the template file.""",
                        default='/etc/os-net-config/template.yaml')
    parser.add_argument('-o', '--output-file', metavar='OUTPUT_FILE',
                        help="""path to write the configuration file.""",
                        default='/etc/os-net-config/config.yaml')
    parser.add_argument(
        '-d', '--debug',
        dest="debug",
        action='store_true',
        help="Print debugging output.",
        required=False)
    parser.add_argument(
        '-v', '--verbose',
        dest="verbose",
        action='store_true',
        help="Print verbose output.",
        required=False)
    parser.add_argument(
        '--noop',
        dest="noop",
        action='store_true',
        help="Return the configuration, without writing to output file.",
        required=False)
    #TODO: Versioning (if this does not get rolled in to os-net-config)
    #parser.add_argument('--version', action='version',
    #                    version=version.version_info.version_string())

    opts = parser.parse_args(argv[1:])

    return opts

def configure_logger(verbose=False, debug=False):
    LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
    DATE_FORMAT = '%Y/%m/%d %I:%M:%S %p'
    log_level = logging.WARN

    if verbose:
        log_level = logging.INFO
    elif debug:
        log_level = logging.DEBUG

    logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT,
                        level=log_level)

def main(argv=sys.argv):
    opts = parse_opts(argv)
    configure_logger(opts.verbose, opts.debug)
    logger.info('Using template file at: %s' % opts.template_file)
    logger.info('Using subnets file at: %s' % opts.subnets_file)

    if os.path.exists(opts.subnets_file):
        with open(opts.subnets_file) as sf:
            subnet_yaml = yaml.load(sf.read()).get("subnets")
            logger.debug('subnets JSON: %s' % str(subnet_yaml))
    else:
        logger.error('No config file exists at: %s' % opts.subnets_file)
        return 1
    if not isinstance(subnet_yaml, list):
        logger.error('No subnets defined in file: %s' % opts.subnets_file)
        return 1
    if os.path.exists(opts.template_file):
        with open(opts.template_file) as tf:
            template_raw = tf.read()
            token_match = utils.tokenize_template(template_raw)
    else:
        logger.error('No config file exists at: %s' % opts.subnets_file)
        return 1
    subnets = []
    subnet_name = ""
    for subnet in subnet_yaml:
        kwargs = {}
        if "name" in subnet:
            subnet_name = subnet["name"]
        if "gateway" in subnet:
            kwargs["gateway"] = subnet["gateway"]
        if "host_range" in subnet:
            kwargs["host_range"] = subnet["host_range"]
        logger.info('Creating subnet "%s" with parameters: %s' %
                    (subnet_name, kwargs))
        obj = objects.Subnet(subnet["ip_netmask"], subnet_name, **kwargs)
        subnets.append(obj)
    for subnet in subnets:
        logger.debug('Subnets created from config file:')
        logger.debug('Subnet created: "%s": %s' %
                     (obj.name, repr(obj.network)))
    replacements = {}
    # extract the $var or ${var} token values and get replacement values
    for token in token_match:
        token_raw = token.strip("$|{|}|")
        token_keys = token_raw.split('_')
        for i in range(0, len(token_keys)):
            token_keys[i] = token_keys[i].strip()
        replacements[token_raw] = utils.replace_token(subnets, token_keys)
    logger.debug('Field token replacements: %s' % replacements)
    rendered_config = utils.process_template(template_raw, replacements)
    if opts.noop:
        print "Rendered Config (--noop specified, not writing to file):\n"
        print rendered_config
    else:
        utils.write_output_file(opts.output_file, rendered_config)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))