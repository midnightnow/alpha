
import React, { useRef, useEffect, useCallback, useImperativeHandle, forwardRef } from 'react';
import { WaveParams, LayerVisibility, ViewState } from '../types';
import { SEPHIROTIC_NODES, HARIC_POINTS, ANATOMICAL_LEVELS } from '../constants';

interface VisualizerProps {
  params: WaveParams;
  layers: LayerVisibility;
  view: ViewState;
  setStats: (stats: string) => void;
  setView: React.Dispatch<React.SetStateAction<ViewState>>;
}

export interface VisualizerHandle {
  takeSnapshot: () => void;
}

// Layer Z-depths for Projection Mode
const LAYER_DEPTHS: Record<string, number> = {
    origin: -22,       
    foundation: 0,     
    hexagonal: 1,      
    earthMoon: 2,      
    triangle: 3,       
    heptagon: 4,        
    primeMod: 5,       
    platonic: 6,       
    sephiroth: 7,      
    harmonic: 8,       
    vitruvian: 9,      
    tetrahedral: 10,
    haric: -2,         // Deeper than foundation
    coreStar: -1       // Deep inside
};

const Visualizer = forwardRef<VisualizerHandle, VisualizerProps>(({ params, layers, view, setStats, setView }, ref) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const requestRef = useRef<number | null>(null);
  // Start time at ~PI/2 relative to default frequency to ensure initial visibility (sin=1)
  const timeRef = useRef<number>(2.8); 
  const isDragging = useRef(false);
  const lastMouse = useRef({ x: 0, y: 0 });
  const mouseButton = useRef<number | null>(null);

  // Expose Snapshot Functionality
  useImperativeHandle(ref, () => ({
    takeSnapshot: () => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        
        // Create a temporary link to download
        const link = document.createElement('a');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        link.download = `mathman-field-capture-${timestamp}.png`;
        link.href = canvas.toDataURL('image/png', 1.0);
        link.click();
    }
  }));

  // Helper to project 3D point to 2D screen
  const project = useCallback((x: number, y: number, z: number, cx: number, cy: number, mm: number, yaw: number, pitch: number) => {
    // Rotation
    const x_r = x * Math.cos(yaw) - z * Math.sin(yaw);
    const z_r = x * Math.sin(yaw) + z * Math.cos(yaw);
    
    // Invert Y for math coords (up is positive) -> canvas coords (down is positive) 
    const y_r = y * Math.cos(pitch) - z_r * Math.sin(pitch);
    const z_rr = y * Math.sin(pitch) + z_r * Math.cos(pitch);

    // Perspective projection
    const f = 800 / (800 + z_rr * mm);
    
    // Map to screen
    return { 
        x: cx + x_r * mm * f, 
        y: cy - y_r * mm * f, 
        z: z_rr,
        scale: f 
    };
  }, []);

  const getLayerZ = (layerKey: string) => {
      if (!params.projectionMode) return 0;
      return (LAYER_DEPTHS[layerKey] || 0) * params.layerSeparation;
  };

  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // High DPI setup
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    // Clear
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, rect.width, rect.height);

    // --- State & Config ---
    const t = timeRef.current;
    const { 
        originSeparation, originCOffset, wavelength, 
        phasePhi, phasePsi, scanHeight, 
        intensityThreshold, waveBrightness, nodalBudget,
        projectionMode, layerSeparation, temporalFrequency
    } = params;

    const zoom = view.zoom * 20; // Pixels per mm
    const cx = rect.width / 2 + view.panX;
    const cy = rect.height / 2 + view.panY + (3.5 * zoom); // Center at feet (0,0 is feet)
    
    // Resonance Lock (Snap to 22.5 deg)
    const rawYaw = view.rotation;
    const snappedYaw = view.resonanceLock ? Math.round(rawYaw / 22.5) * 22.5 : rawYaw;
    
    const yaw = snappedYaw * Math.PI / 180;
    const pitch = view.pitch * Math.PI / 180;

    // Helper for scribing lines
    const scribe = (col: string, wid: number) => { ctx.strokeStyle = col; ctx.lineWidth = wid; };
    const p3d = (x: number, y: number, z: number) => {
        const p = project(x, y, z, cx, cy, zoom, yaw, pitch);
        // Apply Mirror Mode
        if (view.mirror) {
            p.x = cx - (p.x - cx);
        }
        return p;
    };

    // --- DRAW LAYERS ---

    // 0. Projection Rays
    if (projectionMode) {
        const originZ = LAYER_DEPTHS.origin * layerSeparation;
        const pOrigin = p3d(0, -3.5, originZ);
        
        ctx.save();
        ctx.fillStyle = 'rgba(255, 220, 100, 0.9)';
        ctx.shadowBlur = 20;
        ctx.shadowColor = 'rgba(255, 200, 50, 0.8)';
        ctx.beginPath();
        ctx.arc(pOrigin.x, pOrigin.y, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }

    // Haric Level (Deepest foundation)
    if (layers.haricLevel) {
        const z = getLayerZ('haric');
        // Laser Line
        const pTop = p3d(0, HARIC_POINTS.idPoint, z);
        const pBot = p3d(0, -2, z); // Into earth
        
        scribe('rgba(255, 215, 0, 0.6)', 3); // Gold laser line
        ctx.beginPath();
        ctx.moveTo(pTop.x, pTop.y);
        ctx.lineTo(pBot.x, pBot.y);
        ctx.stroke();

        // ID Point (Inverted Funnel)
        const pID = p3d(0, HARIC_POINTS.idPoint, z);
        ctx.fillStyle = 'rgba(200, 200, 255, 0.9)';
        ctx.beginPath();
        ctx.moveTo(pID.x - 5, pID.y - 10);
        ctx.lineTo(pID.x + 5, pID.y - 10);
        ctx.lineTo(pID.x, pID.y);
        ctx.fill();

        // Soul Seat (Diffuse Light)
        const pSS = p3d(0, HARIC_POINTS.soulSeat, z);
        const grad = ctx.createRadialGradient(pSS.x, pSS.y, 1, pSS.x, pSS.y, 15 * pSS.scale);
        grad.addColorStop(0, 'rgba(180, 180, 255, 0.9)');
        grad.addColorStop(1, 'rgba(180, 180, 255, 0.0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(pSS.x, pSS.y, 15 * pSS.scale, 0, Math.PI*2);
        ctx.fill();

        // Tan Tien (Ball of Power)
        const pTT = p3d(0, HARIC_POINTS.tanTien, z);
        ctx.fillStyle = '#ff4500'; // Red-Orange
        ctx.beginPath();
        ctx.arc(pTT.x, pTT.y, 6 * pTT.scale, 0, Math.PI*2);
        ctx.fill();
        ctx.strokeStyle = '#ffd700'; // Gold rim
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Core Star Level
    if (layers.coreStarLevel) {
        const z = getLayerZ('coreStar');
        const pCS = p3d(0, HARIC_POINTS.coreStar, z);
        
        // Radiating Star
        ctx.save();
        ctx.translate(pCS.x, pCS.y);
        // Rotate slowly
        ctx.rotate(t * 0.2);
        
        const rays = 12;
        ctx.fillStyle = 'white';
        ctx.beginPath();
        for(let i=0; i<rays*2; i++) {
            const rad = (i % 2 === 0) ? 20 * pCS.scale : 4 * pCS.scale;
            const a = (i / (rays*2)) * Math.PI * 2;
            ctx.lineTo(Math.cos(a)*rad, Math.sin(a)*rad);
        }
        ctx.fill();
        
        // Glow
        const grad = ctx.createRadialGradient(0, 0, 2, 0, 0, 40 * pCS.scale);
        grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        grad.addColorStop(0.4, 'rgba(200, 240, 255, 0.5)');
        grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(0, 0, 40*pCS.scale, 0, Math.PI*2);
        ctx.fill();
        
        ctx.restore();
    }

    // 1. Foundation (Vitruvian Proportions - Circle & Square)
    if (layers.foundation) {
        const z = getLayerZ('foundation');
        scribe('rgba(100, 80, 40, 0.3)', 2);
        
        ctx.beginPath();
        for(let i=0; i<=64; i++) {
            const ang = (i/64) * Math.PI * 2;
            const r = 3.5; 
            const px = Math.cos(ang) * r * 1.2;
            const py = Math.sin(ang) * r * 1.2 + 3.5;
            const p = p3d(px, py, z);
            if(i===0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();

        const pSq1 = p3d(-3.5, 0, z);
        const pSq2 = p3d(3.5, 0, z);
        const pSq3 = p3d(3.5, 7, z);
        const pSq4 = p3d(-3.5, 7, z);
        ctx.beginPath();
        ctx.moveTo(pSq1.x, pSq1.y);
        ctx.lineTo(pSq2.x, pSq2.y);
        ctx.lineTo(pSq3.x, pSq3.y);
        ctx.lineTo(pSq4.x, pSq4.y);
        ctx.closePath();
        ctx.stroke();
    }

    // 1b. The Visualised Man (Vitruvian Figure) - THE "MAN" HIMSELF
    if (layers.vitruvian) {
        const z = getLayerZ('vitruvian');
        
        // Style: "Blueprint" Blue/Cyan
        scribe('rgba(0, 190, 255, 0.4)', 2);

        // -- CENTRAL AXIS --
        // Spine
        const pNeck = p3d(0, 5.8, z);
        const pCrotch = p3d(0, 3.0, z); // "Root" relative to proportions
        ctx.beginPath(); ctx.moveTo(pNeck.x, pNeck.y); ctx.lineTo(pCrotch.x, pCrotch.y); ctx.stroke();

        // Head (Circle)
        const pHeadC = p3d(0, 6.3, z);
        ctx.beginPath();
        // Scale head radius appropriately
        ctx.arc(pHeadC.x, pHeadC.y, 10 * pHeadC.scale, 0, Math.PI * 2);
        ctx.stroke();

        // -- LIMBS SET 1 (Square / Material) --
        // Shoulders
        const pLShldr = p3d(-1.0, 5.8, z);
        const pRShldr = p3d(1.0, 5.8, z);
        ctx.beginPath(); ctx.moveTo(pLShldr.x, pLShldr.y); ctx.lineTo(pRShldr.x, pRShldr.y); ctx.stroke();

        // Arms (Horizontal)
        const pLArm = p3d(-3.5, 5.8, z);
        const pRArm = p3d(3.5, 5.8, z);
        ctx.beginPath(); ctx.moveTo(pLShldr.x, pLShldr.y); ctx.lineTo(pLArm.x, pLArm.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(pRShldr.x, pRShldr.y); ctx.lineTo(pRArm.x, pRArm.y); ctx.stroke();

        // Hips
        const pLHip = p3d(-0.6, 3.0, z);
        const pRHip = p3d(0.6, 3.0, z);
        ctx.beginPath(); ctx.moveTo(pLHip.x, pLHip.y); ctx.lineTo(pRHip.x, pRHip.y); ctx.stroke();

        // Legs (Vertical)
        const pLFoot = p3d(-0.6, 0, z);
        const pRFoot = p3d(0.6, 0, z);
        ctx.beginPath(); ctx.moveTo(pLHip.x, pLHip.y); ctx.lineTo(pLFoot.x, pLFoot.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(pRHip.x, pRHip.y); ctx.lineTo(pRFoot.x, pRFoot.y); ctx.stroke();

        // -- LIMBS SET 2 (Circle / Etheric) --
        scribe('rgba(0, 190, 255, 0.2)', 1.5); // Fainter
        
        // Arms (Raised ~20 deg)
        const armLen = 3.5;
        const armAng = 20 * Math.PI / 180;
        const pLArmUp = p3d(-Math.cos(armAng)*armLen, 5.5 + Math.sin(armAng)*armLen, z);
        const pRArmUp = p3d(Math.cos(armAng)*armLen, 5.5 + Math.sin(armAng)*armLen, z);
        
        ctx.beginPath(); ctx.moveTo(pLShldr.x, pLShldr.y); ctx.lineTo(pLArmUp.x, pLArmUp.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(pRShldr.x, pRShldr.y); ctx.lineTo(pRArmUp.x, pRArmUp.y); ctx.stroke();

        // Legs (Spread)
        const pLFootSpr = p3d(-1.5, 0.2, z);
        const pRFootSpr = p3d(1.5, 0.2, z);
        ctx.beginPath(); ctx.moveTo(pLHip.x, pLHip.y); ctx.lineTo(pLFootSpr.x, pLFootSpr.y); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(pRHip.x, pRHip.y); ctx.lineTo(pRFootSpr.x, pRFootSpr.y); ctx.stroke();
    }

    // 2. Hexagonal Lattice
    if (layers.hexagonalLattice) {
        const z = getLayerZ('hexagonal');
        scribe('rgba(139, 69, 19, 0.15)', 1);
        const rad = 1.0;
        for (let j = -4; j <= 2; j++) {
            for (let i = -3; i <= 3; i++) {
                const off = (j % 2 === 0) ? 0 : rad * 0.866;
                const fx = i * rad * 1.732 + off;
                const fy = 3.5 + j * rad * 1.5; 
                
                ctx.beginPath();
                for (let k = 0; k <= 16; k++) {
                    const a = (k / 16) * Math.PI * 2;
                    const p = p3d(fx + Math.cos(a) * rad, fy + Math.sin(a) * rad, z);
                    if (k === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
                }
                ctx.stroke();
            }
        }
    }

    // 3. Earth-Moon Geometric Ratio
    if (layers.earthMoon) {
        const z = getLayerZ('earthMoon');
        const sEarth = 7.0;
        const dMoon = sEarth * (2160 / 7920); // Michell (1969)
        
        scribe('rgba(255, 255, 255, 0.15)', 1);
        ctx.beginPath();
        const mCy = 7 + (dMoon/2); 
        for(let k=0; k<=32; k++) {
            const a = (k/32) * Math.PI * 2;
            const p = p3d(Math.cos(a) * (dMoon/2), mCy + Math.sin(a) * (dMoon/2), z);
            if(k===0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();

        const pyrBaseHalf = 3.5 * (5.5/7); 
        const pApex = p3d(0, 7, z);
        const pBL = p3d(-pyrBaseHalf*1.27, 0, z);
        const pBR = p3d(pyrBaseHalf*1.27, 0, z);
        
        ctx.fillStyle = 'rgba(240, 220, 180, 0.1)';
        ctx.beginPath();
        ctx.moveTo(pApex.x, pApex.y);
        ctx.lineTo(pBL.x, pBL.y);
        ctx.lineTo(pBR.x, pBR.y);
        ctx.closePath();
        ctx.fill();
        scribe('rgba(255, 200, 100, 0.5)', 1.5);
        ctx.stroke();
    }

    // 4. Triangle Geometry
    if (layers.triangleGeometry) {
        const z = getLayerZ('triangle');
        scribe('rgba(0, 255, 128, 0.4)', 1.5);
        
        // Isosceles representation
        const h = 5.0; 
        const w = 2.4;
        const pTip = p3d(0, 3.5 + h/2, z);
        const pLeft = p3d(-w, 3.5 - h/2, z);
        const pRight = p3d(w, 3.5 - h/2, z);

        ctx.beginPath();
        ctx.moveTo(pTip.x, pTip.y);
        ctx.lineTo(pLeft.x, pLeft.y);
        ctx.lineTo(pRight.x, pRight.y);
        ctx.closePath();
        ctx.stroke();
    }

    // 5. Heptagonal Grid
    if (layers.heptagonalGrid) {
        const z = getLayerZ('heptagon');
        scribe('rgba(0, 220, 255, 0.6)', 1.5);
        const hRad = 2.68;
        const hCenterY = 4.32; 
        ctx.beginPath();
        for (let i = 0; i < 7; i++) {
            const a = (i * 2 * Math.PI / 7) - Math.PI / 2 + (t * 0.05);
            const p = p3d(Math.cos(a) * hRad, hCenterY + Math.sin(a) * hRad, z);
            if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.closePath();
        ctx.stroke();
    }
    
    // 6. Prime Modulo Grid (Mod 24)
    if (layers.primeModuloGrid) {
        const z = getLayerZ('primeMod');
        const center = { x: 0, y: 3.5 };
        const maxRad = 4.0;
        
        scribe('rgba(0, 255, 255, 0.1)', 1);
        // 24 Rays
        for(let i=0; i<24; i++) {
            const angle = (i / 24) * Math.PI * 2 - Math.PI/2; 
            const isPrimeRay = [1, 5, 7, 11, 13, 17, 19, 23].includes(i);
            
            ctx.strokeStyle = isPrimeRay ? 'rgba(0, 255, 255, 0.5)' : 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = isPrimeRay ? 1.5 : 0.5;
            
            const pStart = p3d(center.x, center.y, z);
            const pEnd = p3d(center.x + Math.cos(angle)*maxRad, center.y + Math.sin(angle)*maxRad, z);
            
            ctx.beginPath();
            ctx.moveTo(pStart.x, pStart.y);
            ctx.lineTo(pEnd.x, pEnd.y);
            ctx.stroke();
            
            // Numbers
            if(layers.annotations && isPrimeRay) {
                const pText = p3d(center.x + Math.cos(angle)*(maxRad+0.3), center.y + Math.sin(angle)*(maxRad+0.3), z);
                ctx.fillStyle = 'rgba(0, 255, 255, 0.8)';
                ctx.font = '10px JetBrains Mono';
                ctx.textAlign = 'center';
                ctx.fillText(i.toString(), pText.x, pText.y);
            }
        }
        
        // Concentric Circles for Modulo Rings
        for(let r=1; r<=3; r++) {
             ctx.beginPath();
             const scaleR = r * 1.2;
             // Approximate circle in 3d projection (might be ellipse)
             for(let k=0; k<=48; k++) {
                 const a = (k/48)*Math.PI*2;
                 const p = p3d(center.x + Math.cos(a)*scaleR, center.y + Math.sin(a)*scaleR, z);
                 if(k===0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
             }
             ctx.stroke();
        }
    }

    // 7. Nested Platonic Polygons
    if (layers.platonic) {
        const z = getLayerZ('platonic');
        const depth = Math.min(12, Math.max(1, Math.floor(params.nestingDepth)));
        const centerY = 3.5;

        const drawPoly = (sides: number, radius: number, currentDepth: number, offset: number, colorBase: string) => {
            if (currentDepth <= 0) return;
            
            // Nested rotation
            const rot = t * 0.05 * (currentDepth % 2 === 0 ? 1 : -1) + offset;
            
            ctx.beginPath();
            for (let i = 0; i <= sides; i++) {
                const theta = (i / sides) * Math.PI * 2 + rot;
                const px = Math.cos(theta) * radius;
                const py = Math.sin(theta) * radius;
                
                const p = p3d(px, centerY + py, z);
                if (i===0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
            }
            
            ctx.strokeStyle = colorBase.replace('ALPHA', `${0.9 - (currentDepth/depth)*0.6}`);
            ctx.lineWidth = 1.5;
            ctx.stroke();
            
            // Recursion with Phi decay
            drawPoly(sides, radius * 0.618, currentDepth - 1, offset + (Math.PI/sides), colorBase);
        };

        // Hexagonal Nested (Metatron-ish)
        drawPoly(6, 4.0, depth, 0, 'rgba(0, 255, 255, ALPHA)');
        
        // Triangular Nested (Tetra)
        drawPoly(3, 4.0, depth, Math.PI/6, 'rgba(255, 100, 100, ALPHA)');
        
        // Square Nested (Octa/Cube)
        drawPoly(4, 3.2, depth, 0, 'rgba(255, 255, 100, ALPHA)');
    }

    // 8. Sephirotic Graph (Reference)
    if (layers.sephiroticGraph) {
        const z = getLayerZ('sephiroth');
        ctx.fillStyle = 'rgba(218, 165, 32, 0.8)';
        ctx.textAlign = 'center';
        
        SEPHIROTIC_NODES.forEach(node => {
            const p = p3d(node.x, node.y, z);
            ctx.beginPath();
            ctx.arc(p.x, p.y, 4 * p.scale, 0, Math.PI * 2);
            ctx.fill();
            
            if (layers.annotations) {
                ctx.fillStyle = 'rgba(255,255,255,0.5)';
                ctx.fillText(node.id, p.x, p.y - 10);
                ctx.fillStyle = 'rgba(218, 165, 32, 0.8)';
            }
        });
        
        scribe('rgba(218, 165, 32, 0.3)', 1);
        const drawLink = (id1: string, id2: string) => {
            const n1 = SEPHIROTIC_NODES.find(n => n.id === id1);
            const n2 = SEPHIROTIC_NODES.find(n => n.id === id2);
            if(n1 && n2) {
                const p1 = p3d(n1.x, n1.y, z);
                const p2 = p3d(n2.x, n2.y, z);
                ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
            }
        };
        drawLink('K','C'); drawLink('K','B'); drawLink('C','B'); drawLink('C','Ch'); drawLink('B','G');
        drawLink('Ch','G'); drawLink('Ch','T'); drawLink('G','T'); drawLink('T','N'); drawLink('T','H');
        drawLink('N','H'); drawLink('N','Y'); drawLink('H','Y'); drawLink('Y','M');
    }
    
    // 9. Harmonic Spine (Chakras & Kundalini)
    if (layers.harmonicSpine) {
        const z = getLayerZ('harmonic');
        const xAmp = 0.4;
        
        // Central Pillar
        scribe('rgba(255, 255, 255, 0.3)', 4);
        const pTop = p3d(0, 7.5, z);
        const pBot = p3d(0, -0.5, z);
        ctx.beginPath(); ctx.moveTo(pTop.x, pTop.y); ctx.lineTo(pBot.x, pBot.y); ctx.stroke();
        
        // Kundalini Snakes
        const drawSnake = (mirror: boolean) => {
             ctx.beginPath();
             ctx.strokeStyle = mirror ? 'rgba(255, 100, 100, 0.6)' : 'rgba(100, 100, 255, 0.6)';
             ctx.lineWidth = 2;
             for(let y=0; y<=7.0; y+=0.1) {
                 const x = Math.sin(y * Math.PI + t + (mirror ? Math.PI : 0)) * xAmp * (0.5 + y/7);
                 const p = p3d(x, y, z);
                 if(y===0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
             }
             ctx.stroke();
        };
        drawSnake(false); // Ida
        drawSnake(true);  // Pingala
        
        // Chakra Points
        ANATOMICAL_LEVELS.forEach((level, idx) => {
             const p = p3d(0, level.y, z);
             // Rainbow colors roughly
             const hues = [0, 25, 50, 120, 200, 270, 300]; 
             const hue = hues[idx % hues.length];
             
             // Glow
             const grad = ctx.createRadialGradient(p.x, p.y, 1, p.x, p.y, 10*p.scale);
             grad.addColorStop(0, `hsla(${hue}, 100%, 70%, 1)`);
             grad.addColorStop(1, `hsla(${hue}, 100%, 50%, 0)`);
             ctx.fillStyle = grad;
             
             ctx.beginPath(); ctx.arc(p.x, p.y, 6*p.scale, 0, Math.PI*2); ctx.fill();
        });
    }

    // 10. Star Tetrahedron (Compound Geometry)
    if (layers.starTetrahedron) {
        const zOffset = getLayerZ('tetrahedral');
        const rot = t * 0.22;
        const R = 4.45;
        const rB = R * Math.sqrt(8) / 3;
        const yB = -R / 3;

        const drawTetra = (isMale: boolean) => {
            const s = isMale ? 1 : -1;
            const ptsRaw = [
                {x: 0, y: R*s, z: 0},
                {x: rB, y: yB*s, z: 0},
                {x: -rB/2, y: yB*s, z: rB * Math.sqrt(3)/2},
                {x: -rB/2, y: yB*s, z: -rB * Math.sqrt(3)/2}
            ];
            
            const pts = ptsRaw.map(p => {
                const rx = p.x * Math.cos(rot) - p.z * Math.sin(rot);
                const rz = p.x * Math.sin(rot) + p.z * Math.cos(rot);
                return p3d(rx, 3.5 + p.y, zOffset + rz);
            });

            ctx.strokeStyle = isMale ? 'rgba(0, 255, 255, 0.6)' : 'rgba(255, 255, 255, 0.6)';
            ctx.lineWidth = 1.5;
            const edges = [[0,1], [0,2], [0,3], [1,2], [2,3], [3,1]];
            edges.forEach(e => {
                ctx.beginPath(); ctx.moveTo(pts[e[0]].x, pts[e[0]].y); ctx.lineTo(pts[e[1]].x, pts[e[1]].y); ctx.stroke();
            });
        };
        drawTetra(true);
        drawTetra(false);
    }
    
    // 11. Origins & Annotations
    if(layers.annotations) {
        const pA = p3d(-originSeparation/2, 0, 0);
        const pB = p3d(originSeparation/2, 0, 0);
        const pC = p3d(0, originCOffset, 0);

        ctx.fillStyle = 'rgba(0, 200, 255, 0.8)';
        ctx.beginPath(); ctx.arc(pA.x, pA.y, 5*pA.scale, 0, Math.PI*2); ctx.fill();
        ctx.fillText("Src A", pA.x, pA.y+15);

        ctx.fillStyle = 'rgba(180, 0, 255, 0.8)';
        ctx.beginPath(); ctx.arc(pB.x, pB.y, 5*pB.scale, 0, Math.PI*2); ctx.fill();
        ctx.fillText("Src B", pB.x, pB.y+15);

        ctx.fillStyle = 'rgba(255, 255, 200, 0.9)';
        ctx.beginPath(); ctx.arc(pC.x, pC.y, 5*pC.scale, 0, Math.PI*2); ctx.fill();
        ctx.fillText("Src C", pC.x, pC.y-15);
    }

    // --- INTERFERENCE FIELD CALCULATION (Hecht, 2002) ---
    // Superposition Principle: I = Sum(A * cos(k*r - wt + phi))
    
    const k = (2 * Math.PI) / wavelength;
    const phiRad = (phasePhi * Math.PI) / 180;
    const psiRad = (phasePsi * Math.PI) / 180;
    const pulse = view.primePulse ? (1 + 0.1 * Math.sin(t * 24)) : 1.0; // 24n harmonic

    const Ax = -originSeparation / 2;
    const Bx = originSeparation / 2;
    const Cy = originCOffset; 

    const nodeBuffer: {x: number, y: number, intensity: number}[] = [];
    const res = Math.max(0.5, 1.5 / view.zoom); 

    // sinWt oscillates. At t=0, sin(0)=0 -> BLACK SCREEN. 
    // We initialized timeRef to 2.8 so sin(0.571 * 2.8) ~= 1.0
    const sinWt = Math.sin(temporalFrequency * t);
    
    // Sampling Grid
    for (let myRaw = -20; myRaw <= 20; myRaw += res) {
        for (let mxRaw = -20; mxRaw <= 20; mxRaw += res) {
            
            // Quaternion/Mandala Mode (4-fold absolute symmetry)
            const mx = view.quaternion ? Math.abs(mxRaw) : mxRaw;
            const my = view.quaternion ? Math.abs(myRaw) : myRaw;
            
            const da = Math.sqrt(Math.pow(mx - Ax, 2) + Math.pow(my - 0, 2) + Math.pow(scanHeight, 2));
            const db = Math.sqrt(Math.pow(mx - Bx, 2) + Math.pow(my - 0, 2) + Math.pow(scanHeight, 2));
            const dc = Math.sqrt(Math.pow(mx - 0, 2) + Math.pow(my - Cy, 2) + Math.pow(scanHeight, 2));

            const valA = Math.cos(k * da) * sinWt;
            const valB = Math.cos(k * db + phiRad) * sinWt;
            const valC = Math.cos(k * dc + psiRad) * sinWt;

            let totalI = (valA + valB + valC) / 3;
            totalI *= pulse;
            
            const absI = Math.abs(totalI);
            
            // Filtering based on intensity threshold
            if (absI > intensityThreshold) {
                if (Math.random() > 0.5) continue; // Stochastic sampling for performance
                nodeBuffer.push({ x: mxRaw, y: myRaw, intensity: absI });
            }
        }
    }

    nodeBuffer.sort((a, b) => b.intensity - a.intensity);
    const renderCount = Math.min(nodeBuffer.length, nodalBudget);

    // Render Nodes with Additive Blending for "Photon" effect
    ctx.save();
    // ctx.globalCompositeOperation = 'lighter'; // Optional: additive blending for glow
    
    for (let i = 0; i < renderCount; i++) {
        const n = nodeBuffer[i];
        const p = p3d(n.x, n.y, 0);
        
        const alpha = ((n.intensity - intensityThreshold) / (1 - intensityThreshold)) * waveBrightness * 3;
        
        // Color based on intensity
        if (n.intensity > 0.85) {
             ctx.fillStyle = `rgba(200, 255, 255, ${alpha})`;
        } else {
             ctx.fillStyle = `rgba(190, 150, 90, ${alpha})`;
        }

        const s = 1.8 * p.scale * params.nodeSize;
        ctx.fillRect(p.x - s/2, p.y - s/2, s, s);
    }
    ctx.restore();

    setStats(`Nodes: ${renderCount} | T: ${t.toFixed(2)} | Pitch: ${pitch.toFixed(2)} | Yaw: ${snappedYaw.toFixed(1)}°${view.resonanceLock ? ' [LOCK]' : ''}`);

    timeRef.current += 0.01;
    requestRef.current = requestAnimationFrame(render);
  }, [params, layers, view, setStats]);

  useEffect(() => {
    requestRef.current = requestAnimationFrame(render);
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [render]);

  const handleMouseDown = (e: React.MouseEvent) => {
      isDragging.current = true;
      lastMouse.current = { x: e.clientX, y: e.clientY };
      mouseButton.current = e.button;
      e.preventDefault(); 
  };

  const handleMouseMove = (e: React.MouseEvent) => {
      if (!isDragging.current) return;
      const dx = e.clientX - lastMouse.current.x;
      const dy = e.clientY - lastMouse.current.y;
      lastMouse.current = { x: e.clientX, y: e.clientY };

      setView(prev => {
          const newState = { ...prev };
          if (mouseButton.current === 0 && !e.shiftKey) {
              newState.rotation += dx * 0.5;
              newState.pitch = Math.max(-90, Math.min(90, newState.pitch + dy * 0.5));
          }
          else if (mouseButton.current === 2 || (mouseButton.current === 0 && e.shiftKey)) {
              newState.panX += dx;
              newState.panY += dy;
          }
          return newState;
      });
  };

  const handleMouseUp = () => {
      isDragging.current = false;
      mouseButton.current = null;
  };
  
  const handleWheel = (e: React.WheelEvent) => {
      setView(prev => ({
          ...prev,
          zoom: Math.max(0.1, Math.min(10, prev.zoom - e.deltaY * 0.001))
      }));
  };

  return (
    <canvas 
        ref={canvasRef} 
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
        onContextMenu={(e) => e.preventDefault()}
        className="absolute top-0 left-0 w-full h-full cursor-move"
    />
  );
});

export default Visualizer;
