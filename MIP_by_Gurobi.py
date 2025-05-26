from ortools.linear_solver import pywraplp
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.4f} seconds")
        return result
    return wrapper

def input_data():
    try:
        with open('input.txt', 'r') as f:
            num_papers, num_reviewers, reviews_per_paper = map(int, f.readline().strip().split())
            willing_reviewers = defaultdict(list)
            reviewer_loads = defaultdict(int)
            
            for i in range(num_papers):
                line = list(map(int, f.readline().strip().split()))
                paper_id = i + 1
                reviewers = line[1:]
                willing_reviewers[paper_id] = reviewers
                
                for reviewer in reviewers:
                    reviewer_loads[reviewer] += 1
                    
            return num_papers, num_reviewers, reviews_per_paper, willing_reviewers, reviewer_loads
    except FileNotFoundError:
        print("Error: Input file not found!")
        exit(1)
    except Exception as e:
        print(f"Error reading input: {str(e)}")
        exit(1)

def solve_subproblem(paper_ids, willing_reviewers, reviews_per_paper, num_reviewers):
    """Giải quyết một phần bài toán cho tập paper con"""
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return None
    
    # Biến quyết định cho subset papers
    x = {}
    for paper in paper_ids:
        for reviewer in willing_reviewers[paper]:
            x[(paper, reviewer)] = solver.BoolVar(f'x[{paper},{reviewer}]')

    # Ràng buộc cho mỗi paper
    for paper in paper_ids:
        solver.Add(
            sum(x[(paper, reviewer)] for reviewer in willing_reviewers[paper]) == reviews_per_paper
        )

    # Ràng buộc tải reviewer (tính toán song song)
    loads = {}
    for reviewer in range(1, num_reviewers + 1):
        loads[reviewer] = solver.IntVar(0, len(paper_ids), f'load[{reviewer}]')
        solver.Add(loads[reviewer] == sum(
            x[(paper, reviewer)] for paper in paper_ids 
            if (paper, reviewer) in x
        ))

    max_load = solver.IntVar(0, len(paper_ids), 'max_load')
    for reviewer in range(1, num_reviewers + 1):
        solver.Add(loads[reviewer] <= max_load)

    solver.Minimize(max_load)
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return {k: v.solution_value() for k, v in x.items() if v.solution_value() > 0.5}
    return None

@time_execution
def main():
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers, reviewer_loads = input_data()
    
    # Chia bài toán thành các phần nhỏ để xử lý song song
    num_threads = multiprocessing.cpu_count()
    papers_per_thread = num_papers // num_threads
    paper_ids = list(range(1, num_papers + 1))
    chunks = [paper_ids[i:i + papers_per_thread] for i in range(0, num_papers, papers_per_thread)]
    
    results = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(
                solve_subproblem,
                chunk,
                willing_reviewers,
                reviews_per_paper,
                num_reviewers
            ) for chunk in chunks
        ]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    # Tổng hợp kết quả từ các luồng
    final_assignment = {}
    for result in results:
        final_assignment.update(result)
    
    # Tính toán tải cuối cùng của các reviewer
    final_loads = defaultdict(int)
    for (paper, reviewer), assigned in final_assignment.items():
        if assigned:
            final_loads[reviewer] += 1
    
    if final_loads:
        max_load = max(final_loads.values())
        print(f"\nMaximum reviewer load: {max_load}")
        """print("\nReviewer loads:")
        for reviewer in sorted(final_loads.keys()):
            print(f"Reviewer {reviewer}: {final_loads[reviewer]} papers")"""
    else:
        print("No feasible solution found")

if __name__ == '__main__':
    main()