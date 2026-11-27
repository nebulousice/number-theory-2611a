# Conjecture 6.1 of Banerjee and Smoot fails at $`\alpha=3`$

*Write-up, 2026-11-27. Paper: [`paper.pdf`](paper.pdf), Zenodo [doi:10.5281/zenodo.24596332](https://doi.org/10.5281/zenodo.24596332). Human-directed research produced with the help of AI tools (Claude). Additional verification may still be required. This note has not been refereed. **Expert verification required.** Verified so far with two independent exact computations (python-flint and Node.js BigInt) and Lean 4 + Mathlib (the two congruences, for the truncated products).*

> **In one line:** Banerjee and Smoot conjectured two infinite families of congruences modulo powers of 11. As stated, both fail at level $`\alpha=3`$: for $a=36$ in part (1) and $a=40$ in part (2), the coefficient of $`q^{54}`$ is divisible by 11 but not by 121, while the conjecture requires 121.

## Summary

**Theorem.** Let $`(q;q)_\infty=\prod_{k\ge 1}(1-q^k)`$ and $`(-q;q)_\infty=\prod_{k\ge 1}(1+q^k)`$ (the $q$-Pochhammer symbols), and define integers $`p^{[1]}_a(m)`$, $`p^{[2]}_a(m)`$ by

```math
\sum_{m\ge 0}p^{[1]}_a(m)q^m=\frac{(-q;q)_\infty^{a}}{(q;q)_\infty},\qquad
\sum_{m\ge 0}p^{[2]}_a(m)q^m=\frac{(-q;q)_\infty^{a}}{(q;q)_\infty^{5}} .
```

Then

```math
p^{[1]}_{36}(54)=62043410886974649205238011198\equiv 33 \pmod{121},
```

```math
p^{[2]}_{40}(54)=66134580699742235651549220246110\equiv 55 \pmod{121}.
```

Here $`36\equiv 3`$ and $`40\equiv 7 \pmod{11}`$, and $`24\cdot 54\equiv 1-36\equiv 5-40 \pmod{11^3}`$. So both values are instances of Conjecture 6.1 of K. Banerjee and N. A. Smoot, *On a problem of Gordon and Hughes: the 11-adic properties of meromorphic modular functions on $`X_0(22)`$*, [arXiv:2611.09681v1](https://arxiv.org/abs/2611.09681v1) (2026-11-06), with $`\alpha=3`$ and $n=0$. The conjecture asserts that both are $`\equiv 0 \pmod{11^{\lceil 3/2\rceil}}`$, that is, modulo 121. **So both parts of the conjecture, as stated, fail at $`\alpha=3`$.** Both values have 11-adic valuation exactly 1, so the instances with $`\alpha=1`$ and $`\alpha=2`$ at this index hold.

The conjecture in full, with every symbol defined, is in [`PROOF.md`](PROOF.md) §1–2.

**Credits.**
- Conjecture 6.1 is due to **Koustav Banerjee and Nicolas Allen Smoot** ([arXiv:2611.09681v1](https://arxiv.org/abs/2611.09681v1)). They proved the case $a=2$ of part (2) (their Theorem 1.1). Nothing here concerns that case.
- The question of a congruence family on a curve of genus 2 goes back to **B. Gordon and K. Hughes** (*Ramanujan congruences for q(n)*, Lecture Notes in Math. 899, 1981, [doi:10.1007/BFb0096473](https://doi.org/10.1007/BFb0096473)), as described by Banerjee and Smoot.
- Related work on congruences modulo powers of 11: Gordon ([Glasgow Math. J. 24 (1983)](https://www.cambridge.org/core/journals/glasgow-mathematical-journal/article/ramanujan-congruences-for-pk-mod-11/25B481EC52D78BF72E4FAF7DCC110E64)) and Shashika Petta Mestrige ([arXiv:1906.00428](https://arxiv.org/abs/1906.00428)).
- A priority search on 2026-11-27 (14:24–15:19 UTC) found no report, correction or claim of this failure; the source is at version 1 only ([`LITERATURE_CHECK.md`](LITERATURE_CHECK.md)). This describes our search only. It is not a priority claim. The authors may well correct the statement themselves.

**Method.**
1. Check the hypotheses and compute the shift $`\delta=54`$ by hand. The same arithmetic is checked in Lean.
2. Prove by hand that the coefficient of $`q^{54}`$ of each infinite product equals that of the product over $`k\le 54`$ (a truncation lemma).
3. Compute the two coefficients exactly with two independent programs: Python with python-flint (products and exact series division) and Node.js BigInt (a divisor-sum recurrence for the infinite products). A third script checks that their results are identical.
4. Check the coefficients of the truncated products, and their residues modulo 121, in the Lean 4 kernel.
5. Combine: the conjecture asserts divisibility by 121, and the residues are 33 and 55.

**Side facts.**
- *Other shifts.* The congruence for $`\delta`$ fixes it only modulo 1331. Every solution $`\delta\le 54`$ has 54 in its progression. For the next three solutions, $`\delta=1385`$, $2716$ and $4047$, the $n=0$ coefficient is also nonzero modulo 121 (residues 11, 11, 11 in part (1); 55, 66, 99 in part (2)). Larger solutions were not computed.
- *Small $a$.* For every allowed $a$ with $`\lvert a\rvert\le 33`$, the conjecture holds at levels $`\alpha\le 4`$ for all indices below 300000 (numerical). This is why small checks do not see the failure.
- *Many failures.* Over $`a\in[-1400,1400]`$, level 3 fails for 391 of the 763 allowed $a$ in part (1) and 224 of the 2037 in part (2) (numerical).
- *A pattern.* Whether level 3 holds is predicted well by a simple "carry" condition on the shifts. It suggests a corrected statement, which we record as a heuristic only (see "What the data suggest" below).

**Verification.**
- **Certificates:** two independent exact programs agree on every value, in a clean rerun on 2026-11-27 ([`cert/NTA-1/`](cert/NTA-1/)).
- **Lean 4:** the coefficients of the truncated products, their residues modulo 121, and the arithmetic side conditions are checked by the Lean kernel, with standard axioms only and no `sorry` ([`LEAN.md`](LEAN.md)). **Not formalized:** the truncation lemma (passing from the infinite products to the truncations), and the statement of the conjecture itself.
- **Reviews:** this note has not been refereed ([`REVIEWS.md`](REVIEWS.md)).
- **Expert verification required.** Verified so far with two independent exact computations (python-flint and Node.js BigInt) and Lean 4 + Mathlib (the two congruences, for the truncated products)

**How it was made.** Human-directed research produced with the help of AI tools (Claude). Every number here comes from an archived program output. The process is logged under "Research log" below.

### Status of the claims

| Claim | Status | Evidence |
| --- | --- | --- |
| Banerjee–Smoot Conj. 6.1 (arXiv:2611.09681v1 §6) fails in both parts at α = 3: p^{[1]}_{36}(54) = 62043410886974649205238011198 ≡ 33 (mod 121) (a = 36 ≡ 3 mod 11, 24·54 ≡ 1−36 mod 1331) and p^{[2]}_{40}(54) = 66134580699742235651549220246110 ≡ 55 (mod 121) (a = 40 ≡ 7 mod 11, 24·54 ≡ 5−40 mod 1331); conjecture requires ≡ 0 mod 121 | certified (flint fmpz_series primary and Node BigInt divisor-sum cross-check agree, clean checkout of dd8b84c); formalized for the truncated products F₅₄, E₅₄ in ℤ⟦X⟧ (lean_check PASS; the truncation of the infinite products is not formalized) | [`cert/NTA-1/out/NTA-1.out`](cert/NTA-1/out/NTA-1.out), [`NTA-1_x.out`](cert/NTA-1/out/NTA-1_x.out), [`compare.out`](cert/NTA-1/out/compare.out), [`lean_check.out`](cert/NTA-1/out/lean_check.out); [`lean/Pipeline/BanerjeeSmoot/Main.lean`](lean/Pipeline/BanerjeeSmoot/Main.lean) |
| Carry rule: among allowed a in [−1400,1400], a carry at α = 3 always gives the mod-121 congruence (304/304 part 1, 1789/1789 part 2); conjecture holds for all allowed abs(a) ≤ 33, α ≤ 4 | numerical | [`scripts/out/scan_a.log`](scripts/out/scan_a.log); the abs(a) ≤ 33 part is in [`scripts/out/rows.log`](scripts/out/rows.log) |

The archived runs were made on a clean clone of the author's working repository at commit `dd8b84c`, which is not part of this repository; the script hashes recorded in the output headers match the files here. The Zenodo PDF (version 1) links to the repository under its earlier name, `nebulousice/number-theory-2611a`, which redirects here; otherwise it is identical to the paper in this repository.

## Where to start

| If you want… | Read |
| --- | --- |
| The proof, step by step, with status words | [`PROOF.md`](PROOF.md) |
| A short paper | [`paper.pdf`](paper.pdf), source [`paper.tex`](paper.tex) (amsart) |
| To rerun the certificates | `pip install python-flint==0.7.1`, then `bash cert/NTA-1/run_all.sh 3` (needs Node.js 18 or later); see [`REPRODUCE.md`](REPRODUCE.md) |
| What Lean checks, and what it does not | [`LEAN.md`](LEAN.md) |
| The priority search | [`LITERATURE_CHECK.md`](LITERATURE_CHECK.md) |
| The review status | [`REVIEWS.md`](REVIEWS.md) |

---

## Research log

### Setup

Banerjee and Smoot prove an infinite family of congruences modulo powers of 11 for the case $a=2$ of part (2) below (their Theorem 1.1). They describe it as the first explicit congruence family associated with the modular curve $`X_0(22)`$, which has genus 2. In §6 of their paper they conjecture two families of the same shape, one for each of the series above, for every $a$ in certain residue classes modulo 11.

The conjecture (restated in our notation; symbols defined in [`PROOF.md`](PROOF.md) §1):

> Let $`\alpha\in\mathbb{N}`$ and $`n\in\mathbb{N}_0`$.
> (1) If $`a\equiv 3,5,7\pmod{11}`$, then $`p^{[1]}_a\left(11^{\alpha}n+\delta^{[1]}_{a,\alpha}\right)\equiv 0 \pmod{11^{\lceil\alpha/2\rceil}}`$, where $`24\delta^{[1]}_{a,\alpha}\equiv 1-a \pmod{11^{\alpha}}`$.
> (2) If $`a\not\equiv 1,3,5\pmod{11}`$, then $`p^{[2]}_a\left(11^{\alpha}n+\delta^{[2]}_{a,\alpha}\right)\equiv 0 \pmod{11^{\lceil\alpha/2\rceil}}`$, where $`24\delta^{[2]}_{a,\alpha}\equiv 5-a \pmod{11^{\alpha}}`$.

In words: fix $a$ in an allowed class and a level $`\alpha\ge 1`$. Let $`\delta`$ solve $`24\delta\equiv 1-a`$ (part 1) or $5-a$ (part 2) modulo $`11^\alpha`$. Then every coefficient at an index $`11^\alpha n+\delta`$, $`n\ge 0`$, should be divisible by $`11^{\lceil\alpha/2\rceil}`$.

### Notation

We write $c=1$ for part (1) and $c=5$ for part (2), so the series is $`(-q;q)_\infty^a/(q;q)_\infty^c`$ and the shift solves $`24\delta\equiv c-a \pmod{11^\alpha}`$. We call $a$ *allowed* if it lies in the classes of its part. For $`\alpha\ge 1`$:

```math
\delta_\alpha(a)=\text{least } \delta\ge 0 \text{ with } 24\delta\equiv c-a \pmod{11^\alpha},\qquad
\rho_\alpha=\text{least } \rho\ge 0 \text{ with } 8\rho\equiv c \pmod{11^\alpha}.
```

We say $a$ has a *carry at level* $`\alpha`$ when $`\delta_\alpha(a)>\rho_\alpha`$. Equivalently, $`\delta_\alpha(a)+\delta_\alpha(-a-c)\ge 11^\alpha`$; the two shifts always add up to $`\rho_\alpha`$ modulo $`11^\alpha`$, and a carry means the sum overflows. For $c=1$, $`\rho_1=7`$ and $`\rho_3=832`$; for $c=5$, $`\rho_1=2`$ and $`\rho_3=167`$. For $a=36$ ($c=1$) and $a=40$ ($c=5$): $`\delta_1=10`$ and $`\delta_3=54`$, so there is a carry at level 1 and none at level 3.

Finally, $`\kappa_\alpha(a)`$ is the number of odd levels $`\alpha'\le\alpha`$ at which $a$ has a carry.

### Results along the way

| # | Statement | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Our conventions reproduce the source: its Theorem 1.1 ($a=2$, part (2)) holds for $`\alpha\le 5`$ on all indices below 300000, with the stated exponents attained | numerical | [`scripts/out/rows.log`](scripts/out/rows.log) |
| 2 | For every allowed $a$ with $`\lvert a\rvert\le 33`$ (both parts), levels $`\alpha\le 4`$ hold for all indices below 300000 | numerical | [`scripts/out/rows.log`](scripts/out/rows.log) |
| 3 | For every allowed $`a\in[-1400,1400]`$, levels $`\alpha\le 2`$ hold for all indices below 30000 | numerical | [`scripts/out/scan_a.log`](scripts/out/scan_a.log) |
| 4 | Level 3 fails for 391 of 763 allowed $a$ (part 1) and 224 of 2037 (part 2) in $[-1400,1400]$; smallest $`\lvert a\rvert`$: 36, −37, 47, −48, … (part 1) and 40, −45, 51, −56, … (part 2) | numerical | [`scripts/out/scan_a.log`](scripts/out/scan_a.log) |
| 5 | $36$ and $40$ are allowed; the shift at $`\alpha=3`$ is $54$ for both; the modulus is $121$ | formalized (arithmetic) | `side_conditions` in [`Main.lean`](lean/Pipeline/BanerjeeSmoot/Main.lean) |
| 6 | Truncation lemma: the coefficient of $q^m$ depends only on the factors with $`k\le m`$ | hand proof (not refereed; not formalized) | [`PROOF.md`](PROOF.md) Step 2 |
| 7 | $`p^{[1]}_{36}(54)=62043410886974649205238011198\equiv 33 \pmod{121}`$ | certified; formalized for the truncated products | [`cert/NTA-1/out/`](cert/NTA-1/out/), `part1_coeff` |
| 8 | $`p^{[2]}_{40}(54)=66134580699742235651549220246110\equiv 55 \pmod{121}`$ | certified; formalized for the truncated products | [`cert/NTA-1/out/`](cert/NTA-1/out/), `part2_coeff` |
| 9 | **Conjecture 6.1 fails in both parts at $`\alpha=3`$, $n=0$** | **certified** | [`PROOF.md`](PROOF.md), [`cert/NTA-1/`](cert/NTA-1/) |
| 10 | The coefficients at $54+1331t$, $t=1,2,3$, are nonzero modulo 121 in both parts, with $`v_{11}=1`$ | certified | [`cert/NTA-1/out/compare.out`](cert/NTA-1/out/compare.out) |
| 11 | At level 1, the residues of $a$ modulo 11 with a carry are exactly the allowed classes, in both parts | numerical | [`scripts/out/scan_a.log`](scripts/out/scan_a.log) |
| 12 | Every allowed $`a\in[-1400,1400]`$ with a carry at level 3 satisfies level 3 on indices below 30000 (304 of 304 in part 1; 1789 of 1789 in part 2); without a carry, level 3 fails for 391 of 459 (part 1) and 224 of 248 (part 2) | numerical | [`scripts/out/scan_a.log`](scripts/out/scan_a.log) |
| 13 | Corrected statement: $`p_a(11^\alpha n+\delta_\alpha(a))\equiv 0 \pmod{11^{\kappa_\alpha(a)}}`$ for allowed $a$, $`\alpha\le 3`$, all $n$ | heuristic | rows 3, 11–12 |

### What the data suggest (numerical and heuristic only)

Nothing in this section is proved. It is not used in the proof of the theorem.

**Observations** (rows 2–4, 11, 12 above). The conjecture agrees with all our data for $`\lvert a\rvert\le 33`$. Level 3 fails for many allowed $a$ with $`\lvert a\rvert>33`$ (row 4). At level 1, "carry" is exactly the source's residue condition. At level 3, a carry at level 3 was always enough for the congruence in our range, and its absence usually, but not always, led to failure.

**Heuristic (a possible corrected statement).** For every allowed integer $a$, every level $`\alpha\in\lbrace 1,2,3\rbrace`$ and every $`n\ge 0`$,

```math
p_a\left(11^{\alpha}n+\delta_\alpha(a)\right)\equiv 0 \pmod{11^{\kappa_\alpha(a)}},
```

where $`p_a=p^{[1]}_a`$ for $c=1$ and $`p_a=p^{[2]}_a`$ for $c=5$.

- The number of odd levels up to $`\alpha`$ is $`\lceil\alpha/2\rceil`$. So this agrees with the exponent of Conjecture 6.1 exactly when $a$ has a carry at every odd level up to $`\alpha`$.
- For $a=2$, $c=5$ (the proved Theorem 1.1): for odd $`\alpha`$, $`\delta_\alpha(2)=(5\cdot 11^\alpha+1)/8`$ and $`\rho_\alpha=(11^\alpha+5)/8`$, so every odd level has a carry, in agreement with that theorem.
- The heuristic is a lower bound for the exponent, not a characterization: some allowed $a$ without a carry at level 3 still satisfy level 3 (row 12).
- It is stated only for allowed $a$ and $`\alpha\le 3`$, because that is what the evidence covers (rows 3, 11 and 12: $`\lvert a\rvert\le 1400`$, indices below 30000). Whether the same rule holds for all $a$ and all $`\alpha`$ has not been tested. It is unproved.

### Timeline (all 2026-11-27)

1. The conjecture was found on the arXiv math.NT listing. A first priority search found it open, with the case $a=2$ of part (2) proved in the source.
2. Exploration reproduced the source's values, confirmed the conjecture for $`\lvert a\rvert\le 33`$, and found the failures at $a=36$ and $a=40$ by scanning larger $`\lvert a\rvert`$.
3. Certification: two independent exact programs, run in a clean checkout, agree on both counterexamples and on the extra shifts.
4. Formal check: the Lean 4 kernel verifies the coefficients of the truncated products.
5. A second priority search, for the failure itself (14:24–15:19 UTC), found no report, correction or claim.
6. This write-up.

## Files

| Path | Contents |
| --- | --- |
| [`PROOF.md`](PROOF.md) | The complete proof, every step with its status word |
| [`paper.tex`](paper.tex) | The same result as a short amsart paper |
| [`cert/NTA-1/`](cert/NTA-1/) | Certificates: primary program `NTA-1.py`, cross-check `NTA-1_x.mjs`, `compare.py`, `run_all.sh`, the Lean data generator `gen_lean_stages.py`, a certification report `README.md`, and archived outputs in `out/` |
| [`lean/`](lean/) | Lean 4 files (`Pipeline/BanerjeeSmoot/Main.lean`, `Stages.lean`), archived build and axiom logs, project files, and a root module for a standalone build |
| [`scripts/`](scripts/) | Exploratory programs and their logs (`rows.py`, `scan_a.py`, `counterexample.py`, `witness_naive.py`, `alpha5.py`, shared `bs_common.py`), and `lean_check.sh` |
| [`LITERATURE_CHECK.md`](LITERATURE_CHECK.md) | Priority searches and related work |
| [`REVIEWS.md`](REVIEWS.md) | Review history and known weak points |
| [`LEAN.md`](LEAN.md) | What is formalized, and what is not |
| [`REPRODUCE.md`](REPRODUCE.md) | Commands, versions, runtimes, expected output |

File names under `cert/` and the Lean theorem name `BanerjeeSmoot.NTA1` keep their original names so that the archived hashes and logs still match.

## Acknowledgements

- The conjecture, and the proof of its case $a=2$ of part (2): Koustav Banerjee and Nicolas Allen Smoot.
- The original question of a genus-2 congruence family: B. Gordon and K. Hughes.
- Human-directed research produced with the help of AI tools (Claude). Additional verification may still be required.
