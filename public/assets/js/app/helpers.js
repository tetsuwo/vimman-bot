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

                        var urlhash = window.location.href.replace(/\?.*/, '');
                        window.location.href = urlhash + '?' + queryString;
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

