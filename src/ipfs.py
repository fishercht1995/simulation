import subprocess
import os
import json

class IPFSCluster:
    def __init__(self):
        pass

    def add_file(self, node, file_path):
        """Add a file to the IPFS node."""
        cmd = f"iptb shell {node} & ipfs add {file_path}"
        output = self.run_command(cmd)
        print(output)
        cid = output.split()[-2]  # CID is the second-to-last item in output
        print(f"Added file '{file_path}' with CID {cid}")
        return cid

    def get_file(self, cid, output_path):
        """Get a file from the IPFS network."""
        cmd = f"ipfs get {cid} -o {output_path}"
        self.run_command(cmd)
        print(f"Retrieved file with CID {cid} to {output_path}")

    def connect(self, multiaddr):
        """Connect to another node."""
        cmd = f"ipfs swarm connect {multiaddr}"
        output = self.run_command(cmd)
        print(f"Connected to {multiaddr}")
        return output