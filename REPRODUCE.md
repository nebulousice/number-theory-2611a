# How to reproduce

All commands are run from the root of this repository unless a `cd` is shown. The archived outputs were produced on 2026-11-27 on Windows 11 (10.0.26200), under Git Bash (MINGW64). Runtimes are wall-clock times on a shared, heavily loaded machine; expect them to be shorter elsewhere.

Paths written inside the copied files (for example `targets/number-theory-2611a/...` in `cert/NTA-1/README.md`, or the `cwd` lines in the output headers) refer to the private working repository in which they were made. In this repository the same files are under `cert/`, `scripts/` and `lean/`.

## Versions

| Tool | Version used | Needed for |
| --- | --- | --- |
| Python | 3.12.10 | `cert/NTA-1/NTA-1.py`, `compare.py`, everything in `scripts/` |
| python-flint | 0.7.1 (`pip install python-flint==0.7.1`) | `cert/NTA-1/NTA-1.py`, `scripts/` (not `witness_naive.py`) |
| Node.js | v24.20.0 (any version 18 or later should do) | `cert/NTA-1/NTA-1_x.mjs` (BigInt, no packages) |
| bash, git, sha256sum | any | `cert/NTA-1/run_all.sh` (writes the archived headers) |
| Lean 4 (through `elan`) | `leanprover/lean4:v4.37.0-rc1` (from `lean/lean-toolchain`) | `lean/` |
| Mathlib | `8ec7bd8e5f837ab7e335374928e18341c4e9f385` (pinned in `lean/lake-manifest.json`) | `lean/` |

`paper.pdf` (12 pages, revised 2026-11-28 to credit the earlier reports) was compiled from `paper.tex` with Tectonic (`tectonic -X compile paper.tex`): no errors and no undefined references or citations. Any TeX Live or MiKTeX with `amsart`, `amssymb`, `booktabs`, `url` and `hyperref` also works (`latexmk -pdf paper.tex`).

## 1. The certificates (the main result)

The two programs share no code, and both use exact integer arithmetic only.

```
cd cert/NTA-1
python NTA-1.py 3        # primary: python-flint exact series        (91.96 s)
node NTA-1_x.mjs 3       # cross-check: Node BigInt recurrence       (16.96 s)
```

The argument `3` asks for the three extra shifts $m=1385, 2716, 4047$ besides $m=54$.

Expected last line of `python NTA-1.py 3` (archived in [`cert/NTA-1/out/NTA-1.out`](cert/NTA-1/out/NTA-1.out)):
```
PASS NTA-1 primary (flint fmpz_series)
```

Expected last line of `node NTA-1_x.mjs 3` (archived in [`cert/NTA-1/out/NTA-1_x.out`](cert/NTA-1/out/NTA-1_x.out)):
```
PASS NTA-1 cross-check (Node BigInt, divisor-sum recurrence)
```

Other lines to compare, in both outputs:
```
  p^[1]_36(54) = 62043410886974649205238011198
     mod 121 = 33, mod 11 = 0, v_11 = 1
  p^[2]_40(54) = 66134580699742235651549220246110
     mod 121 = 55, mod 11 = 0, v_11 = 1
```

Each program exits with a non-zero status, and prints `FAIL` instead of `PASS`, if any check fails. In a spot rerun during the write-up (2026-11-27, unloaded machine), `node NTA-1_x.mjs 3` took 1.1 s and printed exactly the archived body.

**With the archived headers and the comparison.** Inside a git clone of this repository:

```
cp -r cert/NTA-1/out /tmp/archived_out          # keep the archived outputs
bash cert/NTA-1/run_all.sh 3                    # rewrites cert/NTA-1/out/*.out with fresh headers
for f in NTA-1.out NTA-1_x.out compare.out; do
  diff <(sed -n '/^----$/,/^----$/p' /tmp/archived_out/$f) <(sed -n '/^----$/,/^----$/p' cert/NTA-1/out/$f)
done
git checkout -- cert/NTA-1/out                  # restore the archived outputs
```

The `diff` compares only the bodies between the two `----` lines, so dates, wall times and paths in the headers are ignored. It should print nothing. The last line of [`cert/NTA-1/out/compare.out`](cert/NTA-1/out/compare.out) is:
```
PASS NTA-1 compare (primary and cross-check identical)
```

The script hashes recorded in the archived headers are those of the files here:
```
b952aa8efd905795b5d2110a9258b7d7c73fcd5de47d7d4015a20e0035a6a47f  NTA-1.py
6b1d05f58c8f6ca252ed349b3a8141ec37620c4ee28d690aedf9b7e4e5b98c65  NTA-1_x.mjs
b6e1af1c87abc989508f5389944d258482d95e2579211e3be983022ee75c2839  compare.py
4fb43e29594baec354ebdb5db7bafc975b729b36e9c728fbafb080a511cbf3e8  run_all.sh
```

## 2. The exploratory scripts (numerical evidence)

These are not certificates. They found the counterexamples first and produced the numerical observations in [`README.md`](README.md). Their logs have no version header; they were run with Python 3.12.10 and python-flint 0.7.1. Write to new file names so that the archived logs are kept, then compare.

```
cd scripts
python rows.py 300000                    > rerun_rows.log            # source values; |a| <= 33, alpha <= 4   (233 s)
python scan_a.py 30000 -1400 1400 rerun_scan.json > rerun_scan_a.log # scan in a, carry rule              (413 s)
python counterexample.py 1 36 3 2800     > rerun_cx1.log             # part (1) witness, two methods
python counterexample.py 5 40 3 2800     > rerun_cx2.log             # part (2) witness, two methods
python witness_naive.py                  > rerun_naive.log           # products straight from the definition
python alpha5.py 5 500000 3              > rerun_alpha5.log          # level 5 test (not used in any claim here; about 90 s)
```

The runtime of `counterexample.py` was not recorded. `witness_naive.py` took about 2 s in a spot rerun during the write-up, and its output was identical to the archived log. Lines that print elapsed time will differ.

Expected lines (archived logs in [`scripts/out/`](scripts/out/)):

- `rows.py` ([`rows.log`](scripts/out/rows.log)):
  ```
  [MATCH] B   every allowed a with |a| <= 33 satisfies the conjecture for alpha <= 4 in range failures: []
  ALL SOURCE VALUES MATCH: True   (233.0 s)
  ```
- `scan_a.py` ([`scan_a.log`](scripts/out/scan_a.log)), part (1) block:
  ```
    allowed a in range: 763;  alpha<=2 holds for all of them: True
    alpha=3 FAILS (min v_11 = 1 < 2) for 391 allowed a;  smallest |a|: [36, -37, 47, -48, 58, -59, 60, -61, 69, -70]
    (carry(3), alpha=3 holds) counts: {(True, True): 304, (False, False): 391, (False, True): 68}
  ```
  and part (2) block:
  ```
    allowed a in range: 2037;  alpha<=2 holds for all of them: True
    alpha=3 FAILS (min v_11 = 1 < 2) for 224 allowed a;  smallest |a|: [40, -45, 51, -56, 62, 64, -67, -69, 75, -80]
    (carry(3), alpha=3 holds) counts: {(False, False): 224, (True, True): 1789, (False, True): 24}
  ```
  (The order of the entries in the `counts` dictionary may differ.)
- `counterexample.py` ([`counterexample_part1_a36_alpha3.log`](scripts/out/counterexample_part1_a36_alpha3.log), [`counterexample_part2_a40_alpha3.log`](scripts/out/counterexample_part2_a40_alpha3.log)):
  ```
  RESULT: 3 violating value(s) among the first 3;  implementations agree: True
  ```
- `witness_naive.py` ([`witness_naive.log`](scripts/out/witness_naive.log)):
  ```
    p(54) mod 11 = 0,  p(54) mod 121 = 33   (Conjecture 6.1 requires 0 mod 121)
    p(54) mod 11 = 0,  p(54) mod 121 = 55   (Conjecture 6.1 requires 0 mod 121)
  ```

## 3. Lean 4

The archived check ran in the shared project of the private working repository ([`LEAN.md`](LEAN.md)). To build this repository's `lean/` folder on its own:

```
cd lean
lake exe cache get        # downloads prebuilt Mathlib (several GB; network access)
lake build                # builds Pipeline.lean -> Pipeline.BanerjeeSmoot.Main
lake env lean Pipeline/BanerjeeSmoot/Main.lean     # prints the axiom report
```

Or, from the repository root, `bash scripts/lean_check.sh BanerjeeSmoot`, which runs the build, scans for `sorry`/`admit` and checks the axioms. Note that it **overwrites** the archived logs `lean/Pipeline/BanerjeeSmoot/build.log` and `axioms.log`; restore them afterwards with `git checkout -- lean/Pipeline/BanerjeeSmoot/build.log lean/Pipeline/BanerjeeSmoot/axioms.log`.

Expected output (as archived in [`cert/NTA-1/out/lean_check.out`](cert/NTA-1/out/lean_check.out); the job count will be smaller in a standalone build):
```
Build completed successfully (6991 jobs).
'BanerjeeSmoot.NTA1' depends on axioms: [propext, Classical.choice, Quot.sound]
'BanerjeeSmoot.side_conditions' depends on axioms: [propext]
PASS lean_check BanerjeeSmoot (Lean (version 4.37.0-rc1, x86_64-w64-windows-gnu, commit 0b77e12952ad39077d80d8bd6b66d601f225c321, Release))
```

Runtime of the archived check: 24 min 48 s for the whole shared project; `Main.lean` alone took 662 s to build. **The standalone build has not been run yet.**

To regenerate the untrusted stage data (not needed for checking; the kernel re-checks it):
```
python cert/NTA-1/gen_lean_stages.py /tmp/Stages.lean
diff /tmp/Stages.lean lean/Pipeline/BanerjeeSmoot/Stages.lean
```
