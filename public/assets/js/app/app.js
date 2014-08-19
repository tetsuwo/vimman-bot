;(function (exports) {

    'use strict';

    exports.app = new Vue({
        el: '#app',

        data: {
            currentView: 'questions'
        },

        created: function() {
            var that = this;
            this.$on('content-created', function (child) {
                console.log(that.$data.currentView, 'created');
            });
        },

        ready: function() {
            var that = this;
            this.$on('content-ready', function (child) {
                console.log(that.$data.currentView, 'ready');
            });
        },

        attached: function() {
            var that = this;
            this.$on('content-attached', function (child) {
                console.log(that.$data.currentView, 'attached');
            });
        },

        detached: function() {
            var that = this;
            this.$on('content-detached', function (child) {
                console.log(that.$data.currentView, 'detached');
            });
        },

        beforeDestroy: function() {
            var that = this;
            this.$on('content-beforeDestroy', function (child) {
                console.log(that.$data.currentView, 'beforeDestroy');
            });
        },

        afterDestroy: function() {
            var that = this;
            this.$on('content-afterDestroy', function (child) {
                console.log(that.$data.currentView, 'afterDestroy');
            });
        }
    });

})(window);
