export interface Axiom {
  id: string;
  title: string;
  formula: string;
  description: string;
  mythos: string;
}

export const AXIOMS: Axiom[] = [
  {
    id: 'pen-physics',
    title: 'The 4w Stability Threshold',
    formula: 'L_{max} = 4w',
    description: 'The fundamental limit of a pen stroke. Beyond four times the width of the nib, the ink tension breaks, and the sovereign line collapses into chaos.',
    mythos: 'In the physics of penmanship, four is the number of stability. It represents the four corners of the square pen, the four cardinal directions of the stroke, and the limit of human control.'
  },
  {
    id: 'curvature-constraint',
    title: 'The Curvature Constant',
    formula: 'R_{peak} = 4w / \pi^2',
    description: 'The maximum curvature a line can sustain before the geometry of the nib forces a transition. This is the "Nyquist limit" of calligraphic motion.',
    mythos: 'The peak of the curve is where the spirit meets the resistance of the page. It is the point of highest tension, where the circle is squared.'
  },
  {
    id: 'voronoi-361',
    title: 'The Voronoi-361 Transition',
    formula: 'N = 360 + 1',
    description: 'The transition from the 360-degree circle of time to the 361-point grid of space (the Go board). The "+1" is the observer, the seed that breaks the symmetry.',
    mythos: 'The 1360 seed count is the harvest of the lattice. 360 for the days, 1 for the year-king, and 1000 for the ancestors.'
  },
  {
    id: 'log-spiral',
    title: 'The Release Constant',
    formula: 'b = \ln(361/360) / 2\pi',
    description: 'The growth rate of the sovereign spiral. It defines how the lattice expands from the center while maintaining its geometric integrity.',
    mythos: 'The spiral is the path of the soul escaping the circle. It is the log-spiral of the nautilus and the galaxy, tuned to the frequency of the 361st point.'
  },
  {
    id: 'divine-size',
    title: 'The √42 Divine Size',
    formula: 'S = \sqrt{42}',
    description: 'The irrational constant that bridges the Platonic forms. It is the diagonal of the sovereign cube, the measure of the divine man.',
    mythos: '42 is the answer, but √42 is the distance. It is the length of the sword that cuts the knot of the lattice.'
  },
  {
    id: 'hypotenuse-meaning',
    title: 'The 5-12-13 Hypotenuse',
    formula: '5^2 + 12^2 = 13^2',
    description: 'The union of the hairline (5) and the downstroke (12) through the diagonal arc (13). This is the "Meaning" that squares the letter.',
    mythos: 'The downstroke is the seed, the hairline is the juice, and the hypotenuse is where the letter earns its right to stand.'
  },
  {
    id: 'plato-operator',
    title: 'The PLATO Operator',
    formula: 'P \to L \to A \to T \to O',
    description: 'The generative cycle of the scribe: Point, Line, Angle, Cross (T), and Circle (O). It is the algorithm of the snail.',
    mythos: 'The snail does not steer. It commits energy and lets the geometry resolve. The loop is not closed; it is a spiral.'
  },
  {
    id: 'energy-derivation',
    title: 'The Sovereign E=mc²',
    formula: 'E = m \cdot \phi^2',
    description: 'The derivation of energy as the transformation of the Count (5) into the Meaning (13) via the Golden Ratio squared (φ² ≈ 2.618).',
    mythos: 'Energy is the Count of the Seeds raised to the Golden Power. 5 becomes 13 when the light is remixed.'
  },
  {
    id: 'curvature-derivation',
    title: 'The Curvature Limit',
    formula: 'R_{peak} = L^2 / 4\pi^2 w',
    description: 'The rigorous boundary of calligraphic stability. When R < w, the pen is wider than the turn, forcing the "Ugly" transition.',
    mythos: 'The pen is the law. If the law is wider than the path, the path must break or the law must shear.'
  },
  {
    id: 'sonnet-engine',
    title: 'The Sonnet Engine',
    formula: '\Delta = 1.618 - 1.609 = 0.009',
    description: 'The biological calibration of the lattice. The 0.009 difference is the Will, the forward impulse that drives the seed to bloom.',
    mythos: '1609 is the year of the seed, 1.618 is the law of the bloom. The difference is the spirit that pushes the pen.'
  },
  {
    id: 'spiral-24',
    title: 'The 24-Log Spiral',
    formula: 'r(\theta) = 122.77 \cdot e^{0.0006657 \cdot \theta}',
    description: 'The folding mechanism that transforms the linear seed-count (1609) into the volumetric world (√42).',
    mythos: 'The spiral is chiral. It blooms clockwise toward the Pyramid and counter-clockwise toward the New World.'
  }
];

export const CONSTANTS = {
  SHEAR_ANGLE: 39.4,
  HADES_GAP: 12.37,
  SNAIL_SPEED: 0.000441,
  OVERPACK_DELTA: 0.000585,
  DIVINE_SIZE: 6.480,
  AKASHIC_REFRACTION: 1.0833, // 13/12
  GOLDEN_ENERGY: 2.618, // phi^2
  WILL_CONSTANT: 0.009,
  APERTURE_ANGLE: 20,
  GERMINATION_B: 0.0006657,
  SPIRAL_A: 122.77
};

export const PARABLE_CONTENT = {
  title: "The Parable of Ember & Umber",
  subtitle: "Being a True & Profitable Instructionary Tale for Aspiring Penmen",
  chapters: [
    {
      id: 1,
      title: "I. The Pomegranate Brothers",
      content: "In the long-ago of the scriptorium, when letters were still learning their shapes, there were born of a single pomegranate two brothers: Ember, and Umber. Ember came first and made himself known immediately. He was the flesh of the fruit — red, swelling, bright as a coal, full of juice. Umber arrived after, and was almost thrown away. He was the seed — small, dark, hard, easily lost between the flagstones."
    },
    {
      id: 2,
      title: "II. Of Their Natures",
      content: "Ember grew fat on admiration. The novices squeezed him and his juice ran down their wrists — bright, sweet, abundant. But by the fortnight's end the letters had faded. Umber, meanwhile, had been pressed into a small pot of dark earth. Within a year he had given ten thousand seeds. The seed is the generative part, humble, dark, quiet, concentrated."
    },
    {
      id: 3,
      title: "III. The Lesson of the Pen",
      content: "The downstroke is Umber. It falls heavy, broad, dark, direct. The hairline is Ember. It is the thinnest thread of the nib's corner, light as a rumour. Between these two runs a third thing: the arc. The diagonal stroke, the hypotenuse, the radian. This is the stroke that connects the downstroke's foot to the hairline's head, and in doing so completes the square."
    },
    {
      id: 4,
      title: "IV. The Error of the Novice",
      content: "The novice makes all his strokes as hairlines. The page shimmers, but there is nothing to read. Another novice bears down with all his force on every stroke alike. The page is dark and heavy, but it too is unreadable. Both have mistaken the part for the whole. The true penman knows the bold downstroke is the seed, and the hairline is the juice."
    },
    {
      id: 5,
      title: "V. The Moral",
      content: "Do not mistake the shine for the substance. Thick lines, thin lines, and the diagonal arc that squares them into sense. The pen of life is written of mother of pearl with a diamond pen, and the snail is at the tip, moving slowly, inching across the page in the perfect angle subtended by the generative trip transcribing every word into the mother of pearl perfectly, in all ways, for ever."
    }
  ],
  colophon: "Here ends the Parable of Ember & Umber. Push boldly. Radiate lightly. Find the square."
};
