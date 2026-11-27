// NTA-1 independent cross-check (Node.js BigInt, divisor-sum recurrence).
//
// Independent of NTA-1.py: different language, no library, different algorithm.
// For P(q) = prod_{k>=1} (1+q^k)^a (1-q^k)^(-b), taking q d/dq log P gives
//     n * p(n) = sum_{k=1}^{n} s(k) p(n-k),   p(0) = 1,
//     s(k) = sum_{d | k} d * ( b + a * (-1)^(k/d + 1) ).
// Every division by n is checked to be exact.  Exact BigInt arithmetic only.
//
// Part (1): a = 36, b = 1, 24*delta = 1 - a (mod 1331).  Part (2): a = 40, b = 5, 24*delta = 5 - a.
// The modular inverse of 24 mod 1331 is found by brute-force search (not extended Euclid).
// Usage: node NTA-1_x.mjs [NEXTRA]   (default 3: m = 54 + 1331 n, n = 0..NEXTRA)

const NEXTRA = process.argv.length > 2 ? parseInt(process.argv[2], 10) : 3;
const M = 1331n, MC = 121n;

function modp(x, m) { return ((x % m) + m) % m; }

function deltaBrute(c, a) {           // least d in [0,1331) with 24 d = c - a (mod 1331)
  const sols = [];
  for (let d = 0n; d < M; d++) if (modp(24n * d - (c - a), M) === 0n) sols.push(d);
  if (sols.length !== 1) throw new Error("delta not unique");
  return sols[0];
}

function coefficients(a, b, N) {
  // s(k) via divisor sieve, as BigInt
  const s = new Array(N + 1).fill(0n);
  const A = BigInt(a), B = BigInt(b);
  for (let d = 1; d <= N; d++) {
    for (let k = d; k <= N; k += d) {
      const j = k / d;
      const sign = (j % 2 === 1) ? 1n : -1n;   // (-1)^(j+1)
      s[k] += BigInt(d) * (B + A * sign);
    }
  }
  const p = new Array(N + 1);
  p[0] = 1n;
  for (let n = 1; n <= N; n++) {
    let acc = 0n;
    for (let k = 1; k <= n; k++) acc += s[k] * p[n - k];
    const bn = BigInt(n);
    if (acc % bn !== 0n) throw new Error(`inexact division at n=${n}`);
    p[n] = acc / bn;
  }
  return p;
}

function v11(x) {
  if (x === 0n) return null;
  let v = 0; if (x < 0n) x = -x;
  while (x % 11n === 0n) { x /= 11n; v++; }
  return v;
}

let ok = true;
// sanity: a=0,b=1 gives p(n); a=1,b=0 gives distinct partitions
const pp = coefficients(0, 1, 100);
if (pp[100] !== 190569292n || pp[10] !== 42n) { console.log("sanity p(n) failed"); ok = false; }
const qq = coefficients(1, 0, 10);
if (qq.map(String).join(",") !== "1,1,1,2,2,3,4,5,6,8,10") { console.log("sanity Q(n) failed"); ok = false; }

const cases = [
  { part: 1, a: 36, b: 1, c: 1n, expected: 62043410886974649205238011198n, residue: 33n },
  { part: 2, a: 40, b: 5, c: 5n, expected: 66134580699742235651549220246110n, residue: 55n },
];
const N = 54 + 1331 * NEXTRA;
const results = [];
for (const cs of cases) {
  const A = BigInt(cs.a);
  const r = cs.a % 11;
  const allowed = cs.part === 1 ? [3, 5, 7].includes(r) : ![1, 3, 5].includes(r);
  const d = deltaBrute(cs.c, A);
  console.log(`part (${cs.part}): a = ${cs.a}, a mod 11 = ${r}, allowed = ${allowed}, delta (brute force, unique in [0,1331)) = ${d}`);
  ok = ok && allowed && d === 54n;
  const p = coefficients(cs.a, cs.b, N);
  const rows = [];
  for (let n = 0; n <= NEXTRA; n++) {
    const m = Number(d) + 1331 * n;
    const val = p[m];
    rows.push({ m, mod11: Number(val % 11n), mod121: Number(val % MC), n, v11: v11(val), value: val.toString() });
    console.log(`  p^[${cs.part}]_${cs.a}(${m}) = ${val}`);
    console.log(`     mod 121 = ${val % MC}, mod 11 = ${val % 11n}, v_11 = ${v11(val)}`);
  }
  const w = p[Number(d)];
  const good = w === cs.expected && w % MC === cs.residue && w % MC !== 0n;
  console.log(`part (${cs.part}) witness: matches claim = ${w === cs.expected}, mod 121 = ${w % MC}, nonzero mod 121 = ${w % MC !== 0n}`);
  ok = ok && good;
  results.push({ a: cs.a, b: cs.b, delta: Number(d), part: cs.part, rows });
}
// JSON with sorted keys at every level, to compare with the primary's output
function sortKeys(o) {
  if (Array.isArray(o)) return o.map(sortKeys);
  if (o && typeof o === "object") { const r = {}; for (const k of Object.keys(o).sort()) r[k] = sortKeys(o[k]); return r; }
  return o;
}
console.log("JSON " + JSON.stringify(sortKeys({ alpha: 3, results })));
console.log(`node ${process.version}, N = ${N}`);
console.log(ok ? "PASS NTA-1 cross-check (Node BigInt, divisor-sum recurrence)" : "FAIL NTA-1 cross-check (Node BigInt, divisor-sum recurrence)");
process.exit(ok ? 0 : 1);
