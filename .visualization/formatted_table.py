#!/usr/bin/env python3
"""
Simple table visualization with N=, M=, b= format labels
Reads parameters directly from CSV params column
"""

import csv
import os

def load_csv_data(filename):
    """Load data from a CSV file"""
    data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    return data

def load_all_results():
    """Load results from all optimization methods"""
    methods = ['cp', 'greedy', 'local_search', 'LP', 'MIP', 'max_flow']
    all_data = {}
    
    print("Loading optimization results...")
    for method in methods:
        filename = f'result_{method}.csv'
        data = load_csv_data(filename)
        if data:
            all_data[method] = data
            print(f"✓ Loaded {len(data)} records from {filename}")
        else:
            print(f"✗ Failed to load {filename}")
    
    return all_data

def format_params(params_str):
    """Convert '5 3 2' to 'N=5, M=3, b=2' format"""
    try:
        values = params_str.split()
        if len(values) == 3:
            N, M, b = values
            return f"N={N}, M={M}, b={b}"
        else:
            return params_str
    except:
        return params_str

def create_comparison_table(all_data):
    """Create a comparison table showing max_load for each method"""
    if not all_data:
        print("No data available for comparison")
        return
    
    # Get all test cases with their parameters
    case_data = {}
    for method_data in all_data.values():
        for row in method_data:
            case_file = row['case_file']
            params = row['params']
            if case_file not in case_data:
                case_data[case_file] = params
    
    # Sort cases by case number
    sorted_cases = sorted(case_data.keys(), key=lambda x: int(x.replace('case', '').replace('.txt', '')))
    methods = sorted(all_data.keys())
    
    print("\n" + "="*120)
    print("MAX LOAD COMPARISON TABLE")
    print("="*120)
    
    # Header
    header = f"{'Parameters':<25}"
    for method in methods:
        header += f"{method.upper():<12}"
    print(header)
    print("-" * len(header))
    
    # Data rows
    for case_file in sorted_cases:
        params_formatted = format_params(case_data[case_file])
        row = f"{params_formatted:<25}"
        
        for method in methods:
            max_load = "N/A"
            if method in all_data:
                for data_row in all_data[method]:
                    if data_row['case_file'] == case_file:
                        max_load = data_row['max_load']
                        # Convert to int if possible for cleaner display
                        try:
                            if float(max_load).is_integer():
                                max_load = str(int(float(max_load)))
                        except:
                            pass
                        break
            row += f"{max_load:<12}"
        print(row)

def create_execution_time_table(all_data):
    """Create execution time table"""
    if not all_data:
        print("No data available for execution time comparison")
        return
    
    # Get all test cases with their parameters
    case_data = {}
    for method_data in all_data.values():
        for row in method_data:
            case_file = row['case_file']
            params = row['params']
            if case_file not in case_data:
                case_data[case_file] = params
    
    # Sort cases by case number
    sorted_cases = sorted(case_data.keys(), key=lambda x: int(x.replace('case', '').replace('.txt', '')))
    methods = sorted(all_data.keys())
    
    print("\n" + "="*120)
    print("EXECUTION TIME COMPARISON TABLE (seconds)")
    print("="*120)
    
    # Header
    header = f"{'Parameters':<25}"
    for method in methods:
        header += f"{method.upper():<12}"
    print(header)
    print("-" * len(header))
    
    # Data rows
    for case_file in sorted_cases:
        params_formatted = format_params(case_data[case_file])
        row = f"{params_formatted:<25}"
        
        for method in methods:
            exec_time = "N/A"
            if method in all_data:
                for data_row in all_data[method]:
                    if data_row['case_file'] == case_file:
                        try:
                            exec_time = f"{float(data_row['exec_time']):.4f}"
                        except:
                            exec_time = data_row['exec_time']
                        break
            row += f"{exec_time:<12}"
        print(row)

def create_summary_statistics(all_data):
    """Create summary statistics for each method"""
    if not all_data:
        print("No data available for summary statistics")
        return
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS BY METHOD")
    print("="*80)
    
    for method in sorted(all_data.keys()):
        data = all_data[method]
        max_loads = []
        exec_times = []
        
        for row in data:
            try:
                max_loads.append(float(row['max_load']))
                exec_times.append(float(row['exec_time']))
            except ValueError:
                continue
        
        if max_loads and exec_times:
            print(f"\n{method.upper()} Method:")
            print(f"  Max Load - Avg: {sum(max_loads)/len(max_loads):.2f}, "
                  f"Min: {min(max_loads):.1f}, Max: {max(max_loads):.1f}")
            print(f"  Exec Time - Avg: {sum(exec_times)/len(exec_times):.4f}s, "
                  f"Min: {min(exec_times):.4f}s, Max: {max(exec_times):.4f}s")
            print(f"  Total Cases: {len(max_loads)}")

def find_best_solutions(all_data):
    """Find the best solution for each test case"""
    if not all_data:
        print("No data available for finding best solutions")
        return
    
    # Get all test cases with their parameters
    case_data = {}
    for method_data in all_data.values():
        for row in method_data:
            case_file = row['case_file']
            params = row['params']
            if case_file not in case_data:
                case_data[case_file] = params
    
    # Sort cases by case number
    sorted_cases = sorted(case_data.keys(), key=lambda x: int(x.replace('case', '').replace('.txt', '')))
    
    print("\n" + "="*80)
    print("BEST SOLUTIONS (Lowest Max Load)")
    print("="*80)
    
    for case_file in sorted_cases:
        params_formatted = format_params(case_data[case_file])
        
        best_load = float('inf')
        best_methods = []
        
        for method in all_data:
            for row in all_data[method]:
                if row['case_file'] == case_file:
                    try:
                        load = float(row['max_load'])
                        if load < best_load:
                            best_load = load
                            best_methods = [method]
                        elif load == best_load:
                            if method not in best_methods:
                                best_methods.append(method)
                    except ValueError:
                        continue
        
        if best_load != float('inf'):
            methods_str = ', '.join(best_methods)
            load_str = str(int(best_load)) if best_load.is_integer() else f"{best_load:.1f}"
            print(f"{params_formatted:<20} Best Load: {load_str:<6} Methods: {methods_str}")

def export_to_csv(all_data):
    """Export results to CSV format for easy viewing"""
    if not all_data:
        print("No data available for export")
        return
    
    # Get all test cases with their parameters
    case_data = {}
    for method_data in all_data.values():
        for row in method_data:
            case_file = row['case_file']
            params = row['params']
            if case_file not in case_data:
                case_data[case_file] = params
    
    # Sort cases by case number
    sorted_cases = sorted(case_data.keys(), key=lambda x: int(x.replace('case', '').replace('.txt', '')))
    methods = sorted(all_data.keys())
    
    # Export max load comparison
    with open('max_load_comparison_formatted.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        header = ['Parameters'] + [method.upper() for method in methods]
        writer.writerow(header)
        
        # Data rows
        for case_file in sorted_cases:
            params_formatted = format_params(case_data[case_file])
            row = [params_formatted]
            
            for method in methods:
                max_load = "N/A"
                if method in all_data:
                    for data_row in all_data[method]:
                        if data_row['case_file'] == case_file:
                            max_load = data_row['max_load']
                            try:
                                if float(max_load).is_integer():
                                    max_load = int(float(max_load))
                            except:
                                pass
                            break
                row.append(max_load)
            writer.writerow(row)
    
    print(f"✓ Exported max load comparison to: max_load_comparison_formatted.csv")
    
    # Export execution time comparison
    with open('execution_time_comparison_formatted.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        header = ['Parameters'] + [f"{method.upper()}_TIME" for method in methods]
        writer.writerow(header)
        
        # Data rows
        for case_file in sorted_cases:
            params_formatted = format_params(case_data[case_file])
            row = [params_formatted]
            
            for method in methods:
                exec_time = "N/A"
                if method in all_data:
                    for data_row in all_data[method]:
                        if data_row['case_file'] == case_file:
                            try:
                                exec_time = float(data_row['exec_time'])
                            except:
                                exec_time = data_row['exec_time']
                            break
                row.append(exec_time)
            writer.writerow(row)
    
    print(f"✓ Exported execution time comparison to: execution_time_comparison_formatted.csv")

def main():
    """Main function to run all analyses"""
    all_data = load_all_results()
    
    if not all_data:
        print("No data files found. Please run crawl.py first to generate CSV files.")
        return
    
    # Display all analyses with formatted parameters
    create_comparison_table(all_data)
    create_execution_time_table(all_data)
    create_summary_statistics(all_data)
    find_best_solutions(all_data)
    
    # Export to CSV
    export_to_csv(all_data)
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("CSV files with N=, M=, b= format have been created.")
    print("="*80)

if __name__ == "__main__":
    main()
