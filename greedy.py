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

@time_execution

def input_data():
    with open('Project/input.txt', 'r') as f:
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
    load = [0] * (num_reviewers + 1)
    sorted_dict = dict(sorted(willing_reviewers.items(), key=lambda item: len(item[1])))
    selected_reviewers = {}
    for paper,reviewers in sorted_dict.items():
        #Sort the reviewers by their current load
        reviewers.sort(key=lambda x: load[x])
        # Select the first K reviewers
        selected_reviewers[paper] = reviewers[:reviews_per_paper]
        # Update the load of the selected reviewers
        for reviewer in selected_reviewers:
            load[reviewer] += 1
    # Find the maximum load
    max_load = max(load[1:])
    return selected_reviewers

def main():
    num_papers, num_reviewers, reviews_per_paper, willing_reviewers, willing_papers = input_data()
    willing_papers=dict(sorted(willing_papers.items(), key=lambda item: len(item[1])))

    if (num_papers*reviews_per_paper) % num_reviewers == 0:
        min_capactice_max_load=(num_papers*reviews_per_paper) // num_reviewers
    else:
        min_capactice_max_load=(num_papers*reviews_per_paper) // num_reviewers + 1
    print(matching_papers(num_papers, num_reviewers, reviews_per_paper, willing_reviewers))
if __name__ == "__main__":
    main()
    