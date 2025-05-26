import subprocess

# List of files to run
selected_files = [
    "/workspaces/rtewr/Project/generate.py",
    "/workspaces/rtewr/Project/greedy.py",
    "/workspaces/rtewr/Project/local_search.py", 
    "/workspaces/rtewr/Project/max_flow.py",
    "/workspaces/rtewr/Project/cp.py",
    
    "/workspaces/rtewr/Project/LP.py",
    "/workspaces/rtewr/Project/MIP.py" # Added local search
   
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

