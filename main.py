import sys
import json
import logging
import inspect
import argparse

import settings

from nextstep.core.errors import ModuleNameError

from nextstep.modules.process import StartProcess
from nextstep.modules import load_module, get_modules

# Use logging module for "printing" info while we run the tool
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] - %(name)s - %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def module_banner():
    """ Prints available modules to screen """
    all_modules = get_modules()
        
    logger.info("Available modules:")
    for name, module in all_modules.items():
        logger.info("> {} | {}".format(name, module.description))
    
    logger.info('Try "--help --module [name]" for more information')


def run_module(module, *params, **kwargs):
    """ Runs our module after parsing provided params """
    # Snag our modules parser (it handles the rest of our args)
    mp = module.get_parser()

    # Parse the arguments for our modules run function    
    args, unknown = mp.parse_known_args(params)

    # Build our our invocation dictionary
    _kwargs = {}
    _kwargs.update(vars(args))
    _kwargs.update(kwargs)

    if unknown and len(unknown) > 0:
        logger.warning("Unrecognized parameters: {}".format(unknown))

    try:
        # Invoke the module
        module.run(**_kwargs)
    except Exception as ex:
        logger.error("Module raised exception during execution:\n> {}".format(ex))
        return False

    return True


def get_parser():
    parser = argparse.ArgumentParser(conflict_handler='resolve')

    parser.add_argument("--help", action='store_true')
    parser.add_argument("--show-modules", action='store_true', help="Prints available modules")
    parser.add_argument("--module", help="Name of module to run")
    parser.add_argument("--playbook", help="Json file with list of plays to run")

    return parser


def main(args=None):
    logger.info("NextStep started - loading module arguments")
    logger.info("Execution trace information located in: {}".format(settings.LOG_FILE))

    # Our NextStep parser
    parser = get_parser()

    # Grab the args we care about, keep extras for the module
    args, extras = parser.parse_known_args()

    # Print basic help here (if args.module is set, we print module's help later)
    if args.help and not args.module:
        parser.print_help()
        return

    # Check if we just want to show available modules
    if args.show_modules:
        module_banner()
        return

    # Ensure we specify a module OR a play book
    if not args.module and not args.playbook:
        logger.error("Please specify a module name or a target playbook to execute")
        parser.print_help()
        exit(-1)

    # Detect if we run a playbook here, or we are running a single module
    if args.playbook:
        with open(args.playbook, "r") as f:
            playbook = json.load(f)

        for play in playbook:
            if "module" not in play:
                logger.error("Play must contain key: 'module'")
                continue

            try:
                logger.info("Loading module: {}".format(play["module"]))

                # Load the module: play["module"]
                module = load_module(play["module"])
            except ModuleNameError as ex:
                logger.error(ex)
                continue # Skip the rest, our module didn't load properly

            # Invoke our module
            run_module(module, **play["run"])
    else:
        try:
            logger.info("Loading module: {}".format(args.module))

            # Load the module: args.module
            module = load_module(args.module)
        except ModuleNameError as ex:
            logger.error(ex)
            parser.print_help()
            exit(-1)

        # We just wanted the help for our module
        if args.help:
            mp = module.get_parser()
            mp.print_help()
        else:
            # run our module
            run_module(module, *extras)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Exit caught - quitting")
    except Exception as ex:
        print("Unhandled exception :: <{}> {}".format(type(ex), ex))
