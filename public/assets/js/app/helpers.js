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

