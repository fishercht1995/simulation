import sys
import os

# 添加 src 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(src_dir)

# 导入 IPTB 类
from iptb import IPTB
from ipfs import IPFSCluster

def main():
    # 测试 IPTB 类
    print("IPTB 0")
    iptb = IPTB(num_nodes=5, base_path="./testbed", node_type="localipfs")
    print("IPTB 1")
    iptb.init_network()
    for i in range(4):
        iptb.start_node(i)
    print("IPTB network setup tested successfully!")

    ipfs = IPFSCluster()
    ipfs.connect(1,4)
    ipfs.connect(4,1)
    print("add")
    cid = ipfs.add_file(4, "~/test")
    print(f"Get {cid}")
    ipfs.get_file(1, cid)


if __name__ == "__main__":
    main()