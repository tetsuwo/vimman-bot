/**
 * Get HTML from URL
 *
 * @param  {String} url
 * @return {String} html
 */
function getHTML(url) {
    var html = '';

    $.ajax({
        dataType : 'html',
        url      : url,
        async    : false,
        success  : function(response, status) {
            html = response;
        }
    });

    return html;
}

/**
 * Get Preset Object for Component
 *
 * @return {Object}
 */
function getPresetComponent() {
    return {
        created: function() {
            this.$dispatch('content-created', this);
        },
        ready: function() {
            this.$dispatch('content-ready', this);
        },
        attached: function() {
            this.$dispatch('content-attached', this);
        },
        detached: function() {
            this.$dispatch('content-detached', this);
        },
        beforeDestroy: function() {
            this.$dispatch('content-beforeDestroy', this);
        },
        afterDestroy: function() {
            this.$dispatch('content-afterDestroy', this);
        }
    };
}

function buildQueryString(param, prefix) {
    var query = [];

    for(var p in param) {
        var k = prefix ? prefix + '[' + p + ']' : p, v = param[p];
        query.push(
            typeof v == 'object' ?
                buildQueryString(v, k) :
                encodeURIComponent(k) + '=' + encodeURIComponent(v)
        );
    }

    return query.join('&');
}

function getPages(startIndex, total, limit) {
    var pages = [];
    var per = total / limit;

    for (var i = startIndex; i <= per; i++) {
        pages.push(i);
    }

    return pages;
}

/**
 * Get Preset Object for List Component
 *
 * @return {Object}
 */
function getPresetListComponent(componentName) {
    return {

        template: getHTML('assets/js/app/components/' + componentName + '/template.html'),

        created: function () {
            console.log(componentName, 'component.created');
            this.fetch();
        },

        beforeDestroy: function() {
            console.log(componentName, 'component.beforeDestroy');
            this.$dispatch('content-beforeDestroy', this);
            this.notFound();
            this.loading(true);
        },

        methods: {
            fetch: function() {
                this.loading(true);

                var that        = this;
                var requestUri  = 'assets/js/app/components/' + componentName + '/dummy.json';
                var queryString = buildQueryString(this.$parent.conditions);
                var page        = this.$parent.conditions.page;
                console.log('queryString', queryString);

                window.setTimeout(function() {
                    $.ajax({
                            url      : requestUri + '?' + queryString,
                            dataType : 'json'
                        })
                        .done(function (response) {
                            console.log('success', response);
                            that.found(response, page);
                        })
                        .fail(function (response) {
                            console.log('failure', response);
                            that.notFound();
                        });

                        window.location.href = window.location.href + '?' + queryString;
                }, 800);
            },
            loading: function(flag) {
                this.$parent.isLoading = flag;
            },
            found: function(data, page) {
                console.log('found', data, page);
                this.$parent.result.list        = data.result;
                this.$parent.result.currentPage = page;
                this.$parent.result.pages       = getPages(page, data.total_count, 10);
                this.$parent.result.totalCount  = data.total_count;
                this.$parent.result.totalPage   = Math.ceil(data.total_count / 10);
                this.loading(false);
            },
            notFound: function() {
                this.$parent.result.list        = [];
                this.$parent.result.currentPage = 1;
                this.$parent.result.pages       = [];
                this.$parent.result.totalCount  = 0;
                this.$parent.result.currentPage = 1;
                this.loading(false);
            },
            remove: function(id) {
                console.log('remove', id);
                if (confirm('本当に削除しますか？')) {
                }
            },
            page: function(page) {
                console.log('page', page);
                this.$parent.conditions.page = page;
                this.fetch();
            },
            prevPage: function(e) {
                if ($(e.target).closest('li').hasClass('disabled')) {
                    return;
                }
                console.log('prevPage');
                var page = this.$parent.result.currentPage;
                page--;
                this.$parent.conditions.page = page;
                this.fetch();
            },
            nextPage: function(e) {
                if ($(e.target).closest('li').hasClass('disabled')) {
                    return;
                }
                console.log('nextPage');
                var page = this.$parent.result.currentPage;
                page++;
                this.$parent.conditions.page = page;
                this.fetch();
            }
        }
    };
}

/**
 * Merge component
 *
 * @param  {string} url
 * @return {string} html
 */
function mergeComponent(component) {
    return Vue.extend(
        jQuery.extend(
            getPresetComponent(),
            component
        )
    );
}


Vue.component('questions', getPresetListComponent('questions'));

Vue.component('questions-create', mergeComponent({
    template: getHTML('assets/js/app/components/questions-create/template.html')
}));

Vue.component('questions-update', mergeComponent({
    template: getHTML('assets/js/app/components/questions-update/template.html')
}));

Vue.component('operators', getPresetListComponent('operators'));

Vue.component('operators-create', mergeComponent({
    template: getHTML('assets/js/app/components/operators-create/template.html')
}));

Vue.component('operators-update', mergeComponent({
    template: getHTML('assets/js/app/components/operators-update/template.html')
}));

Vue.component('informations', getPresetListComponent('informations'));

Vue.component('informations-create', mergeComponent({
    template: getHTML('assets/js/app/components/informations-create/template.html')
}));

Vue.component('informations-update', mergeComponent({
    template: getHTML('assets/js/app/components/informations-update/template.html')
}));

Vue.component('responses', getPresetListComponent('responses'));

Vue.component('responses-create', mergeComponent({
    template: getHTML('assets/js/app/components/responses-create/template.html')
}));

Vue.component('responses-update', mergeComponent({
    template: getHTML('assets/js/app/components/responses-update/template.html')
}));

Vue.component('tweets', getPresetListComponent('tweets'));

Vue.component('pagination', Vue.extend({
    template: getHTML('assets/js/app/components/pagination/template.html')
}));

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

//;(function (exports) {
//
//    'use strict';
//
//    exports.app.nav = new Vue({
//        el: '#nav',
//
//        // data
//        data: {
//        },
//
//        // a custom directive to wait for the DOM to be updated
//        // before focusing on the input field.
//        // http://vuejs.org/guide/directives.html#Writing_a_Custom_Directive
//        directives: {
//        },
//
//        // computed property
//        // http://vuejs.org/guide/computed.html
//        computed: {
//        },
//
//        // methods that implement data logic.
//        // note there's no DOM manipulation here at all.
//        methods: {
//        }
//    });
//
//})(window);

;(function (exports) {

    'use strict';

    var routes = {};

    routes['/'] = function() {
        app.currentView = 'questions';
    };

    routes['/questions'] = function() {
        app.currentView = 'questions';
    };

    routes['/questions/create'] = function() {
        app.currentView = 'questions-create';
    };

    routes['/questions/:id/update'] = function() {
        app.currentView = 'questions-update';
    };

    routes['/questions/:id/delete'] = function() {
    };


    routes['/responses'] = function(view) {
        app.currentView = 'responses';
    };

    routes['/responses/create'] = function() {
        app.currentView = 'responses-create';
    };

    routes['/responses/:id/update'] = function() {
        app.currentView = 'responses-update';
    };

    routes['/responses/:id/delete'] = function() {
    };


    routes['/informations'] = function(view) {
        app.currentView = 'informations';
    };

    routes['/informations/create'] = function() {
        app.currentView = 'informations-create';
    };

    routes['/informations/:id/update'] = function() {
        app.currentView = 'informations-update';
    };


    routes['/tweets'] = function(view) {
        app.currentView = 'tweets';
    };


    routes['/operators'] = function(view) {
        app.currentView = 'operators';
    };

    routes['/operators/create'] = function() {
        app.currentView = 'operators-create';
    };

    routes['/operators/:id/update'] = function() {
        app.currentView = 'operators-update';
    };


    var router = new Router(routes);
    router.init();

})(window);
