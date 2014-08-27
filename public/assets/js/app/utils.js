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

            var query = queryString.split('&');
            for (var q in query) {
                var st = q.split('\+');
                if (st[0] && st[1]) {
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
        }
    };

})(window);
