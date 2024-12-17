import sys
import os

# 添加 src 目录到模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(src_dir)

import networkx as nx
import os
import time
from iptb import IPTB
seed = 4
class IPFSSimulation:
    def __init__(self, num_nodes=5):
        self.num_nodes = num_nodes
        self.iptb = IPTB(num_nodes=num_nodes, node_type="localipfs")
        self.graph = None  # 保存生成的图结构

    def generate_graph(self):
        """生成一个随机无向图。"""
        self.graph = nx.erdos_renyi_graph(self.num_nodes, 0.5, seed = seed)  # 生成一个随机图，连边概率为 0.5
        print("Generated Graph:")
        print(self.graph.edges())

    def init_nodes(self):
        """初始化 IPFS 网络节点。"""
        self.iptb.init_network()
        self.iptb.start()
        print(f"Initialized {self.num_nodes} IPFS nodes.")

    def connect_nodes(self):
        """根据图的边连接 IPFS 节点。"""
        print("Connecting nodes based on the graph edges...")
        for edge in self.graph.edges():
            node1, node2 = edge
            print(f"Connecting node {node1} to node {node2}...")
            self.iptb.connect(node1, node2)
            time.sleep(1)  # 确保连接命令有时间完成
        print("All nodes connected based on the graph.")


    def run_simulation(self):
        """运行完整的 IPFS 网络模拟流程。"""
        self.generate_graph()
        self.init_nodes()
        self.connect_nodes()

if __name__ == "__main__":
    # 设置节点数量
    NUM_NODES = 5

    # 初始化 Simulation 类
    simulation = IPFSSimulation(num_nodes=NUM_NODES)

    # 运行模拟
    simulation.run_simulation()