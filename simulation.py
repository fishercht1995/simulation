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
from ipfs import IPFSCluster
import time
from event import AddFileEvent, GetFileEvent, LargeScaleFailureEvent
import random

seed = 4

class SimulationWorkload:
    def __init__(self):
        self.event = []
        self.cids = {}

    def log_event(self, event):
        """记录事件到事件列表中。"""
        self.events.append(event)
        print(event)

    def update_cids(self, filename, cid):
        self.event[filename] = cid

    def add_file_event(self, node, file_name):
        """记录添加文件事件。"""
        event = AddFileEvent(node=node, file_name=file_name)
        self.log_event(event)

    def get_file_event(self, node, cid):
        """记录获取文件事件。"""
        event = GetFileEvent(node=node, cid=cid)
        self.log_event(event)

    def large_scale_failure_event(self, failure_nodes):
        """记录大规模节点失败事件。"""
        event = LargeScaleFailureEvent(failure_nodes=failure_nodes)
        self.log_event(event)
    
    def show_event_log(self):
        """打印所有记录的事件。"""
        print("\n--- Event Log ---")
        for event in self.events:
            print(event)

class IPFSSimulation:
    def __init__(self, num_nodes=5):
        self.num_nodes = num_nodes
        self.iptb = IPTB(num_nodes=num_nodes, node_type="localipfs")
        self.ipfs = IPFSCluster()
        self.graph = None  # 保存生成的图结构
        self.events = []

    def generate_graph(self):
        """生成一个随机无向图。"""
        self.graph = nx.erdos_renyi_graph(self.num_nodes, 0.5, seed = seed)  # 生成一个随机图，连边概率为 0.5
        print("Generated Graph:")
        print(self.graph.edges())

    def init_nodes(self):
        """初始化 IPFS 网络节点。"""
        self.iptb.init_network()
        self.iptb.start()
        time.sleep(30)
        print(f"Initialized {self.num_nodes} IPFS nodes.")

    def connect_nodes(self):
        """根据图的边连接 IPFS 节点。"""
        print("Connecting nodes based on the graph edges...")
        for edge in self.graph.edges():
            node1, node2 = edge
            print(f"Connecting node {node1} to node {node2}...")
            self.ipfs.connect(node1, node2)
            time.sleep(1)  # 确保连接命令有时间完成
        print("All nodes connected based on the graph.")


    def run_simulation(self):
        """运行完整的 IPFS 网络模拟流程。"""
        self.generate_graph()
        self.init_nodes()
        self.connect_nodes()



def generate_custom_workload(replica, N, wt, fn, fnt):
    """生成自定义的 workload。"""
    workload = SimulationWorkload()
    # 1. Time 0: 添加 3 个 Add File 事件
    file_names = []
    print("\n--- Generating Add File Events at Time 0 ---")
    for _ in range(replica):
        node = random.randint(0, N)
        file_name = "~/test"
        workload.add_file_event(node=node, file_name=file_name)
        file_names.append(file_name)
        

    # 2. Time 0-200s: 生成 30 个 Get File 事件
    print("\n--- Generating 30 Get File Events between 0-200s ---")
    for _ in range(30):
        node = random.randint(0, N)
        file_name = random.choice(file_name)  # 从前面生成的 CID 中随机选择
        event_time = random.randint(0, wt)  # 时间在 0 到 200s 之间
        workload.get_file_event(node=node, cid=file_name, event_time=event_time)

    # 3. Time 300s: 生成 Large Scale Failure 事件
    print("\n--- Generating Large Scale Failure Event at 300s ---")
    failure_nodes = random.sample(range(0, N), fn)  # 从 0-99 随机选择 30 个节点
    workload.large_scale_failure_event(failure_nodes=failure_nodes, event_time=fnt)

    return workload


if __name__ == "__main__":
    # 设置节点数量
    workload = generate_custom_workload(3, 100, 200, 30, 300)
    """
    NUM_NODES = 5

    # 初始化 Simulation 类
    simulation = IPFSSimulation(num_nodes=NUM_NODES)

    # 运行模拟
    simulation.run_simulation()
    """