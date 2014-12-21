
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
                var requestUri  = 'http://' + window.location.host + '/api/' + componentName;
                var queryString = Utils.buildQueryString(conditions);
                var page        = conditions.page;
                //console.log('queryString', queryString);

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

                        if (window.location.hash != '') {
                            var pushStateUrl = window.location.href.replace(/\?.*/, '');
                            //console.log(pushStateUrl);
                            //console.log(conditions);
                            pushStateUrl += conditions ? '?' + queryString : '';
                            console.log('pushStateUrl', window.location.href, ' => ', pushStateUrl);
                            window.location.href = pushStateUrl;
                        }
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

                return true;
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

