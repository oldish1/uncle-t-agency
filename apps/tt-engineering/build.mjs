import { build, context } from 'esbuild';
import { cpSync, mkdirSync, rmSync, copyFileSync } from 'node:fs';

const watch = process.argv.includes('--watch');
rmSync('dist', { recursive: true, force: true });
mkdirSync('dist', { recursive: true });
copyFileSync('index.html', 'dist/index.html');
copyFileSync('styles.css', 'dist/styles.css');
cpSync('fonts', 'dist/fonts', { recursive: true });
cpSync('public', 'dist', { recursive: true });

const opts = {
  entryPoints: ['src/main.jsx'], bundle: true, minify: !watch, outfile: 'dist/app.js',
  jsx: 'automatic', target: 'es2020', format: 'iife', define: { 'process.env.NODE_ENV': '"production"' }, logLevel: 'info'
};
if (watch) { const c = await context(opts); await c.watch(); } else await build(opts);
