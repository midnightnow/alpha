/**
 * Sexagesimal (Base-60) Formatting Utilities
 *
 * Old Babylonian mathematicians used base-60, which is why we have
 * 60 seconds in a minute and 360 degrees in a circle.
 *
 * Notation conventions:
 * - Integers: comma-separated places (e.g., "57, 36" = 57×60 + 36 = 3456)
 * - Fractions: semicolon after integer part (e.g., "0;45" = 45/60 = 0.75)
 */

/**
 * Format an integer in sexagesimal notation
 * @param {number} n - The integer to format
 * @param {object} opts - Options
 * @param {boolean} opts.padPlaces - Pad subsequent places to 2 digits (default true)
 * @returns {string} Sexagesimal representation (e.g., 3456 → "57, 36")
 */
export function formatSexagesimalInt(n, { padPlaces = true } = {}) {
  if (!Number.isFinite(n)) return "—";
  if (n === 0) return "0";

  const sign = n < 0 ? "-" : "";
  let rem = Math.floor(Math.abs(n));
  const places = [];

  while (rem > 0) {
    places.unshift(rem % 60);
    rem = Math.floor(rem / 60);
  }

  const out = places
    .map((p, idx) => (padPlaces && idx > 0 ? String(p).padStart(2, "0") : String(p)))
    .join(", ");

  return sign + out;
}

/**
 * Exact sexagesimal for a rational number numerator/denominator.
 * Great for pitch r = s/l where precision matters.
 * @param {number} numer - Numerator
 * @param {number} denom - Denominator
 * @param {number} maxPlaces - Maximum fractional places (default 4)
 * @returns {string} Exact sexagesimal (e.g., 119/120 → "0;59,30")
 */
export function formatSexagesimalRational(numer, denom, maxPlaces = 4) {
  if (!Number.isFinite(numer) || !Number.isFinite(denom) || denom === 0) return "—";

  const sign = (numer / denom) < 0 ? "-" : "";
  numer = Math.abs(Math.round(numer));
  denom = Math.abs(Math.round(denom));

  const intPart = Math.floor(numer / denom);
  let rem = numer % denom;

  const parts = [String(intPart)];

  for (let i = 0; i < maxPlaces && rem !== 0; i++) {
    rem *= 60;
    const digit = Math.floor(rem / denom);
    rem = rem % denom;
    parts.push(String(digit).padStart(2, "0"));
  }

  return sign + parts[0] + (parts.length > 1 ? ";" + parts.slice(1).join(",") : "");
}

/**
 * Format a fraction/ratio in sexagesimal notation
 * Uses semicolon to separate integer from fractional part
 * @param {number} r - The ratio to format (0 < r < 1 typically)
 * @param {number} maxPlaces - Maximum fractional places (default 4)
 * @returns {string} Sexagesimal representation (e.g., 0.75 → "0;45")
 */
export function formatSexagesimalFrac(r, maxPlaces = 4) {
  if (!Number.isFinite(r)) return "—";

  const sign = r < 0 ? "-" : "";
  r = Math.abs(r);

  const intPart = Math.floor(r);
  let frac = r - intPart;
  const parts = [intPart.toString()];

  for (let i = 0; i < maxPlaces && frac > 1e-9; i++) {
    frac *= 60;
    const digit = Math.floor(frac);
    parts.push(digit.toString().padStart(2, "0"));
    frac -= digit;
  }

  // Format: "intPart;fracPart1,fracPart2,..."
  if (parts.length === 1) {
    return sign + parts[0];
  }
  return sign + parts[0] + ";" + parts.slice(1).join(",");
}

/**
 * Parse sexagesimal integer notation back to decimal
 * Handles signs and extra whitespace
 * @param {string} sexStr - Sexagesimal string (e.g., "57, 36" or "-1, 05")
 * @returns {number} Decimal value
 */
export function parseSexagesimalInt(sexStr) {
  if (typeof sexStr !== "string") return NaN;

  const s = sexStr.trim();
  const sign = s.startsWith("-") ? -1 : 1;
  const clean = s.replace(/^[+-]/, "");

  const parts = clean.split(",").map(t => Number.parseInt(t.trim(), 10));
  if (parts.some(p => !Number.isFinite(p) || p < 0 || p >= 60)) return NaN;

  let result = 0;
  for (const p of parts) result = result * 60 + p;
  return sign * result;
}

/**
 * Calculate greatest common divisor
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
export function gcd(a, b) {
  a = Math.abs(Math.round(a));
  b = Math.abs(Math.round(b));
  while (b !== 0) {
    [a, b] = [b, a % b];
  }
  return a;
}

/**
 * Reduce a triple to its primitive form
 * @param {number} s - Short side
 * @param {number} l - Long side
 * @param {number} d - Diagonal (hypotenuse)
 * @returns {{s: number, l: number, d: number, scaleFactor: number}}
 */
export function reduceTriple(s, l, d) {
  const g = gcd(gcd(s, l), d);
  return {
    s: Math.round(s / g),
    l: Math.round(l / g),
    d: Math.round(d / g),
    scaleFactor: g
  };
}

/**
 * Check if a number is "regular" (only has 2, 3, 5 as prime factors)
 * Regular numbers have terminating sexagesimal representations
 * @param {number} n - The number to check
 * @returns {boolean}
 */
export function isRegular(n) {
  if (n <= 0) return false;
  n = Math.abs(Math.round(n));

  // Divide out all factors of 2, 3, and 5
  while (n % 2 === 0) n /= 2;
  while (n % 3 === 0) n /= 3;
  while (n % 5 === 0) n /= 5;

  // If we're left with 1, the number was regular
  return n === 1;
}

/**
 * Get prime factorization as a formatted string
 * @param {number} n
 * @returns {string} e.g., "2³·3·5"
 */
export function formatPrimeFactors(n) {
  if (n <= 1) return String(n);

  const factors = [];
  const superscripts = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"];

  function toSuperscript(num) {
    if (num === 1) return "";
    return String(num).split("").map(d => superscripts[parseInt(d)]).join("");
  }

  let remaining = n;
  for (const prime of [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]) {
    let count = 0;
    while (remaining % prime === 0) {
      remaining /= prime;
      count++;
    }
    if (count > 0) {
      factors.push(`${prime}${toSuperscript(count)}`);
    }
    if (remaining === 1) break;
  }

  if (remaining > 1) {
    factors.push(String(remaining));
  }

  return factors.join("·");
}

/**
 * Convert pitch ratio to "rise per 12 run" notation (carpenter style)
 * @param {number} r - The pitch ratio (s/l)
 * @returns {string} e.g., "9/12" or "11.9/12"
 */
export function toPitchPer12(r) {
  const risePer12 = r * 12;
  // If close to integer, show as integer
  if (Math.abs(risePer12 - Math.round(risePer12)) < 0.01) {
    return `${Math.round(risePer12)}/12`;
  }
  return `${risePer12.toFixed(1)}/12`;
}

/**
 * Format a number with trailing zeros trimmed
 * @param {number} n
 * @param {number} digits
 * @returns {string}
 */
export function toFixedTrim(n, digits = 3) {
  if (!Number.isFinite(n)) return "—";
  const s = n.toFixed(digits);
  return s.replace(/\.?0+$/, "");
}
