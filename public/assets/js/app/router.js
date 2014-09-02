(function (exports) {

    'use strict';


    //page('/(questions)?', function() {
    //    app.currentView = 'questions';
    //});

    //page('/questions/create', function() {
    //    app.currentView = 'questions-create';
    //});


    //page('/questions/:id/update', function() {
    //    app.currentView = 'questions-update';
    //});

    //page('/questions/:id/delete', function() {
    //});


    //page('/responses', function() {
    //    app.currentView = 'responses';
    //});

    //page('/responses/create', function() {
    //    app.currentView = 'responses-create';
    //});

    //page('/responses/:id/update', function() {
    //    app.currentView = 'responses-update';
    //});

    //page('/responses/:id/delete', function() {
    //});


    //page('/informations', function() {
    //    app.currentView = 'informations';
    //});

    //page('/informations/create', function() {
    //    app.currentView = 'informations-create';
    //});

    //page('/informations/:id/update', function() {
    //    app.currentView = 'informations-update';
    //});


    //page('/tweets', function() {
    //    app.currentView = 'tweets';
    //});


    //page('/operators', function() {
    //    app.currentView = 'operators';
    //});

    //page('/operators/create', function() {
    //    app.currentView = 'operators-create';
    //});

    //page('/operators/:id/update', function() {
    //    app.currentView = 'operators-update';
    //});

    //page();


    var routes = {};

    routes['/(questions)?'] = function() {
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
