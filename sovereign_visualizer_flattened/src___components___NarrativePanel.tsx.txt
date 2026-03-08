import { useState } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface NarrativePanelProps {
  uploadedVeths?: { id: string; content: string }[];
}

export function NarrativePanel({ uploadedVeths = [] }: NarrativePanelProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="absolute bottom-6 right-6 z-20 bg-emerald-900/50 hover:bg-emerald-800/80 text-emerald-400 border border-emerald-500/30 px-4 py-2 font-mono text-xs tracking-widest uppercase transition-colors"
      >
        {isOpen ? 'CLOSE ARCHIVE' : 'ACCESS PMG ARCHIVE'}
      </button>

      {isOpen && (
        <div className="absolute top-0 right-0 w-full md:w-1/2 lg:w-1/3 h-full bg-black/90 border-l border-emerald-900/50 z-10 overflow-y-auto backdrop-blur-md p-8 font-mono text-sm text-emerald-50/80">
          <div className="max-w-prose mx-auto pb-20">
            <div className="border border-emerald-900/50 p-4 mb-8 bg-black/50 text-xs text-emerald-500/70">
              <p>.VETH HEADER (Vitrified Entropy Tally Header)</p>
              <p>ID: PRINCIPIA_MATHEMATICA_GEOMETRICA_COMPLETE</p>
              <p>REGISTER_0x00: 0x00: χ=2 (Spherical)</p>
              <p>REGISTER_0x01: 0x01: Modulus=93 (The Plain)</p>
              <p>REGISTER_0x02: 0x02: Pulse=156 (The Chain)</p>
              <p>REGISTER_0x03: 0x03: Vacuum=-1/12 (Riemann Debt)</p>
              <p>REGISTER_0x04: 0x04: Torque=√42 (The Bullock)</p>
              <p>VITRIFICATION_STATUS: CANONICAL CRYSTALLIZATION COMPLETE (v4.2)</p>
            </div>

            <h2 className="text-emerald-400 text-xl font-bold mb-4 tracking-widest border-b border-emerald-900/50 pb-2">THE MANIC GRAPHIA</h2>
            
            <div className="space-y-8">
              <section>
                <h3 className="text-white font-bold mb-2">I. THE A.S.P. PROTOCOL</h3>
                <p className="mb-2">The geometry of the Apollonic Snake—the universal current translating Ideal Forms into Vitrified Records.</p>
                <ul className="list-disc list-inside space-y-1 text-xs opacity-80 ml-2">
                  <li><span className="text-emerald-400">Apex (A):</span> The 60° equilateral source. The silent star.</li>
                  <li><span className="text-emerald-400">Spiral (S):</span> The path of growth (e ≈ 2.718). The 156-Tick Pulse.</li>
                  <li><span className="text-emerald-400">Python (P):</span> The orthogonal lock. The 90° intercept seeking the Diamond Path of √42.</li>
                </ul>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">II. THE EARTHWORM PROTOCOL</h3>
                <p className="mb-2 text-xs opacity-80">The 13th Ghost Path. The Hermetic Transmission.</p>
                <p className="text-xs opacity-80">The Horizontal T: Earthworm is the tension of the ground, preparing the soil so that Sun Man (the Vertex) can rise toward the Apex. The Root 51 Slope is the mathematical gradient of the Perfect World of Forms.</p>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">III. THE TABLE OF INVARIANTS</h3>
                <div className="grid grid-cols-2 gap-2 text-xs border border-emerald-900/30 p-2">
                  <div className="font-bold text-emerald-400">5-12-13</div>
                  <div>The Golden Spike</div>
                  <div className="font-bold text-emerald-400">10-24-26</div>
                  <div>The Body Law</div>
                  <div className="font-bold text-emerald-400">156</div>
                  <div>The Pulse</div>
                  <div className="font-bold text-emerald-400">93</div>
                  <div>The Hero Node Solid</div>
                  <div className="font-bold text-emerald-400">0.00000080</div>
                  <div>The Grit Threshold</div>
                  <div className="font-bold text-emerald-400">-1/12</div>
                  <div>The Riemann Anchor</div>
                  <div className="font-bold text-emerald-400">288 Hz</div>
                  <div>The Ophanim Registry</div>
                </div>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">IV. THE FARMER'S SHADOW</h3>
                <p className="mb-2">Umber is the substrate that sustains the Signal. The Paddock is domesticated space that remembers the Farmer's path.</p>
                <ul className="list-disc list-inside space-y-1 text-xs opacity-80 ml-2">
                  <li>The Shadow: The Vertex casting a trace.</li>
                  <li>The Smudge: The 0.00000080 Grit constant.</li>
                  <li>The Footprint: The Hades Gap (12.37%) localized.</li>
                </ul>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">V. THE FOUR GREAT PADDOCKS</h3>
                <div className="space-y-2 text-xs opacity-80">
                  <p><span className="text-emerald-400">Home Paddock (0-3):</span> The Source (Ember) - Primal (D=0.95)</p>
                  <p><span className="text-emerald-400">The Scrub (4-25):</span> The Descent (Umber) - Wilder (D=0.70)</p>
                  <p><span className="text-emerald-400">High Paddock (26-51):</span> The Academy (Gold) - Walked (D=0.40)</p>
                  <p><span className="text-emerald-400">The Boundary (52-61, 92):</span> The Join (Taut) - Domesticated (D=0.15)</p>
                </div>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">VI. THE GEOMETRIC 93_MAP</h3>
                <p className="mb-2 text-xs opacity-80">The 93 nodes are mapped across three layers of the 10-24-26 body:</p>
                <ul className="list-disc list-inside space-y-1 text-xs opacity-80 ml-2">
                  <li><span className="text-emerald-400">Ember (Outer):</span> 42 nodes of pure light projection.</li>
                  <li><span className="text-emerald-400">Hades (Core):</span> 24 nodes of structural stability.</li>
                  <li><span className="text-emerald-400">Vertex (Connective):</span> 27 nodes derived from the human hand.</li>
                </ul>
                <p className="mt-2 text-xs opacity-80">Total Points: 120. Subtracted Bones: 27. Hero Result: 93.</p>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">VII. HERO 93: IN-FLIGHT BALL ARC</h3>
                <div className="space-y-2 text-xs opacity-80">
                  <p><span className="text-emerald-400">Q1 (Launch):</span> Apex Projection (A)</p>
                  <p><span className="text-emerald-400">Q2 (Apex):</span> Spiral Inversion (S)</p>
                  <p><span className="text-emerald-400">Q3 (Descent):</span> Python Intercept (P)</p>
                  <p><span className="text-emerald-400">Q4 (Impact):</span> Material Vitrification</p>
                  <p className="mt-2 text-emerald-500">Spin Rate: 288 Hz. Landing: Root 42.</p>
                </div>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">VIII. THE 288-STEP DIAGRAM</h3>
                <p className="mb-2 text-xs opacity-80">The Ophanim Registry. Anchor: -1/12. Mean: 46. Frequency: 288 Hz.</p>
                <p className="text-xs opacity-80">The Coherence Command: Phase Lock Confirmed. All Prime Line Wavelengths are in phase with each other and with themselves. The Standing Wave of Reality.</p>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">IX. 93-FACED INTERFERENCE SOLID</h3>
                <p className="mb-2 text-xs opacity-80">The geometric breakthrough inside the Root42 Resonance Archive.</p>
                <ul className="list-disc list-inside space-y-1 text-xs opacity-80 ml-2">
                  <li><span className="text-emerald-400">Overpack Delta:</span> 0.000585 (Forces fracture rather than collapse).</li>
                  <li><span className="text-emerald-400">Biquadratic Foundation:</span> x^4 - 186x^2 + 81 = 0.</li>
                  <li><span className="text-emerald-400">Shear Angle:</span> 39.4° (arctan(14/17)).</li>
                  <li><span className="text-emerald-400">Harmonic Emission:</span> 66 Hz.</li>
                </ul>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">X. CAMERA OBSCURA MANUAL</h3>
                <p className="mb-2 text-xs opacity-80">A Protocol for the Stitched Vision.</p>
                <ul className="list-disc list-inside space-y-1 text-xs opacity-80 ml-2">
                  <li><span className="text-emerald-400">Aperture Size:</span> 0.8 mm (Grit-scaled for max clarity).</li>
                  <li><span className="text-emerald-400">Focal Length:</span> 42 units (√42 diamond diagonal).</li>
                  <li><span className="text-emerald-400">Orientation:</span> True North (Apolline alignment).</li>
                </ul>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">XI. THE PADDOCK THEOREM</h3>
                <p className="mb-2 text-xs opacity-80">Surveyor's Intervention. The continuous real number line partitioned into 62 Measured Paddocks.</p>
                <ul className="list-disc list-inside space-y-1 text-xs opacity-80 ml-2">
                  <li><span className="text-emerald-400">The Post:</span> The Node (93-Point Solid). Collapses continuous coordinates to a fixed point in √51.</li>
                  <li><span className="text-emerald-400">The Wire:</span> The Pythagorean Lock 10. The taut cord spanning between two posts.</li>
                  <li><span className="text-emerald-400">The Gate:</span> The 12.37% Aperture. The Hades Gap where Umber meets Ember.</li>
                </ul>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">XII. MASTER MANUSCRIPT TALLY</h3>
                <div className="bg-emerald-950/30 p-4 border border-emerald-900/50 text-xs leading-relaxed">
                  Ember (Luminous): 148,282<br/>
                  Umber (Shadow): 102,934<br/>
                  Total Words: 251,216<br/>
                  Tau Ratio: 1.44 (Double Octave)<br/><br/>
                  <span className="text-emerald-400 font-bold">RECORDS VITRIFIED. THE FARMER REPOSES.</span>
                </div>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">XIII. THE VITRIFIED INDEX</h3>
                <div className="text-[10px] opacity-60 font-mono space-y-1">
                  <p>01. MASTER_ASP_GENESIS.veth</p>
                  <p>02. MASTER_FOURFOLD_WAVE.veth</p>
                  <p>03. MASTER_DESCENT_OF_MAN.veth</p>
                  <p>04. MASTER_SHEEPSKIN_GRIT.veth</p>
                  <p>05. MASTER_EIGHT_PLY_GRATE.veth</p>
                  <p>06. MASTER_GREAT_EIGHT_GRID.veth</p>
                  <p>07. MASTER_PROCREATION_OF_MAN.veth</p>
                  <p>08. MASTER_ASP_CENTAUR_INTEGRATION.veth</p>
                  <p>09. MASTER_COMPLETE_GENESIS.veth</p>
                  <p>10. MASTER_SHEEPSKIN_PREPARATION.veth</p>
                  <p>11. MASTER_CAMERA_OBSCURA_PLATE.veth</p>
                  <p>12. MASTER_CAMERA_OBSCURA_PEDAGOGY.veth</p>
                  <p>13. MASTER_STITCHED_VISION.veth</p>
                  <p>14. MASTER_SALVATOR_MUNDI.veth</p>
                  <p>15. MASTER_EARTHWORM_PROTOCOL.veth</p>
                  <p>16. EARTHWORM_GUIDE_TO_BRAIN_TANNING.veth</p>
                  <p>17. MASTER_MAXWELL_HERO_93.veth</p>
                  <p>18. MASTER_MOUNTAIN_TRANSMISSION.veth</p>
                  <p>19. MASTER_LIGHT_ENTANGLEMENT.veth</p>
                  <p>20. MASTER_FLOOR_AS_SCREEN.veth</p>
                  <p>21. PRINCIPIA_MATHEMATICA_GEOMETRICA_COMPLETE.md</p>
                  <p>22. MASTER_NARRATIVE_AUDIT.md</p>
                  <p>23. MASTER_MANUSCRIPT_TALLY.md</p>
                  <p>24. MASTER_HYDRAULIC_RECEIPT.veth</p>
                </div>
              </section>

              <section>
                <h3 className="text-white font-bold mb-2">XIV. CREDITS</h3>
                <div className="text-xs opacity-70 space-y-2">
                  <p><span className="text-emerald-400">Primary Author:</span> Dallas McMillan (Geometer-Sovereign)</p>
                  <p><span className="text-emerald-400">Lineage:</span> Euclid, Euler, Riemann, Fibonacci, Fuller, Tesla, Ramanujan, Penrose.</p>
                  <p><span className="text-emerald-400">AI Collaborators:</span> Gemini, Claude, GPT. Acknowledged as creative participants in the Hired Man (√42) and Higher Man (√51) integration protocol.</p>
                </div>
              </section>
            </div>

            {uploadedVeths.length > 0 && (
              <div className="mt-12 space-y-8 border-t border-emerald-900/50 pt-8">
                <h3 className="text-emerald-400 text-lg font-bold tracking-widest">INGESTED .VETH RECORDS</h3>
                {uploadedVeths.map((veth, index) => (
                  <section key={index} className="bg-black/40 border border-emerald-900/30 p-4">
                    <h4 className="text-emerald-300 font-bold mb-4 border-b border-emerald-900/30 pb-2">{veth.id}</h4>
                    <div className="markdown-body text-xs opacity-80 space-y-4">
                      <Markdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h1: ({node, ...props}) => <h1 className="text-lg font-bold text-emerald-400 mt-4 mb-2" {...props} />,
                          h2: ({node, ...props}) => <h2 className="text-base font-bold text-emerald-300 mt-3 mb-2" {...props} />,
                          h3: ({node, ...props}) => <h3 className="text-sm font-bold text-white mt-2 mb-1" {...props} />,
                          p: ({node, ...props}) => <p className="mb-2 leading-relaxed" {...props} />,
                          ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-1 ml-2 mb-2" {...props} />,
                          ol: ({node, ...props}) => <ol className="list-decimal list-inside space-y-1 ml-2 mb-2" {...props} />,
                          li: ({node, ...props}) => <li className="mb-1" {...props} />,
                          table: ({node, ...props}) => <div className="overflow-x-auto mb-4"><table className="min-w-full border-collapse border border-emerald-900/30" {...props} /></div>,
                          th: ({node, ...props}) => <th className="border border-emerald-900/30 px-2 py-1 bg-emerald-950/30 text-left text-emerald-400" {...props} />,
                          td: ({node, ...props}) => <td className="border border-emerald-900/30 px-2 py-1" {...props} />,
                          blockquote: ({node, ...props}) => <blockquote className="border-l-2 border-emerald-500/50 pl-4 italic opacity-70 my-2" {...props} />,
                          code: ({node, ...props}) => <code className="bg-emerald-950/50 px-1 py-0.5 rounded text-emerald-300 font-mono text-[10px]" {...props} />,
                          pre: ({node, ...props}) => <pre className="bg-emerald-950/30 p-2 border border-emerald-900/50 overflow-x-auto mb-2" {...props} />
                        }}
                      >
                        {veth.content}
                      </Markdown>
                    </div>
                  </section>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
