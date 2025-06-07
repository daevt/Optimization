from ortools.sat.python import cp_model
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
def main()->None:
    # Read input data
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()  
    # Create the model
    model = cp_model.CpModel()
    # Create binary variables for each paper-reviewer pair
    x= {}
    for paper in range(1, num_papers + 1):
        for reviewer in willing_reviewers[paper]:
            x[(paper, reviewer)] = model.NewBoolVar(f'x[{paper},{reviewer}]')

    # Each paper must be reviewed by exactly reviews_per_paper reviewers
    for paper in range(1, num_papers + 1):
        model.Add(sum(x[(paper, reviewer)] for reviewer in willing_reviewers[paper]) == reviews_per_paper)
    # Load for each reviewer
    loads = {}
    for reviewer in range(1, num_reviewers + 1):
        loads[reviewer] = model.NewIntVar(0, num_papers, f'load[{reviewer}]')
        model.Add(loads[reviewer] == sum(x[(paper, reviewer)] for paper in range(1, num_papers + 1) if (paper, reviewer) in x))
    
    # Add constraints max of loads is minium
    max_load = model.NewIntVar(0, num_papers, 'max_load')
    for reviewer in range(1, num_reviewers + 1):
        model.Add(loads[reviewer] <= max_load)

    # Objective: minimize the maximum load
    model.Minimize(max_load)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # Print the solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        """print(num_papers)
        for paper in range(1, num_papers + 1):
            print(reviews_per_paper, end=' ')
            for reviewer in willing_reviewers[paper]:
                if solver.Value(x[(paper, reviewer)]) == 1:
                    print(reviewer, end=' ')
            print()"""
        print(solver.ObjectiveValue())
    else:
        print('No solution found.')
    """# Print statistics
    print()
    print('Statistics:')
    print(f'  status   : {solver.StatusName(status)}')
    print(f'  conflicts: {solver.NumConflicts()}')
    print(f'  branches : {solver.NumBranches()}')
    print(f'  wall time: {solver.WallTime()} ms')
    print(f'  load     : {solver.ObjectiveValue()}')"""
if __name__ == "__main__":
    main()








