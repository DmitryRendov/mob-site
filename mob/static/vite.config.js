import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// Vite replaces the old Grunt + Bower toolchain. It compiles the custom LESS
// and minifies the custom JS, writing them back into the static tree using the
// exact legacy file names so no Django templates need to change:
//   src/less/styles.less -> css/styles.min.css
//   src/js/main.js        -> js/app.min.js
export default defineConfig({
  base: '/static/',
  build: {
    outDir: '.',
    emptyOutDir: false,
    cssMinify: true,
    rollupOptions: {
      input: fileURLToPath(new URL('./src/index.js', import.meta.url)),
      output: {
        entryFileNames: 'js/app.min.js',
        assetFileNames: (assetInfo) => {
          const name = assetInfo.names?.[0] ?? assetInfo.name ?? ''
          if (name.endsWith('.css')) return 'css/styles.min.css'
          return 'assets/[name][extname]'
        },
      },
    },
  },
})
