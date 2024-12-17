import subprocess
import os
import json

class IPFSCluster:
    def __init__(self):
        pass
    
    def run_command(self, cmd, capture_output=True):
        """Run a shell command on a specific IPFS node."""
        result = subprocess.run(cmd, shell=True, text=True, capture_output=capture_output)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}\nError: {result.stderr.strip()}")
        return result.stdout.strip()

    def add_file(self, node, file_path):
        """Add a file to the IPFS node."""
        cmd = f"iptb shell {node} & ipfs add {file_path}"
        output = self.run_command(cmd)
        print(output)
        cid = output.split()[-2]  # CID is the second-to-last item in output
        print(f"Added file '{file_path}' with CID {cid}")
        cmd = f"exit"
        output = self.run_command(cmd)
        return cid
    
    def connect(self, node1, node2):
        cmd = f"iptb connect {node1} {node2}"

    def get_file(self, cid, output_path):
        """Get a file from the IPFS network."""
        cmd = f"ipfs get {cid} -o {output_path}"
        self.run_command(cmd)
        print(f"Retrieved file with CID {cid} to {output_path}")
