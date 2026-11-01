import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter({ pages: 'dist', assets: 'dist', fallback: undefined, strict: false }),
    prerender: { handleMissingId: 'ignore' }
  }
};
