from ortools.graph.python import max_flow
import time
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
    # Read first line for parameters
    num_papers, num_reviewers, reviews_per_paper = map(int, input().strip().split())
    
    willing_reviewers = {}
    # Read paper reviewers data
    for i in range(num_papers):
        line = list(map(int, input().strip().split()))
        paper_id = i+1
        reviewers = line[1:]  # First element is the number of reviewers, skip it
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



def main(): 
    # Instantiate a SimpleMaxFlow solver.
    smf = max_flow.SimpleMaxFlow()

    # Read input data
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()

    #Minimum capactices of max_load
    if (num_papers*reviews_per_paper) % num_reviewers == 0:
        min_capactice_max_load=(num_papers*reviews_per_paper) // num_reviewers
    else:
        min_capactice_max_load=(num_papers*reviews_per_paper) // num_reviewers + 1
    

    #Dirichlet's theorem
    max_load= min_capactice_max_load 

    while True:        
        start_nodes, end_nodes, capacities = pre_processing_data(num_papers,num_reviewers,reviews_per_paper ,willing_reviewers,max_load)

        #   note: we could have used add_arc_with_capacity(start, end, capacity)
        all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

        # Find the maximum flow between node 0 and node 4.
        status = smf.solve(0, num_papers + num_reviewers + 1)

        if (status == smf.OPTIMAL) and smf.optimal_flow()== num_papers * reviews_per_paper:
            # Print the solution
            print(num_papers)
            solution_flows = smf.flows(all_arcs)
            arc_indices = {arc: i for i, arc in enumerate(zip(start_nodes, end_nodes))}
       
            for paper in range(1, num_papers + 1):
                print(reviews_per_paper, end=' ')
                assigned_reviewers = []
                
                # Check all arcs from this paper to reviewers
                for reviewer in willing_reviewers[paper]:
                    arc = (paper, reviewer + num_papers)
                    if arc in arc_indices:
                        flow_index = arc_indices[arc]
                        if solution_flows[flow_index] == 1:
                            assigned_reviewers.append(reviewer)
                
                # Print assigned reviewers
                for rev in assigned_reviewers[:reviews_per_paper]:  # Ensure we don't exceed required reviews
                    print(rev, end=' ')
                print()
            break
        else:
            max_load += 1

       
        
if __name__ == "__main__":
    main()
