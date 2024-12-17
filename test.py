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
    iptb = IPTB(num_nodes=5, base_path="./testbed", node_type="localipfs")
    iptb.init_network()
    iptb.start_node(0)
    iptb.stop_node(0)
    print("IPTB network setup tested successfully!")

if __name__ == "__main__":
    main()