import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List
import numpy as np

class OptimizationResultsVisualizer:
    def __init__(self):
        self.methods = ['cp', 'LP', 'local_search', 'greedy', 'MIP', 'max_flow']
        self.method_names = {
            'cp': 'Constraint Programming',
            'LP': 'Linear Programming + Randomized Rounding',
            'local_search': 'Greedy + Local Search',
            'greedy': 'Greedy Algorithm',
            'MIP': 'Mixed Integer Programming',
            'max_flow': 'Max Flow Algorithm'
        }
        self.combined_data = None
        
    def format_params(self, params_str):
        """Convert '5 3 2' to 'N=5, M=3, b=2' format"""
        try:
            values = params_str.split()
            if len(values) == 3:
                N, M, b = values
                return f"N={N}, M={M}, b={b}"
            else:
                return params_str        except:
            return params_str
        
    def load_and_combine_data(self) -> pd.DataFrame:
        """Load all CSV files and combine them into one DataFrame"""
        all_data = []
        
        for method in self.methods:
            csv_file = f'result_{method}.csv'
            if os.path.exists(csv_file):
                try:
                    df = pd.read_csv(csv_file)
                    df['method'] = method
                    df['method_name'] = self.method_names[method]
                    # Convert max_load and exec_time to numeric, handling errors
                    df['max_load'] = pd.to_numeric(df['max_load'], errors='coerce')
                    df['exec_time'] = pd.to_numeric(df['exec_time'], errors='coerce')
                    # Format parameters for better display
                    df['formatted_params'] = df['params'].apply(self.format_params)
                    all_data.append(df)
                    print(f"✓ Loaded {len(df)} records from {csv_file}")
                except Exception as e:
                    print(f"✗ Error loading {csv_file}: {e}")
            else:
                print(f"✗ File {csv_file} not found")
        
        if all_data:
            self.combined_data = pd.concat(all_data, ignore_index=True)
            print(f"\n📊 Combined data: {len(self.combined_data)} total records")
            return self.combined_data
        else:
            print("❌ No data loaded")
            return pd.DataFrame()
    
    def create_summary_table(self) -> pd.DataFrame:
        """Create a summary table with all methods for each test case"""
        if self.combined_data is None or self.combined_data.empty:
            return pd.DataFrame()
          # Pivot table for max_load
        max_load_pivot = self.combined_data.pivot_table(
            index='formatted_params',
            columns='method_name',
            values='max_load',
            aggfunc='first'
        )
        
        # Pivot table for execution time
        exec_time_pivot = self.combined_data.pivot_table(
            index='formatted_params',
            columns='method_name',
            values='exec_time',
            aggfunc='first'
        )
        
        # Create comprehensive summary table
        summary_data = []
        for params in max_load_pivot.index:
            row = {'Parameters': params}
            
            # Add max_load for each method
            for method in max_load_pivot.columns:
                max_load = max_load_pivot.loc[params, method]
                exec_time = exec_time_pivot.loc[params, method]
                row[f'{method} (Load)'] = max_load if pd.notna(max_load) else 'N/A'
                row[f'{method} (Time)'] = f"{exec_time:.4f}s" if pd.notna(exec_time) else 'N/A'
            
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)
    
    def create_comparison_table(self) -> pd.DataFrame:
        """Create a cleaner comparison table focusing on max_load values"""
        if self.combined_data is None or self.combined_data.empty:
            return pd.DataFrame()
          # Pivot table for max_load only
        comparison_table = self.combined_data.pivot_table(
            index='formatted_params',
            columns='method_name',
            values='max_load',
            aggfunc='first'
        ).round(1)
        
        # Add best method column
        method_cols = list(comparison_table.columns)
        comparison_table['Best Method'] = comparison_table[method_cols].idxmin(axis=1)
        comparison_table['Best Load'] = comparison_table[method_cols].min(axis=1)
        
        return comparison_table
    
    def create_execution_time_table(self) -> pd.DataFrame:
        """Create a table focusing on execution times"""
        if self.combined_data is None or self.combined_data.empty:
            return pd.DataFrame()
          # Pivot table for execution time
        exec_table = self.combined_data.pivot_table(
            index='formatted_params',
            columns='method_name',
            values='exec_time',
            aggfunc='first'
        ).round(4)
        
        # Add fastest method column
        method_cols = list(exec_table.columns)
        exec_table['Fastest Method'] = exec_table[method_cols].idxmin(axis=1)
        exec_table['Fastest Time'] = exec_table[method_cols].min(axis=1)
        
        return exec_table
    
    def plot_max_load_comparison(self):
        """Create bar plot comparing max_load across methods and test cases"""
        if self.combined_data is None or self.combined_data.empty:
            return
        
        plt.figure(figsize=(15, 8))
          # Create pivot table for plotting
        pivot_data = self.combined_data.pivot_table(
            index='formatted_params',
            columns='method_name',
            values='max_load',
            aggfunc='first'
        )
        
        # Create grouped bar plot
        ax = pivot_data.plot(kind='bar', width=0.8, figsize=(15, 8))
        plt.title('Max Load Comparison Across Different Optimization Methods', fontsize=16, fontweight='bold')
        plt.xlabel('Test Cases (N=Papers, M=Reviewers, b=Reviews per Paper)', fontsize=12)
        plt.ylabel('Maximum Load', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title='Optimization Methods', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('max_load_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_execution_time_comparison(self):
        """Create bar plot comparing execution times"""
        if self.combined_data is None or self.combined_data.empty:
            return
        
        plt.figure(figsize=(15, 8))
          # Create pivot table for plotting
        pivot_data = self.combined_data.pivot_table(
            index='formatted_params',
            columns='method_name',
            values='exec_time',
            aggfunc='first'
        )
        
        # Use log scale for better visualization of time differences
        ax = pivot_data.plot(kind='bar', width=0.8, figsize=(15, 8), logy=True)
        plt.title('Execution Time Comparison Across Different Optimization Methods', fontsize=16, fontweight='bold')
        plt.xlabel('Test Cases (N=Papers, M=Reviewers, b=Reviews per Paper)', fontsize=12)
        plt.ylabel('Execution Time (seconds, log scale)', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title='Optimization Methods', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('execution_time_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_performance_vs_time_scatter(self):
        """Create scatter plot showing performance vs execution time trade-off"""
        if self.combined_data is None or self.combined_data.empty:
            return
        
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot
        for method in self.combined_data['method_name'].unique():
            method_data = self.combined_data[self.combined_data['method_name'] == method]
            plt.scatter(method_data['exec_time'], method_data['max_load'], 
                       label=method, alpha=0.7, s=100)
        
        plt.xlabel('Execution Time (seconds)', fontsize=12)
        plt.ylabel('Maximum Load', fontsize=12)
        plt.title('Performance vs Execution Time Trade-off', fontsize=16, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('performance_vs_time.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_statistics_summary(self) -> pd.DataFrame:
        """Generate statistical summary for each method"""
        if self.combined_data is None or self.combined_data.empty:
            return pd.DataFrame()
        
        stats_data = []
        for method in self.combined_data['method_name'].unique():
            method_data = self.combined_data[self.combined_data['method_name'] == method]
            
            stats = {
                'Method': method,
                'Avg Max Load': method_data['max_load'].mean(),
                'Min Max Load': method_data['max_load'].min(),
                'Max Max Load': method_data['max_load'].max(),
                'Std Max Load': method_data['max_load'].std(),
                'Avg Exec Time': method_data['exec_time'].mean(),
                'Min Exec Time': method_data['exec_time'].min(),
                'Max Exec Time': method_data['exec_time'].max(),
                'Std Exec Time': method_data['exec_time'].std()
            }
            stats_data.append(stats)
        
        return pd.DataFrame(stats_data).round(4)
    
    def save_all_tables(self):
        """Save all tables to Excel and CSV files"""
        if self.combined_data is None or self.combined_data.empty:
            print("❌ No data to save")
            return
        
        try:
            # Create Excel file with multiple sheets
            with pd.ExcelWriter('optimization_results_analysis.xlsx', engine='openpyxl') as writer:
                # Combined raw data
                self.combined_data.to_excel(writer, sheet_name='Raw Data', index=False)
                
                # Comparison table (max load)
                comparison_table = self.create_comparison_table()
                comparison_table.to_excel(writer, sheet_name='Max Load Comparison')
                
                # Execution time table
                exec_time_table = self.create_execution_time_table()
                exec_time_table.to_excel(writer, sheet_name='Execution Time')
                
                # Statistics summary
                stats_summary = self.generate_statistics_summary()
                stats_summary.to_excel(writer, sheet_name='Statistics Summary', index=False)
                
                # Detailed summary
                summary_table = self.create_summary_table()
                summary_table.to_excel(writer, sheet_name='Detailed Summary', index=False)
            
            # Save individual CSV files
            comparison_table.to_csv('max_load_comparison.csv')
            exec_time_table.to_csv('execution_time_comparison.csv')
            stats_summary.to_csv('statistics_summary.csv', index=False)
            
            print("✓ All tables saved successfully!")
            print("  - optimization_results_analysis.xlsx (Excel with multiple sheets)")
            print("  - max_load_comparison.csv")
            print("  - execution_time_comparison.csv")
            print("  - statistics_summary.csv")
            
        except Exception as e:
            print(f"❌ Error saving files: {e}")
    
    def display_tables(self):
        """Display all tables in a formatted way"""
        if self.combined_data is None or self.combined_data.empty:
            print("❌ No data to display")
            return
        
        print("="*80)
        print("📊 OPTIMIZATION RESULTS ANALYSIS")
        print("="*80)
        
        # 1. Max Load Comparison Table
        print("\n🎯 MAX LOAD COMPARISON")
        print("-"*50)
        comparison_table = self.create_comparison_table()
        print(comparison_table.to_string())
        
        # 2. Execution Time Comparison Table
        print("\n⏱️ EXECUTION TIME COMPARISON")
        print("-"*50)
        exec_time_table = self.create_execution_time_table()
        print(exec_time_table.to_string())
        
        # 3. Statistics Summary
        print("\n📈 STATISTICS SUMMARY")
        print("-"*50)
        stats_summary = self.generate_statistics_summary()
        print(stats_summary.to_string(index=False))
        
        print("\n" + "="*80)

def main():
    """Main function to run the visualization"""
    print("🚀 Starting Optimization Results Visualization...")
    
    # Create visualizer instance
    visualizer = OptimizationResultsVisualizer()
    
    # Load and combine data
    print("\n📂 Loading data from CSV files...")
    combined_data = visualizer.load_and_combine_data()
    
    if combined_data.empty:
        print("❌ No data loaded. Please ensure CSV files exist.")
        return
    
    # Display tables
    visualizer.display_tables()
    
    # Create visualizations
    print("\n📊 Creating visualizations...")
    try:
        visualizer.plot_max_load_comparison()
        visualizer.plot_execution_time_comparison()
        visualizer.plot_performance_vs_time_scatter()
        print("✓ Visualizations created successfully!")
    except Exception as e:
        print(f"⚠️ Warning: Could not create plots: {e}")
    
    # Save all tables
    print("\n💾 Saving results to files...")
    visualizer.save_all_tables()
    
    print("\n🎉 Analysis completed successfully!")
    print("\nFiles generated:")
    print("  📊 Plots: max_load_comparison.png, execution_time_comparison.png, performance_vs_time.png")
    print("  📋 Tables: optimization_results_analysis.xlsx and individual CSV files")

if __name__ == "__main__":
    main()