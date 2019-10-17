class Module(object):
    """ Base module class used to implement new modules
        for the tool. Inherit this class and override the
        run and get_parser method to expose a new module.
    """
    def __init__(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        """ Override this method for the invocation of a module.
            
            It should accept args that match the exposed arguments
            from the get_parser() function.
        """
        raise NotImplementedError("{}\n{}".format(
            "Run functionnot implemented for module",
            "Suggestion: override method run()"
        ))

    def print_help(self):
        parser = self.get_parser()
        parser.print_help()

    @property
    def description(self):
        """ Returns back the description exposed by the parser """
        try:
            return self.get_parser().description
        except:
            pass # Problem loading our argparser
        return None

    @staticmethod
    def get_parser():
        """ Override this method with a valid argparser.

            It should expose any arguments that would be required to
            invoke the run() method.
        """
        raise NotImplementedError("{}\n{}".format(
            "Argument parser must be implemented for module",
            "Suggestion: override staticmethod get_parser()"
        ))