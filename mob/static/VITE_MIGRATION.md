# Vite Migration Guide

Migrating from Grunt + Bower to Vite for the minecraft.of.by project.

---

## ✅ Summary — What Was Actually Done

The migration is **complete**. A deliberately minimal, low-risk approach was
taken: Vite is used **only as a build tool** that reproduces the exact outputs
the legacy Grunt build produced. No template changes, no Bootstrap upgrade, no
vendor bundling.

**Changes:**
- Replaced **Grunt + Bower** with **Vite 5.x** (+ `less`); all `grunt-*` and
  Bower files removed (`Gruntfile.js`, `bower.json`, `.bowerrc`, `.jshintrc`,
  `.jshintignore`).
- Rewrote `package.json` (`type: module`, v2.0.0) with `dev` / `build` /
  `preview` scripts and only two dev dependencies: `vite` and `less`.
- Added `vite.config.js` and `src/index.js` (entry) that import
  `src/less/styles.less` and `src/js/main.js`.
- Build outputs use the **legacy file names** so `templates/base.html` is
  unchanged:
  - `src/less/styles.less` → `css/styles.min.css`
  - `src/js/main.js` → `js/app.min.js`
  - `src/js/ga.js` → `js/ga.js` (copied)
- **Kept Bootstrap 3** (bootswatch "slate"). Vendor libs (jQuery, Bootstrap,
  jquery.easing, lightbox2, mixitup, font-awesome, html5shiv, respond) remain in
  `js/`/`css/` and are loaded separately in `base.html` — **not** bundled by Vite.

**Build commands:**
```bash
cd mob/static
npm install
npm run build
```

> **Note:** The detailed step-by-step guide below documents the original, more
> ambitious plan (Bootstrap 5, bundled vendors, django-vite). It is kept for
> reference only — the implemented migration is the minimal approach summarized
> above. See **"Deploying to Production"** near the end for the prod steps.

---

## Overview

This guide walks through replacing:
- **Bower** → **npm** (unified package manager)
- **Grunt** → **Vite** (modern bundler)
- Keep LESS styling with Vite's built-in LESS support

**Migration time**: 2-3 hours  
**Zero changes needed** to Django backend

---

## Why Vite?

| Feature | Grunt | Vite |
|---------|-------|------|
| **Dev server** | Slow, file watching | Lightning-fast HMR |
| **Build speed** | Minutes | <1 second |
| **Module system** | Concatenation | Native ES modules |
| **Tree-shaking** | Manual | Automatic |
| **Setup complexity** | High | Low |
| **Maintenance** | Deprecated | Active (Vue team) |

---

## Step 1: Backup Current Setup

```bash
cd /home/dmitry/mob-site/mob/static

# Save current state
git add -A && git commit -m "Before Vite migration"

# Or create manual backup
cp -r . ../static-backup-$(date +%Y%m%d)
```

---

## Step 2: Clean Up and Initialize Vite

### 2.1 Remove Bower and Grunt

```bash
# Remove old tools
rm -rf bower_components node_modules
rm bower.json Gruntfile.js .jshintrc

# Keep package.json - we'll update it
```

### 2.2 Initialize npm and install Vite

```bash
# Update package.json with Vite dependencies
npm install --save-dev \
  vite@latest \
  less@latest \
  autoprefixer@latest \
  postcss@latest

# Install frontend dependencies (needed for styles/scripts)
npm install \
  jquery \
  bootstrap@5 \
  font-awesome@6 \
  lightbox2 \
  matchheight
```

---

## Step 3: Create Vite Configuration

Create `vite.config.js` in `/home/dmitry/mob-site/mob/static/`:

```javascript
import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
  root: __dirname,
  base: '/static/',
  
  build: {
    outDir: '.',  // Output to same directory
    emptyOutDir: false,
    manifest: true,
    
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/index.js'),
        styles: path.resolve(__dirname, 'src/index.less'),
      },
      output: {
        entryFileNames: 'js/[name].min.js',
        chunkFileNames: 'js/[name].[hash].min.js',
        assetFileNames: ({ name }) => {
          if (/\.css$/.test(name ?? '')) {
            return 'css/[name].min.[ext]'
          }
          return 'fonts/[name].[ext]'
        }
      }
    }
  },

  server: {
    middlewareMode: false,
    watch: {
      usePolling: true  // For Docker/VM compatibility
    }
  }
})
```

---

## Step 4: Reorganize Source Files

### 4.1 Create new directory structure

```bash
# Create src directory
mkdir -p src/js src/less src/fonts

# Move LESS files
mv css/src/less/* src/less/

# Move your JS files
mv src/js/*.js src/js/  # If not already there

# Move GA file
cp css/src/js/ga.js src/js/
```

### 4.2 Create entry point: `src/index.js`

```javascript
// Import styles
import './index.less'

// Import third-party JS
import jQuery from 'jquery'
window.$ = window.jQuery = jQuery

// Import bootstrap (if using it)
import 'bootstrap'

// Import your custom scripts
import './main.js'
import './ga.js'

// Import lightbox
import lightbox from 'lightbox2'
import 'lightbox2/dist/css/lightbox.min.css'
```

### 4.3 Create entry point: `src/index.less`

```less
// Import Bootstrap 5
@import "../../node_modules/bootstrap/scss/bootstrap.scss";

// Import Font-Awesome
@import "../../node_modules/font-awesome/less/font-awesome.less";

// Your custom styles
@import "./styles.less";
@import "./custom.less";
@import "./process.less";
@import "./projects.less";
@import "./timeline.less";
@import "./lightbox.less";
```

---

## Step 5: Update package.json

Replace scripts section:

```json
{
  "name": "minecraft-of-by",
  "version": "2.0.0",
  "description": "UI theme for minecraft.of.by project",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "less": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  },
  "dependencies": {
    "jquery": "^3.7.0",
    "bootstrap": "^5.3.0",
    "font-awesome": "^6.4.0",
    "lightbox2": "^2.11.0",
    "matchheight": "^0.7.2"
  }
}
```

---

## Step 6: Create PostCSS Configuration

Create `postcss.config.js`:

```javascript
export default {
  plugins: {
    autoprefixer: {}
  }
}
```

---

## Step 7: Update Django Template

Update `templates/base.html` to reference Vite assets:

```html
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <!-- Development: Vite HMR (only for dev server) -->
    {% if debug %}
        <script type="module" src="http://localhost:5173/@vite/client"></script>
        <script type="module" src="http://localhost:5173/src/index.js"></script>
    {% else %}
        <!-- Production: Use built assets -->
        {% comment %} Vite generates manifest.json for production {% endcomment %}
        <link rel="stylesheet" href="{% static 'css/main.min.css' %}">
    {% endif %}
</head>
<body>
    <!-- ... rest of template ... -->
    
    {% if not debug %}
        <script src="{% static 'js/main.min.js' %}"></script>
    {% endif %}
</body>
</html>
```

**Or use Django Vite package** (recommended for cleaner integration):

```bash
pip install django-vite
```

Then in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_vite',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django_vite.context_processors.vite_dev_server',
            ],
        },
    },
]
```

And in template:

```html
{% load django_vite %}

<!DOCTYPE html>
<html>
<head>
    {% vite_style "src/index.less" %}
</head>
<body>
    {% vite_script "src/index.js" %}
</body>
</html>
```

---

## Step 8: Test Development Server

```bash
cd /home/dmitry/mob-site/mob/static

# Install dependencies
npm install

# Start Vite dev server
npm run dev

# In another terminal, start Django
cd /home/dmitry/mob-site/mob
python manage.py runserver
```

Access Django app at `http://localhost:8000`  
Vite dev server runs at `http://localhost:5173` (HMR only)

**Features:**
- Edit LESS files → instant reload
- Edit JS → instant module replacement
- Console shows Vite messages

---

## Step 9: Build for Production

```bash
cd /home/dmitry/mob-site/mob/static
npm run build
```

Outputs:
- `js/index.min.js` - Minified JavaScript
- `css/index.min.css` - Minified CSS
- `manifest.json` - Asset manifest for Django

---

## Step 10: Collect Static Files

```bash
cd /home/dmitry/mob-site/mob
python manage.py collectstatic --noinput
```

This copies all static files to the location Apache serves from.

---

## Step 11: Update Apache Config

Your Apache config already points to `/home/dmitry/mob-site/mob/static/`, but ensure these rewrite rules work:

```apache
# In xn--80ashg.xn--90ais.conf and xn--80ashg.xn--90ais-le-ssl.conf

# serve static files using the /static/ format
RewriteCond %{REQUEST_FILENAME} ^/static/(.*)
RewriteCond /home/dmitry/mob-site/mob/static/%1 -f
RewriteRule ^/static/(.+)$ /home/dmitry/mob-site/mob/static/$1 [L]
```

Restart Apache:

```bash
sudo apache2ctl configtest
sudo systemctl restart apache2
```

---

## File Structure After Migration

```
mob/static/
├── src/
│   ├── index.js           # Main entry point
│   ├── index.less         # Main styles entry
│   ├── js/
│   │   ├── main.js
│   │   ├── ga.js
│   │   └── ...
│   └── less/
│       ├── styles.less
│       ├── custom.less
│       ├── process.less
│       ├── projects.less
│       ├── timeline.less
│       └── lightbox.less
├── js/
│   ├── index.min.js       # Generated
│   └── ...
├── css/
│   ├── index.min.css      # Generated
│   └── ...
├── fonts/                 # Generated/copied
├── img/
├── icons/
├── vite.config.js
├── postcss.config.js
├── package.json
├── package-lock.json
└── manifest.json          # Generated (production)
```

---

## Troubleshooting

### Port 5173 already in use?

```bash
# Find and kill process
lsof -i :5173
kill -9 <PID>

# Or specify different port in vite.config.js
server: {
  port: 5174
}
```

### Assets not loading in Django?

1. **Check STATIC_URL** in `settings.py`:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')
   ```

2. **Run collectstatic**:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Check Apache rewrite rules** point to correct path

### LESS not compiling?

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### JS errors in console?

1. Check `src/index.js` imports are correct
2. Verify jQuery is imported before Bootstrap
3. Check browser console for actual error

---

## Performance Gains

Before (Grunt):
- Development rebuild: 2-5 seconds
- Production build: 15-30 seconds
- No HMR

After (Vite):
- Development rebuild: <100ms
- Production build: <2 seconds
- Instant HMR for LESS/JS

---

## Next Steps (Optional)

1. **Remove jQuery** when no longer needed (5+ years modern)
   - Replace with vanilla JS or Alpine.js

2. **Upgrade Bootstrap**
   - Already at v5, no major breaking changes expected

3. **Replace Font-Awesome**
   - Consider web font optimization or SVG sprites

4. **Consider Tailwind**
   - Modern alternative to Bootstrap
   - Smaller CSS bundles

---

## Deploying to Production

Steps to roll the Vite-based build out on the production server. This reflects
the **implemented** migration (minimal approach — see the summary at the top).

> The build outputs (`js/`, `css/`, `fonts/`) are gitignored and served directly
> by Apache, so they must be generated **on the server** (or built locally and
> copied up). They are not pulled in by `git pull`.

### 1. Pull the latest code

```bash
cd /home/dmitry/mob-site
git pull
```

### 2. Ensure Node.js is available

```bash
node --version   # needs >= 18.x
# If missing, install via your distro or nvm, e.g.:
# curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs
```

### 3. Install build dependencies and build

```bash
cd /home/dmitry/mob-site/mob/static
npm ci          # clean, reproducible install from package-lock.json
npm run build   # writes css/styles.min.css, js/app.min.js, js/ga.js
```

> Use `npm ci` in production for a reproducible install. Fall back to
> `npm install` if there is no `package-lock.json`.

### 4. (Optional) Verify the outputs

```bash
ls -la css/styles.min.css js/app.min.js js/ga.js
```

These are the exact files `templates/base.html` references — no template or
`settings.py` change is required.

### 5. Collect static files (if using `collectstatic`)

```bash
cd /home/dmitry/mob-site/mob
python manage.py collectstatic --noinput
```

Skip this if Apache serves directly from `mob/static/` (see the Apache config).

### 6. Reload the application

```bash
# Apache config test + reload (touch the WSGI file if using mod_wsgi)
sudo apache2ctl configtest
sudo systemctl reload apache2
# or: touch /home/dmitry/mob-site/etc/application.wsgi
```

### 7. Smoke test

- Load https://minecraft.of.by and hard-refresh (Ctrl+Shift+R) to bypass the
  long Apache cache (`Cache-Control: max-age=...`).
- Confirm styles load (`/static/css/styles.min.css`) and JS works
  (`/static/js/app.min.js` — page-scroll, project filtering/mixitup, lightbox).

### Cleanup on the server (one-time)

The old Grunt/Bower tooling is no longer needed:

```bash
cd /home/dmitry/mob-site/mob/static
rm -rf bower_components            # old Bower vendor dir, if present
# Gruntfile.js / bower.json are already removed from the repo
```

---

## Rollback Plan

If migration fails:

```bash
# Restore backup
rm -rf node_modules src vite.config.js
git checkout bower.json Gruntfile.js package.json
bower install
npm install
```

---

## References

- [Vite Docs](https://vitejs.dev/)
- [Django Vite Package](https://github.com/bndr/django-vite)
- [Bootstrap 5 Migration](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [LESS Language](https://lesscss.org/)
