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
                return params_str
        except:
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
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('performance_vs_time.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_statistics_summary(self) -> pd.DataFrame:
        """Create statistics summary for each method"""
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
                'Std Exec Time': method_data['exec_time'].std(),
                'Test Cases': len(method_data)
            }
            stats_data.append(stats)
        
        return pd.DataFrame(stats_data).round(4)
    
    def export_to_excel(self, filename='optimization_results_analysis.xlsx'):
        """Export all tables to Excel file with multiple sheets"""
        if self.combined_data is None or self.combined_data.empty:
            print("❌ No data to export")
            return
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Export comparison table
            comparison_table = self.create_comparison_table()
            if not comparison_table.empty:
                comparison_table.to_excel(writer, sheet_name='Max Load Comparison')
            
            # Export execution time table
            exec_time_table = self.create_execution_time_table()
            if not exec_time_table.empty:
                exec_time_table.to_excel(writer, sheet_name='Execution Time')
            
            # Export statistics summary
            stats_summary = self.create_statistics_summary()
            if not stats_summary.empty:
                stats_summary.to_excel(writer, sheet_name='Statistics Summary', index=False)
            
            # Export raw combined data
            self.combined_data.to_excel(writer, sheet_name='Raw Data', index=False)
        
        print(f"✅ Exported analysis to {filename}")
    
    def export_to_csv(self):
        """Export tables to individual CSV files"""
        if self.combined_data is None or self.combined_data.empty:
            print("❌ No data to export")
            return
        
        # Export comparison table
        comparison_table = self.create_comparison_table()
        if not comparison_table.empty:
            comparison_table.to_csv('max_load_comparison.csv')
            print("✅ Exported max_load_comparison.csv")
        
        # Export execution time table
        exec_time_table = self.create_execution_time_table()
        if not exec_time_table.empty:
            exec_time_table.to_csv('execution_time_comparison.csv')
            print("✅ Exported execution_time_comparison.csv")
        
        # Export statistics summary
        stats_summary = self.create_statistics_summary()
        if not stats_summary.empty:
            stats_summary.to_csv('statistics_summary.csv', index=False)
            print("✅ Exported statistics_summary.csv")
    
    def display_tables(self):
        """Display all tables in console"""
        print("\n" + "="*80)
        print("MAX LOAD COMPARISON TABLE")
        print("="*80)
        comparison_table = self.create_comparison_table()
        if not comparison_table.empty:
            print(comparison_table.to_string())
        
        print("\n" + "="*80)
        print("EXECUTION TIME COMPARISON TABLE")
        print("="*80)
        exec_time_table = self.create_execution_time_table()
        if not exec_time_table.empty:
            print(exec_time_table.to_string())
        
        print("\n" + "="*80)
        print("STATISTICS SUMMARY")
        print("="*80)
        stats_summary = self.create_statistics_summary()
        if not stats_summary.empty:
            print(stats_summary.to_string(index=False))
    
    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        print("🔄 Starting optimization results analysis...")
        
        # Load data
        self.load_and_combine_data()
        
        if self.combined_data is None or self.combined_data.empty:
            print("❌ No data loaded. Analysis cannot proceed.")
            return
        
        # Display tables
        self.display_tables()
        
        # Create plots
        print("\n📊 Generating plots...")
        self.plot_max_load_comparison()
        self.plot_execution_time_comparison()
        self.plot_performance_vs_time_scatter()
        
        # Export results
        print("\n💾 Exporting results...")
        self.export_to_excel()
        self.export_to_csv()
        
        print("\n🎉 Analysis completed successfully!")
        print("Files generated:")
        print("  📊 Plots: max_load_comparison.png, execution_time_comparison.png, performance_vs_time.png")
        print("  📋 Tables: optimization_results_analysis.xlsx and individual CSV files")

def main():
    """Main function to run the analysis"""
    try:
        # Install required packages if not available
        import subprocess
        import sys
        
        required_packages = ['pandas', 'matplotlib', 'seaborn', 'openpyxl']
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        # Run analysis
        visualizer = OptimizationResultsVisualizer()
        visualizer.run_full_analysis()
        
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        print("Make sure all CSV result files are in the current directory.")

if __name__ == "__main__":
    main()
