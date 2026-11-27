"""Shared helpers for targets/number-theory-2611a (Banerjee-Smoot Conj. 6.1).

Two independent ways to get p^{[c]}_a(n) = [q^n] f_2^a / f_1^(a+c):

  impl 1  series_mod(...)   python-flint fmpz_mod_poly, truncated products mod 11^K
  impl 2  sigma_exact(...)  pure Python big integers, the logarithmic-derivative
                            recurrence  n p(n) = sum_{k=1..n} s(k) p(n-k),
                            s(k) = (a+c) sigma(k) - 2 a sigma(k/2)   (exact, no modulus)

Conventions (source: arXiv:2611.09681v1, Section 6):
  f_m = (q^m; q^m)_infinity,  P^{[1]}_a = f_2^a/f_1^(a+1)  (c = 1),  P^{[2]}_a = f_2^a/f_1^(a+5)  (c = 5),
  delta = least non-negative residue of (c - a)/24 mod 11^alpha,
  conjectured modulus 11^ceil(alpha/2).
"""
from flint import fmpz_mod_poly_ctx

ALLOWED = {1: {3, 5, 7}, 5: {0, 2, 4, 6, 7, 8, 9, 10}}


def delta(a, c, alpha):
    m = 11 ** alpha
    return ((c - a) * pow(24, -1, m)) % m


def val11(v, cap=99):
    v = int(v)
    if v == 0:
        return cap
    k = 0
    while v % 11 == 0:
        v //= 11
        k += 1
    return k


def euler_coeffs(N, step):
    """Coefficients of prod_{n>=1} (1 - q^(step n)) up to q^(N-1) (pentagonal number theorem)."""
    c = [0] * N
    k = 0
    while True:
        e1 = step * k * (3 * k - 1) // 2
        e2 = step * k * (3 * k + 1) // 2
        if e1 >= N:
            break
        s = 1 if k % 2 == 0 else -1
        c[e1] += s
        if k > 0 and e2 < N:
            c[e2] += s
        k += 1
    return c


class ModSeries:
    """Truncated power series mod 11^K with python-flint (impl 1)."""

    def __init__(self, N, K):
        self.N, self.K, self.M = N, K, 11 ** K
        self.R = fmpz_mod_poly_ctx(self.M)
        self.f1 = self.R(euler_coeffs(N, 1))
        self.f2 = self.R(euler_coeffs(N, 2))
        self.f1i = self.f1.inverse_series_trunc(N)
        self.f2i = self.f2.inverse_series_trunc(N)
        self.E = self.f2.mul_low(self.f1i, N)    # f_2/f_1 = (-q;q)_inf
        self.Ei = self.f1.mul_low(self.f2i, N)

    def base(self, c):
        return self.f1i.pow_trunc(c, self.N)     # 1/f_1^c  (= P_0)

    def P(self, a, c):
        b = self.base(c)
        if a >= 0:
            return b.mul_low(self.E.pow_trunc(a, self.N), self.N)
        return b.mul_low(self.Ei.pow_trunc(-a, self.N), self.N)

    def coeffs(self, P):
        co = [int(t) for t in P.coeffs()]
        return co + [0] * (self.N - len(co))

    def sweep(self, c, a_lo, a_hi):
        """Yield (a, coefficient list) for a = a_lo..a_hi, one truncated product per step."""
        P = self.P(a_lo, c)
        for a in range(a_lo, a_hi + 1):
            yield a, self.coeffs(P)
            P = P.mul_low(self.E, self.N)


def min_vals(co, a, c, alphas, cap):
    """For each alpha: (min 11-adic valuation over n with 11^alpha n + delta < len(co), count, first n attaining it)."""
    out = []
    N = len(co)
    for al in alphas:
        m, d = 11 ** al, delta(a, c, al)
        best, cnt, arg = None, 0, None
        for i, n in enumerate(range(d, N, m)):
            v = val11(co[n], cap)
            cnt += 1
            if best is None or v < best:
                best, arg = v, i
        out.append((best, cnt, arg))
    return out


def sigma_table(N):
    s = [0] * (N + 1)
    for d in range(1, N + 1):
        for m in range(d, N + 1, d):
            s[m] += d
    return s


def sigma_exact(a, c, N, sig=None):
    """Exact integers p^{[c]}_a(0..N) by the sigma recurrence (impl 2, pure Python)."""
    if sig is None:
        sig = sigma_table(N)
    s = [0] * (N + 1)
    for k in range(1, N + 1):
        s[k] = (a + c) * sig[k] - (2 * a * sig[k // 2] if k % 2 == 0 else 0)
    p = [0] * (N + 1)
    p[0] = 1
    for n in range(1, N + 1):
        t = 0
        for k in range(1, n + 1):
            t += s[k] * p[n - k]
        q, r = divmod(t, n)
        assert r == 0
        p[n] = q
    return p
