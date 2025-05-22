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
    with open('Project/input.txt', 'r') as f:
        num_papers,num_reviewers,reviews_per_paper = map(int, f.readline().strip().split())
        willing_reviewers = {}
        for i in range(num_papers):
            line = list(map(int, f.readline().strip().split()))
            paper_id = i+1
            reviewers = line[1:]
            willing_reviewers[paper_id] = reviewers
    return num_papers, num_reviewers, reviews_per_paper, willing_reviewers
def create_network(num_papers,num_reviewers,reviews_per_paper ,willing_reviewers,max_load):
    
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
    # Read input data
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()
    # Create the network
    if (num_papers*reviews_per_paper) % num_reviewers == 0:
        min_capactice_max_load=(num_papers*reviews_per_paper) // num_reviewers
    else:
        min_capactice_max_load=(num_papers*reviews_per_paper) // num_reviewers + 1
    

    #Dirichlet's theorem
    max_load= min_capactice_max_load 

    start_nodes, end_nodes, capacities = create_network(num_papers,num_reviewers,reviews_per_paper ,willing_reviewers,max_load)
    feasible_flow={}
    for i in range(len(start_nodes)):
        feasible_flow[(start_nodes[i], end_nodes[i])] = 0
    gap_flow = {}
    for i in range(len(start_nodes)):
        gap_flow[(start_nodes[i], end_nodes[i])] = capacities[i]
@time_execution
    # Create the max flow solver



    
