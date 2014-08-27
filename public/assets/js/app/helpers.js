
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

        created: function () {
            console.log(componentName, 'component.created');
            this.fetch(this.$parent.conditions.page);
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
                var requestUri  = 'assets/js/app/components/' + componentName + '/dummy.json';
                var queryString = Utils.buildQueryString(conditions);
                var page        = conditions.page;
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

                        var pushStateUrl = window.location.href.replace(/\?.*/, '');
                        pushStateUrl += conditions ? '?' + queryString : '';
                        window.location.href = pushStateUrl;
                }, 800);
            },

            loading: function(flag) {
                console.log('loading', flag);
                this.$parent.isLoading = flag;
            },

            found: function(data, page) {
                console.log('found', data, 'page', page);
                this.$parent.result.list        = data.result;
                this.$parent.result.currentPage = page;
                this.$parent.result.pages       = Utils.getPages(page, data.total_count, 10);
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

