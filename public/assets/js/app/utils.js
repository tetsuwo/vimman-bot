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
