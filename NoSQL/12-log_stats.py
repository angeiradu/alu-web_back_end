#!/usr/bin/env python3
""" a Python script that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient

if __name__ == "__main__":
    """ Main Function """
    client = MongoClient('mongodb://localhost:27017')
    nginx = client.logs.nginx
    print(f"{nginx.count_documents({})} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check_count = nginx.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
