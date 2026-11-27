# Proof: Conjecture 6.1 of Banerjee and Smoot fails at $\alpha=3$

*2026-11-27. Self-contained proof, with a status word on every step. No referee review yet. **Expert verification required.** Verified so far with two independent exact computations (python-flint and Node.js BigInt) and Lean 4 + Mathlib (the two congruences, for the truncated products).*

**Status words.** Each step below carries one of these words.

| Word | Meaning |
| --- | --- |
| formalized | Checked by Lean 4 with Mathlib: the build passes, no `sorry`, standard axioms only |
| certified | Exact integer computation, reproduced by an independent second program, output archived |
| proposed | Written argument, not yet reviewed |
| numerical | Finite computation by one program |
| heuristic | Plausible, no proof |

## 1. Definitions

**Power series.** We work in the ring $\mathbb{Z}[[q]]$ of formal power series in $q$ with integer coefficients. For a series $F$, write $[q^m]F$ for its coefficient of $q^m$. A series with constant term $1$ is a unit of $\mathbb{Z}[[q]]$. So all its integer powers, negative ones included, are again series with integer coefficients.

**$q$-Pochhammer symbols.** The $q$-Pochhammer symbol is $(x;q)_\infty=\prod_{j\ge 0}(1-xq^j)$. We need two cases:

```math
(q;q)_\infty=\prod_{k\ge 1}(1-q^k),\qquad (-q;q)_\infty=\prod_{k\ge 1}(1+q^k).
```

For each $m$, the coefficient of $q^m$ in the partial product over $k\le K$ is the same for every $K\ge m$. By definition, this common value is the coefficient of $q^m$ in the infinite product. Both products have constant term $1$, so both are units.

**The two sequences.** For an integer $a$, the integers $p^{[1]}_a(m)$ and $p^{[2]}_a(m)$, for $m\ge 0$, are defined by

```math
P^{[1]}_a(q):=\frac{(-q;q)_\infty^{a}}{(q;q)_\infty}=\sum_{m\ge 0}p^{[1]}_a(m)q^m,\qquad
P^{[2]}_a(q):=\frac{(-q;q)_\infty^{a}}{(q;q)_\infty^{5}}=\sum_{m\ge 0}p^{[2]}_a(m)q^m .
```

For $m<0$ we set both to $0$. For example, $p^{[1]}_0(m)$ is the number of partitions of $m$.

**Valuation and ceiling.** For a nonzero integer $N$, the $11$-adic valuation $v_{11}(N)$ is the largest $e\ge 0$ with $11^e$ dividing $N$. For a real $x$, $\lceil x\rceil$ is the least integer $\ge x$. $\mathbb{N}=\{1,2,\dots\}$ and $\mathbb{N}_0=\{0,1,2,\dots\}$.

**The shift $\delta$.** Let $\alpha\ge 1$ and let $b$ be an integer. Since $24$ is prime to $11$, the congruence $24\delta\equiv b \pmod{11^\alpha}$ has a unique solution modulo $11^\alpha$. The source takes $b=1-a$ for part (1) and $b=5-a$ for part (2). We take the least non-negative solution unless we say otherwise; §5.2 treats the other solutions.

**Congruence family.** For fixed $a$, the statements below for all levels $\alpha\in\mathbb{N}$ and all $n\in\mathbb{N}_0$ form a congruence family: the coefficients along the progression $11^\alpha n+\delta$ are all divisible by $11^{\lceil\alpha/2\rceil}$.

## 2. The conjecture

K. Banerjee and N. A. Smoot, *On a problem of Gordon and Hughes: the 11-adic properties of meromorphic modular functions on $X_0(22)$*, [arXiv:2611.09681v1](https://arxiv.org/abs/2611.09681v1) (2026-11-06), §6, Conjecture 6.1, verbatim:

> Let $\alpha\in\mathbb{N}$ and $n\in\mathbb{N}_0$.
> (1) If $a\equiv 3,5,7\pmod{11}$, then $p^{[1]}_a\left(11^{\alpha}n+\delta^{[1]}_{a,\alpha}\right)\equiv 0 \pmod{11^{\lceil\alpha/2\rceil}}$, where $24\delta^{[1]}_{a,\alpha}\equiv 1-a \pmod{11^{\alpha}}$.
> (2) If $a\not\equiv 1,3,5\pmod{11}$, then $p^{[2]}_a\left(11^{\alpha}n+\delta^{[2]}_{a,\alpha}\right)\equiv 0 \pmod{11^{\lceil\alpha/2\rceil}}$, where $24\delta^{[2]}_{a,\alpha}\equiv 5-a \pmod{11^{\alpha}}$.

**Reading of the statement.**
- It was copied from version 1, the only version, and checked against both the PDF and the HTML renderings.
- $\alpha=3$ lies in $\mathbb{N}$ under either convention, and $n=0$ lies in $\mathbb{N}_0$.
- The modulus has a ceiling. This agrees with the source's Theorem 1.1, whose exponent is $\lfloor(\alpha+1)/2\rfloor=\lceil\alpha/2\rceil$. Under a floor reading, $11^{\lfloor 3/2\rfloor}=11$, and the two coefficients below would satisfy the congruence. That reading contradicts the printed statement and Theorem 1.1.
- The source calls $P^{[1]}_a$ and $P^{[2]}_a$ eta quotients of level 2 and says that their congruence families live on the modular curve $X_0(22)$. The proof below does not use this; it uses only the definitions of §1.

## 3. The theorem

Put

```math
N_1=62043410886974649205238011198,\qquad N_2=66134580699742235651549220246110.
```

**Theorem.** Let $\alpha=3$ and $n=0$.
1. $a=36$ satisfies $a\equiv 3 \pmod{11}$, and $\delta^{[1]}_{36,3}=54$. Moreover $p^{[1]}_{36}(54)=N_1\equiv 33 \pmod{121}$.
2. $a=40$ satisfies $a\not\equiv 1,3,5 \pmod{11}$, and $\delta^{[2]}_{40,3}=54$. Moreover $p^{[2]}_{40}(54)=N_2\equiv 55 \pmod{121}$.

Since $11^{\lceil 3/2\rceil}=121$, both parts of Conjecture 6.1 are false. Also $v_{11}(N_1)=v_{11}(N_2)=1$.

**Overall status: certified** (two independent exact programs agree); the coefficients of the truncated products are **formalized** in Lean. The truncation step (Step 2) is a hand argument with status **proposed**.

## 4. Proof

The proof checks the hypotheses (Step 1), reduces the coefficients to coefficients of polynomials (Step 2), and computes them (Steps 3 and 4). Steps 3 and 4 are the only computer steps. Step 5 combines the earlier steps. No step uses the conjecture or any consequence of it.

### Step 1. Hypotheses and the shift. Status: formalized

1. $36=3\cdot 11+3$ and $40=3\cdot 11+7$, and $7\notin\{1,3,5\}$. So $36$ is allowed in part (1) and $40$ in part (2).
2. $\lceil 3/2\rceil=2$, so the modulus at $\alpha=3$ is $121$.
3. $24\cdot 54=1296=1331-35$, and $1-36=5-40=-35$. So $24\cdot 54\equiv 1-36\equiv 5-40 \pmod{1331}$. The solution is unique modulo $1331$, and $0\le 54<1331$. Hence $\delta^{[1]}_{36,3}=\delta^{[2]}_{40,3}=54$.

This arithmetic is checked in Lean (theorem `side_conditions` in [`lean/Pipeline/BanerjeeSmoot/Main.lean`](lean/Pipeline/BanerjeeSmoot/Main.lean)). Both programs of Step 3 also compute $\delta=54$, one by a modular inverse and one by searching all of $[0,1331)$.

### Step 2. Truncation lemma. Status: proposed

**Lemma.** Let $0\le m\le M$, and put

```math
F_M=\prod_{k=1}^{M}(1+q^k),\qquad E_M=\prod_{k=1}^{M}(1-q^k).
```

Then for all integers $a$ and $b$,

```math
[q^m]\Big((-q;q)_\infty^{a}(q;q)_\infty^{-b}\Big)=[q^m]\Big(F_M^{a}E_M^{-b}\Big).
```

*Idea.* Compare both sides modulo $q^{m+1}$, using only the definition of the infinite products.

*Proof.* $F_M$ and $E_M$ have constant term $1$, so they are units and the right side is defined. Let $I=q^{m+1}\mathbb{Z}[[q]]$. Two series are congruent modulo $I$ exactly when their coefficients of $q^0,\dots,q^m$ agree.

For $K\ge M$,

```math
\prod_{k=1}^{K}(1+q^k)=F_M\prod_{k=M+1}^{K}(1+q^k)\equiv F_M \pmod{I},
```

because each factor $1+q^k$ with $k>M\ge m$ is congruent to $1$ modulo $I$. The coefficients of $q^0,\dots,q^m$ of $(-q;q)_\infty$ are those of these partial products (§1). Hence $(-q;q)_\infty\equiv F_M \pmod{I}$. In the same way, $(q;q)_\infty\equiv E_M \pmod{I}$.

The quotient map from $\mathbb{Z}[[q]]$ to $\mathbb{Z}[[q]]/I$ is a ring homomorphism. It maps units to units and inverses to inverses. So $(-q;q)_\infty^{a}(q;q)_\infty^{-b}\equiv F_M^{a}E_M^{-b} \pmod{I}$ for all integers $a$ and $b$. $\square$

This lemma is **not formalized**: Mathlib has no infinite $q$-Pochhammer product.

### Step 3. The two coefficients. Status: certified; formalized for the truncated products

(a) $p^{[1]}_{36}(54)=N_1$ and $p^{[2]}_{40}(54)=N_2$.

(b) $[q^{54}]\big(F_{54}^{36}E_{54}^{-1}\big)=N_1$ and $[q^{54}]\big(F_{54}^{40}E_{54}^{-5}\big)=N_2$.

These are finite integer computations. They are not done by hand.

- Part (a) is **certified** by two independent exact programs ([`cert/NTA-1/`](cert/NTA-1/)).
  - The primary program (Python with python-flint) uses the products over $k\le 4047$. By Step 2 with $m=54$ and $M=4047$, this gives the coefficients of the infinite products.
  - The cross-check (Node.js BigInt, no libraries) uses the recurrence below, which holds for the infinite products themselves, so it does not truncate.
  - A third script requires the two result lines to be identical.
- Part (b) is **formalized** in Lean ([`LEAN.md`](LEAN.md)). By Step 2 with $m=M=54$, parts (a) and (b) state the same equalities. So the Lean check is a third verification of (a), and it relies on Step 2.

The cross-check's recurrence, for $P=\prod_{k\ge 1}(1+q^k)^{a}(1-q^k)^{-b}=\sum_m p(m)q^m$:

```math
m\cdot p(m)=\sum_{k=1}^{m}s(k)p(m-k)\quad(m\ge 1),\qquad p(0)=1,\qquad s(k)=\sum_{e\mid k}e\left(b+a(-1)^{k/e+1}\right).
```

It comes from applying $\theta=q\frac{d}{dq}$ to $\log P$: for each $e\ge 1$, $\theta\log(1+q^e)=\sum_{j\ge 1}(-1)^{j+1}e q^{je}$ and $-\theta\log(1-q^e)=\sum_{j\ge 1}e q^{je}$. So $\theta P$ equals $P$ times $\sum_k s(k)q^k$, and comparing coefficients gives the recurrence.

### Step 4. Residues modulo 121. Status: certified; formalized

$N_1\equiv 33 \pmod{121}$ and $N_2\equiv 55 \pmod{121}$. Both programs print these residues, and Lean proves them (with $121\nmid N_1$ and $121\nmid N_2$).

### Step 5. Conclusion. Status: certified

*Part (1).* By Step 1, $a=36$ satisfies the hypothesis of part (1), and the shift at $\alpha=3$ is $54$. With $n=0$, the conjecture asserts $p^{[1]}_{36}(54)\equiv 0 \pmod{121}$. By Step 3, $p^{[1]}_{36}(54)=N_1$. By Step 4, $N_1\equiv 33\not\equiv 0 \pmod{121}$. So part (1) fails.

*Part (2).* The same argument with $a=40$, shift $54$, $p^{[2]}_{40}(54)=N_2$ and $N_2\equiv 55\not\equiv 0 \pmod{121}$.

*Valuations.* By Step 4, $N_1=121k+33=11(11k+3)$ for some integer $k$. So $11$ divides $N_1$, and $N_1/11\equiv 3 \pmod{11}$ is not divisible by $11$. Hence $v_{11}(N_1)=1$. In the same way $N_2/11\equiv 5 \pmod{11}$, so $v_{11}(N_2)=1$. Both programs also print $v_{11}=1$. $\square$

## 5. Remarks

### 5.1 The failure starts at level 3. Status: certified

The congruence $24\cdot 54\equiv -35 \pmod{1331}$ of Step 1 also holds modulo $11$ and modulo $121$. So, in both parts, the shift is $10$ at level 1 (as $54=4\cdot 11+10$) and $54$ at level 2. The index $54$ is the term $n=4$ of the level-1 progression and the term $n=0$ of the level-2 progression. At both levels the modulus is $11$, and $11$ divides $N_1$ and $N_2$ (Step 5). So these instances of the conjecture hold.

### 5.2 Other choices of the shift. Status: certified (for the values computed)

Every integer solution of $24\delta\equiv -35 \pmod{1331}$ is $\delta=54+1331t$ with $t\in\mathbb{Z}$.
- If $t\le 0$, the progression $1331n+\delta$ with $n\in\mathbb{N}_0$ contains $54$, at $n=-t$. So the conjecture with this $\delta$ again asserts that $121$ divides the coefficient at $54$, which is false.
- If $t\in\{1,2,3\}$, the instance $n=0$ concerns the index $54+1331t$. Both programs computed these coefficients exactly. None is $0$ modulo $121$ (table below), so the conjecture fails for these choices too.
- For $t\ge 4$ the coefficients have not been computed.

With $\delta=54$, the indices $1385$, $2716$, $4047$ are the instances $n=1,2,3$: three further failures in each part.

| $m$ | $p^{[1]}_{36}(m)$ mod 121 | $p^{[2]}_{40}(m)$ mod 121 |
| --- | --- | --- |
| 54 | 33 | 55 |
| 1385 | 11 | 55 |
| 2716 | 11 | 66 |
| 4047 | 11 | 99 |

All eight coefficients have $v_{11}=1$. Source: [`cert/NTA-1/out/NTA-1.out`](cert/NTA-1/out/NTA-1.out) and [`cert/NTA-1/out/NTA-1_x.out`](cert/NTA-1/out/NTA-1_x.out), compared in [`cert/NTA-1/out/compare.out`](cert/NTA-1/out/compare.out).

## 6. What this proof does not cover

- It does not use or test the source's proved Theorem 1.1 (the case $a=2$ of part (2)).
- It says nothing about which other values of $a$ satisfy the conjecture. The numerical data and the heuristic in [`README.md`](README.md) are separate from this proof and have weaker status (numerical and heuristic).
- Step 2 is not formalized, and the statement of Conjecture 6.1 itself is not written in Lean. The link between the Lean theorems and the conjecture is Steps 1, 2 and 5, done by hand.
