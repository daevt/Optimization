from ortools.linear_solver import pywraplp
import time

def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{execution_time:.4f}")
        return result
    return wrapper




def input_data():
    with open('input.txt', 'r') as f:
        num_papers,num_reviewers,reviews_per_paper = map(int, f.readline().strip().split())
        willing_reviewers = {}
        for i in range(num_papers):
            line = list(map(int, f.readline().strip().split()))
            paper_id = i+1
            reviewers = line[1:]
            willing_reviewers[paper_id] = reviewers
    return num_papers, num_reviewers, reviews_per_paper, willing_reviewers

@time_execution
def main():
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()  
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    
    x = {}
    for paper in range(1, num_papers + 1):
        for reviewer in willing_reviewers[paper]:
            x[(paper, reviewer)] = solver.BoolVar(f'x[{paper},{reviewer}]')

    # Ràng buộc: Mỗi paper phải được đánh giá bởi đúng số lượng reviewers
    for paper in range(1, num_papers + 1):
        solver.Add(solver.Sum(x[(paper, reviewer)] for reviewer in willing_reviewers[paper]) == reviews_per_paper)

    # Ràng buộc: Tải của mỗi reviewer
    loads = {}
    for reviewer in range(1, num_reviewers + 1):
        loads[reviewer] = solver.IntVar(0, num_papers, f'load[{reviewer}]')
        solver.Add(loads[reviewer] == solver.Sum(x[(paper, reviewer)] for paper in range(1, num_papers + 1) if (paper, reviewer) in x))
    
    # Ràng buộc: Tải tối đa của các reviewers là nhỏ nhất
    max_load = solver.IntVar(0, num_papers, 'max_load')
    for reviewer in range(1, num_reviewers + 1):
        solver.Add(loads[reviewer] <= max_load)

    # Hàm mục tiêu: Tối thiểu hóa tải tối đa
    solver.Minimize(max_load)

    # Giải bài toán
    status = solver.Solve()
    # In kết quả
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(max_load.solution_value())
        
    else:
        print('Không tìm được nghiệm tối ưu.')
# Tạo solver: MIP = Mixed Integer Programming
solver = pywraplp.Solver.CreateSolver('SCIP')

if __name__ == '__main__':
    main()
