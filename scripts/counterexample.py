"""counterexample.py -- exact witnesses against Conjecture 6.1 of arXiv:2611.09681v1.

Usage:  python counterexample.py c a alpha [max_index]
  c = 1 (part (1)) or 5 (part (2));  a must lie in an allowed class mod 11.

For the progression 11^alpha n + delta (24 delta = c - a mod 11^alpha) it prints every n with
index <= max_index, the exact integer p^{[c]}_a(11^alpha n + delta) and its 11-adic valuation, from
  impl 2: pure Python sigma recurrence (exact integers),
  impl 3: python-flint fmpz_series, exact product f_2^a * f_1^-(a+c) (no modulus),
and compares them.  A value with valuation < ceil(alpha/2) contradicts the conjecture for this a.
"""
import sys, hashlib
from bs_common import delta, val11, sigma_exact, euler_coeffs, ALLOWED
import flint
from flint import fmpz_series

c, a, alpha = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
m = 11 ** alpha
d = delta(a, c, alpha)
NMAX = int(sys.argv[4]) if len(sys.argv) > 4 else d + 2 * m
need = (alpha + 1) // 2
assert (a % 11) in ALLOWED[c], "a is not in an allowed class"
print(f"part ({1 if c == 1 else 2}): P = f_2^{a} / f_1^{a + c},  a = {a} = {a % 11} mod 11 (allowed),  alpha = {alpha}")
print(f"delta = {d}  (24*delta - ({c} - {a}) = {24 * d - (c - a)} = 11^{alpha} * {(24 * d - (c - a)) // m}),  conjectured modulus 11^{need}")

# impl 2
p2 = sigma_exact(a, c, NMAX)

# impl 3
flint.ctx.cap = NMAX + 1
def ser(step):
    return fmpz_series(euler_coeffs(NMAX + 1, step), NMAX + 1)
def spow(f, e):
    r = fmpz_series([1], NMAX + 1)
    b = f
    while e:
        if e & 1:
            r = r * b
        b = b * b
        e >>= 1
    return r
f1, f2 = ser(1), ser(2)
one = fmpz_series([1], NMAX + 1)
def zpow(f, e):
    return spow(f, e) if e >= 0 else one / spow(f, -e)
P3 = zpow(f2, a) * zpow(f1, -(a + c))
p3 = [int(P3[i]) for i in range(NMAX + 1)]

agree = p2 == p3
print(f"impl 2 == impl 3 on all coefficients 0..{NMAX}: {agree}")
print(f"sha256 of the coefficient list: {hashlib.sha256(repr(p2).encode()).hexdigest()}")
viol = 0
for n in range((NMAX - d) // m + 1):
    idx = m * n + d
    v = p2[idx]
    k = val11(v)
    flag = "VIOLATES" if k < need else "ok"
    viol += k < need
    s = str(v)
    short = s if len(s) <= 60 else f"{s[:25]}...{s[-25:]} ({len(s)} digits)"
    print(f"  n={n}  index={idx}  v_11={k}  mod 11^{need + 1} = {v % 11 ** (need + 1)}  value={short}  {flag}")
    if k < need and viol == 1:
        print(f"    full value: {v}")
print(f"RESULT: {viol} violating value(s) among the first {(NMAX - d) // m + 1};  implementations agree: {agree}")
