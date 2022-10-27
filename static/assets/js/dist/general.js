! function() {
    var t = {
            91230: function(t, e, o) {
                "use strict";

                function n(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                o.r(e), o.d(e, {
                    default: function() {
                        return i
                    }
                });
                var i = function() {
                    function t() {
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, t), this.classes = {
                            eventMessage: ".event-message"
                        }, this.ionSettings = {
                            sounds: [{
                                name: "new_message",
                                preload: !0
                            }],
                            volume: .2,
                            path: Utils.cdnBaseUrl("/js/libs/sounds/")
                        }
                    }
                    var e, o, i;
                    return e = t, (o = [{
                        key: "setGetParameter",
                        value: function(t, e) {
                            var o = window.location.href,
                                n = location.hash;
                            if ((o = o.replace(n, "")).indexOf(t + "=") >= 0) {
                                var i = o.substring(0, o.indexOf(t + "=")),
                                    a = o.substring(o.indexOf(t + "="));
                                o = i + t + "=" + e + (a = (a = a.substring(a.indexOf("=") + 1)).indexOf("&") >= 0 ? a.substring(a.indexOf("&")) : "")
                            } else o.indexOf("?") < 0 ? o += "?" + t + "=" + e : o += "&" + t + "=" + e;
                            return o + n
                        }
                    }, {
                        key: "oldOs",
                        value: function() {
                            var t = window.navigator.userAgent,
                                e = [{
                                    os: /(Windows 8|Windows NT 6.2)/
                                }, {
                                    os: /(Windows XP|Windows NT 5.2)/
                                }, {
                                    os: /(Windows XP|Windows NT 5.1)/
                                }];
                            for (var o in e) e[o].os.test(t) && document.body.classList.add("os-old")
                        }
                    }, {
                        key: "checkCsrfTokenTtl",
                        value: function() {
                            window.csrfExpire && window.serverTime && setInterval((function() {
                                window.csrfExpire < Utils.getServerTime() && (window.isReloading = !0, document.location.reload())
                            }), 1e4)
                        }
                    }, {
                        key: "checkSafariBrowser",
                        value: function() {
                            var t = this;
                            "function" == typeof Utils.isSafariBrowser && Utils.isSafariBrowser() && (window.initSound = !1, $(document).on("click", (function() {
                                void 0 === window.initSound || "undefined" == typeof ion || window.initSound || (ion.sound.play("new_message", {
                                    volume: 0
                                }), ion.sound(t.ionSettings), window.initSound = !0)
                            })))
                        }
                    }, {
                        key: "removeTmpLocalStorageVars",
                        value: function() {
                            for (var t = 0; t < localStorage.length; t += 1) {
                                var e = localStorage.key(t);
                                e && e.indexOf && -1 !== e.indexOf("tmp-") && localStorage.removeItem(e)
                            }
                        }
                    }, {
                        key: "hidePortfolioLimitedNotice",
                        value: function(t) {
                            $(t).closest(this.classes.eventMessage).hide(), $.get("/api/portfolio/hidelimitnotice")
                        }
                    }, {
                        key: "hideTechnicalWorksNotification",
                        value: function(t) {
                            this.apiPostRequest("user/hidetechnicalworksnotification"), $(t).closest(this.classes.eventMessage).hide()
                        }
                    }, {
                        key: "getBillAmount",
                        value: function(t) {
                            var e = Utils.getFloatValue(t),
                                o = 0;
                            return e > 0 && (o = "undefined" != typeof refillCommission && refillCommission.isActive && refillCommission.getSum(e) ? refillCommission.getSum(e) : Math.round(e + e * parseFloat(BILL_COMISSION) / 100)), o
                        }
                    }, {
                        key: "clearPriceStr",
                        value: function(t) {
                            var e = t;
                            return "string" == typeof e && (e = e.replace(/\s/g, "").replace(",", ".")), e
                        }
                    }, {
                        key: "checkDownloadFile",
                        value: function() {
                            void 0 !== window.downloadFile && window.downloadFile && window.signinSignup.showLogin(!0, (function() {
                                window.location.href = window.downloadFile, setTimeout((function() {
                                    window.location.reload()
                                }), 5e3)
                            }))
                        }
                    }, {
                        key: "getGetParams",
                        value: function() {
                            var t = window.location.href;
                            if (-1 == t.indexOf("?")) return [];
                            var e = [],
                                o = t.split("?", 2)[1];
                            return new URLSearchParams(o).forEach((function(t, o) {
                                e[o] = t
                            })), e
                        }
                    }, {
                        key: "addRefParam",
                        value: function() {
                            var t = this.getGetParams();
                            return t.ref ? "&ref=" + t.ref : ""
                        }
                    }, {
                        key: "apiPostRequest",
                        value: function(t, e, o, n) {
                            $.post("/api/" + t, e, "json").done((function(e) {
                                e.success || console.error("method " + t + " has error", e), void 0 !== o && o.call(this, e.data || e)
                            })).fail((function() {
                                void 0 !== n && n()
                            }))
                        }
                    }, {
                        key: "copyTextToClipboard",
                        value: function(t, e, o) {
                            var n = document.createElement("textarea");
                            n.style.position = "fixed", n.style.top = 0, n.style.left = 0, n.style.width = "2em", n.style.height = "2em", n.style.padding = 0, n.style.border = "none", n.style.outline = "none", n.style.boxShadow = "none", n.style.background = "transparent", n.value = t, document.body.append(n), n.select(), document.execCommand("copy");
                            try {
                                e && e()
                            } catch (t) {
                                console.log("Oops, unable to copy"), o && o()
                            }
                            document.body.removeChild(n)
                        }
                    }, {
                        key: "implodeURI",
                        value: function(t, e) {
                            var o = "",
                                n = e || null;
                            if (!n) {
                                var i = window.location.href.split("?");
                                n = 1 == i.length ? window.location.href : i[0]
                            }
                            return o = n + ((o = $.param(t)) ? "?" + o : "")
                        }
                    }, {
                        key: "declension",
                        value: function(t, e, o, n, i) {
                            var a, r = i,
                                s = t;
                            return null != r && "" != r || (r = null), s = s || 0, "ru" == (r = r || lang || "ru") ? (a = Math.abs(s) % 100) > 10 && a < 20 ? n : (a %= 10) > 1 && a < 5 ? o : 1 == a ? e : n : 1 == (a = Math.abs(s)) ? e : n
                        }
                    }, {
                        key: "initNotification",
                        value: function() {
                            if ("undefined" != typeof ion && window.PULL_MODULE_ENABLE) {
                                this.ionSettings && this.ionSettings.sounds && ion.sound(this.ionSettings);
                                var t = Math.random();
                                "undefined" != typeof Storage && (Utils.setStorageData("soundTabId", t), setInterval((function() {
                                    Utils.setStorageData("soundTabId", t)
                                }), 3e3)), PullModule.on(PULL_EVENT_POP_UP_NOTIFY, (function(e) {
                                    window.bus && e.pop_up_notify && window.bus.$emit("POPUP_NOTIFICATIONS_ADD", e.pop_up_notify), 1 == MESSAGE_SOUND_ENABLE && ("undefined" != typeof Storage && localStorage.getItem("soundTabId") != t || ion.sound.play("new_message", {
                                        volume: .2
                                    }))
                                })), PullModule.on(PULL_EVENT_EDIT_POP_UP_NOTIFY, (function(t) {
                                    window.bus && t.pop_up_notify && window.bus.$emit("POPUP_NOTIFICATIONS_EDIT", t.pop_up_notify)
                                })), PullModule.on(PULL_EVENT_REMOVE_POP_UP_NOTIFY, (function(t) {
                                    window.bus && t.id && window.bus.$emit("POPUP_NOTIFICATIONS_REMOVE", t.id)
                                }))
                            }
                        }
                    }, {
                        key: "updateBalance",
                        value: function() {
                            var t = "tmp-total-funds";
                            window.OrdersCount.singleAjaxRequest("tmp-is-ajax-request", (function(e) {
                                $.ajax({
                                    url: "/balance/get",
                                    data: {
                                        csrftoken: $("input[name=csrftoken]").val()
                                    },
                                    method: "post",
                                    dataType: "json",
                                    success: function(o) {
                                        if (o.success) {
                                            var n = o.data.result;
                                            window.allowedToWithdraw = o.data.allowedToWithdraw, window.total_funds = o.data.raw, $(".js-header-balance").text(n), Utils.setStorageData(t, n), Utils.setStorageData(e, 0)
                                        }
                                    }
                                })
                            }), (function() {
                                null !== localStorage.getItem(t) && $(".js-header-balance").text(localStorage.getItem(t))
                            }))
                        }
                    }]) && n(e.prototype, o), i && n(e, i), Object.defineProperty(e, "prototype", {
                        writable: !1
                    }), t
                }();
                window.GeneralFunctions = new i
            },
            63856: function(t, e, o) {
                "use strict";

                function n(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                o.r(e), o.d(e, {
                    default: function() {
                        return i
                    }
                });
                var i = function() {
                    function t() {
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, t)
                    }
                    var e, o, i;
                    return e = t, i = [{
                        key: "showMessage",
                        value: function(e, o, n) {
                            var i = n || "",
                                a = "\n\t\t\t<div id='fox_notification_block'>\n\t\t\t\t<div class='fox_".concat(e, "' data-name='").concat(i, "'>\n\t\t\t\t\t<p>").concat(o, "</p>\n\t\t\t\t</div>\n\t\t\t</div>\n\t\t");
                            t.closeMessage(), $(".all_page").prepend(a), t.toggleEvents()
                        }
                    }, {
                        key: "closeMessage",
                        value: function() {
                            $("#fox_notification_block > div").remove(), t.toggleEvents()
                        }
                    }, {
                        key: "fadeMessageWithTimeout",
                        value: function() {
                            var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0,
                                o = $("#fox_notification_block > div");
                            o.length && (setTimeout((function() {
                                o.fadeOut((function() {
                                    o.remove()
                                }))
                            }), e), t.toggleEvents())
                        }
                    }, {
                        key: "closeMessageByName",
                        value: function(e) {
                            $("#fox_notification_block > div").filter('[data-name="'.concat(e, '"]')).remove(), t.toggleEvents()
                        }
                    }, {
                        key: "hasMessages",
                        value: function() {
                            return $("#fox_notification_block").children().length > 0
                        }
                    }, {
                        key: "toggleEvents",
                        value: function() {
                            var e = $(".js-event-list");
                            0 !== e.length && e.toggle(!t.hasMessages())
                        }
                    }], (o = null) && n(e.prototype, o), i && n(e, i), Object.defineProperty(e, "prototype", {
                        writable: !1
                    }), t
                }();
                window.MessageState = i
            },
            35498: function(t, e, o) {
                "use strict";

                function n(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                o.r(e), o.d(e, {
                    default: function() {
                        return i
                    }
                });
                var i = function() {
                    function t() {
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, t), this.classes = {
                            popup: ".popup",
                            headerMobile: ".js-header-mobile",
                            popupInstantClose: ".popup-instant-close-js"
                        }, this.events()
                    }
                    var e, o, i;
                    return e = t, (o = [{
                        key: "events",
                        value: function() {
                            $(document).on("mouseup touchend", this.classes.popupInstantClose, (function(t) {
                                t.preventDefault(), disableCurrentClick = !0, window.PopupHandler.close(this)
                            })).on("click", ".popup .overlay, .popup-close-js", (function() {
                                window.PopupHandler.close(this)
                            })).on("keydown", (function(t) {
                                27 == t.keyCode && window.openedLegacyPopup && window.PopupHandler.close(window.openedLegacyPopup)
                            }))
                        }
                    }, {
                        key: "close",
                        value: function(t) {
                            var e = $("body"),
                                o = $(t),
                                n = o;
                            n.is(this.classes.popup) || (n = o.parents(this.classes.popup));
                            var i = n.data("afterClose");
                            if (o.hasClass("overlay-disabled")) return !1;
                            if (window.openedLegacyPopup = null, unlockBodyForPopup(), n.hasClass("signin-signup__popup")) {
                                if ($(this.classes.headerMobile).fadeIn(0), o.hasClass("overlay") && e.hasClass("is_mobile")) return !1;
                                n.hide(), window.defferScripts.on("commonBottomDcl", (function() {
                                    changeBodyScrollbar("unlock")
                                }))
                            } else n.trigger("popup.remove"), n.remove();
                            ($(document).width() < 768 || isMobile()) && ($(".js-kworks-filter-button-wrapper").removeClass("fixed"), e.css("overflow", "")), e.removeClass("popup-android"), i && _.isFunction(i) && i()
                        }
                    }]) && n(e.prototype, o), i && n(e, i), Object.defineProperty(e, "prototype", {
                        writable: !1
                    }), t
                }();
                window.PopupHandler = new i
            },
            50901: function(t, e, o) {
                "use strict";

                function n(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                o.r(e), o.d(e, {
                    default: function() {
                        return i
                    }
                });
                var i = function() {
                    function t() {
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, t), this.classes = {
                            spinnerContainer: ".ispinner-container",
                            kworkSpinnerContainer: ".sliderImage",
                            thumbnailImgLoad: ".thumbnail-img-load"
                        }
                    }
                    var e, o, i;
                    return e = t, o = [{
                        key: "removeISpinner",
                        value: function(t) {
                            var e = arguments.length > 1 && void 0 !== arguments[1] && arguments[1],
                                o = $(e ? t : t.target);
                            if (!(o.length <= 0)) {
                                var n = o.closest(this.classes.spinnerContainer);
                                if (!(n.length <= 0)) {
                                    var i = n.find(this.classes.thumbnailImgLoad);
                                    i.length <= 0 || i.remove()
                                }
                            }
                        }
                    }], o && n(e.prototype, o), i && n(e, i), Object.defineProperty(e, "prototype", {
                        writable: !1
                    }), t
                }();
                window.Spinner = new i
            },
            41986: function() {
                "function" == typeof Utils.initActiveWindowListener && Utils.initActiveWindowListener(), document.addEventListener("DOMContentLoaded", (function() {
                    GeneralFunctions.removeTmpLocalStorageVars()
                })), $(window).on("storage", (function(t) {
                    "change-sound-message" === t.originalEvent.key && (MESSAGE_SOUND_ENABLE = t.originalEvent.newValue, $(".message_sound_block .js-message-sound-ico").toggleClass("hidden"))
                })), $((function() {
                    var t = ".js-only-integer";
                    $(document).on("keydown", t, (function(t) {
                        var e = t.keyCode; - 1 !== $.inArray(e, [46, 8, 9, 27, 13]) || 65 == e && (!0 === t.ctrlKey || !0 === t.metaKey) || (67 == e || 45 == e) && (!0 === t.ctrlKey || !0 === t.metaKey) || 1 == t.shiftKey && 45 == e || 86 == e && (!0 === t.ctrlKey || !0 === t.metaKey) || 88 == e && (!0 === t.ctrlKey || !0 === t.metaKey) || e >= 35 && e <= 39 || (t.shiftKey || t.keyCode < 48 || t.keyCode > 57) && (t.keyCode < 96 || t.keyCode > 105) && t.preventDefault()
                    })).on("input", t, (function(t) {
                        if (t) {
                            var e = t.target;
                            if (e && "value" in e && e.value) {
                                var o = $(e),
                                    n = !1,
                                    i = "",
                                    a = parseInt(e.value.replace(/[^0-9]/g, ""));
                                if (Number.isInteger(a)) {
                                    var r = o.data("maxValue");
                                    void 0 !== r && a > r && (a = r.toString(), n = !0);
                                    var s = o.data("minValue");
                                    void 0 !== s && a < s && (a = s.toString(), n = !0), i = a.toString()
                                }
                                o.val(i.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1 ")), n && o.trigger("only-integer:change")
                            }
                        }
                    })), setTimeout((function() {
                        $(window).on("blur", (function() {
                            setTimeout((function() {
                                $("html").addClass("html-is-blur")
                            }), 0)
                        })).on("focus", (function() {
                            setTimeout((function() {
                                $("html").removeClass("html-is-blur")
                            }), 0)
                        }))
                    })), GeneralFunctions.checkCsrfTokenTtl(), GeneralFunctions.oldOs(), GeneralFunctions.checkSafariBrowser()
                })), $((function() {
                    if ("/track" === window.location.pathname && window.location.hash) {
                        var t = window.location.hash;
                        "scrollRestoration" in history && (history.scrollRestoration = "manual");
                        var e = $(t);
                        e.length > 0 && setTimeout((function() {
                            $("html, body").animate({
                                scrollTop: e.offset().top - 100
                            }, 400, (function() {
                                history.replaceState(null, null, " ")
                            }))
                        }), 200)
                    }
                })), $((function() {
                    $(".js-poll-notify__close").on("click", (function() {
                        $(".js-scroll-up").removeClass("from-badge"), $(this).closest(".abandoned-basket").slideUp(300), $.post("/api/user/closepollnotify", (function() {}))
                    })), $(".abandoned-basket").each((function(t) {
                        $(this).css("bottom", t * ($(this).height() + 1) + "px")
                    }))
                })), $((function() {
                    deferScript("pullJs", (function() {
                        deferScript("ionSound", (function() {
                            GeneralFunctions.initNotification()
                        }))
                    }), window.defferJqueryPages), setTimeout((function() {
                        $.fn.jScrollPane && $(".cart-popup .block-popup_body").jScrollPane({
                            autoReinitialise: !0
                        }), window.document.body.addEventListener("wheel", (function(t) {
                            $(t.target).closest(".cart-popup .block-popup_body, .message .block-popup").length > 0 && t.preventDefault()
                        }), {
                            passive: !1
                        })
                    })), $("body").on("change keyup input click", ".js-input-number", (function() {
                        this.value.match(/[^0-9]/g, "") && (this.value = this.value.replace(/[^0-9]/g, ""))
                    })), deferScript("pullJs", (function() {
                        "undefined" != typeof PULL_MODULE_ENABLE && PULL_MODULE_ENABLE && window.PullModule && PullModule.on(PULL_EVENT_ACCOUNT_DELETED, (function() {
                            window.location.reload()
                        })), "undefined" != typeof PULL_MODULE_ENABLE && PULL_MODULE_ENABLE && window.PullModule && PullModule.on(PULL_EVENT_UPDATE_BALANCE, GeneralFunctions.updateBalance)
                    }), window.defferJqueryPages), $(document).on("click", ".js-get-portfolio", (function() {
                        var t = $(this).data("portfolio-id");
                        deferScript("portfolioViewPopup", (function() {
                            window.portfolioCard.getPortfolio(t)
                        }))
                    })), setTimeout((function() {
                        $("body").on("mouseenter", ".hoverMe", (function() {
                            $(".order-extras").addClass("open").removeClass("om-close")
                        })).on("mouseleave", ".hoverMe", (function() {
                            $(".order-extras").removeClass("open").addClass("om-close"), $(".chosen-container.chosen-container-single.chosen-container-single-nosearch.chosen-container-active").removeClass("chosen-with-drop chosen-container-active")
                        })), $(".order-extras-list").on("webkitAnimationEnd oanimationend msAnimationEnd animationend", (function() {
                            $(this).height() > 0 && $(this).addClass("no-overflow")
                        })), $(".js-more-kwork-links-sites").on("click", (function(t) {
                            t.preventDefault();
                            var e = $(this),
                                o = e.parent().find("img");
                            e.addClass("hidden"), o.removeClass("hidden"), $.ajax({
                                url: "/api/kwork/getkworksites",
                                data: {
                                    kworkId: e.data("id"),
                                    showHosts: e.data("showHosts")
                                },
                                method: "GET",
                                dataType: "json",
                                success: function(t) {
                                    if (o.addClass("hidden"), t.success) {
                                        var n = $(".kwork-links-sites-table").find("tbody");
                                        n.append(t.html), n.find("tr").length < e.data("total") && e.parent().find("span").removeClass("hidden");
                                        var i = $(".b-about-text");
                                        if (i.hasClass("active")) {
                                            var a = $(".b-about-text_container", i),
                                                r = $(".b-about-text_container_text", a).height();
                                            a.css("height", r)
                                        }
                                    }
                                },
                                error: function() {
                                    o.addClass("hidden"), e.removeClass("hidden")
                                }
                            })
                        }))
                    }))
                })), $(document).on("click", ".js-mobile-render", (function() {
                    Cookies.remove("only_desktop_version"), setTimeout((function() {
                        location.reload(!0)
                    }), 300)
                })).on("click", ".js-render-desktop", (function() {
                    Cookies.set("only_desktop_version", !0, {
                        path: "/"
                    }), Cookies.get("isIPadOS") && Cookies.remove("isIPadOS"), setTimeout((function() {
                        window.location.replace(GeneralFunctions.setGetParameter("desktop", "true"))
                    }), 300)
                })), $(document).on("mouseup touchend", (function() {
                    window.disableCurrentClick && setTimeout((function() {
                        window.disableCurrentClick = !1
                    }), 200)
                }));
                var t = !1;
                $(document).on("click", ".js-link-once", (function() {
                    return !t && (t = !0, !0)
                })), $((function() {
                    $(".js-only-numeric").on("keydown", (function(t) {
                        if (1 == t.key.length && t.key.match(/[^0-9.,]/)) return !1
                    })).on("keyup input", (function() {
                        var t = $(this),
                            e = t.val().replace(/(\s)/g, ""),
                            o = Utils.hasMark(e);
                        if (o) {
                            var n = e.split(o);
                            n.length > 1 && (e = parseInt(n[0]).toString() + o + n[1].charAt(0))
                        } else e = parseInt(e).toString();
                        var i = parseFloat(e.replace(",", "."));
                        isNaN(i) && (e = "");
                        var a = t.attr("data-max");
                        a > 0 && i > a && (e = a.toString()), $(this).val(e.replace(/[^0-9.,]/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, " "))
                    }))
                }))
            },
            85635: function() {
                window.csSendQueue = [], window.oldCsSendQueue = [], window.touchIsUsed = !1, window.disableCurrentClick = !1, window.formData = new FormData
            },
            85751: function(t, e, o) {
                "use strict";

                function n(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                o.r(e);
                var i = function() {
                    function t() {
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, t)
                    }
                    var e, o, i;
                    return e = t, i = [{
                        key: "initPageTooltips",
                        value: function() {
                            setTimeout((function() {
                                var t = $(".js-tooltip");
                                t.length > 0 && t.tooltip()
                            }))
                        }
                    }, {
                        key: "measure",
                        value: function(t) {
                            var e = $(this).clone(!1);
                            e.css({
                                visibility: "hidden",
                                position: "absolute"
                            }), e.appendTo("body");
                            var o = t.apply(e);
                            return e.remove(), o
                        }
                    }, {
                        key: "setTooltipDimensions",
                        value: function(e) {
                            var o = $(this);
                            o.data("proportion") && t.setByProportion($(e), o.data("proportion"));
                            var n = $(e),
                                i = n.data("position"),
                                a = t.measure.call(e, (function() {
                                    return o.data("proportion") && t.setByProportion(this, o.data("proportion")), this.outerWidth()
                                })),
                                r = t.measure.call(e, (function() {
                                    return o.data("proportion") && t.setByProportion(this, o.data("proportion")), this.outerHeight()
                                })),
                                s = $(this).offset().left + parseInt($(this).css("margin-left")) + $(this).outerWidth() / 2,
                                l = $(this).offset().left + parseInt($(this).css("margin-left")) + $(this).outerWidth();
                            t.setVertical.call(this, n), t.setHorizontal.call(this, n);
                            var c = 0,
                                u = 0;
                            switch (i) {
                                case "center":
                                    c = s + a / 2 + 50, u = s - a / 2;
                                    break;
                                case "right":
                                    c = s - a + 50, u = s - a + 30;
                                    break;
                                case "right-fill":
                                    c = l - a, u = l - a;
                                    break;
                                case "left-fill":
                                    c = s + a + 50 + 25, u = s - 25;
                                    break;
                                default:
                                    c = s + a + 50, u = s - 30
                            }
                            c > $(window).width() && (u = $(document).width() - a - 10), u < 0 && (u = 0);
                            var d = u;
                            if ("right" == n.data("aroundPosition")) {
                                o.data("proportion") || n.css("width", c - u + 50 + "px");
                                var p = -r / 2 + 10;
                                n.find(".js-tooltip-block-corner__inner").css({
                                    top: p + "px"
                                }), d = n.offset().left
                            } else if ("top" == n.data("aroundPosition")) {
                                var f = 0;
                                n.parents("*").each((function(t) {
                                    if ("relative" == $(this).css("position")) return f = $(this).offset().left - 2, !1
                                })), n.css({
                                    left: u - f + "px"
                                });
                                var h = s - u - 40;
                                n.find(".js-tooltip-block-corner__inner").css({
                                    left: h + "px"
                                })
                            } else if ("left" === n.data("aroundPosition")) {
                                o.data("proportion") || n.css("width", c - u + "px");
                                var v = -r / 2 + 10;
                                n.find(".js-tooltip-block-corner__inner").css({
                                    top: v + "px"
                                }), d = n.offset().left
                            } else {
                                n.css({
                                    left: u + "px"
                                });
                                var m = s - u - 30;
                                n.find(".js-tooltip-block-corner__inner").css({
                                    left: m + "px"
                                })
                            }
                            var y = a;
                            d + a > $(window).width() && (y = $(document).width() - d - 10), o.data("proportion") ? n.outerWidth(y) : n.css("width", y + "px")
                        }
                    }, {
                        key: "setByProportion",
                        value: function(e, o) {
                            var n, i = e.width(),
                                a = o;
                            n = !0 === a ? 2 : (a = a.split(":"))[0] / a[1];
                            for (var r = i, s = e.width() / e.height(); s > n;) r -= 10, e.width(r), s = e.width() / e.height();
                            for (var l = 0; !t.canSqueeze(e) && l < 50;) r += 10, e.width(r), l += 1;
                            t.canSqueeze(e) || e.find(".js-tooltip-block__text").css({
                                "word-break": "break-all",
                                "overflow-x": "inherit"
                            })
                        }
                    }, {
                        key: "canSqueeze",
                        value: function(t) {
                            var e = t.find(".js-tooltip-block__text");
                            return e.css("overflow-x", "auto"), e[0].scrollWidth <= e.width()
                        }
                    }, {
                        key: "setVertical",
                        value: function(e) {
                            var o, n = $(this),
                                i = t.measure.call(e[0], (function() {
                                    return n.data("proportion") && t.setByProportion(this, n.data("proportion")), this.outerHeight()
                                })),
                                a = $(this).offset().top,
                                r = $("body").scrollTop(),
                                s = {};
                            "right" == e.data("aroundPosition") || "left" == e.data("aroundPosition") ? s.vertical = "right" : s.vertical = "top", "top" == s.vertical ? (a - i < r ? (o = $(this).position().top + $(this).outerHeight() + 10, e.removeClass("tooltip-block--top").addClass("tooltip-block--bottom")) : (o = $(this).position().top + parseInt($(this).css("margin-top")) - i - 10, e.css({
                                top: o + "px"
                            }), e.removeClass("tooltip-block--bottom").addClass("tooltip-block--top")), e.css({
                                top: o + "px"
                            })) : "right" == s.vertical && (o = $(this).position().top + $(this).outerHeight() / 2 - i / 2, e.css({
                                top: o + "px"
                            }))
                        }
                    }, {
                        key: "setHorizontal",
                        value: function(t) {
                            var e, o, n;
                            "right" == t.data("aroundPosition") ? (e = $(this).position().left + $(this).outerWidth() + 10, o = "tooltip-block--bottom tooltip-block--top", n = "tooltip-block--right") : "left" == t.data("aroundPosition") && (e = $(this).position().left - 10 - t.outerWidth(), o = "tooltip-block--bottom tooltip-block--top", n = "tooltip-block--left"), t.css({
                                left: e + "px"
                            }), t.removeClass(o).addClass(n)
                        }
                    }, {
                        key: "needHide",
                        value: function(t, e) {
                            if (void 0 !== $(e).data("tooltip")) {
                                var o = $(e).data("tooltip").tooltip;
                                return !$(t.relatedTarget).closest(".js-tooltip-block").filter(o).length
                            }
                            return 0 == $(t.relatedTarget).filter(e).length
                        }
                    }], (o = null) && n(e.prototype, o), i && n(e, i), Object.defineProperty(e, "prototype", {
                        writable: !1
                    }), t
                }();

                function a(t, e) {
                    var o = Object.keys(t);
                    if (Object.getOwnPropertySymbols) {
                        var n = Object.getOwnPropertySymbols(t);
                        e && (n = n.filter((function(e) {
                            return Object.getOwnPropertyDescriptor(t, e).enumerable
                        }))), o.push.apply(o, n)
                    }
                    return o
                }

                function r(t, e, o) {
                    return e in t ? Object.defineProperty(t, e, {
                        value: o,
                        enumerable: !0,
                        configurable: !0,
                        writable: !0
                    }) : t[e] = o, t
                }

                function s(t) {
                    return function(t) {
                        if (Array.isArray(t)) return c(t)
                    }(t) || function(t) {
                        if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"]) return Array.from(t)
                    }(t) || function(t, e) {
                        if (!t) return;
                        if ("string" == typeof t) return c(t, e);
                        var o = Object.prototype.toString.call(t).slice(8, -1);
                        "Object" === o && t.constructor && (o = t.constructor.name);
                        if ("Map" === o || "Set" === o) return Array.from(t);
                        if ("Arguments" === o || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(o)) return c(t, e)
                    }(t) || function() {
                        throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
                    }()
                }

                function c(t, e) {
                    (null == e || e > t.length) && (e = t.length);
                    for (var o = 0, n = new Array(e); o < e; o++) n[o] = t[o];
                    return n
                }

                function u(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                var d = new RegExp("^".concat(/(?:(?:https?|ftp):\/\/(?:[а-яёa-z0-9_-]{1,32}(?::[а-яёa-z0-9_-]{1,32})?@)?)?(?:(?:[а-яёa-z0-9-]{1,128}\.)+(?:рф|xn--p1ai|рус|xn--p1acf|укр|xn--j1amh|сайт|xn--80aswg|онлайн|xn--80asehdb|дети|xn--d1acj3b|москва|xn--80adxhks|бг|xn--90ae|срб|xn--90a3ac|бел|xn--90ais|[a-z]{2,10})|(?!0)(?:(?!0[^.]|255)[0-9]{1,3}\.){3}(?!0|255)[0-9]{1,3})(?:\/[а-яёa-z0-9.,_@%&?+=\:\~/-]*)?(?:#[^ '\"&]*)?/.source, "$"), "i"),
                    p = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/,
                    f = function() {
                        function t() {
                            ! function(t, e) {
                                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                            }(this, t)
                        }
                        var e, o, n;
                        return e = t, n = [{
                            key: "p2nl",
                            value: function(t) {
                                var e = t.replace(/\r\n/g, /\n/).split(/(<\/p>|<br>|<br\/>|<br \/>)/i),
                                    o = [];
                                return _.forEach(e, (function(t) {
                                    var e = t.replace(/<\/?[^>]*>/gi, "").trim();
                                    (e = he.decode(e)).length && o.push(e)
                                })), o.join("\n")
                            }
                        }, {
                            key: "isValidURL",
                            value: function(t) {
                                return d.test(t)
                            }
                        }, {
                            key: "isValidEmail",
                            value: function(t) {
                                return p.test(t)
                            }
                        }, {
                            key: "getMonths",
                            value: function() {
                                return [{
                                    id: 1,
                                    name: l("srcClassesHelpersJs1", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 2,
                                    name: l("srcClassesHelpersJs2", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 3,
                                    name: l("srcClassesHelpersJs3", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 4,
                                    name: l("srcClassesHelpersJs4", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 5,
                                    name: l("srcClassesHelpersJs5", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 6,
                                    name: l("srcClassesHelpersJs6", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 7,
                                    name: l("srcClassesHelpersJs7", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 8,
                                    name: l("srcClassesHelpersJs8", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 9,
                                    name: l("srcClassesHelpersJs9", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 10,
                                    name: l("srcClassesHelpersJs10", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 11,
                                    name: l("srcClassesHelpersJs11", "legacy-translations"),
                                    selectable: !0
                                }, {
                                    id: 12,
                                    name: l("srcClassesHelpersJs12", "legacy-translations"),
                                    selectable: !0
                                }]
                            }
                        }, {
                            key: "dateDifference",
                            value: function(t, e) {
                                var o = {
                                        years: 0,
                                        months: 0
                                    },
                                    n = [];
                                if (e - t > 0) {
                                    o.years = e.getFullYear() - t.getFullYear(), o.months = e.getMonth() - t.getMonth(), o.months < 0 && (o.years -= 1, o.months += 12), o.days < 0 && (o.months = Math.max(0, o.months - 1));
                                    for (var i = 12 * o.years + o.months, a = 1; a <= i; a += 1) {
                                        var r = new Date(t.getFullYear(), t.getMonth());
                                        n.push(r.setMonth(r.getMonth() + a))
                                    }
                                }
                                return n
                            }
                        }, {
                            key: "datePeriod",
                            value: function(t) {
                                var e = {
                                        years: 0,
                                        months: 0
                                    },
                                    o = t.reduce((function(t, e) {
                                        return t.includes(e) ? t : [].concat(s(t), [e])
                                    }), []);
                                e.years = Math.trunc(o.length / 12), e.months = o.length % 12;
                                var n = e.years + " " + GeneralFunctions.declension(e.years, l("srcClassesHelpersJs13", "legacy-translations"), l("srcClassesHelpersJs14", "legacy-translations"), l("srcClassesHelpersJs15", "legacy-translations")),
                                    i = e.months + " " + GeneralFunctions.declension(e.months, l("srcClassesHelpersJs16", "legacy-translations"), l("srcClassesHelpersJs17", "legacy-translations"), l("srcClassesHelpersJs18", "legacy-translations"));
                                switch (!0) {
                                    case e.years > 0 && e.months > 0:
                                        return n + l("srcClassesHelpersJs19", "legacy-translations") + i;
                                    case 0 === e.years && e.months > 0:
                                        return i;
                                    case e.years > 0 && 0 === e.months:
                                        return n;
                                    default:
                                        return ""
                                }
                            }
                        }, {
                            key: "getYears",
                            value: function(t, e) {
                                for (var o = [], n = e; n >= t; n -= 1) o.push({
                                    id: n,
                                    name: n
                                });
                                return o
                            }
                        }, {
                            key: "stripTags",
                            value: function(t) {
                                return t.replace(/<\/?[^>]*>/gi, "")
                            }
                        }, {
                            key: "forEachAsync",
                            value: function(t, e, o) {
                                var n = this,
                                    i = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : 0;
                                i >= t.length ? o && o() : e(t[i], i, (function() {
                                    n.forEachAsync(t, e, o, i + 1)
                                }))
                            }
                        }, {
                            key: "unescapeSlashes",
                            value: function(t) {
                                return t.replace(/\\\\/g, "\\")
                            }
                        }, {
                            key: "priceClear",
                            value: function(t, e) {
                                var o = t,
                                    n = function(t) {
                                        for (var e = 1; e < arguments.length; e++) {
                                            var o = null != arguments[e] ? arguments[e] : {};
                                            e % 2 ? a(Object(o), !0).forEach((function(e) {
                                                r(t, e, o[e])
                                            })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(o)) : a(Object(o)).forEach((function(e) {
                                                Object.defineProperty(t, e, Object.getOwnPropertyDescriptor(o, e))
                                            }))
                                        }
                                        return t
                                    }({
                                        float: !1
                                    }, e),
                                    i = n.float;
                                return void 0 === o ? 0 : (o = (o = o.replace(/ /g, "")).replace(/^[0]+/g, ""), i ? ("en" === window.actor_lang && (o = o.replaceAll(",", "")), parseFloat(o)) : parseInt(o))
                            }
                        }, {
                            key: "numberFormatByLang",
                            value: function(t) {
                                var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0,
                                    o = ",",
                                    n = document.documentElement.lang;
                                return "ru" === n || "fr" === n ? o = " " : "de" !== n && "es" !== n || (o = "."), Utils.numberFormat(t, e, ".", o)
                            }
                        }, {
                            key: "cutPasteSpecial",
                            value: function(t, e) {
                                var o = t,
                                    n = [];
                                return o = e(o = o.replace(/&[#0-9a-z]+;/g, (function(t) {
                                    var e = "<symbol".concat(n.length, ">");
                                    return n.push({
                                        symbol: t,
                                        tag: e
                                    }), e
                                }))), _.forEach(n, (function(t) {
                                    o = o.replace(t.tag, t.symbol)
                                })), o
                            }
                        }], (o = null) && u(e.prototype, o), n && u(e, n), Object.defineProperty(e, "prototype", {
                            writable: !1
                        }), t
                    }();

                function h(t) {
                    return h = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
                        return typeof t
                    } : function(t) {
                        return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
                    }, h(t)
                }

                function v(t, e) {
                    for (var o = 0; o < e.length; o++) {
                        var n = e[o];
                        n.enumerable = n.enumerable || !1, n.configurable = !0, "value" in n && (n.writable = !0), Object.defineProperty(t, n.key, n)
                    }
                }
                var m = function() {
                    function t() {
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, t), this.TOOLTIP_CIRCLE = ".tooltip_circle, .btn-title_right", this.TOOLTIP_CIRCLE_HOVER = "tooltip_circle_hover", this.TOOLTIP_ICON = ".icon-custom-help", this.TOOLTIP_ICON_HOVER = "icon-custom-help_hover", this.TOOLTIP_BLOCK = ".tooltip_block", this.TOOLTIP_BLOCK_HOVER = "tooltip_block_hover", this.init()
                    }
                    var e, o, n;
                    return e = t, n = [{
                        key: "parseEmojiShortCode",
                        value: function(t) {
                            var e = t.content();
                            e && window.emojiReplacements && t.content(window.emojiReplacements.shortcodeToSpan(e.toString()))
                        }
                    }, {
                        key: "formatUrlTags",
                        value: function(t) {
                            var e = t.content();
                            if (e && window.he && !0 !== new RegExp("(href|src)=('|\\\"|&quot;|&amp;quot;)", "gi").test(e)) {
                                var o = new RegExp(/(^|[^="']\s*)((?:(https?|ftp):\/\/[-A-Za-zА-Яа-я0-9+&@#/%?=~_|!:.,;]+[-A-Za-zА-Яа-я0-9+&@#/%=~_|]))/.source, "gi"),
                                    n = new RegExp("".concat(/(?:[.,'!$%^*;:{}=`~()&"])/.source, "$"), "i"),
                                    i = f.cutPasteSpecial(e, (function(t) {
                                        return t.replace(o, (function(t, e, o) {
                                            var i = "",
                                                a = he.decode(o),
                                                r = a = a.replace(n, (function(t) {
                                                    return t && (i = he.encode(t)), ""
                                                }));
                                            try {
                                                r = decodeURI(r)
                                            } catch (t) {}
                                            var s = he.encode(r),
                                                l = he.encode(r);
                                            return "".concat(e, '<a rel="nofollow noopener" target="_blank" class="shortened-url" href="').concat(s, '">').concat(l, "</a>").concat(i || "")
                                        }))
                                    }));
                                t.content(i)
                            }
                        }
                    }], (o = [{
                        key: "init",
                        value: function() {
                            var t = this;
                            window.TOOLTIP_CONFIG = this.tooltipConfig(), $((function() {
                                "object" === h(window.defferScripts) ? window.defferScripts.on("tooltipster", (function() {
                                    t.initTooltipster()
                                })) : t.initTooltipster()
                            }))
                        }
                    }, {
                        key: "tooltipConfig",
                        value: function() {
                            var e = this;
                            return {
                                animationDuration: 200,
                                distance: 4,
                                contentAsHTML: !0,
                                interactive: !0,
                                contentCloning: !0,
                                side: "top",
                                theme: "tooltipster-light",
                                minIntersection: 14,
                                zIndex: 9999,
                                delay: [50, 90],
                                plugins: ["sideTip", "scrollableTip"],
                                trigger: "custom",
                                triggerOpen: {
                                    mouseenter: !0,
                                    touchstart: !0
                                },
                                triggerClose: {
                                    mouseleave: !0,
                                    scroll: !0,
                                    tap: !0
                                },
                                functionFormat: function(t, e, o) {
                                    return "string" == typeof o ? o.trim() : o
                                },
                                functionInit: function(o, n) {
                                    var i = $(n.origin),
                                        a = {},
                                        r = o.option("maxWidth"),
                                        s = o.option("delay");
                                    try {
                                        i.attr() && i.attr().data && i.attr().data.tooltip && (a = i.attr().data && i.attr().data.tooltip)
                                    } catch (t) {
                                        return
                                    }
                                    if (a) {
                                        var l = [];
                                        $.each(a, (function(i, c) {
                                            switch (i) {
                                                case "disabled":
                                                    o.disable();
                                                    break;
                                                case "text":
                                                    !o.content() && c && o.content(c);
                                                    break;
                                                case "theme":
                                                    "dark" == c ? (o.option("theme", "tooltipster-borderless"), o.option("minIntersection", 12)) : "dark-minimal" == c && (o.option("theme", "tooltipster-borderless-minimal"), o.option("minIntersection", 8));
                                                    break;
                                                case "width":
                                                    r = c;
                                                    break;
                                                case "minwidth":
                                                    c && o.option("minWidth", c);
                                                    break;
                                                case "destroy":
                                                    1 == c && o.option("functionAfter", (function(t, o) {
                                                        e.tooltipsterFunctionAfter(t, o), t.destroy()
                                                    }));
                                                    break;
                                                case "child":
                                                    1 == c && l.push((function(t, o) {
                                                        e.tooltipsterFunctionBefore(t, o)
                                                    }));
                                                    break;
                                                case "uncheckonmobile":
                                                    1 == c && l.push((function(t) {
                                                        window.touchIsUsed && $(t.content()[0]).find("input").prop("checked", !1)
                                                    }));
                                                    break;
                                                case "target":
                                                    o.option("functionPosition", (function(t, e, o) {
                                                        var n = $(e.origin),
                                                            i = n.offset(),
                                                            a = n.find(c);
                                                        if (a.length) {
                                                            var r = a.offset();
                                                            o.coord.top += r.top - i.top, o.target = r.left + a.outerWidth() / 2
                                                        }
                                                        return o
                                                    }));
                                                    break;
                                                case "custom":
                                                    o.option("trigger", "custom"), o.option("triggerOpen", {}), o.option("triggerClose", {});
                                                    break;
                                                case "mhidden":
                                                    l.push((function() {
                                                        if ($(window).width() < 768) return !1
                                                    }));
                                                    break;
                                                case "thidden":
                                                    n.origin && window.touchDetector.listen(n.origin), l.push((function() {
                                                        if (window.touchDetector.isTouch()) return !1
                                                    }));
                                                    break;
                                                case "mpopup":
                                                    $(n.origin).on("click", (function() {
                                                        isMobile() && window.bus.$emit("simple-popup-open", {
                                                            title: c,
                                                            content: a.text
                                                        })
                                                    })), l.push((function() {
                                                        if (isMobile()) return !1
                                                    }));
                                                    break;
                                                case "delay":
                                                    s = c.toString().split(",");
                                                    break;
                                                case "tprevent":
                                                    isTouchDevice() && $(n.origin).on("click", (function(t) {
                                                        t.preventDefault()
                                                    }));
                                                    break;
                                                case "baseclass":
                                                    o.option("functionReady", (function(t, e) {
                                                        $(e.tooltip).addClass(c)
                                                    }));
                                                    break;
                                                case "interactive":
                                                    o.option("interactive", "true" == c);
                                                    break;
                                                case "resetable":
                                                    l.push((function(t) {
                                                        t.content(a.text)
                                                    }));
                                                    break;
                                                case "emoji":
                                                    c && l.push(t.parseEmojiShortCode);
                                                    break;
                                                case "url":
                                                    c && l.push(t.formatUrlTags);
                                                    break;
                                                default:
                                                    o.option(i, c)
                                            }
                                        })), l.length > 0 && o.option("functionBefore", (function() {
                                            return l.every((function(t) {
                                                return !1 !== t(o, n)
                                            }))
                                        }))
                                    }
                                    var c, u = o.content();
                                    u && null == r && ("object" === h(u) && (u = $(u[0]).html()), (c = (u += "").replace(/<[^>]+>/g, "").length) > 40 && c <= 100 && (r = 220), c > 100 && c <= 200 && (r = 280), c > 200 && (r = 400));
                                    r && o.option("maxWidth", r), s && (o.option("delay", s), o.option("trackerInterval", s[0]))
                                },
                                functionReady: function(t, e) {
                                    $(e.tooltip).addClass($(e.origin).data("tooltip-class"))
                                },
                                functionBefore: function(t, o) {
                                    $.each($.tooltipster.instances(), (function(t, e) {
                                        e.close()
                                    })), e.tooltipsterFunctionBefore(t, o)
                                },
                                functionAfter: function(t, o) {
                                    e.tooltipsterFunctionAfter(t, o)
                                }
                            }
                        }
                    }, {
                        key: "tooltipsterFunctionBefore",
                        value: function(t, e) {
                            var o = $(e.origin);
                            o.is(this.TOOLTIP_CIRCLE) ? o.addClass(this.TOOLTIP_CIRCLE_HOVER) : o.is(this.TOOLTIP_ICON) ? o.addClass(this.TOOLTIP_ICON_HOVER) : o.is(this.TOOLTIP_BLOCK) && o.addClass(this.TOOLTIP_BLOCK_HOVER)
                        }
                    }, {
                        key: "tooltipsterFunctionAfter",
                        value: function(t, e) {
                            var o = $(e.origin);
                            o.is(this.TOOLTIP_CIRCLE) ? o.removeClass(this.TOOLTIP_CIRCLE_HOVER) : o.is(this.TOOLTIP_ICON) ? o.removeClass(this.TOOLTIP_ICON_HOVER) : o.is(this.TOOLTIP_BLOCK) && o.removeClass(this.TOOLTIP_BLOCK_HOVER)
                        }
                    }, {
                        key: "initTooltipster",
                        value: function() {
                            if ($.fn.tooltipster) {
                                var t = $(this.TOOLTIP_ICON);
                                _.forEach(t, (function(t) {
                                    addScriptToQueue((function() {
                                        var e = $(t);
                                        e.parents(".tooltipster").length > 0 || e.tooltipster(TOOLTIP_CONFIG)
                                    }))
                                })), addScriptToQueue((function() {
                                    $(".tooltipster.tooltipster-pre-init").tooltipster(TOOLTIP_CONFIG), $("body").on("mouseenter", ".tooltipster:not(.tooltipstered)", (function() {
                                        $(this).tooltipster(TOOLTIP_CONFIG).tooltipster("open")
                                    }))
                                }))
                            }
                        }
                    }]) && v(e.prototype, o), n && v(e, n), Object.defineProperty(e, "prototype", {
                        writable: !1
                    }), t
                }();
                o(86073), window.TooltipsterSettings = i, $((function() {
                    i.initPageTooltips()
                })), window.TooltipsterConfig = new m
            },
            86073: function() {
                function t(e) {
                    return t = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
                        return typeof t
                    } : function(t) {
                        return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
                    }, t(e)
                }
                $((function() {
                    var e = {
                        init: function() {
                            return this.each((function() {
                                var t = $(this),
                                    o = t.find(".js-tooltip-text").length ? t.find(".js-tooltip-text").html() : t.data("tooltipText"),
                                    n = t.data("tooltipClass") || "",
                                    i = t.data("tooltipBlockClass") || "",
                                    a = t.data("tooltipTheme") || "light",
                                    r = t.data("tooltip"),
                                    s = $("<div />", {
                                        html: '<div class="js-tooltip-block__text '.concat(n, '">').concat(o, "</div>")
                                    }).addClass("js-tooltip-block tooltip-block tooltip-block_theme_".concat(a, " ").concat(i)),
                                    l = $("<div>").addClass("tooltip-block__corner").html('<div class="tooltip-block-corner__inner js-tooltip-block-corner__inner">');
                                if (s.append(l), t.data("tooltipHidden")) return this;
                                r || (t.data("tooltip", {
                                    target: t,
                                    tooltip: s
                                }), t.on({
                                    "mouseenter.tooltip": e.show,
                                    "mouseleave.tooltip": e.hide
                                }))
                            }))
                        },
                        destroy: function() {
                            return this.each((function() {
                                var t = $(this),
                                    e = t.data("tooltip");
                                $(window).off(".tooltip"), e.tooltip.remove(), t.removeData("tooltip")
                            }))
                        },
                        show: function() {
                            if (!($(".js-tooltip-block").length > 0)) {
                                var t = $(this);
                                t.trigger("beforeshow.tooltip");
                                var o = t.data("tooltip").tooltip;
                                t.data("tooltipBlockClass") && $("." + t.data("tooltipBlockClass")).remove(), o.show(), t.before(o), o.bind({
                                    "mouseleave.tooltip": e.hide
                                }), $(window).width() < 575 && $(".modal .js-tooltip").data("tooltipAroundPosition", "top"), o.data("position", void 0 !== t.data("tooltipPosition") ? t.data("tooltipPosition") : "left"), o.data("aroundPosition", void 0 !== t.data("tooltipAroundPosition") ? t.data("tooltipAroundPosition") : "top"), o.data("animation", void 0 !== t.data("tooltipAnimation") && t.data("tooltipAnimation")), o.data("delay", void 0 !== t.data("tooltipDelay") && t.data("tooltipDelay")), t.data("currentTooltip", o), t.trigger("show.tooltip"), TooltipsterSettings.setTooltipDimensions.apply(this, o), t.trigger("aftershow.tooltip"), o.data("animation") && (o.css("opacity", 0), o.animate({
                                    opacity: 1
                                }, 200)), o.data("delay") && (o.css("opacity", 0), o.delay(1e3 * parseFloat(o.data("delay"))).animate({
                                    opacity: 1
                                }, 0))
                            }
                        },
                        get: function() {
                            return $(this).data("tooltip").tooltip
                        },
                        hide: function(t) {
                            if (TooltipsterSettings.needHide(t, this)) {
                                var e, o = $(this);
                                o.data("currentTooltip") ? (o.trigger("hide.tooltip"), e = o.data("currentTooltip")) : (o.next().trigger("hide.tooltip"), e = o.next().data("currentTooltip")), e.data("delayHide", void 0 !== o.data("tooltipDelayHide") && o.data("tooltipDelayHide")), e.data("animation") ? e.animate({
                                    opacity: 0
                                }, 200, (function() {
                                    e.removeAttr("style"), e.remove()
                                })) : (e = e.data("delayHide") ? e.delay(1e3 * parseFloat(e.data("delayHide"))) : e).animate({
                                    opacity: 0
                                }, 10, (function() {
                                    e.removeAttr("style"), e.remove()
                                }))
                            }
                        },
                        update: function(t) {
                            var e = $($(this).data("currentTooltip"));
                            e.find(".js-tooltip-block__text").html(t), TooltipsterSettings.setTooltipDimensions.apply(this, e)
                        },
                        setContent: function(t) {
                            var e = $(this).data("tooltip").tooltip;
                            e.find(".js-tooltip-block__text").html(t), TooltipsterSettings.setTooltipDimensions.apply(this, e)
                        }
                    };
                    $.fn.tooltip = function(o) {
                        return e[o] ? e[o].apply(this, Array.prototype.slice.call(arguments, 1)) : "object" !== t(o) && o ? void $.error("Метод с именем " + o + " не существует для jQuery.tooltip") : e.init.apply(this, arguments)
                    }
                })), $(document).on("touchstart", ".js-tooltip-block", (function(t) {
                    $(t.target).is("a") || $(this).remove()
                }))
            }
        },
        e = {};

    function o(n) {
        var i = e[n];
        if (void 0 !== i) return i.exports;
        var a = e[n] = {
            exports: {}
        };
        return t[n](a, a.exports, o), a.exports
    }
    o.d = function(t, e) {
        for (var n in e) o.o(e, n) && !o.o(t, n) && Object.defineProperty(t, n, {
            enumerable: !0,
            get: e[n]
        })
    }, o.o = function(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, o.r = function(t) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(t, "__esModule", {
            value: !0
        })
    }, Object.defineProperty(o, "p", {
        get: function() {
            try {
                if ("string" != typeof chunkCdnUrl) throw new Error("WebpackRequireFrom: 'chunkCdnUrl' is not a string or not available at runtime. See https://github.com/agoldis/webpack-require-from#troubleshooting");
                return chunkCdnUrl
            } catch (t) {
                return console.error(t), "/"
            }
        },
        set: function(t) {
            console.warn("WebpackRequireFrom: something is trying to override webpack public path. Ignoring the new value" + t + ".")
        }
    }), o(85635), o(91230), o(85751), o(50901), o(63856), o(35498), o(41986), window.defferScripts.triggerExecuted("generalJs")
}();