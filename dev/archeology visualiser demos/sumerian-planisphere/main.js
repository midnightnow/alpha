/**
 * Sumerian Planisphere K8538 Visualizer
 * An interactive 3D museum exhibit visualizing ancient Mesopotamian astronomy
 *
 * Architecture:
 * - PlanisphereSector: Wedge-shaped sector with hover/select animations
 * - StarField: Instanced stars positioned according to sector data
 * - CameraRig: Orbital controls with preset views
 * - InteractionManager: rAF-throttled raycasting
 * - InspectorPanel: DOM overlay with astronomical calculations
 */

import * as THREE from "three";
import gsap from "gsap";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import {
  toSexagesimal,
  toBase60String,
  calculateSectorGeometry,
  calculateHeliacalRising,
  angularSeparation,
  formatRA,
  formatMagnitude,
  toFixedTrim,
  CUNEIFORM,
  toCuneiformNumber,
  ANCIENT_LATITUDES,
  OBLIQUITY
} from "./src/utils/astronomy.js";
import planisphereData from "./src/data/planisphere.json";

// ===========================================
// Constants
// ===========================================

const LENS_HEADLINES = {
  astronomical: "A Map of the Heavens",
  mathematical: "Celestial Mathematics",
  cultural: "Stars & Society"
};

const LENS_CONTEXTS = {
  astronomical: "This planisphere shows 8 sectors of the night sky as observed from ancient Mesopotamia. Each sector contains constellations, individual stars, and astronomical markers used for navigation and calendar keeping.",
  mathematical: "Babylonian astronomers used base-60 (sexagesimal) mathematics to track celestial positions. Each 45° sector represents sophisticated angular measurement, with star positions recorded in 'cubits' from reference points.",
  cultural: "The stars governed life in ancient Mesopotamia—from agricultural timing to religious festivals. Celestial omens were recorded and interpreted by court astronomers who advised kings on auspicious dates for warfare, construction, and coronations."
};

// ===========================================
// State
// ===========================================

let currentLens = "astronomical";
let currentCoordTab = "ecliptic";
let currentEpoch = -700;
let selectedSector = null;
let compareSector = null;
let isAutoRotating = false;
let isTopDown = false;

// ===========================================
// Three.js Setup
// ===========================================

const container = document.getElementById("canvas-container");
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.9;
container.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050810);

// Add fog for depth
scene.fog = new THREE.FogExp2(0x050810, 0.015);

const camera = new THREE.PerspectiveCamera(
  50,
  window.innerWidth / window.innerHeight,
  0.1,
  500
);
camera.position.set(0, 12, 20);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enablePan = false;
controls.minDistance = 10;
controls.maxDistance = 60;
controls.target.set(0, 0, 0);
controls.update();

// Lights
const ambientLight = new THREE.AmbientLight(0x334466, 0.4);
scene.add(ambientLight);

const mainLight = new THREE.DirectionalLight(0xffffee, 0.8);
mainLight.position.set(5, 15, 10);
scene.add(mainLight);

const rimLight = new THREE.DirectionalLight(0x6688ff, 0.3);
rimLight.position.set(-10, 5, -10);
scene.add(rimLight);

// Ground plane (subtle starfield effect)
const groundGeom = new THREE.PlaneGeometry(200, 200);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x030508,
  roughness: 1.0,
  metalness: 0.0
});
const ground = new THREE.Mesh(groundGeom, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -8;
scene.add(ground);

// ===========================================
// Background Stars
// ===========================================

function createBackgroundStars() {
  const starCount = 2000;
  const positions = new Float32Array(starCount * 3);
  const colors = new Float32Array(starCount * 3);
  const sizes = new Float32Array(starCount);

  for (let i = 0; i < starCount; i++) {
    // Distribute on a sphere
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = 80 + Math.random() * 40;

    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);

    // Vary star colors slightly (warm to cool)
    const temp = Math.random();
    colors[i * 3] = 0.8 + temp * 0.2;
    colors[i * 3 + 1] = 0.8 + (1 - temp) * 0.2;
    colors[i * 3 + 2] = 0.9 + Math.random() * 0.1;

    sizes[i] = 0.5 + Math.random() * 1.5;
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  const material = new THREE.PointsMaterial({
    size: 0.15,
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    sizeAttenuation: true
  });

  const stars = new THREE.Points(geometry, material);
  scene.add(stars);

  return stars;
}

const backgroundStars = createBackgroundStars();

// ===========================================
// PlanisphereSector Class
// ===========================================

class PlanisphereSector {
  constructor(sectorData, index) {
    this.data = sectorData;
    this.index = index;

    // Geometry parameters
    this.innerRadius = 1.5;
    this.outerRadius = 7;
    this.thickness = 0.4;

    // Calculate angles (in radians)
    const geo = calculateSectorGeometry(index);
    this.startAngle = (geo.startAngle - 90) * Math.PI / 180; // Rotate so 0 is at top
    this.endAngle = (geo.endAngle - 90) * Math.PI / 180;

    this.group = new THREE.Group();
    this.group.userData.sector = sectorData;
    this.group.userData.index = index;

    // Create the wedge
    this.wedgeMesh = this._createWedge();
    this.group.add(this.wedgeMesh);

    // Create sector lines
    this.lines = this._createLines();
    this.group.add(this.lines);

    // Create star markers
    this.starMarkers = this._createStarMarkers();
    this.group.add(this.starMarkers);

    // Create label
    this.label = this._createLabel();
    this.group.add(this.label);

    this._tl = null;
    this.isHighlighted = false;
  }

  _createWedge() {
    const shape = new THREE.Shape();
    const segments = 32;

    // Start at inner radius
    shape.moveTo(
      Math.cos(this.startAngle) * this.innerRadius,
      Math.sin(this.startAngle) * this.innerRadius
    );

    // Arc along outer radius
    shape.absarc(0, 0, this.outerRadius, this.startAngle, this.endAngle, false);

    // Line to inner radius
    shape.lineTo(
      Math.cos(this.endAngle) * this.innerRadius,
      Math.sin(this.endAngle) * this.innerRadius
    );

    // Arc back along inner radius
    shape.absarc(0, 0, this.innerRadius, this.endAngle, this.startAngle, true);

    const extrudeSettings = {
      depth: this.thickness,
      bevelEnabled: true,
      bevelThickness: 0.02,
      bevelSize: 0.02,
      bevelSegments: 2,
      steps: 1
    };

    const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
    geometry.rotateX(-Math.PI / 2);
    geometry.translate(0, this.thickness / 2, 0);

    // Clay-like material with subtle color tint
    const hue = new THREE.Color(this.data.color);
    const material = new THREE.MeshStandardMaterial({
      color: 0xc2b280,
      roughness: 0.95,
      metalness: 0.0,
      transparent: true,
      opacity: 0.9,
      emissive: hue,
      emissiveIntensity: 0.02
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.userData.isSector = true;
    mesh.userData.sector = this.data;
    mesh.receiveShadow = true;

    return mesh;
  }

  _createLines() {
    const group = new THREE.Group();
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x887755,
      transparent: true,
      opacity: 0.6
    });

    // Radial lines
    [this.startAngle, this.endAngle].forEach(angle => {
      const pts = [
        new THREE.Vector3(
          Math.cos(angle) * this.innerRadius,
          this.thickness + 0.01,
          Math.sin(angle) * this.innerRadius
        ),
        new THREE.Vector3(
          Math.cos(angle) * this.outerRadius,
          this.thickness + 0.01,
          Math.sin(angle) * this.outerRadius
        )
      ];
      const lineGeom = new THREE.BufferGeometry().setFromPoints(pts);
      group.add(new THREE.Line(lineGeom, lineMat));
    });

    return group;
  }

  _createStarMarkers() {
    const group = new THREE.Group();

    if (!this.data.stars || this.data.stars.length === 0) return group;

    const midAngle = (this.startAngle + this.endAngle) / 2;
    const angleSpan = (this.endAngle - this.startAngle) * 0.6;

    // Store references for animation
    this._starMeshes = [];
    this._glowMeshes = [];

    this.data.stars.forEach((star, i) => {
      const starAngle = midAngle + (i - (this.data.stars.length - 1) / 2) * angleSpan / Math.max(this.data.stars.length - 1, 1);
      const radius = this.innerRadius + (this.outerRadius - this.innerRadius) * (0.4 + i * 0.15);

      // Star size based on magnitude (brighter = lower mag = bigger)
      const size = Math.max(0.08, 0.25 - star.magnitude * 0.04);

      const starGeom = new THREE.SphereGeometry(size, 8, 6);
      const starMat = new THREE.MeshBasicMaterial({
        color: 0xffffee,
        transparent: true,
        opacity: 0.3
      });
      const starMesh = new THREE.Mesh(starGeom, starMat);

      starMesh.position.set(
        Math.cos(starAngle) * radius,
        this.thickness + 0.1,
        -Math.sin(starAngle) * radius
      );
      starMesh.userData.star = star;

      group.add(starMesh);
      this._starMeshes.push(starMesh);

      // Add glow
      const glowGeom = new THREE.SphereGeometry(size * 2, 8, 6);
      const glowMat = new THREE.MeshBasicMaterial({
        color: 0xaaccff,
        transparent: true,
        opacity: 0.03
      });
      const glow = new THREE.Mesh(glowGeom, glowMat);
      glow.position.copy(starMesh.position);
      group.add(glow);
      this._glowMeshes.push(glow);
    });

    return group;
  }

  _createLabel() {
    // Create a simple sprite for the constellation name
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = 'rgba(0,0,0,0)';
    ctx.fillRect(0, 0, 256, 64);

    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.font = '24px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(this.data.name.split('/')[0].trim(), 128, 32);

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      opacity: 0.6
    });

    const sprite = new THREE.Sprite(material);
    sprite.scale.set(3, 0.75, 1);

    const midAngle = (this.startAngle + this.endAngle) / 2;
    const labelRadius = this.outerRadius * 0.65;

    sprite.position.set(
      Math.cos(midAngle) * labelRadius,
      this.thickness + 0.3,
      -Math.sin(midAngle) * labelRadius
    );

    return sprite;
  }

  highlight() {
    if (this.isHighlighted) return;
    this.isHighlighted = true;

    if (this._tl) this._tl.kill();

    this._tl = gsap.timeline();

    // Lift and glow
    this._tl.to(this.group.position, {
      y: 0.5,
      duration: 0.35,
      ease: "power2.out"
    }, 0);

    this._tl.to(this.wedgeMesh.material, {
      emissiveIntensity: 0.15,
      duration: 0.25,
      ease: "power2.out"
    }, 0);

    this._tl.to(this.label.material, {
      opacity: 1.0,
      duration: 0.2
    }, 0);

    // Light up the stars
    if (this._starMeshes) {
      this._starMeshes.forEach(star => {
        this._tl.to(star.material, {
          opacity: 1.0,
          duration: 0.25,
          ease: "power2.out"
        }, 0);
        this._tl.to(star.scale, {
          x: 1.5, y: 1.5, z: 1.5,
          duration: 0.3,
          ease: "back.out(2)"
        }, 0);
      });
    }

    // Intensify glow
    if (this._glowMeshes) {
      this._glowMeshes.forEach(glow => {
        this._tl.to(glow.material, {
          opacity: 0.4,
          duration: 0.3,
          ease: "power2.out"
        }, 0);
        this._tl.to(glow.scale, {
          x: 1.8, y: 1.8, z: 1.8,
          duration: 0.35,
          ease: "power2.out"
        }, 0);
      });
    }

    return this._tl;
  }

  unhighlight() {
    if (!this.isHighlighted) return;
    this.isHighlighted = false;

    if (this._tl) this._tl.kill();

    this._tl = gsap.timeline();

    this._tl.to(this.group.position, {
      y: 0,
      duration: 0.3,
      ease: "power2.out"
    }, 0);

    this._tl.to(this.wedgeMesh.material, {
      emissiveIntensity: 0.02,
      duration: 0.2,
      ease: "power2.out"
    }, 0);

    this._tl.to(this.label.material, {
      opacity: 0.6,
      duration: 0.2
    }, 0);

    // Dim the stars significantly
    if (this._starMeshes) {
      this._starMeshes.forEach(star => {
        this._tl.to(star.material, {
          opacity: 0.3,
          duration: 0.2,
          ease: "power2.out"
        }, 0);
        this._tl.to(star.scale, {
          x: 1, y: 1, z: 1,
          duration: 0.25,
          ease: "power2.out"
        }, 0);
      });
    }

    // Reduce glow significantly
    if (this._glowMeshes) {
      this._glowMeshes.forEach(glow => {
        this._tl.to(glow.material, {
          opacity: 0.03,
          duration: 0.2,
          ease: "power2.out"
        }, 0);
        this._tl.to(glow.scale, {
          x: 1, y: 1, z: 1,
          duration: 0.25,
          ease: "power2.out"
        }, 0);
      });
    }

    return this._tl;
  }
}

// ===========================================
// Center Hub
// ===========================================

function createCenterHub() {
  const group = new THREE.Group();

  // Central disk
  const diskGeom = new THREE.CylinderGeometry(1.5, 1.5, 0.5, 32);
  const diskMat = new THREE.MeshStandardMaterial({
    color: 0xd4c494,
    roughness: 0.9,
    metalness: 0.0
  });
  const disk = new THREE.Mesh(diskGeom, diskMat);
  disk.position.y = 0.25;
  group.add(disk);

  // Center symbol (AN - heaven)
  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 128;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = 'rgba(0,0,0,0)';
  ctx.fillRect(0, 0, 128, 128);
  ctx.fillStyle = '#554433';
  ctx.font = '64px serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('𒀭', 64, 64);

  const texture = new THREE.CanvasTexture(canvas);
  const symbolMat = new THREE.MeshBasicMaterial({
    map: texture,
    transparent: true,
    opacity: 0.7
  });

  const symbolGeom = new THREE.PlaneGeometry(1.2, 1.2);
  const symbol = new THREE.Mesh(symbolGeom, symbolMat);
  symbol.rotation.x = -Math.PI / 2;
  symbol.position.y = 0.51;
  group.add(symbol);

  return group;
}

// ===========================================
// CameraRig Class
// ===========================================

class CameraRig {
  constructor(camera, controls) {
    this.camera = camera;
    this.controls = controls;

    this.defaultPos = new THREE.Vector3(0, 12, 20);
    this.defaultTarget = new THREE.Vector3(0, 0, 0);

    this.topDownPos = new THREE.Vector3(0, 25, 0.1);
    this.topDownTarget = new THREE.Vector3(0, 0, 0);
  }

  toTopDown() {
    gsap.to(this.camera.position, {
      x: this.topDownPos.x, y: this.topDownPos.y, z: this.topDownPos.z,
      duration: 1.0,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
    gsap.to(this.controls.target, {
      x: this.topDownTarget.x, y: this.topDownTarget.y, z: this.topDownTarget.z,
      duration: 1.0,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
  }

  toDefault() {
    gsap.to(this.camera.position, {
      x: this.defaultPos.x, y: this.defaultPos.y, z: this.defaultPos.z,
      duration: 1.0,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
    gsap.to(this.controls.target, {
      x: this.defaultTarget.x, y: this.defaultTarget.y, z: this.defaultTarget.z,
      duration: 1.0,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
  }
}

// ===========================================
// InteractionManager Class
// ===========================================

class InteractionManager {
  constructor({ camera, domElement, pickables, onHover, onClick, onHoverNone }) {
    this.camera = camera;
    this.domElement = domElement;
    this.pickables = pickables;
    this.onHover = onHover;
    this.onClick = onClick;
    this.onHoverNone = onHoverNone;

    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    this.hoveredId = null;

    this._rafPending = false;
    this._lastEvent = null;

    this._onMove = (e) => {
      this._lastEvent = e;
      if (this._rafPending) return;
      this._rafPending = true;
      requestAnimationFrame(() => {
        this._rafPending = false;
        this._pick(this._lastEvent);
      });
    };

    this._onClick = (e) => {
      this._pick(e, true);
    };

    this._onLeave = () => {
      if (this.hoveredId != null) {
        this.hoveredId = null;
        this.onHoverNone();
      }
    };

    domElement.addEventListener("pointermove", this._onMove);
    domElement.addEventListener("click", this._onClick);
    domElement.addEventListener("pointerleave", this._onLeave);
  }

  dispose() {
    this.domElement.removeEventListener("pointermove", this._onMove);
    this.domElement.removeEventListener("click", this._onClick);
    this.domElement.removeEventListener("pointerleave", this._onLeave);
  }

  _pick(e, isClick = false) {
    const rect = this.domElement.getBoundingClientRect();
    this.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, this.camera);

    const hits = this.raycaster.intersectObjects(this.pickables, true);
    const hit = hits.find(h => h.object?.userData?.isSector);

    if (!hit) {
      if (this.hoveredId != null && !isClick) {
        this.hoveredId = null;
        this.onHoverNone();
      }
      return;
    }

    const sector = hit.object.userData.sector;
    if (!sector) return;

    if (isClick) {
      const isShift = e.shiftKey;
      this.onClick(sector, isShift);
    } else if (this.hoveredId !== sector.id) {
      this.hoveredId = sector.id;
      this.onHover(sector);
    }
  }
}

// ===========================================
// Build Planisphere
// ===========================================

const planisphereGroup = new THREE.Group();
scene.add(planisphereGroup);

const sectors = planisphereData.sectors.map((sectorData, idx) => {
  const sector = new PlanisphereSector(sectorData, idx);
  planisphereGroup.add(sector.group);
  return sector;
});

const centerHub = createCenterHub();
planisphereGroup.add(centerHub);

const pickables = sectors.map(s => s.wedgeMesh);
const cameraRig = new CameraRig(camera, controls);

// ===========================================
// UI Functions
// ===========================================

function buildSectorList() {
  const listEl = document.getElementById("sector-list");
  listEl.innerHTML = "";

  planisphereData.sectors.forEach((sector, idx) => {
    const geo = calculateSectorGeometry(idx);

    const item = document.createElement("div");
    item.className = "sector-item";
    item.dataset.sectorId = sector.id;

    const starCount = sector.stars ? sector.stars.length : 0;

    item.innerHTML = `
      <span class="sector-idx" style="color: ${sector.color}">${idx + 1}</span>
      <div class="sector-content">
        <div class="sector-name">${sector.name}</div>
        <div class="sector-secondary">
          <span class="sector-sumerian">${sector.sumerian}</span>
          <span class="sector-angle">${geo.startAngle}°–${geo.endAngle}°</span>
        </div>
      </div>
      <span class="sector-stars">${starCount} ★</span>
    `;

    item.addEventListener("click", (e) => {
      handleSectorClick(sector, e.shiftKey);
    });

    item.addEventListener("mouseenter", () => {
      if (!selectedSector || selectedSector.id !== sector.id) {
        handleSectorHover(sector);
      }
    });

    listEl.appendChild(item);
  });
}

function updateSectorListSelection() {
  document.querySelectorAll(".sector-item").forEach(el => {
    el.classList.remove("active", "compare");
    if (selectedSector && el.dataset.sectorId == selectedSector.id) {
      el.classList.add("active");
    }
    if (compareSector && el.dataset.sectorId == compareSector.id) {
      el.classList.add("compare");
    }
  });
}

function updateInspector(sector) {
  const inspector = document.getElementById("inspector");
  const coordDisplay = document.getElementById("coordinate-display");
  const starDataContent = document.getElementById("star-data-content");

  if (!sector) {
    inspector.innerHTML = `
      <h3>Select a Sector</h3>
      <p class="instruction">Click on a wedge to explore its celestial contents.</p>
    `;
    coordDisplay.style.display = "none";
    return;
  }

  const geo = calculateSectorGeometry(sector.id - 1);

  // Main inspector content
  inspector.innerHTML = `
    <h3>${sector.name}</h3>
    <div class="cuneiform-header">
      <span class="cuneiform-text">${CUNEIFORM.MUL} ${sector.sumerian}</span>
      <span class="akkadian-text">(${sector.akkadian})</span>
    </div>

    <div class="inspector-grid">
      <div class="inspector-stat">
        <div class="inspector-stat-label">Arc Span</div>
        <div class="inspector-stat-value">${geo.angleSpan}°</div>
        <div class="inspector-stat-sub">${toBase60String(geo.angleSpan)} (base-60)</div>
      </div>
      <div class="inspector-stat">
        <div class="inspector-stat-label">Time Span</div>
        <div class="inspector-stat-value">${geo.daysSpan} days</div>
        <div class="inspector-stat-sub">${Math.round(geo.timeSpanMinutes)} min rotation</div>
      </div>
      <div class="inspector-stat">
        <div class="inspector-stat-label">Stars Shown</div>
        <div class="inspector-stat-value highlight">${sector.stars?.length || 0}</div>
        <div class="inspector-stat-sub">${sector.modernConstellation}</div>
      </div>
      <div class="inspector-stat">
        <div class="inspector-stat-label">Sector Arc</div>
        <div class="inspector-stat-value">${geo.startAngleSex.formatted}</div>
        <div class="inspector-stat-sub">to ${geo.endAngleSex.formatted}</div>
      </div>
    </div>

    <p class="sector-interpretation">${sector.interpretation}</p>
  `;

  // Coordinate display
  coordDisplay.style.display = "block";
  updateCoordinateContent(sector);

  // Star data
  if (sector.stars && sector.stars.length > 0) {
    let starHtml = '<div class="star-table">';
    starHtml += '<div class="star-row star-header"><span>Star</span><span>Mag</span><span>Heliacal</span></div>';

    sector.stars.forEach(star => {
      // Calculate heliacal rising (simplified)
      const heliacal = calculateHeliacalRising(geo.midAngle, 0, ANCIENT_LATITUDES.nineveh, currentEpoch);

      starHtml += `
        <div class="star-row">
          <span class="star-name">${star.name}</span>
          <span class="star-mag">${formatMagnitude(star.magnitude)}</span>
          <span class="star-heliacal">~${heliacal.daysFromVernalEquinox}d</span>
        </div>
      `;
    });
    starHtml += '</div>';
    starDataContent.innerHTML = starHtml;
  } else {
    starDataContent.innerHTML = '<p class="research-body">No individual stars recorded in this sector.</p>';
  }
}

function updateCoordinateContent(sector) {
  if (!sector) return;

  const content = document.getElementById("coordinate-content");
  const geo = calculateSectorGeometry(sector.id - 1);

  let html = "";

  switch (currentCoordTab) {
    case "ecliptic":
      html = `
        <div class="coord-value">${geo.startAngle}° – ${geo.endAngle}°</div>
        <div class="coord-note">Ecliptic longitude range</div>
        <div class="coord-detail">Mid-sector: ${toFixedTrim(geo.midAngle, 2)}°</div>
      `;
      break;
    case "equatorial":
      // Simplified conversion
      const raStart = formatRA(geo.startAngle);
      const raEnd = formatRA(geo.endAngle);
      html = `
        <div class="coord-value">${raStart} – ${raEnd}</div>
        <div class="coord-note">Right Ascension range (approx)</div>
        <div class="coord-detail">Epoch: ${Math.abs(currentEpoch)} ${currentEpoch < 0 ? 'BCE' : 'CE'}</div>
      `;
      break;
    case "sexagesimal":
      html = `
        <div class="coord-value">${geo.startAngleSex.formatted}</div>
        <div class="coord-note">Start angle in base-60</div>
        <div class="coord-detail">${toCuneiformNumber(Math.floor(geo.startAngle / 10))} × 10 UŠ</div>
      `;
      break;
  }

  content.innerHTML = html;
}

function updateLensUI() {
  document.getElementById("headline").textContent = LENS_HEADLINES[currentLens];
  document.getElementById("context-text").textContent = LENS_CONTEXTS[currentLens];

  document.querySelectorAll(".lens-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.lens === currentLens);
  });
}

function updateCompareOverlay() {
  const overlay = document.getElementById("compare-overlay");
  const dataEl = document.getElementById("compare-data");

  if (!selectedSector || !compareSector) {
    overlay.style.display = "none";
    return;
  }

  const geo1 = calculateSectorGeometry(selectedSector.id - 1);
  const geo2 = calculateSectorGeometry(compareSector.id - 1);

  const deltaAngle = Math.abs(geo2.midAngle - geo1.midAngle);

  overlay.style.display = "block";
  dataEl.innerHTML = `
    <div class="compare-row">
      <span>Sector ${selectedSector.id}: ${selectedSector.name.split('/')[0]}</span>
      <span>${geo1.midAngle}°</span>
    </div>
    <div class="compare-row">
      <span>Sector ${compareSector.id}: ${compareSector.name.split('/')[0]}</span>
      <span>${geo2.midAngle}°</span>
    </div>
    <div class="compare-delta">
      Angular separation: ${toFixedTrim(deltaAngle, 1)}° (${toBase60String(deltaAngle)})
    </div>
  `;
}

// ===========================================
// Interaction Handlers
// ===========================================

function handleSectorHover(sectorData) {
  sectors.forEach(s => {
    if (s.data.id === sectorData.id) {
      s.highlight();
    } else if (!selectedSector || s.data.id !== selectedSector.id) {
      s.unhighlight();
    }
  });

  if (!selectedSector) {
    updateInspector(sectorData);
  }
}

function handleSectorClick(sectorData, isShift) {
  if (isShift && selectedSector && selectedSector.id !== sectorData.id) {
    compareSector = sectorData;
    const sectorObj = sectors.find(s => s.data.id === sectorData.id);
    sectorObj?.highlight();
  } else {
    if (compareSector) {
      const prevCompare = sectors.find(s => s.data.id === compareSector.id);
      prevCompare?.unhighlight();
      compareSector = null;
    }

    selectedSector = sectorData;
    updateInspector(sectorData);

    sectors.forEach(s => {
      if (s.data.id === sectorData.id) {
        s.highlight();
      } else {
        s.unhighlight();
      }
    });
  }

  updateSectorListSelection();
  updateCompareOverlay();
}

function handleHoverNone() {
  if (!selectedSector) {
    sectors.forEach(s => s.unhighlight());
    updateInspector(null);
  }
}

// ===========================================
// Event Listeners
// ===========================================

const interaction = new InteractionManager({
  camera,
  domElement: renderer.domElement,
  pickables,
  onHover: handleSectorHover,
  onClick: handleSectorClick,
  onHoverNone: handleHoverNone
});

// Lens toggle
document.querySelectorAll(".lens-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    currentLens = btn.dataset.lens;
    updateLensUI();
  });
});

// Coordinate tabs
document.querySelectorAll(".coord-tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".coord-tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    currentCoordTab = tab.dataset.tab;
    if (selectedSector) updateCoordinateContent(selectedSector);
  });
});

// Epoch selector
document.querySelectorAll(".epoch-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".epoch-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentEpoch = parseInt(btn.dataset.epoch);
    if (selectedSector) updateInspector(selectedSector);
  });
});

// Auto-rotate toggle
document.getElementById("btn-rotate").addEventListener("click", () => {
  isAutoRotating = !isAutoRotating;
  const btn = document.getElementById("btn-rotate");

  if (isAutoRotating) {
    btn.classList.add("active");
    btn.innerHTML = '<span class="icon">⏹</span> Stop Rotation';
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.5;
  } else {
    btn.classList.remove("active");
    btn.innerHTML = '<span class="icon">⟲</span> Auto-Rotate Sky';
    controls.autoRotate = false;
  }
});

// Top-down view
document.getElementById("btn-flatten").addEventListener("click", () => {
  isTopDown = !isTopDown;
  const btn = document.getElementById("btn-flatten");

  if (isTopDown) {
    cameraRig.toTopDown();
    btn.classList.add("active");
    btn.innerHTML = '<span class="icon">◐</span> 3D View';
  } else {
    cameraRig.toDefault();
    btn.classList.remove("active");
    btn.innerHTML = '<span class="icon">◎</span> Top-Down View';
  }
});

// Clear compare
document.getElementById("btn-clear-compare").addEventListener("click", () => {
  if (compareSector) {
    const sectorObj = sectors.find(s => s.data.id === compareSector.id);
    sectorObj?.unhighlight();
    compareSector = null;
    updateSectorListSelection();
    updateCompareOverlay();
  }
});

// Resize
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// Keyboard shortcuts
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    if (compareSector) {
      const sectorObj = sectors.find(s => s.data.id === compareSector.id);
      sectorObj?.unhighlight();
      compareSector = null;
    } else if (selectedSector) {
      selectedSector = null;
      sectors.forEach(s => s.unhighlight());
      updateInspector(null);
    }
    updateSectorListSelection();
    updateCompareOverlay();
  }

  // Number keys to select sectors
  const num = parseInt(e.key);
  if (num >= 1 && num <= 8) {
    const sector = planisphereData.sectors[num - 1];
    if (sector) handleSectorClick(sector, e.shiftKey);
  }
});

// ===========================================
// Render Loop
// ===========================================

function tick() {
  controls.update();

  // Subtle star twinkle
  if (backgroundStars && backgroundStars.material) {
    backgroundStars.material.opacity = 0.65 + Math.sin(Date.now() * 0.001) * 0.05;
  }

  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}

// ===========================================
// Initialize
// ===========================================

function init() {
  buildSectorList();
  updateLensUI();

  // Hide loader
  setTimeout(() => {
    document.getElementById("loader").classList.add("hidden");
  }, 1000);

  tick();
}

init();
