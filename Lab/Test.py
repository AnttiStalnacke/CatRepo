__author__ = 'Antti'

import time

print time.time()


print 'This is the testfile!!!'
A = 5
B = 3
C = A + B
print 'A + B is', C
print 'this has nothing to do with time, yet'
D = A*B
print 'But it does multiplication. A times B is', D

print 'And we step this as well'


def fib(n):    # write Fibonacci series up to n
    "Print a Fibonacci series up to n"
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a+b

fib(6)
