from ortools.linear_solver import pywraplp
import time
import random   

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
def main()-> None:
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()  
    solver=pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver not created.")
        return
    # Create binary variables for each paper-reviewer pair
    x = {}
    for paper in range(1, num_papers + 1):
        for reviewer in willing_reviewers[paper]:
            x[(paper, reviewer)] = solver.NumVar(0,1,f'x[{paper},{reviewer}]')
    loads= {}   
    for reviewer in range(1, num_reviewers + 1):
        loads[reviewer] = solver.NumVar(0, num_papers, f'load[{reviewer}]')
    for j in range(1,num_papers+1):
        solver.Add(solver.Sum(x[(j,i)] for i in willing_reviewers[j]) == reviews_per_paper)
    for i in range(1, num_reviewers + 1):
        solver.Add(loads[i] == solver.Sum(x[(j, i)] for j in range(1, num_papers + 1) if (j, i) in x))
    max_load = solver.NumVar(0, num_papers, 'max_load')
    for i in range(1, num_reviewers + 1):
        solver.Add(loads[i] <= max_load)
    solver.Minimize(max_load)
    
    # Solve the LP model
    status = solver.Solve()
    
    # Check if a solution was found
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        print('No solution found.')
        return
        
    # Print the LP solution
    print(f"LP Solution - Maximum load: {max_load.solution_value()}")
    
    # Randomized Rounding
    assignments = {}
    reviewer_counts = {r: 0 for r in range(1, num_reviewers + 1)}
    
    for paper in range(1, num_papers + 1):
        # Get the fractional solution values for this paper
        probabilities = []
        reviewers = []
        for reviewer in willing_reviewers[paper]:
            probabilities.append(x[(paper, reviewer)].solution_value())
            reviewers.append(reviewer)
        
        # Normalize probabilities (they should sum to reviews_per_paper)
        total = sum(probabilities)
        if total > 0:
            probabilities = [p/total for p in probabilities]
        # Select reviewers without replacement
        chosen = []
        for _ in range(reviews_per_paper):
            if not probabilities:  # In case all probabilities are zero
                remaining = [r for r in willing_reviewers[paper] if r not in chosen]
                if not remaining:
                    break
                r = random.choice(remaining)
            else:
                r = random.choices(reviewers, weights=probabilities, k=1)[0]
                while r in chosen:
                    # Resample if we get a duplicate (for cases where we sample with replacement)
                    r = random.choices(reviewers, weights=probabilities, k=1)[0]
            
            chosen.append(r)
            reviewer_counts[r] += 1
        
        assignments[paper] = chosen
    
    # Output the results
    print(f"Maximum load: {max(reviewer_counts.values())}")
    

if __name__ == "__main__":
    main()