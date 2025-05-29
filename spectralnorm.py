# The Computer Language Benchmarks Game
# https://salsa.debian.org/benchmarksgame-team/benchmarksgame/
#
# Contributed by Sebastien Loisel
# Fixed by Isaac Gouy
# Sped up by Josh Goldfoot
# Dirtily sped up by Simon Descarpentries
# Used list comprehension by Vadim Zelenin
# Concurrency by Jason Stitt
# Concurrency simplified by Matt Vollrath
# Optimized math by Adam Beckmeyer

from math import sqrt
from sys import argv
from time import time


def eval_A(i, j):
    ij = i + j
    return ij * (ij + 1) // 2 + i + 1


def A_sum(u, i):
    return sum(u_j / eval_A(i, j) for j, u_j in enumerate(u))


def At_sum(u, i):
    return sum(u_j / eval_A(j, i) for j, u_j in enumerate(u))


def parallel_A_sum(u, n):
    tmp = [0.0] * n
    @par(num_threads=4)
    for i in range(n):
        tmp[i] = A_sum(u, i)
    return tmp


def parallel_At_sum(tmp, n):
    result = [0.0] * n
    @par(num_threads=4)
    for i in range(n):
        result[i] = At_sum(tmp, i)
    return result


def multiply_AtAv(u):
    n = len(u)
    tmp = parallel_A_sum(u, n)
    return parallel_At_sum(tmp, n)


def main():
    t0 = time()
    n = int(argv[1])
    u = [1.0] * n

    for _ in range(10):
        v = multiply_AtAv(u)
        u = multiply_AtAv(v)

    vBv = vv = 0.0

    for ue, ve in zip(u, v):
        vBv += ue * ve
        vv += ve * ve

    result = sqrt(vBv/vv)
    t1 = time()
    print(f'{result} in {t1 - t0} seconds')


if __name__ == '__main__':
    main()
