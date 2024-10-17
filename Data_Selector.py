import os
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

def fetch_from_mongodb():
    data = collection.find_one()  
    return data if data else {"data": "No data found in MongoDB"}

def fetch_from_local_files():
    try:
        with open("local_data.txt", "r") as file:
            return {"data": file.read()}
    except FileNotFoundError:
        return {"error": "Local file not found"}

def fetch_from_pe3_dump():
    try:
        with open("pe3_dump.csv", "r") as file:
            return {"data": file.read()}
    except FileNotFoundError:
        return {"error": "PE3 Dump file not found"}

class DataSourceManager:
    def __init__(self):
        self.data_source = "MongoDB"  

    def set_data_source(self, source):
        if source in ["MongoDB", "Local Files", "PE3 Dump"]:
            self.data_source = source
        else:
            raise ValueError("Invalid data source")

    def get_data(self):
        if self.data_source == 'MongoDB':
            return fetch_from_mongodb()
        elif self.data_source == 'Local Files':
            return fetch_from_local_files()
        elif self.data_source == 'PE3 Dump':
            return fetch_from_pe3_dump()
        else:
            return {"error": "No valid data source selected"}

if __name__ == '__main__':
    data_manager = DataSourceManager()
    
    while True:
        print("\nCurrent Data Source:", data_manager.data_source)
        print("Choose Data Source: 1 - MongoDB, 2 - Local Files, 3 - PE3 Dump")
        choice = input("Enter the number to select data source (or 'q' to quit): ")

        if choice == 'q':
            break
        elif choice == '1':
            data_manager.set_data_source('MongoDB')
        elif choice == '2':
            data_manager.set_data_source('Local Files')
        elif choice == '3':
            data_manager.set_data_source('PE3 Dump')
        else:
            print("Invalid selection. Repeat")
            continue

        data = data_manager.get_data()
        print("\nFetched Data:", data)
