import time
from itertools import cycle

class StatelessServerNode:
    """ Represents an isolated, stateless Python application server instance"""

    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.is_healthy = True

    def handle_request(self, user_id: str, request_type: str) -> dict:
        """ Simulates executing stateless business logic """

        return {
            "status": "success",
            "processed_ by": f"{self.name} (Port {self.port})",
            "timestamp": time.time(),
            "data": f"Fetched academic tracking stats for Student {user_id}"
        }

class RoundRobinLoadBalancer:
    """ The central routing layer acting as the traffic cop """

    def __init__(self):
        self.server_pool = []
        self._pool_cycle = None

    def register_server(self, server: StatelessServerNode):
        """ Dynamicaly scales out the infrastructure horizontally """

        self.server_pool.append(server)
        # Re-initialize the iterator whenever the server pool size changes
        self._pool_cycle = cycle(self.server_pool)
        print(f"[SYSTEM]: Registratered horizontal server node: {server.name}")

    def route_request(self, user_id: str, request_type: str) -> dict:
        """ Applies the Round Robin algorithm to distribute incoming traffic """

        if not self.server_pool:
            return{"Status": "error", "message": "No backend instance available"}

        # Look for a healthy server in the cluster
        attempts = 0
        while attempts < len(self.server_pool):
            next_server = next(self._pool_cycle)
            attempts += 1

            if next_server.is_healthy:
                return next_server.handle_request(user_id, request_type)

        return {"status": "error", "message": "All backend servers are currently offline "}


#================================================================================
# Simulation in action (The student procastination app layout)
#================================================================================

if __name__ == "__main__":
    print("\n--- Initializing Backend Compute Layer ---\n")

    #1. Spin up three identical, horizontal, stateless server instances
    server_a = StatelessServerNode("Python-Server-A", 8001)
    server_b = StatelessServerNode("Python-Server-B", 8002)
    server_c = StatelessServerNode("Python-Server-C", 8003)

    #2. Initialize the Routing Gateway (Load Balancer)
    gateway = RoundRobinLoadBalancer()
    gateway.register_server(server_a)
    gateway.register_server(server_b)
    gateway.register_server(server_c)

    print("\n--- Simulating High Student Traffic Volume (Round Robin Distribution) ---\n")

    #3. Stream incoming student dashboard requests
    incoming_requests = [
        {"user_id": "452", "action": "get_progress"}, 
        {"user_id": "990", "action": "get_progress"},
        {"user_id": "112", "action": "get_progress"},
        {"user_id": "304", "action": "get_progress"}
    ]

    for req in incoming_requests:
        response = gateway.route_request(req["user_id"], req["action"])
        print(f"Incoming Request from User {req['user_id']} -> Routed to: {response['processed_ by']}")

    print("\n --- Simulating Fault Tolerance / Server Outage ---")

    #4. Simulate Python-Server-B crashing due to a hardware failure
    print("[ALERT]: Python-Server-B (Port 8002) has encountered a failure!")
    server_b.is_healthy = False

    print("\n --- Routing Post-Failure Traffic ---")
    #5. Verify the Load Balancer bypasses the broken server seamlessly
    for req in incoming_requests:
        response = gateway.route_request(req["user_id"], req["action"])
        print(f"Incoming Request from User {req['user_id']} -> Routed to: {response['processed_ by']}")