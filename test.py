import sys
import os

# 添加 src 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(src_dir)

# 导入 IPTB 类
from iptb import IPTB

def main():
    # 测试 IPTB 类
    print("IPTB 0")
    iptb = IPTB(num_nodes=5, base_path="./testbed", node_type="localipfs")
    print("IPTB 1")
    iptb.init_network()
    print("IPTB 2")
    iptb.start_node(0)
    print("IPTB 3")
    iptb.stop_node(0)
    print("IPTB network setup tested successfully!")

if __name__ == "__main__":
    main()