! function() {
    var e = {
            96004: function() {
                var e = ".js-footer-menu-column",
                    t = ".js-footer-menu-title",
                    r = "active";

                function n(t) {
                    var n = getComputedStyle(document.body).getPropertyValue("--footer-mobile-max-width") || "767.98px";
                    if (!window.matchMedia("(min-width:".concat(n, ")")).matches) {
                        var o = $(t.currentTarget).closest(e);
                        o.hasClass(r) ? o.removeClass(r) : ($(e).removeClass(r), o.toggleClass(r))
                    }
                }
                _.forEach(document.querySelectorAll(t), (function(e) {
                    e.addEventListener("click", n)
                }))
            }
        },
        t = {};

    function r(n) {
        var o = t[n];
        if (void 0 !== o) return o.exports;
        var i = t[n] = {
            exports: {}
        };
        return e[n](i, i.exports, r), i.exports
    }
    r.n = function(e) {
            var t = e && e.__esModule ? function() {
                return e.default
            } : function() {
                return e
            };
            return r.d(t, {
                a: t
            }), t
        }, r.d = function(e, t) {
            for (var n in t) r.o(t, n) && !r.o(e, n) && Object.defineProperty(e, n, {
                enumerable: !0,
                get: t[n]
            })
        }, r.o = function(e, t) {
            return Object.prototype.hasOwnProperty.call(e, t)
        }, Object.defineProperty(r, "p", {
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
            r(96004)
        }()
}();