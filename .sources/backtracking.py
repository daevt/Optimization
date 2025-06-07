def backtrack_alternative(N, M, b, L, max_load):
    assignment = [[] for _ in range(N)]
    load = [0] * M

    def assign(paper_index):
        if paper_index == N:
            return True

        def try_reviewer_set(start, current_reviewers):
            if len(current_reviewers) == b:
                assignment[paper_index] = current_reviewers[:]
                for r in current_reviewers:
                    load[r - 1] += 1
                if assign(paper_index + 1):
                    return True
                for r in current_reviewers:
                    load[r - 1] -= 1
                assignment[paper_index] = []
                return False

            for i in range(start, len(L[paper_index])):
                reviewer = L[paper_index][i]
                if reviewer not in current_reviewers and load[reviewer - 1] < max_load:
                    current_reviewers.append(reviewer)
                    if try_reviewer_set(i + 1, current_reviewers):
                        return True
                    current_reviewers.pop()
            return False

        return try_reviewer_set(0, [])

    if assign(0):
        return assignment
    return None

def solve_alternative(N, M, b, L):
    lo, hi = 1, N
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        result = backtrack_alternative(N, M, b, L, mid)
        if result:
            hi = mid - 1
            best = result
        else:
            lo = mid + 1
    return best

def main():   
    N, M, b = map(int, input().split())
    L=[]
    for _ in range(N):
        line=list(map(int,input().split()))
        L.append(line[1:] if len(line)>1 else [])

    result = solve_alternative(N, M, b, L)

    print(N)
    for reviewers in result:
        print(b, *reviewers)

if _name_ == "_main_":
    main()
