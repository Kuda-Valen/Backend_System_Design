""" This is to learn to implement Load Balancer from scratch """

#  1. Server Template (class named Server)
#  2. The Balancer Container (class that hold the server pool as a list of servers)
#  3. The Load Balancer Algorithm  
#  Round Robin Load Balancer Algorithm

# Step 1: Server Template
class Server:
    def __init__ (self, name):
        self.name
        self.is_healthy = True
        self.connections = 0

    def handle_request(self, req_id: str):
        ...

# Step 2: Load Balancer Container
class LoadBalancer:
    def __init__(self, server_list):
        self.pool = server_list

    def get_next_RR_server(self, server) -> Server:
        ...

    def route_request(req_id: str) -> dict:
        ...

# Step 3: The Algorithm