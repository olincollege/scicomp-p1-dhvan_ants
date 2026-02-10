import pickle

with open("runs/case3/data.pkl", 'rb') as f:
    data = pickle.load(f)
    
    sum_r = 0
    sum_lost = 0
    sum_follow = 0
    for r, n in data:
        sum_r += r
        sum_lost += n[0]
        sum_follow += n[1]
        
        
    print(sum_r / 10, sum_lost / 10, sum_follow / 10)