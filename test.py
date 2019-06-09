import random

b = [1,2,3,4,5,6,7,8,5,4,2,10]

print(b)

for i in range(len(b)) :
    idx = random.randrange(len(b))
    print(b[idx])
    del b[idx]
    print(b)