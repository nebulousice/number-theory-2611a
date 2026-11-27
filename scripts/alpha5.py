"""alpha5.py -- test of the carry criterion at alpha = 5 (lead L2; numerical).

Usage: python alpha5.py c N count
Picks the 'count' smallest |a| with carry(1), carry(3) and NOT carry(5), and the 'count' smallest |a| >= 1331
with carry(1), carry(3), carry(5); prints min v_11 on the progressions alpha = 1..5 (index < N, mod 11^5).
Prediction: first group has min valuation 2 at alpha = 5 (conjecture needs 3), second group has >= 3.
"""
import sys, time
from bs_common import ModSeries, min_vals, delta

c, N, cnt = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rho = lambda al: (c * pow(8, -1, 11 ** al)) % 11 ** al
carry = lambda a, al: delta(a, c, al) > rho(al)
cand = sorted(range(-40000, 40001), key=abs)
bad = [a for a in cand if carry(a, 1) and carry(a, 3) and not carry(a, 5)][:cnt]
good = [a for a in cand if abs(a) >= 1331 and carry(a, 1) and carry(a, 3) and carry(a, 5)][:cnt]
ms = ModSeries(N, 5)
t0 = time.time()
for tag, lst in (("no carry(5): predicted to fail at alpha=5", bad), ("carry(1,3,5): predicted to hold", good)):
    print(tag)
    for a in lst:
        co = ms.coeffs(ms.P(a, c))
        mv = min_vals(co, a, c, (1, 2, 3, 4, 5), 9)
        print(f"  c={c} a={a} (mod 11: {a % 11})  delta_5={delta(a, c, 5)} rho_5={rho(5)}  min v_11 = {[m[0] for m in mv]}  counts = {[m[1] for m in mv]}  ({time.time() - t0:.0f} s)", flush=True)
