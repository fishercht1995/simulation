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
import json
from datetime import datetime

seed = 10

class SimulationWorkload:
    def __init__(self):
        self.events = []
        self.cids = {}

    def log_event(self, event):
        """记录事件到事件列表中。"""
        self.events.append(event)
        print(event)

    def update_cids(self, filename, cid):
        self.event[filename] = cid

    def add_file_event(self, node, file_name, timestamp):
        """记录添加文件事件。"""
        event = AddFileEvent(node=node, file_name=file_name, timestamp = timestamp)
        self.log_event(event)

    def get_file_event(self, node, cid, timestamp):
        """记录获取文件事件。"""
        event = GetFileEvent(node=node, cid=cid, timestamp = timestamp)
        self.log_event(event)

    def large_scale_failure_event(self, failure_nodes, timestamp):
        """记录大规模节点失败事件。"""
        event = LargeScaleFailureEvent(failure_nodes=failure_nodes, timestamp = timestamp)
        self.log_event(event)
    
    def show_event_log(self):
        """打印所有记录的事件。"""
        print("\n--- Event Log ---")
        for event in self.events:
            print(event)

class IPFSSimulation:
    def __init__(self, num_nodes=5, output_dir="/root/output"):
        self.num_nodes = num_nodes
        self.iptb = IPTB(num_nodes=num_nodes, node_type="localipfs")
        self.ipfs = IPFSCluster()
        self.graph = None  # 保存生成的图结构
        self.events = []
        self.current_time = 0  # 模拟器的当前时间
        self.output_dir = output_dir
        self.cids = {}
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


    def load_workload(self, workload):
        """加载 workload 并将事件按时间排序。"""
        self.events = sorted(workload.events, key=lambda e: e.timestamp)
        print("\n--- Workload Loaded and Sorted by Time ---")
        for event in self.events:
            print(event)

    def execute_workload(self, config):
        """执行事件，按照时间顺序逐一处理。"""
        print("\n--- Executing Workload ---")
        event_data = []  # 存储事件数据
        for event in self.events:
            print(event, event.timestamp)
            # 计算时间差并模拟时间流逝
            time_to_wait = event.timestamp - self.current_time
            if time_to_wait >= 0:
                print(f"Sleeping for {time_to_wait:.2f} seconds...")
                time.sleep(time_to_wait)
            
            # 更新当前时间
            self.current_time = event.timestamp
            start_time = time.time()
            try:
                # 执行不同类型的事件
                if isinstance(event, AddFileEvent):
                    self.handle_add_file(event)
                elif isinstance(event, GetFileEvent):
                    self.handle_get_file(event)
                elif isinstance(event, LargeScaleFailureEvent):
                    self.handle_failure(event)
                
                # 记录正常执行时间
                execution_time = time.time() - start_time
                if execution_time > 20:
                    raise TimeoutError("Execution time exceeded 20 seconds.")
            except TimeoutError:
                print(f"Event timed out: {event}")
                execution_time = 100  # 设置超时执行时间为 100
            except Exception as e:
                print(f"Unknown Error: {e}")  # 其他未知错误
                execution_time = -100
            # 记录事件数据
            event_data.append({
                "event_type": event.event_type,
                "timestamp": event.timestamp,
                "execution_time": execution_time,
                "details": event.__dict__,
            })
        
        # 保存数据到 JSON 文件
        timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(self.output_dir, f"event_log_{config.en}.json")
        with open(output_file, "w") as f:
            json.dump(event_data, f, indent=4)

        print(f"Event log saved to: {output_file}")
        
    def handle_add_file(self, event):
        """处理 Add File 事件。"""
        print(f"[{event.timestamp}] Handling ADD_FILE: '{event.file_name}' at Node {event.node}")
        cid = self.ipfs.add_file(event.node, event.file_name)
        self.cids = {event.file_name: cid}
    
    def handle_get_file(self, event):
        """处理 Get File 事件。"""
        print(f"[{event.timestamp}] Handling GET_FILE: CID '{event.cid}' at Node {event.node}")
        self.ipfs.get_file(event.node, self.cids[event.cid])

    def handle_failure(self, event):
        """处理 Large Scale Failure 事件。"""
        print(f"[{event.timestamp}] Handling FAILURE: Nodes {event.failure_nodes} are failing")
        for node in event.failure_nodes:
            self.iptb.stop_node(node)  # 停止失败的节点

    def generate_graph(self, r = 0.5):
        """生成一个随机无向图。"""
        self.graph = nx.erdos_renyi_graph(self.num_nodes, r, seed = seed)  # 生成一个随机图，连边概率为 0.5
        print("Generated Graph:")
        print(self.graph.edges())

    def init_nodes(self):
        """初始化 IPFS 网络节点。"""
        self.iptb.init_network()
        self.iptb.start()
        time.sleep(300)
        print(f"Initialized {self.num_nodes} IPFS nodes.")

    def connect_nodes(self):
        """根据图的边连接 IPFS 节点。"""
        print("Connecting nodes based on the graph edges...")
        for edge in self.graph.edges():
            node1, node2 = edge
            print(f"Connecting node {node1} to node {node2}...")
            self.ipfs.connect(node1, node2)
        print("All nodes connected based on the graph.")


    def run_simulation(self, config):
        """运行完整的 IPFS 网络模拟流程。"""
        self.generate_graph(config.graph)
        self.init_nodes()
        self.connect_nodes()
        print("Start run workload")
        self.execute_workload(config)



def generate_custom_workload(replica, N, request, wt, fn, fnt):
    """生成自定义的 workload。"""
    workload = SimulationWorkload()
    # 1. Time 0: 添加 3 个 Add File 事件
    file_names = []
    for _ in range(replica):
        node = random.randint(0, N)
        file_name = "~/test"
        workload.add_file_event(node=node, file_name=file_name, timestamp = 0)
        file_names.append(file_name)
        

    # 2. Time 0-200s: 生成 30 个 Get File 事件
    for _ in range(request):
        node = random.randint(0, N)
        file_name = random.choice(file_names)  # 从前面生成的 CID 中随机选择
        event_time = random.randint(2, wt)  # 时间在 0 到 200s 之间
        workload.get_file_event(node=node, cid=file_name, timestamp=event_time)

    # 3. Time 300s: 生成 Large Scale Failure 事件
    failure_nodes = random.sample(range(0, N), fn)  # 从 0-99 随机选择 30 个节点
    workload.large_scale_failure_event(failure_nodes=failure_nodes, timestamp=fnt)

    return workload

class Config:
    def __init__(self, replica, num_node, request, wt, failure_node, failure_time, graph):
        self.replica = replica
        self.num_node = num_node
        self.request = request
        self.wt = wt
        self.failure_node = failure_node
        self.failure_time = failure_time
        self.graph = graph
        self.en = "{}-{}-{}-{}-{}-{}".format(self.replica, self.num_node, self.request, self.wt, self.failure_node, self.failure_time)
        self.en += ("-g"+str(self.graph))

if __name__ == "__main__":
    # 设置节点数量
    import argparse

    # 创建解析器
    parser = argparse.ArgumentParser(description="Example script for passing parameters")

    # 添加参数
    parser.add_argument('-replica', type=int, required=True, default=3, help="replica")
    parser.add_argument('-num_node', type=int, required=True, default=100, help="num_node")
    parser.add_argument('-request', type=int, required=True, default=30, help="request")
    parser.add_argument('-wt', type=int, required=True, default=300, help="workload time")
    parser.add_argument('-fn', type=int, required=True, default=30, help="failure node")
    parser.add_argument('-ft', type=int, required=True, default=250, help="failure time")
    parser.add_argument('-graph', type=float, required=True, default=0.5, help="graph connection rate")

    # 解析参数
    args = parser.parse_args()
    NUM_NODES = 100
    # replica, num_cluster, request, workload time, failure nodes, failure time
    config = Config(args.replica, args.num_node, args.request, args.wt, args.fn, args.ft, args.graph)
    workload = generate_custom_workload(args.replica, args.num_node, args.request, args.wt, args.fn, args.ft)
    # one replica
    # request get: trace
    # join, leave,
    # user -> model, data,
    # eracoding ipfs
    # graph, node: ipfs, ed: connection
    #workload = generate_custom_workload(1, NUM_NODES, 3, 20, 3, 15)
    # 初始化 Simulation 类
    simulation = IPFSSimulation(num_nodes=NUM_NODES)
    simulation.load_workload(workload)
    # 运行模拟
    simulation.run_simulation(config)
