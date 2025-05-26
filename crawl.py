import subprocess
import pandas as pd
import sqlite3

# List of files to run
selected_files = [
    "generate.py",
    "greedy.py",
    "local_search.py",
    "max_flow.py",
    "cp.py",
    "LP.py",
    "MIP.py" # Added local search
]



for file in selected_files:
    try:
        result = subprocess.run(["python", file], capture_output=True, text=True)
        line=result.stdout.split("\n")
        print(line)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except Exception as e:
        continue


