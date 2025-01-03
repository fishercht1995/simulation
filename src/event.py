from abc import ABC, abstractmethod
import time

class Event(ABC):
    """Abstract base class for all events."""
    def __init__(self, event_type):
        self.event_type = event_type

    @abstractmethod
    def __repr__(self):
        """Abstract method for string representation of the event."""
        pass

class AddFileEvent(Event):
    """Event for adding a file to a node."""
    def __init__(self, node, file_name, timestamp):
        super().__init__(event_type="ADD_FILE")
        self.node = node
        self.file_name = file_name
        self.timestamp = timestamp

    def __repr__(self):
        return f"[{self.timestamp}] ADD_FILE: '{self.file_name}' added at Node {self.node}"

class GetFileEvent(Event):
    """Event for retrieving a file from the network."""
    def __init__(self, node, cid, timestamp):
        super().__init__(event_type="GET_FILE")
        self.node = node
        self.cid = cid
        self.timestamp = timestamp

    def __repr__(self):
        return f"[{self.timestamp}] GET_FILE: CID '{self.cid}' fetched at Node {self.node}"
    
class LargeScaleFailureEvent(Event):
    """Event for simulating a large-scale node failure."""
    def __init__(self, failure_nodes, timestamp):
        super().__init__(event_type="FAILURE")
        self.failure_nodes = failure_nodes
        self.timestamp = timestamp

    def __repr__(self):
        return f"[{self.timestamp}] FAILURE: Nodes {self.failure_nodes} failed"
