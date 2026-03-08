/**
 * Plimpton 322 Visualizer
 * An interactive 3D museum exhibit visualizing the world's oldest catalog of slopes
 *
 * Architecture:
 * - PlimptonRow: Clay bar + wedge reveal animation
 * - VoxelGenerator: InstancedMesh for 60-cube blocks
 * - InteractionManager: rAF-throttled raycasting
 * - InspectorPanel: DOM overlay with sexagesimal display
 * - CameraRig: Default ↔ isometric transitions
 */

import * as THREE from "three";
import gsap from "gsap";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import {
  formatSexagesimalInt,
  formatSexagesimalFrac,
  formatSexagesimalRational,
  toFixedTrim,
  toPitchPer12,
  gcd,
  reduceTriple,
  isRegular,
  formatPrimeFactors
} from "./src/utils/sexagesimal.js";
import plimptonData from "./src/data/plimpton322.json";

// ===========================================
// Constants
// ===========================================

const ROMAN_NUMERALS = [
  "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
  "X", "XI", "XII", "XIII", "XIV", "XV"
];

const LENS_HEADLINES = {
  ratio: "A Catalog of Practical Slopes",
  trig: "An Early Trigonometric Table",
  number: "A Scribal Exercise in Regular Numbers"
};

const LENS_CONTEXTS = {
  ratio: "This tablet contains 15 rows of Pythagorean triples, ordered by slope from steepest (~45°) to flattest (~32°). Builders could reference this for precise rise/run ratios.",
  trig: "Mansfield & Wildberger (2017) argue this is the world's first trigonometric table, using exact ratios rather than angles. The precision exceeds modern tables for certain applications.",
  number: "Robson (2001) places this in scribal school context. The numbers are chosen for their 'regular' properties (factors of 2, 3, 5 only), making sexagesimal arithmetic clean."
};

// ===========================================
// State
// ===========================================

let currentLens = "ratio";
let currentSlopeTab = "degrees";
let selectedRow = null;
let compareRow = null;
let isIsometric = false;
let showReconstruction = true;

// ===========================================
// Three.js Setup
// ===========================================

const container = document.getElementById("canvas-container");
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
container.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b0d10);

const camera = new THREE.PerspectiveCamera(
  45,
  window.innerWidth / window.innerHeight,
  0.1,
  200
);
camera.position.set(0, 8, 22);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enablePan = false;
controls.minDistance = 12;
controls.maxDistance = 45;
controls.target.set(0, -4, 0);
controls.update();

// Lights
const hemiLight = new THREE.HemisphereLight(0xffffff, 0x223344, 0.7);
scene.add(hemiLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 1.1);
dirLight.position.set(10, 15, 12);
scene.add(dirLight);

const backLight = new THREE.DirectionalLight(0x88aaff, 0.3);
backLight.position.set(-10, 5, -10);
scene.add(backLight);

// Ground plane
const groundGeom = new THREE.PlaneGeometry(100, 100);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x0e1117,
  roughness: 1.0,
  metalness: 0.0
});
const ground = new THREE.Mesh(groundGeom, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -14;
scene.add(ground);

// ===========================================
// PlimptonRow Class
// ===========================================

class PlimptonRow {
  constructor(rowData, index) {
    this.data = rowData;
    this.index = index;
    this.targetLong = 9;
    this.depth = 0.7;

    this.group = new THREE.Group();
    this.group.userData.row = rowData;

    // Create clay bar
    this.clayMesh = this._createClayBar();
    this.group.add(this.clayMesh);

    // Create wedge (starts hidden)
    this.wedgeGroup = this._createWedge();
    this.wedgeGroup.visible = false;
    this.wedgeGroup.scale.setScalar(0.01);
    this.group.add(this.wedgeGroup);

    // Position in stack
    this.group.position.y = -index * 1.4;

    this._tl = null;
    this.isRevealed = false;
  }

  _createClayBar() {
    const geom = new THREE.BoxGeometry(this.targetLong + 2, 0.9, 0.6);
    const mat = new THREE.MeshStandardMaterial({
      color: 0xc2b280,
      roughness: 1.0,
      metalness: 0.0,
      transparent: true,
      opacity: 1.0
    });

    const mesh = new THREE.Mesh(geom, mat);
    mesh.userData.isClay = true;
    mesh.userData.row = this.data;
    mesh.receiveShadow = true;
    return mesh;
  }

  _createWedge() {
    const { s, l } = this.data;
    const scale = this.targetLong / l;

    // Right triangle shape: A(0,0), B(l,0), C(0,s)
    const shape = new THREE.Shape()
      .moveTo(0, 0)
      .lineTo(l * scale, 0)
      .lineTo(0, s * scale)
      .lineTo(0, 0);

    const wedgeGeom = new THREE.ExtrudeGeometry(shape, {
      depth: this.depth,
      bevelEnabled: false,
      steps: 1
    });
    wedgeGeom.computeVertexNormals();

    const wedgeMat = new THREE.MeshStandardMaterial({
      color: 0x44aaff,
      roughness: 0.35,
      metalness: 0.05,
      transparent: true,
      opacity: 0.0,
      side: THREE.DoubleSide,
      depthWrite: false
    });

    const wedge = new THREE.Mesh(wedgeGeom, wedgeMat);

    // Hypotenuse line
    const pts = [
      new THREE.Vector3(0, s * scale, 0),
      new THREE.Vector3(l * scale, 0, 0)
    ];
    const lineGeom = new THREE.BufferGeometry().setFromPoints(pts);
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x111111,
      transparent: true,
      opacity: 0.0,
      depthWrite: false
    });
    const hypo = new THREE.Line(lineGeom, lineMat);
    hypo.position.z = this.depth + 0.001;

    const group = new THREE.Group();
    group.add(wedge);
    group.add(hypo);

    // Center the group
    const box = new THREE.Box3().setFromObject(group);
    const center = box.getCenter(new THREE.Vector3());
    group.position.sub(center);

    group.userData.wedge = wedge;
    group.userData.hypo = hypo;
    group.userData.scale = scale;

    return group;
  }

  reveal() {
    if (this.isRevealed) return;
    this.isRevealed = true;

    if (this._tl) this._tl.kill();

    this.wedgeGroup.visible = true;

    const wedgeMat = this.wedgeGroup.userData.wedge.material;
    const lineMat = this.wedgeGroup.userData.hypo.material;

    this._tl = gsap.timeline();

    // Fade clay
    this._tl.to(this.clayMesh.material, {
      opacity: 0.15,
      duration: 0.25,
      ease: "power2.out"
    }, 0);

    // Pop wedge
    this._tl.to(this.wedgeGroup.scale, {
      x: 1, y: 1, z: 1,
      duration: 0.55,
      ease: "back.out(1.8)"
    }, 0.02);

    // Fade in wedge + line
    this._tl.to(wedgeMat, { opacity: 0.92, duration: 0.25, ease: "power2.out" }, 0);
    this._tl.to(lineMat, { opacity: 0.85, duration: 0.25, ease: "power2.out" }, 0);

    // Slide out
    this._tl.to(this.wedgeGroup.position, {
      x: 0.9,
      duration: 0.55,
      ease: "power2.out"
    }, 0);

    return this._tl;
  }

  hide() {
    if (!this.isRevealed) return;
    this.isRevealed = false;

    if (this._tl) this._tl.kill();

    const wedgeMat = this.wedgeGroup.userData.wedge.material;
    const lineMat = this.wedgeGroup.userData.hypo.material;

    this._tl = gsap.timeline({
      onComplete: () => {
        this.wedgeGroup.visible = false;
      }
    });

    this._tl.to(wedgeMat, { opacity: 0.0, duration: 0.15, ease: "power2.out" }, 0);
    this._tl.to(lineMat, { opacity: 0.0, duration: 0.15, ease: "power2.out" }, 0);
    this._tl.to(this.wedgeGroup.scale, {
      x: 0.01, y: 0.01, z: 0.01,
      duration: 0.18,
      ease: "power2.out"
    }, 0);
    this._tl.to(this.wedgeGroup.position, { x: 0.0, duration: 0.18 }, 0);
    this._tl.to(this.clayMesh.material, {
      opacity: 1.0,
      duration: 0.22,
      ease: "power2.out"
    }, 0.05);

    return this._tl;
  }
}

// ===========================================
// VoxelGenerator Class
// ===========================================

class VoxelGenerator {
  constructor() {
    this.mesh = null;
    this._dummy = new THREE.Object3D();
  }

  removeFrom(parent) {
    if (!this.mesh) return;
    parent.remove(this.mesh);
    this.mesh.geometry.dispose();
    this.mesh.material.dispose();
    this.mesh = null;
  }

  createBlock({ s, l, depth, unitSize, gap = 0.04 }) {
    const count = s * l * depth;
    const boxSize = unitSize * (1 - gap);

    const geom = new THREE.BoxGeometry(boxSize, boxSize, boxSize);
    const mat = new THREE.MeshStandardMaterial({
      color: 0x44aaff,
      roughness: 0.25,
      metalness: 0.05,
      transparent: true,
      opacity: 0.0,
      depthWrite: false
    });

    const inst = new THREE.InstancedMesh(geom, mat, count);
    inst.instanceMatrix.setUsage(THREE.DynamicDrawUsage);

    const offsetX = (l - 1) * 0.5;
    const offsetY = (s - 1) * 0.5;
    const offsetZ = (depth - 1) * 0.5;

    let idx = 0;
    for (let z = 0; z < depth; z++) {
      for (let y = 0; y < s; y++) {
        for (let x = 0; x < l; x++) {
          this._dummy.position.set(
            (x - offsetX) * unitSize,
            (y - offsetY) * unitSize,
            (z - offsetZ) * unitSize
          );
          this._dummy.updateMatrix();
          inst.setMatrixAt(idx++, this._dummy.matrix);
        }
      }
    }
    inst.instanceMatrix.needsUpdate = true;

    this.mesh = inst;
    inst.scale.setScalar(1.0);
    mat.opacity = 0.0;

    return inst;
  }

  animateEntry() {
    if (!this.mesh) return;
    const mat = this.mesh.material;

    gsap.killTweensOf(mat);
    gsap.to(mat, { opacity: 0.65, duration: 0.4, ease: "power2.out" });
    gsap.fromTo(
      this.mesh.scale,
      { x: 0.01, y: 0.01, z: 0.01 },
      { x: 1, y: 1, z: 1, duration: 0.9, ease: "elastic.out(1,0.55)" }
    );
  }

  animateExit(onComplete) {
    if (!this.mesh) { onComplete?.(); return; }
    const mat = this.mesh.material;

    gsap.to(mat, { opacity: 0.0, duration: 0.2, ease: "power2.out" });
    gsap.to(this.mesh.scale, {
      x: 0.01, y: 0.01, z: 0.01,
      duration: 0.2,
      ease: "power2.out",
      onComplete
    });
  }
}

// ===========================================
// CameraRig Class
// ===========================================

class CameraRig {
  constructor(camera, controls) {
    this.camera = camera;
    this.controls = controls;

    this.defaultPos = new THREE.Vector3(0, 8, 22);
    this.defaultTarget = new THREE.Vector3(0, -4, 0);

    this.isoPos = new THREE.Vector3(18, 18, 18);
    this.isoTarget = new THREE.Vector3(0, -4, 0);

    this.isIso = false;
  }

  toIsometric() {
    this.isIso = true;
    gsap.to(this.camera.position, {
      x: this.isoPos.x, y: this.isoPos.y, z: this.isoPos.z,
      duration: 0.9,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
    gsap.to(this.controls.target, {
      x: this.isoTarget.x, y: this.isoTarget.y, z: this.isoTarget.z,
      duration: 0.9,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
  }

  toDefault() {
    this.isIso = false;
    gsap.to(this.camera.position, {
      x: this.defaultPos.x, y: this.defaultPos.y, z: this.defaultPos.z,
      duration: 0.9,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
    gsap.to(this.controls.target, {
      x: this.defaultTarget.x, y: this.defaultTarget.y, z: this.defaultTarget.z,
      duration: 0.9,
      ease: "power2.inOut",
      onUpdate: () => this.controls.update()
    });
  }
}

// ===========================================
// InteractionManager Class
// ===========================================

class InteractionManager {
  constructor({ camera, domElement, pickables, onHoverRow, onClickRow, onHoverNone }) {
    this.camera = camera;
    this.domElement = domElement;
    this.pickables = pickables;
    this.onHoverRow = onHoverRow;
    this.onClickRow = onClickRow;
    this.onHoverNone = onHoverNone;

    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
    this.hoveredRowId = null;

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
      if (this.hoveredRowId != null) {
        this.hoveredRowId = null;
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
    const hit = hits.find(h => h.object?.userData?.isClay);

    if (!hit) {
      if (this.hoveredRowId != null && !isClick) {
        this.hoveredRowId = null;
        this.onHoverNone();
      }
      return;
    }

    const row = hit.object.userData.row;
    if (!row) return;

    if (isClick) {
      const isShift = e.shiftKey;
      this.onClickRow(row, isShift);
    } else if (this.hoveredRowId !== row.row_id) {
      this.hoveredRowId = row.row_id;
      this.onHoverRow(row);
    }
  }
}

// ===========================================
// Build Rows
// ===========================================

const rows = plimptonData.rows.map((rowData, idx) => {
  const row = new PlimptonRow(rowData, idx);
  scene.add(row.group);
  return row;
});

const pickables = rows.map(r => r.clayMesh);
const voxels = new VoxelGenerator();
let voxelAttachedTo = null;
const cameraRig = new CameraRig(camera, controls);

// ===========================================
// UI Functions
// ===========================================

function buildRowList() {
  const listEl = document.getElementById("row-list");
  listEl.innerHTML = "";

  plimptonData.rows.forEach((row, idx) => {
    const prevRow = idx > 0 ? plimptonData.rows[idx - 1] : null;
    const deltaAngle = prevRow ? row.angleDeg - prevRow.angleDeg : 0;

    const item = document.createElement("div");
    item.className = "row-item";
    item.dataset.rowId = row.row_id;

    // Use exact rational formatter for pitch (s/l)
    const pitchSex = formatSexagesimalRational(row.s, row.l, 2);

    item.innerHTML = `
      <span class="row-idx">${ROMAN_NUMERALS[row.row_id]}</span>
      <div class="row-content">
        <div class="row-pitch">
          ${pitchSex}
          <span class="row-pitch-decimal">(${toFixedTrim(row.ratio, 3)})</span>
        </div>
        <div class="row-secondary">
          <span class="row-angle">${toFixedTrim(row.angleDeg, 2)}°</span>
          ${prevRow ? `<span class="row-smidge ${deltaAngle > -0.6 ? 'steep' : ''}">▼ ${toFixedTrim(Math.abs(deltaAngle), 2)}°</span>` : ''}
          ${row.pitchPer12 ? `<span>${row.pitchPer12}</span>` : ''}
        </div>
      </div>
      ${row.isUnitTriangle ? '<span class="row-tag special">3-4-5</span>' : ''}
    `;

    item.addEventListener("click", (e) => {
      handleRowClick(row, e.shiftKey);
    });

    item.addEventListener("mouseenter", () => {
      if (selectedRow?.row_id !== row.row_id) {
        handleRowHover(row);
      }
    });

    listEl.appendChild(item);
  });
}

function updateRowListSelection() {
  document.querySelectorAll(".row-item").forEach(el => {
    el.classList.remove("active", "compare");
    if (selectedRow && el.dataset.rowId == selectedRow.row_id) {
      el.classList.add("active");
    }
    if (compareRow && el.dataset.rowId == compareRow.row_id) {
      el.classList.add("compare");
    }
  });
}

function updateInspector(row) {
  const inspector = document.getElementById("inspector");
  const slopeDisplay = document.getElementById("slope-display");
  const btnVoxels = document.getElementById("btn-voxels");

  if (!row) {
    inspector.innerHTML = `
      <h3>Select a Row</h3>
      <p class="instruction">Hover over a clay bar to analyze its geometry.</p>
    `;
    slopeDisplay.style.display = "none";
    btnVoxels.style.display = "none";
    return;
  }

  const reduced = reduceTriple(row.s, row.l, row.d);

  // Original tablet notation
  const tablet = row.tablet || {};
  const tabletSection = tablet.colII ? `
    <div class="tablet-notation">
      <div class="tablet-notation-header">
        <span class="tablet-icon">𒀭</span> Original Tablet
        ${tablet.colI_damaged ? '<span class="damaged-badge">Col I damaged</span>' : ''}
      </div>
      <div class="tablet-values">
        <div class="tablet-col">
          <span class="tablet-col-label">II (s)</span>
          <span class="tablet-col-value">${tablet.colII}</span>
        </div>
        <div class="tablet-col">
          <span class="tablet-col-label">III (d)</span>
          <span class="tablet-col-value">${tablet.colIII}</span>
        </div>
        ${tablet.colI ? `
        <div class="tablet-col col-i">
          <span class="tablet-col-label">I (ratio)</span>
          <span class="tablet-col-value">${tablet.colI}</span>
        </div>
        ` : ''}
      </div>
    </div>
  ` : '';

  inspector.innerHTML = `
    <h3>Row ${ROMAN_NUMERALS[row.row_id]}</h3>
    ${tabletSection}
    <div class="inspector-grid">
      <div class="inspector-stat">
        <div class="inspector-stat-label">Short Side (s)</div>
        <div class="inspector-stat-value">${row.s.toLocaleString()}</div>
        <div class="inspector-stat-sub">${formatSexagesimalInt(row.s)}</div>
      </div>
      <div class="inspector-stat">
        <div class="inspector-stat-label">Long Side (l)</div>
        <div class="inspector-stat-value highlight">${row.l.toLocaleString()}</div>
        <div class="inspector-stat-sub">${formatSexagesimalInt(row.l)}</div>
      </div>
      <div class="inspector-stat">
        <div class="inspector-stat-label">Diagonal (d)</div>
        <div class="inspector-stat-value">${row.d.toLocaleString()}</div>
        <div class="inspector-stat-sub">${formatSexagesimalInt(row.d)}</div>
      </div>
      <div class="inspector-stat">
        <div class="inspector-stat-label">Reduced</div>
        <div class="inspector-stat-value">${reduced.s}–${reduced.l}–${reduced.d}</div>
        <div class="inspector-stat-sub">×${reduced.scaleFactor}</div>
      </div>
    </div>
    ${row.notes ? `<p style="margin-top: 12px; font-size: 0.85rem; color: var(--text-secondary); font-style: italic;">${row.notes}</p>` : ''}
  `;

  slopeDisplay.style.display = "block";
  updateSlopeContent(row);

  // Show voxels button for small rows
  if (reduced.s <= 10 && reduced.l <= 10) {
    btnVoxels.style.display = "block";
  } else {
    btnVoxels.style.display = "none";
  }
}

function updateSlopeContent(row) {
  if (!row) return;

  const content = document.getElementById("slope-content");
  let html = "";

  switch (currentSlopeTab) {
    case "degrees":
      html = `
        <div class="slope-value">${toFixedTrim(row.angleDeg, 3)}°</div>
        <div class="slope-note">Ramp angle from horizontal</div>
      `;
      break;
    case "ratio":
      html = `
        <div class="slope-value">${row.s}/${row.l}</div>
        <div class="slope-note">${formatSexagesimalFrac(row.ratio, 3)} ≈ ${toFixedTrim(row.ratio, 4)}</div>
      `;
      break;
    case "pitch":
      html = `
        <div class="slope-value">${row.pitchPer12} pitch</div>
        <div class="slope-note">Rise per 12 units of run (carpenter notation)</div>
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

  if (!selectedRow || !compareRow) {
    overlay.style.display = "none";
    return;
  }

  const deltaAngle = compareRow.angleDeg - selectedRow.angleDeg;
  const deltaRatio = compareRow.ratio - selectedRow.ratio;

  overlay.style.display = "block";
  dataEl.innerHTML = `
    <div class="compare-row">
      <span>Row ${ROMAN_NUMERALS[selectedRow.row_id]}:</span>
      <span>${toFixedTrim(selectedRow.angleDeg, 2)}° | ${formatSexagesimalFrac(selectedRow.ratio, 2)}</span>
    </div>
    <div class="compare-row">
      <span>Row ${ROMAN_NUMERALS[compareRow.row_id]}:</span>
      <span>${toFixedTrim(compareRow.angleDeg, 2)}° | ${formatSexagesimalFrac(compareRow.ratio, 2)}</span>
    </div>
    <div class="compare-delta">
      Δθ = ${toFixedTrim(deltaAngle, 2)}° | Δr = ${toFixedTrim(deltaRatio, 4)}
    </div>
  `;
}

// ===========================================
// Interaction Handlers
// ===========================================

function handleRowHover(rowData) {
  // Hide all except hovered
  rows.forEach(r => {
    if (r.data.row_id === rowData.row_id) {
      r.reveal();
    } else if (!selectedRow || r.data.row_id !== selectedRow.row_id) {
      r.hide();
    }
  });

  // Update inspector if no selection locked
  if (!selectedRow) {
    updateInspector(rowData);
  }
}

function handleRowClick(rowData, isShift) {
  if (isShift && selectedRow && selectedRow.row_id !== rowData.row_id) {
    // Compare mode
    compareRow = rowData;
    const rowObj = rows.find(r => r.data.row_id === rowData.row_id);
    rowObj?.reveal();
  } else {
    // Normal select
    if (compareRow) {
      const prevCompare = rows.find(r => r.data.row_id === compareRow.row_id);
      prevCompare?.hide();
      compareRow = null;
    }

    selectedRow = rowData;
    updateInspector(rowData);

    // Reveal selected, hide others
    rows.forEach(r => {
      if (r.data.row_id === rowData.row_id) {
        r.reveal();
      } else {
        r.hide();
      }
    });

    // Handle Row 11 special voxels
    handleVoxels(rowData);
  }

  updateRowListSelection();
  updateCompareOverlay();
}

function handleHoverNone() {
  if (!selectedRow) {
    rows.forEach(r => r.hide());
    updateInspector(null);

    // Clean up voxels
    if (voxelAttachedTo) {
      voxels.animateExit(() => {
        voxels.removeFrom(voxelAttachedTo);
        voxelAttachedTo = null;
      });
    }
  }
}

function handleVoxels(rowData) {
  const reduced = reduceTriple(rowData.s, rowData.l, rowData.d);

  // Only show for small reduced triples
  if (reduced.s > 10 || reduced.l > 10) {
    if (voxelAttachedTo) {
      voxels.animateExit(() => {
        voxels.removeFrom(voxelAttachedTo);
        voxelAttachedTo = null;
      });
    }
    return;
  }

  const rowObj = rows.find(r => r.data.row_id === rowData.row_id);
  if (!rowObj) return;

  const target = rowObj.wedgeGroup;

  if (voxelAttachedTo && voxelAttachedTo !== target) {
    voxels.removeFrom(voxelAttachedTo);
    voxelAttachedTo = null;
  }

  if (!voxelAttachedTo) {
    const targetLong = rowObj.targetLong;
    const unitSize = targetLong / reduced.l;

    const inst = voxels.createBlock({
      s: reduced.s,
      l: reduced.l,
      depth: 5,
      unitSize,
      gap: 0.06
    });

    inst.position.z -= 1.5;
    target.add(inst);
    voxelAttachedTo = target;

    // Animate in after a slight delay
    setTimeout(() => voxels.animateEntry(), 600);
  }
}

// ===========================================
// Event Listeners
// ===========================================

const interaction = new InteractionManager({
  camera,
  domElement: renderer.domElement,
  pickables,
  onHoverRow: handleRowHover,
  onClickRow: handleRowClick,
  onHoverNone: handleHoverNone
});

// Lens toggle
document.querySelectorAll(".lens-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    currentLens = btn.dataset.lens;
    updateLensUI();
  });
});

// Slope tabs
document.querySelectorAll(".slope-tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".slope-tab").forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    currentSlopeTab = tab.dataset.tab;
    if (selectedRow) updateSlopeContent(selectedRow);
  });
});

// Isometric toggle
document.getElementById("btn-iso").addEventListener("click", () => {
  isIsometric = !isIsometric;
  const btn = document.getElementById("btn-iso");

  if (isIsometric) {
    cameraRig.toIsometric();
    btn.classList.add("active");
    btn.innerHTML = '<span class="icon">⬡</span> Exit Isometric';
  } else {
    cameraRig.toDefault();
    btn.classList.remove("active");
    btn.innerHTML = '<span class="icon">⬡</span> Isometric Mode';
  }
});

// Clear compare
document.getElementById("btn-clear-compare").addEventListener("click", () => {
  if (compareRow) {
    const rowObj = rows.find(r => r.data.row_id === compareRow.row_id);
    rowObj?.hide();
    compareRow = null;
    updateRowListSelection();
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
    if (compareRow) {
      const rowObj = rows.find(r => r.data.row_id === compareRow.row_id);
      rowObj?.hide();
      compareRow = null;
    } else if (selectedRow) {
      selectedRow = null;
      rows.forEach(r => r.hide());
      updateInspector(null);
    }
    updateRowListSelection();
    updateCompareOverlay();
  }

  // Lens shortcuts
  if (e.key === "1") {
    currentLens = "ratio";
    updateLensUI();
  } else if (e.key === "2") {
    currentLens = "trig";
    updateLensUI();
  } else if (e.key === "3") {
    currentLens = "number";
    updateLensUI();
  }
});

// ===========================================
// Render Loop
// ===========================================

function tick() {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}

// ===========================================
// Initialize
// ===========================================

function init() {
  buildRowList();
  updateLensUI();

  // Hide loader
  setTimeout(() => {
    document.getElementById("loader").classList.add("hidden");
  }, 800);

  tick();
}

init();
