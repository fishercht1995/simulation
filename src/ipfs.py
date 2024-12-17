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
        try:
            # 在指定节点上运行 ipfs add 命令
            cmd = f"iptb run {node} ipfs add -q {file_path}"
            output = self.run_command(cmd)
            cid = output.strip().split()[-1].strip()  # 获取返回的 CID
            print("$$$$$$$$$$ {} $$$$$$$".format(cid))
            print(f"节点 {node}: 添加文件 '{file_path}'，CID 为 {cid}")
            return cid
        except Exception as e:
            print(f"Failed to add file on node {node}: {e}")
            return None

    
    def connect(self, node1, node2):
        cmd = f"iptb connect {node1} {node2}"

    def get_file(self, node, cid, output_dir="~/downloads"):
        """Get a file from the IPFS network on the specified node."""
        try:
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 在指定节点上运行 ipfs get 命令，使用引号包裹命令字符串
            cmd = f"iptb run {node} 'ipfs get {cid}'"
            self.run_command(cmd)
            print(f"节点 {node}: 成功获取 CID '{cid}' 的文件到 '{output_dir}' 目录。")
        except Exception as e:
            print(f"Failed to get file on node {node}: {e}")
            print(cmd)
