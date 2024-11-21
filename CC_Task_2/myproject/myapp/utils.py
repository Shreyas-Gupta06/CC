import os

def read_ids(file_path):
    ids = []
    with open(file_path, 'r') as file:
        for line in file:
            ids.append(line.strip())
    return ids
