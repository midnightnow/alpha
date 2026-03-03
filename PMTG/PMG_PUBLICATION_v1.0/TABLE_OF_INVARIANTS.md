# TABLE OF INVARIANTS

## *Principia Mathematica Geometrica — Reference Card*

---

### The Axioms

| # | Axiom | Statement |
|---|-------|-----------|
| A1 | Succession | From count $n$, produce $n+1$ |
| A2 | Unit | The smallest count is 1 |
| A3 | Ghost Post | $n$ intervals require $n+1$ boundaries |
| A4 | Closure | The right angle extends counting to 2D |
| A5 | Bilateral | Embodied observers double their structures |

---

### The Forced Chain

$$1 \xrightarrow{A1} n \xrightarrow{A3} n{+}1 \xrightarrow{A4} 3\text{-}4\text{-}5 \xrightarrow{12} 5\text{-}12\text{-}13 \xrightarrow{A5} 10\text{-}24\text{-}26$$

---

### The Numbers

| Number | What It Is | How It Arises | Status |
|--------|-----------|---------------|--------|
| **3-4-5** | Minimal right triangle | $3^2+4^2=5^2$, smallest integers | FORCED |
| **5** | Counting hand | Odd leg of base-12 triple | FORCED |
| **12** | Cycle base | Minimal highly composite | CHOSEN |
| **13** | Ghost Post | $12+1$ boundaries | FORCED |
| **10-24-26** | Bilateral manifold | $2 \times (5, 12, 13)$ | FORCED |
| **93** | Icosahedral matrix | $12+20+60+1$ nodes | CHOSEN |
| **171** | The Spark | $13^2+2$; multiplier for alphabet | CHOSEN |
| **42** | The Pivot | $(5 \times 12) - (5+13) = 60-18$ | FORCED |
| **42.25** | Radius squared | $(5^2+12^2+13^2)/8 = 338/8$ | FORCED |
| **6.5** | Circumradius | $\sqrt{42.25} = 13/2$ | FORCED |
| **365** | Calendar resonance | $171 \times 2 + 23$ | CORRESPONDENCE |

---

### The Prime Sieve

$$42 = 2 \times 3 \times 7$$

$$\varphi(42) = 12 \quad \text{(the base cycle is the totient of the pivot)}$$

**12 channels:** $\{1, 5, 11, 13, 17, 19, 23, 25, 29, 31, 37, 41\}$

Every prime $p > 7$ satisfies $p \bmod 42 \in$ this set.

---

### The Complete Loop

$$42 \xrightarrow{\varphi} 12 \xrightarrow{+1} 13 \xrightarrow{{}^2+2} 171 \xrightarrow{\bmod 93} 5 \text{ gaps} \xrightarrow{\text{vowels}} \text{language}$$

---

### The Five Missing Nodes

$$\{16, 31, 46, 61, 76\}$$

Vowel-consonant thresholds. Arithmetic consequence of 171 mod 93.

---

### The Bilateral Signature

$$\frac{5}{10} = \frac{12}{24} = \frac{13}{26} = \frac{1}{2}$$

---

### The Status Flags

| Flag | Meaning |
|------|---------|
| **FORCED** | Arithmetic/geometric necessity |
| **CHOSEN (utilitarian)** | Pragmatic selection among alternatives |
| **CHOSEN (aesthetic)** | Selection for interpretability |
| **OBSERVED RESONANCE** | Pattern noted, not derived |

---

### Quick Verification

```
3² + 4² = 5²           ✓     5² + 12² = 13²        ✓
10² + 24² = 26²        ✓     9 + 3 + 1 = 13         ✓
171 = 13² + 2           ✓     171 mod 93 = 78         ✓
gcd(78,93) = 3          ✓     338/8 = 42.25           ✓
√42.25 = 6.5 = 13/2    ✓     (5×12)-(5+13) = 42     ✓
φ(42) = 12              ✓     171×2 + 23 = 365        ✓
```

---

*Pin this to the wall. Take the compass. Draw.*
