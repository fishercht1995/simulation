import subprocess
import os
import json

class IPFSNode:
    def __init__(self, node_index, base_path="./iptb_network"):
        self.node_index = node_index
        self.base_path = base_path

    def run_command(self, cmd, capture_output=True):
        """Run a shell command on a specific IPFS node."""
        full_cmd = f"iptb run --index {self.node_index} {cmd} --path {self.base_path}"
        result = subprocess.run(full_cmd, shell=True, text=True, capture_output=capture_output)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}\nError: {result.stderr.strip()}")
        return result.stdout.strip()

    def add_file(self, file_path):
        """Add a file to the IPFS node."""
        cmd = f"ipfs add {file_path}"
        output = self.run_command(cmd)
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

    def get_node_info(self):
        """Get the IPFS node information."""
        cmd = "ipfs id"
        output = self.run_command(cmd)
        info = json.loads(output)
        return info