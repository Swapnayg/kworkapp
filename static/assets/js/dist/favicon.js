! function() {
    var e = {
            63529: function() {
                var e = !1,
                    r = !1,
                    t = "/favicons",
                    n = "/favicons-dark",
                    o = "-notify",
                    a = document.querySelectorAll(".js-theme-favicon");

                function i() {
                    var o = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : void 0,
                        a = arguments.length > 1 && void 0 !== arguments[1] && arguments[1],
                        i = arguments.length > 2 && void 0 !== arguments[2] && arguments[2];
                    if (e !== o && void 0 !== o || r !== a || i) {
                        var c = t,
                            d = n;
                        o !== e && void 0 !== o || (e ? c = d : d = c), e = u(void 0 === o ? e : o, a, c, d), r = a
                    }
                }

                function c(e, t, n, a, i) {
                    var c = r !== n && n ? a + o : a,
                        u = r !== n && n ? i + o : i;
                    return t ? e.replace(r ? a + o : a, u) : e.replace(r ? i + o : i, c)
                }

                function u(e, r, t, n) {
                    for (var o = 0, i = a.length; o < i; o += 1) {
                        var u = a[o],
                            d = c(u.dataset.url, e, r, t, n);
                        u.href ? u.href = d : u.content && (u.content = d), u.dataset.url = d
                    }
                    return e
                }! function() {
                    for (var e = 0, r = a.length; e < r; e += 1) {
                        var t = a[e];
                        t.href ? t.dataset.url = t.href : t.content && (t.dataset.url = t.content)
                    }
                }(), i(window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches, parseInt(window.unreadNotifyCount) > 0 || parseInt(window.unreadDialogCount) > 0, !0), window.matchMedia("(prefers-color-scheme: dark)").addListener((function(e) {
                    i(e.matches)
                })), window.updateFav = i
            }
        },
        r = {};

    function t(n) {
        var o = r[n];
        if (void 0 !== o) return o.exports;
        var a = r[n] = {
            exports: {}
        };
        return e[n](a, a.exports, t), a.exports
    }
    t.n = function(e) {
            var r = e && e.__esModule ? function() {
                return e.default
            } : function() {
                return e
            };
            return t.d(r, {
                a: r
            }), r
        }, t.d = function(e, r) {
            for (var n in r) t.o(r, n) && !t.o(e, n) && Object.defineProperty(e, n, {
                enumerable: !0,
                get: r[n]
            })
        }, t.o = function(e, r) {
            return Object.prototype.hasOwnProperty.call(e, r)
        }, Object.defineProperty(t, "p", {
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
            t(63529)
        }()
}();