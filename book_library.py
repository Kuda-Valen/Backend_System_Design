import time

# ==========================================
# DATABASE TIER (Primary & Replicas)
# ==========================================
class DatabaseCluster:
    def __init__(self):
        # The primary Database (Single Source of Truth for WRITES)
        self.primary_students = []
        self.primary_books = []

        # Read Replicas (Clones for READ operations)
        self.replica_one_students = []
        self.replica_one_books = []

        self.replica_two_students = []
        self.replica_two_books = []

    def sync_replicas(self):
        """ Simulates Asynchronous Replication streaming changes to replicas """
        self.replica_one_students = list(self.primary_students)
        self.replica_two_students = list(self.primary_students)
        self.replica_one_books = list(self.primary_books)
        self.replica_two_books = list(self.primary_books)

    def write_student(self, student_data: dict):
        """ All writes go strictly to Primary """
        print("  [DB WRITE]: Persisting new student to primary Database...")
        self.primary_students.append(student_data)
        self.sync_replicas()              # This stream updates to replicas

    def read_student_replica(self, name: str) -> dict:
        """ Reads are load balanced across Replicas """
        print("  [DB READ]: Querying Read Replica One on disk ")
        for student in self.replica_one_students:
            if student['name'] == name:
                return student
        return None

db_cluster = DatabaseCluster()

# ====================================
# CACHING TIER (In memory Redis RAM)
# ====================================
class RedisCache:
    def __init__(self):
        self.storage = {}

    def get(self, key: str):
        return self.storage.get(key)

    def set(self, key: str, value: dict):
        self.storage[key] = value

redis_cache = RedisCache()

# ===================================================
# STATELESS SERVER NODES
# ===================================================
class StatelessServer:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.connections = 0
        self.is_healthy = True

    def handle_request(self, student_name: str) -> dict:
        self.connections += 1
        cache_key = f"student:{student_name}"

        cached_data = redis_cache.get(cache_key)
        if cached_data:
            print(f"    [{self.name}]: CACHE HIT! Returning data instantly from RAM ")
            self.connections -= 1
            return cached_data

        print(f"    [{self.name}]: CACHE MISS! Reading from Database Replica..")
        student_data = db_cluster.read_student_replica(student_name)

        if student_data:
            redis_cache.set(cache_key, student_data)

        self.connections -= 1
        return student_data
    
# ============================================================
# Load Balancer
# ============================================================
class LeastConnections:
    def __init__(self):
        self.server_pool = []

    def register_server(self, server: StatelessServer):
        self.server_pool.append(server)

    def route_request(self) -> StatelessServer:
        healthy_servers = [s for s in self.server_pool if s.is_healthy]
        if not healthy_servers:
            return None

        return min(healthy_servers, key=lambda s: s.connections)


class Book:
    def __init__(self, name: str, author: str, year: str, copies: str):
        self.name = name
        self.author = author
        self.year = year
        self.copies = copies

        book = {"name":name, "author":author, "year":year, "copies":copies}

    def add_book(book):
        primary_database_books.append(book)

class Student:
    def __init__(self, name: str, surname: str, age: int, course: str, year: int):
        self.name = name
        self.surname = surname
        self.age = age
        self.course = course
        self.year = year

        self.student = {"name": name, "surname": surname, "age": age, "course": course, "year": year}

if __name__ == "__main__":
    lb = LeastConnections()
    server1 = StatelessServer("Server-1", 8001)
    server2 = StatelessServer("Server-2", 8002)
    lb.register_server(server1)
    lb.register_server(server2)

    new_student = Student("Kudakwashe", "Mukwasi", 23, "Robotics", 3)
    db_cluster.write_student(new_student)

    print("\n--- Request 1: First Read (Cold Cache) ---")
    node_a = lb.route_request()
    result1 = node_a.handle_request("Kudakwashe")
    print(f"Result: {result1['name']} | Course: {result1['course']}")

    print("\n--- Request 2: Second Read (Hot Cache) --- ")
    node_b = lb.route_request()
    result2 = node_b.handle_request("Kudakwashe")
    print(f"Result: {result2['name']} | Course: {result2['course']}")