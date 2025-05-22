import random

def generate_test_case():
    P = 9000  # Số papers
    R = 300 # Số reviewers
    K = 30   # Số reviewers mỗi paper cần
    min_reviewers_per_paper = 100 # Mỗi paper có 5 reviewers sẵn sàng

    with open('/workspaces/rtewr/Project/input.txt', 'w') as f:
        # Dòng đầu: P R K
        f.write(f"{P} {R} {K}\n")
        
        # Mỗi paper chọn ngẫu nhiên 5 reviewers từ R reviewers
        for paper in range(1, P + 1):
            reviewers = random.sample(range(1, R + 1), min_reviewers_per_paper)
            f.write(f"{min_reviewers_per_paper} {' '.join(map(str, reviewers))}\n")

if __name__ == "__main__":
    generate_test_case()