(function (exports) {

    exports.Utils = {

        /**
         * Get HTML from URL
         *
         * @param  {String} url
         * @return {String} html
         */
        getHTML: function (url) {
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
        },

        buildQueryString: function (param, prefix) {
            var query = [];

            for (var p in param) {
                var k = prefix ? prefix + '[' + p + ']' : p, v = param[p];
                if (!k || !v) {
                    continue;
                }
                query.push(
                    typeof v == 'object' ?
                        Utils.buildQueryString(v, k) :
                        encodeURIComponent(k) + '=' + encodeURIComponent(v)
                );
            }

            return query.join('&');
        },

        parseQueryString: function (queryString) {
            var param = {};

            var queries = queryString.split('&');
            for (var q in queries) {
                var st = queries[q].split('=');
                console.log(q, st);
                if (st[0] && st[1]) {
                    param[st[0]] = st[1];
                }
            }

            return param;
        },

        _parseQueryString: function (queries, result) {
            var param = {};

            for (var q in queries) {
                var st = queries[q].split('=');
                console.log(q, st);
                if (st[0].match(/(.+)\[(.+)\]/)) {
                    console.log('_parseQueryString', RegExp.$1, RegExp.$2);
                } else {
                    param[st[0]] = st[1];
                }
            }

            return param;
        },

        getPages: function (startIndex, total, limit) {
            var pages = [];
            var per = total / limit;

            for (var i = startIndex; i <= per; i++) {
                pages.push(i);
            }

            return pages;
        },

        calcPagination: function (page, max, limit, delta) {
            var total = Math.ceil(max / limit);
            var alpha = 0;
            if (page <= delta) {
                alpha = delta - (page + 1);
            }
            var calc = page + delta + alpha;
            var pages = [];
            for (var i = page - delta; (i <= calc) && (i <= total); i++) {
                if (i < 1) {
                    continue;
                }
                pages.push(i);
            }

            return pages;
        }
    };

})(window);


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

/**
 * Get Preset Object for List Component
 *
 * @return {Object}
 */
function getPresetListComponent(componentName) {
    return {

        template: Utils.getHTML('assets/js/app/components/' + componentName + '/template.html'),

        created: function() {
            console.log(componentName, 'component.created');
            this.resetCondition();
            var matches = window.location.href.match(/\?(.*)/);
            if (matches && matches[1]) {
                var queries = Utils.parseQueryString(matches[1]);
                this.assignSearchForm(queries);
            }
            if (!this.search()) {
                this.fetch(this.$parent.conditions);
            }
            // TODO loginページを別の固定ページで設ける？？？
            if (componentName == 'login') {
                $('.navbar-nav').css({'visibility': 'hidden'});
            } else {
                $('.navbar-nav').css({'visibility': 'visible'});
            }
        },

        beforeDestroy: function() {
            console.log(componentName, 'component.beforeDestroy');
            this.$dispatch('content-beforeDestroy', this);
            this.notFound();
            this.loading(true);
        },

        methods: {
            fetch: function(conditions) {
                console.log('fetch', conditions);
                this.loading(true);

                var that        = this;
                //var requestUri  = 'assets/js/app/components/' + componentName + '/dummy.json';
                var requestUri  = 'http://www.vimmanbot.local/api/' + componentName;
                var queryString = Utils.buildQueryString(conditions);
                var page        = conditions.page;
                //console.log('queryString', queryString);

                window.setTimeout(function() {
                    $.ajax({
                            url      : requestUri + '?' + queryString,
                            headers  : {
                                'api-key': 'himejimaspecial'
                            },
                            dataType : 'json'
                        })
                        .done(function (response) {
                            console.log('success', response);
                            that.found(response, page);
                        })
                        .fail(function (response) {
                            console.log('failure', response);
                            that.notFound();
                        })
                        ;

                        var pushStateUrl = window.location.href.replace(/\?.*/, '');
                        console.log(pushStateUrl);
                        console.log(conditions);
                        pushStateUrl += conditions ? '?' + queryString : '';
                        console.log('pushStateUrl', window.location.href, ' => ', pushStateUrl);

                        window.location.href = pushStateUrl;
                }, 800);
            },

            loading: function(flag) {
                //console.log('loading', flag);
                this.$parent.isLoading = flag;
            },

            found: function(data, page) {
                console.log('found', data, 'page', page);
                this.$parent.result.list        = data.result;
                this.$parent.result.currentPage = page;
                //this.$parent.result.pages       = Utils.getPages(page, data.total_count, 10);
                this.$parent.result.pages       = Utils.calcPagination(page, data.total_count, 10, 4);
                this.$parent.result.totalCount  = data.total_count;
                this.$parent.result.totalPage   = Math.ceil(data.total_count / 10);
                this.loading(false);
            },

            notFound: function() {
                console.log('notFound');
                this.$parent.result.list        = [];
                this.$parent.result.currentPage = 1;
                this.$parent.result.pages       = [];
                this.$parent.result.totalCount  = 0;
                this.$parent.result.totalPage   = 0;
                this.$parent.result.currentPage = 1;
                this.loading(false);
            },

            resetCondition: function() {
                this.$parent.conditions = {};
                this.$parent.conditions.page = 1;
            },

            remove: function(id) {
                console.log('remove', id);
                if (confirm('本当に削除しますか？')) {
                }
            },

            page: function(page) {
                console.log('page', page);
                this.$parent.conditions.page = page;
                this.fetch(this.$parent.conditions);
            },

            prevPage: function(e) {
                if ($(e.target).closest('li').hasClass('disabled')) {
                    return;
                }
                //console.log('prevPage');
                var page = this.$parent.result.currentPage - 1;
                this.page(page);
            },

            nextPage: function(e) {
                if ($(e.target).closest('li').hasClass('disabled')) {
                    return;
                }
                //console.log('nextPage');
                var page = this.$parent.result.currentPage + 1;
                this.page(page);
            },

            search: function() {
                var $form = $(this.$el).find('.search-form');
                if ($form.size() !== 1) {
                    return false;
                }
                var formValues = {};
                var formArray = $form.serializeArray();
                for (var i in formArray) {
                    var form = formArray[i];
                    var matches = form.name.match(/search\[(.+)\]/);
                    if (matches && matches[1]) {
                        formValues[matches[1]] = form.value;
                    }
                }
                if (0 < formValues.length) {
                    this.$parent.conditions.search = formValues;
                }
                this.fetch(this.$parent.conditions);
            },

            assignSearchForm: function(queries) {
                for (var i in queries) {
                    var query = queries[i];
                    var formName = decodeURIComponent(i);
                    //console.log('assignSearchForm', formName, query);
                    $('[name="' + formName + '"]').val(query);
                }
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


Vue.component('login', getPresetListComponent('login'));

Vue.component('questions', getPresetListComponent('questions'));

Vue.component('questions-create', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/questions-create/template.html')
}));

Vue.component('questions-update', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/questions-update/template.html')
}));

Vue.component('operators', getPresetListComponent('operators'));

Vue.component('operators-create', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/operators-create/template.html')
}));

Vue.component('operators-update', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/operators-update/template.html')
}));

Vue.component('informations', getPresetListComponent('informations'));

Vue.component('informations-create', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/informations-create/template.html')
}));

Vue.component('informations-update', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/informations-update/template.html')
}));

Vue.component('responses', getPresetListComponent('responses'));

Vue.component('responses-create', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/responses-create/template.html')
}));

Vue.component('responses-update', mergeComponent({
    template: Utils.getHTML('assets/js/app/components/responses-update/template.html')
}));

Vue.component('tweets', getPresetListComponent('tweets'));

Vue.component('pagination', Vue.extend({
    template: Utils.getHTML('assets/js/app/components/pagination/template.html')
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

(function (exports) {

    'use strict';

    var routes = {};
    routes['/(questions)?(\\?.*)?'] = function() {
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
    routes['/responses(\\?.*)?'] = function(view) {
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
    routes['/informations(\\?.*)?'] = function(view) {
        app.currentView = 'informations';
    };
    routes['/informations/create'] = function() {
        app.currentView = 'informations-create';
    };
    routes['/informations/:id/update'] = function() {
        app.currentView = 'informations-update';
    };
    routes['/tweets(\\?.*)?'] = function(view) {
        app.currentView = 'tweets';
    };
    routes['/operators(\\?.*)?'] = function(view) {
        app.currentView = 'operators';
    };
    routes['/operators/create'] = function() {
        app.currentView = 'operators-create';
    };
    routes['/operators/:id/update'] = function() {
        app.currentView = 'operators-update';
    };
    routes['/login'] = function() {
        app.currentView = 'login'
    };
    var router = new Router(routes);
    router.init();

})(window);


$(function() {
    $('body').on('click', '.dialog', function(e) {
        // modalを動的取得 ajax
        console.log(777);
    });
});
