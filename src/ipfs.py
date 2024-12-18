import subprocess
import os
import json

class IPFSCluster:
    def __init__(self):
        pass
    
    def run_command(self, cmd):
        """Run a shell command using os.popen()."""
        with os.popen(cmd) as stream:
            output = stream.read()
        if "Error" in output or "failed" in output.lower():
            raise RuntimeError(f"Command failed: {cmd}\nError: {output.strip()}")
        return output.strip()

    
    def add_file(self, node, file_path):
        """Add a file to the IPFS node."""
        try:
            # 在指定节点上运行 ipfs add 命令
            cmd = f"iptb run {node} ipfs add {file_path}"
            output = self.run_command(cmd)
            print(f"######### {output} #########")
            cid = output.strip().split()[4].strip()  # 获取返回的 CID
            return cid
        except Exception as e:
            print(f"Failed to add file on node {node}: {e}")
            return None

    
    def connect(self, node1, node2):
        cmd = f"iptb connect {node1} {node2}"
        self.run_command(cmd)

    def get_file(self, node, cid, output_dir="/root/downloads"):
        """Get a file from the IPFS network on the specified node."""
        try:
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 在指定节点上运行 ipfs get 命令，使用引号包裹命令字符串
            cmd = f"iptb run {node} ipfs get {cid} -o {output_dir}"
            self.run_command(cmd)
            print(f"节点 {node}: 成功获取 CID '{cid}' 的文件到 '{output_dir}' 目录。")
        except Exception as e:
            print(f"Failed to get file on node {node}: {e}")
            print(cmd)
