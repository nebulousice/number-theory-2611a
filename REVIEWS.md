# Review history

*Updated 2026-11-27.*

## Current status

- **No independent referee review has been run.** The planned process has two AI referees, on different models, review the full package blind. If they do not both accept with zero issues, the issues are fixed and three referees (the two plus a third, on a third model) review the fixed version; at least two of the three must accept with zero issues, and any major issue blocks. None of this has started for this result.
- **Expert verification required.** Verified so far with two independent exact computations (python-flint and Node.js BigInt) and Lean 4 + Mathlib (the two congruences, for the truncated products)
- The credit lines in [`README.md`](README.md) and [`paper.tex`](paper.tex) are drafts. They have not yet been approved by the repository owner.

## Checks made so far (these are not referee reviews)

| Date | Check | By | Outcome |
| --- | --- | --- | --- |
| 2026-11-27 | Priority search: is Conjecture 6.1 open? | an AI agent (priority gate) | Open; only $a=2$ of part (2) proved (the source's Theorem 1.1); $a=0,-5$ possibly covered by older work ([`LITERATURE_CHECK.md`](LITERATURE_CHECK.md)) |
| 2026-11-27 | Exploration: reproduce the source's values, scan in $a$ | an AI agent (strategy stage) | Source values reproduced; conjecture holds for allowed $\lvert a\rvert\le 33$, $\alpha\le 4$; failures found at $a=36$ (part 1) and $a=40$ (part 2), $\alpha=3$ ([`scripts/out/`](scripts/out/)) |
| 2026-11-27 | Certification: two independent exact programs, clean checkout; convention audit (quantifiers, choice of $\delta$, ceiling versus floor, residue classes) | an AI agent (certification stage) | Both programs agree on all eight values; no reading of the statement found that rescues it, except a floor reading of the modulus, which contradicts the printed statement ([`cert/NTA-1/README.md`](cert/NTA-1/README.md)) |
| 2026-11-27 | Lean 4 check of the truncated products | an AI agent (certification stage) | `PASS`, standard axioms only; the truncation step is not formalized ([`LEAN.md`](LEAN.md)) |
| 2026-11-27 | Priority search for the failure itself | an AI agent (priority gate) | No report, correction or claim found ([`LITERATURE_CHECK.md`](LITERATURE_CHECK.md)) |
| 2026-11-27 | Write-up, with spot reruns | an AI agent (writing stage) | The cross-check `node NTA-1_x.mjs 3` was rerun (1.1 s) and its output body is identical to the archived one; `scripts/witness_naive.py` and `cert/NTA-1/gen_lean_stages.py` reproduce their archived output exactly. Static checks of `paper.tex` only: no TeX engine was available, so the paper has not been compiled |

## Known weak points a referee should look at

1. **The truncation lemma** ([`PROOF.md`](PROOF.md) Step 2) is a hand argument and is not formalized. It is standard and short, but it is the only link between the Lean theorems and the infinite products. The two certificate programs do not depend on it in the same way: the cross-check works with the infinite products directly, through a recurrence; the primary program truncates at $k\le 4047$, which needs the same lemma.
2. **The reading of the statement.** The counterexamples need the modulus $11^{\lceil\alpha/2\rceil}$ with a ceiling. A floor would give modulus 11 at $\alpha=3$, and both values would then satisfy it. The ceiling was read from the PDF glyphs and the HTML, and it is the reading that matches the source's own Theorem 1.1. A referee should confirm this against the PDF.
3. **The choice of $\delta$.** The congruence fixes $\delta$ only modulo 1331. Choices $\delta\le 54$ are covered by the index 54 itself, and $\delta=1385, 2716, 4047$ were computed. Larger choices were not computed; under such a choice the $n=0$ instance is a different coefficient.
4. **Independence of the two programs.** They share no code and use different languages, algorithms and ways of computing $\delta$. Both were written within the same automated pipeline, so the independence is one of method, not of authorship.
5. **The numerical observations and the heuristic** in [`README.md`](README.md) come from one program each (computing modulo $11^4$ or $11^6$) and have not been reproduced independently. They are not used in the proof.
