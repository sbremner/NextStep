import os
import shlex
import getpass
import argparse
import subprocess

from pathlib import Path
from datetime import datetime

from nextstep.core.module import Module
from nextstep.core.logging import make_event, write_event


class StartProcess(Module):
    def __init__(self, *args, **kwargs):
        super(StartProcess, self).__init__(*args, **kwargs)

    def run(self, path, command=None, block=False, timeout=None):
        # Resolves/validates path is good
        p = Path(path).resolve(strict=True)
        
        # Build our execution command
        to_exec = shlex.split('"{}" {}'.format(p, command or ""))

        # Start our process/save timestamp
        ts = datetime.utcnow()

        try:
            proc = subprocess.Popen(to_exec, stdin=None, stdout=None, stderr=None, close_fds=True)

            # Block if we were asked to
            if block:
                proc.wait(timeout=timeout)

        except subprocess.CalledProcessError:
            # Another error occured
            pass
        except subprocess.TimeoutExpired:
            # Process expired
            proc.kill()

        # Returns us back an event that we want to send to our log
        log = make_event(
            timestamp=ts.isoformat(),
            username=getpass.getuser(),
            process_name=path,
            command_line=command,
            process_id=proc.pid
        )

        # Write the event for our process execution
        write_event(log)

        return True

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description="Starts a process")

        parser.add_argument('--path', help="Path of process to execute")
        parser.add_argument('--command', help="Command line arguments to include", required=False)
        parser.add_argument('--block', action="store_true", default=False, help="Block program execution until subprocess completes")
        parser.add_argument('--timeout', type=int, required=False, help="Sets timeout in seconds (requires: --block)")

        return parser