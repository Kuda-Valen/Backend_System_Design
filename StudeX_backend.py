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
            best_server = min(healthy_servers, key=lambda server: server.connections)
            print(f"[GATEWAY]: Routing Request {req_id} to {best_server.name} (Current load was: {best_server.connections})")

            best_server.start_processing(req_id)
            return best_server

class MockDatabase:
    """ This simulates a physical database engine with strict query thresholds """
    def __init__(self):
        self.hit_count = 0

    def query_exam_countdown(self) -> str:
        self.hit_count += 1
        print(f"  [DATABASE QUERY #{self.hit_count}]: Executing heavy I/O read on disk...")

        # Simulate a crash if databse gets slammed 5 times in a row
        if self.hit_count >= 5:
            raise Exception("DATABASE CRASH! CPU usage hit 100% due to connection exhaustion!")
        return "Exam Countdown: 48 Hours Remaining"

class MockRedisCache:
    """ Simulates ultra-fast RAM key-value storage """
    def __init__(self):
        self.storage = {}

    def get(self, key: str):
        # Returns cached data if hit, otherwise returns None (Cache Miss)
        return self.storage.get(key)

    def set(self, key: str, value: str):
        self.storage[key] = value
        print(f"  [REDIS WRITE]: Stored key '{key}' in RAM.")

def get_exam_countdown(user_id: str, db: MockDatabase, cache: MockRedisCache) -> str:
        cache_key = "exam_count_data"

        # 1. Check RAM Cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"   [CACHE HIT]: Served Student {user_id} directly from RAM! (0ms latency)")
            return cached_data

        print(f"   [CACHE MISS]: Student {user_id} reading from Database...")
        db_data = db.query_exam_countdown()

        # 3. Populate Cache for all future requests
        cache.set(cache_key, db_data)

        return db_data

if __name__ == "__main__":
    gateway = LCLoadBalancer()

    server_1 = Server("Python-Server-1", 8001)
    server_2 = Server("Python-Server-2", 8002)
    server_3 = Server("Python-Server-3", 8003)

    gateway.register_server(server_1)
    gateway.register_server(server_2)
    gateway.register_server(server_3)

    print("\n --- Phase 1: Heavy Traffic Starts Stacking ---")
    # Simulate 4 immediate incoming requests arriving before anything finishes
    active_jobs = {}

    active_jobs["Req_101"] = gateway.route_request("Req_101")
    active_jobs["Req_102"] = gateway.route_request("Req_102")
    active_jobs["Req_103"] = gateway.route_request("Req_103")
    active_jobs["Req_104"] = gateway.route_request("Req_104")
    active_jobs["Req_105"] = gateway.route_request("Req_105")
    active_jobs["Req_106"] = gateway.route_request("Req_106")
    active_jobs["Req_107"] = gateway.route_request("Req_107")
    active_jobs["Req_108"] = gateway.route_request("Req_108")
    active_jobs["Req_109"] = gateway.route_request("Req_109")
    active_jobs["Req_110"] = gateway.route_request("Req_110")
    active_jobs["Req_111"] = gateway.route_request("Req_111")
    active_jobs["Req_112"] = gateway.route_request("Req_112")
    active_jobs["Req_113"] = gateway.route_request("Req_113")
    active_jobs["Req_114"] = gateway.route_request("Req_114")

    print("\n--- Phase 2: Processing Finishes Asychronously ---")
    # Asynchronous means not happening at the same time
    # Lets say Server 1 finishes its job, freeing up its capacity
    active_jobs["Req_101"].complete_processing("Req_102")
    active_jobs["Req_102"].complete_processing("Req_105")

    print("\n--- Phase 3: New Traffic Arrives ---")
    gateway.route_request("Req_115")

    print("\n--- Phase 4: Simulating 10 Student requests via Cache-Aside ---")
    db = MockDatabase()
    cache = MockRedisCache()

    # Simulating 10 students hitting the endpoint
    for i in range(1, 11):
        user_id = f"Student_{i}"
        data = get_exam_countdown(user_id, db, cache)
        print(f"Response to {user_id}: {data}\n")
