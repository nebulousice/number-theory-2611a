# Lean 4: what is formalized, and what is not

*2026-11-27. Toolchain `leanprover/lean4:v4.37.0-rc1` with Mathlib (commit `8ec7bd8e5f837ab7e335374928e18341c4e9f385`, pinned in [`lean/lake-manifest.json`](lean/lake-manifest.json)). **Expert verification required.** Verified so far with two independent exact computations (python-flint and Node.js BigInt) and Lean 4 + Mathlib (the two congruences, for the truncated products).*

## Summary

| Statement | Lean status | Where |
| --- | --- | --- |
| In $\mathbb{Z}[[X]]$, with $F_{54}=\prod_{k=1}^{54}(1+X^k)$ and $E_{54}=\prod_{k=1}^{54}(1-X^k)$: the coefficient of $X^{54}$ in $F_{54}^{36}G$, for any $G$ with $GE_{54}=1$, is $62043410886974649205238011198$ | **formalized** | `BanerjeeSmoot.part1_coeff` |
| Same, for $F_{54}^{40}G$ with $GE_{54}^5=1$: the coefficient is $66134580699742235651549220246110$ | **formalized** | `BanerjeeSmoot.part2_coeff` |
| Such inverses $G$ exist; the two coefficients are $\equiv 33$ and $\equiv 55 \pmod{121}$, and neither is divisible by 121 | **formalized** | `BanerjeeSmoot.NTA1` |
| $36\bmod 11=3$; $1331$ divides $24\cdot 54-(1-36)$; $40\bmod 11=7$; $1331$ divides $24\cdot 54-(5-40)$; $0\le 54<1331$; $(3+1)/2=2$ in integer division, which is $\lceil 3/2\rceil$ | **formalized** | `BanerjeeSmoot.side_conditions` |
| Truncation: the coefficient of $q^{54}$ of $(-q;q)_\infty^{a}(q;q)_\infty^{-b}$ equals that of $F_{54}^{a}E_{54}^{-b}$ | **not formalized** (hand proof, [`PROOF.md`](PROOF.md) Step 2) | — |
| The statement of Conjecture 6.1 and its negation | **not formalized**; the link is the hand argument of [`PROOF.md`](PROOF.md) Steps 1, 2 and 5 | — |
| The numerical observations and the heuristic in [`README.md`](README.md) | not formalized | [`scripts/`](scripts/) |

## Why the truncation is not formalized

Mathlib has no infinite $q$-Pochhammer product $(q;q)_\infty$. Defining it as a limit in $\mathbb{Z}[[X]]$ and proving that factors with $k\ge 55$ do not change the coefficients of $X^0,\dots,X^{54}$ is routine but was not done. The hand proof is three short paragraphs: factors with $k>54$ are $\equiv 1$ modulo $X^{55}$, and reduction modulo $X^{55}$ is a ring homomorphism.

## Files

| File | Content |
| --- | --- |
| [`lean/Pipeline/BanerjeeSmoot/Main.lean`](lean/Pipeline/BanerjeeSmoot/Main.lean) (315 lines) | Definitions, the link between lists and power series, and all theorems. Imports `Stages.lean` and the Mathlib modules `RingTheory.PowerSeries.Inverse`, `Tactic.Ring` and `Tactic.Linarith`. |
| [`lean/Pipeline/BanerjeeSmoot/Stages.lean`](lean/Pipeline/BanerjeeSmoot/Stages.lean) (106 lines) | Generated literal lists: the coefficient lists after each multiplication stage. Written by [`cert/NTA-1/gen_lean_stages.py`](cert/NTA-1/gen_lean_stages.py). **Untrusted:** every step is re-checked by the kernel in `Main.lean`, so an error here can only make the build fail. |
| [`lean/Pipeline.lean`](lean/Pipeline.lean) | Root module for a standalone build of this repository. It imports only `Pipeline.BanerjeeSmoot.Main`. It is the only Lean file written for this repository; it contains no proofs. |
| `lean/lean-toolchain`, `lean/lakefile.toml`, `lean/lake-manifest.json` | Unmodified copies from the shared Lean project in which the check ran. |
| [`lean/Pipeline/BanerjeeSmoot/build.log`](lean/Pipeline/BanerjeeSmoot/build.log), [`axioms.log`](lean/Pipeline/BanerjeeSmoot/axioms.log) | Archived logs of the original check. The build log also lists warnings from unrelated files of the shared project. |
| [`cert/NTA-1/out/lean_check.out`](cert/NTA-1/out/lean_check.out) | The original check's console record: build result, `sorry` scan, axiom report, `PASS` line and timing. |

SHA-256 of the checked files (identical to the files in the shared project at the time of the check):

```
6b6c72137b9f35bf5eb6dfc0bee2c0b9791ad1beb4ff69bb4d3e0fd1ea7cd4e3  lean/Pipeline/BanerjeeSmoot/Main.lean
d2ae62411347fb05d58e2928586715eb8c42c5a7b5fd46f932a99c26329d18d7  lean/Pipeline/BanerjeeSmoot/Stages.lean
```

## How the proof works

1. **Lists.** A truncated series is a list of 55 natural numbers (the coefficients of $X^0,\dots,X^{54}$). `mulOnePlus m` multiplies such a list by $1+X^m$, keeping the length.
2. **Link to power series.** `Rep s f` says that the list `s` gives the first coefficients of `f`. `transport_mulOnePlus` proves that `mulOnePlus m` realises multiplication by $1+X^m$ on these truncations; `transport_iterRange` and `transport_iterPow` extend this to products and powers.
3. **The inverse of $E_{54}$.** $H_{54}=\prod_{k=1}^{54}\prod_{j=0}^{5}(1+X^{k2^j})$. The telescoping identity $(1-X^k)\prod_{j=0}^{5}(1+X^{k2^j})=1-X^{64k}$ (`telescope`) gives $X^{55}\mid 1-H_{54}E_{54}$ (`X55_dvd_HE`). `coeff_eq_of_inv` then shows that for any $G$ with $GE_{54}=1$, $A\cdot G$ and $A\cdot H_{54}$ have the same coefficient of $X^{54}$. For $E_{54}^5$ the same works with $H_{54}^5$ (`dvd_one_sub_pow`).
4. **Kernel computation.** `list1` and `list2` are the coefficient lists of $F_{54}^{36}H_{54}$ and $F_{54}^{40}H_{54}^5$. The kernel checks each stage against the literal lists of `Stages.lean` (`chainF36_ok`, `chainH1_ok`, `chainF40_ok`, `chainH5_ok`, by `decide +kernel`), and then reads off entry 54 (`list1_54`, `list2_54`). No `native_decide` is used, so compiled code is not trusted.
5. **Main theorems.** `part1_coeff` and `part2_coeff` combine steps 2–4. `NTA1` adds the existence of the inverses (from `E54_isUnit`) and the residues modulo 121, again by `decide +kernel`.

## The check

The check was run on 2026-11-27 with `bash scripts/lean_check.sh BanerjeeSmoot` in the shared project. It requires: `lake build` succeeds; no `sorry` or `admit` in the target's files; every `#print axioms` line reports only `propext`, `Classical.choice` and `Quot.sound`. Archived result ([`cert/NTA-1/out/lean_check.out`](cert/NTA-1/out/lean_check.out)):

```
Build completed successfully (6991 jobs).
== sorry / admit scan
== axioms
'BanerjeeSmoot.NTA1' depends on axioms: [propext, Classical.choice, Quot.sound]
'BanerjeeSmoot.side_conditions' depends on axioms: [propext]
PASS lean_check BanerjeeSmoot (Lean (version 4.37.0-rc1, x86_64-w64-windows-gnu, commit 0b77e12952ad39077d80d8bd6b66d601f225c321, Release))

real	24m48.264s
```

The 6991 jobs and the 24 min 48 s include the rest of the shared project; the build log shows `Built Pipeline.BanerjeeSmoot.Stages (15s)` and `Built Pipeline.BanerjeeSmoot.Main (662s)`. The only warnings for the Banerjee–Smoot files are of one kind: they import Mathlib modules "designed for use with the module system". These do not affect the result. Other warnings in the log (for example unused `simp` arguments) concern unrelated files of the shared project.

## Standalone build: not yet run

This repository's `lean/` folder is set up to build on its own (root module [`lean/Pipeline.lean`](lean/Pipeline.lean), unmodified project files). That standalone build has **not** been run: it needs the prebuilt Mathlib cache, a large download. The commands are in [`REPRODUCE.md`](REPRODUCE.md) §3. Until someone runs it, the evidence for the Lean claims is the archived check in the shared project.
