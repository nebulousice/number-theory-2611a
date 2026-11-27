"""witness_naive.py -- third, definition-level check of the two smallest witnesses (pure Python, no shortcuts).

P^{[1]}_a = (-q;q)_inf^a / (q;q)_inf  and  P^{[2]}_a = (-q;q)_inf^a / (q;q)_inf^5, truncated at q^54:
only the factors with n <= 54 matter.  Multiply by (1 + q^n) a times and by 1/(1 - q^n) c times.
"""
D = 54

def coeff(a, c, D):
    p = [1] + [0] * D
    for n in range(1, D + 1):
        for _ in range(a):                      # times (1 + q^n)
            for i in range(D, n - 1, -1):
                p[i] += p[i - n]
        for _ in range(c):                      # times 1/(1 - q^n)
            for i in range(n, D + 1):
                p[i] += p[i - n]
    return p[D]

for part, c, a in ((1, 1, 36), (2, 5, 40)):
    assert (24 * 54 - (c - a)) % 11 ** 3 == 0 and a % 11 in ((3, 5, 7) if c == 1 else (0, 2, 4, 6, 7, 8, 9, 10))
    v = coeff(a, c, D)
    print(f"part ({part}): a = {a} = {a % 11} mod 11, alpha = 3, delta = 54, n = 0")
    print(f"  p(54) = {v}")
    print(f"  p(54) mod 11 = {v % 11},  p(54) mod 121 = {v % 121}   (Conjecture 6.1 requires 0 mod 121)")
