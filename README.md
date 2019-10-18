# NextStep

A framework built to generate activity on an endpoint. Base capabilities include the ability to spawn a process, create a file,
modify a file, delete a file and establish a network connection to
transmit data.

**Table of Contents**

- [Setup](#setup)
- [Execution](#execution)
    - [CLI](#cli)
    - [Playbooks](#playbooks)
- [Custom Modules](#custom-modules)

## Setup

Download the git package and install the requirements as follows:

```> pip install -r requirements.txt```

*Note: This has been tested on python 3.6 on Windows and Linux.*

## Execution

The program allows for two primary methods of invocation. It supports single module execution via a command line interface as well as multi-module execution via a playbook model. See below.

### CLI

The command line module allows execution of modules individually. To get a list of all available commands, use the following:

```> python main.py --help```

To see all available modules, use the `--show-module` command as follows:

```> python main.py --show-modules```

To get more information on a specific module, use the `--help` command while providing a module name:

```> python main.py --help --module process.start```

### Playbooks

Playbooks can be useful when it is necessary to execute multiple modules at a time. This allows the user to build a full testing playbook that can be run.

Playbooks are json files which contain a list of modules to execute. They are in the following format:
```json
[
    {
        "module": "file.create",
        "run": {
            "path": "sample.txt",
            "overwrite": true
        }
    },
    {
        "module": "file.modify",
        "run": {
            "path": "sample.txt",
            "mode": "a",
            "text": "Hello, Sample!"
        }
    }
]
```

To view the "run" arguments for a specific module, use the `--help` command while providing a module name:

```> python main.py --help --module file.create```

Playbooks can be executed as follows:

```> python main.py --playbook book.json```

## Custom Modules

The framework is built to be extended easily with custom modules. There are two key methods to override to get a module operational: `run()` and `get_parser()`.

The `get_parser()` method is a static method that exposes the available parameters for the CLI invocation of the module. These parameters will be passed to the `run()` method when the module is executed.

A sample `get_parser()` method might look as follows:

```python
@staticmethod
def get_parser():
    parser = argparse.ArgumentParser(description="Starts a process")

    parser.add_argument('--path', help="Path of process to execute")
    parser.add_argument('--command', help="Command line arguments to include", required=False)

    return parser
```

The paired method for this is the `run()` method which should include the parameters exposed by the parser. This method will get called when the module is executed:

```python
def run(self, path, command=None):
    pass # Implement the run method here
```
