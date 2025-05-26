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


def reverse_dict(willing_reviewers):
    willing_papers = {}
    for paper, reviewers in willing_reviewers.items():
        for reviewer in reviewers:
            if reviewer not in willing_papers:
                willing_papers[reviewer] = []
            willing_papers[reviewer].append(paper)
    return willing_papers

def input_data():
    with open('input.txt', 'r') as f:
        num_papers,num_reviewers,reviews_per_paper = map(int, f.readline().strip().split())
        willing_reviewers = {}
        for i in range(num_papers):
            line = list(map(int, f.readline().strip().split()))
            paper_id = i+1
            reviewers = line[1:]
            willing_reviewers[paper_id] = reviewers
        #Crate a 
        willing_papers = {}
        for i in range(1,num_reviewers+1):
            for j in range(1,num_papers+1):
                if i in willing_reviewers[j]:
                    willing_papers[i] = willing_papers.get(i, []) + [j]
        #print(willing_papers)
    return num_papers, num_reviewers, reviews_per_paper, willing_reviewers, willing_papers

def matching_papers(num_papers, num_reviewers, reviews_per_paper, willing_reviewers):
    load = {i: 0 for i in range(1, num_reviewers + 1)}  # Fixed: Start from 1 instead of 0
    sorted_dict = dict(sorted(willing_reviewers.items(), key=lambda item: len(item[1])))
    selected_reviewers = {}
    for paper,reviewers in sorted_dict.items():
        #Sort the reviewers by their current load
        reviewers.sort(key=lambda x: load[x])
        # Select the first K reviewers
        selected_reviewers[paper] = reviewers[:reviews_per_paper]
        # Update the load of the selected reviewers
        for reviewer in selected_reviewers[paper]:
            load[reviewer] += 1
    # Find the maximum load
    max_load = max(load.values())
    return max_load, selected_reviewers, load

def local_search(num_papers, num_reviewers, reviews_per_paper, willing_papers, assigned_papers, current_load, depth=0):
    if depth > 100:  # Limit recursion depth
        return assigned_papers, current_load
    
    changed = False
    sorted_load = dict(sorted(current_load.items(), key=lambda item: item[1]))
    #get the max load
    reviewer_of_max_load = max(current_load, key=current_load.get)
    max_load = current_load[reviewer_of_max_load]
    
    for candidate in sorted_load.keys():
        if sorted_load[candidate] < max_load-1:
            # Ensure both reviewers exist in the dictionaries
            if candidate not in willing_papers:
                willing_papers[candidate] = []
            if reviewer_of_max_load not in assigned_papers:
                continue
                
            available_papers = list(set(willing_papers.get(candidate, [])) & set(assigned_papers[reviewer_of_max_load]))
            if len(available_papers) > 0:
                random_paper = random.choice(available_papers)
                assigned_papers[candidate].append(random_paper)
                assigned_papers[reviewer_of_max_load].remove(random_paper)
                # Update the load
                current_load[candidate] += 1
                current_load[reviewer_of_max_load] -= 1
                changed=True
                break
                
    if changed:
        return local_search(num_papers, num_reviewers, reviews_per_paper, willing_papers, assigned_papers, current_load, depth+1)

    return assigned_papers, current_load

@time_execution             
def main():
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers, willing_papers = input_data()

    max_load, selected_reviewers, current_load = matching_papers(num_papers, num_reviewers, reviews_per_paper, willing_reviewers)
    
    # Calculate assigned papers for each reviewer
    assigned_papers = reverse_dict(selected_reviewers)
    
    # Update willing papers by removing already assigned papers
    reviewer_willing_papers = {}
    for i in range(1, num_reviewers+1):
        if i in willing_papers:
            reviewer_willing_papers[i] = list(set(willing_papers[i]) - set(assigned_papers.get(i, [])))
    
    # Perform local search
    optimized_assignments, final_load = local_search(num_papers, num_reviewers, reviews_per_paper, reviewer_willing_papers, assigned_papers, current_load)
    selected_reviewers=reverse_dict(optimized_assignments)
    """print(num_papers)
    for paper, reviewers in selected_reviewers.items():
        print(f"{reviews_per_paper} {' '.join(map(str, reviewers))}")"""
    print(f"Max load: {max(final_load.values())}")
    
if __name__ == "__main__":
    main()
