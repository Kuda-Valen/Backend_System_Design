""" This file is to contrast the difference between Round Robin and Least Connections"""

import time
import random
from itertools import cycle

requests = []
servers = []

class Request():
    def __init__(self, user_id, req_id):
        self.user_id = user_id
        self.req_id = req_id

        request = (user_id, req_id)
        requests.append(request)
    
class StatelessServerNodeRR:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.is_healthy = True

    def handle_request(self, user_id: str, request_type: str) -> dict:
        return {
            "status": "success",
            "processed_ by": f"{self.name} (Port {self.port})",
            "timestamp": time.time(),
            "data": f"Processed Request for User: {user_id}"
        }

class RRLoadBalancer:
    """ The Round Robin Traffic Cop """

    def __init__(self):
        self.server_pool = []
        self._pool_cycle = None

    def register_server(self, server: StatelessServerNodeRR):
        self.server_pool.append(server)
        self._pool_cycle = cycle(self.server_pool)
        print(f"\n[SYSTEM]: Registered horizontal server node: {server.name}")

    def route_request(self, user_id: str, request_type: str) -> dict:
        if not self.server_pool:
            return{"Status": "error", "message": "No backend instance available"}

        # so if there is self.server_pool
        attempts = 0
        while attempts < len(self.server_pool):
            next_server = next(self._pool_cycle)
            attempts += 1

            if next_server.is_healthy:
                return next_server.handle_request(user_id, request_type)

        return {"status": "error", "message": "All backend servers are currently offline "}


if __name__ == "__main__":
    print("\n === INITIALIZING BACKEND COMPUTE LAYER ===\n")
    gateway = RRLoadBalancer()

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

            elif option == 2:
                i = 0
                while i < len(requests):
                    print(requests[i])
                    i += 1

            elif option == 3:
                server_a = gateway.register_server(StatelessServerNodeRR("server_a", 8001))
                server_b = gateway.register_server(StatelessServerNodeRR("server_b", 8002))
                server_c = gateway.register_server(StatelessServerNodeRR("server_c", 8003))

                servers.append(server_a)
                servers.append(server_b)
                servers.append(server_c)

            elif option == 4:
                for req in requests:
                    response = gateway.route_request(req[0], req[1])
                    print(f"Incoming Request from user {req[0]} -> Routed to: {response['processed_ by']}")

            elif option == 5:
                print("Exiting...")
                break

            else:
                print("Invalid option! Choose a valid option")

        except ValueError as e:
            print(f"Encountered Input Error: Please pass integer options. {e}")


                
