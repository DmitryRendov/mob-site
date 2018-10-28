/*
 * Gruntfile.js
 *
 * Copyright (c) 2016-2018 Dmitry Vl. Rendov
 * Licensed under the MIT license.
 * https://github.com/DmitryRendov/mob-site/blob/master/LICENSE
 */

'use strict';

module.exports = function(grunt) {

  var globalConfig = {
    images : 'img',
    styles : 'css',
    fonts : 'fonts',
    scripts : 'js',
    src : 'src',
    bower_path : 'bower_components'
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
          src : '<%= globalConfig.bower_path %>/jquery.easing/js/jquery.easing.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        },{
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/html5shiv/dist/html5shiv.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/bootswatch-dist/js/bootstrap.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/lightbox2/dist/js/lightbox.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/respond/dest/respond.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/jquery-mixitup/dist/mixitup.min.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.src %>/js/ga.js',
          dest : '<%= globalConfig.scripts %>/',
          filter : 'isFile'
        }, {
          expand : true,
          flatten : true,
          src : '<%= globalConfig.bower_path %>/bootswatch-dist/css/bootstrap.min.css',
          dest : '<%= globalConfig.styles %>/',
          filter : 'isFile'
        }, {
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
          src : '<%= globalConfig.bower_path %>/glyphicons-only-bootstrap/fonts/*',
          dest : '<%= globalConfig.fonts %>/',
          filter : 'isFile'
       }]
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
        src : ['<%= globalConfig.src %>/js/**/*.js', '!<%= globalConfig.src %>/js/**/ga.js'],
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
        banner : '/*! \n * <%= pkg.name %> <%= pkg.version %> (<%= pkg.homepage %>) \n * Copyright <%= grunt.template.today("yyyy") %> Dmitry Vl. Rendov \n * Licensed under MIT (https://github.com/DmitryRendov/mob-site/blob/master/LICENSE) \n */ \n'
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
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-clean');

  // Default task(s).
  grunt.registerTask('default', ['copy', 'clean:css', 'less', 'js']);
  grunt.registerTask('js', ['clean:js', 'concat', 'jshint', 'uglify']);

};
