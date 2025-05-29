import os
import shutil
import subprocess
import csv

test_case_dir = 'Test_case'
data_dir = 'Data'
methods = [
    ('cp', 'cp.py'),
    ('LP', 'LP.py'),
    ('local_search', 'local_search.py'),
    ('greedy', 'greedy.py'),
    ('MIP', 'MIP.py'),
    ('max_flow', 'max_flow.py'),
]

# Clear old CSV files first
for name, script in methods:
    csv_path = f'result_{name}.csv'
    if os.path.exists(csv_path):
        os.remove(csv_path)

# Run all methods on all test cases
for case_file in sorted(os.listdir(test_case_dir)):
    if not case_file.endswith('.txt'):
        continue
    
    print(f"Processing {case_file}...")
    shutil.copy(os.path.join(test_case_dir, case_file), 'input.txt')
    
    with open('input.txt', 'r') as f:
        params = f.readline().strip()
    
    for name, script in methods:
        script_path = os.path.join(data_dir, script)
        if not os.path.exists(script_path):
            continue
            
        try:
            result = subprocess.run(['py', script_path], capture_output=True, text=True, timeout=600)
            output = result.stdout.strip().splitlines()
            max_load = ''
            exec_time = ''
              # Filter out system loading messages and keep only numeric outputs
            clean_output = []
            lp_solution_found = False
            for line in output:
                line = line.strip()
                if line and not line.startswith('load ') and 'ortools' not in line and '.dll' not in line:
                    # Check for LP solution line
                    if 'LP Solution' in line:
                        lp_solution_found = True
                        continue
                    # Check if line is numeric (can be int or float)
                    try:
                        float(line)
                        clean_output.append(line)
                    except ValueError:
                        continue
            
            # Parse the clean output based on method type
            if name in ['MIP']:
                # MIP outputs: status, max_load, exec_time
                if len(clean_output) >= 3:
                    max_load = clean_output[1]  # Second line is max_load
                    exec_time = clean_output[2]  # Third line is exec_time
                elif len(clean_output) >= 2:
                    max_load = clean_output[0]
                    exec_time = clean_output[1]
                else:
                    max_load = clean_output[0] if clean_output else 'N/A'
                    exec_time = 'N/A'
            elif name in ['LP'] or lp_solution_found:
                # LP outputs: max_load, exec_time (after filtering LP solution line)
                if len(clean_output) >= 2:
                    max_load = clean_output[0]
                    exec_time = clean_output[1]
                elif len(clean_output) == 1:
                    max_load = clean_output[0]
                    exec_time = 'N/A'
                else:
                    max_load = 'N/A'
                    exec_time = 'N/A'
            else:
                # CP, Greedy, Max Flow, Local Search outputs: max_load, exec_time
                if len(clean_output) >= 2:
                    max_load = clean_output[0]
                    exec_time = clean_output[1]
                elif len(clean_output) == 1:
                    max_load = clean_output[0]
                    exec_time = 'N/A'
                else:
                    max_load = 'N/A'
                    exec_time = 'N/A'
            
            # Write directly to CSV
            csv_path = f'result_{name}.csv'
            write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
            with open(csv_path, 'a', newline='', encoding='utf-8') as fout:
                writer = csv.writer(fout)
                if write_header:
                    writer.writerow(['case_file', 'params', 'max_load', 'exec_time'])
                writer.writerow([case_file, params, max_load, exec_time])
                
        except Exception as e:
            csv_path = f'result_{name}.csv'
            write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
            with open(csv_path, 'a', newline='', encoding='utf-8') as fout:
                writer = csv.writer(fout)
                if write_header:
                    writer.writerow(['case_file', 'params', 'max_load', 'exec_time'])
                writer.writerow([case_file, params, f'ERROR: {e}', ''])

print('Crawling finished. Results are in result_*.csv files.')
