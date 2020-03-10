import math
a=int(input())
b=int(input())

if a<0 and b<0:
    a=abs(a)
    b=abs(b)
    print(a//b)
if a>0 and b<0:
    # b=abs(b)
    print(math.ceil(a/b))
