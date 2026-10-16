import { useEffect, useRef, useState } from 'react';
import { useInView, useReducedMotion } from 'framer-motion';
import Embers from './Embers.jsx';
import { loadManifest } from './media.js';

/* A full-bleed video frame. Uses the real clip when it exists, the ember field until then. */
export default function MediaFrame({ media, cut = false, label, className = '' }) {
  const ref = useRef(null);
  const inView = useInView(ref, { margin: '200px' });
  const reduce = useReducedMotion();
  const [ready, setReady] = useState(false);
  const [failed, setFailed] = useState(true);
  useEffect(() => { loadManifest().then(s => { if (s.has(media.src)) setFailed(false); }); }, [media.src]);

  useEffect(() => {
    const v = ref.current?.querySelector('video'); if (!v) return;
    if (inView && !reduce) v.play().catch(() => {}); else v.pause();
  }, [inView, reduce, ready]);

  return (
    <div className={'media ' + className} ref={ref} role={label ? 'img' : undefined} aria-label={label} aria-hidden={label ? undefined : 'true'}>
      {!ready && <Embers cut={cut} />}
      {!failed && (
        <video className={'media-video' + (ready ? ' is-ready' : '')} src={media.src} poster={media.poster} muted loop playsInline preload="metadata"
          onLoadedData={() => setReady(true)} onError={() => setFailed(true)} />
      )}
    </div>
  );
}
