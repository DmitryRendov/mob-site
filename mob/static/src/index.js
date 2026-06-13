// Build entry for Vite. Reproduces the legacy Grunt build outputs:
//   css/styles.min.css  (compiled + minified from src/less/styles.less)
//   js/app.min.js       (minified from src/js/main.js)
//
// Vendor libraries (jQuery, Bootstrap 3, jquery.easing, lightbox, mixitup) and
// ga.js are loaded separately in templates/base.html and are intentionally NOT
// bundled here, so the runtime behaviour stays identical to the Grunt setup.
import './less/styles.less'
import './js/main.js'
