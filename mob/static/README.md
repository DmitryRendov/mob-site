# MOB-site UI #

UI theme for the minecraft.of.by project. The frontend is built with
[Vite](https://vitejs.dev/) (replacing the legacy Grunt + Bower toolchain).

## Prerequisites ##

- Node.js >= 18.x
- npm

## What Vite builds ##

Vite compiles the custom sources from `src/` back into the static tree using the
same file names the templates already reference (no Django template changes needed):

| Source                 | Output               |
|------------------------|----------------------|
| `src/less/styles.less` | `css/styles.min.css` |
| `src/js/main.js`       | `js/app.min.js`      |
| `src/js/ga.js`         | `js/ga.js` (copied)  |

Vendor libraries (jQuery, Bootstrap 3, jquery.easing, lightbox2, mixitup,
font-awesome, html5shiv, respond) live in `js/` and `css/` and are loaded
separately in `templates/base.html`. They are intentionally **not** bundled by
Vite, so runtime behaviour is identical to the old Grunt setup.

## Installation ##

Install the build dependencies:
```bash
npm install
```

## Building the static assets ##

Create the minified UI assets:
```bash
npm run build
```

Other available scripts:
```bash
npm run dev      # start the Vite dev server (HMR)
npm run preview  # preview a production build
```

Open the site in browser to http://minecraft.of.by

