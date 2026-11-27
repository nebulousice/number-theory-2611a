import Mathlib.RingTheory.PowerSeries.Inverse
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Pipeline.BanerjeeSmoot.Stages

/-!
# Banerjee–Smoot Conjecture 6.1 fails at α = 3 (ledger NTA-1)

Source: K. Banerjee, N. A. Smoot, arXiv:2611.09681v1, §6, Conjecture 6.1. With
`P¹_a = (-q;q)_∞^a / (q;q)_∞` and `P²_a = (-q;q)_∞^a / (q;q)_∞^5`, the conjecture asserts
`p_a(11^α n + δ) ≡ 0 (mod 11^⌈α/2⌉)`. At α = 3, n = 0, δ = 54 (least residue of the
δ-congruence mod 1331) we show:

* part (1), a = 36 ≡ 3 (mod 11): the coefficient of `q^54` is
  `62043410886974649205238011198`, which is `≡ 33 (mod 121)`;
* part (2), a = 40 ≡ 7 (mod 11): the coefficient of `q^54` is
  `66134580699742235651549220246110`, which is `≡ 55 (mod 121)`.

**What is formalized.** Write `F₅₄ = ∏_{k=1}^{54} (1 + X^k)` and `E₅₄ = ∏_{k=1}^{54} (1 - X^k)`
in `ℤ⟦X⟧`. For *every* power series `G` with `G * E₅₄ = 1` (resp. `G * E₅₄^5 = 1`) the
coefficient of `X^54` in `F₅₄^36 * G` (resp. `F₅₄^40 * G`) is the stated integer, and it is not
divisible by 121; such a `G` exists (`E₅₄` is a unit). The computation is done on lists of
naturals and checked by the kernel (`decide +kernel`, no `native_decide`), in stages whose
intermediate lists are generated literals (`Stages.lean`, from
`targets/number-theory-2611a/cert/NTA-1/gen_lean_stages.py`) re-checked step by step; a proved
transport lemma links each list step to multiplication by `1 + X^m` in `ℤ⟦X⟧`, and
`1/(1 - X^k)` is replaced by `∏_{j<6} (1 + X^(k 2^j))`, which agrees with it modulo `X^55`.

**Not formalized (standard, one line).** Mathlib has no infinite `q`-Pochhammer product, so
the passage from `(±q;q)_∞` to the truncations at `k ≤ 54` is not in Lean: factors with
`k ≥ 55` are `≡ 1 (mod q^55)` and do not change the coefficients of `q^0, …, q^54`.
-/

namespace BanerjeeSmoot

open PowerSeries

/-! ## Computable side: truncated coefficient lists -/

/-- Multiply a truncated coefficient list by `1 + X^m`; the length is preserved. -/
def mulOnePlus (m : ℕ) (s : List ℕ) : List ℕ :=
  List.zipWith (· + ·) s (List.replicate m 0 ++ s)

/-- Apply `op 0`, then `op 1`, …, then `op (n-1)`. -/
def iterRange (op : ℕ → List ℕ → List ℕ) : ℕ → List ℕ → List ℕ
  | 0, s => s
  | n + 1, s => op n (iterRange op n s)

/-- Apply `op` `c` times. -/
def iterPow (op : List ℕ → List ℕ) : ℕ → List ℕ → List ℕ
  | 0, s => s
  | c + 1, s => op (iterPow op c s)

/-! ## Link to `ℤ⟦X⟧` -/

/-- `s` lists the first `s.length` coefficients of `f`. -/
def Rep (s : List ℕ) (f : PowerSeries ℤ) : Prop :=
  ∀ i (h : i < s.length), coeff i f = ((s[i]'h : ℕ) : ℤ)

/-- The list operation `op` realises multiplication by `Q` on truncations. -/
def Transport (op : List ℕ → List ℕ) (Q : PowerSeries ℤ) : Prop :=
  ∀ s f, Rep s f → Rep (op s) (Q * f)

theorem length_mulOnePlus (m : ℕ) (s : List ℕ) : (mulOnePlus m s).length = s.length := by
  simp [mulOnePlus]

theorem transport_mulOnePlus (m : ℕ) : Transport (mulOnePlus m) (1 + X ^ m) := by
  intro s f hs i hi
  have hi' : i < s.length := by simpa [length_mulOnePlus] using hi
  simp only [mulOnePlus, List.getElem_zipWith, add_mul, one_mul, map_add, coeff_X_pow_mul',
    hs i hi', Nat.cast_add]
  congr 1
  rw [List.getElem_append]
  by_cases h : i < m
  · have h' : ¬ m ≤ i := by omega
    simp [h, h']
  · have h' : m ≤ i := by omega
    have h3 : i - m < s.length := by omega
    simp [h, h', hs (i - m) h3]

theorem transport_iterRange (op : ℕ → List ℕ → List ℕ) (Q : ℕ → PowerSeries ℤ)
    (h : ∀ k, Transport (op k) (Q k)) (n : ℕ) :
    Transport (iterRange op n) (∏ k ∈ Finset.range n, Q k) := by
  induction n with
  | zero => intro s f hs; simpa [iterRange] using hs
  | succ n ih =>
    intro s f hs
    rw [Finset.prod_range_succ, mul_comm _ (Q n), mul_assoc]
    exact h n _ _ (ih _ _ hs)

theorem transport_iterPow (op : List ℕ → List ℕ) (Q : PowerSeries ℤ) (h : Transport op Q)
    (c : ℕ) : Transport (iterPow op c) (Q ^ c) := by
  induction c with
  | zero => intro s f hs; simpa [iterPow] using hs
  | succ c ih =>
    intro s f hs
    rw [pow_succ', mul_assoc]
    exact h _ _ (ih _ _ hs)

theorem rep_init (N : ℕ) : Rep (1 :: List.replicate N 0) 1 := by
  intro i hi
  rcases i with _ | i
  · simp [coeff_one]
  · simp [coeff_one]

/-! ## The truncated products -/

/-- `(-q;q)_∞` truncated to the factors `k ≤ 54`. -/
noncomputable def F54 : PowerSeries ℤ := ∏ k ∈ Finset.range 54, (1 + X ^ (k + 1))

/-- `(q;q)_∞` truncated to the factors `k ≤ 54`. -/
noncomputable def E54 : PowerSeries ℤ := ∏ k ∈ Finset.range 54, (1 - X ^ (k + 1))

/-- `∏_{k ≤ 54} ∏_{j < 6} (1 + X^(k 2^j))`, equal to `1 / E54` modulo `X^55`. -/
noncomputable def H54 : PowerSeries ℤ :=
  ∏ k ∈ Finset.range 54, ∏ j ∈ Finset.range 6, (1 + X ^ ((k + 1) * 2 ^ j))

def opF : List ℕ → List ℕ := iterRange (fun k => mulOnePlus (k + 1)) 54

def opH : List ℕ → List ℕ :=
  iterRange (fun k => iterRange (fun j => mulOnePlus ((k + 1) * 2 ^ j)) 6) 54

theorem transport_F : Transport opF F54 :=
  transport_iterRange _ _ (fun k => transport_mulOnePlus (k + 1)) 54

theorem transport_H : Transport opH H54 :=
  transport_iterRange _ _
    (fun k => transport_iterRange _ _ (fun j => transport_mulOnePlus ((k + 1) * 2 ^ j)) 6) 54

/-! ## `H54` inverts `E54` modulo `X^55` -/

theorem telescope (k n : ℕ) :
    (1 - X ^ k) * ∏ j ∈ Finset.range n, (1 + X ^ (k * 2 ^ j)) = (1 - X ^ (k * 2 ^ n) : ℤ⟦X⟧) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.prod_range_succ, ← mul_assoc, ih]
    have : k * 2 ^ (n + 1) = k * 2 ^ n + k * 2 ^ n := by ring
    rw [this, pow_add]
    ring

theorem dvd_one_sub_prod {ι : Type*} [DecidableEq ι] (s : Finset ι) (u : ι → PowerSeries ℤ)
    (p : PowerSeries ℤ) (h : ∀ i ∈ s, p ∣ u i) : p ∣ 1 - ∏ i ∈ s, (1 - u i) := by
  induction s using Finset.induction_on with
  | empty => simp
  | insert a s ha ih =>
    rw [Finset.prod_insert ha]
    have h1 : p ∣ u a := h a (Finset.mem_insert_self a s)
    have h2 := ih (fun i hi => h i (Finset.mem_insert_of_mem hi))
    have e : 1 - (1 - u a) * ∏ i ∈ s, (1 - u i)
        = (1 - ∏ i ∈ s, (1 - u i)) + u a * ∏ i ∈ s, (1 - u i) := by ring
    rw [e]
    exact dvd_add h2 (dvd_mul_of_dvd_left h1 _)

theorem dvd_one_sub_pow {p x : PowerSeries ℤ} (h : p ∣ 1 - x) (c : ℕ) : p ∣ 1 - x ^ c := by
  induction c with
  | zero => simp
  | succ c ih =>
    have e : 1 - x ^ (c + 1) = (1 - x ^ c) + x ^ c * (1 - x) := by ring
    rw [e]
    exact dvd_add ih (dvd_mul_of_dvd_right h _)

theorem HE_eq : H54 * E54 = ∏ k ∈ Finset.range 54, (1 - X ^ ((k + 1) * 2 ^ 6)) := by
  unfold H54 E54
  rw [← Finset.prod_mul_distrib]
  refine Finset.prod_congr rfl (fun k _ => ?_)
  rw [mul_comm, telescope]

theorem X55_dvd_HE : (X : ℤ⟦X⟧) ^ 55 ∣ 1 - H54 * E54 := by
  rw [HE_eq]
  refine dvd_one_sub_prod _ _ _ (fun k _ => pow_dvd_pow X (by omega))

/-- If `G * E = 1` and `H` inverts `E` modulo `X^(n+1)`, then `A * G` and `A * H` agree at `X^n`. -/
theorem coeff_eq_of_inv {A G E H : PowerSeries ℤ} {n : ℕ} (hG : G * E = 1)
    (hHE : (X : ℤ⟦X⟧) ^ (n + 1) ∣ 1 - H * E) : coeff n (A * G) = coeff n (A * H) := by
  have e : A * G - A * H = A * G * (1 - H * E) := by
    calc A * G - A * H = A * G - A * H * (G * E) := by rw [hG, mul_one]
      _ = A * G * (1 - H * E) := by ring
  have hd : (X : ℤ⟦X⟧) ^ (n + 1) ∣ A * G - A * H := e ▸ dvd_mul_of_dvd_right hHE _
  rw [X_pow_dvd_iff] at hd
  have := hd n (Nat.lt_succ_self n)
  rw [map_sub] at this
  exact sub_eq_zero.mp this

theorem E54_isUnit : IsUnit E54 := by
  rw [isUnit_iff_constantCoeff]
  unfold E54
  rw [map_prod]
  simp

/-! ## The two kernel computations -/

def init : List ℕ := 1 :: List.replicate 54 0

/-- Coefficients `q^0..q^54` of `F54^36 * H54`. -/
def list1 : List ℕ := iterPow opH 1 (iterPow opF 36 init)

/-- Coefficients `q^0..q^54` of `F54^40 * H54^5`. -/
def list2 : List ℕ := iterPow opH 5 (iterPow opF 40 init)

/-- A chain of literal lists `Ls` with `Ls[0] = s` and `op Ls[c] = Ls[c+1]` computes `op^n s`.
The literal lists come from `Stages.lean` (generated, untrusted); each step is kernel-checked
below. Staging keeps the kernel's recursion depth small. -/
theorem iterPow_chain (op : List ℕ → List ℕ) (Ls : List (List ℕ)) (s : List ℕ) :
    ∀ n, Ls.getD 0 [] = s → (∀ c, c < n → op (Ls.getD c []) = Ls.getD (c + 1) []) →
      iterPow op n s = Ls.getD n []
  | 0, h0, _ => by rw [iterPow]; exact h0.symm
  | n + 1, h0, h => by
      rw [iterPow, iterPow_chain op Ls s n h0 (fun c hc => h c (by omega)), h n (by omega)]

set_option maxRecDepth 100000 in
theorem chainF36_ok : ∀ c, c < 36 → opF (chainF36.getD c []) = chainF36.getD (c + 1) [] := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem chainH1_ok : ∀ c, c < 1 → opH (chainH1.getD c []) = chainH1.getD (c + 1) [] := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem chainF40_ok : ∀ c, c < 40 → opF (chainF40.getD c []) = chainF40.getD (c + 1) [] := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem chainH5_ok : ∀ c, c < 5 → opH (chainH5.getD c []) = chainH5.getD (c + 1) [] := by
  decide +kernel

set_option maxRecDepth 100000 in
theorem list1_54 : list1[54]? = some 62043410886974649205238011198 := by
  have e1 : iterPow opF 36 init = chainF36.getD 36 [] :=
    iterPow_chain _ _ _ 36 (by decide +kernel) chainF36_ok
  have e2 : iterPow opH 1 (chainF36.getD 36 []) = chainH1.getD 1 [] :=
    iterPow_chain _ _ _ 1 (by decide +kernel) chainH1_ok
  unfold list1
  rw [e1, e2]
  decide +kernel

set_option maxRecDepth 100000 in
theorem list2_54 : list2[54]? = some 66134580699742235651549220246110 := by
  have e1 : iterPow opF 40 init = chainF40.getD 40 [] :=
    iterPow_chain _ _ _ 40 (by decide +kernel) chainF40_ok
  have e2 : iterPow opH 5 (chainF40.getD 40 []) = chainH5.getD 5 [] :=
    iterPow_chain _ _ _ 5 (by decide +kernel) chainH5_ok
  unfold list2
  rw [e1, e2]
  decide +kernel

theorem rep1 : Rep list1 (F54 ^ 36 * H54) := by
  have := transport_iterPow _ _ transport_H 1 _ _
    (transport_iterPow _ _ transport_F 36 _ _ (rep_init 54))
  have e : H54 ^ 1 * (F54 ^ 36 * 1) = F54 ^ 36 * H54 := by ring
  rw [e] at this
  exact this

theorem rep2 : Rep list2 (F54 ^ 40 * H54 ^ 5) := by
  have := transport_iterPow _ _ transport_H 5 _ _
    (transport_iterPow _ _ transport_F 40 _ _ (rep_init 54))
  have e : H54 ^ 5 * (F54 ^ 40 * 1) = F54 ^ 40 * H54 ^ 5 := by ring
  rw [e] at this
  exact this

theorem coeff_of_rep {s : List ℕ} {f : PowerSeries ℤ} {v : ℕ} (hr : Rep s f) (hs : s[54]? = some v) :
    coeff 54 f = v := by
  rw [List.getElem?_eq_some_iff] at hs
  obtain ⟨h, hv⟩ := hs
  rw [hr 54 h, hv]

/-! ## Main statements -/

/-- Part (1), a = 36, α = 3, δ = 54: the coefficient of `q^54` of `(-q;q)^36/(q;q)`. -/
theorem part1_coeff (G : PowerSeries ℤ) (hG : G * E54 = 1) :
    coeff 54 (F54 ^ 36 * G) = 62043410886974649205238011198 := by
  rw [coeff_eq_of_inv (n := 54) hG X55_dvd_HE]
  exact_mod_cast coeff_of_rep rep1 list1_54

/-- Part (2), a = 40, α = 3, δ = 54: the coefficient of `q^54` of `(-q;q)^40/(q;q)^5`. -/
theorem part2_coeff (G : PowerSeries ℤ) (hG : G * E54 ^ 5 = 1) :
    coeff 54 (F54 ^ 40 * G) = 66134580699742235651549220246110 := by
  have hHE : (X : ℤ⟦X⟧) ^ (54 + 1) ∣ 1 - H54 ^ 5 * E54 ^ 5 := by
    rw [← mul_pow]; exact dvd_one_sub_pow X55_dvd_HE 5
  rw [coeff_eq_of_inv (n := 54) hG hHE]
  exact_mod_cast coeff_of_rep rep2 list2_54

/-- The hypotheses `a ≡ 3 (mod 11)` / `a ≢ 1,3,5 (mod 11)` and `24 δ ≡ c - a (mod 11^3)`. -/
theorem side_conditions :
    (36 : ℤ) % 11 = 3 ∧ (24 * 54 - (1 - 36) : ℤ) % 11 ^ 3 = 0 ∧
    (40 : ℤ) % 11 = 7 ∧ (24 * 54 - (5 - 40) : ℤ) % 11 ^ 3 = 0 ∧
    (0 : ℕ) ≤ 54 ∧ 54 < 11 ^ 3 ∧ (3 + 1) / 2 = 2 := by
  decide +kernel

/-- **NTA-1.** Conjecture 6.1 fails at α = 3, n = 0 in both parts: for the (unique) inverse
`G` of `E54` resp. `E54^5`, the relevant coefficient is `≡ 33` resp. `≡ 55 (mod 11^2)`. -/
theorem NTA1 :
    (∃ G : PowerSeries ℤ, G * E54 = 1) ∧ (∃ G : PowerSeries ℤ, G * E54 ^ 5 = 1) ∧
    (∀ G : PowerSeries ℤ, G * E54 = 1 →
      coeff 54 (F54 ^ 36 * G) % 121 = 33 ∧ ¬ (121 : ℤ) ∣ coeff 54 (F54 ^ 36 * G)) ∧
    (∀ G : PowerSeries ℤ, G * E54 ^ 5 = 1 →
      coeff 54 (F54 ^ 40 * G) % 121 = 55 ∧ ¬ (121 : ℤ) ∣ coeff 54 (F54 ^ 40 * G)) := by
  obtain ⟨u, hu⟩ := E54_isUnit
  refine ⟨⟨↑u⁻¹, by rw [← hu]; exact u.inv_mul⟩, ⟨↑(u ^ 5)⁻¹, ?_⟩, ?_, ?_⟩
  · rw [← hu, ← Units.val_pow_eq_pow_val]; exact (u ^ 5).inv_mul
  · intro G hG
    rw [part1_coeff G hG]
    constructor
    · decide +kernel
    · decide +kernel
  · intro G hG
    rw [part2_coeff G hG]
    constructor
    · decide +kernel
    · decide +kernel

end BanerjeeSmoot

#print axioms BanerjeeSmoot.NTA1
#print axioms BanerjeeSmoot.side_conditions
