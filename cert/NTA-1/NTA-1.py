#!/usr/bin/env python3
"""NTA-1 primary certificate (python-flint, exact fmpz power series).

Claim (targets/number-theory-2611a, ledger row NTA-1): Banerjee-Smoot Conj. 6.1
(arXiv:2611.09681v1, Section 6) fails in both parts at alpha = 3, n = 0.

    P1_a(q) = (-q;q)_inf^a / (q;q)_inf       part (1): a = 3,5,7 (mod 11), 24*delta = 1 - a (mod 11^alpha)
    P2_a(q) = (-q;q)_inf^a / (q;q)_inf^5     part (2): a != 1,3,5 (mod 11), 24*delta = 5 - a (mod 11^alpha)
    claim: p_a(11^alpha n + delta) = 0 (mod 11^ceil(alpha/2)).

Witnesses: part (1) a = 36, part (2) a = 40, alpha = 3, delta = 54 (least non-negative
residue), n = 0.  Expected p1_36(54) = 62043410886974649205238011198 = 33 (mod 121) and
p2_40(54) = 66134580699742235651549220246110 = 55 (mod 121).

Method: build (-q;q)_inf = prod_{k<=N}(1+q^k) and (q;q)_inf = prod_{k<=N}(1-q^k) as exact
truncated integer power series (flint fmpz_series, precision N+1; factors with k > N do not
affect coefficients of q^0..q^N), raise to the power and divide exactly.  The series
quotient is exact because (q;q)_inf has constant term 1.  No floating point is used.

Also computed (convention audit): the coefficients at m = 54 + 1331*n for n = 1, 2, 3, which
are the n = 0 witnesses for the alternative choices delta = 54 + 1331*n of a solution of the
delta-congruence.

Usage: python NTA-1.py [NMAX_EXTRA]   (default 3: n = 0..3)
"""
import json
import sys
import flint

ALPHA = 3
MOD_DELTA = 11 ** ALPHA                    # 1331
EXP = (ALPHA + 1) // 2                     # ceil(alpha/2) by integer arithmetic = 2
MOD_CLAIM = 11 ** EXP                      # 121

CASES = [
    # part, a, power b of 1/(q;q), c in 24*delta = c - a, allowed classes test, expected
    dict(part=1, a=36, b=1, c=1, expected=62043410886974649205238011198, residue=33),
    dict(part=2, a=40, b=5, c=5, expected=66134580699742235651549220246110, residue=55),
]


def allowed(part, a):
    r = a % 11
    if part == 1:
        return r in (3, 5, 7)
    return r not in (1, 3, 5)


def v11(x):
    if x == 0:
        return None
    v = 0
    while x % 11 == 0:
        x //= 11
        v += 1
    return v


def series_product(N, sign):
    """prod_{k=1}^{N} (1 + sign*q^k) as exact fmpz_series of precision N+1."""
    s = flint.fmpz_series([1], prec=N + 1)
    for k in range(1, N + 1):
        coeffs = [0] * (k + 1)
        coeffs[0] = 1
        coeffs[k] = sign
        s = s * flint.fmpz_series(coeffs, prec=N + 1)
    return s


def coeff(s, m):
    c = s.coeffs()
    return int(c[m]) if m < len(c) else 0


def main():
    n_extra = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    ok = True
    inv24 = pow(24, -1, MOD_DELTA)
    assert (24 * inv24) % MOD_DELTA == 1
    deltas = {}
    for case in CASES:
        a, c, part = case["a"], case["c"], case["part"]
        d = ((c - a) * inv24) % MOD_DELTA      # least non-negative residue
        deltas[part] = d
        cong = (24 * d - (c - a)) % MOD_DELTA == 0
        print(f"part ({part}): a = {a}, a mod 11 = {a % 11}, allowed = {allowed(part, a)}; "
              f"delta = {d} (least residue mod {MOD_DELTA}); 24*delta - ({c}-a) = {24*d - (c - a)} "
              f"= {(24*d - (c - a)) // MOD_DELTA}*{MOD_DELTA}; congruence holds = {cong}")
        ok &= allowed(part, a) and cong and d == 54
        # sanity: the excluded classes are really excluded (statement edge cases)
    print("allowed classes part (1):", [r for r in range(11) if allowed(1, r)])
    print("allowed classes part (2):", [r for r in range(11) if allowed(2, r)])
    print(f"alpha = {ALPHA}, modulus 11^ceil(alpha/2) = 11^{EXP} = {MOD_CLAIM}")

    N = 54 + MOD_DELTA * n_extra
    flint.ctx.cap = N + 1
    E = series_product(N, -1)                  # (q;q)_inf mod q^(N+1)
    F = series_product(N, +1)                  # (-q;q)_inf mod q^(N+1)
    # sanity checks of the building blocks against classical values
    eul = [coeff(E, k) for k in range(16)]
    assert eul == [1, -1, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, -1, 0, 0, -1], eul   # Euler pentagonal
    dist = [coeff(F, k) for k in range(11)]
    assert dist == [1, 1, 1, 2, 2, 3, 4, 5, 6, 8, 10], dist                  # A000009
    pinv = 1 / E
    assert [coeff(pinv, k) for k in range(11)] == [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]  # A000041
    flint.ctx.cap = max(N + 1, 101)
    assert coeff(1 / series_product(100, -1), 100) == 190569292                # p(100)
    flint.ctx.cap = N + 1

    results = []
    for case in CASES:
        a, b, part = case["a"], case["b"], case["part"]
        P = (F ** a) / (E ** b)
        # exactness check: P * E^b == F^a up to precision
        chk = P * (E ** b) - F ** a
        assert all(int(x) == 0 for x in chk.coeffs()), "series division not exact"
        d = deltas[part]
        rows = []
        for n in range(n_extra + 1):
            m = MOD_DELTA * n + d
            val = coeff(P, m)
            rows.append(dict(n=n, m=m, value=str(val), mod121=val % 121, mod11=val % 11, v11=v11(val)))
            print(f"  p^[{part}]_{a}({m}) = {val}")
            print(f"     mod 121 = {val % 121}, mod 11 = {val % 11}, v_11 = {v11(val)}")
        w = rows[0]
        good = (int(w["value"]) == case["expected"] and w["mod121"] == case["residue"]
                and w["mod121"] != 0)
        print(f"part ({part}) witness n=0: value matches claim = {int(w['value']) == case['expected']}, "
              f"residue mod 121 = {w['mod121']} (claimed {case['residue']}), nonzero mod 121 = {w['mod121'] != 0}")
        # the failure is exactly at alpha = 3: alpha = 1,2 congruences (mod 11) hold for m = 54
        a1 = (case["c"] - a) * pow(24, -1, 11) % 11
        a2 = (case["c"] - a) * pow(24, -1, 121) % 121
        print(f"   lower levels: delta_1 = {a1} (54 mod 11 = {54 % 11}), delta_2 = {a2} (54 mod 121 = {54 % 121}); "
              f"value mod 11 = {w['mod11']}")
        ok &= good
        results.append(dict(part=part, a=a, b=b, delta=d, rows=rows))
    print("JSON " + json.dumps(dict(alpha=ALPHA, results=results), sort_keys=True))
    print(f"flint {flint.__version__}, N = {N}")
    print("PASS NTA-1 primary (flint fmpz_series)" if ok else "FAIL NTA-1 primary (flint fmpz_series)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
