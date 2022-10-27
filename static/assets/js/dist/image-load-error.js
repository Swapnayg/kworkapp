! function() {
    var e = {
            12800: function() {
                window.imageLoadError = function(e) {
                    var r = e.src.match("/(collage/categories_first_level|collage/categories_second_level)/");
                    if (r && r.length > 1) {
                        var n = "/images/" + r[1] + "/blank.png";
                        if (e.src = n, "picture" === e.parentElement.nodeName.toLowerCase())
                            for (var t = 0; t < e.parentElement.children.length; t += 1) {
                                var o = e.parentElement.children[t].nodeName.toLowerCase();
                                "source" !== o && "img" !== o || (e.parentElement.children[t].srcset = n)
                            } else e.srcset = n
                    }
                    e.onerror = null
                }
            }
        },
        r = {};

    function n(t) {
        var o = r[t];
        if (void 0 !== o) return o.exports;
        var i = r[t] = {
            exports: {}
        };
        return e[t](i, i.exports, n), i.exports
    }
    n.n = function(e) {
            var r = e && e.__esModule ? function() {
                return e.default
            } : function() {
                return e
            };
            return n.d(r, {
                a: r
            }), r
        }, n.d = function(e, r) {
            for (var t in r) n.o(r, t) && !n.o(e, t) && Object.defineProperty(e, t, {
                enumerable: !0,
                get: r[t]
            })
        }, n.o = function(e, r) {
            return Object.prototype.hasOwnProperty.call(e, r)
        }, Object.defineProperty(n, "p", {
            get: function() {
                try {
                    if ("string" != typeof chunkCdnUrl) throw new Error("WebpackRequireFrom: 'chunkCdnUrl' is not a string or not available at runtime. See https://github.com/agoldis/webpack-require-from#troubleshooting");
                    return chunkCdnUrl
                } catch (e) {
                    return console.error(e), "/"
                }
            },
            set: function(e) {
                console.warn("WebpackRequireFrom: something is trying to override webpack public path. Ignoring the new value" + e + ".")
            }
        }),
        function() {
            "use strict";
            n(12800)
        }()
}();