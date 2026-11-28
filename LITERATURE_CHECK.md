# Literature and priority check

- **Dates:** two searches on 2026-11-27. The first (06:07–13:22 UTC) asked whether Conjecture 6.1 was open. The second (14:24–15:19 UTC) asked whether anyone had already reported, corrected, restricted or claimed its failure.
- **Correction (2026-11-28):** these searches missed two earlier reports of the same failure, both on GitHub: [AmirMakir/broken-conjectures](https://github.com/AmirMakir/broken-conjectures/tree/234e28fc05/conjectures/eleven-adic-2611.09681) (2026-11-25, commit `234e28f`) and [rpinho/math-certificates](https://github.com/rpinho/math-certificates/tree/main/conjectures/2611-09681-conj61) (2026-11-26, with a Lean proof). Neither search included GitHub code search; they were found by a re-check on 2026-11-28. Credit for the counterexamples goes to them; we claim no priority.
- **Result as recorded on 2026-11-27 (superseded):** no report, correction, restriction or claim of the failure was found. The source is at version 1 only (still so on 2026-11-28), with no recorded citing work.
- **Main risk:** the authors themselves. They are active on this programme, and a version 2 of their preprint, or a follow-up paper, could restrict or correct the conjecture at any time.

## The source

K. Banerjee and N. A. Smoot, *On a problem of Gordon and Hughes: the 11-adic properties of meromorphic modular functions on $X_0(22)$*, [arXiv:2611.09681](https://arxiv.org/abs/2611.09681).

- **Versions.** Only v1 exists, submitted 2026-11-06 16:30:02 UTC. There is no comments field, journal reference, erratum or withdrawal. The address `/abs/2611.09681v2` returned HTTP 404 at 15:19 UTC on 2026-11-27.
- **Statement check.** Conjecture 6.1 was copied from the PDF and compared with the HTML rendering ([HTML v1](https://arxiv.org/html/2611.09681v1)). The PDF's text layer drops relation symbols, so the raw glyphs were decoded: part (1) has $\equiv$, part (2) has $\not\equiv$, the modulus is $11^{\lceil\alpha/2\rceil}$ (ceiling), and the congruences for $\delta$ are modulo $11^\alpha$. The two renderings agree symbol for symbol.
- **Proved case.** Theorem 1.1 of the source (if $8n\equiv 1 \pmod{11^\alpha}$ then $d_2(n)\equiv 0 \pmod{11^{\lfloor(\alpha+1)/2\rfloor}}$, where $\sum d_2(n)q^n=(q^2;q^2)_\infty^2/(q;q)_\infty^7$) is exactly the case $a=2$ of part (2), because $\lfloor(\alpha+1)/2\rfloor=\lceil\alpha/2\rceil$ and $24\delta\equiv 3$ is equivalent to $8\delta\equiv 1$ modulo $11^\alpha$. The source proves only this case. Its supplementary notebooks ([supplement page](https://homepage.univie.ac.at/nicolas.allen.smoot/?page_id=257)) cover only this case.
- **Evidence range in the source.** The source states no numerical range for other values of $a$.
- **Level 2 and $X_0(22)$.** The source calls $P^{[1]}_a$ and $P^{[2]}_a$ "eta quotients of level 2" and says that the associated congruence families live on $X_0(22)$. Both phrases are in the source; the level $22=2\cdot 11$ is that of the curve on which the families are studied. The counterexample uses only the $q$-series definitions, so it does not depend on this description.
- **Author pages and talks.** Both authors list the preprint as submitted, with no erratum (checked 2026-11-27). Smoot's slides for the Michigan Tech partition seminar ([2026-04-02](https://pages.mtu.edu/~wjkeith/PartitionsSpecialtySeminar/Nicolas-Smoot-Apr2026.pdf)) and for SLC 96 ([2026-10-05](https://www.mat.univie.ac.at/~slc/wpapers/s96vortrag/smoot.pdf)) present Theorem 1.1 only. The later slides ask whether more congruence families like it can be found. Neither states Conjecture 6.1. As far as we found, its first and only public statement is arXiv v1.

## Timeline

| Date | Event | Link |
| --- | --- | --- |
| 1967 | Atkin proves Ramanujan's conjecture for $p(n)$ modulo powers of 11 | [doi:10.1017/S0017089500000045](https://doi.org/10.1017/S0017089500000045) |
| 1981 | Gordon and Hughes, *Ramanujan congruences for q(n)*; according to the source, they first speculated about a congruence family attached to a curve of genus 2 | [doi:10.1007/BFb0096473](https://doi.org/10.1007/BFb0096473) |
| 1983 | Gordon, *Ramanujan congruences for $p_{-k}$ (mod $11^r$)* | [Glasgow Math. J.](https://www.cambridge.org/core/journals/glasgow-mathematical-journal/article/ramanujan-congruences-for-pk-mod-11/25B481EC52D78BF72E4FAF7DCC110E64) |
| 2019-06-02 | Petta Mestrige, *Congruences modulo powers of 11 for some eta-quotients* | [arXiv:1906.00428](https://arxiv.org/abs/1906.00428) |
| 2026-04-02 | Smoot, Michigan Tech seminar talk "A Genus 2 Congruence Family" (Theorem 1.1 only) | [slides](https://pages.mtu.edu/~wjkeith/PartitionsSpecialtySeminar/Nicolas-Smoot-Apr2026.pdf) |
| 2026-10-05 | Smoot, SLC 96 talk (Theorem 1.1; more families named as future work) | [slides](https://www.mat.univie.ac.at/~slc/wpapers/s96vortrag/smoot.pdf) |
| 2026-11-06 | Banerjee–Smoot, arXiv v1, with Theorem 1.1 and Conjecture 6.1 | [arXiv:2611.09681v1](https://arxiv.org/abs/2611.09681v1) |
| 2026-11-27 | The failure at $\alpha=3$ ($a=36$, $a=40$) is found, certified by two independent programs and checked in Lean; the second search finds no earlier report | this repository |

## Where the conjecture is known to hold

- **Part (2), $a=2$, every $\alpha$:** proved in the source (Theorem 1.1). This is the authors' result.
- **Part (2), $a=0$ and $a=-5$:** here the series are $1/(q;q)_\infty^5$ and $1/(q^2;q^2)_\infty^5$, so both cases reduce to the 5-coloured partition function $p_{-5}$, with $24m\equiv 5 \pmod{11^\alpha}$. Congruences for $p_{-k}$ modulo powers of 11 were proved by Gordon (1983); his paper is paywalled and was not read, only the restatement in K. Hughes, Canad. J. Math. 43 (1991) 506–525 ([doi:10.4153/CJM-1991-031-0](https://doi.org/10.4153/CJM-1991-031-0)). Petta Mestrige (arXiv:1906.00428, Theorem 1.1 and Tables 2–3) gives an explicit exponent. By our reading of those tables, the exponent for $p_{-5}$ is $\lfloor\alpha/2\rfloor+1$, which is at least $\lceil\alpha/2\rceil$, so these two cases of the conjecture hold. This reading has not been reviewed. These two cases live on $X_0(11)$ (genus 1) rather than genuinely on $X_0(22)$.
- **Everything else** was open before this work: no proof, partial proof or counterexample was found for any other $a$ in either part.

The counterexamples ($a=36$ in part (1), $a=40$ in part (2)) are not among these known cases.

## Sources searched for the failure (14:24–15:19 UTC, 2026-11-27)

| Source | What was searched | Finding |
| --- | --- | --- |
| arXiv | The abs page and API for 2611.09681 (versions); author searches for Smoot and Banerjee; abstract searches ("Gordon and Hughes", "X_0(22)", "genus 2" with congruence, "congruence family", "11-adic", "powers of 11", elongated partitions, eta quotients with congruences); recent math.NT and math.CO congruence listings since 2026-11-06 | Still v1; nothing by either author after 2026-11-06; no follow-up, erratum or counterexample |
| Citation indexes | OpenAlex (citing works), Semantic Scholar (citations endpoint) | 0 citing works in both |
| Author pages | Smoot's homepage (publications, talks, modification dates); Banerjee's research and activities pages; the Michigan Tech seminar page | Preprint listed as submitted; no erratum; no later talk on the conjecture |
| Web and GitHub | Web search (six phrasings); GitHub code search for "2611.09681" and issue searches | Only the paper, the slides, and arXiv listing bots |
| Problem catalogs and AI-assisted projects | [solved-conjectures](https://github.com/1337isnot1337/solved-conjectures) (issues, comments since 05:00 UTC, both branches); [trureturing](https://github.com/the-omega-institute/trureturing) (issues, code, mdbook); RealRooted issues; formal-conjectures; Zenodo (author, title and keyword searches); Hexagon, Prove2Me, Crab Research and eulersolve sitemaps; MathDB search; several other public repositories | No entry for Conjecture 6.1 and no report of its failure |
| Q&A and sequences | MathOverflow and Math.SE (StackExchange API); OEIS | Nothing relevant |

## What could not be checked

- Google Scholar (a bot check blocked the search), so its "cited by" count is unknown.
- The Semantic Scholar paper record (rate-limited; the citations endpoint did answer, with none).
- UnsolvedMath (rate-limited).
- Hexagon paper pages (behind a sign-in; only the public sitemaps were read).
- The content of Prove2Me's formalpedia (not code-indexed).
- arXiv full text (not searchable; body-only citations would show only in the citation indexes).
- The video of the 2026-04-02 talk (not watched; it predates the paper).

## Before any public release

Re-check, on the day of release: arXiv for a version 2 or erratum of 2611.09681; the authors' pages; and the catalogs above. If the authors have corrected or restricted the conjecture by then, the credit lines and this file must say so.
