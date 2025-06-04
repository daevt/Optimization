from ortools.graph.python import max_flow
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
def pre_processing_data(num_papers,num_reviewers,reviews_per_paper ,willing_reviewers,max_load):
    
    source = 0
    sink = num_papers + num_reviewers + 1

    start_nodes = []
    end_nodes = []
    capacities = []

    # Arcs from source to papers
    start_nodes += [source] * num_papers
    end_nodes += [i for i in range(1, num_papers + 1)]
    capacities += [reviews_per_paper] * num_papers

    # Arcs from papers to reviewers (with correct offset)
    for paper in range(1, num_papers + 1):
        for reviewer in willing_reviewers[paper]:
            start_nodes.append(paper)
            end_nodes.append(reviewer + num_papers)  # Add offset here
            capacities.append(1)

    # Arcs from reviewers to sink
    for reviewer in range(1, num_reviewers + 1):
        start_nodes.append(reviewer + num_papers)
        end_nodes.append(sink)
        capacities.append(max_load)
    return start_nodes, end_nodes, capacities
def reverse_dict(willing_reviewers):
    willing_papers = {}
    for paper, reviewers in willing_reviewers.items():
        for reviewer in reviewers:
            if reviewer not in willing_papers:
                willing_papers[reviewer] = []
            willing_papers[reviewer].append(paper)
    return willing_papers

@time_execution
def main(): 
    # Instantiate a SimpleMaxFlow solver.
    smf = max_flow.SimpleMaxFlow()

    # Read input data
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()

    max_load = 100000000
    # Pre-process the data to create arcs with capacities
    start_nodes, end_nodes, capacities = pre_processing_data(num_papers,num_reviewers,reviews_per_paper ,willing_reviewers,max_load)
    #   note: we could have used add_arc_with_capacity(start, end, capacity)
    all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

     # Find the maximum flow between node 0 and node 4.
    status = smf.solve(0, num_papers + num_reviewers + 1)

    if (status == smf.OPTIMAL) and smf.optimal_flow()== num_papers * reviews_per_paper:
        print("Matching is possible")   
    else:
        print("Matching is not possible")

        

       
        
if __name__ == "__main__":
    main()
