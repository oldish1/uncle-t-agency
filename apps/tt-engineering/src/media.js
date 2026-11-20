/* Drop real files into public/media with these names and the site uses them automatically.
   Until a file exists, the frame shows the ember field instead. */
export const MEDIA = {
  laser: { src: 'media/laser.mp4', poster: 'media/laser.jpg' },
  brake: { src: 'media/brake.mp4', poster: 'media/brake.jpg' },
  bend: { src: 'media/bend.mp4', poster: 'media/bend.jpg' }
};

/* public/media/manifest.json lists the files that really exist, so the site never requests a missing one. */
let cache;
export function loadManifest() {
  if (!cache) cache = fetch('media/manifest.json', { cache: 'no-cache' }).then(r => (r.ok ? r.json() : { files: [] })).then(j => new Set(j.files || [])).catch(() => new Set());
  return cache;
}
