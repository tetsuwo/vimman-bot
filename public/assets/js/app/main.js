//;(function (exports) {
//
//    'use strict';
//
//    exports.app.main = new Vue({
//        el: '#main',
//        data: {
//            currentView: 'questions'
//        },
//        created: function() {
//            var that = this;
//            this.$on('content-created', function (child) {
//                console.log(that.$data.currentView, 'created');
//            });
//        },
//        ready: function() {
//            var that = this;
//            this.$on('content-ready', function (child) {
//                console.log(that.$data.currentView, 'ready');
//            });
//        },
//        attached: function() {
//            var that = this;
//            this.$on('content-attached', function (child) {
//                console.log(that.$data.currentView, 'attached');
//            });
//        },
//        dettached: function() {
//            var that = this;
//            this.$on('content-dettached', function (child) {
//                console.log(that.$data.currentView, 'dettached');
//            });
//        },
//        beforeDestroy: function() {
//            var that = this;
//            this.$on('content-beforeDestroy', function (child) {
//                console.log(that.$data.currentView, 'beforeDestroy');
//            });
//        },
//        afterDestroy: function() {
//            var that = this;
//            this.$on('content-afterDestroy', function (child) {
//                console.log(that.$data.currentView, 'afterDestroy');
//            });
//        }
//    });
//
//})(window);
