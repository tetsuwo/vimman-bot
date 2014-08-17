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

Vue.component('questions', Vue.extend({
    template: getHTML('assets/js/app/components/questions/template.html')
}));

Vue.component('questions-create', Vue.extend({
    template: getHTML('assets/js/app/components/questions-create/template.html')
}));

Vue.component('questions-update', Vue.extend({
    template: getHTML('assets/js/app/components/questions-update/template.html')
}));

Vue.component('operators', Vue.extend({
    template: getHTML('assets/js/app/components/operators/template.html')
}));

Vue.component('operators-create', Vue.extend({
    template: getHTML('assets/js/app/components/operators-create/template.html')
}));

Vue.component('operators-update', Vue.extend({
    template: getHTML('assets/js/app/components/operators-update/template.html')
}));

Vue.component('informations', Vue.extend({
    template: getHTML('assets/js/app/components/informations/template.html')
}));

Vue.component('informations-create', Vue.extend({
    template: getHTML('assets/js/app/components/informations-create/template.html')
}));

Vue.component('informations-update', Vue.extend({
    template: getHTML('assets/js/app/components/informations-update/template.html')
}));

Vue.component('responses', Vue.extend({
    template: getHTML('assets/js/app/components/responses/template.html')
}));

Vue.component('responses-create', Vue.extend({
    template: getHTML('assets/js/app/components/responses-create/template.html')
}));

Vue.component('responses-update', Vue.extend({
    template: getHTML('assets/js/app/components/responses-update/template.html')
}));

Vue.component('tweets', Vue.extend({
    template: getHTML('assets/js/app/components/tweets/template.html')
}));

;(function (exports) {

    'use strict';

    exports.app = {};

})(window);

;(function (exports) {

    'use strict';

    exports.app.main = new Vue({
        el: '#main',
        data: {
            currentView: 'questions'
        }
    });

})(window);

;(function (exports) {

    'use strict';

    exports.app.nav = new Vue({
        el: '#nav',

        // data
        data: {
        },

        // a custom directive to wait for the DOM to be updated
        // before focusing on the input field.
        // http://vuejs.org/guide/directives.html#Writing_a_Custom_Directive
        directives: {
        },

        // computed property
        // http://vuejs.org/guide/computed.html
        computed: {
        },

        // methods that implement data logic.
        // note there's no DOM manipulation here at all.
        methods: {
        }
    });

})(window);

;(function (exports) {

    'use strict';

    var routes = {};

    routes['/'] = function() {
        app.main.currentView = 'questions';
    };

    routes['/questions'] = function() {
        app.main.currentView = 'questions';
    };

    routes['/questions/create'] = function() {
        app.main.currentView = 'questions-create';
    };

    routes['/questions/:id/update'] = function() {
        app.main.currentView = 'questions-update';
    };

    routes['/questions/:id/delete'] = function() {
    };


    routes['/responses'] = function(view) {
        app.main.currentView = 'responses';
    };

    routes['/responses/create'] = function() {
        app.main.currentView = 'responses-create';
    };

    routes['/responses/:id/update'] = function() {
        app.main.currentView = 'responses-update';
    };

    routes['/responses/:id/delete'] = function() {
    };


    routes['/informations'] = function(view) {
        app.main.currentView = 'informations';
    };

    routes['/informations/create'] = function() {
        app.main.currentView = 'informations-create';
    };

    routes['/informations/:id/update'] = function() {
        app.main.currentView = 'informations-update';
    };


    routes['/tweets'] = function(view) {
        app.main.currentView = 'tweets';
    };


    routes['/operators'] = function(view) {
        app.main.currentView = 'operators';
    };

    routes['/operators/create'] = function() {
        app.main.currentView = 'operators-create';
    };

    routes['/operators/:id/update'] = function() {
        app.main.currentView = 'operators-update';
    };


    var router = new Router(routes);
    router.init();

})(window);
