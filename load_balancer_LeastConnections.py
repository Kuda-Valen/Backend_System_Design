import time
import random

class RealTimeServerNode:
    """ Represents a stateless server node tracking its own active load """

    def __self__(self, name: str):
        self.name = name
        self.active_connections = 0    # This is the counter the Load Balancer inspects
        self.is_healthy = True

    def start_processing(self, request_id: str):
        """ Simulates a connection opening up on this server """

        self.active_connections += 1
        print(f"[{self.name}]: Accecpted Request {request_id}. (Active Load: {self.active_connections})")

    def complete_processing(self, request_id: str):
        """ Simulates a request finishing and clearing resources """

        if self.active_connections > 0:
            self.active_connections -= 1
        print(f"[{self.name}]: Compleleted Request {request_id}. (Active Load: {self.active_connections})")

class LeastConnectionsLoadBalancer:
    """ The intelligent gateway that motors concurrent connection counts """
    def __init__(self):
        self.server_pool = []

    def register_server(self, server: RealTimeServerNode):
        """ Registers an upstream server node """
        self.server_pool.append(server)
        print(f"[GATEWAY]: Register horizontal node: {server.name}")

    def route_request(self, request_id: str) -> RealTimeServerNode:
        """ Finds and returns the server with the absolute lowerst active connection count """
        healthy_servers = [s for s in self.server_pool if s.is_healthy]

        if not healthy_servers:
            print("[GATEWAY ERROR]: No healthy backends available ")
            return None

        best_server = min(healthy_servers, key=lambda server: server.active_connections)

        print(f"[GATEWAY]: Routing Request {request_id} to {best_server.name} (Current load was: {best_server.active_connections})")

        # Open the connection on the chosen server
        best_server.start_processing(request_id)
        return best_server


#====================================================================
# SIMULATION: ASYMETRIC SYSTEM TRAFFIC
#====================================================================

if __name__ == "__main__":
    print("\n---- Initializing Cluster & Gateway ---- \n")
    gateway = LeastConnectionsLoadBalancer()

    # Spin up 3 identical servers
    server_1 = RealTimeServerNode("Python-Node-1")
    server_2 = RealTimeServerNode("Python-Node-2")
    server_3 = RealTimeServerNode("Python-Node-3")

    gateway.register_server(server_1)
    gateway.register_server(server_2)
    gateway.register_server(server_3)

    print("\n--- Phase 1: Heavy Traffic Starts Stacking ---\n")
    # Simulate 4 immediate incoming requests arriving before anything finishes
    active_jobs = {}

    # User A triggers a masive PDF report
    active_jobs["Req_101"] = gateway.route_request("Req_101")
    # User B triggers another heavy report
    active_jobs["Req_102"] = gateway.route_request("Req_102")
    # User C logs in
    active_jobs["Req_103"] = gateway.route_request("Req_103")
    # User D logs in 
    active_jobs["Req_104"] = gateway.route_request("Req_104")

    print("\n--- Phase 2: Processing Finishes Asynchronously ---- \n")
    # Lets say Node 1 finsihes its job, freeing up its capacity entirelyt
    active_jobs["Req_101"].complete_processing("Req_101")

    print("\n --- Phase 3: New Traffic Arrives --- ")
    # A new student arrives (Req_105). Round Robin would blindly choose Node 2.
    # Lets see who Least Connections chooses:
    gateway.route_request("Req_105")