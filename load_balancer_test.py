""" This file is to contrast the difference between Round Robin and Least Connections"""

import time
import random
from itertools import cycle

requests = []

class Request():
    def __init__(self, user_id, req_id):
        self.user_id = user_id
        self.req_id = req_id

        request = (user_id, req_id)
        requests.append(request)
    

if __name__ == "__main__":
    request = Request

    user_id = input("Enter User ID: ")
    req_id = input("Enter Request ID: ")
    request = Request(user_id, req_id)

    print("\n== Request ==\n")
    print(requests[0])
