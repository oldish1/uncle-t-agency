/* Cape Town as seen from Table Bay. x runs left to right (0..1), y is height from the top of the picture (0..1).
   Left to right: Signal Hill, Lion's Head, Table Mountain (flat top), Devil's Peak. */
export const base = 0.8; // where the city meets the water

export const ridge = [
  [0, 0.72], [0.04, 0.66], [0.09, 0.6], [0.13, 0.62], [0.16, 0.58], [0.19, 0.51], [0.22, 0.5], [0.245, 0.56], [0.27, 0.64],
  [0.3, 0.55], [0.34, 0.45], [0.37, 0.41], [0.4, 0.4], [0.68, 0.4], [0.71, 0.415], [0.74, 0.47], [0.77, 0.51], [0.8, 0.46],
  [0.83, 0.41], [0.86, 0.43], [0.9, 0.52], [0.95, 0.64], [1, 0.72]
];

/* CBD and Foreshore: [x, width, height], heights measured up from the base line */
const raw = [
  [0.31, 0.018, 0.045], [0.332, 0.02, 0.07], [0.356, 0.016, 0.055], [0.376, 0.024, 0.09], [0.404, 0.02, 0.12],
  [0.428, 0.026, 0.075], [0.456, 0.02, 0.165], /* Portside, the tallest */ [0.48, 0.022, 0.1], [0.506, 0.03, 0.06],
  [0.54, 0.018, 0.085], [0.562, 0.024, 0.05], [0.59, 0.02, 0.07], [0.614, 0.026, 0.045], [0.646, 0.02, 0.035]
];
export const buildings = raw.map(([x, w, h]) => [x, w, h * 1.35]);

/* Cape Town Stadium (Green Point), a low pale oval left of the CBD */
export const stadium = { x: 0.225, w: 0.06, h: 0.026 };

/* Harbour cranes right of the CBD: [x, height] */
export const cranes = [[0.69, 0.07], [0.715, 0.09], [0.74, 0.065]];

/* Pull the whole scene into the lower part of its frame so headlines sit in clear sky */
export const lift = (y, top = 0.3) => top + (1 - top) * y;

export function ridgeY(n) {
  let k = 1;
  while (k < ridge.length - 1 && n > ridge[k][0]) k++;
  const [x0, y0] = ridge[k - 1], [x1, y1] = ridge[k];
  const t = Math.min(1, Math.max(0, (n - x0) / (x1 - x0)));
  const e = t * t * (3 - 2 * t);
  return y0 + (y1 - y0) * e;
}
