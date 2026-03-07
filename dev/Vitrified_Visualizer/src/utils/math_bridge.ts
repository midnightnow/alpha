/**
 * Sexagesimal (Base-60) Formatting Utilities for Sovereign Engine
 */

export function formatSexagesimalInt(n: number, { padPlaces = true } = {}): string {
    if (!Number.isFinite(n)) return "—";
    if (n === 0) return "0";

    const sign = n < 0 ? "-" : "";
    let rem = Math.floor(Math.abs(n));
    const places: number[] = [];

    while (rem > 0) {
        places.unshift(rem % 60);
        rem = Math.floor(rem / 60);
    }

    const out = places
        .map((p, idx) => (padPlaces && idx > 0 ? String(p).padStart(2, "0") : String(p)))
        .join(", ");

    return sign + out;
}

export function formatSexagesimalRational(numer: number, denom: number, maxPlaces = 4): string {
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

export function formatSexagesimalFrac(r: number, maxPlaces = 4): string {
    if (!Number.isFinite(r)) return "—";

    const sign = r < 0 ? "-" : "";
    const absR = Math.abs(r);

    const intPart = Math.floor(absR);
    let frac = absR - intPart;
    const parts = [intPart.toString()];

    for (let i = 0; i < maxPlaces && frac > 1e-9; i++) {
        frac *= 60;
        const digit = Math.floor(frac);
        parts.push(digit.toString().padStart(2, "0"));
        frac -= digit;
    }

    if (parts.length === 1) {
        return sign + parts[0];
    }
    return sign + parts[0] + ";" + parts.slice(1).join(",");
}

export function gcd(a: number, b: number): number {
    a = Math.abs(Math.round(a));
    b = Math.abs(Math.round(b));
    while (b !== 0) {
        [a, b] = [b, a % b];
    }
    return a;
}

export function reduceTriple(s: number, l: number, d: number) {
    const g = gcd(gcd(s, l), d);
    return {
        s: Math.round(s / g),
        l: Math.round(l / g),
        d: Math.round(d / g),
        scaleFactor: g
    };
}

export function toFixedTrim(n: number, digits = 3): string {
    if (!Number.isFinite(n)) return "—";
    const s = n.toFixed(digits);
    return s.replace(/\.?0+$/, "");
}

export function toPitchPer12(r: number): string {
    const risePer12 = r * 12;
    if (Math.abs(risePer12 - Math.round(risePer12)) < 0.01) {
        return `${Math.round(risePer12)}/12`;
    }
    return `${risePer12.toFixed(1)}/12`;
}
