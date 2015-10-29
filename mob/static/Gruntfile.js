/*
 * Gruntfile.js
 *
 * Copyright (c) 2014 Dmitry Vl. Rendov
 * Licensed under the MIT license.
 * https://github.com/DmitryRendov/nanny-theme/blob/master/LICENSE
 */

'use strict';

module.exports = function(grunt) {

  var globalConfig = {
    images : 'images',
    styles : 'css',
    fonts : 'fonts',
    scripts : 'js',
    src : 'src',
    bower_path : 'libraries'
  };

  grunt.initConfig({
    globalConfig : globalConfig,
    pkg : grunt.file.readJSON('package.json'),
    copy : {
      main : {
        files : [{
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/jquery/dist/jquery.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/html5shiv/dist/html5shiv.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/bootstrap/dist/js/bootstrap.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        },/* {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/bootstrap/dist/css/bootstrap.min.css',
          dest : '<%= globalConfig.styles %>/',
          filter : 'isFile'
        }*/ {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/font-awesome/css/font-awesome.min.css',
          dest : '<%= globalConfig.styles %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/font-awesome/fonts/*',
          dest : '<%= globalConfig.fonts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/respond/dest/respond.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }]
      }
    },
    modernizr : {

      dist : {
        // [REQUIRED] Path to the build you're using for development.
        "devFile" : '<%= globalConfig.bower_path %>/modernizr/modernizr.js',

        // [REQUIRED] Path to save out the built file.
        "outputFile" : '<%= globalConfig.scripts %>/modernizr-custom.min.js',

        // Based on default settings on http://modernizr.com/download/
        "extra" : {
          "shiv" : true,
          "printshiv" : false,
          "load" : true,
          "mq" : false,
          "cssclasses" : true
        },

        // Based on default settings on http://modernizr.com/download/
        "extensibility" : {
          "addtest" : false,
          "prefixed" : false,
          "teststyles" : false,
          "testprops" : false,
          "testallprops" : false,
          "hasevents" : false,
          "prefixes" : false,
          "domprefixes" : false
        },

        // By default, source is uglified before saving
        "uglify" : true,

        // Define any tests you want to implicitly include.
        "tests" : [],

        // By default, this task will crawl your project for references to Modernizr tests.
        // Set to false to disable.
        "parseFiles" : true,

        // When parseFiles = true, this task will crawl all *.js, *.css, *.scss files, except files that are in node_modules/.
        // You can override this by defining a "files" array below.
        // "files" : {
        // "src": []
        // },

        // When parseFiles = true, matchCommunityTests = true will attempt to
        // match user-contributed tests.
        "matchCommunityTests" : false,

        // Have custom Modernizr tests? Add paths to their location here.
        "customTests" : []
      }

    },
    clean : {
      js : ['<%= globalConfig.scripts %>/app.js', '<%= globalConfig.scripts %>/app.min.js'],
      css : ['<%= globalConfig.styles %>/styles.css', '<%= globalConfig.styles %>/styles.min.css']
    },
    less : {
      development : {
        options : {
          paths : ["styles"],
        },
        files : {
          "<%= globalConfig.styles %>/styles.css" : "<%= globalConfig.src %>/less/styles.less"
        }
      },
      production : {
        options : {
          paths : ["styles"],
          compress : true,
          yuicompress : true,
          optimization : 2,
          cleancss : true
        },
        files : {
          "<%= globalConfig.styles %>/styles.min.css" : "<%= globalConfig.src %>/less/styles.less"
        }
      }
    },
    watch : {
      styles : {
        files : ['<%= globalConfig.src %>/less/*.less'],
        tasks : ['less'],
        options : {
          nospawn : true
        }
      },
      scripts : {
        files : ['<%= globalConfig.src %>/js/*.js', '!app.js'],
        tasks : ['js'],
        options : {
          nospawn : true
        }
      }
    },
    concat : {
      dist : {
        src : ['<%= globalConfig.src %>/js/**/*.js'],
        dest : '<%= globalConfig.scripts %>/app.js',
        options : {
          banner : ";(function( window, undefined ){ \n 'use strict'; \n",
          footer : "\n}( window ));"
        }
      }
    },
    jshint : {
      all : ['Gruntfile.js', '<%= globalConfig.src %>/js/**/*.js'],
      options : {
        jshintrc : '.jshintrc'
      }
    },
    uglify : {
      options : {
        // the banner is inserted at the top of the output
        banner : '/*! \n * <%= pkg.name %> <%= pkg.version %> (<%= pkg.homepage %>) \n * Copyright <%= grunt.template.today("yyyy") %> Dmitry Vl. Rendov \n * Licensed under MIT (https://github.com/DmitryRendov/mob/blob/master/LICENSE) \n */ \n'
      },
      dist : {
        files : {
          '<%= globalConfig.scripts %>/app.min.js' : ['<%= concat.dist.dest %>']
        }
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks("grunt-modernizr");
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-clean');

  // Default task(s).
  grunt.registerTask('default', ['copy', 'modernizr', 'clean:css', 'less', 'js']);
  grunt.registerTask('js', ['clean:js', 'concat', 'jshint', 'uglify']);

};
