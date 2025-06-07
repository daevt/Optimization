import subprocess


def main():
    # generate.py is used to generate the data files
    file = "generate.py"
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
    
    # check matching
    file = "check_matching.py"
    print(f"Running: {file}")
    try:
        result = subprocess.run(["python", file], capture_output=True, text=True)
        print("Output:")
        print(result.stdout)
        line=[line.strip() for line in result.stdout.splitlines()]
        if line[-2] != "Matching is possible":
            print("Matching check failed. Stopping execution.")
            return
    except Exception as e:
        print(f"Error executing {file}: {e}")
        return
    print("-" * 60)

    # List of files to run
    selected_files = [
        "MIP.py",
        "cp.py",
        "max_flow.py",
        "greedy.py",
        "local_search.py",
        "LP.py",
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


if __name__ == "__main__":
    main()

