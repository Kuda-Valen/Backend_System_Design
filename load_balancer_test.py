""" This file is to contrast the difference between Round Robin and Least Connections"""

import time
from itertools import cycle

requests = []

class Request():
    def __init__(self, user_id: str, action: str, processing_time: float):
        self.user_id = user_id
        self.action = action
        self.processing_time = processing_time
        requests.append(self)
    
class ServerNode:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.is_healthy = True
        self.active_connections = 0

    def handle_request(self, user_id: str, action: str) -> dict:
        return{
            "processed_by": f"{self.name} (Port {self.port})",
            "active_load": self.active_connections
        }

class RRLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self._pool_cycle = cycle(self.servers)

    def route_request(self, req: Request) -> dict:
        healthy_servers = [s for s in self.servers if s.is_healthy]
        if not healthy_servers:
            return {"processed_by": "Error: No healthy servers"}

        server = next(self._pool_cycle)
        return server.handle_request(req.user_id, req.action)

class LCLoadBalancer:
    def __init__(self, servers):
        self.servers = servers

    def route_request(self, req: Request) -> dict:
        healthy_servers = [s for s in self.servers if s.is_healthy]
        if not healthy_servers:
            return {"processed_by": "Error: No healthy servers"}

        best_server = min(healthy_servers, key=lambda s: s.active_connections)
        initial_load = best_server.active_connections

        best_server.active_connections += 1
        response = best_server.handle_request(req.user_id, req.action)
        response["Active_load"] = initial_load
        return response

if __name__ == "__main__":
    rr_servers = [ServerNode("RR_Server_A", 8001),
                  ServerNode("RR_Server_B", 8002),
                  ServerNode("RR_Server_C", 8003)]
    lc_servers = [ServerNode("LC_Server_A", 9001),
                  ServerNode("LC_Server_B", 9002),
                  ServerNode("LC_Server_C", 9003)]

    rr_gateway = RRLoadBalancer(rr_servers)
    lc_gateway = LCLoadBalancer(lc_servers)

    while True:
        print("\n==== SYSTEM DESIGN INTERACTIVE TERMINAL === \n")
        print("\n1. Add Requests (Light vs Heavy Workloads)")
        print("2. View All Requests Queue")
        print("3. Run Comparative Simulation")
        print("4. Clear Server Active connection loads")
        print("5. Exit")

        try:
            option = int(input("\nChoose an Option: "))

            if option == 1:
                user_id = input("Enter User ID: ")
                action = input("Enter Request Action: ")
                print("Select Weight: 1 for Light (5ms) | 2 for Heavy (4s report)")
                weight = int(input("Choice: "))

                # Simulating connections holding memory/CPU load
                load_score = 0 if weight == 1 else 3

                Request(user_id, action, load_score)
                print(f"Success: Registered asymmetric request for User {user_id}")

            # left here, working on option 2
            elif option == 2:
                if not requests:
                    print("Queue empty.")
                for idx, r in enumerate(requests):
                    type_str = "HEAVY" if r.processing_time > 0 else "LIGHT"
                    print(f"[{idx}] User: {r.user_id} | Action: {r.action} | Workload: {type_str}")

            elif option == 3:
                if not requests:
                    print("Please add requests to simulate first.")
                    continue

                print("\n--- SIMULATING ROUND ROBIN GATEWAY ---")
                for r in requests:
                    res = rr_gateway.route_request(r)
                    print(f"Incoming request -> Allocated to: {res['processed_by']}")

                print("\n--- SIMULATING LEAST CONNECTIONS GATEWAY ---")
                for r in requests:
                    res = lc_gateway.route_request(r)
                    print(f"Incoming request -> Allocated to: {res['processed_by']} (Active load was: {res['active_load']})")

                    """ If its a light request, clear the connection instantly
                        If its a heavy, leave it open to simulate a slow system database execution!"""

                    if r.processing_time == 0:
                        for s in lc_servers :
                            if s.name in res['processed_by'] and s.active_connections > 0:
                                s.active_connections -= 1

            elif option == 4:
                for s in lc_servers:
                    s.active_connections = 0
                print("All server trackin states reset.")

            elif option == 5:
                print("Exiting...")
                break

            else:
                print("Invalid option! Choose a valid option")

        except ValueError as e:
            print(f"Encountered Input Error: Please pass integer options. {e}")


                
