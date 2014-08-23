(function (exports) {

    'use strict';

    exports.app = new Vue({

        el: '#app',

        data: {
            currentView: 'questions',
            isLoading: true,
            conditions: { page: 1 },
            result: {
                totalCount: 0,
                totalPage: 0,
                currentPage: 1,
                list: [],
                pages: []
            }
        },

        filters: {
            formatDate: function (v) {
                //return v.replace(/T|Z/g, ' ');
                return v.substr(0, v.length - 3);
            }
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
        },

        methods: {
        }
    });

})(window);
