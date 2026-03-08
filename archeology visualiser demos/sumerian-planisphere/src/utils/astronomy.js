/**
 * Sumerian Planisphere - Astronomical Utilities
 * Calculations for ancient Mesopotamian astronomy
 */

// ===========================================
// Sexagesimal (Base-60) Formatting
// ===========================================

/**
 * Convert decimal degrees to sexagesimal (DMS)
 * Babylonians used base-60 for astronomical calculations
 */
export function toSexagesimal(decimal) {
  const sign = decimal < 0 ? '-' : '';
  decimal = Math.abs(decimal);

  const degrees = Math.floor(decimal);
  const minutesDec = (decimal - degrees) * 60;
  const minutes = Math.floor(minutesDec);
  const seconds = Math.round((minutesDec - minutes) * 60);

  return {
    degrees,
    minutes,
    seconds,
    formatted: `${sign}${degrees};${minutes.toString().padStart(2, '0')},${seconds.toString().padStart(2, '0')}`,
    babylonian: formatBabylonianDegrees(degrees, minutes, seconds)
  };
}

/**
 * Format as Babylonian notation (US = 60s, USH = 60 USH)
 */
export function formatBabylonianDegrees(deg, min, sec) {
  // UŠ (degree) = 1° = 1/360 of circle
  // In Babylonian astronomy, they divided the circle into 360°
  // (based on ~365 days in year, rounded to 360 for sexagesimal convenience)
  return `${deg}° ${min}' ${sec}"`;
}

/**
 * Convert decimal to pure sexagesimal string (base-60)
 * Format: whole;fractional,fractional2
 */
export function toBase60String(decimal, fracPlaces = 2) {
  const whole = Math.floor(decimal);
  let frac = decimal - whole;

  let fracParts = [];
  for (let i = 0; i < fracPlaces; i++) {
    frac *= 60;
    fracParts.push(Math.floor(frac).toString().padStart(2, '0'));
    frac -= Math.floor(frac);
  }

  return `${whole};${fracParts.join(',')}`;
}

// ===========================================
// Celestial Coordinate Systems
// ===========================================

/**
 * Calculate Right Ascension from ecliptic longitude
 * Simplified formula assuming obliquity of ~23.44°
 */
export function eclipticToEquatorial(eclipticLong, eclipticLat, obliquity = 23.44) {
  const eps = obliquity * Math.PI / 180;
  const lambda = eclipticLong * Math.PI / 180;
  const beta = eclipticLat * Math.PI / 180;

  const sinRA = Math.sin(lambda) * Math.cos(eps) - Math.tan(beta) * Math.sin(eps);
  const cosRA = Math.cos(lambda);

  let ra = Math.atan2(sinRA, cosRA) * 180 / Math.PI;
  if (ra < 0) ra += 360;

  const sinDec = Math.sin(beta) * Math.cos(eps) + Math.cos(beta) * Math.sin(eps) * Math.sin(lambda);
  const dec = Math.asin(sinDec) * 180 / Math.PI;

  return { ra, dec };
}

/**
 * Calculate the altitude of a star at a given latitude and hour angle
 */
export function calculateAltitude(dec, lat, hourAngle) {
  const decRad = dec * Math.PI / 180;
  const latRad = lat * Math.PI / 180;
  const haRad = hourAngle * Math.PI / 180;

  const alt = Math.asin(
    Math.sin(decRad) * Math.sin(latRad) +
    Math.cos(decRad) * Math.cos(latRad) * Math.cos(haRad)
  );

  return alt * 180 / Math.PI;
}

/**
 * Calculate azimuth of a celestial object
 */
export function calculateAzimuth(dec, lat, hourAngle, altitude) {
  const decRad = dec * Math.PI / 180;
  const latRad = lat * Math.PI / 180;
  const haRad = hourAngle * Math.PI / 180;
  const altRad = altitude * Math.PI / 180;

  const cosAz = (Math.sin(decRad) - Math.sin(altRad) * Math.sin(latRad)) /
                (Math.cos(altRad) * Math.cos(latRad));

  let az = Math.acos(Math.max(-1, Math.min(1, cosAz))) * 180 / Math.PI;

  if (Math.sin(haRad) > 0) {
    az = 360 - az;
  }

  return az;
}

// ===========================================
// Mesopotamian Astronomical Constants
// ===========================================

// Latitude of ancient cities
export const ANCIENT_LATITUDES = {
  nineveh: 36.36,      // Nineveh (modern Mosul)
  babylon: 32.54,      // Babylon
  ur: 30.96,           // Ur
  uruk: 31.32          // Uruk
};

// Obliquity of ecliptic at different epochs (degrees)
export const OBLIQUITY = {
  modern: 23.44,       // J2000
  bce700: 23.66,       // 700 BCE (approx)
  bce3300: 24.01       // 3300 BCE (approx)
};

// Babylonian month names and their stellar associations
export const BABYLONIAN_MONTHS = [
  { number: 1, name: 'Nisannu', stars: 'Pleiades', season: 'Spring' },
  { number: 2, name: 'Aiaru', stars: 'Taurus', season: 'Spring' },
  { number: 3, name: 'Simanu', stars: 'Orion', season: 'Spring' },
  { number: 4, name: 'Du\'uzu', stars: 'Gemini', season: 'Summer' },
  { number: 5, name: 'Abu', stars: 'Leo', season: 'Summer' },
  { number: 6, name: 'Ululu', stars: 'Virgo', season: 'Summer' },
  { number: 7, name: 'Tashritu', stars: 'Libra', season: 'Autumn' },
  { number: 8, name: 'Arahsamnu', stars: 'Scorpius', season: 'Autumn' },
  { number: 9, name: 'Kislimu', stars: 'Sagittarius', season: 'Autumn' },
  { number: 10, name: 'Tebetu', stars: 'Capricornus', season: 'Winter' },
  { number: 11, name: 'Shabatu', stars: 'Aquarius', season: 'Winter' },
  { number: 12, name: 'Addaru', stars: 'Pisces', season: 'Winter' }
];

// ===========================================
// Star Calculations
// ===========================================

/**
 * Calculate the heliacal rising date for a star
 * (First visible rising just before dawn)
 * @param {number} ra - Right Ascension in degrees
 * @param {number} dec - Declination in degrees
 * @param {number} lat - Observer latitude
 * @param {number} year - Year (negative for BCE)
 * @returns {object} Approximate date and sun longitude
 */
export function calculateHeliacalRising(ra, dec, lat, year = -700) {
  // Simplified calculation
  // Star is visible when it rises at least 10° before the sun
  // and reaches 5° altitude before twilight

  const arcusvisionis = calculateArcusVisionis(dec);

  // Sun longitude when star has heliacal rising
  // This is an approximation: sun_long ≈ RA - 90 + correction
  let sunLong = (ra - 90 + arcusvisionis) % 360;
  if (sunLong < 0) sunLong += 360;

  // Convert sun longitude to approximate date
  // 0° Aries = March 21
  const daysFromEquinox = sunLong * 365.25 / 360;

  return {
    sunLongitude: sunLong,
    sunLongSexagesimal: toSexagesimal(sunLong),
    daysFromVernalEquinox: Math.round(daysFromEquinox),
    arcusVisionis: arcusvisionis
  };
}

/**
 * Calculate arcus visionis (minimum sun depression for star visibility)
 * Based on star's declination
 */
function calculateArcusVisionis(dec) {
  // Brighter stars near celestial equator need less sun depression
  // This is a simplified model
  const baseDep = 10; // degrees
  const decCorrection = Math.abs(dec) * 0.1;
  return baseDep + decCorrection;
}

/**
 * Calculate the angular separation between two celestial points
 */
export function angularSeparation(ra1, dec1, ra2, dec2) {
  const ra1Rad = ra1 * Math.PI / 180;
  const dec1Rad = dec1 * Math.PI / 180;
  const ra2Rad = ra2 * Math.PI / 180;
  const dec2Rad = dec2 * Math.PI / 180;

  const sep = Math.acos(
    Math.sin(dec1Rad) * Math.sin(dec2Rad) +
    Math.cos(dec1Rad) * Math.cos(dec2Rad) * Math.cos(ra1Rad - ra2Rad)
  );

  return sep * 180 / Math.PI;
}

// ===========================================
// Sector Calculations
// ===========================================

/**
 * Calculate sector properties based on angular division
 */
export function calculateSectorGeometry(sectorIndex, totalSectors = 8) {
  const anglePerSector = 360 / totalSectors;
  const startAngle = sectorIndex * anglePerSector;
  const endAngle = startAngle + anglePerSector;
  const midAngle = startAngle + anglePerSector / 2;

  return {
    startAngle,
    endAngle,
    midAngle,
    angleSpan: anglePerSector,
    startAngleSex: toSexagesimal(startAngle),
    endAngleSex: toSexagesimal(endAngle),
    // In Babylonian system, 1 UŠ = 4 minutes of time
    timeSpanMinutes: anglePerSector * 4,
    // Sector corresponds to this fraction of the year
    yearFraction: anglePerSector / 360,
    daysSpan: Math.round((anglePerSector / 360) * 365.25)
  };
}

/**
 * Calculate which sector a given ecliptic longitude falls into
 */
export function getSectorForLongitude(eclipticLong, rotation = 0) {
  const adjusted = (eclipticLong - rotation + 360) % 360;
  return Math.floor(adjusted / 45) + 1;
}

// ===========================================
// Display Formatting
// ===========================================

/**
 * Format a number to fixed decimal places, trimming trailing zeros
 */
export function toFixedTrim(num, digits = 2) {
  return parseFloat(num.toFixed(digits)).toString();
}

/**
 * Format hours:minutes:seconds
 */
export function formatHMS(hours) {
  const h = Math.floor(hours);
  const m = Math.floor((hours - h) * 60);
  const s = Math.round(((hours - h) * 60 - m) * 60);
  return `${h}h ${m}m ${s}s`;
}

/**
 * Format Right Ascension
 */
export function formatRA(degrees) {
  const hours = degrees / 15;
  return formatHMS(hours);
}

/**
 * Format star magnitude with visual indicator
 */
export function formatMagnitude(mag) {
  const stars = mag <= 1 ? '★★★' : mag <= 2 ? '★★' : mag <= 3 ? '★' : '·';
  return `${mag.toFixed(1)} ${stars}`;
}

// ===========================================
// Cuneiform Symbols (Unicode approximations)
// ===========================================

export const CUNEIFORM = {
  AN: '𒀭',      // Sky/Heaven/God determinative
  MUL: '𒀯',     // Star
  DINGIR: '𒀭', // God/Divine
  UD: '𒌓',     // Sun/Day
  SIN: '𒌍',    // Moon (approximation)
  KI: '𒆠',     // Earth/Place
  GUD: '𒄞',    // Bull
  SAG: '𒊕',    // Head
  UDU: '𒇻',    // Sheep

  // Numbers
  DISH: '𒁹',   // 1
  MIN: '𒈫',    // 2
  ESH: '𒐈',    // 3
  LIMMU: '𒐉', // 4
  IA: '𒐊',     // 5
  ASH: '𒐋',    // 6
  IMIN: '𒐌',   // 7
  USSU: '𒐍',   // 8
  ILIMMU: '𒐎', // 9
  U: '𒌋'       // 10
};

/**
 * Convert a number to cuneiform-style representation
 */
export function toCuneiformNumber(n) {
  if (n <= 0 || n > 59) return n.toString();

  const tens = Math.floor(n / 10);
  const ones = n % 10;

  let result = '';
  for (let i = 0; i < tens; i++) result += CUNEIFORM.U;

  const oneSymbols = ['', CUNEIFORM.DISH, CUNEIFORM.MIN, CUNEIFORM.ESH,
                     CUNEIFORM.LIMMU, CUNEIFORM.IA, CUNEIFORM.ASH,
                     CUNEIFORM.IMIN, CUNEIFORM.USSU, CUNEIFORM.ILIMMU];
  result += oneSymbols[ones] || '';

  return result || CUNEIFORM.DISH;
}
