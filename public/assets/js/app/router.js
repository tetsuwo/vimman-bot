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
