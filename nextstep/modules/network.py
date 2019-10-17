import socket
import psutil
import getpass
import argparse

from datetime import datetime

from nextstep.core.utils import rebuild_cmdline
from nextstep.core.module import Module
from nextstep.core.logging import make_event, write_event


class NetworkConnection(Module):
    def __init__(self, *args, **kwargs):
        super(NetworkConnection, self).__init__(*args, **kwargs)

    def run(self, target, message):        
        if not ":" in target:
            raise ValueError("target format must be [addr:port]")

        # Split our address to get addr/port
        daddr, dport = target.split(":")

        # Convert our port to an int (raises ValueError if it fails)
        dport = int(dport)

        # Build our socket, connect and send the data
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect
            sock.connect((daddr, dport))
            
            # Actual peer name after connection
            daddr, dport = sock.getpeername()

            # Get the source addr/port
            saddr, sport = sock.getsockname()

            # Build our "payload" to send
            payload = bytes(message + "\n", "utf-8")
            payload_sz = len(payload)

            # Send our payload
            sock.sendall(payload)
            
            # Snag timestamp when we performed our action
            ts = datetime.utcnow()
        
        # Get a reference to our process
        proc = psutil.Process()

        log = make_event(
            timestamp=ts.isoformat(),
            username=getpass.getuser(),
            dest_addr=daddr,
            dest_port=dport,
            src_addr=saddr,
            src_port=sport,
            data_sent=payload_sz,
            protocol="TCP",
            process_name=proc.name(),
            command_line=rebuild_cmdline(proc.cmdline()[1:]),
            process_id=proc.pid
        )

        write_event(log)


    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description="Send network message to target")

        parser.add_argument('--target', help="destination to send data [addr:port]")
        parser.add_argument('--message', help="Data to send to target")

        return parser