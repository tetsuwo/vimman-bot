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
        afterDestroy: function() {
            this.$dispatch('content-afterDestroy', this);
        }
    };
}

function mergeComponent(component) {
    return Vue.extend(
        jQuery.extend(
            component,
            getPresetComponent()
        )
    );
}


Vue.component('questions', mergeComponent({
    template: getHTML('assets/js/app/components/questions/template.html')
}));

Vue.component('questions-create', mergeComponent({
    template: getHTML('assets/js/app/components/questions-create/template.html')
}));

Vue.component('questions-update', mergeComponent({
    template: getHTML('assets/js/app/components/questions-update/template.html')
}));

Vue.component('operators', mergeComponent({
    template: getHTML('assets/js/app/components/operators/template.html')
}));

Vue.component('operators-create', mergeComponent({
    template: getHTML('assets/js/app/components/operators-create/template.html')
}));

Vue.component('operators-update', mergeComponent({
    template: getHTML('assets/js/app/components/operators-update/template.html')
}));

Vue.component('informations', mergeComponent({
    template: getHTML('assets/js/app/components/informations/template.html')
}));

Vue.component('informations-create', mergeComponent({
    template: getHTML('assets/js/app/components/informations-create/template.html')
}));

Vue.component('informations-update', mergeComponent({
    template: getHTML('assets/js/app/components/informations-update/template.html')
}));

Vue.component('responses', mergeComponent({
    template: getHTML('assets/js/app/components/responses/template.html')
}));

Vue.component('responses-create', mergeComponent({
    template: getHTML('assets/js/app/components/responses-create/template.html')
}));

Vue.component('responses-update', mergeComponent({
    template: getHTML('assets/js/app/components/responses-update/template.html')
}));

Vue.component('tweets', mergeComponent({
    template: getHTML('assets/js/app/components/tweets/template.html')
}));

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
