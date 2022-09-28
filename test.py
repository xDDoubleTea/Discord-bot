def foo(m,n):
    return m+n/(n*m+4)

total = 0
for i in range(2015):
    total = foo(i+1,i+2)

print(total)

