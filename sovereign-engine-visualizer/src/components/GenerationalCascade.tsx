import { useState, useEffect, useRef } from "react";

const EK = 0.037;
const REGISTRY = 288;
const N_START = 93;
const N_GEN = 12;

function gn(n: number) { return Math.sqrt(n * (n + 1)); }
function delta(n: number) { return (n + 0.5) - gn(n); }

// 12 generations across 288 ticks → 24 ticks each
const TICKS_PER_GEN = REGISTRY / N_GEN; // 24

function genToTick(genIdx: number, frac: number) {
    return genIdx * TICKS_PER_GEN + frac * TICKS_PER_GEN;
}

interface GenData {
    n: number; g: number; d: number; bridgeFrac: number;
    parentTick: number; bridgeTick: number; arithTick: number; childTick: number;
    pell: number; errApprox: number;
}

const GENERATIONS: GenData[] = Array.from({ length: N_GEN }, (_, i) => {
    const n = N_START + i;
    const g = gn(n);
    const d = delta(n);
    const bridgeFrac = g - n;
    const parentTick = genToTick(i, 0);
    const bridgeTick = genToTick(i, bridgeFrac);
    const arithTick = genToTick(i, 0.5);
    const childTick = genToTick(i, 1.0);
    const pell = (2 * n + 1) * (2 * n + 1) - 4 * g * g;
    return {
        n, g, d, bridgeFrac, parentTick, bridgeTick, arithTick, childTick, pell,
        errApprox: 1 / (8 * n)
    };
});

const W = 760, H_TIMELINE = 220, H_DETAIL = 200, PAD = 44;
const TW = W - PAD * 2;

function tickX(tick: number) { return PAD + (tick / REGISTRY) * TW; }

export default function GenerationalCascade() {
    const [t, setT] = useState(0);
    const [hovered, setHovered] = useState<number | null>(null);
    const [playing, setPlaying] = useState(true);
    const [showArith, setShowArith] = useState(true);
    const [showError, setShowError] = useState(true);
    const [showPell, setShowPell] = useState(false);
    const rafRef = useRef<number>(0);
    const t0Ref = useRef<number | null>(null);

    useEffect(() => {
        if (!playing) { cancelAnimationFrame(rafRef.current); return; }
        const animate = (ts: number) => {
            if (!t0Ref.current) t0Ref.current = ts;
            setT(((ts - t0Ref.current) / 1000 * EK * 12) % 1);
            rafRef.current = requestAnimationFrame(animate);
        };
        rafRef.current = requestAnimationFrame(animate);
        return () => cancelAnimationFrame(rafRef.current);
    }, [playing]);

    function pulse(genIdx: number) {
        const phase = (t + genIdx / N_GEN) % 1;
        return 0.4 + 0.6 * Math.sin(phase * Math.PI * 2);
    }

    const hGen = hovered != null ? GENERATIONS[hovered] : null;

    return (
        <div style={{
            background: "#06090f", minHeight: "100vh", color: "#c8d8e8",
            fontFamily: "'Courier New',monospace", padding: "20px",
            display: "flex", flexDirection: "column", alignItems: "center"
        }}>
            <div style={{ color: "#1a3040", fontSize: 8, letterSpacing: 5, marginBottom: 4 }}>
                SOVEREIGN ENGINE · GENERATIONAL CASCADE · 288-TICK REGISTRY
            </div>
            <div style={{ color: "#00ffee", fontSize: 17, fontWeight: "bold", letterSpacing: 3, marginBottom: 2 }}>
                ☙ 12-GENERATION INHERITANCE MAP
            </div>
            <div style={{ color: "#1a4055", fontSize: 8, letterSpacing: 2, marginBottom: 14 }}>
                n = 93…104 · g_n = √(n·(n+1)) · (2n+1)²−4g_n²=1 · δ_n ≈ 1/8n
            </div>

            {/* Controls */}
            <div style={{ display: "flex", gap: 10, marginBottom: 14, flexWrap: "wrap", justifyContent: "center" }}>
                {(
                    [
                        ["▶ PLAY / PAUSE", () => { setPlaying(p => !p); t0Ref.current = null; }, playing ? "#00ffee" : "#1a3040", playing ? "#00ffee22" : "transparent"],
                        ["Arith Mean", () => setShowArith(v => !v), showArith ? "#ffaa44" : "#1a3040", showArith ? "#ffaa4422" : "transparent"],
                        ["Error δₙ", () => setShowError(v => !v), showError ? "#ff7733" : "#1a3040", showError ? "#ff773322" : "transparent"],
                        ["Pell = 1", () => setShowPell(v => !v), showPell ? "#cc44ff" : "#1a3040", showPell ? "#cc44ff22" : "transparent"],
                    ] as [string, () => void, string, string][]
                ).map(([label, fn, col, bg]) => (
                    <button key={label} onClick={fn} style={{
                        background: bg, border: `1px solid ${col}`, color: col,
                        padding: "5px 13px", fontSize: 8, letterSpacing: 2,
                        cursor: "pointer", outline: "none", fontFamily: "'Courier New',monospace",
                        transition: "all .2s"
                    }}>{label}</button>
                ))}
            </div>

            {/* TIMELINE SVG */}
            <svg width={W} height={H_TIMELINE} style={{ background: "#040710", border: "1px solid #0a1a28", display: "block" }}>

                {/* Ghost Path zone (ticks 276–288) */}
                <rect x={tickX(276)} y={0} width={tickX(288) - tickX(276)} height={H_TIMELINE}
                    fill="#00ffee" opacity={0.025} />
                <text x={tickX(282)} y={14} fill="#00ffee" fontSize={7} textAnchor="middle" opacity={0.3}>
                    GHOST PATH
                </text>

                {/* Tick marks every 24 */}
                {Array.from({ length: 13 }, (_, i) => (
                    <g key={i}>
                        <line x1={tickX(i * 24)} x2={tickX(i * 24)} y1={H_TIMELINE - 20} y2={H_TIMELINE - 12}
                            stroke="#1a3040" strokeWidth={1} />
                        <text x={tickX(i * 24)} y={H_TIMELINE - 4} fill="#1a3040" fontSize={7} textAnchor="middle">
                            {i * 24}
                        </text>
                        {i < N_GEN && (
                            <text x={tickX(i * 24 + 12)} y={24} fill="#0d2030" fontSize={7} textAnchor="middle">
                                n={N_START + i}
                            </text>
                        )}
                    </g>
                ))}

                {/* Generation lane separators */}
                {GENERATIONS.map(({ parentTick }, i) => (
                    <line key={i} x1={tickX(parentTick)} x2={tickX(parentTick)}
                        y1={28} y2={H_TIMELINE - 24} stroke="#0a1a28" strokeWidth={1} />
                ))}

                {/* Per generation */}
                {GENERATIONS.map((gen, i) => {
                    const { n, g, d, bridgeTick, arithTick, childTick, parentTick, errApprox } = gen;
                    const px = tickX(parentTick);
                    const bx = tickX(bridgeTick);
                    const ax = tickX(arithTick);
                    const cx = tickX(childTick);
                    const p = pulse(i);
                    const isH = hovered === i;
                    const cy_main = 110;
                    const cy_err = 70;

                    return (
                        <g key={i} style={{ cursor: "pointer" }}
                            onMouseEnter={() => setHovered(i)} onMouseLeave={() => setHovered(null)}>

                            {isH && <rect x={px} width={cx - px} y={28} height={H_TIMELINE - 52}
                                fill="#00ffee" opacity={0.04} />}

                            <line x1={px} x2={cx} y1={cy_main} y2={cy_main}
                                stroke={isH ? "#1a3040" : "#0a1a28"} strokeWidth={1} />

                            {showError && (
                                <>
                                    <line x1={bx} x2={ax} y1={cy_err} y2={cy_err}
                                        stroke="#ff7733" strokeWidth={isH ? 2 : 1} strokeDasharray="2,2" opacity={0.7} />
                                    <text x={(bx + ax) / 2} y={cy_err - 5} fill="#ff7733"
                                        fontSize={6.5} textAnchor="middle" opacity={0.8}>
                                        δ={d.toFixed(5)}
                                    </text>
                                </>
                            )}

                            {showArith && (
                                <>
                                    <line x1={ax} x2={ax} y1={cy_main - 8} y2={cy_main + 8}
                                        stroke="#ffaa44" strokeWidth={1} opacity={0.5} />
                                    <circle cx={ax} cy={cy_main} r={2} fill="#ffaa44" opacity={0.4} />
                                </>
                            )}

                            <circle cx={bx} cy={cy_main} r={10 + p * 6}
                                fill="none" stroke="#00ffee" strokeWidth={1}
                                opacity={p * (isH ? 0.6 : 0.25)} />
                            <circle cx={bx} cy={cy_main} r={5 + p * 2}
                                fill="none" stroke="#00ffee" strokeWidth={1.5}
                                opacity={p * (isH ? 0.9 : 0.5)} />

                            <circle cx={px} cy={cy_main} r={isH ? 6 : 4}
                                fill="#2a1040" stroke="#aa44ff" strokeWidth={1.5} opacity={0.9} />
                            <text x={px} y={cy_main + 18} fill="#aa44ff"
                                fontSize={7} textAnchor="middle">{n}</text>

                            <circle cx={cx} cy={cy_main} r={isH ? 5 : 3}
                                fill="#400810" stroke="#ff3311" strokeWidth={1.5}
                                opacity={0.3 + p * 0.6} />
                            <text x={cx} y={cy_main + 18} fill="#ff5533"
                                fontSize={7} textAnchor="middle" opacity={0.3 + p * 0.6}>{n + 1}</text>

                            <circle cx={bx} cy={cy_main} r={isH ? 7 : 4}
                                fill="#003344" stroke="#00ffee" strokeWidth={2}
                                opacity={0.85} />
                            <text x={bx} y={cy_main - 14} fill="#00ffee"
                                fontSize={6.5} textAnchor="middle" opacity={isH ? 1 : 0.5}>
                                {g.toFixed(4)}
                            </text>

                            {showPell && (
                                <text x={bx} y={cy_main + 32} fill="#cc44ff"
                                    fontSize={6} textAnchor="middle" opacity={0.7}>
                                    Pell≡1
                                </text>
                            )}

                            {isH && showError && (
                                <text x={(bx + ax) / 2} y={cy_err - 15} fill="#ff7733" fontSize={6.5} textAnchor="middle">
                                    ≈1/8n={errApprox.toFixed(5)}
                                </text>
                            )}
                        </g>
                    );
                })}

                <text x={PAD} y={H_TIMELINE - 34} fill="#1a3040" fontSize={7}>TICK 0 — ENTRY</text>
                <text x={W - PAD - 4} y={H_TIMELINE - 34} fill="#00ffee" fontSize={7} textAnchor="end" opacity={0.5}>
                    TICK 288 — ARCHIVE
                </text>

                {(
                    [
                        [30, 45, "#aa44ff", "Parent n"],
                        [30, 58, "#00ffee", "Bridge gₙ"],
                        showArith ? [30, 71, "#ffaa44", "Arith n+½"] : null,
                        showError ? [30, 84, "#ff7733", "Error δₙ"] : null,
                    ].filter(Boolean) as [number, number, string, string][]
                ).map(([x, y, col, label]) => (
                    <g key={label}>
                        <circle cx={x + 4} cy={y - 3} r={3} fill={col} opacity={0.7} />
                        <text x={x + 12} y={y} fill={col} fontSize={7} opacity={0.7}>{label}</text>
                    </g>
                ))}
            </svg>

            {/* DETAIL PANEL */}
            <div style={{
                marginTop: 8, width: W, background: "#040710",
                border: `1px solid ${hGen ? "#00ffee33" : "#0a1a28"}`,
                padding: "14px 20px", transition: "border-color .3s"
            }}>
                {hGen ? (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px 24px", fontSize: 10 }}>
                        <div>
                            <div style={{ color: "#1a4055", fontSize: 8, letterSpacing: 2, marginBottom: 4 }}>GENERATION</div>
                            <div style={{ color: "#00ffee", fontSize: 14, fontWeight: "bold" }}>n = {hGen.n}</div>
                            <div style={{ color: "#1a3040", marginTop: 3 }}>Parent tick: {hGen.parentTick.toFixed(2)}</div>
                            <div style={{ color: "#1a3040" }}>Child tick: {hGen.childTick.toFixed(2)}</div>
                        </div>
                        <div>
                            <div style={{ color: "#1a4055", fontSize: 8, letterSpacing: 2, marginBottom: 4 }}>BRIDGE VALUES</div>
                            <div><span style={{ color: "#1a4055" }}>gₙ = √(n·n+1):  </span>
                                <span style={{ color: "#00ffee" }}>{hGen.g.toFixed(8)}</span></div>
                            <div><span style={{ color: "#1a4055" }}>arith n+½:       </span>
                                <span style={{ color: "#ffaa44" }}>{(hGen.n + 0.5).toFixed(1)}</span></div>
                            <div><span style={{ color: "#1a4055" }}>δₙ = ½−gₙ:      </span>
                                <span style={{ color: "#ff7733" }}>{hGen.d.toFixed(8)}</span></div>
                            <div><span style={{ color: "#1a4055" }}>≈ 1/8n:          </span>
                                <span style={{ color: "#ff7733" }}>{hGen.errApprox.toFixed(8)}</span></div>
                        </div>
                        <div>
                            <div style={{ color: "#1a4055", fontSize: 8, letterSpacing: 2, marginBottom: 4 }}>PELL IDENTITY</div>
                            <div><span style={{ color: "#1a4055" }}>(2n+1)²:         </span>
                                <span style={{ color: "#cc44ff" }}>{(2 * hGen.n + 1) ** 2}</span></div>
                            <div><span style={{ color: "#1a4055" }}>4·gₙ²:           </span>
                                <span style={{ color: "#cc44ff" }}>{(4 * hGen.g * hGen.g).toFixed(6)}</span></div>
                            <div><span style={{ color: "#1a4055" }}>diff (→ 1):      </span>
                                <span style={{ color: "#00ffee" }}>{hGen.pell.toFixed(8)} ✓</span></div>
                            <div><span style={{ color: "#1a4055" }}>bridge tick:     </span>
                                <span style={{ color: "#00ffee" }}>{hGen.bridgeTick.toFixed(4)}</span></div>
                        </div>
                    </div>
                ) : (
                    <div style={{ color: "#1a3040", fontSize: 10, textAlign: "center", padding: "8px 0" }}>
                        hover a generation to inspect · each lane = 24 ticks · bridge at gₙ ≈ n + ½ − 1/8n
                    </div>
                )}
            </div>

            {/* ERROR TAPER CHART */}
            <div style={{ marginTop: 8, width: W }}>
                <div style={{ color: "#1a3040", fontSize: 8, letterSpacing: 3, marginBottom: 6 }}>
                    ERROR TAPER  δₙ = ½ − gₙ  (converging toward 0 — the "breathing room")
                </div>
                <svg width={W} height={H_DETAIL} style={{ background: "#040710", border: "1px solid #0a1a28", display: "block" }}>

                    <line x1={PAD} x2={W - PAD} y1={H_DETAIL - 40} y2={H_DETAIL - 40}
                        stroke="#ffaa44" strokeWidth={0.5} strokeDasharray="4,4" opacity={0.3} />
                    <text x={W - PAD + 2} y={H_DETAIL - 37} fill="#ffaa44" fontSize={7} opacity={0.4}>n+½</text>

                    {GENERATIONS.map((gen, i) => {
                        const { d, errApprox, bridgeTick } = gen;
                        const bx = tickX(bridgeTick);
                        const maxErr = 1 / (8 * N_START);
                        const errH = (H_DETAIL - 60) * (d / maxErr);
                        const ey = H_DETAIL - 40 - errH;
                        const p = pulse(i);
                        const isH = hovered === i;

                        return (
                            <g key={i} style={{ cursor: "pointer" }}
                                onMouseEnter={() => setHovered(i)} onMouseLeave={() => setHovered(null)}>
                                <rect x={bx - 5} y={ey} width={10} height={errH}
                                    fill="#ff7733" opacity={isH ? 0.7 : 0.35 + (p * 0.15)} />
                                <circle cx={bx} cy={H_DETAIL - 40 - (H_DETAIL - 60) * (errApprox / maxErr)}
                                    r={2} fill="#ffaa44" opacity={0.6} />
                                {isH && (
                                    <text x={bx} y={ey - 6} fill="#ff7733" fontSize={7} textAnchor="middle">
                                        {d.toFixed(5)}
                                    </text>
                                )}
                            </g>
                        );
                    })}

                    <text x={PAD - 2} y={32} fill="#1a3040" fontSize={7} textAnchor="end">
                        {(1 / (8 * N_START)).toFixed(5)}
                    </text>
                    <text x={PAD - 2} y={H_DETAIL - 37} fill="#1a3040" fontSize={7} textAnchor="end">0</text>
                    <text x={W / 2} y={H_DETAIL - 6} fill="#1a3040" fontSize={7} textAnchor="middle">
                        Registry tick position of gₙ — error shrinks as n→∞ (convergence to half-step)
                    </text>

                    <rect x={PAD + 8} y={14} width={8} height={8} fill="#ff7733" opacity={0.5} />
                    <text x={PAD + 20} y={22} fill="#ff7733" fontSize={7}>actual δₙ</text>
                    <circle cx={PAD + 60} cy={18} r={2.5} fill="#ffaa44" opacity={0.7} />
                    <text x={PAD + 68} y={22} fill="#ffaa44" fontSize={7}>≈ 1/8n</text>
                    <text x={PAD + 116} y={22} fill="#cc44ff" fontSize={7} opacity={0.6}>
                        pulse = {EK} Hz (operating temperature)
                    </text>
                </svg>
            </div>

            <div style={{ marginTop: 10, color: "#1a3040", fontSize: 8, letterSpacing: 2, textAlign: "center" }}>
                ◈ 288 ticks = 12 generations × 24 ticks each · bridge at tick ≈ 12 within each lane ·
                ghost path ticks 276–288 ◈
            </div>
        </div>
    );
}
