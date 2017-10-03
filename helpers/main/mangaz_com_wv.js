// curl 'https://vw.mangaz.com/virgo/docx/127751.json' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: virgo!__ticket=f5271cde4b37ea9c26f7f32694175a38dcd183c9; virgo!marker=127751%3A0' --data '__ticket=f5271cde4b37ea9c26f7f32694175a38dcd183c9&pub=-----BEGIN+PUBLIC+KEY-----%0D%0AMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAIhwp2SCbWQEp2aji0sv8hX0aID7kU0D%0D%0AD2D4uvtpSN5PTiXEYLCk3WsjZlodDLKLWm%2FdQ11y0JfPR%2FY6PDKwiYECAwEAAQ%3D%3D%0D%0B-----END+PUBLIC+KEY-----%0D%0A' --compressed

$(function() {
    if (window.JCOMI)
        throw Error("JCOMI LIBRARY ERROR");
    window.JCOMI = {};
    JCOMI.namespace = function(e) {
        e = e.split(".");
        var a = JCOMI;
        "JCOMI" === e[0] && (e = e.slice(1));
        for (var b = 0; b < e.length; ++b)
            "undefined" === typeof a[e[b]] && (a[e[b]] = {}),
            a = a[e[b]];
        return a
    }
    ;
    JCOMI.log = new function() {
        function e(b) {
            try {
                for (var d = 1; d < arguments.length; d++)
                    b = b.replace(new RegExp("\\{" + (d - 1) + "\\}","g"), arguments[d]);
                "undefined" != typeof console && ("undefined" != typeof console.debug ? a && console.debug(b) : "undefined" != typeof console.log && a && console.log(b))
            } catch (n) {}
        }
        var a = !0;
        this.setEnableLog = function(b) {
            a = b
        }
        ;
        this.debug = function(b) {
            e(b)
        }
    }
});
$(function() {
    JCOMI.config = new function() {
        this.getVersion = function() {
            return "6.2.1"
        }
        ;
        var e = {
            ar: "Arabic",
            "bs-Latn": "Bosnian (Latin)",
            bg: "Bulgarian",
            ca: "Catalan",
            "zh-CHS": "Chinese Simplified",
            "zh-CHT": "Chinese Traditional",
            hr: "Croatian",
            cs: "Czech",
            da: "Danish",
            nl: "Dutch",
            en: "English",
            et: "Estonian",
            fi: "Finnish",
            fr: "French",
            de: "German",
            el: "Greek",
            ht: "Haitian Creole",
            he: "Hebrew",
            hi: "Hindi",
            mww: "Hmong Daw",
            hu: "Hungarian",
            id: "Indonesian",
            it: "Italian",
            ja: "Japanese",
            sw: "Kiswahili",
            tlh: "Klingon",
            "tlh-Qaak": "Klingon (pIqaD)",
            ko: "Korean",
            lv: "Latvian",
            lt: "Lithuanian",
            ms: "Malay",
            mt: "Maltese",
            no: "Norwegian",
            fa: "Persian",
            pl: "Polish",
            pt: "Portuguese",
            otq: "Querétaro Otomi",
            ro: "Romanian",
            ru: "Russian",
            "sr-Cyrl": "Serbian (Cyrillic)",
            "sr-Latn": "Serbian (Latin)",
            sk: "Slovak",
            sl: "Slovenian",
            es: "Spanish",
            sv: "Swedish",
            th: "Thai",
            tr: "Turkish",
            uk: "Ukrainian",
            ur: "Urdu",
            vi: "Vietnamese",
            cy: "Welsh",
            yua: "Yucatec Maya"
        };
        this.getBingLangTable = function() {
            return e
        }
        ;
        var a = {
            af: null,
            be: null,
            bg: "bg",
            ca: "ca",
            cs: "cs",
            da: "da",
            de: "de",
            "de-AU": "de",
            "de-CH": "de",
            "de-DE": "de",
            el: "el",
            en: "en",
            "en-GB": "en",
            "en-US": "en",
            es: "es",
            "es-AR": "es",
            "es-CO": "es",
            "es-ES": "es",
            "es-MX": "es",
            eu: null,
            fi: "fi",
            fo: null,
            fr: "fr",
            "fr-BE": "fr",
            "fr-CA": "fr",
            "fr-CH": "fr",
            "fr-FR": "fr",
            ga: null,
            gd: null,
            gl: null,
            hr: "hr",
            hu: "hu",
            id: "id",
            is: null,
            it: "it",
            ja: "en",
            ko: "ko",
            mk: null,
            nl: "nl",
            "nl-BE": "nl",
            no: "no",
            pl: "pl",
            pt: "pt",
            "pt-BR": "pt",
            ro: "ro",
            ru: "ru",
            sk: "sk",
            sl: "sl",
            sq: null,
            sr: null,
            sv: "sv",
            tr: "tr",
            uk: "uk",
            zh: "zh-CHS",
            "zh-CN": "zh-CHS",
            "zh-TW": "zh-CHT"
        };
        this.getTranslateLangCode = function(b) {
            return a[b] ? a[b] : "en"
        }
        ;
        this.getEnableLog = function() {
            return !0
        }
        ;
        this.getTwoPageMaxImageWidth = function() {
            return 827
        }
        ;
        this.getTwoPageMaxImageHeight = function() {
            return 1170
        }
        ;
        this.getSinglePageMaxImageWidth = function() {
            return 827
        }
        ;
        this.getSinglePageMaxImageHeight = function() {
            return 1170
        }
        ;
        this.getTranslateTimeout = function() {
            return 1E4
        }
        ;
        this.getGoogleTtsMaxLength = function() {
            return 100
        }
        ;
        this.getServerErrMsg = function() {
            return "サーバーと通信できませんでした。"
        }
    }
});
$(function() {
    function e() {
        return /opera/i.test(navigator.userAgent) ? "Opera" : /msie/i.test(navigator.userAgent) ? "IE" : /trident/i.test(navigator.userAgent) ? "IE" : /chrome/i.test(navigator.userAgent) ? "Chrome" : /safari/i.test(navigator.userAgent) ? "Safari" : /firefox/i.test(navigator.userAgent) ? "FireFox" : /gecko/i.test(navigator.userAgent) ? "Gecko" : "else"
    }
    JCOMI.vname = "virgo";
    JCOMI.log.setEnableLog(JCOMI.config.getEnableLog());
    JCOMI.sample = function() {}
    ;
    JCOMI.getTimestamp = function() {
        var a = new Date
          , b = a.getHours()
          , d = a.getMinutes()
          , n = a.getSeconds()
          , a = a.getMilliseconds();
        return b + ":" + d + ":" + n + ":" + a
    }
    ;
    JCOMI.setDisplayPosition = function() {
        var a = "0px";
        $("body").height() > $("#viewer").height() + $("#tool_bar").height() && (a = ($("body").height() - ($("#viewer").height() + $("#tool_bar_frame").height())) / 2 + "px");
        $("#viewer").css("margin-top", a)
    }
    ;
    JCOMI.ajaxPost = function(a) {
        var b = $.extend({
            url: "",
            type: "POST",
            dataType: "json",
            timeout: 1E4,
            success: function() {},
            error: function() {}
        }, a);
        $.ajax({
            url: b.url,
            type: b.type,
            dataType: b.dataType,
            data: b.data,
            timeout: b.timeout,
            async: b.async,
            success: function(a, n) {
                b.success(a, n)
            },
            error: function(a, n, e) {
                b.error(a, n, e)
            }
        })
    }
    ;
    JCOMI.DropDownList = function(a) {
        var b = $.extend({
            selector: "#"
        }, a).selector;
        this.getSelectedValue = function() {
            return $(":selected", $(b)).val()
        }
        ;
        this.getSelectedText = function() {
            return $(":selected", $(b)).text()
        }
        ;
        this.setSelectedValue = function(a) {
            var n = $(b).children();
            $.each(n, function() {
                a == $(this).val() ? $(this).attr("selected", !0) : $(this).attr("selected", !1)
            })
        }
    }
    ;
    JCOMI.TimeoutTimer = function(a) {
        var b = $.extend({
            timeoutMsec: 1E4,
            timeout: function() {}
        }, a), d = !1, n = !1, e;
        this.start = function(c) {
            var a = $.extend(b, c);
            d = !1;
            n = !0;
            clearTimeout(e);
            return e = setTimeout(function() {
                n ? (d = !0,
                n = !1,
                a.timeout()) : (clearTimeout(e),
                d = n = !1)
            }, b.timeoutMsec)
        }
        ;
        this.stop = function() {
            var c = d;
            clearTimeout(e);
            d = n = !1;
            return c
        }
        ;
        this.isWait = function() {
            return !d
        }
    }
    ;
    JCOMI.isChrome = function() {
        return "Chrome" == e() ? !0 : !1
    }
    ;
    JCOMI.getBrowser = function() {
        return e()
    }
});
$(function() {
    JCOMI.PageSlider = new function(e) {
        function a(a) {
            return a
        }
        function b(a) {
            return d.max + 1 - a
        }
        var d = $.extend({
            selector: "",
            min: 1,
            max: 255,
            value: 3,
            isNormal: !0,
            onSlide: function(a) {},
            onStop: function(a) {}
        }, e);
        this.setPageSliderOption = function(a) {
            d = $.extend(d, a)
        }
        ;
        this.initPageSlider = function() {
            var e = d.min
              , r = d.max + 1
              , c = d.value
              , h = a;
            d.isNormal || (c = r - c,
            h = b);
            $(d.selector).slider({
                min: e,
                max: d.max,
                value: c,
                slide: function(a, c) {
                    var b = h(c.value);
                    d.onSlide(b)
                },
                stop: function(a, c) {
                    var b = h(c.value);
                    d.onStop(b)
                }
            })
        }
        ;
        this.setPageSliderValue = function(a) {
            d.isNormal || (a = b(a));
            $(d.selector).slider("option", "value", a)
        }
    }
});
$(function() {
    JCOMI.document = new function(e) {
        function a(a) {
            a = parseInt(a);
            a = 1E3 * (a - 10) - (new Date).getTime();
            0 >= a && (a = 1E3);
            p.start({
                timeoutMsec: a
            })
        }
        function b(b) {
            try {
                var d = q + "/" + JCOMI.vname + "/docx/" + w + ".json"
                  , e = r.getApiParam();
                e.pub = forge.pki.publicKeyToPem(g.publicKey);
                forge.pki.privateKeyToPem(g.privateKey);
                JCOMI.ajaxPost({
                    url: d,
                    data: e,
                    success: function(d, e) {
                        if ("OK" != d.status) {
                            JCOMI.log.debug("" + JCOMI.vname + "API get page information failed.");
                            if (confirm(c.getServerErrMsg() + "\n\nリトライしますか？")) {
                                window.location.href = d.redirect;
                                return
                            }
                            window.close()
                        }
                        var k = window.atob(d.bi)
                          , m = g.privateKey.decrypt(window.atob(d.ek))
                          , k = forge.aes.startDecrypting(m, k);
                        k.update(forge.util.createBuffer(window.atob(d.data)));
                        k.finish();
                        k = $.parseJSON(k.output.toString());
                        "undefined" !== typeof k.Enc && (k.Enc.key = window.atob(k.Enc.key),
                        k.Enc.iv = window.atob(k.Enc.iv));
                        h = k;
                        a(h.bingToken.expires);
                        b()
                    },
                    error: function(a, b, g) {
                        JCOMI.log.debug(b);
                        confirm(c.getServerErrMsg() + "\n\nリトライしますか？") ? window.location.reload() : window.close()
                    },
                    dataType: "json"
                })
            } catch (l) {
                JCOMI.log.debug(l),
                confirm(c.getServerErrMsg() + "\n\nリトライしますか？") ? window.location.reload() : window.close()
            }
        }
        function d(a) {
            try {
                JCOMI.ajaxPost({
                    url: q + "/" + JCOMI.vname + "/serifs/" + w + ".json",
                    data: r.getApiParam(),
                    success: function(c, b) {
                        "OK" != c.status ? JCOMI.log.debug("" + JCOMI.vname + "API get serifs failed.") : (r._serifs = c._serifs,
                        a())
                    },
                    error: function(a, c, b) {
                        JCOMI.log.debug(c)
                    },
                    dataType: "json"
                })
            } catch (b) {
                JCOMI.log.debug(b),
                confirm(c.getServerErrMsg() + "\n\nリトライしますか？") ? window.location.reload() : window.close()
            }
        }
        function n() {
            try {
                JCOMI.ajaxPost({
                    url: q + "/" + JCOMI.vname + "/bingToken/" + w + ".json",
                    data: r.getApiParam(),
                    success: function(c, b) {
                        "OK" != c.status ? JCOMI.log.debug("" + JCOMI.vname + "API get bing token failed.") : (h.bingToken = c.bingToken,
                        a(h.bingToken.expires))
                    },
                    error: function(a, c, b) {
                        JCOMI.log.debug(c)
                    },
                    dataType: "json"
                })
            } catch (b) {
                JCOMI.log.debug(b),
                confirm(c.getServerErrMsg() + "\n\nリトライしますか？") ? window.location.reload() : window.close()
            }
        }
        var r = this
          , c = JCOMI.namespace("JCOMI.config")
          , h = null
          , u = null
          , y = !1
          , w = $("#baid").val()
          , q = $("#host").val()
          , A = $("body").hasClass("smp")
          , t = $("body").hasClass("tablet")
          , g = forge.pki.rsa.generateKeyPair(512)
          , F = __serial;
        __serial = null;
        var p = new JCOMI.TimeoutTimer({
            timeoutMsec: 6E6,
            timeout: function() {
                p.stop();
                n()
            }
        });
        this.initialize = function(a) {
            b(a);
            $("#version").text(c.getVersion());
            a = c.getBingLangTable();
            $("#Language > option").remove();
            $.each(a, function(a, c) {
                var b = $("<option>").val(a).text(c);
                $("#Language").append(b)
            })
        }
        ;
        this.getDoc = function() {
            return h
        }
        ;
        this.getProtect = function() {
            return y
        }
        ;
        this.setProtect = function(a) {
            y = a
        }
        ;
        this.getBaid = function() {
            return w
        }
        ;
        this.isMobile = function() {
            return A
        }
        ;
        this.isTablet = function() {
            return t
        }
        ;
        this.isSmartPhone = function() {
            return A && !t
        }
        ;
        this.getUser = function() {
            return h.User
        }
        ;
        this.getUserPremium = function() {
            return h.User.premium
        }
        ;
        this.getBook = function() {
            return h.Book
        }
        ;
        this.getBookPageUrl = function() {
            return h.Book.url
        }
        ;
        this.getImages = function() {
            return h.Images
        }
        ;
        this.getImageSide = function(a) {
            return h.Images[a].side
        }
        ;
        this.getLoaction = function() {
            return h.Location
        }
        ;
        this.getLocationDir = function(a) {
            return h.Location.base + h.Location[a]
        }
        ;
        this.getPageDirection = function() {
            return h.Book.page_direction
        }
        ;
        this.getPageLayout = function() {
            return h.Book.page_layout
        }
        ;
        this.isTwoPageLayout = function() {
            return "TwoPageLeft" == h.Book.page_layout || "TwoColumnLeft" == h.Book.page_layout || "TwoPageRight" == h.Book.page_layout || "TwoColumnRight" == h.Book.page_layout ? !0 : !1
        }
        ;
        this.getPageMaxWidth = function() {
            return parseInt(h.Book.page_max_width)
        }
        ;
        this.getPageMaxHeight = function() {
            return parseInt(h.Book.page_max_height)
        }
        ;
        this.getImageCount = function() {
            return parseInt(h.Book.image_count)
        }
        ;
        this.getR18 = function() {
            return h.Book.r18
        }
        ;
        this.getRating = function() {
            return parseInt(h.Book.rating)
        }
        ;
        this.getLang = function() {
            return u ? u : lang = this.getDefaultTranslateLang()
        }
        ;
        this.setLang = function(a, c) {
            u = a;
            c && $.cookie(JCOMI.vname + "!lang", u, {
                path: "/" + JCOMI.vname + "/",
                expires: 30
            })
        }
        ;
        this.getBrowserLanguage = function() {
            return window.navigator.languages && window.navigator.languages[0] || window.navigator.language || window.navigator.userLanguage || window.navigator.browserLanguage
        }
        ;
        this.getDefaultTranslateLang = function() {
            var a = this.getBrowserLanguage();
            return c.getTranslateLangCode(a)
        }
        ;
        this.getServerDomain = function() {
            return h.Location.domain
        }
        ;
        this.getBaid = function() {
            return h.Book.baid
        }
        ;
        this.getDebug = function() {
            return h.debug
        }
        ;
        this.getApiParam = function() {
            var a = $.cookie(JCOMI.vname + "!__ticket");
            return {
                __serial: F,
                __ticket: a
            }
        }
        ;
        this.isLogin = function() {
            return void 0 == h ? !1 : h.User.login
        }
        ;
        this.getBingToken = function() {
            return h.bingToken.token
        }
        ;
        this.loadSerifs = function(a) {
            d(a)
        }
    }
});
$(function() {
    JCOMI.viewer = new function(e) {
        function a() {
            $(".page .speech_bubble").remove()
        }
        function b(f) {
            if (D) {
                var a = "center";
                t.isTwoPageDisplay() && (a = g.getImageSide(f));
                var M = $(".page." + a).width()
                  , c = $(".page." + a).height();
                $(".page." + a + " .screen").width(M).height(c);
                c = $(".page." + a + " .page_unit").width();
                $(".page." + a + " .screen").css("left", (c - M) / 2);
                $(".page." + a + " .speech_bubble").remove();
                g._serifs[f] && $.each(g._serifs[f].s, function(f, a) {
                    lang = g.getLang();
                    a[lang] ? d(a, a[lang].text) : A(a, "ja", lang)
                })
            }
        }
        function d(f, a) {
            var c = f.ino;
            if (c == p || c == z) {
                var b = "center";
                t.isTwoPageDisplay() && (b = g.getImageSide(c));
                var d = g._serifs[c]
                  , c = $(".page." + b + " .screen").height()
                  , e = c / d.img.ih
                  , d = $("#template .speech_bubble").clone(!0);
                d.attr("id", "serif" + f.id);
                d.html(a);
                var h = f.y * e;
                d.css("left", f.x * e).css("top", h);
                e *= f.w;
                100 < e && d.css("max-width", e + "px");
                $(".page." + b + " .screen").append(d);
                b = d.height();
                h + b > c && (d.css("max-height", c - h + "px"),
                d.css("max-width", "300px"));
                d.show()
            }
        }
        function n(f) {
            f = parseInt(f);
            $(".page .page_unit").hide();
            a();
            p = f;
            r(f, !0);
            var c = g.getImages()
              , b = c[f].pair_no;
            t.isTwoPageDisplay() ? null != b ? (z = b,
            b < f && (z = p,
            p = b),
            r(b, !1)) : (z = null,
            $(".page." + ("left" == c[f].side ? "right" : "left")).hide()) : z = null
        }
        function r(f, a) {
            f = parseInt(f);
            var c = g.getImageSide(f);
            t.isTwoPageDisplay() || (c = "center");
            "center" == c ? ($(".page.left").hide(),
            $(".page.right").hide()) : $(".page.center").hide();
            c = ".page." + c;
            $(c).data("image", f).show();
            var d = y(f);
            if (null != d && "undefined" !== typeof v[k][f] && "undefined" !== typeof v[k][f].loaded && !1 !== v[k][f].loaded) {
                c += " .page_unit";
                if ("undefined" === typeof g.getDoc().Location.enc)
                    $(c + " .image").attr("src", d.src);
                else {
                    var e = c + " canvas"
                      , h = $(c).width()
                      , H = $(c).height();
                    $(e).attr("width", h);
                    $(e).attr("height", H);
                    $(e).get(0).getContext("2d").drawImage(d, 0, 0, d.width, d.height, 0, 0, h, H)
                }
                $(c).show();
                b(f);
                if ("undefined" === typeof J[f] || 0 == J[f])
                    J[f] = !0,
                    x++
            } else
                a && (B && (B.stop(),
                B = null),
                u(f + 1, 4, !0))
        }
        function c() {
            var f = g.getPageMaxWidth()
              , a = g.getPageMaxHeight()
              , c = f
              , b = a;
            g.isMobile() ? (b = $("#viewer").height(),
            c = $("#viewer").width(),
            t.isTwoPageDisplay() && (c /= 2),
            b / c > a / f ? (b = Math.floor(c / f * a),
            c = b / a * f) : (c = Math.floor(b / a * f),
            b = c / f * a),
            $("#viewer .page").width(c).height(b),
            $("#viewer #book").height(b),
            t.isTwoPageDisplay() ? $("#viewer #book").width(2 * c) : $("#viewer #book").width(c),
            f = ($("#viewer").height() - $("#viewer #book").height()) / 2,
            a = ($("#viewer").width() - $("#viewer #book").width()) / 2,
            $("#viewer #book").css("top", f),
            $("#viewer #book").css("left", a)) : (m ? ($("html").css("overflow", "hidden"),
            b = $(window).innerHeight(),
            c = Math.floor(b / a * f),
            b = c / f * a,
            $("#viewer .page").width(c).height(b - 2),
            $("html").css("overflow", "auto")) : $("#viewer .page").width(c).height(b),
            t.isTwoPageDisplay() ? ($("#viewer").width(2 * c + 16),
            $("#viewer #book").width(2 * c)) : ($("#viewer").width(c + 40),
            $("#viewer #book").width(c)),
            f = ($("body").width() - $("#viewer").width()) / 2,
            0 > f ? f = 0 : 160 < f && (f = 160),
            $(".ad_wall.left").width(f),
            $(".ad_wall.left").css("left", -1 * f),
            $(".ad_wall.right").width(f),
            $(".ad_wall.right").css("right", -1 * f))
        }
        function h(f) {
            B && B.stop();
            B = new JCOMI.TimeoutTimer({
                timeoutMsec: 5E3
            });
            B.start(f)
        }
        function u(f, a, c) {
            var b = g.getImageCount()
              , d = f;
            if (0 < a)
                for (f = i = 0; 10 > i; ) {
                    d >= b && (d = 0);
                    if (w(d))
                        d++;
                    else if (y(d),
                    d++,
                    ++f >= a)
                        break;
                    i++
                }
            else
                0 > a || (c = !1);
            c && b <= E && (c = !1);
            c && h({
                timeout: function() {
                    u(d, a, !0)
                }
            })
        }
        function y(f) {
            var a = g.getImageCount();
            if (0 > f || a <= f)
                return null;
            var c = null;
            if (w(f))
                c = v[k][f].image;
            else {
                v[k][f] = {
                    image: null,
                    loaded: !1
                };
                var b = g.getDoc()
                  , a = g.getImages()
                  , a = g.getLocationDir(k) + a[f].file + "?vw=" + encodeURIComponent(F.getVersion())
                  , c = new Image;
                if ("undefined" === typeof b.Location.enc)
                    v[k][f].image = c,
                    c.onload = function() {
                        v[k][f].loaded = !0;
                        E++;
                        p != f && z != f || r(f)
                    }
                    ,
                    c.src = a;
                else {
                    v[k][f].image = c;
                    var d = new XMLHttpRequest;
                    d.open("GET", a, !0);
                    d.responseType = "arraybuffer";
                    d.onload = function() {
                        var a = forge.aes.startDecrypting(b.Enc.key, b.Enc.iv);
                        a.update(forge.util.createBuffer(this.response));
                        a.finish();
                        c.onload = function() {
                            v[k][f].loaded = !0;
                            E++;
                            p != f && z != f || r(f)
                        }
                        ;
                        c.src = "data:image/jpg;base64," + a.output.toString()
                    }
                    ;
                    d.send()
                }
            }
            return c
        }
        function w(a) {
            return "undefined" === typeof v[k][a] || "undefined" === typeof v[k][a].image || null === v[k][a].image ? !1 : !0
        }
        function q(a) {
            if (!(x <= H && p == N))
                try {
                    var c = g.getBaid()
                      , b = "/" + JCOMI.vname + "/pp/" + c + ".json"
                      , d = g.getApiParam();
                    d.pages = x;
                    d.current_image_no = p;
                    JCOMI.ajaxPost({
                        url: b,
                        data: d,
                        success: function(a, c) {
                            "OK" != a.status ? JCOMI.log.debug("" + JCOMI.vname + " " + b + " failed.") : (H = x,
                            N = p)
                        },
                        error: function(a, c, f) {
                            JCOMI.log.debug(c)
                        },
                        async: a,
                        dataType: "json"
                    })
                } catch (e) {
                    JCOMI.log.debug(e)
                }
        }
        function A(a, c, b) {
            var e = a[c].text;
            c == b ? d(a, e) : (c = {
                appId: "Bearer " + g.getBingToken(),
                from: c,
                to: b,
                text: e
            },
            $.ajax({
                url: "https://api.microsofttranslator.com/V2/Ajax.svc/Translate",
                type: "GET",
                dataType: "text",
                data: c,
                timeout: 1E4,
                success: function(c, e) {
                    var g = c, h;
                    null !== (h = /^"(.+)"$/i.exec(c)) && (g = h[1]);
                    g = g.replace(/\\"/gi, '"');
                    a[b] = {
                        text: g
                    };
                    d(a, g)
                },
                error: function(a, c, f) {
                    JCOMI.log.debug(c)
                }
            }))
        }
        var t = this
          , g = JCOMI.namespace("JCOMI.document")
          , F = JCOMI.namespace("JCOMI.config")
          , p = 0
          , z = null
          , k = "hq"
          , m = !0
          , l = !1
          , D = !1
          , G = []
          , C = {
            langChanged: function() {}
        }
          , B = null
          , v = {
            hq: [],
            st: [],
            enc: []
        }
          , E = 0
          , J = {}
          , x = 0
          , H = 0
          , N = 0
          , O = null;
        e = g.isSmartPhone() ? 60 : 40;
        console.log(e);
        var K = new JCOMI.TimeoutTimer({
            timeoutMsec: 1E3 * e,
            timeout: function() {
                K.stop();
                $(".ad_overlap_wrapper").fadeIn(1E3)
            }
        })
          , I = new JCOMI.TimeoutTimer({
            timeoutMsec: 3E5,
            timeout: function() {
                I.stop();
                q(!0);
                I.start()
            }
        })
          , L = new JCOMI.TimeoutTimer({
            timeoutMsec: 200,
            timeout: function() {
                a();
                n(p)
            }
        });
        this.addComicEventListener = function(a) {
            var c = $.extend({}, C);
            $.extend(c, a);
            G.push(c)
        }
        ;
        this.initialize = function() {
            "undefined" !== typeof g.getDoc().Location.enc ? k = "enc" : (k = "st",
            $(".page .image").show(),
            $(".page canvas").remove());
            var a = g.getUser();
            p = parseInt(a.initial.image_no);
            (a = t.getImageNoFromUrl()) && (p = parseInt(a));
            if (p >= g.getImageCount() || 0 > p)
                p = 0;
            a = p;
            u(a, 4, !0);
            1 <= a && u(a - 1, -2);
            1 == g.getPageDirection() ? ($(".page.first").addClass("right"),
            $(".page.second").addClass("left")) : ($(".page.first").addClass("left"),
            $(".page.second").addClass("right"));
            $(".flip-left").css("cursor", "url(/virgo/img/arrow_btn_left_on.cur),move");
            $(".flip-right").css("cursor", "url(/virgo/img/arrow_btn_right_on.cur),move");
            g.isMobile() && (10 <= g.getUserPremium() ? $("#viewer").css("bottom", "0") : $("#viewer").css("bottom", "50px"));
            c();
            I.start()
        }
        ;
        this.startup = function() {
            $("#initial-screen").hide();
            18 <= g.getBook().rating && 0 == g.getUser().adult_gate && !$.cookie(JCOMI.vname + "!adult") && (g.setProtect(!0),
            $("#protect").show(),
            $("#show_dialog").dialog({
                modal: !0,
                buttons: {
                    "読みます": function() {
                        $(this).dialog("close")
                    },
                    "本を閉じます": function() {
                        t.exitViewer();
                        return !1
                    }
                },
                close: function() {
                    $.cookie(JCOMI.vname + "!adult", 1, {
                        path: "/" + JCOMI.vname + "/",
                        expires: 1
                    });
                    $("#protect").hide();
                    g.setProtect(!1)
                }
            }));
            $("#viewer").show();
            t.movePage(p, !0)
        }
        ;
        this.getImageNoFromUrl = function() {
            var a = location.hash;
            return a && a.match(/#i:(\d+)/) || window.location.href.match(/\/i:(\d+)/) ? parseInt(RegExp.$1) : null
        }
        ;
        this.getCurrentImageNo = function() {
            return p
        }
        ;
        this.isBookmarkEnabled = function(a) {}
        ;
        this.isBookmarkSelected = function(a) {
            var c = !1
              , b = $.cookie(JCOMI.vname + "!bookmark");
            if (null != b && (b = b.split(":"),
            2 == b.length)) {
                var d = b[1];
                b[0] == g.getBaid() && parseInt(d) == a && (c = !0)
            }
            return c
        }
        ;
        this.isLikeEnabled = function(a) {}
        ;
        this.isLikeSelected = function(a) {}
        ;
        this.countLike = function(a) {
            return 0
        }
        ;
        this.countLikeLevel = function(a) {
            a = this.countLike(a);
            return 0 >= a || 0 == a ? 0 : 20 >= a ? 1 : 100 >= a ? 2 : 3
        }
        ;
        this.isMostLike = function(a) {
            return !1
        }
        ;
        this.isTweetEnabled = function(a) {}
        ;
        this.selectBookmark = function(a) {
            $.cookie(JCOMI.vname + "!bookmark", g.getBaid() + ":" + a, {
                path: "/",
                domain: g.getLocation().domain,
                expires: 365
            })
        }
        ;
        this.unselectBookmark = function(a) {
            $.cookie(JCOMI.vname + "!bookmark", null, {
                path: "/",
                domain: g.getLocation().domain,
                expires: 365
            })
        }
        ;
        this.selectLike = function(a) {
            this._pagefav(a, 1)
        }
        ;
        this.unselectLike = function(a) {
            this._pagefav(a, 0)
        }
        ;
        this._pagefav = function(a, c) {
            if (!_doc.Pages[a] || "image" != _doc.Pages[a].unit)
                return !1;
            var b = String(_doc.Pages[a].i);
            if (c)
                _doc.User.Favs.push(b),
                _doc.Favs.list[b] || (_doc.Favs.list[b] = 0),
                _doc.Favs.list[b]++;
            else {
                var d = jQuery.inArray(b, _doc.User.Favs);
                _doc.User.Favs.splice(d, 1);
                _doc.Favs.list[b] && _doc.Favs.list[b]--
            }
            try {
                var e = "/" + JCOMI.vname + "/pagefav/" + _doc.getBaid() + "/" + b + "/" + c
                  , g = $.cookie(JCOMI.vname + "!__ticket");
                JCOMI.ajaxPost({
                    url: e,
                    data: {
                        __ticket: g,
                        __dataset: __dataset,
                        __serial: __serialx
                    },
                    success: function(a, c) {
                        "OK" == a.status && (_doc.User.Favs = a._doc.User.Favs,
                        _doc.Favs = a._doc.Favs)
                    },
                    error: function(a, c, b) {},
                    dataType: "json"
                })
            } catch (h) {}
        }
        ;
        this.isTwoPageDisplay = function() {
            return g.isMobile() && "landscape" != O ? !1 : g.isTwoPageLayout()
        }
        ;
        this.movePage = function(a, c) {
            n(a);
            $.cookie("" + JCOMI.vname + "!marker", g.getBaid() + ":" + p, {
                path: "/" + JCOMI.vname + "/",
                expires: 365
            });
            this.hasNextPage();
            this.hasPrevPage() ? $(".flip .prev").show() : $(".flip .prev").hide();
            $(document).scrollTop(0);
            1 == g.getPageDirection() ? $(document).scrollLeft($(document).width()) : $(document).scrollLeft(0)
        }
        ;
        this.nextPage = function() {
            if (!this.hasNextPage())
                return this.jumpFinishPage();
            var a = 1;
            this.isTwoPageDisplay() && (a = 2);
            var a = p + a
              , c = g.getImageCount();
            c <= a && (a = c - 1);
            this.movePage(a, !1)
        }
        ;
        this.prevPage = function() {
            if (!this.hasPrevPage())
                return !1;
            var a = 1;
            this.isTwoPageDisplay() && (a = 2);
            a = p - a;
            0 > a && (a = 0);
            this.movePage(a, !1)
        }
        ;
        this.hasNextPage = function() {
            var a = g.getImageCount()
              , c = 1;
            this.isTwoPageDisplay() && (c = 2);
            return a - p > c ? !0 : !1
        }
        ;
        this.hasPrevPage = function() {
            return 0 < p ? !0 : !1
        }
        ;
        this.toggleDisplay = function() {
            m = l ? !0 : m ? !1 : !0;
            c();
            n(p)
        }
        ;
        this.getDisplayFit = function() {
            return m
        }
        ;
        this.isFullscreen = function() {
            return l
        }
        ;
        this.toggleFullscreen = function() {
            l ? ($.fullscreen.exit(),
            l = !1) : ($("body").fullscreen(),
            m = l = !0)
        }
        ;
        this.resize = function(b) {
            L.isWait() ? L.stop() : a();
            L.start();
            c()
        }
        ;
        this.setScreenOrientation = function(a) {
            O = a
        }
        ;
        this.jumpFinishPage = function() {
            var a = g.getBaid()
              , a = g.getLoaction().host + "/book/fin/" + a;
            window.location.href = a;
            return !1
        }
        ;
        this.exitViewer = function() {
            var a = g.getBookPageUrl();
            try {
                if (window.opener) {
                    window.opener.location.href = a;
                    window.blur();
                    window.opener.focus();
                    window.close();
                    return
                }
            } catch (c) {}
            location.href = a;
            return !1
        }
        ;
        this.unload = function() {
            I.stop();
            q(!1)
        }
        ;
        this.getDisplaySerif = function() {
            return D
        }
        ;
        this.toggleSerif = function() {
            D = D ? !1 : !0;
            this.refreshSerif()
        }
        ;
        this.refreshSerif = function() {
            D ? (a(),
            g.getImages(),
            b(p),
            null != z && b(z)) : a()
        }
        ;
        this.closeAdOverlap = function() {
            $(".ad_overlap_wrapper").hide();
            10 > g.getUser().premium && (K.stop(),
            K.start())
        }
    }
});
$(function() {
    JCOMI.event = new function(e) {
        function a() {
            $("#toolbar").addClass("visible");
            $("#top-area").hide();
            $(".attention-bounce").removeClass("bounce").removeClass("animated");
            window.setTimeout(function() {
                $(".attention-bounce").addClass("bounce").addClass("animated")
            }, 200)
        }
        function b() {
            $("#toolbar").removeClass("visible");
            $("#top-area").show()
        }
        function d() {
            $("#toolbar").hasClass("visible") ? b() : a();
            return !1
        }
        function n(a) {
            G && (G = !1,
            a(),
            setTimeout(function() {
                $(".tap").hide();
                G = !0
            }, 100))
        }
        function r() {
            if (l.getProtect())
                return !1;
            m.nextPage();
            k.update();
            return !1
        }
        function c() {
            if (l.getProtect())
                return !1;
            m.prevPage();
            k.update();
            return !1
        }
        function h() {
            if (l.getProtect())
                return !1;
            m.movePage(0);
            k.update();
            return !1
        }
        function u() {
            if (l.getProtect())
                return !1;
            var a = l.getImageCount();
            m.movePage(a - 1);
            k.update();
            return !1
        }
        function y() {
            return l.getProtect() ? !1 : l._serifs ? w() : (l.loadSerifs(w),
            !1)
        }
        function w() {
            k._bubble_zidx = 50;
            m.toggleSerif();
            k.update();
            return !1
        }
        function q() {
            m.resize(this.update);
            k.update();
            g()
        }
        function A(a, b, d, e) {
            if (l.getProtect())
                return !1;
            a = $(window).height() < $(document).height() ? 1 : 0;
            if (0 < e) {
                if (0 < $(window).scrollTop())
                    return C = 0,
                    !0;
                if (C < a)
                    return C++,
                    !1;
                C = 0;
                if (l.getPageDirection()) {
                    if ($(window).scrollLeft() + $(window).width() + 20 < $(document).width())
                        return $(document).scrollLeft($(window).width()),
                        $(window).scrollTop() + $(window).height() == $(document).height() && $(document).scrollTop(0),
                        !1
                } else if (0 < $(window).scrollLeft())
                    return $(document).scrollLeft(0),
                    $(window).scrollTop() + $(window).height() == $(document).height() && $(document).scrollTop(0),
                    !1;
                c()
            } else if (0 > e) {
                if ($(window).scrollTop() + $(window).height() < $(document).height())
                    return C = 0,
                    !0;
                if (C < a)
                    return C++,
                    !1;
                C = 0;
                if (l.getPageDirection()) {
                    if (0 < $(window).scrollLeft())
                        return $(document).scrollLeft(0),
                        $(window).scrollTop() + $(window).height() == $(document).height() && $(document).scrollTop(0),
                        !1
                } else if ($(window).scrollLeft() + $(window).width() + 20 < $(document).width())
                    return $(document).scrollLeft($(window).width()),
                    $(window).scrollTop() + $(window).height() == $(document).height() && $(document).scrollTop(0),
                    !1;
                r()
            }
            return !1
        }
        function t() {
            $("#protect, #protect .attention").show();
            l.setProtect(!0);
            return !1
        }
        function g() {
            $("iframe").blur();
            $("#protect .attention").is(":visible") && ($("#protect, #protect .attention").hide(),
            $(window.top).focus(),
            l.setProtect(!1));
            return !1
        }
        function F() {
            m.closeAdOverlap();
            g();
            return !1
        }
        function p(a) {}
        function z(a) {
            m.movePage(a);
            k.update()
        }
        $.extend({}, e);
        var k = this
          , m = JCOMI.namespace("JCOMI.viewer")
          , l = JCOMI.namespace("JCOMI.document")
          , D = JCOMI.namespace("JCOMI.PageSlider")
          , G = !0
          , C = 0
          , B = null
          , v = null
          , E = 50;
        this.initialize = function() {
            $("#toolbar").addClass("visible");
            setTimeout(function() {
                $("#toolbar").removeClass("visible")
            }, 1500);
            $(window.top).blur(function() {
                t()
            });
            $(window.top).focus(function() {
                g()
            });
            $(document).on("keyup", function(a) {
                switch (a.keyCode) {
                case 44:
                    return window.clipboardData && window.clipboardData.clearData(),
                    t(),
                    !1
                }
            });
            $(document).on("keydown", function(a) {
                if (a.altKey || a.ctrlKey || a.shiftKey && a.ctrlKey)
                    return t(),
                    !1
            });
            $("#protect, #un-protect").on("click", function() {
                g()
            });
            var e = "pgdn, space, down, enter"
              , x = "pgup, backspace, up";
            1 == l.getPageDirection() ? (e += ", left",
            x += ", right",
            $(".btnNext span").text("進む"),
            $(".btnBack span").text("戻る"),
            $(".btnNext").addClass("next"),
            $(".btnBack").addClass("prev"),
            $(".flip.flip-right").addClass("prev"),
            $(".flip.flip-left").addClass("next"),
            B = r,
            v = c) : (e += ", right",
            x += ", left",
            $(".btnNext span").text("戻る"),
            $(".btnBack span").text("進む"),
            $(".btnNext").addClass("prev"),
            $(".btnBack").addClass("next"),
            $(".flip.flip-left").addClass("prev"),
            $(".flip.flip-right").addClass("next"),
            B = c,
            v = r);
            $(document).jkey(e, function() {
                1 == l.getPageDirection() ? $(".tap.left").show() : $(".tap.right").show();
                n(r)
            });
            $(document).jkey(x, function() {
                1 == l.getPageDirection() ? $(".tap.right").show() : $(".tap.left").show();
                n(c)
            });
            $(document).jkey("home", function() {
                n(h)
            });
            $(document).jkey("end", function() {
                n(u)
            });
            $(document).jkey("m", function() {
                n(d)
            });
            $(window).on("load orientationchange resize", function() {
                if (l.isMobile()) {
                    var a;
                    a = window.orientation ? 90 === Math.abs(window.orientation) ? "landscape" : "portrait" : $(window).innerHeight() <= $(window).innerWidth() ? "landscape" : "portrait";
                    m.setScreenOrientation(a)
                }
                q()
            });
            $(document).on("mousewheel", "html", function(a, c, b, d) {
                return A(a, c, b, d)
            });
            (l.isMobile() || "IE" != JCOMI.getBrowser()) && $("#viewer").swipe({
                swipe: function(a, b, d, e, g, h) {
                    k._swiped = !0;
                    "left" == b ? v() : "right" == b ? B() : "up" == b ? c() : "down" == b && r()
                },
                threshold: 40
            });
            l.isMobile() ? ($(".next").swipe({
                tap: function(a, c) {
                    return r(a)
                }
            }),
            $(".prev").swipe({
                tap: function(a, b) {
                    return c(a)
                }
            }),
            $(".menu").swipe({
                tap: function(a, c) {
                    return d()
                }
            }),
            $("#top-area").swipe({
                tap: function(a, c) {
                    return d()
                }
            })) : ($(".next").on("click", function(a) {
                return r(a)
            }),
            $(".prev").on("click", function(a) {
                return c(a)
            }),
            $(".menu").on("click", function(a) {
                return d()
            }),
            $("#top-area").mouseenter(function() {
                a()
            }),
            $("#toolbar").mouseleave(function() {
                b()
            }));
            e = "ontouchstart"in document ? "touchstart" : "mousedown";
            x = "ontouchend"in document ? "touchend" : "mouseup";
            $(".flip-left").on(e, function() {
                $(".tap.left").show()
            });
            $(".flip-left").on(x, function() {
                $(".tap.left").hide()
            });
            $(".flip-right").on(e, function() {
                $(".tap.right").show()
            });
            $(".flip-right").on(x, function() {
                $(".tap.right").hide()
            });
            $(".menu").on(e, function() {
                $("#toolbar").hasClass("visible") ? $(".tap.menu-up").show() : $(".tap.menu-down").show()
            });
            $(".menu").on(x, function() {
                $("#toolbar").hasClass("visible") ? $(".tap.menu-up").hide() : $(".tap.menu-down").hide()
            });
            $(".speech_bubble").click(function() {
                var a = $(this).css("z-index");
                E < a && (E = a);
                $(this).css("z-index", ++E)
            });
            e = "ontouchend"in document ? "click touchend" : "click";
            JCOMI.log.debug(e);
            $(".ad_overlap_close_btn").on(e, function() {
                F();
                return !1
            });
            if (l.isMobile())
                $(".ad_overlap_wrapper").on(e, function() {
                    F();
                    return !1
                });
            $(".size-fix").on(e, function() {
                m.toggleDisplay();
                k.update();
                return !1
            });
            $(".fullscreen").on(e, function() {
                m.toggleFullscreen();
                k.update();
                g();
                return !1
            });
            $(".serif").on(e, function() {
                return y()
            });
            $(".exit").on(e, function() {
                m.exitViewer();
                return !1
            });
            $(window).on("beforeunload", function(a) {
                m.unload()
            });
            D.setPageSliderOption({
                selector: "#slider",
                max: l.getImageCount() - 1,
                value: m.getCurrentImageNo(),
                isNormal: 0 == l.getPageDirection() ? !0 : !1,
                onSlide: p,
                onStop: z
            });
            D.initPageSlider();
            $(".help").colorbox({
                inline: !0
            });
            $(".setting").colorbox({
                inline: !0,
                speed: 150,
                onOpen: function() {
                    $("#Language").val(l.getLang())
                }
            });
            $(".twshare").click(function() {
                var a = l.getBook()
                  , c = encodeURIComponent(window.location.href)
                  , b = a.title;
                document.volume && (b += " " + document.volume);
                b += " (p" + (m.getCurrentImageNo() + 1) + ")";
                a.Authors && (b += " [" + a.Authors.join(",") + "]");
                a = " #マンガ図書館Z" + (1 == parseInt(a.site_target) ? "R18" : "");
                b = encodeURIComponent(a + " " + b + "\n");
                window.open("https://twitter.com/share?url=" + c + "&text=" + b, "_tweet", "width=550,height=450").focus()
            });
            $(".tshirt").click(function() {
                window.location.href = $(".tshirt").data("host") + "/shop/tshirt/goods/" + $(".tshirt").data("no") + "/viewer/" + l.getBaid() + "/" + m.getCurrentImageNo()
            });
            $("#Language").change(function() {
                "" == $("#Language").val() ? $("#Language").val(l.getLang()) : (l.setLang($("#Language").val(), !0),
                $.colorbox.close(),
                m.refreshSerif(),
                k.update())
            });
            $("#toolbarMod").show()
        }
        ;
        this.update = function() {
            m.hasPrevPage() ? $(".flip.prev").show() : $(".flip.prev").hide();
            var a = m.getCurrentImageNo();
            $(".current-number").text(a + 1);
            $(".total-number").text(l.getImageCount());
            D.setPageSliderValue(m.getCurrentImageNo());
            m.getDisplayFit() ? ($(".btnZoom span").text("100%"),
            $(".btnZoom").removeClass("fit")) : ($(".btnZoom span").text("ﾌｨｯﾄ"),
            $(".btnZoom").addClass("fit"));
            m.isFullscreen() ? ($(".btnAll span").text("通常画面"),
            $(".btnAll").addClass("return")) : ($(".btnAll span").text("全画面"),
            $(".btnAll").removeClass("return"));
            m.getDisplaySerif() ? $(".btnSerif").addClass("on") : $(".btnSerif").removeClass("on");
            var c;
            window.history.replaceState ? (c = window.location.href.match(/\/i:(\d+)/) ? window.location.href.replace(/\/i:(\d+)/, "/i:" + a) : window.location.href + "/i:" + a,
            window.history.replaceState(JCOMI.vname, "", c)) : (window.location.hash = "#i:" + a,
            c = window.location.href + "/i:" + a);
            var b = "p" + (parseInt(a) + 1);
            $(".page.center").is(":hidden") && (b = [],
            $(".page.left").is(":visible") && b.push("p" + (parseInt($(".page.left").data("image")) + 1)),
            $(".page.right").is(":visible") && b.push("p" + (parseInt($(".page.right").data("image")) + 1)),
            b = b.join(" : "));
            $("#page-display").text(b);
            $("meta.share-url").prop("content", c);
            $("meta.image-url").prop("content", window.location.protocol + "//" + window.location.host + "/img/share/" + l.getBaid() + "/" + a)
        }
    }
    ({})
});
$(document).ready(function() {
    var e = JCOMI.namespace("JCOMI.document")
      , a = JCOMI.namespace("JCOMI.viewer")
      , b = JCOMI.namespace("JCOMI.event");
    $(".social").hide();
    $("body").bind("contextmenu", function(a) {
        return 0 != e.getDebug() ? !0 : !1
    });
    document.oncopy = function(a) {
        return !1
    }
    ;
    $("div").css("user-select", "none");
    e.initialize(function() {
        a.initialize();
        b.initialize();
        a.startup();
        b.update()
    })
});
function parseUri(e) {
    var a = parseUri.options;
    e = a.parser[a.strictMode ? "strict" : "loose"].exec(e);
    for (var b = {}, d = 14; d--; )
        b[a.key[d]] = e[d] || "";
    b[a.q.name] = {};
    b[a.key[12]].replace(a.q.parser, function(d, e, c) {
        e && (b[a.q.name][e] = c)
    });
    return b
}
parseUri.options = {
    strictMode: !1,
    key: "source protocol authority userInfo user password host port relative path directory file query anchor".split(" "),
    q: {
        name: "queryKey",
        parser: /(?:^|&)([^&=]*)=?([^&]*)/g
    },
    parser: {
        strict: /^(?:([^:\/?#]+):)?(?:\/\/((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?))?((((?:[^?#\/]*\/)*)([^?#]*))(?:\?([^#]*))?(?:#(.*))?)/,
        loose: /^(?:(?![^:@]+:[^:@\/]*@)([^:\/?#.]+):)?(?:\/\/)?((?:(([^:@]*)(?::([^:@]*))?)?@)?([^:\/?#]*)(?::(\d*))?)(((\/(?:[^?#](?![^?#\/]*\.[^?#\/.]+(?:[?#]|$)))*\/?)?([^?#\/]*))(?:\?([^#]*))?(?:#(.*))?)/
    }
};
window.sprintf || function() {
    var e = {
        i: 32785,
        d: 32785,
        u: 32801,
        o: 33121,
        x: 33377,
        X: 37473,
        f: 146,
        c: 10240,
        s: 132
    }
      , a = /%(?:(\d+)\$)?(#|0)?(\d+)?(?:\.(\d+))?(l)?([%iduoxXfcs])/g;
    window.sprintf = function(b) {
        var d = 1
          , n = 0
          , r = arguments;
        return b.replace(a, function(a, b, u, y, w, q, A) {
            if ("%" === A)
                return "%";
            a = "";
            q = e[A];
            var t;
            n = b ? parseInt(b) : d++;
            q & 1024 || (a = void 0 === r[n] ? "" : r[n]);
            q & 3 && (a = q & 1 ? parseInt(a) : parseFloat(a),
            a = isNaN(a) ? "" : a);
            q & 4 && (a = (("s" === A ? a : A) || "").toString());
            q & 32 && (a = 0 <= a ? a : a % 4294967296 + 4294967296);
            q & 768 && (a = a.toString(q & 256 ? 8 : 16));
            q & 64 && "#" === u && (a = (q & 256 ? "0" : "0x") + a);
            q & 128 && w && (a = q & 2 ? a.toFixed(w) : a.slice(0, w));
            q & 24576 && (t = "number" !== typeof a || 0 > a);
            q & 8192 && (a = t ? "" : String.fromCharCode(a));
            q & 32768 && (u = "0" === u ? "" : u);
            a = q & 4096 ? a.toString().toUpperCase() : a.toString();
            q & 2048 || void 0 === y || a.length >= y || (b = Array(y - a.length + 1).join(u ? "#" === u ? " " : u : " "),
            a = q & 16 && "0" === u && !a.indexOf("-") ? "-" + b + a.slice(1) : b + a);
            return a
        })
    }
}();
