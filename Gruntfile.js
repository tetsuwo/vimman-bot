module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'public/assets/js/project.js',
        dest: 'public/assets/js/project.min.js'
      }
    },
    concat: {
      backyard: {
        src: [
          'public/assets/js/app/helpers.js',
          'public/assets/js/app/components/questions/index.js',
          'public/assets/js/app/components/questions-create/index.js',
          'public/assets/js/app/components/questions-update/index.js',
          'public/assets/js/app/components/operators/index.js',
          'public/assets/js/app/components/operators-create/index.js',
          'public/assets/js/app/components/operators-update/index.js',
          'public/assets/js/app/components/informations/index.js',
          'public/assets/js/app/components/informations-create/index.js',
          'public/assets/js/app/components/informations-update/index.js',
          'public/assets/js/app/components/responses/index.js',
          'public/assets/js/app/components/responses-create/index.js',
          'public/assets/js/app/components/responses-update/index.js',
          'public/assets/js/app/components/tweets/index.js',
          'public/assets/js/app/components/pagination/index.js',
          'public/assets/js/app/app.js',
          'public/assets/js/app/main.js',
          'public/assets/js/app/nav.js',
          'public/assets/js/app/router.js',
        ],
        dest: 'public/assets/js/project.js'
      }
    },
    jshint: {
      files: [
        'Gruntfile.js',
        'public/assets/js/*/*.js',
        'public/assets/js/*/*/*.js',
        'public/assets/js/*/*/*/*.js'
      ],
      options: {
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true
        }
      }
    },
    watch: {
      scripts: {
        files: [
          'public/assets/js/*/*.js',
          'public/assets/js/*/*/*.js',
          'public/assets/js/*/*/*/*.js'
        ],
        tasks: ['jshint', 'concat', 'uglify']
      }
    }
  });

  // Load the plugins
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Register tasks
  grunt.registerTask('default', ['jshint', 'concat', 'uglify']);

};
