# Plimpton 322: The Shape of Numbers

An interactive 3D visualization of Plimpton 322, the famous Babylonian clay tablet from c. 1800 BCE containing the world's oldest known trigonometric table.

**[Live Demo](https://plimpton-322.web.app)** | **[Documentation](docs/)**

> *"Babylonian trigonometry is exact, whereas we are accustomed to approximate trigonometry."*
> — Dr. Daniel Mansfield, UNSW Sydney

## Overview

This visualization interprets Plimpton 322 as **"A Catalog of Practical Slopes"** - presenting the tablet's 15 rows as a builder's reference for constructing ramps and inclines at precise angles. Each row encodes a Pythagorean triple (a right triangle with integer sides), ordered by slope from steepest (~45°) to flattest (~31°).

### Features

- **Interactive 3D Clay Bars**: Click any row to reveal its geometric wedge
- **Three Interpretation Lenses**:
  - *Builder*: Practical rise/run ratios for construction
  - *Trig*: Early trigonometric table perspective
  - *Number Theory*: Scribal exercise in "regular" sexagesimal numbers
- **Authentic Sexagesimal Display**: Numbers shown in base-60 notation
- **Isometric & Perspective Views**: Switch camera modes for different analysis
- **Compare Mode**: Analyze multiple rows side-by-side
- **Reconstruction Toggle**: Show/hide the hypothetical missing Column 0

## Installation

```bash
git clone https://github.com/midnightnow/plimpton322-viz.git
cd plimpton322-viz
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Build for Production

```bash
npm run build
npm run preview  # Test production build locally
```

## Technology Stack

- **[Three.js](https://threejs.org/)** - 3D rendering
- **[GSAP](https://greensock.com/gsap/)** - Animation
- **[Vite](https://vitejs.dev/)** - Build tooling

## The Tablet

Plimpton 322 is a Babylonian clay tablet, believed to have been written around 1800 BCE during the Old Babylonian period, likely in the ancient city of Larsa (modern-day Iraq). It is currently housed at Columbia University's Rare Book and Manuscript Library.

The tablet contains a table of 15 rows and 4 columns of numbers written in sexagesimal (base-60) cuneiform script. The left edge is broken, suggesting there may have been additional columns.

### The Mathematical Content

Each row contains a **Pythagorean triple** - three integers (s, l, d) satisfying:

```
s² + l² = d²
```

Where:
- **s** = short side of the right triangle
- **l** = long side (always a "regular" number in base-60)
- **d** = diagonal (hypotenuse)

The rows are ordered by decreasing slope angle, from approximately 45° down to 31°.

## Academic References

This visualization is informed by the following scholarly works:

### Primary Source Interpretation

1. **Mansfield, D.F., & Wildberger, N.J.** (2017). "Plimpton 322 is Babylonian exact sexagesimal trigonometry." *Historia Mathematica*, 44(4), 395-419. [https://doi.org/10.1016/j.hm.2017.08.001](https://doi.org/10.1016/j.hm.2017.08.001)

   > *Key insight*: The tablet is an exact ratio-based trigonometric table using sexagesimal arithmetic, predating Greek trigonometry by over 1,000 years.

2. **Robson, E.** (2001). "Neither Sherlock Holmes nor Babylon: A Reassessment of Plimpton 322." *Historia Mathematica*, 28(3), 167-206. [https://doi.org/10.1006/hmath.2001.2317](https://doi.org/10.1006/hmath.2001.2317)

   > *Key insight*: The tablet likely served as a teacher's aid for generating problems involving reciprocal pairs, emphasizing pedagogical context.

3. **Britton, J.P., Proust, C., & Shnider, S.** (2011). "Plimpton 322: A Review and a Different Perspective." *Archive for History of Exact Sciences*, 65(5), 519-566.

   > *Key insight*: Analysis of scribal errors and tablet structure suggests systematic generation methods.

### Historical Context

4. **Neugebauer, O., & Sachs, A.** (1945). *Mathematical Cuneiform Texts*. American Oriental Society. (Original publication describing Plimpton 322)

5. **Friberg, J.** (2007). *A Remarkable Collection of Babylonian Mathematical Texts*. Springer.

### The "Practical Slopes" Interpretation

This visualization adopts the Mansfield-Wildberger interpretation that the tablet served as a practical reference for builders and surveyors, with each row representing a specific slope that could be constructed using integer measurements - essentially a "lookup table" for ancient construction.

The three interpretation lenses allow users to explore alternative scholarly perspectives:
- **Builder Lens**: Practical construction ratios
- **Trig Lens**: Trigonometric function values
- **Number Lens**: Regular number exercises

## Data Sources

The tablet data in `src/data/plimpton322.json` is compiled from:
- CDLI (Cuneiform Digital Library Initiative): [P254790](https://cdli.ucla.edu/P254790)
- High-resolution imagery from Columbia University Libraries
- Transcriptions verified against Robson (2001) and Mansfield & Wildberger (2017)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

**Design & Development**: [Influential Digital](https://influential.digital)

**Academic Consultation**: Based on peer-reviewed research in the history of mathematics.

**Artifact**: Plimpton 322 is the property of Columbia University, New York. Catalog number: CULC 322.

---

*"This is not just the world's oldest trig table - it's also the most accurate, because it uses exact ratios instead of approximations."*
— Daniel Mansfield, UNSW Sydney

## Citation

If you use this visualization in academic work, please cite:

```bibtex
@software{plimpton322viz,
  author = {{Influential Digital}},
  title = {Plimpton 322: The Shape of Numbers - Interactive Visualization},
  year = {2025},
  url = {https://github.com/midnightnow/plimpton322-viz},
  note = {Based on Mansfield \& Wildberger (2017) interpretation}
}
```
