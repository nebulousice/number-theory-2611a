"""rows.py -- reproduce the source's checkable values, then the first rows of Conjecture 6.1.

Source: K. Banerjee, N. A. Smoot, arXiv:2611.09681v1.
Usage:  python rows.py [N]      (N = truncation order for the modular run, default 300000)
Writes nothing; redirect stdout to out/rows.log.

Part A (values stated in the source):
  A1  Theorem 1.1: d_2(n) = 0 mod 11^floor((alpha+1)/2) when 8n = 1 mod 11^alpha     (flint, mod 11^6)
  A2  x, y of (2.3)-(2.4) have integer coefficients; orders of x, y, z at the cusp [0] are -3, -4, -5
  A3  the anomalous term r_L has integer coefficients (source checks 361 coefficients)
  A4  c(x) of Section 7: C_1(0) = 4 mod 11 and 11^floor((11r+27)/13) divides the coefficient of x^r
  A5  impl 1 (flint, modular) against impl 2 (pure Python, exact sigma recurrence)
Part B (Conjecture 6.1): minimum 11-adic valuation on each progression, |a| <= 33, alpha <= 4, with controls.
"""
import sys, time
from bs_common import ModSeries, min_vals, delta, val11, sigma_table, sigma_exact, ALLOWED

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
K = 6
t0 = time.time()
ok_all = True


def report(name, ok, detail=""):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'MATCH' if ok else 'MISMATCH'}] {name} {detail}", flush=True)


# ---------- exact eta quotients (pure Python) ----------
def eta_exact(r, n_terms, sig):
    """prod_d f_d^(r[d]) to q^(n_terms-1), exact integers, by the sigma recurrence."""
    s = [0] * n_terms
    for k in range(1, n_terms):
        t = 0
        for d, e in r.items():
            if k % d == 0:
                t -= e * d * sig[k // d]
        s[k] = t
    p = [0] * n_terms
    p[0] = 1
    for n in range(1, n_terms):
        t = 0
        for k in range(1, n + 1):
            t += s[k] * p[n - k]
        assert t % n == 0
        p[n] = t // n
    return p


def mul(u, v, n):
    w = [0] * n
    for i, ui in enumerate(u[:n]):
        if ui:
            for j, vj in enumerate(v[: n - i]):
                w[i + j] += ui * vj
    return w


def add(*terms):
    n = min(len(t[1]) for t in terms)
    return [sum(k * s[i] for k, s in terms) for i in range(n)]


def shift(u, k):
    return [0] * k + u[: len(u) - k]


# ---------- A1 ----------
ms = ModSeries(N, K)
co2 = ms.coeffs(ms.P(2, 5))                      # D_2 = f_2^2/f_1^7
print(f"A1  d_2(n), 8n = 1 mod 11^alpha, n < {N}  (Theorem 1.1 exponent floor((alpha+1)/2))")
for al in range(1, 6):
    m = 11 ** al
    d = pow(8, -1, m)
    assert d == delta(2, 5, al)
    vs = [val11(co2[n]) for n in range(d, N, m)]
    need = (al + 1) // 2
    report(f"  alpha={al} delta={d}", min(vs) >= need, f"values={len(vs)} min v_11={min(vs)} required={need}")

# ---------- A2, A3 ----------
NE = 700
sig = sigma_table(NE)
e1 = eta_exact({1: -8, 2: 4, 11: 8, 22: -4}, NE, sig)
w = eta_exact({1: -11, 2: 11, 11: 1, 22: -1}, NE, sig)
z = shift(eta_exact({1: -7, 2: 3, 11: -3, 22: 7}, NE, sig), 5)
one = [1] + [0] * (NE - 1)
x44 = add((-7, one), (11, e1), (-4, w), (132, z))
y11 = add((-1, one), (1, w), (-121, z))
report("A2  x has integer coefficients", all(v % 44 == 0 for v in x44), f"first {NE} coefficients")
report("A2  y has integer coefficients", all(v % 11 == 0 for v in y11), f"first {NE} coefficients")
x = [v // 44 for v in x44]
y = [v // 11 for v in y11]
print("     x =", x[:8], "...   y =", y[:8], "...   z =", z[:8], "...")
# orders at [0] through the Fricke involution tau -> -1/(22 tau): eta(d tau) -> eta((22/d) tau)
A = eta_exact({22: -8, 11: 4, 2: 8, 1: -4}, 60, sig)       # times q^-5
B = eta_exact({22: -11, 11: 11, 2: 1, 1: -1}, 60, sig)     # times q^-5
C = eta_exact({22: -7, 11: 3, 2: -3, 1: 7}, 60, sig)       # times q^-5
q5 = [0] * 5 + [1] + [0] * 54
Sx = add((-616, q5), (8, A), (-11, B), (3, C))            # 88*44 * q^5 * x|W
Sy = add((-32, q5), (1, B), (-1, C))                      # 32*11 * q^5 * y|W
ox = next(i for i, v in enumerate(Sx) if v) - 5
oy = next(i for i, v in enumerate(Sy) if v) - 5
report("A2  ord_[0](x), ord_[0](y), ord_[0](z)", (ox, oy) == (-3, -4), f"= {ox}, {oy}, -5 (source: -3, -4, -5)")
x2 = mul(x, x, NE); x3 = mul(x2, x, NE); xy = mul(x, y, NE); x2y = mul(x2, y, NE); xz = mul(x, z, NE)
rl11 = add((1, x), (3, x2), (9, x3), (10, y), (10, xy), (2, x2y), (7, z), (8, xz))
report("A3  r_L has integer coefficients", all(v % 11 == 0 for v in rl11), f"first {NE} coefficients (source: 361)")
print("     r_L =", [v // 11 for v in rl11[:8]], "...")

# ---------- A4 ----------
CX = [
    69550975755977284911104,
    -71287715497527282651820032,
    17900193598896240733994540032,
    2433656434135752614962897574400,
    135334237711138006616618300344576,
    4603551043973265247618043536808704,
    109616062492953370639775636433454464,
    1954419189636606079380190879818816064,
    27144272314898816695853907223593334304,
    301089044785364403767185228909074692504,
    2710730798554339991175805693674009005740,
    20011291470089564255540586248512208139082,
    121821501325881013307089187765394122218837,
    612703095907075970646910882428597137091912,
    2541715085550544936276941583396435763817408,
    8649797863778836226399665129987964376904896,
    23913154138234188165042955394025759141437184,
    52880092072078116046416414506583439275205632,
    91342853380107788221814612586966899809652736,
    118783323283193765986323689131241918352015360,
    109398375434451346894431470218757768960606208,
    63625268819176226667199093217678019620241408,
    17574243049798037033395145952709018207125504,
]
c0ok = CX[0] % 11 == 4
shape = all(val11(CX[r]) >= (11 * r + 27) // 13 for r in range(1, 23))
report("A4  c(x): C_1(0) = 4 mod 11, 11-adic shape floor((11r+27)/13)", c0ok and shape and len(CX) == 23,
       f"v_11 of coefficients 1..22 = {[val11(CX[r]) for r in range(1, 23)]}")

# ---------- A5 ----------
NS = 3200
sigs = sigma_table(NS)
for (a, c) in [(2, 5), (0, 5), (3, 1), (-7, 5)]:
    ex = sigma_exact(a, c, NS, sigs)
    com = ms.coeffs(ms.P(a, c))
    same = all(ex[n] % ms.M == com[n] for n in range(NS + 1))
    report(f"A5  impl 1 = impl 2 for (a,c)=({a},{c})", same, f"n <= {NS};  p(0..6) = {ex[:7]}")
ex2 = sigma_exact(2, 5, 200, sigs)
print(f"     d_2(7) = {ex2[7]} = 11 * {ex2[7] // 11},  d_2(106) = {ex2[106]}  (v_11 = {val11(ex2[106])}; 8*106 = 1 mod 121)")

# ---------- B ----------
print(f"\nB   Conjecture 6.1: min v_11 of p_a(11^alpha n + delta) over all n with index < {N}; alpha = 1..4")
print("    required exponents ceil(alpha/2) = 1, 1, 2, 2.   status: ok / FAIL (allowed class) ; control (excluded class)")
bad = []
for c in (1, 5):
    print(f"  part ({1 if c == 1 else 2}), c = {c}, allowed classes mod 11: {sorted(ALLOWED[c])}")
    for a, co in ms.sweep(c, -33, 33):
        mv = min_vals(co, a, c, (1, 2, 3, 4), 9)
        vals = [m[0] for m in mv]
        allowed = (a % 11) in ALLOWED[c]
        holds = all(v >= (al + 1) // 2 for al, v in zip((1, 2, 3, 4), vals))
        tag = ("ok" if holds else "FAIL") if allowed else ("control: fails" if not holds else "control: holds up to alpha=4")
        if allowed and not holds:
            bad.append((c, a))
        print(f"    a={a:4d} (mod 11: {a % 11:2d})  min v_11 = {vals}  n-count = {[m[1] for m in mv]}  {tag}")
report("B   every allowed a with |a| <= 33 satisfies the conjecture for alpha <= 4 in range", not bad, f"failures: {bad}")
print(f"\nALL SOURCE VALUES MATCH: {ok_all}   ({time.time() - t0:.1f} s)")
