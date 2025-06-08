import random

def generate_test_case():
    P = 700 # Số papers
    R = 70 # Số reviewers
    K = 3  #Số reviewers mỗi paper cần
    

    with open('input.txt', 'w') as f:
        # Dòng đầu: P R K
        f.write(f"{P} {R} {K}\n")
        # Mỗi paper chọn ngẫu nhiên 5 reviewers từ R reviewers
        for paper in range(1, P + 1):
            nums=random.randint(int(0.2*R),int(0.7*R) )
            reviewers= random.sample(range(1, R+1),nums )
            f.write(f"{nums} {' '.join(map(str, reviewers))}\n")
if __name__ == "__main__":
    generate_test_case()