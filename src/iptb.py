import subprocess
import os
import json

class IPTB:
    def __init__(self, num_nodes=10, base_path="./iptb_network", node_type="localipfs"):
        self.num_nodes = num_nodes  # 当前节点数
        self.base_path = base_path  # IPTB 网络路径
        self.node_type = node_type  # 节点类型

    def run_command(self, cmd, capture_output=True):
        """Run a shell command."""
        result = subprocess.run(cmd, shell=True, text=True, capture_output=capture_output)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {cmd}\nError: {result.stderr.strip()}")
        return result.stdout.strip()

    def init_network(self):
        """Initialize the IPTB network."""
        if os.path.exists(self.base_path):
            print("Network already initialized. Skipping...")
            return
        cmd = f"iptb iptb auto -type localipfs -count {self.num_nodes} --path {self.base_path}"
        self.run_command(cmd)
        print(f"Initialized IPTB network with {self.num_nodes} nodes at {self.base_path}")

    def start_node(self, node_index):
        """Start a specific node by index."""
        cmd = f"iptb start --index {node_index} --path {self.base_path}"
        self.run_command(cmd)
        print(f"Started node {node_index}.")

    def stop_node(self, node_index):
        """Stop a specific node by index."""
        cmd = f"iptb stop --index {node_index} --path {self.base_path}"
        self.run_command(cmd)
        print(f"Stopped node {node_index}.")

    def add_node(self, node_name):
        """Add a new node to the existing network."""
        # Add a new node
        cmd = f"iptb add --count 1 --type {self.node_type} --path {self.base_path}"
        self.run_command(cmd)

        # Rename the new node's directory to the given name
        node_path = os.path.join(self.base_path, f"{self.num_nodes}")
        new_node_path = os.path.join(self.base_path, str(node_name))
        os.rename(node_path, new_node_path)

        self.num_nodes += 1
        print(f"Added new node '{node_name}' to the network.")

    def get_node_addresses(self):
        """Get multiaddresses of all nodes."""
        addresses = []
        for i in range(self.num_nodes):
            try:
                cmd = f"iptb run --index {i} ipfs id --path {self.base_path}"
                output = self.run_command(cmd)
                info = json.loads(output)
                addresses.append(info['Addresses'])
            except Exception as e:
                print(f"Failed to get addresses for node {i}: {e}")
        return addresses
