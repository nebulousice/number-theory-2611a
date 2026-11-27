# NTA-1 certificate: Banerjee–Smoot Conjecture 6.1 fails at α = 3

Target `number-theory-2611a`, stage 5 (Certify), 2026-11-27. Source: K. Banerjee and N. A. Smoot, [arXiv:2611.09681v1](https://arxiv.org/abs/2611.09681v1), §6, Conjecture 6.1. The statement was re-read in the [HTML v1](https://arxiv.org/html/2611.09681v1) on 2026-11-27.

## Claim certified

Let $P^{[1]}_a=(-q;q)_\infty^a/(q;q)_\infty$ and $P^{[2]}_a=(-q;q)_\infty^a/(q;q)_\infty^5$. Take $\alpha=3$ and $n=0$, so the modulus is $11^{\lceil 3/2\rceil}=121$.

| Part | a | Class of a mod 11 | Congruence for δ | δ (least residue mod 1331) | Coefficient at $q^{54}$ | mod 121 |
| --- | --- | --- | --- | --- | --- | --- |
| (1) | 36 | 3 (allowed: 3, 5, 7) | 24·54 − (1 − 36) = 1331 | 54 | 62043410886974649205238011198 | **33** |
| (2) | 40 | 7 (allowed: not 1, 3, 5) | 24·54 − (5 − 40) = 1331 | 54 | 66134580699742235651549220246110 | **55** |

The conjecture requires both residues to be 0. Both coefficients are ≡ 0 (mod 11), with 11-adic valuation exactly 1. So the α = 1 and α = 2 instances (modulus 11) hold at m = 54, and the failure occurs exactly at α = 3.

**The other solutions of the δ-congruence also fail.** The δ-congruence fixes δ only mod 1331. Every non-negative solution is 54 + 1331t, and the conjecture with n ∈ ℕ₀ for the least residue covers all of them. The coefficients at m = 54 + 1331t for t = 1, 2, 3 are also nonzero mod 121, so the witness survives the choice δ = 1385, 2716 or 4047:

| m | p^{[1]}_{36}(m) mod 121 | p^{[2]}_{40}(m) mod 121 |
| --- | --- | --- |
| 54 | 33 | 55 |
| 1385 | 11 | 55 |
| 2716 | 11 | 66 |
| 4047 | 11 | 99 |

The full integers are in `out/NTA-1.out` and `out/NTA-1_x.out`.

## Files

| File | Role |
| --- | --- |
| `NTA-1.py` | Primary certificate. python-flint `fmpz_series`: exact truncated products ∏(1 ± q^k), then power and exact series division. It checks the series division by multiplying back, checks the building blocks against Euler's pentagonal series, A000009 and p(100) = 190569292, computes δ by modular inverse, and checks the residue class. |
| `NTA-1_x.mjs` | Independent cross-check, written in Node.js BigInt with no libraries. It uses the divisor-sum recurrence n·p(n) = Σ s(k) p(n−k), with s(k) = Σ_{d∣k} d(b + a(−1)^{k/d+1}), from the logarithmic derivative, and checks that every division is exact. δ is found by brute-force search over [0, 1331), and its uniqueness is checked. No code is shared with the primary. |
| `compare.py` | Parses the JSON result lines of both outputs and requires them to be identical and both verdicts to be PASS. |
| `run_all.sh` | Runs all three. Each output gets a header with the command, UTC date, commit, sha256 of the scripts, Python, python-flint and Node versions, and host, plus exit code and wall time at the end. |
| `gen_lean_stages.py` | Writes the untrusted stage literals `lean/Pipeline/BanerjeeSmoot/Stages.lean`, which the Lean kernel re-checks step by step. |
| `out/NTA-1.out`, `out/NTA-1_x.out`, `out/compare.out` | Archived outputs of the clean run. Never edited by hand. |

## Clean run (2026-11-27)

The repo was cloned locally and `dd8b84c97441f4ebcb236aa8fbb87676ea5b88b8` checked out. The cert files are not in that commit, so they were copied in; their sha256 hashes are recorded in each header. The run command was `bash targets/number-theory-2611a/cert/NTA-1/run_all.sh 3`, and the `out/` directory was copied back unchanged.

| Run | Tools | Wall time | Verdict |
| --- | --- | --- | --- |
| `python NTA-1.py 3` | Python 3.12.10, python-flint 0.7.1 | 91.96 s | `PASS NTA-1 primary (flint fmpz_series)` |
| `node NTA-1_x.mjs 3` | Node v24.20.0 | 16.96 s | `PASS NTA-1 cross-check (Node BigInt, divisor-sum recurrence)` |
| `python compare.py …` | Python 3.12.10 | 23.32 s (host start-up) | `PASS NTA-1 compare (primary and cross-check identical)` |

The host was shared and heavily loaded, so wall times are inflated. No floating point is used in any decision; the only float is the wall-time printout in `run_all.sh`.

To reproduce, run `bash targets/number-theory-2611a/cert/NTA-1/run_all.sh 3` from the repo root. The argument is the number of extra δ-shifts. It needs python-flint 0.7.x and Node ≥ 18.

## Convention audit (source re-read 2026-11-27, arXiv HTML v1)

- **Definitions.** $P^{[1]}_a$ and $P^{[2]}_a$ are as above, with $a\in\mathbb{Z}$. They are the standard Pochhammer products $(-q;q)_\infty=\prod_{k\ge1}(1+q^k)$ and $(q;q)_\infty=\prod_{k\ge1}(1-q^k)$. Both implementations use exactly these.
- **Quantifiers.** The source says "Let α∈ℕ and n∈ℕ₀". α = 3 lies in ℕ whether or not ℕ contains 0, and n = 0 lies in ℕ₀.
- **δ.** The source defines δ only by $24\delta\equiv c-a\pmod{11^\alpha}$, with no normalisation. Every non-negative solution is 54 + 1331t. The least one, 54, gives the strongest statement, and it implies the statements for all the others. Negative solutions give negative arguments, which carry zero coefficients. For the alternative choices t = 1, 2, 3, the n = 0 coefficients are also nonzero mod 121 (table above). No choice of δ among those checked rescues the conjecture.
- **Modulus.** The source has $11^{\lceil\alpha/2\rceil}$, which is 121 at α = 3. The Gate decoded ⌈ ⌉ from the PDF glyphs, and it agrees with Theorem 1.1's $\lfloor(\alpha+1)/2\rfloor$. Under a floor reading, $11^{\lfloor 3/2\rfloor}=11$, both witnesses would *satisfy* the congruence (both are ≡ 0 mod 11). That is the only reading found under which these witnesses do not refute the statement, and it contradicts the printed ⌈ ⌉ and Theorem 1.1.
- **Residue classes.** 36 ≡ 3 (mod 11), which is allowed in part (1). 40 ≡ 7 (mod 11), which is allowed in part (2), since 7 ∉ {1, 3, 5}.

## Lean

`lean/Pipeline/BanerjeeSmoot/Main.lean` imports the generated `Stages.lean`. The command `bash scripts/lean_check.sh BanerjeeSmoot` gives **PASS** on Lean 4.37.0-rc1 with Mathlib (2026-11-27; log in `out/lean_check.out`). The axioms are `propext`, `Classical.choice` and `Quot.sound`. There is no `sorry` and no `native_decide`.

Theorem `BanerjeeSmoot.NTA1` works in ℤ⟦X⟧ with $F_{54}=\prod_{k=1}^{54}(1+X^k)$ and $E_{54}=\prod_{k=1}^{54}(1-X^k)$. It proves:
- an inverse of $E_{54}$ and of $E_{54}^5$ exists;
- for every $G$ with $G E_{54}=1$, $[X^{54}](F_{54}^{36}G)\bmod 121=33$ and $121\nmid[X^{54}](F_{54}^{36}G)$;
- for every $G$ with $G E_{54}^5=1$, $[X^{54}](F_{54}^{40}G)\bmod 121=55$ and $121\nmid$ that coefficient.

`part1_coeff` and `part2_coeff` give the exact integers, and `side_conditions` checks the residue classes and the δ-congruences.

One step is not formalized: the passage from the infinite products to the truncations $k\le 54$. Mathlib has no $(q;q)_\infty$, and factors with $k\ge 55$ are $\equiv 1 \pmod{q^{55}}$.
