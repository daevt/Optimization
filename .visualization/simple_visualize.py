#!/usr/bin/env python3
"""
Simple visualization script for optimization results
Shows comparison tables without requiring additional packages
"""

import csv
import os
from collections import defaultdict

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
    
    for method in methods:
        filename = f'result_{method}.csv'
        data = load_csv_data(filename)
        if data:
            all_data[method] = data
            print(f"✓ Loaded {len(data)} records from {filename}")
        else:
            print(f"✗ Failed to load {filename}")
    
    return all_data

def create_comparison_table(all_data):
    """Create a comparison table showing max_load for each method and case"""
    if not all_data:
        print("No data available for comparison")
        return
    
    # Get all test cases
    all_cases = set()
    for method_data in all_data.values():
        for row in method_data:
            all_cases.add(row['case_file'])
    
    all_cases = sorted(list(all_cases))
    methods = sorted(all_data.keys())
    
    print("\n" + "="*80)
    print("MAX LOAD COMPARISON TABLE")
    print("="*80)
    
    # Header
    header = f"{'Case':<12}"
    for method in methods:
        header += f"{method.upper():<12}"
    print(header)
    print("-" * len(header))
    
    # Data rows
    for case in all_cases:
        row = f"{case:<12}"
        for method in methods:
            max_load = "N/A"
            if method in all_data:
                for data_row in all_data[method]:
                    if data_row['case_file'] == case:
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
    """Create a table showing execution times for each method and case"""
    if not all_data:
        print("No data available for execution time comparison")
        return
    
    # Get all test cases
    all_cases = set()
    for method_data in all_data.values():
        for row in method_data:
            all_cases.add(row['case_file'])
    
    all_cases = sorted(list(all_cases))
    methods = sorted(all_data.keys())
    
    print("\n" + "="*80)
    print("EXECUTION TIME COMPARISON TABLE (seconds)")
    print("="*80)
    
    # Header
    header = f"{'Case':<12}"
    for method in methods:
        header += f"{method.upper():<12}"
    print(header)
    print("-" * len(header))
    
    # Data rows
    for case in all_cases:
        row = f"{case:<12}"
        for method in methods:
            exec_time = "N/A"
            if method in all_data:
                for data_row in all_data[method]:
                    if data_row['case_file'] == case:
                        exec_time = f"{float(data_row['exec_time']):.4f}"
                        break
            row += f"{exec_time:<12}"
        print(row)

def create_summary_statistics(all_data):
    """Create summary statistics for each method"""
    if not all_data:
        print("No data available for summary statistics")
        return
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
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
    
    # Get all test cases
    all_cases = set()
    for method_data in all_data.values():
        for row in method_data:
            all_cases.add(row['case_file'])
    
    print("\n" + "="*80)
    print("BEST SOLUTIONS (Lowest Max Load)")
    print("="*80)
    
    for case in sorted(all_cases):
        best_load = float('inf')
        best_methods = []
        
        for method in all_data:
            for row in all_data[method]:
                if row['case_file'] == case:
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
            print(f"{case:<12} Best Load: {load_str:<6} Methods: {methods_str}")

def main():
    """Main function to run all analyses"""
    print("Loading optimization results...")
    all_data = load_all_results()
    
    if not all_data:
        print("No data files found. Please run crawl.py first to generate CSV files.")
        return
    
    # Display all analyses
    create_comparison_table(all_data)
    create_execution_time_table(all_data)
    create_summary_statistics(all_data)
    find_best_solutions(all_data)
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)

if __name__ == "__main__":
    main()
