"""scan_a.py -- wide scan in the exponent a, and test of the carry criterion.

Usage:  python scan_a.py N A_LO A_HI out.json
For c in {1, 5} and every a in [A_LO, A_HI] it records the minimum 11-adic valuation of
p^{[c]}_a(11^alpha n + delta) over all n with index < N, for alpha = 1, 2, 3 (python-flint, mod 11^4).

Carry criterion tested here (our lead L2, numerical):
  rho_alpha = least non-negative residue of c/8 mod 11^alpha,
  carry(alpha) :<=> delta_alpha(a) > rho_alpha  <=>  delta_alpha(a) + delta_alpha(-a-c) >= 11^alpha.
  alpha = 1: carry(1) <=> a lies in the source's allowed classes mod 11.
  alpha = 3: is "min valuation >= 2" equivalent to carry(1) and carry(3)?
"""
import sys, json, time
from collections import Counter
from bs_common import ModSeries, min_vals, delta, ALLOWED

N, A0, A1, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
t0 = time.time()
ms = ModSeries(N, 4)
res = {}
for c in (1, 5):
    for a, co in ms.sweep(c, A0, A1):
        res[f"{c},{a}"] = [m[0] for m in min_vals(co, a, c, (1, 2, 3), 9)]
    print(f"c={c} swept a in [{A0},{A1}] at N={N}: {time.time() - t0:.0f} s", flush=True)
json.dump(res, open(out, "w"))

def rho(c, al):
    return (c * pow(8, -1, 11 ** al)) % 11 ** al

for c in (1, 5):
    g = lambda a: res[f"{c},{a}"]
    rng = range(A0, A1 + 1)
    print(f"\npart ({1 if c == 1 else 2}), c = {c}: rho_1 = {rho(c, 1)}, rho_3 = {rho(c, 3)}")
    cls = sorted({a % 11 for a in rng if delta(a, c, 1) > rho(c, 1)})
    print(f"  classes mod 11 with carry(1): {cls}   source's allowed classes: {sorted(ALLOWED[c])}   equal: {cls == sorted(ALLOWED[c])}")
    v1 = sorted({a % 11 for a in rng if g(a)[0] >= 1})
    print(f"  classes mod 11 with min v_11 >= 1 at alpha=1 (data): {v1}")
    allowed = [a for a in rng if a % 11 in ALLOWED[c]]
    print(f"  allowed a in range: {len(allowed)};  alpha<=2 holds for all of them: {all(g(a)[0] >= 1 and g(a)[1] >= 1 for a in allowed)}")
    fails = [a for a in allowed if g(a)[2] < 2]
    print(f"  alpha=3 FAILS (min v_11 = 1 < 2) for {len(fails)} allowed a;  smallest |a|: {sorted(fails, key=abs)[:10]}")
    tab = Counter((delta(a, c, 3) > rho(c, 3), g(a)[2] >= 2) for a in allowed)
    print(f"  (carry(3), alpha=3 holds) counts: {dict(tab)}")
    print(f"  carry(3) => alpha=3 holds, exceptions: {[a for a in allowed if delta(a, c, 3) > rho(c, 3) and g(a)[2] < 2][:10]}")
    nc = [a for a in allowed if delta(a, c, 3) <= rho(c, 3)]
    print(f"  no carry(3): {len(nc)} a, of which alpha=3 still holds for {sum(g(a)[2] >= 2 for a in nc)} (expected about 1/11 if a scalar in F_11 vanishes at random)")
    per = all((g(a)[2] >= 2) == (g(a + 1331)[2] >= 2) for a in allowed if a + 1331 <= A1)
    dual = all(g(a) == g(-a - c) for a in rng if A0 <= -a - c <= A1)
    print(f"  alpha=3 pass/fail periodic in a mod 1331: {per};   profile(a) == profile(-a-c) (W_2 duality): {dual}")
    print(f"  alpha=2 min valuation over allowed a: {dict(Counter(g(a)[1] for a in allowed))};  alpha=3: {dict(Counter(g(a)[2] for a in allowed))}")
