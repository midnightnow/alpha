import { useState } from "react";

const W = 700, H = 500;
const PAD = 60;

// Map math coords to SVG coords
function tx(x: number, xMin: number, xMax: number) { return PAD + ((x - xMin) / (xMax - xMin)) * (W - PAD * 2); }
function ty(y: number, yMin: number, yMax: number) { return H - PAD - ((y - yMin) / (yMax - yMin)) * (H - PAD * 2); }

function gn(n: number) { return Math.sqrt(n * (n + 1)); }
function delta(n: number) { return (n + 0.5) - gn(n); }

export default function HyperbolaBridge() {
    const [hovered, setHovered] = useState<number | null>(null);
    const [nStart, setNStart] = useState(1);
    const [showHyperbola, setShowHyperbola] = useState(true);
    const [showSquares, setShowSquares] = useState(true);
    const [showBridge, setShowBridge] = useState(true);

    const N = 12;
    const nodes = Array.from({ length: N }, (_, i) => {
        const n = nStart + i;
        const g = gn(n);
        const arith = n + 0.5;
        return { n, g, arith, d: delta(n), sq: n + 1 };
    });

    // Viewport in math-space: x = n+0.5, y = gn
    const xMin = nStart - 0.5, xMax = nStart + N + 0.5;
    const yMin = nStart - 0.5, yMax = nStart + N + 0.5;

    // Hyperbola: x² - y² = 1/4  →  y = √(x² - 1/4)
    const hyperPts: { x: number; y: number }[] = [];
    for (let xi = xMin + 0.1; xi <= xMax; xi += 0.05) {
        const y2 = xi * xi - 0.25;
        if (y2 > 0) hyperPts.push({ x: xi, y: Math.sqrt(y2) });
    }
    const hyperPath = hyperPts.map((p, i) =>
        `${i === 0 ? "M" : "L"}${tx(p.x, xMin, xMax)},${ty(p.y, yMin, yMax)}`
    ).join(" ");

    // Perfect squares: y = n (integer lines)
    const intLines = Array.from({ length: N + 2 }, (_, i) => nStart + i);

    const fmtNum = (n: number) => n.toFixed(6);

    return (
        <div style={{
            background: "#080c14", minHeight: "100vh", color: "#c8d8e8",
            fontFamily: "'Courier New', monospace", padding: "24px",
            display: "flex", flexDirection: "column", alignItems: "center"
        }}>
            <div style={{ marginBottom: 8, color: "#1a3040", fontSize: 9, letterSpacing: 4 }}>
                SOVEREIGN ENGINE · HYPERBOLIC BRIDGE · PELL STRUCTURE
            </div>
            <div style={{ color: "#00ffee", fontSize: 18, fontWeight: "bold", letterSpacing: 2, marginBottom: 4 }}>
                ☙ THE GEOMETRIC MEAN MANIFOLD
            </div>
            <div style={{ color: "#1a4055", fontSize: 9, letterSpacing: 2, marginBottom: 20 }}>
                (2n+1)² − 4·gₙ² = 1 · EXACT PELL IDENTITY · HYPERBOLA x²−y²=¼
            </div>

            {/* Controls */}
            <div style={{ display: "flex", gap: 16, marginBottom: 16, flexWrap: "wrap", justifyContent: "center" }}>
                {(
                    [
                        ["Hyperbola", showHyperbola, setShowHyperbola, "#00ffee"],
                        ["Perfect Squares", showSquares, setShowSquares, "#ff5533"],
                        ["Bridge Δ", showBridge, setShowBridge, "#ffaa44"],
                    ] as [string, boolean, (v: boolean) => void, string][]
                ).map(([label, val, set, col]) => (
                    <button key={label} onClick={() => set(!val)} style={{
                        background: val ? col + "18" : "transparent",
                        border: `1px solid ${val ? col : "#0d1f2d"}`,
                        color: val ? col : "#1a3040", padding: "5px 14px",
                        fontSize: 9, letterSpacing: 2, cursor: "pointer", outline: "none",
                        fontFamily: "'Courier New', monospace",
                    }}>{label}</button>
                ))}
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                    <span style={{ color: "#1a3040", fontSize: 9 }}>n START</span>
                    <input type="range" min={1} max={90} value={nStart}
                        onChange={e => setNStart(+e.target.value)}
                        style={{ width: 80, accentColor: "#00ffee" }} />
                    <span style={{ color: "#00ffee", fontSize: 11 }}>{nStart}</span>
                </div>
            </div>

            {/* SVG Canvas */}
            <svg width={W} height={H} style={{ background: "#050a10", border: "1px solid #0d1f2d", display: "block" }}>

                {/* Grid */}
                {intLines.map(n => (
                    <g key={n}>
                        <line x1={PAD} x2={W - PAD}
                            y1={ty(n, yMin, yMax)} y2={ty(n, yMin, yMax)}
                            stroke="#0a1a28" strokeWidth={1} />
                        <line x1={tx(n, xMin, xMax)} x2={tx(n, xMin, xMax)}
                            y1={PAD} y2={H - PAD}
                            stroke="#0a1a28" strokeWidth={1} />
                        <text x={tx(n, xMin, xMax)} y={H - PAD + 14}
                            fill="#1a3040" fontSize={8} textAnchor="middle">{n}</text>
                        <text x={PAD - 8} y={ty(n, yMin, yMax) + 4}
                            fill="#1a3040" fontSize={8} textAnchor="end">{n}</text>
                    </g>
                ))}

                {/* Perfect square markers: y = n+1 (integer child target) */}
                {showSquares && nodes.map(({ n, sq }) => (
                    <circle key={`sq-${n}`}
                        cx={tx(n + 0.5, xMin, xMax)} cy={ty(sq, yMin, yMax)}
                        r={3} fill="none" stroke="#ff5533" strokeWidth={1} opacity={0.5} />
                ))}

                {/* Hyperbola x²-y²=1/4 */}
                {showHyperbola && hyperPath && (
                    <path d={hyperPath} fill="none" stroke="#00ffee" strokeWidth={1.5} opacity={0.4} />
                )}

                {/* For each node: arithmetic mean point, bridge line, gₙ point */}
                {nodes.map(({ n, g, arith }) => {
                    const gx = tx(n + 0.5, xMin, xMax);
                    const gy = ty(g, yMin, yMax);
                    const ay = ty(arith, yMin, yMax);
                    const isH = hovered === n;
                    return (
                        <g key={n}>
                            {/* Bridge gap line: gₙ to arith mean */}
                            {showBridge && (
                                <line x1={gx} x2={gx} y1={gy} y2={ay}
                                    stroke="#ffaa44" strokeWidth={isH ? 2 : 1}
                                    strokeDasharray="3,2" opacity={0.6} />
                            )}
                            {/* Arithmetic mean (n+0.5) */}
                            <circle cx={gx} cy={ay} r={2}
                                fill="#ffaa44" opacity={0.4} />
                            {/* gₙ = √(n(n+1)) on hyperbola */}
                            <circle cx={gx} cy={gy} r={isH ? 7 : 4}
                                fill={isH ? "#00ffee" : "#004455"}
                                stroke="#00ffee" strokeWidth={isH ? 2 : 1}
                                style={{ cursor: "pointer", transition: "all 0.1s" }}
                                onMouseEnter={() => setHovered(n)}
                                onMouseLeave={() => setHovered(null)} />
                            {/* Label */}
                            <text x={gx + 8} y={gy - 6} fill="#00ffee" fontSize={8} opacity={isH ? 1 : 0.4}>
                                g{n}
                            </text>
                        </g>
                    );
                })}

                {/* Axis labels */}
                <text x={W / 2} y={H - 8} fill="#1a3040" fontSize={9} textAnchor="middle">
                    x = n + ½  (arithmetic midpoint axis)
                </text>
                <text x={14} y={H / 2} fill="#1a3040" fontSize={9} textAnchor="middle"
                    transform={`rotate(-90, 14, ${H / 2})`}>y = gₙ (geometric mean)</text>

                {/* Pell label */}
                <text x={W - PAD - 4} y={PAD + 14} fill="#00ffee" fontSize={8.5}
                    textAnchor="end" opacity={0.5}>
                    x² − y² = ¼
                </text>
            </svg>

            {/* Hover detail */}
            <div style={{
                marginTop: 12, padding: "12px 20px", background: "#050a10",
                border: `1px solid ${hovered != null ? "#00ffee33" : "#0d1f2d"}`,
                minWidth: 460, transition: "border-color 0.3s"
            }}>
                {hovered != null ? (() => {
                    const n = hovered;
                    const g = gn(n), d = delta(n);
                    const pellL = (2 * n + 1) * (2 * n + 1), pellR = 4 * g * g;
                    return (
                        <div style={{ fontSize: 10, lineHeight: 1.9 }}>
                            <div style={{ color: "#00ffee", fontWeight: "bold", marginBottom: 6 }}>
                                ◈ NODE n = {n}
                            </div>
                            <div><span style={{ color: "#1a4055" }}>Parent:         </span>{n}</div>
                            <div><span style={{ color: "#1a4055" }}>Child:          </span>{n + 1}</div>
                            <div><span style={{ color: "#1a4055" }}>gₙ = √(n·n+1):  </span>
                                <span style={{ color: "#00ffee" }}>{fmtNum(g)}</span></div>
                            <div><span style={{ color: "#1a4055" }}>Arith mean n+½: </span>{n + 0.5}</div>
                            <div><span style={{ color: "#1a4055" }}>δₙ = ½ − gₙ:   </span>
                                <span style={{ color: "#ffaa44" }}>{fmtNum(d)}</span>
                                <span style={{ color: "#1a4055" }}> ≈ 1/8n = {fmtNum(1 / (8 * n))}</span>
                            </div>
                            <div><span style={{ color: "#1a4055" }}>Pell check:     </span>
                                <span style={{ color: "#ff5533" }}>(2n+1)² </span>= {pellL} · <span style={{ color: "#00ffee" }}>4gₙ²</span> = {fmtNum(pellR)} · diff = {fmtNum(pellL - pellR)}
                            </div>
                            <div><span style={{ color: "#1a4055" }}>Near-sq gap:    </span>
                                (n+1)² − gₙ² = {(n + 1) * (n + 1)} − {fmtNum(g * g)} = {fmtNum((n + 1) * (n + 1) - g * g)}
                            </div>
                            <div><span style={{ color: "#1a4055" }}>Anim frame ~:   </span>
                                frame {Math.round(120 * (g - n))} / 120 (at 120 fps per node)
                            </div>
                        </div>
                    );
                })() : (
                    <div style={{ color: "#1a3040", fontSize: 10, textAlign: "center", padding: "8px 0" }}>
                        hover a cyan node to inspect
                    </div>
                )}
            </div>

            {/* Cascade table */}
            <div style={{ marginTop: 16, width: W, overflowX: "auto" }}>
                <div style={{ color: "#1a3040", fontSize: 8, letterSpacing: 3, marginBottom: 8 }}>
                    CASCADE TABLE — FIRST {N} NODES FROM n={nStart}
                </div>
                <table style={{ width: "100%", fontSize: 9, borderCollapse: "collapse" }}>
                    <thead>
                        <tr>
                            {["n", "gₙ", "arith n+½", "δ = ½−gₙ", "≈ 1/8n", "Pell: (2n+1)²−4gₙ²"].map(h => (
                                <th key={h} style={{
                                    color: "#1a4055", padding: "4px 8px",
                                    borderBottom: "1px solid #0d1f2d", textAlign: "right"
                                }}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {nodes.map(({ n, g, arith, d }) => {
                            const pell = (2 * n + 1) * (2 * n + 1) - 4 * g * g;
                            const isH = hovered === n;
                            return (
                                <tr key={n}
                                    onMouseEnter={() => setHovered(n)}
                                    onMouseLeave={() => setHovered(null)}
                                    style={{ background: isH ? "#00ffee08" : "transparent", cursor: "pointer" }}>
                                    <td style={{ color: isH ? "#00ffee" : "#1a4055", padding: "3px 8px", textAlign: "right" }}>{n}</td>
                                    <td style={{ color: isH ? "#00ffee" : "#2a6070", padding: "3px 8px", textAlign: "right" }}>{g.toFixed(6)}</td>
                                    <td style={{ color: "#1a4055", padding: "3px 8px", textAlign: "right" }}>{arith.toFixed(1)}</td>
                                    <td style={{ color: isH ? "#ffaa44" : "#1a3040", padding: "3px 8px", textAlign: "right" }}>{d.toFixed(6)}</td>
                                    <td style={{ color: "#1a3040", padding: "3px 8px", textAlign: "right" }}>{(1 / (8 * n)).toFixed(6)}</td>
                                    <td style={{ color: isH ? "#ff5533" : "#1a3040", padding: "3px 8px", textAlign: "right" }}>
                                        {pell.toFixed(8)} ✓
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>

            <div style={{ marginTop: 16, color: "#1a3040", fontSize: 8, letterSpacing: 2, textAlign: "center" }}>
                ◈ drag n START slider to walk the cascade · hover nodes for detail ◈
            </div>
        </div>
    );
}
