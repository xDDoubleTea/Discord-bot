from math import sqrt

a,b,c = input().split()

a,b,c = int(a), int(b), int(c)
if ((b*b) -(4*a*c)) > 0:
    sqrt = sqrt(((b*b) -(4*a*c)))
    x1 = (-b+sqrt)/(2*a)
    x2 = (-b-sqrt)/(2*a)
    if x1 < x2:
        x1 , x2 = x2 , x1
    print(f"Two different roots x1={int(x1)} , x2={int(x2)}")
elif ((b*b) -(4*a*c)) == 0:
    sqrt = sqrt(((b*b) -(4*a*c)))
    x = (-b+sqrt)/(2*a)
    print(f"Two same roots x={int(x)}")
elif ((b*b) -(4*a*c)) < 0:
    print("No real root")