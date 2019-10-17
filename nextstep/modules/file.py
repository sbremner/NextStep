import os
import shlex
import psutil
import getpass
import argparse

import pathlib
from datetime import datetime

from nextstep.core.utils import rebuild_cmdline
from nextstep.core.module import Module
from nextstep.core.logging import make_event, write_event


class CreateFile(Module):
    def __init__(self, *args, **kwargs):
        super(CreateFile, self).__init__(*args, **kwargs)

    def run(self, path, overwrite=False):
        p = pathlib.Path(path)

        # Checks if path exists
        if p.exists() and overwrite == False:
            raise FileExistsError("File at path already exists (use --overwrite to force)")

        # Gets our directory
        pdir = pathlib.Path(p.parent)
        
        # Create directory if we don't already exist
        if not pdir.exists():
            pdir.mkdir(parents=True, exist_ok=True)

        # Snag timestamp when we performed our action
        ts = datetime.utcnow()

        # "Touch" the file
        p.touch()

        # Get a reference to our process
        proc = psutil.Process()

        log = make_event(
            timestamp=ts.isoformat(),
            username=getpass.getuser(),
            path=path,
            activity="CREATE",
            process_name=proc.name(),
            command_line=rebuild_cmdline(proc.cmdline()[1:]),
            process_id=proc.pid
        )

        write_event(log)

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description="Creates a new file at specified location")

        parser.add_argument('--path', help="Path of file to create")
        parser.add_argument('--overwrite', action="store_true", default=False, help="Overwrite file if it exists")

        return parser


class ModifyFile(Module):
    OPEN_MODES = ('a', 'w',)

    def __init__(self, *args, **kwargs):
        super(ModifyFile, self).__init__(*args, **kwargs)

    def run(self, path, text, mode="a"):
        p = pathlib.Path(path)

        # Checks if path exists
        if not p.exists():
            raise FileNotFoundError("File at path does not exist")

        # Ensure we are using a valid open mode for our file
        if mode not in self.OPEN_MODES:
            raise ValueError("Invalid open mode: {}".format(mode))

        # Snag timestamp when we performed our action
        ts = datetime.utcnow()

        # Open our file up and write our text out
        with open(str(p), mode=mode) as f:
            f.write(text)

        # Get a reference to our process
        proc = psutil.Process()

        log = make_event(
            timestamp=ts.isoformat(),
            username=getpass.getuser(),
            path=path,
            activity="MODIFY",
            process_name=proc.name(),
            command_line=rebuild_cmdline(proc.cmdline()[1:]),
            process_id=proc.pid
        )

        write_event(log)

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description="Modifies a files content")

        parser.add_argument("--path", help="Path of the file to modify")
        parser.add_argument("--mode", default="a", type=str, choices=["w", "a"], help="Modify in write or append mode")
        parser.add_argument("--text", type=str, help="Data to add to file")

        return parser


class DeleteFile(Module):
    def __init__(self, *args, **kwargs):
        super(DeleteFile, self).__init__(*args, **kwargs)

    def run(self, path):
        p = pathlib.Path(path)

        # Checks if path exists
        if not p.exists():
            raise FileNotFoundError("File at path does not exist")

        # Snag timestamp when we performed our action
        ts = datetime.utcnow()

        # Remove the file at our provided path
        os.remove(str(p))

        # Get a reference to our process
        proc = psutil.Process()

        log = make_event(
            timestamp=ts.isoformat(),
            username=getpass.getuser(),
            path=path,
            activity="DELETE",
            process_name=proc.name(),
            command_line=rebuild_cmdline(proc.cmdline()[1:]),
            process_id=proc.pid
        )

        write_event(log)

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description="Deletes a specified file")

        parser.add_argument("--path", help="Path of the file to delete")

        return parser