from itertools import combinations
def select_reviewers (reviewers, reviews_per_paper):
   
    return list(combinations(reviewers, reviews_per_paper))

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

def pre_processing_data(willing_reviewers):
    # Sort the reviewers for each paper
    sorted_dict=dict(sorted(willing_reviewers.items(), key=lambda item: len(item[1])))
    return sorted_dict

def backtrack(num_papers, num_reviewers, reviews_per_paper, willing_reviewers):
    load=list(0 for i in range(1,num_reviewers+1))
    max_load=max(load)

    #Choose first paper in willing_reviewers
    items= list(willing_reviewers.items())
    paper,reviewers=items[0]
    subsets_reviewers=select_reviewers(reviewers, reviews_per_paper)
    for subset in subsets_reviewers:
        backtrack(num_papers, num_reviewers, reviews_per_paper, willing_reviewers)


num_papers, num_reviewers, reviews_per_paper, willing_reviewers = input_data()
willing_reviewers=pre_processing_data(willing_reviewers)    