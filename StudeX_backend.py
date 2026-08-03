"""
    StudeX is a Student procastination tracking app we are designing.
    It is the morning of starting of a new semester. A massive university influencer
    just posted a video showcasing our app's going live with all the features like "Exam Countdown & 
    Micro-Study Tracker" dashboard etc.
    Traffic spikes from 0 users and 0 requests per minute to about 100, 000 students requesting for the app.
    The backend system wasnt ready as yet, but the deadline just changed drastically

    PYTHON IMPLEMENTATION

    Write a clean python implementation demonstrating your solution
    Implement a MockDatabase class that tracks how many times it gets hit 
    (if it hits 5 times in a row, simulate a crash)
    Implement a MOckRedisCache class that stores keys and handles an 
    expiration simulation or flag.
    Implement a stateless function get_exam_countdown(user_id) that executes
    our chosen caching strategy logic, protecting the database while serving the data.
"""

class Server:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.is_healthy = True
        self.connections = 0

    def start_processing(self, req_id: str):
        self.connections += 1

    def complete_processing(self, req_id: str):
        if self.connections > 0:
            self.connections -= 1


class LCLoadBalancer:
    def __init__(self):
        self.pool = []

    def register_server(self, server: Server):
        self.pool.append(server)
        # Then we print a confirmation message that
        print(f"[GATEWAY]: Registered horizontal node: {server.name}")

    def get_least_conn_server(self) -> Server:
        ...

    def route_request(self, req_id: str) -> dict:
        """ To handle a request using least connections we will need to first 
            find a healthy server with least current connections """

        # So here we are appending all healthy servers in a new heathy_server list
        healthy_servers = [s for s in self.pool if s.is_healthy]

        # Then here we are iterating through that healthy_servers list, to see which one has least connections
        if not healthy_servers:
            print("[GATEWAY ERROR]: No healthy backends available.")
            return None

        else:
            best_server = min(healthy_servers, key=lambda server: server.active_connections)
            print(f"[GATEWAY]: Routing Request {req_id} to {best_server.name} (Current load was: {best_server.active_connections})")

            best_server.start_processing(req_id)
            return best_server

if __name__ == "__main__":
    gateway = LCLoadBalancer()
