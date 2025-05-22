import time

def read_input():
    with open("/workspaces/rtewr/Project/clique.txt", "r") as f:
        n, m = map(int, f.readline().strip().split())
        # Initialize graph with empty adjacency sets for all vertices
        graph = {v: set() for v in range(1, n+1)}
        
        # Read each edge and add to adjacency sets
        for _ in range(m):
            u, v = map(int, f.readline().strip().split())
            graph[u].add(v)
            graph[v].add(u)  # Add in both directions for undirected graph
            
    return graph

def max_clique_backtrack(graph, current_clique, candidates, max_clique):
    # Pruning: if current_clique + remaining candidates is less than max_clique, stop
    if len(current_clique) + len(candidates) <= len(max_clique):
        return max_clique
        
    if not candidates:
        if len(current_clique) > len(max_clique):
            max_clique = current_clique.copy()
        return max_clique
    
    # Chọn đỉnh v có bậc cao nhất trong candidates
    v = max(candidates, key=lambda x: len(graph[x]))
    
    # Nhánh 1: Chọn v -> chỉ xét các đỉnh kề với v
    new_candidates = candidates & graph[v]
    max_clique = max_clique_backtrack(graph, current_clique + [v], new_candidates, max_clique)
    
    # Nhánh 2: Không chọn v -> loại v khỏi candidates
    candidates_copy = candidates.copy()  # Create a copy to avoid modifying the original set
    candidates_copy.remove(v)
    max_clique = max_clique_backtrack(graph, current_clique, candidates_copy, max_clique)
    
    return max_clique
def visualize_graph(graph,max_clique):
    with open("Project/graph.dot", "w") as f:
        f.write("graph G {\n")
        for u in graph:
            for v in graph[u]:
                if u < v:
                    f.write(f"    {u} -- {v};\n")
        f.write("}\n")
    

    
def time_execution(func, *args, **kwargs):
    """
    Measure execution time of a function.
    
    Args:
        func: The function to time
        *args, **kwargs: Arguments to pass to the function
        
    Returns:
        tuple: (function result, execution time in seconds)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

# Gọi hàm ban đầu
graph = read_input()
max_clique, execution_time = time_execution(
    max_clique_backtrack, graph, [], set(graph.keys()), []
)
print(f"Maximum clique size: {len(max_clique)}")
print(f"Maximum clique: {max_clique}")
print(f"Execution time: {execution_time:.4f} seconds")
visualize_graph(graph, max_clique)