__author__ = 'Antti'

import time

print time.time()


print 'This is the testfile!!!'
A = 5
B = 3
C = A + B
print 'A + B is', C



def fib(n):    # write Fibonacci series up to n
    "Print a Fibonacci series up to n"
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a+b

fib(7)