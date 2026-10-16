/* Drop real files into public/media with these names and the site uses them automatically.
   Until a file exists, the frame shows the ember field instead. */
export const MEDIA = {
  hero: { src: 'media/hero.mp4', poster: 'media/hero.jpg' },
  laser: { src: 'media/laser.mp4', poster: 'media/laser.jpg' },
  brake: { src: 'media/brake.mp4', poster: 'media/brake.jpg' },
  shop: ['media/shop-1.jpg', 'media/shop-2.jpg', 'media/shop-3.jpg', 'media/shop-4.jpg']
};

/* public/media/manifest.json lists the files that really exist, so the site never requests a missing one. */
let cache;
export function loadManifest() {
  if (!cache) cache = fetch('media/manifest.json', { cache: 'no-cache' }).then(r => (r.ok ? r.json() : { files: [] })).then(j => new Set(j.files || [])).catch(() => new Set());
  return cache;
}
