import subprocess

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

print("Running all paper-reviewer assignment implementations...")
print("=" * 60)

for file in selected_files:
    print(f"Running: {file}")
    try:
        result = subprocess.run(["python", file], capture_output=True, text=True)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except Exception as e:
        print(f"Error executing {file}: {e}")
    print("-" * 60)

print("All executions completed.")

