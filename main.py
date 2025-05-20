def read_input("clique.txt"):
    with open("clique.txt", "r") as f:
        n = int(f.readline().strip())
        graph = {}
        for i in range(n):
            line = list(map(int, f.readline().strip().split()))
            graph[i] = set(line[1:])  # Chỉ lưu các đỉnh kề
    return n, graph
def max_clique_backtrack(graph, current_clique, candidates, max_clique):
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

# Gọi hàm ban đầu
n,graph= read_input()
max_clique = max_clique_backtrack(graph, [], set(graph.keys()), [])
print(len(max_clique))