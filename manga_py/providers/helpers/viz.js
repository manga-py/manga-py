// TODO: delete me
/**
 * @license
 Hammer.JS - v2.0.4 - 2014-09-28
 http://hammerjs.github.io/

 Copyright (c) 2014 Jorik Tangelder;
 Licensed under the MIT license */
'use strict';
/**
 * @return {undefined}
 */
function debugLogger() {
}
/**
 * @return {?}
 */
function usingFlashReader() {
  return !(Modernizr.canvas && Modernizr.blobconstructor && Modernizr.cors && "true" != flashtest);
}
/**
 * @return {undefined}
 */
function popOut() {
  if (embedded = false, true !== $.browser.mobile) {
    var photoText = $("#reader_header").detach();
    $("#modal-reader").append(photoText);
    $("#reader_tools .reader-popout").addClass("disp-n");
    $("#reader_tools .reader-embed").removeClass("disp-n");
  } else {
    $("#reader_close_control_mobile").show();
  }
  var photoText = $("#reader_window").detach();
  $("#modal-reader").append(photoText);
  ModalReader.toggle("#modal-reader");
  setTimeout(function() {
    openReader();
    googletag.pubads().refresh();
    setTimeout(adjustChapterAd, 250);
  }, 100);
}
/**
 * @return {undefined}
 */
function embed() {
  /** @type {boolean} */
  embedded = true;
  $("#reader_tools .reader-popout").removeClass("disp-n");
  $("#reader_tools .reader-embed").addClass("disp-n");
  if (true === $.browser.mobile) {
    $("#reader_close_control_mobile").hide();
  }
  ModalReader.toggle("#modal-reader");
  openReader();
  googletag.pubads().refresh();
  setTimeout(adjustChapterAd, 250);
}
/**
 * @param {?} url
 * @return {undefined}
 */
function openReaderWrapper(url) {
  if (!readerOpen) {
    /**
     * @return {undefined}
     */
    var handler = function() {
      if (pages > 0) {
        $(document).trigger("open_manga_reader");
        Tracking.sendEvent({
          category : "Manga Reader",
          action : "Open",
          label : getGAEventLabel()
        });
        if (embedded) {
          openReader();
        } else {
          setTimeout(openReader, 100);
          ModalReader.toggle("#modal-reader");
        }
      }
    };
    if (getIsArchiveChapter()) {
      var result = mangaAuthWrapper(manga_id, handler);
      if ("function" == typeof url) {
        result.done(url);
      }
    } else {
      handler();
    }
  }
}
/**
 * @return {undefined}
 */
function openReader() {
  if (true === $.browser.mobile) {
    $("#reader_wrapper").addClass("mobile").css({
      position : "relative"
    });
    $("#reader_container_sc").show();
    $("#reader_page_container").css({
      overflow : "visible"
    });
    setPageMode(true);
    if (!readerOpened) {
      initReader();
      showMobileMenus();
    }
    setupStyles();
    if (readerOpened) {
      loadPages();
      setBookmarkIcon();
      updateDisplayedPages();
      updateOffscreenPages();
      if (embedded) {
        window.scrollTo(0, $("#site-header").height());
      } else {
        window.scrollTo(0, 0);
      }
    } else {
      initEndPages();
      setBookmarkIcon(true);
    }
  } else {
    $("#modal-reader-header h2").html(seriesTitle + ", " + getDisplayName() + (isPreview ? " - Free Preview" : ""));
    if (usingFlashReader()) {
      adjustFlashReader();
    } else {
      $("#reader_wrapper").addClass("not-mobile");
      $("#reader_container_sc").show();
      setPageMode(true);
      if (!readerOpened) {
        initReader();
      }
      setupPageLabels();
      setupStyles();
      if (readerOpened) {
        loadPages();
        setBookmarkIcon();
        updateDisplayedPages();
        updateOffscreenPages();
      } else {
        initEndPages();
        setBookmarkIcon(true);
      }
    }
  }
  /** @type {boolean} */
  readerOpen = true;
  /** @type {boolean} */
  readerOpened = true;
  $(document).trigger("reader_open");
}
/**
 * @param {?} canCreateDiscussions
 * @return {undefined}
 */
function closeReader(canCreateDiscussions) {
  var $newUl = $("#reader_top_container");
  var $drag = $("#reader_bottom_container");
  /** @type {!HTMLDocument} */
  var el = document;
  if (true === $.browser.mobile) {
    clearTimeout(menuTimeout);
    /** @type {number} */
    menuTimeout = 0;
    $newUl.css({
      top : "-" + $newUl.height() + "px"
    }).addClass("m_closed");
    $drag.css({
      bottom : "-" + $drag.height() + "px"
    }).addClass("m_closed");
    $(".readerImgPage").hide();
  }
  if (fullscreenMode) {
    if (el.exitFullscreen) {
      el.exitFullscreen();
    } else {
      if (el.webkitExitFullscreen) {
        el.webkitExitFullscreen();
      } else {
        if (el.mozCancelFullScreen) {
          el.mozCancelFullScreen();
        } else {
          if (el.msExitFullscreen) {
            el.msExitFullscreen();
          }
        }
      }
    }
  }
  $("#reader_container_sc, #reader_container_fl").hide();
  ModalReader.close();
  /** @type {boolean} */
  readerOpen = false;
  if (!canCreateDiscussions) {
    $(el).trigger("reader_closed");
  }
}
/**
 * @param {!Object} id
 * @return {undefined}
 */
function setPageMode(id) {
  var t = $("#reader_wrapper");
  var $allPanels = $("#reader_container_sc");
  var mainViewList = $("#reader_page_container");
  if (true === $.browser.mobile) {
    /** @type {number} */
    var r = 0;
    /** @type {number} */
    var x2 = 0;
    t.width($(window).width());
    var height = window.innerHeight ? window.innerHeight : $(window).height();
    if (debugLogger("Viewport height: " + height), embedded) {
      var s = $("#embedded_mobile_drag_bar");
      if (s.removeClass("disp-n"), 0 == window.orientation && debugLogger("Usable height: " + (height = Math.min(t.width() / refPageWidth, height / refPageHeight) * refPageHeight)), height = height - s.outerHeight(), id) {
        var d = $("#reader_window").detach();
        s.before(d);
        $("#product_image_block, #buy-digital-viz").hide();
      }
    }
    t.height(height);
    if (0 == window.orientation) {
      $allPanels.removeClass("mobile_landscape").addClass("mobile_portrait");
      /** @type {number} */
      respMultiplier = Math.min(t.width() / refPageWidth, t.height() / refPageHeight);
      if (2 == pageMode) {
        togglePageMode(id);
      }
      $(".reader_page_canvas.left, .reader_page_canvas.right").hide();
      $(".reader_page_canvas.single").show();
      /** @type {number} */
      r = -2 * (x2 = refPageWidth * respMultiplier) - 4 * mainViewList.offset().left;
      if (0 != pageModeOffset) {
        /** @type {number} */
        r = -x2 - 2 * mainViewList.offset().left;
      }
      if (isLR) {
        /** @type {number} */
        r = -r;
      }
      $(".reader_page_canvas.single.next").css({
        left : r
      });
      /** @type {number} */
      r = x2 + 2 * mainViewList.offset().left;
      if (0 != pageModeOffset) {
        /** @type {number} */
        r = 2 * x2 + 4 * mainViewList.offset().left;
      }
      if (isLR) {
        /** @type {number} */
        r = -r;
      }
      $(".reader_page_canvas.single.previous").css({
        left : r
      });
    } else {
      $allPanels.removeClass("mobile_portrait").addClass("mobile_landscape");
      /** @type {number} */
      respMultiplier = t.height() / refPageHeight;
      if (1 == pageMode) {
        togglePageMode(id);
      }
      $(".reader_page_canvas.left, .reader_page_canvas.right").show();
      $(".reader_page_canvas.single").hide();
      /** @type {number} */
      r = -2 * x2 - 2 * mainViewList.offset().left;
      if (isLR) {
        /** @type {number} */
        r = -r;
      }
      $(".reader_page_canvas.left.next").css({
        left : r
      });
      /** @type {number} */
      r = -x2 - 2 * mainViewList.offset().left;
      if (isLR) {
        /** @type {number} */
        r = 3 * x2 - 2 * mainViewList.offset().left;
      }
      $(".reader_page_canvas.right.next").css({
        left : r
      });
      /** @type {number} */
      r = 2 * x2 + 2 * mainViewList.offset().left;
      if (isLR) {
        /** @type {number} */
        r = -r;
      }
      $(".reader_page_canvas.left.previous").css({
        left : r
      });
      /** @type {number} */
      r = 3 * x2 - 2 * mainViewList.offset().left;
      if (isLR) {
        /** @type {number} */
        r = -x2 - 2 * mainViewList.offset().left;
      }
      $(".reader_page_canvas.right.previous").css({
        left : r
      });
    }
    setRespVars();
  } else {
    var minPxPerValUnit;
    var dtStep;
    /** @type {number} */
    var l = $(window).width() / $(window).height();
    /** @type {number} */
    var imgNowHeight = 10;
    if (embedded && id) {
      var options = $("#embedded_desktop_wrapper");
      var widgetContainer = $("#reader_header").detach();
      d = $("#reader_window").detach();
      options.append(widgetContainer);
      options.append(d);
      dtStep = t.width();
      $("#product_detail").hide();
      $(".reader-close").attr("onclick", "popOut();return false;");
    } else {
      var h = $("#modal-reader");
      dtStep = h.width();
      /** @type {number} */
      imgNowHeight = (h.height() - refSliderHeight - $("#modal-reader-header").outerHeight(true)) / refPageHeight;
    }
    if (0 == userToggledPageMode) {
      if (l > .75 || $(window).width() >= 1E3) {
        t.removeClass("ar-reader-single").addClass("ar-reader-double");
        /** @type {number} */
        minPxPerValUnit = Math.min(t.width(), dtStep) / refSpreadWidth;
        /** @type {number} */
        respMultiplier = Math.min(minPxPerValUnit, imgNowHeight);
        $(".reader-page-mode.single-page").removeClass("disp-n");
        $(".reader-page-mode.double-page").addClass("disp-n");
        if (1 == pageMode) {
          togglePageMode(id);
        }
      } else {
        t.removeClass("ar-reader-double").addClass("ar-reader-single");
        /** @type {number} */
        minPxPerValUnit = Math.min(t.width(), dtStep) / refPageWidth;
        /** @type {number} */
        respMultiplier = Math.min(minPxPerValUnit, imgNowHeight);
        $(".reader-page-mode.single-page").addClass("disp-n");
        $(".reader-page-mode.double-page").removeClass("disp-n");
        if (2 == pageMode) {
          togglePageMode(id);
        }
      }
      setRespVars();
    } else {
      if (1 == pageMode) {
        t.removeClass("ar-reader-double").addClass("ar-reader-single");
        /** @type {number} */
        minPxPerValUnit = Math.min(t.width(), dtStep) / refPageWidth;
        $(".reader-page-mode.single-page").addClass("disp-n");
        $(".reader-page-mode.double-page").removeClass("disp-n");
      } else {
        t.removeClass("ar-reader-single").addClass("ar-reader-double");
        /** @type {number} */
        minPxPerValUnit = Math.min(t.width(), dtStep) / refSpreadWidth;
        $(".reader-page-mode.single-page").removeClass("disp-n");
        $(".reader-page-mode.double-page").addClass("disp-n");
      }
      /** @type {number} */
      respMultiplier = Math.min(minPxPerValUnit, imgNowHeight);
      setRespVars();
    }
  }
}
/**
 * @return {undefined}
 */
function setRespVars() {
  /** @type {number} */
  respSpreadWidth = respMultiplier * refSpreadWidth;
  /** @type {number} */
  respPageWidth = respMultiplier * refPageWidth;
  /** @type {number} */
  respPageHeight = respMultiplier * refPageHeight;
  respTotalHeight = true === $.browser.mobile ? respPageHeight : respPageHeight + refSliderHeight;
}
/**
 * @return {undefined}
 */
function initEndPages() {
  if (!usingFlashReader()) {
    var formattedChosenQuestion = $("#modal-reader-next-up").html();
    if (isPreview && (formattedChosenQuestion = $("#modal-reader-next-up-preview").html()), $("#end_page_end_card").html(formattedChosenQuestion), $("#end_page_end_card .modal-close").remove(), getIsChapter() ? true === $.browser.mobile && ($("#end_page_end_card").removeClass("pad-y-lg").addClass("pad-y-0"), $("#end_page_end_card .o_end-card-spacer").removeClass("mar-y-md mar-y-lg--lg").addClass("mar-y-0"), $("#end_page_end_card .o_end-chapter-list").addClass("mar-t-md--sm mar-b-md--sm"), $("#end_page_end_card .o_chap-dm-links").removeClass("pad-t-md pad-t-lg--lg"),
    $("#end_page_end_card .o_chap-dm-links .read_button_div span").removeClass("type-lg--md type-xl--lg").addClass("type-sm--sm"), $("#end_page_end_card .o_chap-dm-links .read_button_div a").addClass("type-sm--sm pad-sm--sm"), 0 == window.orientation ? ($("#end_page_end_card .o_chapter-container").removeClass("type-md--lg").addClass("type-sm--sm"), $("#end_page_end_card .o_chap-dm-links p").removeClass("type-md--md").addClass("type-sm--sm pad-y-sm--sm")) : ($("#end_page_end_card .o_end-chapter-list").removeClass("type-rg type-sm--sm type-md--lg").addClass("type-tiny"),
    $("#end_page_end_card .o_chapter-container").removeClass("type-rg type-md--lg").addClass("type-tiny"), $("#end_page_end_card .o_chap-dm-links p").removeClass("type-rg type-md--md").addClass("type-tiny pad-y-sm--sm"))) : (true === $.browser.mobile ? ($("#end_page_end_card div.g-3--sm.g-5--md").removeClass("g-3--sm g-5--md"), $("#end_page_end_card div.g-3--sm.g-7--md p.type-md.type-lg--md").removeClass("type-lg--md").addClass("type-rg--sm type-center"), $("#end_page_end_card div.g-3--sm.g-7--md p.type-rg.type-md--md").removeClass("pad-y-md").addClass("type-center"),
    $("#end_page_end_card span.float-r").removeClass("float-r"), $("#end_page_end_card div.g-3--sm.g-7--md").removeClass("g-3--sm g-7--md")) : $("#end_page_end_card div.g-3--sm.g-5--md").removeClass("pad-x-xl").addClass("pad-x-md"), $("#end_page_end_card .modal-field").addClass("mar-x-md")), $("#end_page_end_card .modal-field").attr("style", "position:relative; top:50%; transform:translateY(-50%);"), showRecProps) {
      if (embedded) {
        $("#end_page_discovery img.lazy").each(function() {
          $(this).removeClass("lazy");
          var originalUrl = $(this).attr("data-original");
          $(this).attr("src", originalUrl);
        });
        $("#end_page_discovery .o_sort_container div.g-3").removeClass("g-3 g-3--md").addClass("g-3 g-6--md");
        $("#end_page_discovery .o_sort_container div").each(function() {
          if ($(this).hasClass("g-omega")) {
            $(this).removeClass("g-omega").addClass("g-omega g-omega--md");
          }
        });
        if (true === $.browser.mobile) {
          $("#end_page_discovery .row").removeClass("mar-y-md").addClass("mar-y-sm");
          $("#end_page_discovery .section_title").parent().removeClass("mar-b-lg mar-t-md").addClass("mar-t-md mar-t-sm--sm mar-b-rg mar-b-md--md mar-b-lg--lg");
          $("#end_page_discovery .o_sort_container div.g-3").removeClass("mar-b-lg").addClass("mar-b-md mar-b-sm--sm mar-b-lg--lg");
          if (0 == window.orientation) {
            $("#end_page_discovery .section_title").removeClass("type-md mar-y-rg").addClass("type-rg");
            $("#end_page_discovery .o_sort_container .o_sortable div.type-center").removeClass("pad-x-rg type-rg--sm").addClass("pad-x-sm pad-x-rg--lg type-bs--sm");
            $("#end_page_discovery .o_sort_container .o_sortable a.o_inner-link").removeClass("type-sm--sm mar-b-rg").addClass("mar-b-sm pad-y-0--sm");
          } else {
            $("#end_page_discovery .section_title").removeClass("type-md mar-y-rg").addClass("type-sm");
            $("#end_page_discovery .o_sort_container .o_sortable div.type-center").removeClass("pad-x-rg type-rg--sm type-sm").addClass("pad-x-sm pad-x-rg--lg type-bs");
            $("#end_page_discovery .o_sort_container .o_sortable a.o_inner-link").removeClass("type-sm--sm mar-b-rg type-bs").addClass("mar-b-sm pad-y-0--sm type-tiny");
          }
          $("#end_page_discovery .o_sort_container .o_sortable a.o_inner-link").each(function() {
            var self = $(this).html();
            $(this).html(self.replace("Chapter", "Chap."));
          });
          $("#end_page_discovery section").removeAttr("id").removeClass("bg-off-white").attr("style", "position:relative; top:50%; transform:translateY(-50%); max-width:850px; margin:auto;");
        } else {
          $("#end_page_discovery section").removeAttr("id").removeClass("bg-off-white").attr("style", "position:relative; top:50%; transform:translateY(-50%); max-width:850px; margin:auto;");
        }
        $("#end_page_discovery .section_see_all").remove();
      } else {
        var formattedChosenQuestion = $(".section_properties").html();
        $("#end_page_discovery").html(formattedChosenQuestion);
        $("#end_page_discovery img.lazy").each(function() {
          $(this).removeClass("lazy");
          var originalUrl = $(this).attr("data-original");
          $(this).attr("src", originalUrl);
        });
        if (true === $.browser.mobile) {
          $("#end_page_discovery .section_title").html("VIZ Editors recommend:").addClass("type-sm--sm");
          $("#end_page_discovery .section_title").parent().addClass("mar-b-md--sm");
          $("#end_page_discovery .o_property-link").addClass("mar-b-md--sm");
          $("#end_page_discovery .o_property-link .type-center").removeClass("type-rg--sm").addClass("pad-x-sm--sm pad-y-rg--sm type-bs--sm");
        } else {
          $("#end_page_discovery .property-row div.g-3").removeClass("g-3 g-3--md").addClass("g-3 g-6--md");
          $("#end_page_discovery .property-row div").each(function() {
            if ($(this).hasClass("g-omega")) {
              $(this).removeClass("g-omega").addClass("g-omega g-omega--md");
            }
          });
          $("#end_page_discovery .row.properties").attr("style", "position:relative; top:50%; transform:translateY(-50%); max-width:850px; margin:auto;");
        }
        $("#end_page_discovery .section_see_all").remove();
      }
    }
    if (getIsChapter() && !adFilled) {
      var formattedChosenQuestion = $("#metamodal-chapter-ad").html();
      $("#end_page_ad_container").html(formattedChosenQuestion);
      $("#metamodal-chapter-ad").remove();
      $("#end_page_ad_container .metamodal-close").remove();
      $("#end_page_ad_container .type-sm").remove();
      setTimeout(function() {
        googletag.cmd.push(function() {
          googletag.display("free-chapter-ad");
        });
      }, 250);
      setTimeout(function() {
        adjustChapterAd();
      }, 750);
    }
    $.browser.mobile;
  }
}
/**
 * @return {undefined}
 */
function initReader() {
  if (true === $.browser.mobile) {
    $('meta[name="viewport"]').attr("content", "minimal-ui, initial-scale=1.0, user-scalable=no, width=device-width");
    window.addEventListener("orientationchange", orientationChanged);
    window.scrollTo(0, $("#site-header").height());
    $("#reader_desktop_paging_info").hide();
  } else {
    $("#reader_desktop_paging_info").delay(1E3).fadeOut(150);
  }
  /** @type {(Element|null)} */
  slider = document.getElementById("page_slider");
  /** @type {string} */
  var direction = "rtl";
  if (isLR) {
    /** @type {string} */
    direction = "ltr";
  }
  /** @type {number} */
  var b = pages - 1;
  b = b + endPages.length;
  noUiSlider.create(slider, {
    animate : false,
    start : 0,
    step : 1,
    direction : direction,
    tooltips : true,
    range : {
      min : 0,
      max : b
    }
  });
  $("#reader_zoom_control").val(1);
  var piped = $.ajax({
    dataType : "text",
    url : pageUrl + "&metadata=1&manga_id=" + manga_id
  });
  piped.done(function(canCreateDiscussions) {
    /** @type {string} */
    metadataURL = canCreateDiscussions;
    var piped = $.ajax({
      dataType : "json",
      url : metadataURL
    });
    piped.done(function(value) {
      /** @type {!Object} */
      metadata = value;
      configureListeners();
      loadPages();
    });
    piped.fail(function(isSlidingUp, canCreateDiscussions) {
      debugLogger("get metadata URL request failed: " + canCreateDiscussions);
      configureListeners();
      loadPages();
    });
  });
  piped.fail(function(isSlidingUp, canCreateDiscussions) {
    debugLogger("metadata request failed: " + canCreateDiscussions);
    configureListeners();
    loadPages();
  });
}
/**
 * @return {undefined}
 */
function setupStyles() {
  if (debugLogger("Setting up styles"), true === $.browser.mobile) {
    $("#reader_header").hide();
    var everLeftWidth = 2 == pageMode ? respSpreadWidth : respPageWidth;
    $("#reader_page_container").width(everLeftWidth);
    $("#reader_page_container").height(respPageHeight);
    if (0 == window.orientation) {
      $("#reader_top_container, #reader_bottom_container").removeClass("double_height");
    } else {
      $("#reader_top_container, #reader_bottom_container").addClass("double_height");
    }
    $("#reader_top_container").css({
      top : "-" + $("#reader_top_container").height() + "px"
    });
    $("#reader_top_container #reader_top_header_1_mobile").html(seriesTitle.toUpperCase());
    $("#reader_top_container #reader_top_header_2_mobile").html(getDisplayName().toUpperCase());
    if (isPreview) {
      $(".reader_bookmark_control_mobile").hide();
    } else {
      $("#reader_top_header_3_mobile").html("");
    }
    $("#reader_bottom_container").css({
      bottom : "-" + $("#reader_bottom_container").height() + "px"
    });
    clearTimeout(menuTimeout);
    $("#page_slider").css({
      width : "66%"
    });
    $(".page_slider_label").hide();
  } else {
    $(".page_loader").width(respPageWidth);
    $(".page_loader").height(respPageHeight);
    everLeftWidth = 2 == pageMode ? respSpreadWidth : respPageWidth;
    var nodesLeftToMove = $(window).width();
    /** @type {number} */
    var oldContW = Math.min(nodesLeftToMove, respSpreadWidth);
    $("#reader_page_container").width(everLeftWidth);
    $("#reader_page_slider_container").width(oldContW);
    $("#page_slider").width(oldContW - $(".page_slider_label.left").outerWidth() - $(".page_slider_label.right").outerWidth() - 20);
    /** @type {number} */
    var maxIndexProperty = ($("#reader_wrapper").width() - everLeftWidth) / 2;
    Math.max(200, maxIndexProperty + .25 * everLeftWidth / pageMode);
    $("#reader_page_container").height(respPageHeight);
    $("#reader_window, #reader_wrapper, #reader_container_sc").height(respPageHeight + refSliderHeight);
    $("#reader_bottom_container").css({
      top : respPageHeight + "px"
    });
    $(".reader_pager_container").css("z-index", "1");
    $(".page_loader").css({
      top : "0px",
      position : "absolute",
      "z-index" : "2"
    });
    $(".page_loader.left").css({
      left : "0px"
    });
    $(".page_loader.right").css({
      left : respPageWidth + "px"
    });
    if (isPreview) {
      $("#reader_tools .reader-bookmark").hide();
    }
  }
  $(".reader_page_end").width(respPageWidth);
  $(".reader_page_end").height(respPageHeight);
}
/**
 * @return {undefined}
 */
function configureListeners() {
  if (true === $.browser.mobile) {
    $(".reader_page_canvas.top").on("touchmove", function(event) {
      event.preventDefault();
    });
    $("#reader_bottom_container, #bookmark_icon_mobile").on("touchmove", function() {
      clearTimeout(menuTimeout);
    });
    $("#reader_bottom_container, #bookmark_icon_mobile").on("touchend", function() {
      /** @type {number} */
      menuTimeout = setTimeout(hideMobileMenus, 750);
    });
    $("#bookmark_icon_mobile").on("click", bookmarkIconClicked);
    $(document).on("click_if_logged_in", ".reader_bookmark_control_mobile", function(event) {
      event.preventDefault();
      setBookmark();
    });
    if (embedded) {
      $("#embedded_popout_control_mobile").on("click", popOut);
      $("#reader_close_control_mobile").on("click", embed);
    } else {
      $("#reader_close_control_mobile").on("click", closeReader);
    }
    $(".reader_page_canvas.top").hammer({
      recognizers : [[Hammer.Pinch, {
        enable : true
      }]],
      touchAction : "manipulation"
    });
    var press = new Hammer.Tap({
      event : "singletap"
    });
    var pan = new Hammer.Tap({
      event : "doubletap",
      taps : 2,
      posThreshold : 50
    });
    var pinch = new Hammer.Pan({
      direction : Hammer.DIRECTION_ALL
    });
    var rotate = new Hammer.Swipe({
      direction : Hammer.DIRECTION_HORIZONTAL
    });
    $(".reader_page_canvas.top").data("hammer").add([pan, press, rotate, pinch]);
    pan.recognizeWith(press);
    press.requireFailure(pan);
    pinch.recognizeWith(rotate);
    $(".reader_page_canvas.top").hammer().on("doubletap", doubletapZoom).on("singletap", handleTap).on("panstart", panCanvasStart).on("panend", panCanvasEnd).on("pan", panCanvas).on("pinchstart", pinchZoomStart).on("pinchend", pinchZoomEnd).on("pinch", pinchZoom);
  } else {
    $("#page_container, #reader_container_sc, #reader_header, #reader_header a, #reader_bottom_container").mouseenter(function() {
      $(".reader_pager").stop(true, true).hide();
    });
    $("#reader_left_pager_control").on("click", {
      dir : "left"
    }, pagerClick);
    $("#reader_right_pager_control").on("click", {
      dir : "right"
    }, pagerClick);
    $(".reader_pager.left").on("click", {
      dir : "left"
    }, pagerClick);
    $(".reader_pager.right").on("click", {
      dir : "right"
    }, pagerClick);
    $("#reader_tools .reader-help").on("click", function() {
      MetaModals.toggle("#metamodal-reader-help");
    });
    $("#bookmark_icon").on("click", bookmarkIconClicked);
    $(document).on("click_if_logged_in", "#reader_tools .reader-bookmark", function(event) {
      event.preventDefault();
      setBookmark();
    });
    $("#reader_tools .reader-page-mode").on("click", function() {
      /** @type {number} */
      userToggledPageMode = 1;
      togglePageMode(false);
      setPageMode(false);
      setupStyles();
      updateDisplayedPages();
      updateEndPages();
    });
    $("#reader_tools .reader-fullscreen").on("click", goFullScreen);
    $("#reader_tools .reader-popout").on("click", popOut);
    $("#reader_tools .reader-embed").on("click", embed);
    $("#reader_tools .reader-zoom.zoom-in").on("click", {
      dir : "in"
    }, zoom);
    $("#reader_tools .reader-zoom.zoom-out").on("click", {
      dir : "out"
    }, zoom);
    $(".reader_page_canvas.top").on("mousemove", panOrHover);
    $(".reader_page_canvas.top").on("mouseup", checkClick);
    $(".reader_page_canvas.top").on("mousedown", recordMousePosition);
    $(document).on("webkitfullscreenchange mozfullscreenchange fullscreenchange MSFullscreenChange", respondToFullscreenChange);
    $(document).keydown(function(event) {
      switch(event.which) {
        case 37:
          if (readerOpen) {
            $(".reader_pager.left").trigger("click");
          }
          break;
        case 39:
          if (readerOpen) {
            $(".reader_pager.right").trigger("click");
          }
          break;
        default:
          return;
      }
      event.preventDefault();
    });
  }
  slider.noUiSlider.on("change", function() {
    /** @type {number} */
    var totalPage = Math.floor(slider.noUiSlider.get());
    /** @type {number} */
    page = totalPage % 2 == 0 ? totalPage : totalPage - 1;
    $("#page_slider .noUi-tooltip").hide();
    loadPages();
    /** @type {number} */
    var name = 0;
    if ("blank page" == endPages[0]) {
      /** @type {number} */
      name = 1;
    }
    if (page > pages + name) {
      $(".reader_page_canvas.left, .reader_page_canvas.right").hide();
    } else {
      $(".reader_page_canvas.left, .reader_page_canvas.right").show();
    }
  });
  slider.noUiSlider.on("slide", function() {
    var e = $("#page_slider .noUi-tooltip");
    /** @type {string} */
    var t = Math.floor(slider.noUiSlider.get()).toString();
    if ("0" == t) {
      /** @type {string} */
      t = "1";
    }
    e.html(t);
    e.show();
  });
}
/**
 * @return {undefined}
 */
function toggleTopMenu() {
  var $this = $("#reader_top_menu");
  if ("on" == $this.attr("data-menu-state")) {
    $this.attr("data-menu-state", "off");
    $this.hide();
  } else {
    $this.attr("data-menu-state", "on");
    $("#reader_top_menu").show();
    $(".reader_pager").stop(true, true).hide();
  }
}
/**
 * @param {!Event} options
 * @return {undefined}
 */
function sliderZoom(options) {
  if (null == options.buttons) {
    var toolbarItemsOption = options.which;
  } else {
    toolbarItemsOption = options.buttons;
  }
  if (1 == toolbarItemsOption) {
    var $hnavbox = $("#reader_container_sc");
    var n = $("#reader_page_container");
    var factor = $(this).val();
    /** @type {number} */
    var size = respPageWidth * factor;
    /** @type {number} */
    var winH = respPageHeight * factor;
    if (2 == pageMode) {
      var song_element = $("#canvas_left_current");
    } else {
      song_element = $("#canvas_single_current");
    }
    var left = song_element.position().left;
    var y = song_element.position().top;
    /** @type {number} */
    var i = (left - n.width() / 2) * factor / currentZoom + n.width() / 2;
    if (2 == pageMode) {
      /** @type {number} */
      var contactCapacity = n.width() - 2 * size - ($hnavbox.width() - n.width()) / 2;
      /** @type {number} */
      var startNo = 0;
    } else {
      /** @type {number} */
      contactCapacity = 0 - 3 * n.width();
      /** @type {number} */
      startNo = (n.width() - respPageWidth) / 2;
    }
    if (i < contactCapacity) {
      /** @type {number} */
      i = contactCapacity;
    }
    if (i > startNo) {
      /** @type {number} */
      i = startNo;
    }
    /** @type {number} */
    var t = (y - n.height() / 2) * factor / currentZoom + n.height() / 2;
    /** @type {number} */
    var l = n.height() - winH;
    if (t < l && (t = l), t > 0 && (t = 0), 2 == pageMode) {
      /** @type {number} */
      var x = i + size;
      if (i + 2 * size < (y = n.width())) {
        /** @type {number} */
        i = y - 2 * size;
      }
      $(".reader_page_canvas.bottom.left").css({
        left : i + "px"
      });
      $(".reader_page_canvas.bottom.right").css({
        left : x + "px"
      });
    } else {
      var y;
      if (size < n.width()) {
        if (i + size < (y = n.width() - (n.width() - respPageWidth) / 2)) {
          /** @type {number} */
          i = y - size;
        }
      }
      $(".reader_page_canvas.bottom.single").css({
        left : i + "px"
      });
    }
    $(".reader_page_canvas.bottom").css({
      width : size + "px",
      height : winH + "px",
      top : t + "px"
    });
    if (1 == factor) {
      $(".reader_page_canvas.top").css({
        cursor : "default"
      });
    } else {
      $(".reader_page_canvas.top").css({
        cursor : "move"
      });
    }
    currentZoom = factor;
  }
}
/**
 * @param {!Object} e
 * @return {undefined}
 */
function zoom(e) {
  if (debugLogger(e), "in" == e.data.dir && currentZoom < 4 || "out" == e.data.dir && currentZoom > 1) {
    var $hnavbox = $("#reader_container_sc");
    var a = $("#reader_page_container");
    var width = currentZoom;
    /** @type {number} */
    var interval_in_elements = 125;
    if ("undefined" != typeof e.data.animTime) {
      interval_in_elements = e.data.animTime;
    }
    if ("in" == e.data.dir) {
      width = width + 1;
    } else {
      if ("out" == e.data.dir) {
        /** @type {number} */
        width = width - 1;
      }
    }
    if ("undefined" != typeof e.data.zoomTo) {
      width = e.data.zoomTo;
    }
    /** @type {number} */
    var size = respPageWidth * width;
    /** @type {number} */
    var offset = respPageHeight * width;
    if (2 == pageMode) {
      var song_element = $("#canvas_left_current");
    } else {
      song_element = $("#canvas_single_current");
    }
    var v = song_element.position().left;
    var y = song_element.position().top;
    /** @type {number} */
    var i = (v - a.width() / 2) * width / currentZoom + a.width() / 2;
    if (2 == pageMode) {
      /** @type {number} */
      var contactCapacity = a.width() - 2 * size - ($hnavbox.width() - a.width()) / 2;
      /** @type {number} */
      var startNo = 0;
    } else {
      /** @type {number} */
      contactCapacity = 0 - 3 * a.width();
      /** @type {number} */
      startNo = (a.width() - respPageWidth) / 2;
    }
    if (i < contactCapacity) {
      /** @type {number} */
      i = contactCapacity;
    }
    if (i > startNo) {
      /** @type {number} */
      i = startNo;
    }
    /** @type {number} */
    var t = (y - a.height() / 2) * width / currentZoom + a.height() / 2;
    /** @type {number} */
    var l = a.height() - offset;
    if (t < l && (t = l), t > 0 && (t = 0), 2 == pageMode) {
      if (i + 2 * size < (y = a.width())) {
        /** @type {number} */
        i = y - 2 * size;
      }
      /** @type {number} */
      var x = i + size;
      $("#canvas_left_current").animate({
        width : size + "px",
        height : offset + "px",
        left : i + "px",
        top : t + "px"
      }, interval_in_elements);
      $("#canvas_right_current").animate({
        width : size + "px",
        height : offset + "px",
        left : x + "px",
        top : t + "px"
      }, interval_in_elements);
    } else {
      var y;
      if (size < a.width()) {
        if (i + size < (y = a.width() - (a.width() - respPageWidth) / 2)) {
          /** @type {number} */
          i = y - size;
        }
      }
      $("#canvas_single_current").animate({
        width : size + "px",
        height : offset + "px",
        left : i + "px",
        top : t + "px"
      }, interval_in_elements);
    }
    if (1 == width) {
      $(".reader_page_canvas.top").css({
        cursor : "default"
      });
      updateOffscreenPages();
      if (1 == pageMode) {
        $("#canvas_single_partner_current, #canvas_single_next, #canvas_single_previous").show();
      } else {
        $("#canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous").show();
      }
    } else {
      $(".reader_page_canvas.top").css({
        cursor : "move"
      });
      if (1 == pageMode) {
        $("#canvas_single_partner_current, #canvas_single_next, #canvas_single_previous").hide();
      } else {
        $("#canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous").hide();
      }
    }
    currentZoom = width;
  }
}
/**
 * @param {!MouseEvent} e
 * @return {undefined}
 */
function checkPagers(e) {
  var mainViewList = $(".reader_pager_container.left");
  var $seekBar = $(".reader_pager_container.right");
  var tag_x = mainViewList.offset().left;
  var change_pos = $seekBar.offset().left + $seekBar.width();
  if ((e.pageX < tag_x || e.pageX > change_pos) && 1 != $.browser.mobile) {
    $(".reader_pager").stop(true, true).hide();
    $(".reader_pager_container").css("z-index", "4");
    /** @type {number} */
    pagerTime = 0;
    clearInterval(pagerInterval);
    /** @type {number} */
    pagerInterval = 0;
  }
}
/**
 * @param {!Object} event
 * @return {undefined}
 */
function panOrHover(event) {
  if (null == event.buttons) {
    var keycode = event.which;
  } else {
    keycode = event.buttons;
  }
  var $seekBar = $("#reader_container_sc");
  var l = $("#reader_page_container");
  if (2 == pageMode) {
    var r = $("#canvas_left_current");
  } else {
    r = $("#canvas_single_current");
  }
  $("#canvas_right_current");
  if (1 == keycode && 1 != currentZoom) {
    /** @type {number} */
    pagerTime = 0;
    $(".reader_pager_container").css("z-index", "4");
    $(".reader_pager").stop(true, true).hide();
    /** @type {number} */
    var x = event.pageX - l.offset().left - lastMousePosX;
    /** @type {number} */
    var searchBarHeight = event.pageY - l.offset().top - lastMousePosY;
    var i = r.position().left + x;
    var topOffset = r.position().top + searchBarHeight;
    if (2 == pageMode) {
      /** @type {number} */
      var startPos = l.width() - 2 * r.width() - ($seekBar.width() - l.width()) / 2;
      $seekBar.width();
      l.width();
    } else {
      /** @type {number} */
      startPos = 0 - 3 * l.width();
    }
    /** @type {number} */
    var bottom = l.height() - r.height();
    if (i < startPos && (i = startPos), i > 0 && (i = 0), topOffset < bottom && (topOffset = bottom), topOffset > 0 && (topOffset = 0), $(".reader_page_canvas.bottom").css({
      top : topOffset + "px"
    }), 2 == pageMode) {
      var iSt = l.width();
      if (i + 2 * r.width() < iSt) {
        /** @type {number} */
        i = iSt - 2 * r.width();
      }
      var ffleft = i + r.width();
      $(".reader_page_canvas.bottom.left").css({
        left : i + "px"
      });
      $(".reader_page_canvas.bottom.right").css({
        left : ffleft + "px"
      });
    } else {
      iSt = l.width();
      if (i + r.width() < iSt) {
        /** @type {number} */
        i = iSt - r.width();
      }
      $(".reader_page_canvas.bottom.single").css({
        left : i + "px"
      });
    }
    /** @type {number} */
    lastMousePosX = event.pageX - l.offset().left;
    /** @type {number} */
    lastMousePosY = event.pageY - l.offset().top;
  } else {
    var u = $("#reader_left_pager_container").width();
    var f = (event.pageX, event.pageY, $seekBar.width(), $("#reader_header").height() + 10);
    $("#reader_container_sc").height();
    $("#reader_bottom_container").outerHeight();
    if (!fullscreenMode) {
      $seekBar.offset().left;
    }
    /** @type {number} */
    var x = (event.pageX - l.offset().left - r.position().left) * metadata.width / parseInt(r.css("width").replace(/[^-\d\.]/g, ""));
    /** @type {number} */
    var i = (event.pageY - l.offset().top - r.position().top) * metadata.height / parseInt(r.css("height").replace(/[^-\d\.]/g, ""));
    if (pageLinks.length > 0) {
      var grid;
      /** @type {number} */
      var cnt = 0;
      var context = document.getElementById("canvas_top").getContext("2d");
      if (1 == pageMode) {
        if (0 == pageModeOffset) {
          var a = pageLinks.filter(function(size) {
            return size.x >= metadata.width;
          });
        } else {
          a = pageLinks.filter(function(viz) {
            return viz.x < metadata.width;
          });
        }
      } else {
        a = pageLinks;
      }
      for (; grid = a[cnt++];) {
        var s = grid.x;
        if (1 == pageMode && 0 == pageModeOffset && (s = grid.x - metadata.width), context.beginPath(), context.rect(s, grid.y, grid.width, grid.height), context.isPointInPath(x, i)) {
          $("#canvas_top").css("cursor", "pointer");
          break;
        }
        if (1 == currentZoom) {
          $("#canvas_top").css("cursor", "default");
        } else {
          $("#canvas_top").css("cursor", "move");
        }
      }
    }
  }
}
/**
 * @param {!MouseEvent} event
 * @return {undefined}
 */
function checkClick(event) {
  if (originalMousePosX == lastMousePosX && originalMousePosY == lastMousePosY) {
    $("#reader_container_sc");
    var mainViewList = $("#reader_page_container");
    if (2 == pageMode) {
      var a = $("#canvas_left_current");
    } else {
      a = $("#canvas_single_current");
    }
    /** @type {number} */
    var x = (event.pageX - mainViewList.offset().left - a.position().left) * metadata.width / parseInt(a.css("width").replace(/[^-\d\.]/g, ""));
    /** @type {number} */
    var y = (event.pageY - mainViewList.offset().top - a.position().top) * metadata.height / parseInt(a.css("height").replace(/[^-\d\.]/g, ""));
    if (pageLinks.length > 0) {
      var node;
      /** @type {number} */
      var j = 0;
      var g = document.getElementById("canvas_top").getContext("2d");
      if (1 == pageMode) {
        if (0 == pageModeOffset) {
          var added = pageLinks.filter(function(size) {
            return size.x >= metadata.width;
          });
        } else {
          added = pageLinks.filter(function(viz) {
            return viz.x < metadata.width;
          });
        }
      } else {
        added = pageLinks;
      }
      for (; node = added[j++];) {
        var dx = node.x;
        if (1 == pageMode && 0 == pageModeOffset && (dx = node.x - metadata.width), g.beginPath(), g.rect(dx, node.y, node.width, node.height), g.isPointInPath(x, y)) {
          node.action;
          switch(node.action) {
            case "goToBrowser":
              ": " + node.args;
              window.open(node.args, "vizwin");
              break;
            case "goToDetails":
              ": " + node.args;
              window.open("http://www.vizmanga.com/reader/" + node.args, "vizwin");
              break;
            case "goToPage":
              if (node.args % 2 == 0) {
                page = node.args;
                /** @type {number} */
                pageModeOffset = 0;
              } else {
                /** @type {number} */
                page = node.args - 1;
                /** @type {number} */
                pageModeOffset = 1;
              }
              loadPages();
          }
          ")";
          Tracking.sendEvent({
            category : "Manga Reader",
            action : "Link Area",
            label : getGAEventLabel()
          });
        }
      }
    }
  }
}
/**
 * @param {!MouseEvent} event
 * @return {undefined}
 */
function recordMousePosition(event) {
  var mainViewList = $("#reader_page_container");
  /** @type {number} */
  originalMousePosX = event.pageX - mainViewList.offset().left;
  /** @type {number} */
  originalMousePosY = event.pageY - mainViewList.offset().top;
  /** @type {number} */
  lastMousePosX = event.pageX - mainViewList.offset().left;
  /** @type {number} */
  lastMousePosY = event.pageY - mainViewList.offset().top;
}
/**
 * @return {undefined}
 */
function respondToFullscreenChange() {
  /** @type {boolean} */
  fullscreenMode = !fullscreenMode;
  if (embedded) {
    if (fullscreenMode) {
      $("#embedded_reader").attr("style", "width:100%; height:100%;");
      $("#embedded_desktop_wrapper").removeClass("row-nopad");
      /** @type {boolean} */
      embedded = false;
      setTimeout(function() {
        openReader();
        /** @type {boolean} */
        embedded = true;
        googletag.pubads().refresh();
        adjustChapterAd();
      }, 100);
    } else {
      $("#embedded_reader").removeAttr("style");
      $("#embedded_desktop_wrapper").addClass("row-nopad");
      setTimeout(function() {
        openReader();
        googletag.pubads().refresh();
        adjustChapterAd();
      }, 100);
    }
  }
  if (fullscreenMode) {
    $(".reader-fullscreen, .reader-popout, .reader-embed").addClass("disp-n");
  } else {
    $(".reader-fullscreen").removeClass("disp-n");
    if (embedded) {
      $(".reader-popout").removeClass("disp-n");
    } else {
      if (getIsChapter()) {
        $(".reader-embed").removeClass("disp-n");
      }
    }
  }
  updateOffscreenPages();
  adjustChapterAd();
}
/**
 * @return {undefined}
 */
function goFullScreen() {
  /** @type {(Element|null)} */
  var c = document.getElementById("modal-reader");
  if (embedded) {
    /** @type {(Element|null)} */
    c = document.getElementById("embedded_reader");
  }
  if (c.requestFullscreen) {
    c.requestFullscreen();
  } else {
    if (c.mozRequestFullScreen) {
      c.mozRequestFullScreen();
    } else {
      if (c.webkitRequestFullscreen) {
        c.webkitRequestFullscreen();
      } else {
        if (c.msRequestFullscreen) {
          c.msRequestFullscreen();
        }
      }
    }
  }
}
/**
 * @param {string} right
 * @return {undefined}
 */
function pagerIncrement(right) {
  pagerTime = pagerTime + 1;
  if ((1 == currentZoom && pagerTime > 7 || 1 != currentZoom && pagerTime > 10) && (0 != page || 0 != pageModeOffset || isLR && "left" != right || !isLR && "right" != right)) {
    $("#reader_" + right + "_pager_container").css("z-index", "6");
    $("#reader_" + right + "_pager").fadeIn(100);
  }
}
/**
 * @return {undefined}
 */
function setupPageLabelsDesktop() {
  if (isLR ? ($(".page_slider_label.right").html("Page " + pageStr), $(".page_slider_label.left").html("Page 1")) : ($(".page_slider_label.left").html("Page " + pageStr), $(".page_slider_label.right").html("Page 1")), 0 == page || 1 == page) {
    $(".page_slider_label.center").html("Page: 1");
  } else {
    if (2 == pageMode) {
      if (getIsChapter()) {
        if (page < pages + endPages.length) {
          $(".page_slider_label.center").html("Pages: " + page + " - " + (page + 1));
        } else {
          $(".page_slider_label.center").html("Page: " + page);
        }
      } else {
        $(".page_slider_label.center").html("Pages: " + page + " - " + (page + 1));
      }
    } else {
      if (isLR) {
        $(".page_slider_label.center").html("Page: " + (page + -1 * pageModeOffset + 1));
      } else {
        $(".page_slider_label.center").html("Page: " + (page + pageModeOffset));
      }
    }
  }
}
/**
 * @param {!Object} gestureEvt
 * @return {undefined}
 */
function handleEndPageTap(gestureEvt) {
  gestureEvt.gesture.srcEvent.preventDefault();
  /** @type {boolean} */
  var t = false;
  /** @type {boolean} */
  var a = false;
  /** @type {boolean} */
  var n = false;
  /** @type {boolean} */
  var r = false;
  var e = gestureEvt.gesture.srcEvent;
  var currentValue = e.changedTouches && e.changedTouches.length ? e.changedTouches[0].clientX : e.layerX;
  var s = e.changedTouches && e.changedTouches.length ? e.changedTouches[0].clientY : e.layerY;
  debugLogger("Tap: " + currentValue + ", " + s);
  $("#end_page_discovery a.o_inner-link").each(function() {
    var $elem = $(this);
    var n = $elem.offset().left;
    var a = $elem.offset().top;
    var m = $elem.offset().left + $elem.outerWidth();
    var samplecount = $elem.offset().top + $elem.outerHeight();
    if (currentValue >= n && currentValue < m && s >= a && s < samplecount) {
      /** @type {boolean} */
      t = true;
      /** @type {boolean} */
      a = true;
      $elem[0].click();
    }
  });
  $("#end_page_ad iframe").each(function() {
    var e = $(this);
    var n = e.offset().left;
    var start = e.offset().top;
    var m = e.offset().left + e.width();
    var samplecount = e.offset().top + e.height();
    if (currentValue >= n && currentValue < m && s >= start && s < samplecount && !a) {
      /** @type {boolean} */
      t = true;
      /** @type {boolean} */
      r = true;
      e.contents().find("a")[0].click();
    }
  });
  $("#end_page_discovery .o_sortable a.hover-bg-red").each(function() {
    var $dl = $(this);
    var n = $dl.offset().left;
    var start = $dl.offset().top;
    var m = $dl.offset().left + $dl.width();
    var samplecount = $dl.offset().top + $dl.height();
    if (currentValue >= n && currentValue < m && s >= start && s < samplecount && !a && !r) {
      /** @type {boolean} */
      t = true;
      /** @type {boolean} */
      n = true;
      $dl[0].click();
    }
  });
  $("#end_page_end_card a").each(function() {
    var $elem = $(this);
    var startDate = $elem.offset().left;
    var start = $elem.offset().top;
    var endDate = $elem.offset().left + $elem.outerWidth();
    var samplecount = $elem.offset().top + $elem.outerHeight();
    if (currentValue >= startDate && currentValue < endDate && s >= start && s < samplecount && !n && !a && !r) {
      /** @type {boolean} */
      t = true;
      $elem[0].click();
    }
  });
  if (!t) {
    if (0 == menuTimeout) {
      showMobileMenus();
    } else {
      hideMobileMenus();
    }
  }
}
/**
 * @param {!Object} e
 * @return {undefined}
 */
function handleTap(e) {
  if ("mouse" != e.gesture.pointerType) {
    if (e.gesture.srcEvent.preventDefault(), 1 == pageMode) {
      if (0 == pageModeOffset) {
        var iconsPaged = pageLinks.filter(function(size) {
          return size.x >= metadata.width;
        });
      } else {
        iconsPaged = pageLinks.filter(function(viz) {
          return viz.x < metadata.width;
        });
      }
    } else {
      iconsPaged = pageLinks;
    }
    /** @type {(Element|null)} */
    var canvas = document.getElementById("canvas_top");
    var ctx = canvas.getContext("2d");
    var evt = e.gesture.srcEvent;
    var count = evt.changedTouches && evt.changedTouches.length ? evt.changedTouches[0].clientX : evt.layerX;
    var w = evt.changedTouches && evt.changedTouches.length ? evt.changedTouches[0].clientY : evt.layerY;
    var context = {
      canvas : canvas,
      ctx : ctx,
      tapX : count,
      tapY : w
    };
    if (iconsPaged.length && 1 == currentZoom) {
      var item;
      /** @type {boolean} */
      var pathSettings = false;
      var formdiv = 1 == pageMode ? $("#canvas_single_current") : $("#canvas_left_current");
      /** @type {number} */
      var WHITE = parseInt(formdiv.css("width").replace(/[^-\d\.]/g, ""));
      /** @type {number} */
      var d = parseInt(formdiv.css("height").replace(/[^-\d\.]/g, ""));
      var offset = formdiv.offset().left;
      /** @type {number} */
      var x = count * metadata.width / WHITE;
      /** @type {number} */
      var y = w * metadata.height / d;
      /** @type {number} */
      var i = 0;
      canvas.width = 1 == pageMode ? metadata.width : 2 * metadata.width;
      canvas.height = metadata.height;
      e: for (; item = iconsPaged[i++];) {
        var i = item.x + offset;
        if (1 == pageMode && 0 == pageModeOffset && (i = i - metadata.width), ctx.beginPath(), ctx.rect(i, item.y, item.width, item.height), ctx.isPointInPath(x, y)) {
          switch(item.action) {
            case "goToBrowser":
            case "goToDetails":
              if (true !== $.browser.mobile) {
                /** @type {boolean} */
                pathSettings = true;
              }
              break;
            case "goToPage":
              /** @type {boolean} */
              pathSettings = true;
          }
          if (pathSettings) {
            Tracking.sendEvent({
              category : "Manga Reader",
              action : "Link Area",
              label : getGAEventLabel()
            });
            activateLink(context, function() {
              switch(item.action) {
                case "goToBrowser":
                  window.open(item.args, "vizwin");
                  break;
                case "goToDetails":
                  /** @type {string} */
                  var facebookString = "http://www.vizmanga.com/reader/" + item.args;
                  window.open(facebookString, "vizwin");
                  break;
                case "goToPage":
                  if (item.args % 2 == 0) {
                    page = item.args;
                    /** @type {number} */
                    pageModeOffset = 0;
                  } else {
                    /** @type {number} */
                    page = item.args - 1;
                    /** @type {number} */
                    pageModeOffset = 1;
                  }
                  loadPages();
              }
            });
            break e;
          }
        }
      }
      if (!(pathSettings || checkPageAdvanceTap(e, context))) {
        if (0 == menuTimeout) {
          showMobileMenus();
        } else {
          hideMobileMenus();
        }
      }
    } else {
      if (!checkPageAdvanceTap(e, context)) {
        if (0 == menuTimeout) {
          showMobileMenus();
        } else {
          hideMobileMenus();
        }
      }
    }
  }
}
/**
 * @param {!Object} e
 * @param {!Object} self
 * @return {?}
 */
function checkPageAdvanceTap(e, self) {
  debugLogger(e);
  e.gesture.srcEvent;
  var a = $("#reader_wrapper");
  var w = a.width();
  var p = a.height();
  var i = $("#reader_page_container");
  var startXPos = i.width();
  var sr_size = i.height();
  /** @type {number} */
  var radius = (w - startXPos) / 2 + startXPos / pageMode * .15;
  if (self.canvas.width = w, self.canvas.height = p, self.ctx.beginPath(), self.ctx.rect(w - radius, 0, w, sr_size), self.ctx.isPointInPath(self.tapX, self.tapY)) {
    if (isLR || page > 0) {
      return activateLink(self, function() {
        panCanvasStart(e);
        panCanvas(e);
        panCanvasEnd(e, "right");
      }), true;
    }
  } else {
    if (self.ctx.beginPath(), self.ctx.rect(0, 0, radius, sr_size), self.ctx.isPointInPath(self.tapX, self.tapY) && (!isLR || page > 0)) {
      return activateLink(self, function() {
        panCanvasStart(e);
        panCanvas(e);
        panCanvasEnd(e, "left");
      }), true;
    }
  }
  return false;
}
/**
 * @param {!Object} options
 * @param {!Function} name
 * @return {undefined}
 */
function activateLink(options, name) {
  /** @type {number} */
  options.ctx.globalAlpha = .2;
  /** @type {string} */
  options.ctx.fillStyle = "#ff0000";
  options.ctx.fill();
  setTimeout(function() {
    options.ctx.clearRect(0, 0, options.canvas.width, options.canvas.height);
    /** @type {number} */
    options.ctx.globalAlpha = 1;
    name();
  }, 50);
}
/**
 * @param {!Object} event
 * @return {undefined}
 */
function doubletapZoom(event) {
  if ("mouse" != event.gesture.pointerType) {
    var t = $("#reader_page_container");
    var r = $("#reader_page_container").css("margin-left").replace(/[^-\d\.]/g, "");
    var inSourceThemeName = $("#reader_page_container").css("margin-top").replace(/[^-\d\.]/g, "");
    var itemDim = t.height();
    if (1 == pageMode) {
      var finalWidth = t.width();
    } else {
      /** @type {number} */
      finalWidth = t.width() / 2;
    }
    if (1 == currentZoom) {
      if (1 == pageMode) {
        var $back = $("#canvas_single_current");
      } else {
        $back = $("#canvas_left_current");
      }
      var v_x = event.gesture.center.x;
      var nodeTly = event.gesture.center.y;
      /** @type {number} */
      var imgLeft = t.width() / 2 - 2 * (v_x - r);
      /** @type {number} */
      var tabPadding = t.height() / 2 - 2 * (nodeTly - inSourceThemeName);
      if (imgLeft < -t.width()) {
        /** @type {number} */
        imgLeft = -t.width();
      } else {
        if (imgLeft > 0) {
          /** @type {number} */
          imgLeft = 0;
        }
      }
      if (tabPadding < -t.height()) {
        /** @type {number} */
        tabPadding = -t.height();
      } else {
        if (tabPadding > 0) {
          /** @type {number} */
          tabPadding = 0;
        }
      }
      $back.animate({
        left : imgLeft,
        top : tabPadding,
        width : 2 * finalWidth,
        height : 2 * itemDim
      }, 125);
      if (2 == pageMode) {
        $("#canvas_right_current").animate({
          left : imgLeft + 2 * finalWidth,
          top : tabPadding,
          width : 2 * finalWidth,
          height : 2 * itemDim
        }, 125);
      }
      /** @type {number} */
      currentZoom = 2;
    } else {
      if (1 == pageMode) {
        $back = $("#canvas_single_current");
      } else {
        $back = $("#canvas_left_current");
      }
      $back.animate({
        left : 0,
        top : 0,
        width : finalWidth,
        height : itemDim
      }, 125);
      if (2 == pageMode) {
        $("#canvas_right_current").animate({
          left : t.width() / 2,
          top : 0,
          width : finalWidth,
          height : itemDim
        }, 125);
      }
      /** @type {number} */
      currentZoom = 1;
    }
  }
}
/**
 * @param {!Object} event
 * @return {undefined}
 */
function panCanvasStart(event) {
  gestureCenter = event.gesture.center;
  /** @type {number} */
  var part = 0;
  if ("blank page" == endPages[0]) {
    /** @type {number} */
    part = 1;
  }
  var pageWindow = pageModeOffset;
  if (isLR) {
    /** @type {number} */
    pageWindow = 1 - pageModeOffset;
  }
  if (2 == pageMode && page < pages - 1 || 1 == pageMode && page + pageWindow < pages) {
    debugLogger("panCanvasStart normal page region");
    if (1 == pageMode) {
      refPage = $("#canvas_single_current");
      $(".reader_page_canvas.left, .reader_page_canvas.right").hide();
      $(".reader_page_canvas.single").show();
    } else {
      refPage = $("#canvas_left_current");
      $(".reader_page_canvas.single").hide();
      $(".reader_page_canvas.left, .reader_page_canvas.right").show();
    }
  } else {
    if (2 == pageMode && page <= pages && page >= pages - 1 || 1 == pageMode && page + pageWindow == pages) {
      debugLogger("panCanvasStart boundary region");
      if (1 == pageMode) {
        refPage = $("#canvas_single_current");
        $(".reader_page_canvas.left, .reader_page_canvas.right").hide();
        $(".reader_page_canvas.single, #" + endPages[0 + part]).show();
      } else {
        refPage = $("#canvas_left_current");
        $(".reader_page_canvas.single, .reader_page_canvas.next").hide();
        $(".reader_page_canvas.left.previous, .reader_page_canvas.right.previous").show();
        $("#" + endPages[0 + part]).show();
        if (endPages.length > 1 + part) {
          $("#" + endPages[1 + part]).show();
        }
      }
    } else {
      if (2 == pageMode && page <= pages + endPages.length || 1 == pageMode && page + pageWindow <= pages + endPages.length) {
        debugLogger("panCanvasStart end page region");
        if (2 == pageMode && page == pages + endPages.length || 1 == pageMode && page + pageWindow == pages + endPages.length) {
          $(".reader_page_canvas.top").hammer().off("pan");
          $(".reader_page_canvas.top").hammer().on("pan", panCanvas);
        }
        if (1 == pageMode) {
          if ("blank page" != endPages[page + pageWindow - pages - 1]) {
            refPage = $("#" + endPages[page + pageWindow - pages - 1]);
            if (page - pageWindow - pages <= endPages.length - 1) {
              $("#" + endPages[page - pageModeOffset - pages]).show();
            }
            if (page - pages + 1 <= endPages.length - 1) {
              $("#" + endPages[page - pages + 1]).show();
            }
            if (0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2]) {
              $("#" + endPages[page - pages - 2]).show();
            } else {
              $("#canvas_single_previous").show();
            }
          } else {
            debugLogger("Trying to queue up blank page as refPage");
          }
          $(".reader_page_canvas.left, .reader_page_canvas.right").hide();
        } else {
          if (isLR) {
            refPage = $("#" + endPages[page - pages - 1]);
            if (page - pages <= endPages.length - 1) {
              $("#" + endPages[page - pages]).show();
            }
            if (page - pages + 1 <= endPages.length - 1) {
              $("#" + endPages[page - pages + 1]).show();
            }
            if (page - pages + 2 <= endPages.length - 1) {
              $("#" + endPages[page - pages + 2]).show();
            }
            if (0 <= page - pages - 1 && "blank page" != endPages[page - pages - 1]) {
              $("#" + endPages[page - pages - 1]).show();
            } else {
              $("#canvas_right_previous").show();
            }
            if (0 <= page - pages - 2) {
              $("#" + endPages[page - pages - 2]).show();
            } else {
              $("#canvas_left_previous").show();
            }
          } else {
            refPage = $("#" + endPages[page - pages]);
            if (0 == refPage.length) {
              refPage = $("#end_page_placeholder");
              refPage.css({
                left : 0
              });
            }
            if (page - pages + 2 <= endPages.length - 1) {
              $("#" + endPages[page - pages + 2]).show();
            }
            if (page - pages + 1 <= endPages.length - 1) {
              $("#" + endPages[page - pages + 1]).show();
            }
            if (0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2]) {
              $("#" + endPages[page - pages - 2]).show();
            } else {
              $("#canvas_left_previous").show();
            }
            if (0 <= page - pages - 3) {
              $("#" + endPages[page - pages - 3]).show();
            } else {
              $("#canvas_right_previous").show();
            }
          }
          $(".reader_page_canvas.single").hide();
        }
      }
    }
  }
  debugLogger("Pan canvas start refpage:");
  debugLogger(refPage);
  refOffset = refPage.offset();
  refPosition = refPage.position();
}
/**
 * @param {!Object} t
 * @param {string} side
 * @return {undefined}
 */
function panCanvasEnd(t, side) {
  var $seekBar = $("#reader_page_container");
  /** @type {number} */
  var delay = 150;
  var item = $();
  var t = $();
  var c = $();
  var d = $();
  var info = $();
  var g = $();
  var resize = $();
  var grid = $();
  var a = $();
  var bb = $();
  /** @type {number} */
  var part = 0;
  if ("blank page" == endPages[0]) {
    /** @type {number} */
    part = 1;
  }
  var pageWindow = pageModeOffset;
  if (isLR) {
    /** @type {number} */
    pageWindow = 1 - pageModeOffset;
  }
  if (2 == pageMode && page < pages - 1 || 1 == pageMode && page + pageWindow < pages) {
    debugLogger("panCanvasEnd normal page region");
    if (1 == pageMode) {
      item = $("#canvas_single_current");
      t = $("#canvas_single_partner_current, #canvas_single_next, #canvas_single_previous");
    } else {
      item = $("#canvas_left_current");
      t = $("#canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous");
    }
  } else {
    if (2 == pageMode && page <= pages && page >= pages - 1 || 1 == pageMode && page + pageWindow == pages) {
      debugLogger("panCanvasEnd boundary region");
      if (1 == pageMode) {
        item = $("#canvas_single_current");
        t = $("#canvas_single_partner_current, #" + endPages[0 + part] + ", #canvas_single_previous");
      } else {
        item = $("#canvas_left_current");
        t = $("#canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous");
        if (isLR) {
          g = $("#" + endPages[0 + part]);
          t = t.add(g);
          if (endPages.length > 1 + part) {
            a = $("#" + endPages[1 + part]);
            t = t.add(a);
          }
        } else {
          a = $("#" + endPages[0 + part]);
          t = t.add(a);
          if (endPages.length > 1 + part) {
            g = $("#" + endPages[1 + part]);
            t = t.add(g);
          }
        }
      }
    } else {
      if (2 == pageMode && page <= pages + endPages.length || 1 == pageMode && page + pageWindow <= pages + endPages.length) {
        debugLogger("panCanvasEnd end page region");
        if (1 == pageMode) {
          if ("blank page" != endPages[page + pageWindow - pages - 1]) {
            item = $("#" + endPages[page + pageWindow - pages - 1]);
            if (page - pageWindow - pages <= endPages.length - 1) {
              c = $("#" + endPages[page - pageWindow - pages]);
              t = t.add(c);
            }
            if (page - pages + 1 <= endPages.length - 1) {
              d = $("#" + endPages[page - pages + 1]);
              t = t.add(d);
            }
            info = 0 <= page - pages - 2 ? "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_single_current") : $("#canvas_single_previous");
            t = t.add(info);
          } else {
            debugLogger("Trying to queue up blank page as refPage");
          }
        } else {
          if (isLR) {
            item = $("#" + endPages[page - pages - 1]);
            if (page - pages <= endPages.length - 1) {
              grid = $("#" + endPages[page - pages]);
              t = t.add(grid);
            }
            if (page - pages + 1 <= endPages.length - 1) {
              g = $("#" + endPages[page - pages + 1]);
              t = t.add(g);
            }
            if (page - pages + 2 <= endPages.length - 1) {
              a = $("#" + endPages[page - pages + 2]);
              t = t.add(a);
            }
            bb = 0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_right_current");
            t = t.add(bb);
            resize = 0 <= page - pages - 3 ? $("#" + endPages[page - pages - 3]) : $("#canvas_left_current");
            t = t.add(resize);
          } else {
            if (0 == (item = $("#" + endPages[page - pages])).length) {
              item = $("#end_page_placeholder");
            }
            grid = $("#" + endPages[page - pages - 1]);
            t = t.add(grid);
            if (page - pages + 2 <= endPages.length - 1) {
              g = $("#" + endPages[page - pages + 2]);
              t = t.add(g);
            } else {
              if (!item.is($("#end_page_placeholder"))) {
                g = $("#end_page_placeholder");
                t = t.add(g);
              }
            }
            debugLogger("leftNext");
            debugLogger(g);
            if (page - pages + 1 <= endPages.length - 1) {
              a = $("#" + endPages[page - pages + 1]);
              t = t.add(a);
            }
            resize = 0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_left_previous");
            t = t.add(resize);
            bb = 0 <= page - pages - 3 ? $("#" + endPages[page - pages - 3]) : $("#canvas_right_previous");
            t = t.add(bb);
          }
        }
      }
    }
  }
  debugLogger("Pan canvas end refpage:");
  debugLogger(item);
  refOffset = item.offset();
  refPosition = item.position();
  debugLogger("Pan canvas end refPosition");
  debugLogger(refPosition);
  if ("left" == side || "right" == side) {
    /** @type {number} */
    delay = 50;
  } else {
    if (2 == pageMode) {
      /** @type {number} */
      delay = 200;
    }
  }
  /** @type {number} */
  var midpoint = .3 * $seekBar.width();
  if (1 != currentZoom) {
    /** @type {number} */
    midpoint = .5 * $seekBar.width();
  }
  var canViewMyFiles = isLR && (0 != page || 1 == pageMode && 1 == pageWindow);
  /** @type {boolean} */
  var canViewSiteFiles = !isLR && 1 == pageMode && page + pageWindow < pages + endPages.length;
  /** @type {boolean} */
  var canUploadFiles = !isLR && 2 == pageMode && page < pages + endPages.length - 1;
  var image = canViewMyFiles || canViewSiteFiles || canUploadFiles;
  /** @type {boolean} */
  var y = !isLR && (0 != page || 1 == pageMode && 1 == pageWindow);
  var x = isLR && 1 == pageMode && page + pageWindow < pages + endPages.length;
  var MIN = isLR && 2 == pageMode && page < pages + endPages.length - 1;
  var min = y || x || MIN;
  if (("left" == side || refPosition.left >= midpoint) && image) {
    $(".reader_page_canvas.top").hammer().off("pan");
    $(".reader_page_canvas.top").hammer().off("pinch");
    item.animate({
      left : $seekBar.width() + 2 * $seekBar.offset().left
    }, delay, function() {
      incrementLeft();
    });
    grid = $("#canvas_right_current");
    (t = t.add(grid)).animate({
      left : "+=" + ($seekBar.width() + 2 * $seekBar.offset().left - refPosition.left)
    }, delay, function() {
    });
  } else {
    if (("right" == side || refPosition.left + item.width() * pageMode < $seekBar.width() - midpoint) && min) {
      $(".reader_page_canvas.top").hammer().off("pan");
      $(".reader_page_canvas.top").hammer().off("pinch");
      item.animate({
        left : -item.width() * pageMode - 2 * $seekBar.offset().left
      }, delay, function() {
        incrementRight();
      });
      if (2 == pageMode && page <= pages) {
        (grid = $("#canvas_right_current")).animate({
          left : -item.width() * pageMode - 2 * $seekBar.offset().left
        }, delay, function() {
        });
      }
      t.animate({
        left : "-=" + (item.width() * pageMode + 2 * $seekBar.offset().left + refPosition.left)
      }, delay, function() {
      });
    } else {
      if (refPosition.left > 0) {
        $(".reader_page_canvas.top").hammer().off("pan");
        $(".reader_page_canvas.top").hammer().off("pinch");
        if (2 == pageMode) {
          if (page <= pages) {
            grid = $("#canvas_right_current");
          } else {
            if (isLR) {
              if (page + 1 < pages + endPages.length) {
                grid = $("#" + endPages[page - pages]);
              }
            } else {
              if (page < pages + endPages.length) {
                grid = $("#" + endPages[page - pages - 1]);
              }
            }
          }
          debugLogger("Adjusting rightCurr: ");
          debugLogger(grid);
          t = t.add(grid);
        }
        item.animate({
          left : "0"
        }, delay, function() {
          setTimeout(function() {
            $(".reader_page_canvas.top").hammer().on("pan", panCanvas);
          }, 50);
          setTimeout(function() {
            $(".reader_page_canvas.top").hammer().on("pinch", pinchZoom);
          }, 50);
          refOffset = $(this).offset();
          refPosition = $(this).position();
        });
        t.animate({
          left : "-=" + refPosition.left
        }, delay, function() {
        });
      } else {
        if (refPosition.left < $seekBar.width() - item.width() * pageMode) {
          $(".reader_page_canvas.top").hammer().off("pan");
          $(".reader_page_canvas.top").hammer().off("pinch");
          if (2 == pageMode) {
            if (page <= pages) {
              grid = $("#canvas_right_current");
            } else {
              if (isLR) {
                if (page + 1 < pages + endPages.length) {
                  grid = $("#" + endPages[page - pages]);
                }
              } else {
                if (page < pages + endPages.length) {
                  grid = $("#" + endPages[page - pages - 1]);
                }
              }
            }
            debugLogger("Adjusting rightCurr: ");
            debugLogger(grid);
            t = t.add(grid);
          }
          item.animate({
            left : $seekBar.width() - item.width() * pageMode
          }, delay, function() {
            setTimeout(function() {
              $(".reader_page_canvas.top").hammer().on("pan", panCanvas);
            }, 50);
            setTimeout(function() {
              $(".reader_page_canvas.top").hammer().on("pinch", pinchZoom);
            }, 50);
            refOffset = $(this).offset();
            refPosition = $(this).position();
          });
          t.animate({
            left : "+=" + Math.abs(refPosition.left - ($seekBar.width() - item.width() * pageMode))
          }, delay, function() {
          });
        }
      }
    }
  }
}
/**
 * @param {!Object} e
 * @return {undefined}
 */
function panCanvas(e) {
  if ("mouse" != e.gesture.pointerType) {
    debugLogger("panCanvas called");
    var dx = e.gesture.deltaX;
    var y = e.gesture.deltaY;
    var n = $("#reader_page_container");
    /** @type {number} */
    var length = 2 * n.offset().left;
    var $t = $();
    var t = ($(), $());
    var result = $();
    var f = $();
    var m = $();
    var p = $();
    var tag = $();
    var c = $();
    var span = $();
    var h = $();
    var info = $();
    /** @type {number} */
    var part = 0;
    if ("blank page" == endPages[0]) {
      /** @type {number} */
      part = 1;
    }
    var pageWindow = pageModeOffset;
    if (isLR) {
      /** @type {number} */
      pageWindow = 1 - pageModeOffset;
    }
    if (2 == pageMode && page < pages - 1 || 1 == pageMode && page + pageWindow < pages) {
      debugLogger("panCanvas normal page region");
      if (1 == pageMode) {
        $t = $("#canvas_single_current");
        f = $("#canvas_single_partner_current");
        m = $("#canvas_single_next");
        p = $("#canvas_single_previous");
        $(".reader_page_canvas.left, .reader_page_canvas.right");
        result = $("#canvas_single_partner_current, #canvas_single_next, #canvas_single_previous");
      } else {
        $t = $("#canvas_left_current");
        span = $("#canvas_right_current");
        tag = $("#canvas_left_next");
        c = $("#canvas_left_previous");
        h = $("#canvas_right_next");
        info = $("#canvas_right_previous");
        $(".reader_page_canvas.single");
        result = $("#canvas_right_current, #canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous");
      }
    } else {
      if (2 == pageMode && page <= pages && page >= pages - 1 || 1 == pageMode && page + pageWindow == pages) {
        debugLogger("panCanvas boundary region");
        if (1 == pageMode) {
          $t = $("#canvas_single_current");
          f = $("#canvas_single_partner_current");
          m = $("#" + endPages[0 + part]);
          if (1 == part) {
            if (isLR) {
              m.css({
                left : $t.position().left + length + $t.width()
              });
            } else {
              m.css({
                left : $t.position().left - length - $t.width()
              });
            }
            $("#canvas_single_next").css({
              left : -5E3
            });
            p = $("#canvas_single_previous");
            $(".reader_page_canvas.left, .reader_page_canvas.right, #canvas_single_partner_current, #canvas_single_next");
            t = m;
            result = $("#canvas_single_partner_current, #canvas_single_next, #" + endPages[0 + part] + ", #canvas_single_previous");
          } else {
            p = $("#canvas_single_previous");
            $(".reader_page_canvas.left, .reader_page_canvas.right");
            t = m;
            result = $("#canvas_single_partner_current, #" + endPages[0 + part] + ", #canvas_single_previous");
          }
        } else {
          $t = $("#canvas_left_current");
          span = $("#canvas_right_current");
          result = $("#canvas_right_current, #canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous");
          if (isLR) {
            debugLogger(tag = $("#" + endPages[0 + part]));
            t = tag;
            result = result.add(tag);
            if (endPages.length > 1 + part) {
              debugLogger(h = $("#" + endPages[1 + part]));
              t = t.add(h);
              result = result.add(h);
            }
          } else {
            h = $("#" + endPages[0 + part]);
            result = result.add(h);
            debugLogger(h);
            if (endPages.length > 1 + part) {
              debugLogger(tag = $("#" + endPages[1 + part]));
              t = t.add(tag);
              result = result.add(tag);
            }
          }
          c = $("#canvas_left_previous");
          info = $("#canvas_right_previous");
          $(".reader_page_canvas.single");
        }
      } else {
        if (2 == pageMode && page <= pages + endPages.length || 1 == pageMode && page + pageWindow <= pages + endPages.length) {
          debugLogger("panCanvas end page region");
          if (1 == pageMode) {
            if ("blank page" != endPages[page + pageWindow - pages - 1]) {
              $t = $("#" + endPages[page + pageWindow - pages - 1]);
              if (page - pageWindow - pages <= endPages.length - 1) {
                f = $("#" + endPages[page - pageWindow - pages]);
                t = t.add(f);
                result = result.add(f);
              }
              if (page - pages + 1 <= endPages.length - 1) {
                m = $("#" + endPages[page - pages + 1]);
                t = t.add(m);
                result = result.add(m);
              }
              p = 0 <= page - pages - 2 ? "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_single_current") : $("#canvas_single_previous");
              t = t.add(p);
              $(".reader_page_canvas.left, .reader_page_canvas.right");
              result = result.add(p);
            } else {
              debugLogger("Trying to queue up blank page as refPage");
            }
            $(".reader_page_canvas.left, .reader_page_canvas.right");
          } else {
            if (isLR) {
              $t = $("#" + endPages[page - pages - 1]);
              if (page - pages <= endPages.length - 1) {
                span = $("#" + endPages[page - pages]);
                t = t.add(span);
                result = result.add(span);
              }
              if (page - pages + 1 <= endPages.length - 1) {
                tag = $("#" + endPages[page - pages + 1]);
                t = t.add(tag);
                result = result.add(tag);
              }
              if (page - pages + 2 <= endPages.length - 1) {
                h = $("#" + endPages[page - pages + 2]);
                t = t.add(h);
                result = result.add(h);
              }
              info = 0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_right_current");
              t = t.add(info);
              result = result.add(info);
              c = 0 <= page - pages - 3 ? $("#" + endPages[page - pages - 3]) : $("#canvas_left_current");
              t = t.add(c);
              result = result.add(c);
            } else {
              if (0 == ($t = $("#" + endPages[page - pages])).length) {
                $t = $("#end_page_placeholder");
              }
              span = $("#" + endPages[page - pages - 1]);
              t = t.add(span);
              result = result.add(span);
              if (page - pages + 2 <= endPages.length - 1) {
                tag = $("#" + endPages[page - pages + 2]);
                t = t.add(tag);
                result = result.add(tag);
              } else {
                if (!$t.is($("#end_page_placeholder"))) {
                  tag = $("#end_page_placeholder");
                  t = t.add(tag);
                  result = result.add(tag);
                }
              }
              if (page - pages + 1 <= endPages.length - 1) {
                h = $("#" + endPages[page - pages + 1]);
                t = t.add(h);
                result = result.add(h);
              }
              c = 0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_left_previous");
              t = t.add(c);
              result = result.add(c);
              info = 0 <= page - pages - 3 ? $("#" + endPages[page - pages - 3]) : $("#canvas_right_previous");
              t = t.add(info);
              result = result.add(info);
            }
            $(".reader_page_canvas.single");
          }
        }
      }
    }
    debugLogger("Pan canvas refpage:");
    debugLogger($t);
    var diff = $t.width();
    var a = $t.height();
    if (0 == gestureCenter.length) {
      gestureCenter = e.gesture.center;
    }
    var width = refPosition.left + dx;
    var x = refPosition.top + y;
    if (0 == page && 1 != pageWindow) {
      if (isLR) {
        if (width > 0) {
          /** @type {number} */
          width = 0;
        }
      } else {
        if (width < n.width() - diff * pageMode) {
          /** @type {number} */
          width = n.width() - diff * pageMode;
        }
      }
    }
    if (x > 0) {
      /** @type {number} */
      x = 0;
    } else {
      if (x < n.height() - a) {
        /** @type {number} */
        x = n.height() - a;
      }
    }
    $t.css({
      left : width,
      top : x
    });
    var offset = $t.width();
    if (1 == pageMode) {
      var end;
      if (isLR) {
        if (0 == pageModeOffset) {
          /** @type {number} */
          end = width - length - offset;
          pos = width + offset + length;
          /** @type {number} */
          left = width - 2 * (length + offset);
        } else {
          end = width + offset + length;
          pos = width + 2 * (length + offset);
          /** @type {number} */
          left = width - length - offset;
        }
      } else {
        if (0 == pageModeOffset) {
          /** @type {number} */
          end = width - length - offset;
          /** @type {number} */
          pos = width - 2 * (length + offset);
          left = width + offset + length;
        } else {
          end = width + offset + length;
          /** @type {number} */
          pos = width - length - offset;
          left = width + 2 * (length + offset);
        }
      }
      if (page == pages && "blank page" == endPages[0]) {
        m.css({
          left : end,
          top : 0
        });
        p.css({
          left : left,
          top : 0
        });
      } else {
        f.css({
          left : end,
          top : 0
        });
        m.css({
          left : pos,
          top : 0
        });
        p.css({
          left : left,
          top : 0
        });
      }
    } else {
      if (isLR) {
        /** @type {number} */
        var left = width - c.width() - info.width() - length;
        var pos = width + 2 * diff + length;
      } else {
        left = width + 2 * diff + length;
        /** @type {number} */
        pos = width - c.width() - info.width() - length;
      }
      span.css({
        left : width + diff,
        top : x
      });
      tag.css({
        left : pos,
        top : 0
      });
      c.css({
        left : left,
        top : 0
      });
      h.css({
        left : pos + tag.width(),
        top : 0
      });
      info.css({
        left : left + c.width(),
        top : 0
      });
    }
  }
}
/**
 * @param {!Object} e
 * @return {undefined}
 */
function pinchZoomStart(e) {
  if (gestureCenter = e.gesture.center, 1 == pageMode) {
    var t = $("#canvas_single_current");
  } else {
    t = $("#canvas_left_current");
  }
  refOffset = t.offset();
  refPosition = t.position();
}
/**
 * @param {!Object} e
 * @return {undefined}
 */
function pinchZoomEnd(e) {
  /** @type {number} */
  var newZoom = e.gesture.scale * currentZoom;
  if (newZoom < 1 && (newZoom = 1), currentZoom = newZoom, 1 == pageMode) {
    var a = $("#canvas_single_current");
  } else {
    a = $("#canvas_left_current");
  }
  refOffset = a.offset();
  refPosition = a.position();
  $(".reader_page_canvas.top").hammer().off("pan");
  setTimeout(function() {
    $(".reader_page_canvas.top").hammer().on("pan", panCanvas);
  }, 50);
}
/**
 * @return {undefined}
 */
function pinchZoomMove() {
}
/**
 * @param {!Object} event
 * @return {undefined}
 */
function pinchZoom(event) {
  if ("mouse" != event.gesture.pointerType) {
    var t = $("#reader_page_container");
    var srcHeight = t.height();
    /** @type {number} */
    var width = t.width() / pageMode;
    if (1 == pageMode) {
      var r = $("#canvas_single_current");
    } else {
      r = $("#canvas_left_current");
    }
    if (0 == gestureCenter.length) {
      gestureCenter = event.gesture.center;
    }
    var pageX = gestureCenter.x;
    var pageY = gestureCenter.y;
    var k = event.gesture.scale;
    /** @type {number} */
    var ratio = k * currentZoom;
    /** @type {number} */
    var left = pageX - t.offset().left - k * (pageX - t.offset().left - refPosition.left);
    /** @type {number} */
    var top = pageY - t.offset().top - k * (pageY - t.offset().top - refPosition.top);
    debugLogger((left = left + (event.gesture.center.x - gestureCenter.x)) + ", " + (top = top + (event.gesture.center.y - gestureCenter.y)));
    if (ratio < 1) {
      /** @type {number} */
      left = 0;
      /** @type {number} */
      top = 0;
      /** @type {number} */
      ratio = 1;
    }
    if (left > 0) {
      /** @type {number} */
      left = 0;
    } else {
      if (left < t.width() - r.width() * pageMode) {
        /** @type {number} */
        left = t.width() - r.width() * pageMode;
      }
    }
    if (top > 0) {
      /** @type {number} */
      top = 0;
    } else {
      if (top < t.height() - r.height()) {
        /** @type {number} */
        top = t.height() - r.height();
      }
    }
    r.css({
      left : left,
      top : top,
      width : width * ratio,
      height : srcHeight * ratio
    });
    if (2 == pageMode) {
      $("#canvas_right_current").css({
        left : left + width * ratio,
        top : top,
        width : width * ratio,
        height : srcHeight * ratio
      });
    }
  }
}
/**
 * @return {undefined}
 */
function showMobileMenus() {
  if (true === $.browser.mobile) {
    clearTimeout(menuTimeout);
    var t = $("#reader_top_container");
    var artbox = $("#reader_bottom_container");
    t.removeClass("m_closed").css({
      top : "-" + t.height() + "px"
    }).animate({
      top : "+=" + t.height()
    }, 125);
    artbox.removeClass("m_closed").css({
      bottom : "-" + artbox.height() + "px"
    }).animate({
      bottom : "+=" + artbox.height()
    }, 125, function() {
      /** @type {number} */
      menuTimeout = setTimeout(hideMobileMenus, hideMenuAfter);
    });
  }
}
/**
 * @return {undefined}
 */
function hideMobileMenus() {
  if (true === $.browser.mobile) {
    clearTimeout(menuTimeout);
    /** @type {number} */
    menuTimeout = 0;
    var e = $("#reader_top_container");
    var $container = $("#reader_bottom_container");
    e.animate({
      top : "-=" + e.height()
    }, 125);
    $container.animate({
      bottom : "-=" + $container.height()
    }, 125, function() {
      e.addClass("m_closed");
      $container.addClass("m_closed");
    });
  }
}
/**
 * @return {undefined}
 */
function orientationChanged() {
  if (setPageMode(false), setupStyles(), setupPageLabels(), setBookmarkIcon(), updateDisplayedPages(), updateOffscreenPages(), updateEndPages(), embedded) {
    $("#reader_wrapper");
    var $header = $("#site-header");
    debugLogger($header.height());
    if ($(window).scrollTop() < $header.height()) {
      window.scrollTo(0, $("#site-header").height());
    }
  } else {
    window.scrollTo(0, 0);
  }
}
/**
 * @return {undefined}
 */
function setupPageLabelsMobile() {
  if (0 == window.orientation) {
    var formattedChosenQuestion = (page + pageModeOffset).toString();
    if (isLR) {
      formattedChosenQuestion = (page + -1 * pageModeOffset + 1).toString();
    }
    if (0 == page) {
      /** @type {string} */
      formattedChosenQuestion = "1";
    }
    $(".page_slider_label.left.mobile, .page_slider_label.right.mobile").hide();
    $(".page_slider_label.center.mobile .page_slider_label_pagenum").html(formattedChosenQuestion);
    $(".page_slider_label.center.mobile .page_slider_label_after").html(" OF " + pageStr);
    $(".page_slider_label.center.mobile").show();
  } else {
    var formattedChosenQuestion = page.toString();
    var $selectorListPanel = (page + 1).toString();
    $(".page_slider_label.center.mobile").hide();
    $(".page_slider_label.left.mobile").css("left", $("#reader_page_container").css("margin-left"));
    $(".page_slider_label.right.mobile").css("right", $("#reader_page_container").css("margin-right"));
    $(".page_slider_label.left.mobile, .page_slider_label.right.mobile").width($("#reader_page_container").width() / 2);
    if (isLR) {
      $(".page_slider_label.left.mobile .page_slider_label_pagenum").html(formattedChosenQuestion);
      $(".page_slider_label.right.mobile .page_slider_label_pagenum").html($selectorListPanel);
      if (0 == page) {
        $(".page_slider_label.left.mobile").hide();
      } else {
        $(".page_slider_label.left.mobile").show();
      }
      $(".page_slider_label.right.mobile").show();
    } else {
      $(".page_slider_label.right.mobile .page_slider_label_pagenum").html(formattedChosenQuestion);
      $(".page_slider_label.left.mobile .page_slider_label_pagenum").html($selectorListPanel);
      if (0 == page) {
        $(".page_slider_label.right.mobile").hide();
      } else {
        $(".page_slider_label.right.mobile").show();
      }
      $(".page_slider_label.left.mobile").show();
    }
  }
}
/**
 * @return {undefined}
 */
function setBookmark() {
  var transformer;
  var step;
  if (debugLogger("setBookmark called"), transformer = bookmarkPage == page, bookmarkPage = transformer ? -1 : page, page > pages && !transformer) {
    debugLogger("BLOCKED bookmark of an end_page.");
  } else {
    (step = $.ajax({
      type : "POST",
      url : "/reader/set_bookmark/" + getMangaId(),
      dataType : "json",
      data : {
        pagenum : bookmarkPage
      },
      dataType : "json"
    })).done(function() {
      toggleBookmarkBtn(!transformer);
      setBookmarkIcon(!transformer);
    });
    step.fail(function(xhr, canCreateDiscussions) {
      if (401 == xhr.status) {
        logout();
      } else {
        if ("parsererror" != canCreateDiscussions) {
          showErr("Set Bookmark error (" + canCreateDiscussions + ")", xhr.responseText);
        }
      }
    });
  }
}
/**
 * @param {boolean} isIron
 * @return {undefined}
 */
function toggleBookmarkBtn(isIron) {
  var currentArrowButton;
  var tmpNxtButton;
  if (true === $.browser.mobile) {
    currentArrowButton = $("#reader_bookmark_add_mobile");
    tmpNxtButton = $("#reader_bookmark_remove_mobile");
  } else {
    currentArrowButton = $(".reader-bookmark.add-bookmark");
    tmpNxtButton = $(".reader-bookmark.remove-bookmark");
  }
  if (isIron) {
    currentArrowButton.addClass("disp-n");
    tmpNxtButton.removeClass("disp-n");
  } else {
    tmpNxtButton.addClass("disp-n");
    currentArrowButton.removeClass("disp-n");
  }
}
/**
 * @param {boolean} zoomAware
 * @return {undefined}
 */
function setBookmarkIcon(zoomAware) {
  var div;
  var docPath;
  var isfMainLine;
  var divSize;
  var closeButtonEl = $("#page_slider");
  div = true === $.browser.mobile ? $("#bookmark_icon_mobile") : $("#bookmark_icon");
  if (false !== zoomAware && -1 != bookmarkPage) {
    /** @type {number} */
    isfMainLine = ((docPath = pages + endPages.length) - 1 - bookmarkPage) * (closeButtonEl.width() / (docPath - 1));
    /** @type {number} */
    divSize = parseInt(closeButtonEl.css("margin-left").replace(/[^-\d\.]/g, "")) + isfMainLine - div.width() / 2;
    div.css("left", divSize + "px");
    if (true === zoomAware) {
      div.removeClass("disp-n");
    }
  } else {
    div.addClass("disp-n");
  }
}
/**
 * @return {undefined}
 */
function bookmarkIconClicked() {
  page = bookmarkPage % 2 == 0 ? bookmarkPage : bookmarkPage - 1;
  loadPages();
}
/**
 * @return {undefined}
 */
function setupPageLabels() {
  if (true === $.browser.mobile) {
    setupPageLabelsMobile();
  } else {
    setupPageLabelsDesktop();
  }
}
/**
 * @param {!Function} localUserprefs
 * @return {undefined}
 */
function togglePageMode(localUserprefs) {
  if (1 == pageMode) {
    /** @type {number} */
    pageMode = 2;
    /** @type {(Element|null)} */
    var canvas = document.getElementById("canvas_left_current");
    /** @type {(Element|null)} */
    var aCanvas = document.getElementById("canvas_right_current");
    var ctx = canvas.getContext("2d");
    var context = aCanvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    context.clearRect(0, 0, aCanvas.width, aCanvas.height);
    $(".reader_page_canvas.left, .reader_page_canvas.right").show();
    $(".reader_page_canvas.single").hide();
  } else {
    /** @type {number} */
    pageMode = 1;
    /** @type {number} */
    pageModeOffset = isLR ? 1 : 0;
    (ctx = (canvas = document.getElementById("canvas_single_current")).getContext("2d")).clearRect(0, 0, canvas.width, canvas.height);
    $(".reader_page_canvas.left, .reader_page_canvas.right").hide();
    $(".reader_page_canvas.single").show();
  }
  if (!localUserprefs) {
    setupPageLabels();
    updateDisplayedPages();
    updateOffscreenPages();
  }
}
/**
 * @return {?}
 */
function checkPageBounds() {
  if (page > pages + endPages.length) {
    if ((page = pages + endPages.length) % 2 == 1) {
      /** @type {number} */
      page = page - 1;
    }
  } else {
    if (page < 0) {
      if (isLR && 1 == pageMode && -2 == page) {
        return page = 0, pageModeOffset = 1, void loadPages();
      }
      /** @type {number} */
      page = 0;
    } else {
      clearInterval(loaderInterval);
      /** @type {boolean} */
      loaderInterval = false;
      loadPages();
    }
  }
}
/**
 * @return {?}
 */
function incrementLeft() {
  if ($(".reader_pager").stop(true, true).hide(), pagerTime = 0, clearInterval(pagerInterval), pagerInterval = 0, 1 == pageMode) {
    if (0 == pageModeOffset) {
      if (isLR || page != pages || "blank page" != endPages[0]) {
        return pageModeOffset = 1, void loadPages();
      }
    } else {
      if (!(isLR && page == pages + 2 && "blank page" == endPages[0])) {
        /** @type {number} */
        pageModeOffset = 0;
      }
    }
  }
  if (isLR) {
    /** @type {number} */
    page = page - 2;
  } else {
    page = page + 2;
  }
  checkPageBounds("left");
}
/**
 * @return {?}
 */
function incrementRight() {
  if (debugLogger("incrementRight called, page = " + page), $(".reader_pager").stop(true, true).hide(), pagerTime = 0, clearInterval(pagerInterval), pagerInterval = 0, 1 == pageMode) {
    if (1 == pageModeOffset) {
      if (!isLR || page != pages || "blank page" != endPages[0]) {
        return pageModeOffset = 0, void loadPages();
      }
    } else {
      if (isLR || page != pages + 2 || "blank page" != endPages[0]) {
        /** @type {number} */
        pageModeOffset = 1;
      }
    }
  }
  if (isLR) {
    page = page + 2;
  } else {
    /** @type {number} */
    page = page - 2;
  }
  checkPageBounds("right");
  debugLogger("incrementRight done, page = " + page);
}
/**
 * @param {!Object} evt
 * @return {undefined}
 */
function pagerClick(evt) {
  var x;
  var width;
  var $seekBar = $("#reader_page_container");
  /** @type {number} */
  var duration = 100;
  var c = $();
  /** @type {number} */
  var padding = 2 * $seekBar.offset().left;
  var p = $();
  var m = $();
  var items = $();
  var s = $();
  var l = $();
  var n = $();
  var e = $();
  var f = $();
  var butel = $();
  var i = $();
  var r = $();
  /** @type {number} */
  var part = 0;
  if ("blank page" == endPages[0]) {
    /** @type {number} */
    part = 1;
  }
  var pageWindow = pageModeOffset;
  if (isLR && (pageWindow = 1 - pageModeOffset), 1 != currentZoom && $(document).trigger("forceZoom"), 2 == pageMode && page < pages - 1 || 1 == pageMode && page + pageWindow < pages ? (debugLogger("Normal content region"), 1 == pageMode ? (c = $("#canvas_single_current"), p = $("#canvas_single_partner_current"), items = $("#canvas_single_previous"), m = $("#canvas_single_next"), butel = $(".reader_page_canvas.left, .reader_page_canvas.right"), r = $("#canvas_single_partner_current, #canvas_single_previous, #canvas_single_next")) :
  (c = $("#canvas_left_current"), s = $("#canvas_left_next"), e = $("#canvas_right_next"), l = $("#canvas_left_previous"), f = $("#canvas_right_previous"), butel = $(".reader_page_canvas.single"), r = $("#canvas_right_current, #canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous"))) : 2 == pageMode && page <= pages && page >= pages - 1 || 1 == pageMode && page + pageWindow == pages ? (debugLogger("Nearing boundary"), 1 == pageMode ? (c = $("#canvas_single_current"),
  p = $("#canvas_single_partner_current"), debugLogger(m = $("#" + endPages[0 + part])), 1 == part ? (isLR ? m.css({
    left : c.position().left + padding + c.width()
  }) : m.css({
    left : c.position().left - padding - c.width()
  }), $("#canvas_single_next").css({
    left : -5E3
  }), items = $("#canvas_single_previous"), butel = $(".reader_page_canvas.left, .reader_page_canvas.right, #canvas_single_partner_current, #canvas_single_next"), i = m, r = $("#canvas_single_partner_current, #canvas_single_next, #" + endPages[0 + part] + ", #canvas_single_previous")) : (items = $("#canvas_single_previous"), butel = $(".reader_page_canvas.left, .reader_page_canvas.right"), i = m, r = $("#canvas_single_partner_current, #" + endPages[0 + part] + ", #canvas_single_previous"))) : (c =
  $("#canvas_left_current"), r = $("#canvas_right_current, #canvas_left_next, #canvas_right_next, #canvas_left_previous, #canvas_right_previous"), isLR ? (debugLogger(s = $("#" + endPages[0 + part])), i = s, r = r.add(s), endPages.length > 1 + part && (debugLogger(e = $("#" + endPages[1 + part])), i = i.add(e), r = r.add(e))) : (e = $("#" + endPages[0 + part]), r = r.add(e), debugLogger(e), endPages.length > 1 + part && (debugLogger(s = $("#" + endPages[1 + part])), i = i.add(s), r = r.add(s))),
  l = $("#canvas_left_previous"), f = $("#canvas_right_previous"), butel = $(".reader_page_canvas.single"))) : (2 == pageMode && page <= pages + endPages.length || 1 == pageMode && page + pageWindow <= pages + endPages.length) && (debugLogger("End page region"), 1 == pageMode ? ("blank page" != endPages[page + pageWindow - pages - 1] ? (c = $("#" + endPages[page + pageWindow - pages - 1]), page - pageWindow - pages <= endPages.length - 1 && (p = $("#" + endPages[page - pageWindow - pages]), i = i.add(p),
  r = r.add(p)), page - pages + 1 <= endPages.length - 1 && (m = $("#" + endPages[page - pages + 1]), i = i.add(m), r = r.add(m)), items = 0 <= page - pages - 2 ? "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_single_current") : $("#canvas_single_previous"), i = i.add(items), butel = $(".reader_page_canvas.left, .reader_page_canvas.right"), r = r.add(items)) : debugLogger("Trying to queue up blank page as refPage"), butel = $(".reader_page_canvas.left, .reader_page_canvas.right")) :
  (isLR ? (c = $("#" + endPages[page - pages - 1]), page - pages <= endPages.length - 1 && (n = $("#" + endPages[page - pages]), i = i.add(n), r = r.add(n)), page - pages + 1 <= endPages.length - 1 && (s = $("#" + endPages[page - pages + 1]), i = i.add(s), r = r.add(s)), page - pages + 2 <= endPages.length - 1 && (e = $("#" + endPages[page - pages + 2]), i = i.add(e), r = r.add(e)), f = 0 <= page - pages - 1 ? "blank page" == endPages[page - pages - 2] ? $("#canvas_right_current") : $("#" + endPages[page -
  pages - 2]) : $("#canvas_right_previous"), i = i.add(f), r = r.add(f), l = 0 < page - pages - 2 ? $("#" + endPages[page - pages - 3]) : $("#canvas_left_current"), i = i.add(l), r = r.add(l)) : (c = $("#" + endPages[page - pages]), n = $("#" + endPages[page - pages - 1]), 0 == c.length && (c = $("#end_page_placeholder")).css({
    left : 0
  }), i = i.add(n), r = r.add(n), page - pages + 2 <= endPages.length - 1 && (s = $("#" + endPages[page - pages + 2]), i = i.add(s), r = r.add(s)), page - pages + 1 <= endPages.length - 1 && (e = $("#" + endPages[page - pages + 1]), i = i.add(e), r = r.add(e)), l = 0 <= page - pages - 2 && "blank page" != endPages[page - pages - 2] ? $("#" + endPages[page - pages - 2]) : $("#canvas_left_current"), i = i.add(l), r = r.add(l), f = 0 <= page - pages - 3 ? $("#" + endPages[page - pages - 3]) : $("#canvas_right_current"),
  i = i.add(f), r = r.add(f)), butel = $(".reader_page_canvas.single"))), x = c.position().left, width = c.width(), 1 == pageMode) {
    var xOffset;
    if (isLR) {
      if (0 == pageModeOffset) {
        /** @type {number} */
        xOffset = x - padding - width;
        y = x + width + padding;
        /** @type {number} */
        left = x - 2 * (padding + width);
      } else {
        xOffset = x + width + padding;
        y = x + 2 * (padding + width);
        /** @type {number} */
        left = x - padding - width;
      }
    } else {
      if (0 == pageModeOffset) {
        /** @type {number} */
        xOffset = x - padding - width;
        /** @type {number} */
        y = x - 2 * (padding + width);
        left = x + width + padding;
      } else {
        xOffset = x + width + padding;
        /** @type {number} */
        y = x - padding - width;
        left = x + 2 * (padding + width);
      }
    }
    if (page == pages && "blank page" == endPages[0]) {
      m.css({
        left : xOffset,
        top : 0
      });
      items.css({
        left : left,
        top : 0
      });
    } else {
      p.css({
        left : xOffset,
        top : 0
      });
      m.css({
        left : y,
        top : 0
      });
      items.css({
        left : left,
        top : 0
      });
    }
  } else {
    if (isLR) {
      /** @type {number} */
      var left = x - 2 * width - padding;
      var y = x + 2 * width + padding;
    } else {
      left = x + 2 * width + padding;
      /** @type {number} */
      y = x - 2 * width - padding;
    }
    s.css({
      left : y,
      top : 0
    });
    l.css({
      left : left,
      top : 0
    });
    e.css({
      left : y + width,
      top : 0
    });
    f.css({
      left : left + width,
      top : 0
    });
    debugLogger("leftNext: " + y + ", rightNext: " + (y + width) + ", pageWidth: " + width);
  }
  /** @type {number} */
  var lastPage = pages + endPages.length - pageMode + 1;
  pages;
  if ("left" == evt.data.dir && (isLR && (0 != page || 1 == pageMode && 0 == pageModeOffset) || !isLR && page + pageMode % 2 * pageModeOffset < lastPage)) {
    $(".reader_page_canvas").show();
    debugLogger("Doing left click animation");
    c.animate({
      left : $seekBar.width() + padding
    }, duration, function() {
      incrementLeft();
    });
    butel.hide();
    i.show();
    r.animate({
      left : "+=" + ($seekBar.width() + padding - x)
    }, duration, function() {
    });
  } else {
    if ("right" == evt.data.dir && (isLR && page + pageMode % 2 * pageWindow < lastPage || !isLR && (0 != page || 1 == pageMode && 1 == pageModeOffset))) {
      $(".reader_page_canvas").show();
      debugLogger("Doing right click animation");
      c.animate({
        left : -$seekBar.width() - padding
      }, duration, function() {
        incrementRight();
      });
      butel.hide();
      i.show();
      debugLogger("Animating: -=" + ($seekBar.width() + padding + x));
      debugLogger(r);
      r.animate({
        left : "-=" + ($seekBar.width() + padding + x)
      }, duration, function() {
      });
    }
  }
}
/**
 * @param {number} i
 * @return {?}
 */
function getRealPageFromSlider(i) {
  return isLR ? i : pages - i;
}
/**
 * @param {number} data
 * @return {undefined}
 */
function preloadImages(data) {
  /** @type {!Array} */
  var conf_shortcuts_icon = [];
  /** @type {!Array} */
  var ajaxArr = [];
  /** @type {!Array} */
  var differedList = [];
  /** @type {number} */
  i = 0;
  for (; i <= pages; i++) {
    if (!(i < page - 4 || i > page + 5)) {
      if ("undefined" == typeof pageImages["page" + i]) {
        (function(i, a, elem) {
          if (i == page || i == page + 1) {
            ajaxArr.push(elem);
          } else {
            if (Math.abs(page - i) <= 2) {
              differedList.push(elem);
            }
          }
          /** @type {!XMLHttpRequest} */
          var r = new XMLHttpRequest;
          if (r.onloadend = function(i, context) {
            return function() {
              /** @type {!Image} */
              var img = new Image;
              /** @type {string} */
              img.crossOrigin = "Anonymous";
              img.onload = function(i, elem) {
                return function() {
                  /** @type {!Image} */
                  pageImages["page" + i] = img;
                  $("body").append('<img class="readerImgPage imgPage' + i + '" src="' + this.src + '" crossOrigin="Anonymous">');
                  $(".imgPage" + i).hide();
                  elem.resolve();
                };
              }(i, context);
              var data = EXIF.readFromBinaryFile(this.response);
              /** @type {string} */
              var r = "";
              var targetWidth = metadata.width;
              var value = metadata.height;
              if (data.ImageUniqueID) {
                r = data.ImageUniqueID;
                targetWidth = data.ImageWidth;
                value = data.ImageHeight;
              }
              /** @type {!DataView} */
              var dataview = new DataView(this.response);
              /** @type {!Blob} */
              var blob = new Blob([dataview], {
                type : "image/jpeg"
              });
              pageKeys["page" + i] = {
                key : r,
                width : targetWidth,
                height : value,
                size : blob.size
              };
              var url = (window.URL || window.webkitURL).createObjectURL(blob);
              img.src = url;
            };
          }(i, elem), r.onerror = function() {
            debugLogger("There was an XHR error!");
          }, debugLogger("preloadImages pageNum: " + i.toString() + ", url: " + typeof a), "string" != typeof a) {
            throw "url is NOT a string!";
          }
          r.open("GET", a, true);
          /** @type {string} */
          r.responseType = "arraybuffer";
          r.send();
        })(i, pageList["page" + i], conf_shortcuts_icon[i] = $.Deferred());
      }
    }
  }
  $.when.apply($, ajaxArr).done(function() {
    if (1 == data) {
      setTimeout(function() {
        updateDisplayedPages();
      }, 10);
      updateDisplayedPages();
    } else {
      clearInterval(loaderInterval);
      /** @type {boolean} */
      loaderInterval = false;
    }
  });
  $.when.apply($, differedList).done(function() {
    updateOffscreenPages();
  });
}
/**
 * @return {undefined}
 */
function loadPages() {
  debugLogger("loadPages called, page = " + page);
  /** @type {boolean} */
  leftPageLoaded = false;
  /** @type {boolean} */
  rightPageLoaded = false;
  /** @type {(Element|null)} */
  var dateSlider = document.getElementById("page_slider");
  /** @type {!Array} */
  var reqs = [];
  /** @type {number} */
  i = page - 4;
  for (; i <= page + 5; i++) {
    if (i <= pages && i >= 0 && "undefined" == typeof pageImages["page" + i]) {
      if (i == page) {
        $("#reader_loading_container").delay(150).fadeIn(150);
      }
      var modDlReq = $.ajax({
        dataType : "text",
        url : pageUrl + "&manga_id=" + manga_id + "&page=" + i
      });
      reqs.push(modDlReq);
    }
  }
  $.when.apply($, reqs).done(function() {
    /** @type {number} */
    i = 0;
    for (; i < reqs.length; i++) {
      var group_rule;
      /** @type {(Array<string>|null)} */
      var a_group_rules = /\/([0-9]+)\.jpg/.exec(reqs[i].responseText);
      if (a_group_rules && a_group_rules.length > 0) {
        /** @type {string} */
        group_rule = a_group_rules[1];
        pageList["page" + group_rule] = reqs[i].responseText;
      }
    }
    dateSlider.noUiSlider.set(page);
    setupPageLabels();
    /** @type {number} */
    var range_to = pages - page - pageModeOffset;
    if (range_to < 0) {
      /** @type {number} */
      range_to = 0;
    }
    if (range_to > pages) {
      range_to = pages;
    }
    $("#pages_left").html(range_to + " LEFT");
    /** @type {!Array} */
    var validPositions = ["left", "right", "single"];
    if (page < pages) {
      /** @type {number} */
      i = 0;
      for (; i < validPositions.length; i++) {
        /** @type {(Element|null)} */
        var frontCanvas = document.getElementById("canvas_" + validPositions[i] + "_current");
        frontCanvas.getContext("2d").clearRect(0, 0, frontCanvas.width, frontCanvas.height);
        document.getElementById("canvas_" + validPositions[i] + "_next").getContext("2d");
        document.getElementById("canvas_" + validPositions[i] + "_previous").getContext("2d");
      }
    } else {
      /** @type {(Element|null)} */
      var frontCanvas = document.getElementById("canvas_single_partner_current");
      frontCanvas.getContext("2d").clearRect(0, 0, frontCanvas.width, frontCanvas.height);
      if (1 == pageMode) {
        $("#canvas_single_partner_current").css({
          left : -3E3
        });
      }
    }
    preloadImages(true);
    if (bookmarkPage == page) {
      toggleBookmarkBtn(true);
    } else {
      toggleBookmarkBtn(false);
    }
    updateEndPages();
    updateLinkAreas();
    var _en = page + pageModeOffset;
    if (!quartileFirst && _en >= Math.floor(.25 * pages)) {
      Tracking.sendEvent({
        category : "Manga Reader",
        action : "First Quartile",
        label : getGAEventLabel()
      });
      /** @type {boolean} */
      quartileFirst = true;
    }
    if (!quartileSecond && _en >= Math.floor(.5 * pages)) {
      Tracking.sendEvent({
        category : "Manga Reader",
        action : "Second Quartile",
        label : getGAEventLabel()
      });
      /** @type {boolean} */
      quartileSecond = true;
    }
    if (!quartileThird && _en >= Math.floor(.75 * pages)) {
      Tracking.sendEvent({
        category : "Manga Reader",
        action : "Third Quartile",
        label : getGAEventLabel()
      });
      /** @type {boolean} */
      quartileThird = true;
    }
    if (!readerComplete && _en >= pages - 1) {
      Tracking.sendEvent({
        category : "Manga Reader",
        action : "Read Complete",
        label : getGAEventLabel()
      });
      /** @type {boolean} */
      readerComplete = true;
    }
  });
}
/**
 * @return {undefined}
 */
function openChapterAd() {
}
/**
 * @return {undefined}
 */
function updateEndPages() {
  debugLogger("update end pages");
  $("#reader_page_container").offset().left;
  var _ileft;
  var increment;
  /** @type {number} */
  var name = 0;
  if ("blank page" == endPages[0] && (name = 1), _ileft = $("#end_page_end_card").width(), increment = pageModeOffset, isLR && (increment = 1 - pageModeOffset), true !== $.browser.mobile && ($("#reader_tools .reader-zoom.zoom-in").off("click"), $("#reader_tools .reader-zoom.zoom-out").off("click")), page > pages + name) {
    if (1 == pageMode) {
      /** @type {number} */
      i = 0;
      for (; i < endPages.length; i++) {
        if (i == page + increment - pages - 1) {
          $("#" + endPages[i]).css({
            left : 0
          });
        } else {
          $("#" + endPages[i]).css({
            left : -3E3
          });
        }
      }
    } else {
      if (isLR) {
        /** @type {number} */
        i = 0;
        for (; i < endPages.length; i++) {
          if (i == page - pages - 1) {
            $("#" + endPages[i]).css({
              left : 0
            });
          } else {
            if (i == page - pages) {
              $("#" + endPages[i]).css({
                left : _ileft
              });
            } else {
              $("#" + endPages[i]).css({
                left : -3E3
              });
            }
          }
        }
      } else {
        /** @type {number} */
        i = 0;
        for (; i < endPages.length; i++) {
          if (i == page - pages - 1) {
            $("#" + endPages[i]).css({
              left : _ileft
            });
          } else {
            if (i == page - pages) {
              $("#" + endPages[i]).css({
                left : 0
              });
            } else {
              $("#" + endPages[i]).css({
                left : -3E3
              });
            }
          }
        }
      }
    }
    if (true === $.browser.mobile) {
      $(".reader_page_canvas.top").hammer().off("doubletap").off("singletap");
      $(".reader_page_canvas.top").on("singletap", handleEndPageTap);
      if (0 == window.orientation) {
        $("#end_page_end_card .o_end-chapter-list").removeClass("type-tiny").addClass("type-rg type-sm--sm type-md--lg");
        $("#end_page_end_card .o_manga-buy-now").removeClass("type-tiny").addClass("type-rg type-sm--sm type-md--lg");
        $("#end_page_end_card .o_chapter-container").removeClass("type-tiny").addClass("type-rg type-md--lg");
        $("#end_page_end_card .o_chap-dm-links p").removeClass("type-tiny").addClass("type-rg type-md--md");
        $("#end_page_discovery .section_title").removeClass("type-sm").addClass("type-rg");
        $("#end_page_discovery .o_sort_container .o_sortable div.type-center").removeClass("type-bs").addClass("type-sm");
        $("#end_page_discovery .o_sort_container .o_sortable a.o_inner-link").removeClass("type-tiny").addClass("type-bs");
      } else {
        $("#end_page_end_card .o_end-chapter-list").removeClass("type-rg type-sm--sm type-md--lg").addClass("type-tiny");
        $("#end_page_end_card .o_manga-buy-now").removeClass("type-rg type-sm--sm type-md--lg").addClass("type-tiny");
        $("#end_page_end_card .o_chapter-container").removeClass("type-sm--sm").addClass("type-tiny");
        $("#end_page_end_card .o_chap-dm-links p").removeClass("type-sm--sm pad-y-sm--sm").addClass("type-tiny");
        $("#end_page_discovery .section_title").removeClass("type-rg").addClass("type-sm");
        $("#end_page_discovery .o_sort_container .o_sortable div.type-center").removeClass("type-sm").addClass("type-bs");
        $("#end_page_discovery .o_sort_container .o_sortable a.o_inner-link").removeClass("type-bs").addClass("type-tiny");
      }
    } else {
      $(".reader_page_canvas.top").hide();
    }
    if (page >= pages + 2) {
      $(".reader_page_canvas.previous").css({
        left : -3E3
      });
    }
  } else {
    $(".reader_page_end").not(".placeholder").css({
      left : -3E3
    });
    if (page >= pages - 1) {
      $(".reader_page_canvas.next").css({
        left : -3E3
      });
    }
    if (true === $.browser.mobile) {
      $(".reader_page_canvas.top").hammer().off("doubletap").off("singletap");
      $(".reader_page_canvas.top").hammer().on("doubletap", doubletapZoom).on("singletap", handleTap);
    } else {
      $("#reader_tools .reader-zoom.zoom-in").on("click", {
        dir : "in"
      }, zoom);
      $("#reader_tools .reader-zoom.zoom-out").on("click", {
        dir : "out"
      }, zoom);
      $(".reader_page_canvas.top").show();
    }
  }
  debugLogger("update end pages done");
}
/**
 * @return {undefined}
 */
function updateDisplayedPages() {
  var value;
  var data;
  debugLogger("update display pages");
  /** @type {!Array} */
  var reqs = [];
  i = page;
  for (; i < page + 2; i++) {
    if (i <= pages) {
      if ("undefined" == typeof pageImages["page" + i]) {
        var modDlReq = $.ajax({
          dataType : "text",
          url : pageUrl + "&manga_id=" + manga_id + "&page=" + i
        });
        reqs.push(modDlReq);
      } else {
        if (i == page) {
          value = {
            pageNum : i,
            src : pageImages["page" + i].src
          };
        } else {
          data = {
            pageNum : i,
            src : pageImages["page" + i].src
          };
        }
      }
    }
  }
  if (reqs.length > 0) {
    $("#reader_loading_container").delay(150).fadeIn(150);
    $.when.apply($, reqs).done(function() {
      /** @type {number} */
      i = 0;
      for (; i < reqs.length; i++) {
        var pageNum;
        /** @type {(Array<string>|null)} */
        var enmlHash = /\/([0-9]+)\.jpg/.exec(reqs[i].responseText);
        if (enmlHash && enmlHash.length > 0) {
          if ((pageNum = parseInt(enmlHash[1])) == page) {
            value = {
              pageNum : pageNum,
              src : reqs[i].responseText
            };
          } else {
            data = {
              pageNum : pageNum,
              src : reqs[i].responseText
            };
          }
        }
      }
      if (isLR) {
        setImages(value, data, "current");
      } else {
        setImages(data, value, "current");
      }
    });
  } else {
    if (isLR) {
      setImages(value, data, "current");
    } else {
      setImages(data, value, "current");
    }
  }
  debugLogger("pageL:");
  debugLogger(data);
  debugLogger("pageR:");
  debugLogger(value);
  /** @type {number} */
  currentZoom = 1;
  debugLogger("update display pages done");
}
/**
 * @return {undefined}
 */
function updateOffscreenPages() {
  var expected;
  var data;
  var value;
  var options;
  debugLogger("update offscreen pages");
  /** @type {!Array} */
  var reqs = [];
  /** @type {!Array} */
  var args = [];
  /** @type {number} */
  i = page - 2;
  for (; i < page; i++) {
    if (i <= pages && i >= 0) {
      if (debugLogger("Previous page " + i + "- type: " + typeof pageImages["page" + i]), "undefined" == typeof pageImages["page" + i]) {
        var a = $.ajax({
          dataType : "text",
          url : pageUrl + "&manga_id=" + manga_id + "&page=" + i
        });
        reqs.push(a);
      } else {
        if (i == page - 2) {
          debugLogger("Setting RP from cache");
          value = {
            pageNum : i,
            src : pageImages["page" + i].src
          };
        } else {
          debugLogger("Setting LP from cache");
          options = {
            pageNum : i,
            src : pageImages["page" + i].src
          };
        }
      }
    }
  }
  i = page + 2;
  for (; i < page + 4; i++) {
    if (i <= pages && i >= 0) {
      if (debugLogger("Next page " + i + "- type: " + typeof pageImages["page" + i]), "undefined" == typeof pageImages["page" + i]) {
        a = $.ajax({
          dataType : "text",
          url : pageUrl + "&manga_id=" + manga_id + "&page=" + i
        });
        args.push(a);
      } else {
        if (i == page + 2) {
          debugLogger("Setting RN from cache");
          expected = {
            pageNum : i,
            src : pageImages["page" + i].src
          };
        } else {
          debugLogger("Setting LN from cache");
          data = {
            pageNum : i,
            src : pageImages["page" + i].src
          };
        }
      }
    }
  }
  if (reqs.length > 0 ? $.when.apply($, reqs).done(function() {
    /** @type {number} */
    i = 0;
    for (; i < reqs.length; i++) {
      var pageNum;
      /** @type {(Array<string>|null)} */
      var enmlHash = /\/([0-9]+)\.jpg/.exec(reqs[i].responseText);
      if (enmlHash && enmlHash.length > 0) {
        if ((pageNum = parseInt(enmlHash[1])) == page - 2) {
          value = {
            pageNum : pageNum,
            src : reqs[i].responseText
          };
        } else {
          options = {
            pageNum : pageNum,
            src : reqs[i].responseText
          };
        }
      }
    }
    if (isLR) {
      setImages(value, options, "previous");
    } else {
      setImages(options, value, "previous");
    }
  }) : 0 != page && (isLR ? (debugLogger("LR LP:"), debugLogger(typeof value), debugLogger("LR RP:"), debugLogger(typeof options), setImages(value, options, "previous")) : setImages(options, value, "previous")), args.length > 0 ? $.when.apply($, args).done(function() {
    /** @type {number} */
    i = 0;
    for (; i < args.length; i++) {
      var pageNum;
      /** @type {(Array<string>|null)} */
      var enmlHash = /\/([0-9]+)\.jpg/.exec(args[i].responseText);
      if (enmlHash && enmlHash.length > 0) {
        if ((pageNum = parseInt(enmlHash[1])) == page + 2) {
          expected = {
            pageNum : pageNum,
            src : args[i].responseText
          };
        } else {
          data = {
            pageNum : pageNum,
            src : args[i].responseText
          };
        }
      }
    }
    if (isLR) {
      setImages(expected, data, "next");
    } else {
      setImages(data, expected, "next");
    }
  }) : page <= pages - 2 && (debugLogger(expected), debugLogger(data), isLR ? setImages(expected, data, "next") : setImages(data, expected, "next")), 2 == pageMode && page >= pages - 1) {
    /** @type {number} */
    var ngiScroll_timeout = 0;
    if (page <= pages) {
      /** @type {number} */
      ngiScroll_timeout = 150;
    }
    setTimeout(function() {
      $(".reader_page_canvas.next").hide();
    }, ngiScroll_timeout);
  }
  /** @type {number} */
  currentZoom = 1;
  debugLogger("update offscreen pages done");
}
/**
 * @param {string} value
 * @param {string} data
 * @param {string} to
 * @return {undefined}
 */
function setImages(value, data, to) {
  debugLogger("setImages page1: ");
  debugLogger(value);
  debugLogger("setImages page2: ");
  debugLogger(data);
  debugLogger("setImages screen: " + to);
  /** @type {number} */
  var w_width = refPageWidth * respMultiplier;
  /** @type {number} */
  var sentimentHeight = refPageHeight * respMultiplier;
  if ($("#right_page_" + to).remove(), $("#left_page_" + to).remove(), $("#single_page_" + to).remove(), $("#single_partner_page_" + to).remove(), currentZoom = 1, $("#reader_zoom_control").val(1), 2 == pageMode) {
    if (void 0 !== value) {
      $("#reader_page_container").prepend('<img style="padding:0px;margin:0px; display:none; z-index:1;" id="left_page_' + to + '" crossorigin="anonymous" src="' + value.src + '">');
      $("#left_page_" + to).load(function() {
        handlePageData(value.pageNum, w_width, sentimentHeight, "left", to);
      });
    } else {
      if ("current" == to) {
        handleEmptyPage(w_width, sentimentHeight, "left", to);
      } else {
        setTimeout(function() {
          handleEmptyPage(w_width, sentimentHeight, "left", to);
        }, 150);
      }
    }
    if (void 0 !== data) {
      $("#reader_page_container").prepend('<img style="padding:0px;margin:0px; display:none; z-index:1;" id="right_page_' + to + '" crossorigin="anonymous" src="' + data.src + '">');
      $("#right_page_" + to).load(function() {
        handlePageData(data.pageNum, w_width, sentimentHeight, "right", to);
      });
    } else {
      if ("current" == to) {
        handleEmptyPage(w_width, sentimentHeight, "right", to);
      } else {
        setTimeout(function() {
          handleEmptyPage(w_width, sentimentHeight, "right", to);
        }, 150);
      }
    }
  } else {
    if ("current" == to) {
      /** @type {string} */
      var res = value;
      /** @type {string} */
      var scope = data;
      if (1 != pageModeOffset) {
        /** @type {string} */
        res = data;
        /** @type {string} */
        scope = value;
      }
    } else {
      if ("next" == to) {
        /** @type {string} */
        res = data;
        if (isLR) {
          /** @type {string} */
          res = value;
        }
      } else {
        if ("previous" == to) {
          /** @type {string} */
          res = value;
          if (isLR) {
            /** @type {string} */
            res = data;
          }
        }
      }
    }
    if (void 0 !== res ? ($("#reader_page_container").prepend('<img style="padding:0px;margin:0px; display:none; z-index:1;" id="single_page_' + to + '" crossorigin="anonymous" src="' + res.src + '">'), $("#single_page_" + to).load(function() {
      handlePageData(res.pageNum, w_width, sentimentHeight, "single", to);
    })) : pages, "current" == to) {
      if (void 0 !== scope) {
        $("#reader_page_container").prepend('<img style="padding:0px;margin:0px; display:none; z-index:1;" id="single_partner_page_current" crossorigin="anonymous" src="' + scope.src + '">');
        $("#single_partner_page_current").load(function() {
          handlePageData(scope.pageNum, w_width, sentimentHeight, "single_partner", to);
        });
      } else {
        if ("current" == to) {
          handleEmptyPage(w_width, sentimentHeight, "single_partner", to);
        } else {
          setTimeout(function() {
            handleEmptyPage(w_width, sentimentHeight, "single_partner", to);
          }, 150);
        }
      }
    }
  }
  if (false === loaderInterval) {
    /** @type {number} */
    loaderInterval = setInterval(function() {
      preloadImages(false);
    }, 9E4);
  }
}
/**
 * @param {number} width
 * @param {number} height
 * @param {string} direction
 * @param {string} to
 * @return {undefined}
 */
function handleEmptyPage(width, height, direction, to) {
  if (page <= pages || 2 == pageMode && "blank page" == endPages[0] && page <= pages - 2) {
    /** @type {number} */
    var x = 0;
    var $seekBar = $("#reader_page_container");
    if ("current" == to) {
      if ("right" == direction) {
        /** @type {number} */
        x = width;
      } else {
        if ("single" == direction) {
          /** @type {number} */
          x = ($seekBar.width() - width) / 2;
        } else {
          if ("single_partner" == direction) {
            x = isLR && 0 == pageModeOffset || !isLR && 0 != pageModeOffset ? $("#reader_page_container").width() + $("#reader_page_container").offset().left : -$("#reader_page_container").width() - $("#reader_page_container").offset().left;
          }
        }
      }
    } else {
      if (2 == pageMode) {
        if ("next" == to) {
          /** @type {number} */
          x = isLR ? "left" == direction ? 2 * width + 2 * $seekBar.offset().left : 3 * width + 2 * $seekBar.offset().left : "left" == direction ? -2 * width - 2 * $seekBar.offset().left : -width - 2 * $seekBar.offset().left;
        } else {
          if ("previous" == to) {
            /** @type {number} */
            x = isLR ? "left" == direction ? -2 * width - 2 * $seekBar.offset().left : -width - 2 * $seekBar.offset().left : "left" == direction ? 2 * width + 2 * $seekBar.offset().left : 3 * width + 2 * $seekBar.offset().left;
          }
        }
      } else {
        if ("next" == to) {
          /** @type {number} */
          x = -2 * width - 4 * $seekBar.offset().left;
          if (0 != pageModeOffset) {
            /** @type {number} */
            x = -width - 2 * $seekBar.offset().left;
          }
          if (isLR) {
            /** @type {number} */
            x = -x;
          }
        } else {
          if ("previous" == to) {
            x = width + 2 * $seekBar.offset().left;
            if (0 != pageModeOffset) {
              /** @type {number} */
              x = 2 * width + 4 * $seekBar.offset().left;
            }
            if (isLR) {
              /** @type {number} */
              x = -x;
            }
          }
        }
      }
    }
    /** @type {(Element|null)} */
    var canvas = document.getElementById("canvas_" + direction + "_" + to);
    debugLogger("Handling empty page: canvas_" + direction + "_" + to);
    var ctx = canvas.getContext("2d");
    /** @type {number} */
    var currentTime = window.devicePixelRatio || 1;
    var duration = ctx.webkitBackingStorePixelRatio || ctx.mozBackingStorePixelRatio || ctx.msBackingStorePixelRatio || ctx.oBackingStorePixelRatio || ctx.backingStorePixelRatio || 1;
    /** @type {number} */
    var ratio = currentTime / duration;
    if (currentTime !== duration) {
      /** @type {number} */
      var w = width;
      /** @type {number} */
      var h = height;
      /** @type {number} */
      canvas.width = w * ratio;
      /** @type {number} */
      canvas.height = h * ratio;
      /** @type {string} */
      canvas.style.width = w + "px";
      /** @type {string} */
      canvas.style.height = h + "px";
      ctx.scale(ratio, ratio);
    } else {
      /** @type {number} */
      canvas.width = width;
      /** @type {number} */
      canvas.height = height;
      /** @type {string} */
      canvas.style.width = width + "px";
      /** @type {string} */
      canvas.style.height = height + "px";
    }
    if (1 == ratio) {
      /** @type {boolean} */
      ctx.imageSmoothingEnabled = false;
      /** @type {boolean} */
      ctx.mozImageSmoothingEnabled = false;
      /** @type {boolean} */
      ctx.msImageSmoothingEnabled = false;
      /** @type {boolean} */
      ctx.oImageSmoothingEnabled = false;
      /** @type {boolean} */
      ctx.webkitImageSmoothingEnabled = false;
    }
    $("#canvas_" + direction + "_" + to).css({
      left : x + "px",
      top : "0px",
      position : "absolute",
      "z-index" : "3",
      width : width + "px",
      height : height + "px"
    });
    /** @type {string} */
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    debugLogger("Placed empty page at left: " + x);
  }
}
/**
 * @param {string} context
 * @param {number} width
 * @param {number} height
 * @param {string} key
 * @param {string} i
 * @return {undefined}
 */
function handlePageData(context, width, height, key, i) {
  /** @type {number} */
  var imgLeft = 0;
  var $seekBar = $("#reader_page_container");
  if ("current" == i) {
    if ("right" == key) {
      /** @type {number} */
      imgLeft = width;
    } else {
      if ("single" == key) {
        /** @type {number} */
        imgLeft = ($seekBar.width() - width) / 2;
      } else {
        if ("single_partner" == key) {
          imgLeft = 0 == pageModeOffset ? -width - 2 * $seekBar.offset().left : width + 2 * $seekBar.offset().left;
        }
      }
    }
  } else {
    if (2 == pageMode) {
      if ("next" == i) {
        /** @type {number} */
        imgLeft = isLR ? "left" == key ? 2 * width + 2 * $seekBar.offset().left : 3 * width + 2 * $seekBar.offset().left : "left" == key ? -2 * width - 2 * $seekBar.offset().left : -width - 2 * $seekBar.offset().left;
      } else {
        if ("previous" == i) {
          /** @type {number} */
          imgLeft = isLR ? "left" == key ? -2 * width - 2 * $seekBar.offset().left : -width - 2 * $seekBar.offset().left : "left" == key ? 2 * width + 2 * $seekBar.offset().left : 3 * width + 2 * $seekBar.offset().left;
        }
      }
    } else {
      if ("next" == i) {
        imgLeft = isLR ? 0 == pageModeOffset ? width + 2 * $seekBar.offset().left : 2 * (width + 2 * $seekBar.offset().left) : 0 == pageModeOffset ? 2 * -(width + 2 * $seekBar.offset().left) : -width - 2 * $seekBar.offset().left;
      } else {
        if ("previous" == i) {
          imgLeft = isLR ? 0 == pageModeOffset ? 2 * -(width + 2 * $seekBar.offset().left) : -width - 2 * $seekBar.offset().left : 0 == pageModeOffset ? width + 2 * $seekBar.offset().left : 2 * (width + 2 * $seekBar.offset().left);
        }
      }
    }
  }
  /** @type {(Element|null)} */
  var canvas = document.getElementById("canvas_" + key + "_" + i);
  debugLogger("Handling page data: canvas_" + key + "_" + i);
  /** @type {(Element|null)} */
  var g_avatarImage = document.getElementById(key + "_page_" + i);
  var ctx = canvas.getContext("2d");
  /** @type {number} */
  var p = window.devicePixelRatio || 1;
  var length = ctx.webkitBackingStorePixelRatio || ctx.mozBackingStorePixelRatio || ctx.msBackingStorePixelRatio || ctx.oBackingStorePixelRatio || ctx.backingStorePixelRatio || 1;
  /** @type {number} */
  var ratio = p / length;
  if (p !== length) {
    /** @type {number} */
    var elW = g_avatarImage.width - 90;
    /** @type {number} */
    var elH = g_avatarImage.height - 140;
    /** @type {number} */
    canvas.width = elW * ratio;
    /** @type {number} */
    canvas.height = elH * ratio;
    /** @type {string} */
    canvas.style.width = elW + "px";
    /** @type {string} */
    canvas.style.height = elH + "px";
    ctx.scale(ratio, ratio);
  } else {
    /** @type {number} */
    canvas.width = g_avatarImage.width - 90;
    /** @type {number} */
    canvas.height = g_avatarImage.height - 140;
    /** @type {string} */
    canvas.style.width = g_avatarImage.width - 90 + "px";
    /** @type {string} */
    canvas.style.height = g_avatarImage.height - 140 + "px";
  }
  if (1 == ratio && (ctx.imageSmoothingEnabled = false, ctx.mozImageSmoothingEnabled = false, ctx.msImageSmoothingEnabled = false, ctx.oImageSmoothingEnabled = false, ctx.webkitImageSmoothingEnabled = false), ctx.clearRect(0, 0, canvas.width, canvas.height), "undefined" != typeof pageKeys["page" + context]) {
    var name = pageKeys["page" + context].key;
  }
  if (void 0 !== name && "" != name) {
    /** @type {number} */
    const width = parseInt(pageKeys["page" + context].width);
    /** @type {number} */
    const height = parseInt(pageKeys["page" + context].height);
    /** @type {number} */
    var new_width = Math.floor(width / 10);
    /** @type {number} */
    var new_height = Math.floor(height / 15);
    var IEVersion = name.split(":");
    ctx.drawImage(g_avatarImage,
        0, 0,
        width, new_height,

        0, 0,
        width, new_height
    );
    ctx.drawImage(g_avatarImage,
        0, new_height + 10,
        new_width, height - 2 * new_height,

        0, new_height,
        new_width, height - 2 * new_height
    );
    ctx.drawImage(g_avatarImage,
        0, 14 * (new_height + 10),
        width, g_avatarImage.height - 14 * (new_height + 10),

        0, 14 * new_height,
        width, g_avatarImage.height - 14 * (new_height + 10)
    );
    ctx.drawImage(g_avatarImage,
        9 * (new_width + 10), new_height + 10,
        new_width + (width - 10 * new_width), height - 2 * new_height,

        9 * new_width, new_height,
        new_width + (width - 10 * new_width), height - 2 * new_height
    );
    /** @type {number} */
    i = 0;
    for (; i < IEVersion.length; i++) {
      /** @type {number} */
      IEVersion[i] = parseInt(IEVersion[i], 16);
      ctx.drawImage(
          g_avatarImage,
          Math.floor((i % 8 + 1) * (new_width + 10)), Math.floor((Math.floor(i / 8) + 1) * (new_height + 10)),
          Math.floor(new_width), Math.floor(new_height),

          Math.floor((IEVersion[i] % 8 + 1) * new_width), Math.floor((Math.floor(IEVersion[i] / 8) + 1) * new_height),
          Math.floor(new_width), Math.floor(new_height)
      );
    }
  }
  switch($("#canvas_" + key + "_" + i).css({
    left : imgLeft + "px",
    top : "0px",
    position : "absolute",
    "z-index" : "3",
    width : width + "px",
    height : height + "px"
  }), key) {
    case "left":
      /** @type {boolean} */
      leftPageLoaded = true;
      if (true === rightPageLoaded) {
        $("#reader_loading_container").stop(true, true).hide();
      }
      break;
    case "right":
      /** @type {boolean} */
      rightPageLoaded = true;
      if (true === leftPageLoaded) {
        $("#reader_loading_container").stop(true, true).hide();
      }
      break;
    case "single":
      $("#reader_loading_container").stop(true, true).hide();
  }
  $(".reader_page_canvas.top").hammer().off("pan").off("pinch");
  $(".reader_page_canvas.top").hammer().on("pan", panCanvas).on("pinch", pinchZoom);
  if (page < 2) {
    $(".reader_page_canvas.previous").hide();
  } else {
    if (page == pages) {
      $(".reader_page_canvas.next").hide();
    } else {
      if (1 == pageMode) {
        $(".reader_page_canvas.single.previous").show();
        $(".reader_page_canvas.single.next").show();
      } else {
        $(".reader_page_canvas.left.previous, .reader_page_canvas.right.previous").show();
        $(".reader_page_canvas.left.next, .reader_page_canvas.right.next").show();
      }
    }
  }
  if (0 == page && 1 == pageMode && 0 == pageModeOffset && pageKeys.page0 !== undefined && pageKeys.page0.size < 6E3) {
    if (isLR) {
      incrementRight();
    } else {
      incrementLeft();
    }
  }
}
/**
 * @return {undefined}
 */
function updateLinkAreas() {
  if (metadata.pages && metadata.pages.length) {
    if (pageLinks = [], pageData = metadata.pages.filter(function(action) {
      return action.pageNumber == page;
    }), pagePlusOneData = metadata.pages.filter(function(table) {
      return table.pageNumber == page + 1;
    }), pageData.length > 0) {
      /** @type {number} */
      var nIdx = 0;
      for (; height = pageData[0].links[nIdx++];) {
        var coords = $.extend(true, {}, height);
        if (!isLR) {
          coords.x += metadata.width;
        }
        pageLinks.push(coords);
      }
    }
    if (pagePlusOneData.length > 0) {
      var height;
      /** @type {number} */
      nIdx = 0;
      for (; height = pagePlusOneData[0].links[nIdx++];) {
        coords = $.extend(true, {}, height);
        if (isLR) {
          coords.x += metadata.width;
        }
        pageLinks.push(coords);
      }
    }
  }
}
/**
 * @return {undefined}
 */
function adjustChapterAd() {
  var $checkingBit = $("#end_page_ad_container");
  var sparklineElement = $("#free-chapter-ad div:first-child");
  var $oElemDragged = $("#free-chapter-ad iframe");
  var filteredView = $oElemDragged.contents();
  if (true === $.browser.mobile && 0 != window.orientation && $("#end_page_ad").width() < 300) {
    /** @type {number} */
    var iframeWidth = 180;
    /** @type {number} */
    var top = 150;
  } else {
    /** @type {number} */
    iframeWidth = 300;
    /** @type {number} */
    top = 250;
  }
  $checkingBit.width(iframeWidth);
  $checkingBit.height(top);
  sparklineElement.attr("style", "border: 0pt none; width:" + iframeWidth + "px; height: " + top + "px;");
  $oElemDragged.attr({
    width : "100%",
    height : "100%"
  });
  filteredView.find("#google_image_div").css({
    width : iframeWidth + "px",
    height : top + "px",
    overflow : "hidden",
    position : "absolute"
  });
  filteredView.find(".img_ad").attr("style", "width:" + iframeWidth + "px; height: " + top + "px;");
  /** @type {number} */
  var _ileft = ($("#end_page_ad").width() - $checkingBit.width()) / 2;
  /** @type {number} */
  var tabPadding = ($("#end_page_ad").height() - $checkingBit.height()) / 2;
  $checkingBit.css({
    left : _ileft,
    top : tabPadding
  });
}
/**
 * @return {undefined}
 */
function adjustChapterAdModal() {
  var $this = $("#metamodal-chapter-ad");
  var t = window.innerHeight ? window.innerHeight : $(window).height();
  var a = $("#free-chapter-ad iframe");
  var o = (a.contents(), a.contents().find("a"));
  var r = a.contents().find("a img");
  if (true === $.browser.mobile && 0 != window.orientation && t < 290) {
    /** @type {number} */
    var i = 210;
    /** @type {number} */
    var h = 175;
  } else {
    /** @type {number} */
    i = 300;
    /** @type {number} */
    h = 250;
  }
  r.width(i);
  o.width(i);
  a.width(i);
  $this.width(i);
  r.height(h);
  a.height(h);
  o.height(h);
  $this.height(h + 40);
  /** @type {number} */
  var _ileft = ($(window).width() - $this.outerWidth()) / 2;
  /** @type {number} */
  var tabPadding = (t - $this.outerHeight()) / 2;
  $this.css({
    left : _ileft,
    top : tabPadding
  });
}
/**
 * @return {undefined}
 */
function checkChapterAdFilled() {
  if (adRendered && !adFilled) {
    MetaModals.toggle("#metamodal-chapter-ad");
  }
}
/**
 * @return {undefined}
 */
function createFlashReader() {
  $("#reader_container_sc").remove();
  var linkCont = $('<div id="reader_container_fl">                            <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" width="100%" height="100%" id="reader" align="t">                              <param name="movie" value=" /assets/reader-b905dad55b251b539b0ff56c70965f67fb7f871cdeca83290ae2bebe4f418f49.swf" />                              <param name="quality" value="high" />                              <param name="bgcolor" value="#ffffff" />                              <param name="play" value="true" />                              <param name="loop" value="true" />                              <param name="wmode" value="opaque" />                              <param name="scale" value="showall" />                              <param name="menu" value="true" />                              <param name="devicefont" value="false" />                              <param name="salign" value="t" />                              <param name="allowScriptAccess" value="sameDomain" />                              <param name="allowFullScreen" value="true" />                              \x3c!--[if !IE]>--\x3e                              <object type="application/x-shockwave-flash" data="/assets/reader-b905dad55b251b539b0ff56c70965f67fb7f871cdeca83290ae2bebe4f418f49.swf" width="100%" height="100%" align="t">                                <param name="movie" value="/assets/reader-b905dad55b251b539b0ff56c70965f67fb7f871cdeca83290ae2bebe4f418f49.swf" />                                <param name="quality" value="high" />                                <param name="bgcolor" value="#ffffff" />                                <param name="play" value="true" />                                <param name="loop" value="true" />                                <param name="wmode" value="opaque" />                                <param name="scale" value="showall" />                                <param name="menu" value="true" />                                <param name="devicefont" value="false" />                                <param name="salign" value="t" />                                <param name="allowScriptAccess" value="sameDomain" />                                <param name="allowFullScreen" value="true" />                              \x3c!--<![endif]--\x3e                                <a href="http://www.adobe.com/go/getflash">                                  <img src="http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif" alt="Get Adobe Flash player" />                                </a>                              \x3c!--[if !IE]>--\x3e                              </object>                              \x3c!--<![endif]--\x3e                            </object>                          </div>');
  $("#reader_wrapper").append(linkCont);
}
/**
 * @return {undefined}
 */
function adjustFlashReader() {
  $("#reader_window");
  var e = $("#modal-reader");
  var $expansion = $("#modal-reader-header");
  e.addClass("pad-md");
  $expansion.addClass("pad-b-md");
  var oldContW = e.width();
  /** @type {number} */
  var n = e.height() - $expansion.outerHeight(true);
  $("#reader_container_fl").addClass("not-mobile").css({
    left : 0,
    top : 0
  }).width(oldContW).height(n).show();
}
!function(window, doc, exportName, undefined) {
  /**
   * @param {!Function} fn
   * @param {?} timeout
   * @param {?} context
   * @return {?}
   */
  function setTimeoutContext(fn, timeout, context) {
    return setTimeout(bindFn(fn, context), timeout);
  }
  /**
   * @param {!Object} arg
   * @param {string} fn
   * @param {!Object} context
   * @return {?}
   */
  function invokeArrayArg(arg, fn, context) {
    return !!Array.isArray(arg) && (each(arg, context[fn], context), true);
  }
  /**
   * @param {string} x
   * @param {!Function} self
   * @param {!Object} a
   * @return {undefined}
   */
  function each(x, self, a) {
    var k;
    if (x) {
      if (x.forEach) {
        x.forEach(self, a);
      } else {
        if (x.length !== undefined) {
          /** @type {number} */
          k = 0;
          for (; k < x.length;) {
            self.call(a, x[k], k, x);
            k++;
          }
        } else {
          for (k in x) {
            if (x.hasOwnProperty(k)) {
              self.call(a, x[k], k, x);
            }
          }
        }
      }
    }
  }
  /**
   * @param {string} target
   * @param {!Object} source
   * @param {string} key
   * @return {?}
   */
  function extend(target, source, key) {
    /** @type {!Array<string>} */
    var keys = Object.keys(source);
    /** @type {number} */
    var i = 0;
    for (; i < keys.length;) {
      if (!key || key && target[keys[i]] === undefined) {
        target[keys[i]] = source[keys[i]];
      }
      i++;
    }
    return target;
  }
  /**
   * @param {boolean} from
   * @param {!Object} key
   * @return {?}
   */
  function merge(from, key) {
    return extend(from, key, true);
  }
  /**
   * @param {!Function} child
   * @param {!Function} base
   * @param {!Object} target
   * @return {undefined}
   */
  function inherit(child, base, target) {
    var childP;
    var baseP = base.prototype;
    /** @type {!Function} */
    (childP = child.prototype = Object.create(baseP)).constructor = child;
    childP._super = baseP;
    if (target) {
      extend(childP, target);
    }
  }
  /**
   * @param {!Function} fn
   * @param {?} context
   * @return {?}
   */
  function bindFn(fn, context) {
    return function() {
      return fn.apply(context, arguments);
    };
  }
  /**
   * @param {!Function} val
   * @param {!Object} args
   * @return {?}
   */
  function boolOrFn(val, args) {
    return typeof val == TYPE_FUNCTION ? val.apply(args && args[0] || undefined, args) : val;
  }
  /**
   * @param {string} val1
   * @param {string} val2
   * @return {?}
   */
  function ifUndefined(val1, val2) {
    return val1 === undefined ? val2 : val1;
  }
  /**
   * @param {string} type
   * @param {!Function} listener
   * @param {!Function} target
   * @return {undefined}
   */
  function addEventListeners(type, listener, target) {
    each($(listener), function(t) {
      type.addEventListener(t, target, false);
    });
  }
  /**
   * @param {!Object} event
   * @param {string} selector
   * @param {?} callback
   * @return {undefined}
   */
  function removeEventListeners(event, selector, callback) {
    each($(selector), function(type) {
      event.removeEventListener(type, callback, false);
    });
  }
  /**
   * @param {!Object} parent
   * @param {!Object} node
   * @return {?}
   */
  function hasParent(parent, node) {
    for (; parent;) {
      if (parent == node) {
        return true;
      }
      parent = parent.parentNode;
    }
    return false;
  }
  /**
   * @param {string} str
   * @param {string} find
   * @return {?}
   */
  function inStr(str, find) {
    return str.indexOf(find) > -1;
  }
  /**
   * @param {string} fn
   * @return {?}
   */
  function $(fn) {
    return fn.trim().split(/\s+/g);
  }
  /**
   * @param {!Array} src
   * @param {!Object} find
   * @param {string} findByKey
   * @return {?}
   */
  function inArray(src, find, findByKey) {
    if (src.indexOf && !findByKey) {
      return src.indexOf(find);
    }
    /** @type {number} */
    var i = 0;
    for (; i < src.length;) {
      if (findByKey && src[i][findByKey] == find || !findByKey && src[i] === find) {
        return i;
      }
      i++;
    }
    return -1;
  }
  /**
   * @param {?} elemntList
   * @return {?}
   */
  function toArray(elemntList) {
    return Array.prototype.slice.call(elemntList, 0);
  }
  /**
   * @param {!NodeList} map
   * @param {string} attr
   * @param {boolean} debug
   * @return {?}
   */
  function build(map, attr, debug) {
    /** @type {!Array} */
    var ret = [];
    /** @type {!Array} */
    var values = [];
    /** @type {number} */
    var i = 0;
    for (; i < map.length;) {
      var key = attr ? map[i][attr] : map[i];
      if (inArray(values, key) < 0) {
        ret.push(map[i]);
      }
      values[i] = key;
      i++;
    }
    return debug && (ret = attr ? ret.sort(function(results, result) {
      return results[attr] > result[attr];
    }) : ret.sort()), ret;
  }
  /**
   * @param {!Object} name
   * @param {string} property
   * @return {?}
   */
  function prefixed(name, property) {
    var prefix;
    var prop;
    var day_display = property[0].toUpperCase() + property.slice(1);
    /** @type {number} */
    var i = 0;
    for (; i < VENDOR_PREFIXES.length;) {
      if ((prop = (prefix = VENDOR_PREFIXES[i]) ? prefix + day_display : property) in name) {
        return prop;
      }
      i++;
    }
    return undefined;
  }
  /**
   * @return {?}
   */
  function uniqueId() {
    return fe++;
  }
  /**
   * @param {!Element} element
   * @return {?}
   */
  function getWindowForElement(element) {
    var doc = element.ownerDocument;
    return doc.defaultView || doc.parentWindow;
  }
  /**
   * @param {?} manager
   * @param {!Function} callback
   * @return {undefined}
   */
  function Input(manager, callback) {
    var thisHandler = this;
    this.manager = manager;
    /** @type {!Function} */
    this.callback = callback;
    this.element = manager.element;
    this.target = manager.options.inputTarget;
    /**
     * @param {!Object} e
     * @return {undefined}
     */
    this.domHandler = function(e) {
      if (boolOrFn(manager.options.enable, [manager])) {
        thisHandler.handler(e);
      }
    };
    this.init();
  }
  /**
   * @param {!Object} manager
   * @return {?}
   */
  function createInputInstance(manager) {
    var ua = manager.options.inputClass;
    return new (ua || (isBrowser ? PointerEventInput : isWorker ? TouchInput : IS_TOUCH_ENABLED ? TouchMouseInput : MouseInput))(manager, inputHandler);
  }
  /**
   * @param {?} manager
   * @param {string} eventType
   * @param {!Object} input
   * @return {undefined}
   */
  function inputHandler(manager, eventType, input) {
    var maxNrStages = input.pointers.length;
    var nrStages = input.changedPointers.length;
    /** @type {(boolean|number)} */
    var i = eventType & INPUT_START && maxNrStages - nrStages == 0;
    /** @type {(boolean|number)} */
    var o = eventType & (INPUT_END | INPUT_CANCEL) && maxNrStages - nrStages == 0;
    /** @type {boolean} */
    input.isFirst = !!i;
    /** @type {boolean} */
    input.isFinal = !!o;
    if (i) {
      manager.session = {};
    }
    /** @type {string} */
    input.eventType = eventType;
    computeInputData(manager, input);
    manager.emit("hammer.input", input);
    manager.recognize(input);
    /** @type {!Object} */
    manager.session.prevInput = input;
  }
  /**
   * @param {!Object} manager
   * @param {!Object} input
   * @return {undefined}
   */
  function computeInputData(manager, input) {
    var session = manager.session;
    var pointers = input.pointers;
    var pointersLength = pointers.length;
    if (!session.firstInput) {
      session.firstInput = simpleCloneInputData(input);
    }
    if (pointersLength > 1 && !session.firstMultiple) {
      session.firstMultiple = simpleCloneInputData(input);
    } else {
      if (1 === pointersLength) {
        /** @type {boolean} */
        session.firstMultiple = false;
      }
    }
    var firstInput = session.firstInput;
    var firstMultiple = session.firstMultiple;
    var offsetCenter = firstMultiple ? firstMultiple.center : firstInput.center;
    var center = input.center = getCenter(pointers);
    /** @type {number} */
    input.timeStamp = now();
    /** @type {number} */
    input.deltaTime = input.timeStamp - firstInput.timeStamp;
    input.angle = getAngle(offsetCenter, center);
    input.distance = getDistance(offsetCenter, center);
    computeDeltaXY(session, input);
    input.offsetDirection = getDirection(input.deltaX, input.deltaY);
    input.scale = firstMultiple ? getScale(firstMultiple.pointers, pointers) : 1;
    input.rotation = firstMultiple ? getRotation(firstMultiple.pointers, pointers) : 0;
    computeIntervalInputData(session, input);
    var target = manager.element;
    if (hasParent(input.srcEvent.target, target)) {
      target = input.srcEvent.target;
    }
    input.target = target;
  }
  /**
   * @param {?} session
   * @param {!Object} input
   * @return {undefined}
   */
  function computeDeltaXY(session, input) {
    var c = input.center;
    var b = session.offsetDelta || {};
    var xhair = session.prevDelta || {};
    var prevInput = session.prevInput || {};
    if (input.eventType === INPUT_START || prevInput.eventType === INPUT_END) {
      xhair = session.prevDelta = {
        x : prevInput.deltaX || 0,
        y : prevInput.deltaY || 0
      };
      b = session.offsetDelta = {
        x : c.x,
        y : c.y
      };
    }
    input.deltaX = xhair.x + (c.x - b.x);
    input.deltaY = xhair.y + (c.y - b.y);
  }
  /**
   * @param {!Object} session
   * @param {!Object} input
   * @return {undefined}
   */
  function computeIntervalInputData(session, input) {
    var velocity;
    var velocityX;
    var velocityY;
    var direction;
    var last = session.lastInterval || input;
    /** @type {number} */
    var deltaTime = input.timeStamp - last.timeStamp;
    if (input.eventType != INPUT_CANCEL && (deltaTime > CAL_INTERVAL || last.velocity === undefined)) {
      /** @type {number} */
      var deltaX = last.deltaX - input.deltaX;
      /** @type {number} */
      var deltaY = last.deltaY - input.deltaY;
      var v = getVelocity(deltaTime, deltaX, deltaY);
      velocityX = v.x;
      velocityY = v.y;
      velocity = abs(v.x) > abs(v.y) ? v.x : v.y;
      direction = getDirection(deltaX, deltaY);
      /** @type {!Object} */
      session.lastInterval = input;
    } else {
      velocity = last.velocity;
      velocityX = last.velocityX;
      velocityY = last.velocityY;
      direction = last.direction;
    }
    input.velocity = velocity;
    input.velocityX = velocityX;
    input.velocityY = velocityY;
    input.direction = direction;
  }
  /**
   * @param {!Object} input
   * @return {?}
   */
  function simpleCloneInputData(input) {
    /** @type {!Array} */
    var pointers = [];
    /** @type {number} */
    var i = 0;
    for (; i < input.pointers.length;) {
      pointers[i] = {
        clientX : round(input.pointers[i].clientX),
        clientY : round(input.pointers[i].clientY)
      };
      i++;
    }
    return {
      timeStamp : now(),
      pointers : pointers,
      center : getCenter(pointers),
      deltaX : input.deltaX,
      deltaY : input.deltaY
    };
  }
  /**
   * @param {!Array} pointers
   * @return {?}
   */
  function getCenter(pointers) {
    var pointersLength = pointers.length;
    if (1 === pointersLength) {
      return {
        x : round(pointers[0].clientX),
        y : round(pointers[0].clientY)
      };
    }
    /** @type {number} */
    var x = 0;
    /** @type {number} */
    var y = 0;
    /** @type {number} */
    var i = 0;
    for (; pointersLength > i;) {
      x = x + pointers[i].clientX;
      y = y + pointers[i].clientY;
      i++;
    }
    return {
      x : round(x / pointersLength),
      y : round(y / pointersLength)
    };
  }
  /**
   * @param {number} deltaTime
   * @param {number} x
   * @param {number} y
   * @return {?}
   */
  function getVelocity(deltaTime, x, y) {
    return {
      x : x / deltaTime || 0,
      y : y / deltaTime || 0
    };
  }
  /**
   * @param {number} x
   * @param {number} y
   * @return {?}
   */
  function getDirection(x, y) {
    return x === y ? DIRECTION_NONE : abs(x) >= abs(y) ? x > 0 ? left : right : y > 0 ? DIRECTION_UP : DIRECTION_DOWN;
  }
  /**
   * @param {?} p1
   * @param {?} p2
   * @param {!Array} props
   * @return {?}
   */
  function getDistance(p1, p2, props) {
    if (!props) {
      /** @type {!Array} */
      props = PROPS_XY;
    }
    /** @type {number} */
    var lightI = p2[props[0]] - p1[props[0]];
    /** @type {number} */
    var lightJ = p2[props[1]] - p1[props[1]];
    return Math.sqrt(lightI * lightI + lightJ * lightJ);
  }
  /**
   * @param {?} p1
   * @param {?} p2
   * @param {!Array} props
   * @return {?}
   */
  function getAngle(p1, p2, props) {
    if (!props) {
      /** @type {!Array} */
      props = PROPS_XY;
    }
    /** @type {number} */
    var mouseStartXFromCentre = p2[props[0]] - p1[props[0]];
    /** @type {number} */
    var trueAnomalyY = p2[props[1]] - p1[props[1]];
    return 180 * Math.atan2(trueAnomalyY, mouseStartXFromCentre) / Math.PI;
  }
  /**
   * @param {!Object} start
   * @param {!Object} end
   * @return {?}
   */
  function getRotation(start, end) {
    return getAngle(end[1], end[0], PROPS_CLIENT_XY) - getAngle(start[1], start[0], PROPS_CLIENT_XY);
  }
  /**
   * @param {!Object} start
   * @param {!Object} end
   * @return {?}
   */
  function getScale(start, end) {
    return getDistance(end[0], end[1], PROPS_CLIENT_XY) / getDistance(start[0], start[1], PROPS_CLIENT_XY);
  }
  /**
   * @return {undefined}
   */
  function MouseInput() {
    /** @type {string} */
    this.evEl = MOUSE_ELEMENT_EVENTS;
    /** @type {string} */
    this.evWin = POINTER_WINDOW_EVENTS;
    /** @type {boolean} */
    this.allow = true;
    /** @type {boolean} */
    this.pressed = false;
    Input.apply(this, arguments);
  }
  /**
   * @return {undefined}
   */
  function PointerEventInput() {
    this.evEl = POINTER_ELEMENT_EVENTS;
    this.evWin = MOUSE_WINDOW_EVENTS;
    Input.apply(this, arguments);
    /** @type {!Array} */
    this.store = this.manager.session.pointerEvents = [];
  }
  /**
   * @return {undefined}
   */
  function SingleTouchInput() {
    /** @type {string} */
    this.evTarget = SINGLE_TOUCH_TARGET_EVENTS;
    /** @type {string} */
    this.evWin = SINGLE_TOUCH_WINDOW_EVENTS;
    /** @type {boolean} */
    this.started = false;
    Input.apply(this, arguments);
  }
  /**
   * @param {!Event} ev
   * @param {number} type
   * @return {?}
   */
  function normalizeSingleTouches(ev, type) {
    var result = toArray(ev.touches);
    var i = toArray(ev.changedTouches);
    return type & (INPUT_END | INPUT_CANCEL) && (result = build(result.concat(i), "identifier", true)), [result, i];
  }
  /**
   * @return {undefined}
   */
  function TouchInput() {
    /** @type {string} */
    this.evTarget = TOUCH_TARGET_EVENTS;
    this.targetIds = {};
    Input.apply(this, arguments);
  }
  /**
   * @param {!Event} e
   * @param {number} type
   * @return {?}
   */
  function getTouches(e, type) {
    var allTouches = toArray(e.touches);
    var targetIds = this.targetIds;
    if (type & (INPUT_START | INPUT_MOVE) && 1 === allTouches.length) {
      return targetIds[allTouches[0].identifier] = true, [allTouches, allTouches];
    }
    var i;
    var columns;
    var args = toArray(e.changedTouches);
    /** @type {!Array} */
    var path = [];
    var target = this.target;
    if (columns = allTouches.filter(function(touch) {
      return hasParent(touch.target, target);
    }), type === INPUT_START) {
      /** @type {number} */
      i = 0;
      for (; i < columns.length;) {
        /** @type {boolean} */
        targetIds[columns[i].identifier] = true;
        i++;
      }
    }
    /** @type {number} */
    i = 0;
    for (; i < args.length;) {
      if (targetIds[args[i].identifier]) {
        path.push(args[i]);
      }
      if (type & (INPUT_END | INPUT_CANCEL)) {
        delete targetIds[args[i].identifier];
      }
      i++;
    }
    return path.length ? [build(columns.concat(path), "identifier", true), path] : void 0;
  }
  /**
   * @return {undefined}
   */
  function TouchMouseInput() {
    Input.apply(this, arguments);
    var handler = bindFn(this.handler, this);
    this.touch = new TouchInput(this.manager, handler);
    this.mouse = new MouseInput(this.manager, handler);
  }
  /**
   * @param {?} manager
   * @param {undefined} value
   * @return {undefined}
   */
  function TouchAction(manager, value) {
    this.manager = manager;
    this.set(value);
  }
  /**
   * @param {string} actions
   * @return {?}
   */
  function cleanTouchActions(actions) {
    if (inStr(actions, TOUCH_ACTION_NONE)) {
      return TOUCH_ACTION_NONE;
    }
    var hasPanX = inStr(actions, TOUCH_ACTION_PAN_X);
    var hasPanY = inStr(actions, TOUCH_ACTION_PAN_Y);
    return hasPanX && hasPanY ? TOUCH_ACTION_PAN_X + " " + TOUCH_ACTION_PAN_Y : hasPanX || hasPanY ? hasPanX ? TOUCH_ACTION_PAN_X : TOUCH_ACTION_PAN_Y : inStr(actions, TOUCH_ACTION_MANIPULATION) ? TOUCH_ACTION_MANIPULATION : peg$c206;
  }
  /**
   * @param {number} options
   * @return {undefined}
   */
  function Recognizer(options) {
    this.id = uniqueId();
    /** @type {null} */
    this.manager = null;
    this.options = merge(options || {}, this.defaults);
    this.options.enable = ifUndefined(this.options.enable, true);
    /** @type {number} */
    this.state = STATE_POSSIBLE;
    this.simultaneous = {};
    /** @type {!Array} */
    this.requireFail = [];
  }
  /**
   * @param {number} state
   * @return {?}
   */
  function f(state) {
    return state & STATE_CANCELLED ? "cancel" : state & STATE_ENDED ? "end" : state & STATE_CHANGED ? "move" : state & STATE_BEGAN ? "start" : "";
  }
  /**
   * @param {number} direction
   * @return {?}
   */
  function directionStr(direction) {
    return direction == DIRECTION_DOWN ? "down" : direction == DIRECTION_UP ? "up" : direction == left ? "left" : direction == right ? "right" : "";
  }
  /**
   * @param {!Object} otherRecognizer
   * @param {!Window} recognizer
   * @return {?}
   */
  function getRecognizerByNameIfManager(otherRecognizer, recognizer) {
    var manager = recognizer.manager;
    return manager ? manager.get(otherRecognizer) : otherRecognizer;
  }
  /**
   * @return {undefined}
   */
  function AttrRecognizer() {
    Recognizer.apply(this, arguments);
  }
  /**
   * @return {undefined}
   */
  function PanRecognizer() {
    AttrRecognizer.apply(this, arguments);
    /** @type {null} */
    this.pX = null;
    /** @type {null} */
    this.pY = null;
  }
  /**
   * @return {undefined}
   */
  function PinchRecognizer() {
    AttrRecognizer.apply(this, arguments);
  }
  /**
   * @return {undefined}
   */
  function PressRecognizer() {
    Recognizer.apply(this, arguments);
    /** @type {null} */
    this._timer = null;
    /** @type {null} */
    this._input = null;
  }
  /**
   * @return {undefined}
   */
  function RotateRecognizer() {
    AttrRecognizer.apply(this, arguments);
  }
  /**
   * @return {undefined}
   */
  function SwipeRecognizer() {
    AttrRecognizer.apply(this, arguments);
  }
  /**
   * @return {undefined}
   */
  function TapRecognizer() {
    Recognizer.apply(this, arguments);
    /** @type {boolean} */
    this.pTime = false;
    /** @type {boolean} */
    this.pCenter = false;
    /** @type {null} */
    this._timer = null;
    /** @type {null} */
    this._input = null;
    /** @type {number} */
    this.count = 0;
  }
  /**
   * @param {string} element
   * @param {!Object} options
   * @return {?}
   */
  function Hammer(element, options) {
    return (options = options || {}).recognizers = ifUndefined(options.recognizers, Hammer.defaults.preset), new Manager(element, options);
  }
  /**
   * @param {!Object} element
   * @param {!Object} options
   * @return {undefined}
   */
  function Manager(element, options) {
    options = options || {};
    this.options = merge(options, Hammer.defaults);
    this.options.inputTarget = this.options.inputTarget || element;
    this.handlers = {};
    this.session = {};
    /** @type {!Array} */
    this.recognizers = [];
    /** @type {!Object} */
    this.element = element;
    this.input = createInputInstance(this);
    this.touchAction = new TouchAction(this, this.options.touchAction);
    toggleCssProps(this, true);
    each(options.recognizers, function(item) {
      var recognizer = this.add(new item[0](item[1]));
      if (item[2]) {
        recognizer.recognizeWith(item[2]);
      }
      if (item[3]) {
        recognizer.requireFailure(item[3]);
      }
    }, this);
  }
  /**
   * @param {!Object} manager
   * @param {string} add
   * @return {undefined}
   */
  function toggleCssProps(manager, add) {
    var element = manager.element;
    each(manager.options.cssProps, function(value, name) {
      element.style[prefixed(element.style, name)] = add ? value : "";
    });
  }
  /**
   * @param {string} event
   * @param {!Object} data
   * @return {undefined}
   */
  function triggerDomEvent(event, data) {
    /** @type {(Event|null)} */
    var gestureEvent = doc.createEvent("Event");
    gestureEvent.initEvent(event, true, true);
    /** @type {!Object} */
    gestureEvent.gesture = data;
    data.target.dispatchEvent(gestureEvent);
  }
  /** @type {!Array} */
  var VENDOR_PREFIXES = ["", "webkit", "moz", "MS", "ms", "o"];
  /** @type {!Element} */
  var TEST_ELEMENT = doc.createElement("div");
  /** @type {string} */
  var TYPE_FUNCTION = "function";
  /** @type {function(?): number} */
  var round = Math.round;
  /** @type {function(?): number} */
  var abs = Math.abs;
  /** @type {function(): number} */
  var now = Date.now;
  /** @type {number} */
  var fe = 1;
  /** @type {!RegExp} */
  var FIREFOX_LINUX = /mobile|tablet|ip(ad|hone|od)|android/i;
  /** @type {boolean} */
  var IS_TOUCH_ENABLED = "ontouchstart" in window;
  /** @type {boolean} */
  var isBrowser = prefixed(window, "PointerEvent") !== undefined;
  /** @type {boolean} */
  var isWorker = IS_TOUCH_ENABLED && FIREFOX_LINUX.test(navigator.userAgent);
  /** @type {string} */
  var INPUT_TYPE_TOUCH = "touch";
  /** @type {string} */
  var INPUT_TYPE_PEN = "pen";
  /** @type {string} */
  var INPUT_TYPE_MOUSE = "mouse";
  /** @type {string} */
  var INPUT_TYPE_KINECT = "kinect";
  /** @type {number} */
  var CAL_INTERVAL = 25;
  /** @type {number} */
  var INPUT_START = 1;
  /** @type {number} */
  var INPUT_MOVE = 2;
  /** @type {number} */
  var INPUT_END = 4;
  /** @type {number} */
  var INPUT_CANCEL = 8;
  /** @type {number} */
  var DIRECTION_NONE = 1;
  /** @type {number} */
  var left = 2;
  /** @type {number} */
  var right = 4;
  /** @type {number} */
  var DIRECTION_UP = 8;
  /** @type {number} */
  var DIRECTION_DOWN = 16;
  /** @type {number} */
  var DIRECTION_HORIZONTAL = left | right;
  /** @type {number} */
  var DIRECTION_VERTICAL = DIRECTION_UP | DIRECTION_DOWN;
  /** @type {number} */
  var DIRECTION_ALL = DIRECTION_HORIZONTAL | DIRECTION_VERTICAL;
  /** @type {!Array} */
  var PROPS_XY = ["x", "y"];
  /** @type {!Array} */
  var PROPS_CLIENT_XY = ["clientX", "clientY"];
  Input.prototype = {
    handler : function() {
    },
    init : function() {
      if (this.evEl) {
        addEventListeners(this.element, this.evEl, this.domHandler);
      }
      if (this.evTarget) {
        addEventListeners(this.target, this.evTarget, this.domHandler);
      }
      if (this.evWin) {
        addEventListeners(getWindowForElement(this.element), this.evWin, this.domHandler);
      }
    },
    destroy : function() {
      if (this.evEl) {
        removeEventListeners(this.element, this.evEl, this.domHandler);
      }
      if (this.evTarget) {
        removeEventListeners(this.target, this.evTarget, this.domHandler);
      }
      if (this.evWin) {
        removeEventListeners(getWindowForElement(this.element), this.evWin, this.domHandler);
      }
    }
  };
  var MOUSE_INPUT_MAP = {
    mousedown : INPUT_START,
    mousemove : INPUT_MOVE,
    mouseup : INPUT_END
  };
  /** @type {string} */
  var MOUSE_ELEMENT_EVENTS = "mousedown";
  /** @type {string} */
  var POINTER_WINDOW_EVENTS = "mousemove mouseup";
  inherit(MouseInput, Input, {
    handler : function(ev) {
      var eventType = MOUSE_INPUT_MAP[ev.type];
      if (eventType & INPUT_START && 0 === ev.button) {
        /** @type {boolean} */
        this.pressed = true;
      }
      if (eventType & INPUT_MOVE && 1 !== ev.which) {
        /** @type {number} */
        eventType = INPUT_END;
      }
      if (this.pressed && this.allow) {
        if (eventType & INPUT_END) {
          /** @type {boolean} */
          this.pressed = false;
        }
        this.callback(this.manager, eventType, {
          pointers : [ev],
          changedPointers : [ev],
          pointerType : INPUT_TYPE_MOUSE,
          srcEvent : ev
        });
      }
    }
  });
  var POINTER_INPUT_MAP = {
    pointerdown : INPUT_START,
    pointermove : INPUT_MOVE,
    pointerup : INPUT_END,
    pointercancel : INPUT_CANCEL,
    pointerout : INPUT_CANCEL
  };
  var IE10_POINTER_TYPE_ENUM = {
    2 : INPUT_TYPE_TOUCH,
    3 : INPUT_TYPE_PEN,
    4 : INPUT_TYPE_MOUSE,
    5 : INPUT_TYPE_KINECT
  };
  /** @type {string} */
  var POINTER_ELEMENT_EVENTS = "pointerdown";
  /** @type {string} */
  var MOUSE_WINDOW_EVENTS = "pointermove pointerup pointercancel";
  if (window.MSPointerEvent) {
    /** @type {string} */
    POINTER_ELEMENT_EVENTS = "MSPointerDown";
    /** @type {string} */
    MOUSE_WINDOW_EVENTS = "MSPointerMove MSPointerUp MSPointerCancel";
  }
  inherit(PointerEventInput, Input, {
    handler : function(ev) {
      var store = this.store;
      /** @type {boolean} */
      var a = false;
      var eventTypeNormalized = ev.type.toLowerCase().replace("ms", "");
      var eventType = POINTER_INPUT_MAP[eventTypeNormalized];
      var pointerType = IE10_POINTER_TYPE_ENUM[ev.pointerType] || ev.pointerType;
      /** @type {boolean} */
      var isTouch = pointerType == INPUT_TYPE_TOUCH;
      var storeIndex = inArray(store, ev.pointerId, "pointerId");
      if (eventType & INPUT_START && (0 === ev.button || isTouch)) {
        if (0 > storeIndex) {
          store.push(ev);
          /** @type {number} */
          storeIndex = store.length - 1;
        }
      } else {
        if (eventType & (INPUT_END | INPUT_CANCEL)) {
          /** @type {boolean} */
          a = true;
        }
      }
      if (!(0 > storeIndex)) {
        /** @type {!Object} */
        store[storeIndex] = ev;
        this.callback(this.manager, eventType, {
          pointers : store,
          changedPointers : [ev],
          pointerType : pointerType,
          srcEvent : ev
        });
        if (a) {
          store.splice(storeIndex, 1);
        }
      }
    }
  });
  var TOUCH_INPUT_MAP = {
    touchstart : INPUT_START,
    touchmove : INPUT_MOVE,
    touchend : INPUT_END,
    touchcancel : INPUT_CANCEL
  };
  /** @type {string} */
  var SINGLE_TOUCH_TARGET_EVENTS = "touchstart";
  /** @type {string} */
  var SINGLE_TOUCH_WINDOW_EVENTS = "touchstart touchmove touchend touchcancel";
  inherit(SingleTouchInput, Input, {
    handler : function(ev) {
      var type = TOUCH_INPUT_MAP[ev.type];
      if (type === INPUT_START && (this.started = true), this.started) {
        var touches = normalizeSingleTouches.call(this, ev, type);
        if (type & (INPUT_END | INPUT_CANCEL) && touches[0].length - touches[1].length == 0) {
          /** @type {boolean} */
          this.started = false;
        }
        this.callback(this.manager, type, {
          pointers : touches[0],
          changedPointers : touches[1],
          pointerType : INPUT_TYPE_TOUCH,
          srcEvent : ev
        });
      }
    }
  });
  var SINGLE_TOUCH_INPUT_MAP = {
    touchstart : INPUT_START,
    touchmove : INPUT_MOVE,
    touchend : INPUT_END,
    touchcancel : INPUT_CANCEL
  };
  /** @type {string} */
  var TOUCH_TARGET_EVENTS = "touchstart touchmove touchend touchcancel";
  inherit(TouchInput, Input, {
    handler : function(ev) {
      var type = SINGLE_TOUCH_INPUT_MAP[ev.type];
      var touches = getTouches.call(this, ev, type);
      if (touches) {
        this.callback(this.manager, type, {
          pointers : touches[0],
          changedPointers : touches[1],
          pointerType : INPUT_TYPE_TOUCH,
          srcEvent : ev
        });
      }
    }
  });
  inherit(TouchMouseInput, Input, {
    handler : function(e, eventType, inputData) {
      /** @type {boolean} */
      var isTouch = inputData.pointerType == INPUT_TYPE_TOUCH;
      /** @type {boolean} */
      var isMouse = inputData.pointerType == INPUT_TYPE_MOUSE;
      if (isTouch) {
        /** @type {boolean} */
        this.mouse.allow = false;
      } else {
        if (isMouse && !this.mouse.allow) {
          return;
        }
      }
      if (eventType & (INPUT_END | INPUT_CANCEL)) {
        /** @type {boolean} */
        this.mouse.allow = true;
      }
      this.callback(e, eventType, inputData);
    },
    destroy : function() {
      this.touch.destroy();
      this.mouse.destroy();
    }
  });
  var PREFIXED_TOUCH_ACTION = prefixed(TEST_ELEMENT.style, "touchAction");
  /** @type {boolean} */
  var NATIVE_TOUCH_ACTION = PREFIXED_TOUCH_ACTION !== undefined;
  /** @type {string} */
  var TOUCH_ACTION_COMPUTE = "compute";
  /** @type {string} */
  var peg$c206 = "auto";
  /** @type {string} */
  var TOUCH_ACTION_MANIPULATION = "manipulation";
  /** @type {string} */
  var TOUCH_ACTION_NONE = "none";
  /** @type {string} */
  var TOUCH_ACTION_PAN_X = "pan-x";
  /** @type {string} */
  var TOUCH_ACTION_PAN_Y = "pan-y";
  TouchAction.prototype = {
    set : function(value) {
      if (value == TOUCH_ACTION_COMPUTE) {
        value = this.compute();
      }
      if (NATIVE_TOUCH_ACTION) {
        /** @type {string} */
        this.manager.element.style[PREFIXED_TOUCH_ACTION] = value;
      }
      this.actions = value.toLowerCase().trim();
    },
    update : function() {
      this.set(this.manager.options.touchAction);
    },
    compute : function() {
      /** @type {!Array} */
      var sortedFolderIds = [];
      return each(this.manager.recognizers, function(recognizer) {
        if (boolOrFn(recognizer.options.enable, [recognizer])) {
          sortedFolderIds = sortedFolderIds.concat(recognizer.getTouchAction());
        }
      }), cleanTouchActions(sortedFolderIds.join(" "));
    },
    preventDefaults : function(input) {
      if (!NATIVE_TOUCH_ACTION) {
        var srcEvent = input.srcEvent;
        var direction = input.offsetDirection;
        if (this.manager.session.prevented) {
          return void srcEvent.preventDefault();
        }
        var actions = this.actions;
        var hasNone = inStr(actions, TOUCH_ACTION_NONE);
        var hasPanY = inStr(actions, TOUCH_ACTION_PAN_Y);
        var hasPanX = inStr(actions, TOUCH_ACTION_PAN_X);
        return hasNone || hasPanY && direction & DIRECTION_HORIZONTAL || hasPanX && direction & DIRECTION_VERTICAL ? this.preventSrc(srcEvent) : void 0;
      }
    },
    preventSrc : function(srcEvent) {
      /** @type {boolean} */
      this.manager.session.prevented = true;
      srcEvent.preventDefault();
    }
  };
  /** @type {number} */
  var STATE_POSSIBLE = 1;
  /** @type {number} */
  var STATE_BEGAN = 2;
  /** @type {number} */
  var STATE_CHANGED = 4;
  /** @type {number} */
  var STATE_ENDED = 8;
  /** @type {number} */
  var STATE_RECOGNIZED = STATE_ENDED;
  /** @type {number} */
  var STATE_CANCELLED = 16;
  /** @type {number} */
  var STATE_FAILED = 32;
  Recognizer.prototype = {
    defaults : {},
    set : function(data) {
      return extend(this.options, data), this.manager && this.manager.touchAction.update(), this;
    },
    recognizeWith : function(otherRecognizer) {
      if (invokeArrayArg(otherRecognizer, "recognizeWith", this)) {
        return this;
      }
      var simultaneous = this.simultaneous;
      return simultaneous[(otherRecognizer = getRecognizerByNameIfManager(otherRecognizer, this)).id] || (simultaneous[otherRecognizer.id] = otherRecognizer, otherRecognizer.recognizeWith(this)), this;
    },
    dropRecognizeWith : function(otherRecognizer) {
      return invokeArrayArg(otherRecognizer, "dropRecognizeWith", this) ? this : (otherRecognizer = getRecognizerByNameIfManager(otherRecognizer, this), delete this.simultaneous[otherRecognizer.id], this);
    },
    requireFailure : function(otherRecognizer) {
      if (invokeArrayArg(otherRecognizer, "requireFailure", this)) {
        return this;
      }
      var requireFail = this.requireFail;
      return -1 === inArray(requireFail, otherRecognizer = getRecognizerByNameIfManager(otherRecognizer, this)) && (requireFail.push(otherRecognizer), otherRecognizer.requireFailure(this)), this;
    },
    dropRequireFailure : function(otherRecognizer) {
      if (invokeArrayArg(otherRecognizer, "dropRequireFailure", this)) {
        return this;
      }
      otherRecognizer = getRecognizerByNameIfManager(otherRecognizer, this);
      var index = inArray(this.requireFail, otherRecognizer);
      return index > -1 && this.requireFail.splice(index, 1), this;
    },
    hasRequireFailures : function() {
      return this.requireFail.length > 0;
    },
    canRecognizeWith : function(otherRecognizer) {
      return !!this.simultaneous[otherRecognizer.id];
    },
    emit : function(data) {
      /**
       * @param {string} withState
       * @return {undefined}
       */
      function emit(withState) {
        that.manager.emit(that.options.event + (withState ? f(state) : ""), data);
      }
      var that = this;
      var state = this.state;
      if (STATE_ENDED > state) {
        emit(true);
      }
      emit();
      if (state >= STATE_ENDED) {
        emit(true);
      }
    },
    tryEmit : function(input) {
      return this.canEmit() ? this.emit(input) : void(this.state = STATE_FAILED);
    },
    canEmit : function() {
      /** @type {number} */
      var i = 0;
      for (; i < this.requireFail.length;) {
        if (!(this.requireFail[i].state & (STATE_FAILED | STATE_POSSIBLE))) {
          return false;
        }
        i++;
      }
      return true;
    },
    recognize : function(inputData) {
      var inputDataClone = extend({}, inputData);
      return boolOrFn(this.options.enable, [this, inputDataClone]) ? (this.state & (STATE_RECOGNIZED | STATE_CANCELLED | STATE_FAILED) && (this.state = STATE_POSSIBLE), this.state = this.process(inputDataClone), void(this.state & (STATE_BEGAN | STATE_CHANGED | STATE_ENDED | STATE_CANCELLED) && this.tryEmit(inputDataClone))) : (this.reset(), void(this.state = STATE_FAILED));
    },
    process : function() {
    },
    getTouchAction : function() {
    },
    reset : function() {
    }
  };
  inherit(AttrRecognizer, Recognizer, {
    defaults : {
      pointers : 1
    },
    attrTest : function(input) {
      var optionPointers = this.options.pointers;
      return 0 === optionPointers || input.pointers.length === optionPointers;
    },
    process : function(input) {
      var state = this.state;
      var eventType = input.eventType;
      /** @type {number} */
      var isRecognized = state & (STATE_BEGAN | STATE_CHANGED);
      var isValid = this.attrTest(input);
      return isRecognized && (eventType & INPUT_CANCEL || !isValid) ? state | STATE_CANCELLED : isRecognized || isValid ? eventType & INPUT_END ? state | STATE_ENDED : state & STATE_BEGAN ? state | STATE_CHANGED : STATE_BEGAN : STATE_FAILED;
    }
  });
  inherit(PanRecognizer, AttrRecognizer, {
    defaults : {
      event : "pan",
      threshold : 10,
      pointers : 1,
      direction : DIRECTION_ALL
    },
    getTouchAction : function() {
      var direction = this.options.direction;
      /** @type {!Array} */
      var actions = [];
      return direction & DIRECTION_HORIZONTAL && actions.push(TOUCH_ACTION_PAN_Y), direction & DIRECTION_VERTICAL && actions.push(TOUCH_ACTION_PAN_X), actions;
    },
    directionTest : function(input) {
      var options = this.options;
      /** @type {boolean} */
      var hasMoved = true;
      var distance = input.distance;
      var direction = input.direction;
      var x = input.deltaX;
      var y = input.deltaY;
      return direction & options.direction || (options.direction & DIRECTION_HORIZONTAL ? (direction = 0 === x ? DIRECTION_NONE : 0 > x ? left : right, hasMoved = x != this.pX, distance = Math.abs(input.deltaX)) : (direction = 0 === y ? DIRECTION_NONE : 0 > y ? DIRECTION_UP : DIRECTION_DOWN, hasMoved = y != this.pY, distance = Math.abs(input.deltaY))), input.direction = direction, hasMoved && distance > options.threshold && direction & options.direction;
    },
    attrTest : function(input) {
      return AttrRecognizer.prototype.attrTest.call(this, input) && (this.state & STATE_BEGAN || !(this.state & STATE_BEGAN) && this.directionTest(input));
    },
    emit : function(input) {
      this.pX = input.deltaX;
      this.pY = input.deltaY;
      var direction = directionStr(input.direction);
      if (direction) {
        this.manager.emit(this.options.event + direction, input);
      }
      this._super.emit.call(this, input);
    }
  });
  inherit(PinchRecognizer, AttrRecognizer, {
    defaults : {
      event : "pinch",
      threshold : 0,
      pointers : 2
    },
    getTouchAction : function() {
      return [TOUCH_ACTION_NONE];
    },
    attrTest : function(input) {
      return this._super.attrTest.call(this, input) && (Math.abs(input.scale - 1) > this.options.threshold || this.state & STATE_BEGAN);
    },
    emit : function(data) {
      if (this._super.emit.call(this, data), 1 !== data.scale) {
        /** @type {string} */
        var inOut = data.scale < 1 ? "in" : "out";
        this.manager.emit(this.options.event + inOut, data);
      }
    }
  });
  inherit(PressRecognizer, Recognizer, {
    defaults : {
      event : "press",
      pointers : 1,
      time : 500,
      threshold : 5
    },
    getTouchAction : function() {
      return [peg$c206];
    },
    process : function(input) {
      var options = this.options;
      /** @type {boolean} */
      var a = input.pointers.length === options.pointers;
      /** @type {boolean} */
      var b = input.distance < options.threshold;
      /** @type {boolean} */
      var i = input.deltaTime > options.time;
      if (this._input = input, !b || !a || input.eventType & (INPUT_END | INPUT_CANCEL) && !i) {
        this.reset();
      } else {
        if (input.eventType & INPUT_START) {
          this.reset();
          this._timer = setTimeoutContext(function() {
            /** @type {number} */
            this.state = STATE_RECOGNIZED;
            this.tryEmit();
          }, options.time, this);
        } else {
          if (input.eventType & INPUT_END) {
            return STATE_RECOGNIZED;
          }
        }
      }
      return STATE_FAILED;
    },
    reset : function() {
      clearTimeout(this._timer);
    },
    emit : function(input) {
      if (this.state === STATE_RECOGNIZED) {
        if (input && input.eventType & INPUT_END) {
          this.manager.emit(this.options.event + "up", input);
        } else {
          /** @type {number} */
          this._input.timeStamp = now();
          this.manager.emit(this.options.event, this._input);
        }
      }
    }
  });
  inherit(RotateRecognizer, AttrRecognizer, {
    defaults : {
      event : "rotate",
      threshold : 0,
      pointers : 2
    },
    getTouchAction : function() {
      return [TOUCH_ACTION_NONE];
    },
    attrTest : function(input) {
      return this._super.attrTest.call(this, input) && (Math.abs(input.rotation) > this.options.threshold || this.state & STATE_BEGAN);
    }
  });
  inherit(SwipeRecognizer, AttrRecognizer, {
    defaults : {
      event : "swipe",
      threshold : 10,
      velocity : .65,
      direction : DIRECTION_HORIZONTAL | DIRECTION_VERTICAL,
      pointers : 1
    },
    getTouchAction : function() {
      return PanRecognizer.prototype.getTouchAction.call(this);
    },
    attrTest : function(input) {
      var velocity;
      var direction = this.options.direction;
      return direction & (DIRECTION_HORIZONTAL | DIRECTION_VERTICAL) ? velocity = input.velocity : direction & DIRECTION_HORIZONTAL ? velocity = input.velocityX : direction & DIRECTION_VERTICAL && (velocity = input.velocityY), this._super.attrTest.call(this, input) && direction & input.direction && input.distance > this.options.threshold && abs(velocity) > this.options.velocity && input.eventType & INPUT_END;
    },
    emit : function(input) {
      var direction = directionStr(input.direction);
      if (direction) {
        this.manager.emit(this.options.event + direction, input);
      }
      this.manager.emit(this.options.event, input);
    }
  });
  inherit(TapRecognizer, Recognizer, {
    defaults : {
      event : "tap",
      pointers : 1,
      taps : 1,
      interval : 300,
      time : 250,
      threshold : 2,
      posThreshold : 10
    },
    getTouchAction : function() {
      return [TOUCH_ACTION_MANIPULATION];
    },
    process : function(input) {
      var options = this.options;
      /** @type {boolean} */
      var a = input.pointers.length === options.pointers;
      /** @type {boolean} */
      var r = input.distance < options.threshold;
      /** @type {boolean} */
      var inPropName = input.deltaTime < options.time;
      if (this.reset(), input.eventType & INPUT_START && 0 === this.count) {
        return this.failTimeout();
      }
      if (r && inPropName && a) {
        if (input.eventType != INPUT_END) {
          return this.failTimeout();
        }
        /** @type {boolean} */
        var e = !this.pTime || input.timeStamp - this.pTime < options.interval;
        /** @type {boolean} */
        var n = !this.pCenter || getDistance(this.pCenter, input.center) < options.posThreshold;
        if (this.pTime = input.timeStamp, this.pCenter = input.center, n && e ? this.count += 1 : this.count = 1, this._input = input, 0 === this.count % options.taps) {
          return this.hasRequireFailures() ? (this._timer = setTimeoutContext(function() {
            /** @type {number} */
            this.state = STATE_RECOGNIZED;
            this.tryEmit();
          }, options.interval, this), STATE_BEGAN) : STATE_RECOGNIZED;
        }
      }
      return STATE_FAILED;
    },
    failTimeout : function() {
      return this._timer = setTimeoutContext(function() {
        /** @type {number} */
        this.state = STATE_FAILED;
      }, this.options.interval, this), STATE_FAILED;
    },
    reset : function() {
      clearTimeout(this._timer);
    },
    emit : function() {
      if (this.state == STATE_RECOGNIZED) {
        this._input.tapCount = this.count;
        this.manager.emit(this.options.event, this._input);
      }
    }
  });
  /** @type {string} */
  Hammer.VERSION = "2.0.4";
  Hammer.defaults = {
    domEvents : false,
    touchAction : TOUCH_ACTION_COMPUTE,
    enable : true,
    inputTarget : null,
    inputClass : null,
    preset : [[RotateRecognizer, {
      enable : false
    }], [PinchRecognizer, {
      enable : false
    }, ["rotate"]], [SwipeRecognizer, {
      direction : DIRECTION_HORIZONTAL
    }], [PanRecognizer, {
      direction : DIRECTION_HORIZONTAL
    }, ["swipe"]], [TapRecognizer], [TapRecognizer, {
      event : "doubletap",
      taps : 2
    }, ["tap"]], [PressRecognizer]],
    cssProps : {
      userSelect : "none",
      touchSelect : "none",
      touchCallout : "none",
      contentZooming : "none",
      userDrag : "none",
      tapHighlightColor : "rgba(0,0,0,0)"
    }
  };
  /** @type {number} */
  var STOP = 1;
  /** @type {number} */
  var FORCED_STOP = 2;
  Manager.prototype = {
    set : function(options) {
      return extend(this.options, options), options.touchAction && this.touchAction.update(), options.inputTarget && (this.input.destroy(), this.input.target = options.inputTarget, this.input.init()), this;
    },
    stop : function(force) {
      /** @type {number} */
      this.session.stopped = force ? FORCED_STOP : STOP;
    },
    recognize : function(inputData) {
      var session = this.session;
      if (!session.stopped) {
        this.touchAction.preventDefaults(inputData);
        var recognizer;
        var recognizers = this.recognizers;
        var curRecognizer = session.curRecognizer;
        if (!curRecognizer || curRecognizer && curRecognizer.state & STATE_RECOGNIZED) {
          /** @type {null} */
          curRecognizer = session.curRecognizer = null;
        }
        /** @type {number} */
        var i = 0;
        for (; i < recognizers.length;) {
          recognizer = recognizers[i];
          if (session.stopped === FORCED_STOP || curRecognizer && recognizer != curRecognizer && !recognizer.canRecognizeWith(curRecognizer)) {
            recognizer.reset();
          } else {
            recognizer.recognize(inputData);
          }
          if (!curRecognizer && recognizer.state & (STATE_BEGAN | STATE_CHANGED | STATE_ENDED)) {
            curRecognizer = session.curRecognizer = recognizer;
          }
          i++;
        }
      }
    },
    get : function(recognizer) {
      if (recognizer instanceof Recognizer) {
        return recognizer;
      }
      var recognizers = this.recognizers;
      /** @type {number} */
      var i = 0;
      for (; i < recognizers.length; i++) {
        if (recognizers[i].options.event == recognizer) {
          return recognizers[i];
        }
      }
      return null;
    },
    add : function(obj) {
      if (invokeArrayArg(obj, "add", this)) {
        return this;
      }
      var existing = this.get(obj.options.event);
      return existing && this.remove(existing), this.recognizers.push(obj), obj.manager = this, this.touchAction.update(), obj;
    },
    remove : function(recognizer) {
      if (invokeArrayArg(recognizer, "remove", this)) {
        return this;
      }
      var recognizers = this.recognizers;
      return recognizer = this.get(recognizer), recognizers.splice(inArray(recognizers, recognizer), 1), this.touchAction.update(), this;
    },
    on : function(name, listener) {
      var handlers = this.handlers;
      return each($(name), function(name) {
        handlers[name] = handlers[name] || [];
        handlers[name].push(listener);
      }), this;
    },
    off : function(name, handler) {
      var handlers = this.handlers;
      return each($(name), function(event) {
        if (handler) {
          handlers[event].splice(inArray(handlers[event], handler), 1);
        } else {
          delete handlers[event];
        }
      }), this;
    },
    emit : function(event, data) {
      if (this.options.domEvents) {
        triggerDomEvent(event, data);
      }
      var urls = this.handlers[event] && this.handlers[event].slice();
      if (urls && urls.length) {
        /** @type {string} */
        data.type = event;
        /**
         * @return {undefined}
         */
        data.preventDefault = function() {
          data.srcEvent.preventDefault();
        };
        /** @type {number} */
        var i = 0;
        for (; i < urls.length;) {
          urls[i](data);
          i++;
        }
      }
    },
    destroy : function() {
      if (this.element) {
        toggleCssProps(this, false);
      }
      this.handlers = {};
      this.session = {};
      this.input.destroy();
      /** @type {null} */
      this.element = null;
    }
  };
  extend(Hammer, {
    INPUT_START : INPUT_START,
    INPUT_MOVE : INPUT_MOVE,
    INPUT_END : INPUT_END,
    INPUT_CANCEL : INPUT_CANCEL,
    STATE_POSSIBLE : STATE_POSSIBLE,
    STATE_BEGAN : STATE_BEGAN,
    STATE_CHANGED : STATE_CHANGED,
    STATE_ENDED : STATE_ENDED,
    STATE_RECOGNIZED : STATE_RECOGNIZED,
    STATE_CANCELLED : STATE_CANCELLED,
    STATE_FAILED : STATE_FAILED,
    DIRECTION_NONE : DIRECTION_NONE,
    DIRECTION_LEFT : left,
    DIRECTION_RIGHT : right,
    DIRECTION_UP : DIRECTION_UP,
    DIRECTION_DOWN : DIRECTION_DOWN,
    DIRECTION_HORIZONTAL : DIRECTION_HORIZONTAL,
    DIRECTION_VERTICAL : DIRECTION_VERTICAL,
    DIRECTION_ALL : DIRECTION_ALL,
    Manager : Manager,
    Input : Input,
    TouchAction : TouchAction,
    TouchInput : TouchInput,
    MouseInput : MouseInput,
    PointerEventInput : PointerEventInput,
    TouchMouseInput : TouchMouseInput,
    SingleTouchInput : SingleTouchInput,
    Recognizer : Recognizer,
    AttrRecognizer : AttrRecognizer,
    Tap : TapRecognizer,
    Pan : PanRecognizer,
    Swipe : SwipeRecognizer,
    Pinch : PinchRecognizer,
    Rotate : RotateRecognizer,
    Press : PressRecognizer,
    on : addEventListeners,
    off : removeEventListeners,
    each : each,
    merge : merge,
    extend : extend,
    inherit : inherit,
    bindFn : bindFn,
    prefixed : prefixed
  });
  if (typeof define == TYPE_FUNCTION && define.amd) {
    define(function() {
      return Hammer;
    });
  } else {
    if ("undefined" != typeof module && module.exports) {
      /** @type {function(string, !Object): ?} */
      module.exports = Hammer;
    } else {
      /** @type {function(string, !Object): ?} */
      window[exportName] = Hammer;
    }
  }
}(window, document, "Hammer"), function(factory) {
  if ("function" == typeof define && define.amd) {
    define(["jquery", "hammerjs"], factory);
  } else {
    if ("object" == typeof exports) {
      factory(require("jquery"), require("hammerjs"));
    } else {
      factory(jQuery, Hammer);
    }
  }
}(function($, Hammer) {
  /**
   * @param {?} el
   * @param {!Function} options
   * @return {undefined}
   */
  function hammerify(el, options) {
    var $el = $(el);
    if (!$el.data("hammer")) {
      $el.data("hammer", new Hammer($el[0], options));
    }
  }
  var originalEmit;
  /**
   * @param {!Function} options
   * @return {?}
   */
  $.fn.hammer = function(options) {
    return this.each(function() {
      hammerify(this, options);
    });
  };
  /** @type {function(string, !Object): undefined} */
  Hammer.Manager.prototype.emit = (originalEmit = Hammer.Manager.prototype.emit, function(type, data) {
    originalEmit.call(this, type, data);
    $(this.element).trigger({
      type : type,
      gesture : data
    });
  });
}), function(factory) {
  if ("function" == typeof define && define.amd) {
    define([], factory);
  } else {
    if ("object" == typeof exports) {
      module.exports = factory();
    } else {
      window.noUiSlider = factory();
    }
  }
}(function() {
  /**
   * @param {!Array} array
   * @return {?}
   */
  function unique(array) {
    return array.filter(function(ballNumber) {
      return !this[ballNumber] && (this[ballNumber] = true);
    }, {});
  }
  /**
   * @param {number} index
   * @param {number} num
   * @return {?}
   */
  function closest(index, num) {
    return Math.round(index / num) * num;
  }
  /**
   * @param {!Object} elem
   * @return {?}
   */
  function offset(elem) {
    var rect = elem.getBoundingClientRect();
    var doc = elem.ownerDocument.documentElement;
    var pageOffset = getPageOffset();
    return /webkit.*Chrome.*Mobile/i.test(navigator.userAgent) && (pageOffset.x = 0), {
      top : rect.top + pageOffset.y - doc.clientTop,
      left : rect.left + pageOffset.x - doc.clientLeft
    };
  }
  /**
   * @param {!Object} a
   * @return {?}
   */
  function isNumeric(a) {
    return "number" == typeof a && !isNaN(a) && isFinite(a);
  }
  /**
   * @param {number} number
   * @return {?}
   */
  function accurateNumber(number) {
    /** @type {number} */
    var power = Math.pow(10, 7);
    return Number((Math.round(number * power) / power).toFixed(7));
  }
  /**
   * @param {undefined} element
   * @param {string} className
   * @param {number} duration
   * @return {undefined}
   */
  function addClassFor(element, className, duration) {
    addClass(element, className);
    setTimeout(function() {
      removeClass(element, className);
    }, duration);
  }
  /**
   * @param {number} n
   * @return {?}
   */
  function limit(n) {
    return Math.max(Math.min(n, 100), 0);
  }
  /**
   * @param {string} a
   * @return {?}
   */
  function asArray(a) {
    return Array.isArray(a) ? a : [a];
  }
  /**
   * @param {string} numStr
   * @return {?}
   */
  function countDecimals(numStr) {
    var ip_segments = numStr.split(".");
    return ip_segments.length > 1 ? ip_segments[1].length : 0;
  }
  /**
   * @param {!Element} element
   * @param {string} className
   * @return {undefined}
   */
  function addClass(element, className) {
    if (element.classList) {
      element.classList.add(className);
    } else {
      element.className += " " + className;
    }
  }
  /**
   * @param {!Element} target
   * @param {string} className
   * @return {undefined}
   */
  function removeClass(target, className) {
    if (target.classList) {
      target.classList.remove(className);
    } else {
      target.className = target.className.replace(new RegExp("(^|\\b)" + className.split(" ").join("|") + "(\\b|$)", "gi"), " ");
    }
  }
  /**
   * @param {!Element} target
   * @param {string} selector
   * @return {undefined}
   */
  function hasClass(target, selector) {
    if (target.classList) {
      target.classList.contains(selector);
    } else {
      (new RegExp("(^| )" + selector + "( |$)", "gi")).test(target.className);
    }
  }
  /**
   * @return {?}
   */
  function getPageOffset() {
    /** @type {boolean} */
    var supportPageOffset = void 0 !== window.pageXOffset;
    /** @type {boolean} */
    var isCSS1Compat = "CSS1Compat" === (document.compatMode || "");
    return {
      x : supportPageOffset ? window.pageXOffset : isCSS1Compat ? document.documentElement.scrollLeft : document.body.scrollLeft,
      y : supportPageOffset ? window.pageYOffset : isCSS1Compat ? document.documentElement.scrollTop : document.body.scrollTop
    };
  }
  /**
   * @param {(Object|number)} userID1
   * @return {?}
   */
  function addCssPrefix(userID1) {
    return function(_) {
      return userID1 + _;
    };
  }
  /**
   * @param {!Object} pa
   * @param {!Object} pb
   * @return {?}
   */
  function subRangeRatio(pa, pb) {
    return 100 / (pb - pa);
  }
  /**
   * @param {!Object} range
   * @param {number} value
   * @return {?}
   */
  function fromPercentage(range, value) {
    return 100 * value / (range[1] - range[0]);
  }
  /**
   * @param {!Object} range
   * @param {number} value
   * @return {?}
   */
  function toPercentage(range, value) {
    return fromPercentage(range, range[0] < 0 ? value + Math.abs(range[0]) : value - range[0]);
  }
  /**
   * @param {!Object} range
   * @param {number} value
   * @return {?}
   */
  function isPercentage(range, value) {
    return value * (range[1] - range[0]) / 100 + range[0];
  }
  /**
   * @param {number} value
   * @param {!Object} arr
   * @return {?}
   */
  function getJ(value, arr) {
    /** @type {number} */
    var j = 1;
    for (; value >= arr[j];) {
      /** @type {number} */
      j = j + 1;
    }
    return j;
  }
  /**
   * @param {!Array} xVal
   * @param {!Object} xPct
   * @param {number} value
   * @return {?}
   */
  function toStepping(xVal, xPct, value) {
    if (value >= xVal.slice(-1)[0]) {
      return 100;
    }
    var va;
    var vb;
    var pa;
    var pb;
    var j = getJ(value, xVal);
    return va = xVal[j - 1], vb = xVal[j], pa = xPct[j - 1], pb = xPct[j], pa + toPercentage([va, vb], value) / subRangeRatio(pa, pb);
  }
  /**
   * @param {string} xVal
   * @param {!Object} xPct
   * @param {number} value
   * @return {?}
   */
  function fromStepping(xVal, xPct, value) {
    if (value >= 100) {
      return xVal.slice(-1)[0];
    }
    var pa;
    var j = getJ(value, xPct);
    return isPercentage([xVal[j - 1], xVal[j]], (value - (pa = xPct[j - 1])) * subRangeRatio(pa, xPct[j]));
  }
  /**
   * @param {!Object} xPct
   * @param {!Object} xSteps
   * @param {!Array} snap
   * @param {number} value
   * @return {?}
   */
  function getStep(xPct, xSteps, snap, value) {
    if (100 === value) {
      return value;
    }
    var step;
    var a;
    var j = getJ(value, xPct);
    return snap ? value - (step = xPct[j - 1]) > ((a = xPct[j]) - step) / 2 ? a : step : xSteps[j - 1] ? xPct[j - 1] + closest(value - xPct[j - 1], xSteps[j - 1]) : value;
  }
  /**
   * @param {string} index
   * @param {!Object} value
   * @param {?} that
   * @return {undefined}
   */
  function handleEntryPoint(index, value, that) {
    var key;
    if ("number" == typeof value && (value = [value]), "[object Array]" !== Object.prototype.toString.call(value)) {
      throw new Error("noUiSlider: 'range' contains invalid value.");
    }
    if (!isNumeric(key = "min" === index ? 0 : "max" === index ? 100 : parseFloat(index)) || !isNumeric(value[0])) {
      throw new Error("noUiSlider: 'range' value isn't numeric.");
    }
    that.xPct.push(key);
    that.xVal.push(value[0]);
    if (key) {
      that.xSteps.push(!isNaN(value[1]) && value[1]);
    } else {
      if (!isNaN(value[1])) {
        that.xSteps[0] = value[1];
      }
    }
  }
  /**
   * @param {!Object} i
   * @param {undefined} n
   * @param {?} that
   * @return {?}
   */
  function handleStepPoint(i, n, that) {
    return !n || void(that.xSteps[i] = fromPercentage([that.xVal[i], that.xVal[i + 1]], n) / subRangeRatio(that.xPct[i], that.xPct[i + 1]));
  }
  /**
   * @param {(Object|string)} entry
   * @param {string} snap
   * @param {number} direction
   * @param {string} singleStep
   * @return {undefined}
   */
  function Spectrum(entry, snap, direction, singleStep) {
    /** @type {!Array} */
    this.xPct = [];
    /** @type {!Array} */
    this.xVal = [];
    /** @type {!Array} */
    this.xSteps = [singleStep || false];
    /** @type {!Array} */
    this.xNumSteps = [false];
    /** @type {string} */
    this.snap = snap;
    /** @type {number} */
    this.direction = direction;
    var index;
    /** @type {!Array} */
    var ordered = [];
    for (index in entry) {
      if (entry.hasOwnProperty(index)) {
        ordered.push([entry[index], index]);
      }
    }
    if (ordered.length && "object" == typeof ordered[0][0]) {
      ordered.sort(function(canCreateDiscussions, isSlidingUp) {
        return canCreateDiscussions[0][0] - isSlidingUp[0][0];
      });
    } else {
      ordered.sort(function(subtractor, subtractee) {
        return subtractor[0] - subtractee[0];
      });
    }
    /** @type {number} */
    index = 0;
    for (; index < ordered.length; index++) {
      handleEntryPoint(ordered[index][1], ordered[index][0], this);
    }
    /** @type {!Array<?>} */
    this.xNumSteps = this.xSteps.slice(0);
    /** @type {number} */
    index = 0;
    for (; index < this.xNumSteps.length; index++) {
      handleStepPoint(index, this.xNumSteps[index], this);
    }
  }
  /**
   * @param {?} parsed
   * @param {!Object} entry
   * @return {undefined}
   */
  function testStep(parsed, entry) {
    if (!isNumeric(entry)) {
      throw new Error("noUiSlider: 'step' is not numeric.");
    }
    /** @type {!Object} */
    parsed.singleStep = entry;
  }
  /**
   * @param {!Object} parsed
   * @param {!Object} entry
   * @return {undefined}
   */
  function testRange(parsed, entry) {
    if ("object" != typeof entry || Array.isArray(entry)) {
      throw new Error("noUiSlider: 'range' is not an object.");
    }
    if (void 0 === entry.min || void 0 === entry.max) {
      throw new Error("noUiSlider: Missing 'min' or 'max' in 'range'.");
    }
    parsed.spectrum = new Spectrum(entry, parsed.snap, parsed.dir, parsed.singleStep);
  }
  /**
   * @param {!Object} parsed
   * @param {string} entry
   * @return {undefined}
   */
  function testStart(parsed, entry) {
    if (entry = asArray(entry), !Array.isArray(entry) || !entry.length || entry.length > 2) {
      throw new Error("noUiSlider: 'start' option is incorrect.");
    }
    parsed.handles = entry.length;
    /** @type {string} */
    parsed.start = entry;
  }
  /**
   * @param {?} o
   * @param {string} t
   * @return {undefined}
   */
  function testSnap(o, t) {
    if (o.snap = t, "boolean" != typeof t) {
      throw new Error("noUiSlider: 'snap' option must be a boolean.");
    }
  }
  /**
   * @param {!Object} parsed
   * @param {boolean} entry
   * @return {undefined}
   */
  function testAnimate(parsed, entry) {
    if (parsed.animate = entry, "boolean" != typeof entry) {
      throw new Error("noUiSlider: 'animate' option must be a boolean.");
    }
  }
  /**
   * @param {!Object} parsed
   * @param {?} lower
   * @return {undefined}
   */
  function testConnect(parsed, lower) {
    if ("lower" === lower && 1 === parsed.handles) {
      /** @type {number} */
      parsed.connect = 1;
    } else {
      if ("upper" === lower && 1 === parsed.handles) {
        /** @type {number} */
        parsed.connect = 2;
      } else {
        if (true === lower && 2 === parsed.handles) {
          /** @type {number} */
          parsed.connect = 3;
        } else {
          if (false !== lower) {
            throw new Error("noUiSlider: 'connect' option doesn't match handle count.");
          }
          /** @type {number} */
          parsed.connect = 0;
        }
      }
    }
  }
  /**
   * @param {?} parsed
   * @param {?} entry
   * @return {undefined}
   */
  function testOrientation(parsed, entry) {
    switch(entry) {
      case "horizontal":
        /** @type {number} */
        parsed.ort = 0;
        break;
      case "vertical":
        /** @type {number} */
        parsed.ort = 1;
        break;
      default:
        throw new Error("noUiSlider: 'orientation' option is invalid.");
    }
  }
  /**
   * @param {!Object} parsed
   * @param {undefined} entry
   * @return {undefined}
   */
  function testMargin(parsed, entry) {
    if (!isNumeric(entry)) {
      throw new Error("noUiSlider: 'margin' option must be numeric.");
    }
    if (parsed.margin = parsed.spectrum.getMargin(entry), !parsed.margin) {
      throw new Error("noUiSlider: 'margin' option is only supported on linear sliders.");
    }
  }
  /**
   * @param {!Object} parsed
   * @param {undefined} entry
   * @return {undefined}
   */
  function testLimit(parsed, entry) {
    if (!isNumeric(entry)) {
      throw new Error("noUiSlider: 'limit' option must be numeric.");
    }
    if (parsed.limit = parsed.spectrum.getMargin(entry), !parsed.limit) {
      throw new Error("noUiSlider: 'limit' option is only supported on linear sliders.");
    }
  }
  /**
   * @param {!Object} parsed
   * @param {?} entry
   * @return {undefined}
   */
  function testDirection(parsed, entry) {
    switch(entry) {
      case "ltr":
        /** @type {number} */
        parsed.dir = 0;
        break;
      case "rtl":
        /** @type {number} */
        parsed.dir = 1;
        parsed.connect = [0, 2, 1, 3][parsed.connect];
        break;
      default:
        throw new Error("noUiSlider: 'direction' option was not recognized.");
    }
  }
  /**
   * @param {!Object} parsed
   * @param {string} entry
   * @return {undefined}
   */
  function testBehaviour(parsed, entry) {
    if ("string" != typeof entry) {
      throw new Error("noUiSlider: 'behaviour' must be a string containing options.");
    }
    /** @type {boolean} */
    var tap = entry.indexOf("tap") >= 0;
    /** @type {boolean} */
    var drag = entry.indexOf("drag") >= 0;
    /** @type {boolean} */
    var fixed = entry.indexOf("fixed") >= 0;
    /** @type {boolean} */
    var snap = entry.indexOf("snap") >= 0;
    if (drag && !parsed.connect) {
      throw new Error("noUiSlider: 'drag' behaviour must be used with 'connect': true.");
    }
    parsed.events = {
      tap : tap || snap,
      drag : drag,
      fixed : fixed,
      snap : snap
    };
  }
  /**
   * @param {!Object} options
   * @param {string} config
   * @return {undefined}
   */
  function draw(options, config) {
    if (true === config && (options.tooltips = true), config && config.format) {
      if ("function" != typeof config.format) {
        throw new Error("noUiSlider: 'tooltips.format' must be an object.");
      }
      options.tooltips = {
        format : config.format
      };
    }
  }
  /**
   * @param {!Object} expression
   * @param {string} value
   * @return {?}
   */
  function render(expression, value) {
    if (expression.format = value, "function" == typeof value.to && "function" == typeof value.from) {
      return true;
    }
    throw new Error("noUiSlider: 'format' requires 'to' and 'from' methods.");
  }
  /**
   * @param {!Object} parsed
   * @param {string} entry
   * @return {undefined}
   */
  function testCssClasses(parsed, entry) {
    if (void 0 !== entry && "string" != typeof entry) {
      throw new Error("noUiSlider: 'cssPrefix' must be a string.");
    }
    /** @type {string} */
    parsed.cssPrefix = entry;
  }
  /**
   * @param {!Object} options
   * @return {?}
   */
  function testOptions(options) {
    var tests;
    var parsed = {
      margin : 0,
      limit : 0,
      animate : true,
      format : defaultFormatter
    };
    tests = {
      step : {
        r : false,
        t : testStep
      },
      start : {
        r : true,
        t : testStart
      },
      connect : {
        r : true,
        t : testConnect
      },
      direction : {
        r : true,
        t : testDirection
      },
      snap : {
        r : false,
        t : testSnap
      },
      animate : {
        r : false,
        t : testAnimate
      },
      range : {
        r : true,
        t : testRange
      },
      orientation : {
        r : false,
        t : testOrientation
      },
      margin : {
        r : false,
        t : testMargin
      },
      limit : {
        r : false,
        t : testLimit
      },
      behaviour : {
        r : true,
        t : testBehaviour
      },
      format : {
        r : false,
        t : render
      },
      tooltips : {
        r : false,
        t : draw
      },
      cssPrefix : {
        r : false,
        t : testCssClasses
      }
    };
    var defaults = {
      connect : false,
      direction : "ltr",
      behaviour : "tap",
      orientation : "horizontal"
    };
    return Object.keys(defaults).forEach(function(i) {
      if (void 0 === options[i]) {
        options[i] = defaults[i];
      }
    }), Object.keys(tests).forEach(function(i) {
      var test = tests[i];
      if (void 0 === options[i]) {
        if (test.r) {
          throw new Error("noUiSlider: '" + i + "' is required.");
        }
        return true;
      }
      test.t(parsed, options[i]);
    }), parsed.pips = options.pips, parsed.style = parsed.ort ? "top" : "left", parsed;
  }
  /**
   * @param {!Node} target
   * @param {!Object} options
   * @return {?}
   */
  function closure(target, options) {
    /**
     * @param {number} a
     * @param {!Object} b
     * @param {string} callback
     * @return {?}
     */
    function getPositions(a, b, callback) {
      var d = a + b[0];
      var c = a + b[1];
      return callback ? (0 > d && (c = c + Math.abs(d)), c > 100 && (d = d - (c - 100)), [limit(d), limit(c)]) : [d, c];
    }
    /**
     * @param {!Object} e
     * @param {number} pageOffset
     * @return {?}
     */
    function fixEvent(e, pageOffset) {
      e.preventDefault();
      var x;
      var y;
      /** @type {boolean} */
      var r = 0 === e.type.indexOf("touch");
      /** @type {boolean} */
      var mouse = 0 === e.type.indexOf("mouse");
      /** @type {boolean} */
      var pointer = 0 === e.type.indexOf("pointer");
      /** @type {!Object} */
      var event = e;
      return 0 === e.type.indexOf("MSPointer") && (pointer = true), r && (x = e.changedTouches[0].pageX, y = e.changedTouches[0].pageY), pageOffset = pageOffset || getPageOffset(), (mouse || pointer) && (x = e.clientX + pageOffset.x, y = e.clientY + pageOffset.y), event.pageOffset = pageOffset, event.points = [x, y], event.cursor = mouse || pointer, event;
    }
    /**
     * @param {boolean} options
     * @param {number} index
     * @return {?}
     */
    function addHandle(options, index) {
      /** @type {!Element} */
      var a = document.createElement("div");
      /** @type {!Element} */
      var n = document.createElement("div");
      /** @type {!Array} */
      var additions = ["-lower", "-upper"];
      return options && additions.reverse(), addClass(n, cssClasses[3]), addClass(n, cssClasses[3] + additions[index]), addClass(a, cssClasses[2]), a.appendChild(n), a;
    }
    /**
     * @param {?} connect
     * @param {undefined} target
     * @param {!Object} handles
     * @return {undefined}
     */
    function addConnection(connect, target, handles) {
      switch(connect) {
        case 1:
          addClass(target, cssClasses[7]);
          addClass(handles[0], cssClasses[6]);
          break;
        case 3:
          addClass(handles[1], cssClasses[6]);
        case 2:
          addClass(handles[0], cssClasses[7]);
        case 0:
          addClass(target, cssClasses[6]);
      }
    }
    /**
     * @param {(number|string)} direction
     * @param {boolean} options
     * @param {!Object} base
     * @return {?}
     */
    function addHandles(direction, options, base) {
      var index;
      /** @type {!Array} */
      var handles = [];
      /** @type {number} */
      index = 0;
      for (; direction > index; index = index + 1) {
        handles.push(base.appendChild(addHandle(options, index)));
      }
      return handles;
    }
    /**
     * @param {number} orientation
     * @param {number} direction
     * @param {!Element} target
     * @return {?}
     */
    function addSlider(orientation, direction, target) {
      addClass(target, cssClasses[0]);
      addClass(target, cssClasses[8 + orientation]);
      addClass(target, cssClasses[4 + direction]);
      /** @type {!Element} */
      var n = document.createElement("div");
      return addClass(n, cssClasses[1]), target.appendChild(n), n;
    }
    /**
     * @param {?} formattedValue
     * @return {?}
     */
    function defaultFormatTooltipValue(formattedValue) {
      return formattedValue;
    }
    /**
     * @param {!Node} dom
     * @return {?}
     */
    function addTooltip(dom) {
      /** @type {!Element} */
      var element = document.createElement("div");
      return element.className = cssClasses[18], dom.firstChild.appendChild(element);
    }
    /**
     * @param {!Object} tooltipsOptions
     * @return {undefined}
     */
    function tooltips(tooltipsOptions) {
      var formatTooltipValue = tooltipsOptions.format ? tooltipsOptions.format : defaultFormatTooltipValue;
      var tips = scope_Handles.map(addTooltip);
      bindEvent("update", function(formattedValues, handleId, rawValues) {
        tips[handleId].innerHTML = formatTooltipValue(formattedValues[handleId], rawValues[handleId]);
      });
    }
    /**
     * @param {string} undefined
     * @param {string} opts
     * @param {number} stepped
     * @return {?}
     */
    function getGroup(undefined, opts, stepped) {
      if ("range" === undefined || "steps" === undefined) {
        return scope_Spectrum.xVal;
      }
      if ("count" === undefined) {
        var height;
        /** @type {number} */
        var lh = 100 / (opts - 1);
        /** @type {number} */
        var lNum = 0;
        /** @type {!Array} */
        opts = [];
        for (; (height = lNum++ * lh) <= 100;) {
          opts.push(height);
        }
        /** @type {string} */
        undefined = "positions";
      }
      return "positions" === undefined ? opts.map(function(value) {
        return scope_Spectrum.fromStepping(stepped ? scope_Spectrum.getStep(value) : value);
      }) : "values" === undefined ? stepped ? opts.map(function(value) {
        return scope_Spectrum.fromStepping(scope_Spectrum.getStep(scope_Spectrum.toStepping(value)));
      }) : opts : void 0;
    }
    /**
     * @param {number} density
     * @param {string} mode
     * @param {!Array} group
     * @return {?}
     */
    function generateSpread(density, mode, group) {
      /**
       * @param {number} value
       * @param {number} increment
       * @return {?}
       */
      function round(value, increment) {
        return (value + increment).toFixed(7) / 1;
      }
      var originalSpectrumDirection = scope_Spectrum.direction;
      var indexes = {};
      var event = scope_Spectrum.xVal[0];
      var lastInRange = scope_Spectrum.xVal[scope_Spectrum.xVal.length - 1];
      /** @type {boolean} */
      var iMachine = false;
      /** @type {boolean} */
      var inclusive = false;
      /** @type {number} */
      var j = 0;
      return scope_Spectrum.direction = 0, (group = unique(group.slice().sort(function(b, a) {
        return b - a;
      })))[0] !== event && (group.unshift(event), iMachine = true), group[group.length - 1] !== lastInRange && (group.push(lastInRange), inclusive = true), group.forEach(function(margin, index) {
        var interval;
        var value;
        var _zAdjPortWidth;
        var o;
        var widthDays;
        var type;
        var steps;
        var _xpos;
        var cellColumnWidth;
        /** @type {!Object} */
        var min = margin;
        var max = group[index + 1];
        if ("steps" === mode && (interval = scope_Spectrum.xNumSteps[index]), interval || (interval = max - min), false !== min && void 0 !== max) {
          value = min;
          for (; max >= value; value = round(value, interval)) {
            /** @type {number} */
            steps = (widthDays = (o = scope_Spectrum.toStepping(value)) - j) / density;
            /** @type {number} */
            cellColumnWidth = widthDays / (_xpos = Math.round(steps));
            /** @type {number} */
            _zAdjPortWidth = 1;
            for (; _xpos >= _zAdjPortWidth; _zAdjPortWidth = _zAdjPortWidth + 1) {
              /** @type {!Array} */
              indexes[(j + _zAdjPortWidth * cellColumnWidth).toFixed(5)] = ["x", 0];
            }
            /** @type {number} */
            type = group.indexOf(value) > -1 ? 1 : "steps" === mode ? 2 : 0;
            if (!index && iMachine) {
              /** @type {number} */
              type = 0;
            }
            if (!(value === max && inclusive)) {
              /** @type {!Array} */
              indexes[o.toFixed(5)] = [value, type];
            }
            j = o;
          }
        }
      }), scope_Spectrum.direction = originalSpectrumDirection, indexes;
    }
    /**
     * @param {!Object} spread
     * @param {?} filterFunc
     * @param {!Object} formatter
     * @return {?}
     */
    function addMarking(spread, filterFunc, formatter) {
      /**
       * @param {number} type
       * @return {?}
       */
      function getSize(type) {
        return ["-normal", "-large", "-sub"][type];
      }
      /**
       * @param {number} name
       * @param {string} source
       * @param {!Object} values
       * @return {?}
       */
      function getTags(name, source, values) {
        return 'class="' + source + " " + source + "-" + style + " " + source + getSize(values[1]) + '" style="' + options.style + ": " + name + '%"';
      }
      /**
       * @param {number} offset
       * @param {!Object} values
       * @return {undefined}
       */
      function addSpread(offset, values) {
        if (scope_Spectrum.direction) {
          /** @type {number} */
          offset = 100 - offset;
        }
        values[1] = values[1] && filterFunc ? filterFunc(values[0], values[1]) : values[1];
        wrapEl.innerHTML += "<div " + getTags(offset, "noUi-marker", values) + "></div>";
        if (values[1]) {
          wrapEl.innerHTML += "<div " + getTags(offset, "noUi-value", values) + ">" + formatter.to(values[0]) + "</div>";
        }
      }
      var style = ["horizontal", "vertical"][options.ort];
      /** @type {!Element} */
      var wrapEl = document.createElement("div");
      return addClass(wrapEl, "noUi-pips"), addClass(wrapEl, "noUi-pips-" + style), Object.keys(spread).forEach(function(a) {
        addSpread(a, spread[a]);
      }), wrapEl;
    }
    /**
     * @param {!Object} grid
     * @return {?}
     */
    function pips(grid) {
      var mode = grid.mode;
      var density = grid.density || 1;
      var filter = grid.filter || false;
      var spread = generateSpread(density, mode, getGroup(mode, grid.values || false, grid.stepped || false));
      var format = grid.format || {
        to : Math.round
      };
      return scope_Target.appendChild(addMarking(spread, filter, format));
    }
    /**
     * @return {?}
     */
    function baseSize() {
      return scope_Base["offset" + ["Width", "Height"][options.ort]];
    }
    /**
     * @param {string} type
     * @param {number} handleNumber
     * @return {undefined}
     */
    function fireEvent(type, handleNumber) {
      if (void 0 !== handleNumber && 1 !== options.handles) {
        /** @type {number} */
        handleNumber = Math.abs(handleNumber - options.dir);
      }
      Object.keys(def).forEach(function(serviceName) {
        /** @type {string} */
        var TYPE_CLIENT = serviceName.split(".")[0];
        if (type === TYPE_CLIENT) {
          def[serviceName].forEach(function(callback) {
            callback(asArray(valueGet()), handleNumber, inSliderOrder(Array.prototype.slice.call(scope_Values)));
          });
        }
      });
    }
    /**
     * @param {!Object} values
     * @return {?}
     */
    function inSliderOrder(values) {
      return 1 === values.length ? values[0] : options.dir ? values.reverse() : values;
    }
    /**
     * @param {string} data
     * @param {!Node} element
     * @param {!Function} callback
     * @param {?} event
     * @return {?}
     */
    function attach(data, element, callback, event) {
      /**
       * @param {!Object} e
       * @return {?}
       */
      var method = function(e) {
        return !scope_Target.hasAttribute("disabled") && (!hasClass(scope_Target, cssClasses[14]) && (e = fixEvent(e, event.pageOffset), !(data === node.start && void 0 !== e.buttons && e.buttons > 1) && (e.calcPoint = e.points[options.ort], void callback(e, event))));
      };
      /** @type {!Array} */
      var ret = [];
      return data.split(" ").forEach(function(name) {
        element.addEventListener(name, method, false);
        ret.push([name, method]);
      }), ret;
    }
    /**
     * @param {!Object} event
     * @param {!Object} data
     * @return {?}
     */
    function move(event, data) {
      if (0 === event.buttons && 0 === event.which && 0 !== data.buttonsProperty) {
        return end(event, data);
      }
      var positions;
      var i;
      var handles = data.handles || scope_Handles;
      /** @type {boolean} */
      var state = false;
      /** @type {number} */
      var proposal = 100 * (event.calcPoint - data.start) / data.baseSize;
      /** @type {number} */
      var handleNumber = handles[0] === scope_Handles[0] ? 0 : 1;
      if (positions = getPositions(proposal, data.positions, handles.length > 1), state = setHandle(handles[0], positions[handleNumber], 1 === handles.length), handles.length > 1) {
        if (state = setHandle(handles[1], positions[handleNumber ? 0 : 1], false) || state) {
          /** @type {number} */
          i = 0;
          for (; i < data.handles.length; i++) {
            fireEvent("slide", i);
          }
        }
      } else {
        if (state) {
          fireEvent("slide", handleNumber);
        }
      }
    }
    /**
     * @param {!Object} event
     * @param {!Object} data
     * @return {undefined}
     */
    function end(event, data) {
      var div = scope_Base.querySelector("." + cssClasses[15]);
      /** @type {number} */
      var i = data.handles[0] === scope_Handles[0] ? 0 : 1;
      if (null !== div) {
        removeClass(div, cssClasses[15]);
      }
      if (event.cursor) {
        /** @type {string} */
        document.body.style.cursor = "";
        document.body.removeEventListener("selectstart", document.body.noUiListener);
      }
      /** @type {!Element} */
      var d = document.documentElement;
      d.noUiListeners.forEach(function(c) {
        d.removeEventListener(c[0], c[1]);
      });
      removeClass(scope_Target, cssClasses[12]);
      fireEvent("set", i);
      fireEvent("change", i);
    }
    /**
     * @param {!Object} event
     * @param {?} data
     * @return {?}
     */
    function start(event, data) {
      /** @type {!Element} */
      var d = document.documentElement;
      if (1 === data.handles.length && (addClass(data.handles[0].children[0], cssClasses[15]), data.handles[0].hasAttribute("disabled"))) {
        return false;
      }
      event.stopPropagation();
      var moveEvent = attach(node.move, d, move, {
        start : event.calcPoint,
        baseSize : baseSize(),
        pageOffset : event.pageOffset,
        handles : data.handles,
        buttonsProperty : event.buttons,
        positions : [scope_Locations[0], scope_Locations[scope_Handles.length - 1]]
      });
      var endEvent = attach(node.end, d, end, {
        handles : data.handles
      });
      if (d.noUiListeners = moveEvent.concat(endEvent), event.cursor) {
        /** @type {string} */
        document.body.style.cursor = getComputedStyle(event.target).cursor;
        if (scope_Handles.length > 1) {
          addClass(scope_Target, cssClasses[12]);
        }
        /**
         * @return {?}
         */
        var f = function() {
          return false;
        };
        /** @type {function(): ?} */
        document.body.noUiListener = f;
        document.body.addEventListener("selectstart", f, false);
      }
    }
    /**
     * @param {!Object} event
     * @return {?}
     */
    function tap(event) {
      var handleNumber;
      var proposal;
      var location = event.calcPoint;
      /** @type {number} */
      var top = 0;
      return event.stopPropagation(), scope_Handles.forEach(function(a) {
        top = top + offset(a)[options.style];
      }), handleNumber = top / 2 > location || 1 === scope_Handles.length ? 0 : 1, proposal = 100 * (location = location - offset(scope_Base)[options.style]) / baseSize(), options.events.snap || addClassFor(scope_Target, cssClasses[14], 300), !scope_Handles[handleNumber].hasAttribute("disabled") && (setHandle(scope_Handles[handleNumber], proposal), fireEvent("slide", handleNumber), fireEvent("set", handleNumber), fireEvent("change", handleNumber), void(options.events.snap && start(event, {
        handles : [scope_Handles[handleNumber]]
      })));
    }
    /**
     * @param {!Object} data
     * @return {undefined}
     */
    function events(data) {
      var i;
      var handles;
      if (!data.fixed) {
        /** @type {number} */
        i = 0;
        for (; i < scope_Handles.length; i = i + 1) {
          attach(node.start, scope_Handles[i].children[0], start, {
            handles : [scope_Handles[i]]
          });
        }
      }
      if (data.tap) {
        attach(node.start, scope_Base, tap, {
          handles : scope_Handles
        });
      }
      if (data.drag) {
        addClass((handles = [scope_Base.querySelector("." + cssClasses[7])])[0], cssClasses[10]);
        if (data.fixed) {
          handles.push(scope_Handles[handles[0] === scope_Handles[0] ? 1 : 0].children[0]);
        }
        handles.forEach(function(newFragment) {
          attach(node.start, newFragment, start, {
            handles : scope_Handles
          });
        });
      }
    }
    /**
     * @param {!Element} handle
     * @param {number} to
     * @param {boolean} value
     * @return {?}
     */
    function setHandle(handle, to, value) {
      /** @type {number} */
      var trigger = handle !== scope_Handles[0] ? 1 : 0;
      var lowerMargin = scope_Locations[0] + options.margin;
      /** @type {number} */
      var upperMargin = scope_Locations[1] - options.margin;
      var lowerLimit = scope_Locations[0] + options.limit;
      /** @type {number} */
      var upperLimit = scope_Locations[1] - options.limit;
      var translatedToPosition = scope_Spectrum.fromStepping(to);
      return scope_Handles.length > 1 && (to = trigger ? Math.max(to, lowerMargin) : Math.min(to, upperMargin)), false !== value && options.limit && scope_Handles.length > 1 && (to = trigger ? Math.min(to, lowerLimit) : Math.max(to, upperLimit)), to = scope_Spectrum.getStep(to), ((to = limit(parseFloat(to.toFixed(7)))) !== scope_Locations[trigger] || translatedToPosition !== scope_Values[trigger]) && (window.requestAnimationFrame ? window.requestAnimationFrame(function() {
        handle.style[options.style] = to + "%";
      }) : handle.style[options.style] = to + "%", handle.previousSibling || (removeClass(handle, cssClasses[17]), to > 50 && addClass(handle, cssClasses[17])), scope_Locations[trigger] = to, scope_Values[trigger] = scope_Spectrum.fromStepping(to), fireEvent("update", trigger), true);
    }
    /**
     * @param {number} b
     * @param {!Object} a
     * @return {undefined}
     */
    function setValues(b, a) {
      var thresh;
      var i;
      var value;
      if (options.limit) {
        b = b + 1;
      }
      /** @type {number} */
      thresh = 0;
      for (; b > thresh; thresh = thresh + 1) {
        if (null !== (value = a[i = thresh % 2]) && false !== value) {
          if ("number" == typeof value) {
            /** @type {string} */
            value = String(value);
          }
          if (false === (value = options.format.from(value)) || isNaN(value) || false === setHandle(scope_Handles[i], scope_Spectrum.toStepping(value), thresh === 3 - options.dir)) {
            fireEvent("update", i);
          }
        }
      }
    }
    /**
     * @param {!Function} input
     * @return {undefined}
     */
    function valueSet(input) {
      var success;
      var i;
      var values = asArray(input);
      if (options.dir && options.handles > 1) {
        values.reverse();
      }
      if (options.animate && -1 !== scope_Locations[0]) {
        addClassFor(scope_Target, cssClasses[14], 300);
      }
      /** @type {number} */
      success = scope_Handles.length > 1 ? 3 : 1;
      if (1 === values.length) {
        /** @type {number} */
        success = 1;
      }
      setValues(success, values);
      /** @type {number} */
      i = 0;
      for (; i < scope_Handles.length; i++) {
        fireEvent("set", i);
      }
    }
    /**
     * @return {?}
     */
    function valueGet() {
      var i;
      /** @type {!Array} */
      var retour = [];
      /** @type {number} */
      i = 0;
      for (; i < options.handles; i = i + 1) {
        retour[i] = options.format.to(scope_Values[i]);
      }
      return inSliderOrder(retour);
    }
    /**
     * @return {undefined}
     */
    function destroy() {
      cssClasses.forEach(function(Drawer__closed) {
        if (Drawer__closed) {
          removeClass(scope_Target, Drawer__closed);
        }
      });
      /** @type {string} */
      scope_Target.innerHTML = "";
      delete scope_Target.noUiSlider;
    }
    /**
     * @return {?}
     */
    function getCurrentStep() {
      return inSliderOrder(scope_Locations.map(function(location, i) {
        var step = scope_Spectrum.getApplicableStep(location);
        var stepDecimals = countDecimals(String(step[2]));
        var value = scope_Values[i];
        var index = 100 === location ? null : step[2];
        /** @type {number} */
        var prev = Number((value - step[2]).toFixed(stepDecimals));
        return [0 === location ? null : prev >= step[1] ? step[2] : step[0] || false, index];
      }));
    }
    /**
     * @param {string} type
     * @param {!Function} query
     * @return {undefined}
     */
    function bindEvent(type, query) {
      def[type] = def[type] || [];
      def[type].push(query);
      if ("update" === type.split(".")[0]) {
        scope_Handles.forEach(function(canCreateDiscussions, i) {
          fireEvent("update", i);
        });
      }
    }
    /**
     * @param {string} name
     * @return {undefined}
     */
    function removeEvent(name) {
      var v = name.split(".")[0];
      var initialStreakDateGivenByUserBkp = name.substring(v.length);
      Object.keys(def).forEach(function(path) {
        /** @type {string} */
        var name = path.split(".")[0];
        /** @type {string} */
        var initialStreakDateGivenByUser = path.substring(name.length);
        if (!(v && v !== name || initialStreakDateGivenByUserBkp && initialStreakDateGivenByUserBkp !== initialStreakDateGivenByUser)) {
          delete def[path];
        }
      });
    }
    /**
     * @param {!Object} optionsToUpdate
     * @return {undefined}
     */
    function updateOptions(optionsToUpdate) {
      var newOptions = testOptions({
        start : [0, 0],
        margin : optionsToUpdate.margin,
        limit : optionsToUpdate.limit,
        step : optionsToUpdate.step,
        range : optionsToUpdate.range,
        animate : optionsToUpdate.animate
      });
      options.margin = newOptions.margin;
      options.limit = newOptions.limit;
      options.step = newOptions.step;
      options.range = newOptions.range;
      options.animate = newOptions.animate;
      scope_Spectrum = newOptions.spectrum;
    }
    var scope_Base;
    var scope_Handles;
    /** @type {!Node} */
    var scope_Target = target;
    /** @type {!Array} */
    var scope_Locations = [-1, -1];
    var scope_Spectrum = options.spectrum;
    /** @type {!Array} */
    var scope_Values = [];
    var def = {};
    /** @type {!Array<?>} */
    var cssClasses = ["target", "base", "origin", "handle", "horizontal", "vertical", "background", "connect", "ltr", "rtl", "draggable", "", "state-drag", "", "state-tap", "active", "", "stacking", "tooltip"].map(addCssPrefix(options.cssPrefix || defaultCssPrefix));
    if (scope_Target.noUiSlider) {
      throw new Error("Slider was already initialized.");
    }
    return scope_Base = addSlider(options.dir, options.ort, scope_Target), scope_Handles = addHandles(options.handles, options.dir, scope_Base), addConnection(options.connect, scope_Target, scope_Handles), events(options.events), options.pips && pips(options.pips), options.tooltips && tooltips(options.tooltips), {
      destroy : destroy,
      steps : getCurrentStep,
      on : bindEvent,
      off : removeEvent,
      get : valueGet,
      set : valueSet,
      updateOptions : updateOptions
    };
  }
  /**
   * @param {!Node} target
   * @param {!Object} originalOptions
   * @return {?}
   */
  function initialize(target, originalOptions) {
    if (!target.nodeName) {
      throw new Error("noUiSlider.create requires a single element.");
    }
    var options = testOptions(originalOptions, target);
    var slider = closure(target, options);
    return slider.set(options.start), target.noUiSlider = slider, slider;
  }
  /** @type {({end: string, move: string, start: string})} */
  var node = window.navigator.pointerEnabled ? {
    start : "pointerdown",
    move : "pointermove",
    end : "pointerup"
  } : window.navigator.msPointerEnabled ? {
    start : "MSPointerDown",
    move : "MSPointerMove",
    end : "MSPointerUp"
  } : {
    start : "mousedown touchstart",
    move : "mousemove touchmove",
    end : "mouseup touchend"
  };
  /** @type {string} */
  var defaultCssPrefix = "noUi-";
  /**
   * @param {number} value
   * @return {?}
   */
  Spectrum.prototype.getMargin = function(value) {
    return 2 === this.xPct.length && fromPercentage(this.xVal, value);
  };
  /**
   * @param {number} value
   * @return {?}
   */
  Spectrum.prototype.toStepping = function(value) {
    return value = toStepping(this.xVal, this.xPct, value), this.direction && (value = 100 - value), value;
  };
  /**
   * @param {number} value
   * @return {?}
   */
  Spectrum.prototype.fromStepping = function(value) {
    return this.direction && (value = 100 - value), accurateNumber(fromStepping(this.xVal, this.xPct, value));
  };
  /**
   * @param {number} value
   * @return {?}
   */
  Spectrum.prototype.getStep = function(value) {
    return this.direction && (value = 100 - value), value = getStep(this.xPct, this.xSteps, this.snap, value), this.direction && (value = 100 - value), value;
  };
  /**
   * @param {number} value
   * @return {?}
   */
  Spectrum.prototype.getApplicableStep = function(value) {
    var j = getJ(value, this.xPct);
    /** @type {number} */
    var offset = 100 === value ? 2 : 1;
    return [this.xNumSteps[j - 2], this.xVal[j - offset], this.xNumSteps[j - offset]];
  };
  /**
   * @param {undefined} value
   * @return {?}
   */
  Spectrum.prototype.convert = function(value) {
    return this.getStep(this.toStepping(value));
  };
  var defaultFormatter = {
    to : function(s) {
      return void 0 !== s && s.toFixed(2);
    },
    from : Number
  };
  return {
    create : initialize
  };
}), function() {
  /**
   * @param {!Object} img
   * @return {?}
   */
  function imageHasData(img) {
    return !!img.exifdata;
  }
  /**
   * @param {string} base64
   * @param {string} contentType
   * @return {?}
   */
  function base64ToArrayBuffer(base64, contentType) {
    contentType = contentType || base64.match(/^data:([^;]+);base64,/im)[1] || "";
    base64 = base64.replace(/^data:([^;]+);base64,/gim, "");
    /** @type {string} */
    var text = atob(base64);
    /** @type {number} */
    var l = text.length;
    /** @type {!ArrayBuffer} */
    var buffer = new ArrayBuffer(l);
    /** @type {!Uint8Array} */
    var uint8Array = new Uint8Array(buffer);
    /** @type {number} */
    var i = 0;
    for (; i < l; i++) {
      /** @type {number} */
      uint8Array[i] = text.charCodeAt(i);
    }
    return buffer;
  }
  /**
   * @param {?} url
   * @param {!Function} callback
   * @return {undefined}
   */
  function objectURLToBlob(url, callback) {
    /** @type {!XMLHttpRequest} */
    var xhr = new XMLHttpRequest;
    xhr.open("GET", url, true);
    /** @type {string} */
    xhr.responseType = "blob";
    /**
     * @return {undefined}
     */
    xhr.onload = function() {
      if (!(200 != this.status && 0 !== this.status)) {
        callback(this.response);
      }
    };
    xhr.send();
  }
  /**
   * @param {!Object} img
   * @param {!Function} callback
   * @return {undefined}
   */
  function getImageData(img, callback) {
    /**
     * @param {(Uint8Array|string)} binFile
     * @return {undefined}
     */
    function handleBinaryFile(binFile) {
      var data = findEXIFinJPEG(binFile);
      var iptcdata = findIPTCinJPEG(binFile);
      img.exifdata = data || {};
      img.iptcdata = iptcdata || {};
      if (callback) {
        callback.call(img);
      }
    }
    if (img.src) {
      if (/^data:/i.test(img.src)) {
        handleBinaryFile(base64ToArrayBuffer(img.src));
      } else {
        if (/^blob:/i.test(img.src)) {
          /**
           * @param {!Event} fileLoadedEvent
           * @return {undefined}
           */
          (fileReader = new FileReader).onload = function(fileLoadedEvent) {
            handleBinaryFile(fileLoadedEvent.target.result);
          };
          objectURLToBlob(img.src, function(data) {
            fileReader.readAsArrayBuffer(data);
          });
        } else {
          /** @type {!XMLHttpRequest} */
          var http = new XMLHttpRequest;
          /**
           * @return {undefined}
           */
          http.onload = function() {
            if (200 != this.status && 0 !== this.status) {
              throw "Could not load image";
            }
            handleBinaryFile(http.response);
            /** @type {null} */
            http = null;
          };
          http.open("GET", img.src, true);
          /** @type {string} */
          http.responseType = "arraybuffer";
          http.send(null);
        }
      }
    } else {
      if (window.FileReader && (img instanceof window.Blob || img instanceof window.File)) {
        var fileReader;
        /**
         * @param {!Event} fileLoadedEvent
         * @return {undefined}
         */
        (fileReader = new FileReader).onload = function(fileLoadedEvent) {
          if (processPercent) {
            console.log("Got file of length " + fileLoadedEvent.target.result.byteLength);
          }
          handleBinaryFile(fileLoadedEvent.target.result);
        };
        fileReader.readAsArrayBuffer(img);
      }
    }
  }
  /**
   * @param {(Uint8Array|string)} file
   * @return {?}
   */
  function findEXIFinJPEG(file) {
    /** @type {!DataView} */
    var dataView = new DataView(file);
    if (processPercent && console.log("Got file of length " + file.byteLength), 255 != dataView.getUint8(0) || 216 != dataView.getUint8(1)) {
      return processPercent && console.log("Not a valid JPEG"), false;
    }
    var n;
    /** @type {number} */
    var offset = 2;
    var fileLength = file.byteLength;
    for (; offset < fileLength;) {
      if (255 != dataView.getUint8(offset)) {
        return processPercent && console.log("Not a valid marker at offset " + offset + ", found: " + dataView.getUint8(offset)), false;
      }
      if (n = dataView.getUint8(offset + 1), processPercent && console.log(n), 225 == n) {
        return processPercent && console.log("Found 0xFFE1 marker"), readEXIFData(dataView, offset + 4, dataView.getUint16(offset + 2) - 2);
      }
      /** @type {number} */
      offset = offset + (2 + dataView.getUint16(offset + 2));
    }
  }
  /**
   * @param {(Uint8Array|string)} file
   * @return {?}
   */
  function findIPTCinJPEG(file) {
    /** @type {!DataView} */
    var dataView = new DataView(file);
    if (processPercent && console.log("Got file of length " + file.byteLength), 255 != dataView.getUint8(0) || 216 != dataView.getUint8(1)) {
      return processPercent && console.log("Not a valid JPEG"), false;
    }
    /** @type {number} */
    var offset = 2;
    var fileLength = file.byteLength;
    /**
     * @param {!DataView} dataView
     * @param {number} offset
     * @return {?}
     */
    var isFieldSegmentStart = function(dataView, offset) {
      return 56 === dataView.getUint8(offset) && 66 === dataView.getUint8(offset + 1) && 73 === dataView.getUint8(offset + 2) && 77 === dataView.getUint8(offset + 3) && 4 === dataView.getUint8(offset + 4) && 4 === dataView.getUint8(offset + 5);
    };
    for (; offset < fileLength;) {
      if (isFieldSegmentStart(dataView, offset)) {
        /** @type {number} */
        var nameHeaderLength = dataView.getUint8(offset + 7);
        return nameHeaderLength % 2 != 0 && (nameHeaderLength = nameHeaderLength + 1), 0 === nameHeaderLength && (nameHeaderLength = 4), readIPTCData(file, offset + 8 + nameHeaderLength, dataView.getUint16(offset + 6 + nameHeaderLength));
      }
      offset++;
    }
  }
  /**
   * @param {!Uint8Array} file
   * @param {number} startOffset
   * @param {number} sectionLength
   * @return {?}
   */
  function readIPTCData(file, startOffset, sectionLength) {
    var fieldValue;
    var fieldName;
    var dataSize;
    var name;
    /** @type {!DataView} */
    var dataView = new DataView(file);
    var data = {};
    /** @type {number} */
    var segmentStartPos = startOffset;
    for (; segmentStartPos < startOffset + sectionLength;) {
      if (28 === dataView.getUint8(segmentStartPos) && 2 === dataView.getUint8(segmentStartPos + 1) && (name = dataView.getUint8(segmentStartPos + 2)) in style) {
        (dataSize = dataView.getInt16(segmentStartPos + 3)) + 5;
        fieldName = style[name];
        fieldValue = getStringFromDB(dataView, segmentStartPos + 5, dataSize);
        if (data.hasOwnProperty(fieldName)) {
          if (data[fieldName] instanceof Array) {
            data[fieldName].push(fieldValue);
          } else {
            /** @type {!Array} */
            data[fieldName] = [data[fieldName], fieldValue];
          }
        } else {
          data[fieldName] = fieldValue;
        }
      }
      segmentStartPos++;
    }
    return data;
  }
  /**
   * @param {!DataView} file
   * @param {?} tiffStart
   * @param {number} dirStart
   * @param {?} strings
   * @param {!Object} bigEnd
   * @return {?}
   */
  function readTags(file, tiffStart, dirStart, strings, bigEnd) {
    var entryOffset;
    var tag;
    var s;
    var samplecount = file.getUint16(dirStart, !bigEnd);
    var tags = {};
    /** @type {number} */
    s = 0;
    for (; s < samplecount; s++) {
      entryOffset = dirStart + 12 * s + 2;
      if (!(tag = strings[file.getUint16(entryOffset, !bigEnd)]) && processPercent) {
        console.log("Unknown tag: " + file.getUint16(entryOffset, !bigEnd));
      }
      tags[tag] = readTagValue(file, entryOffset, tiffStart, dirStart, bigEnd);
    }
    return tags;
  }
  /**
   * @param {!DataView} file
   * @param {number} entryOffset
   * @param {?} tiffStart
   * @param {number} dirStart
   * @param {!Object} bigEnd
   * @return {?}
   */
  function readTagValue(file, entryOffset, tiffStart, dirStart, bigEnd) {
    var offset;
    var vals;
    var val;
    var n;
    var numerator;
    var denominator;
    var c = file.getUint16(entryOffset + 2, !bigEnd);
    var numValues = file.getUint32(entryOffset + 4, !bigEnd);
    var valueOffset = file.getUint32(entryOffset + 8, !bigEnd) + tiffStart;
    switch(c) {
      case 1:
      case 7:
        if (1 == numValues) {
          return file.getUint8(entryOffset + 8, !bigEnd);
        }
        offset = numValues > 4 ? valueOffset : entryOffset + 8;
        /** @type {!Array} */
        vals = [];
        /** @type {number} */
        n = 0;
        for (; n < numValues; n++) {
          vals[n] = file.getUint8(offset + n);
        }
        return vals;
      case 2:
        return getStringFromDB(file, offset = numValues > 4 ? valueOffset : entryOffset + 8, numValues - 1);
      case 3:
        if (1 == numValues) {
          return file.getUint16(entryOffset + 8, !bigEnd);
        }
        offset = numValues > 2 ? valueOffset : entryOffset + 8;
        /** @type {!Array} */
        vals = [];
        /** @type {number} */
        n = 0;
        for (; n < numValues; n++) {
          vals[n] = file.getUint16(offset + 2 * n, !bigEnd);
        }
        return vals;
      case 4:
        if (1 == numValues) {
          return file.getUint32(entryOffset + 8, !bigEnd);
        }
        /** @type {!Array} */
        vals = [];
        /** @type {number} */
        n = 0;
        for (; n < numValues; n++) {
          vals[n] = file.getUint32(valueOffset + 4 * n, !bigEnd);
        }
        return vals;
      case 5:
        if (1 == numValues) {
          return numerator = file.getUint32(valueOffset, !bigEnd), denominator = file.getUint32(valueOffset + 4, !bigEnd), (val = new Number(numerator / denominator)).numerator = numerator, val.denominator = denominator, val;
        }
        /** @type {!Array} */
        vals = [];
        /** @type {number} */
        n = 0;
        for (; n < numValues; n++) {
          numerator = file.getUint32(valueOffset + 8 * n, !bigEnd);
          denominator = file.getUint32(valueOffset + 4 + 8 * n, !bigEnd);
          /** @type {!Number} */
          vals[n] = new Number(numerator / denominator);
          vals[n].numerator = numerator;
          vals[n].denominator = denominator;
        }
        return vals;
      case 9:
        if (1 == numValues) {
          return file.getInt32(entryOffset + 8, !bigEnd);
        }
        /** @type {!Array} */
        vals = [];
        /** @type {number} */
        n = 0;
        for (; n < numValues; n++) {
          vals[n] = file.getInt32(valueOffset + 4 * n, !bigEnd);
        }
        return vals;
      case 10:
        if (1 == numValues) {
          return file.getInt32(valueOffset, !bigEnd) / file.getInt32(valueOffset + 4, !bigEnd);
        }
        /** @type {!Array} */
        vals = [];
        /** @type {number} */
        n = 0;
        for (; n < numValues; n++) {
          /** @type {number} */
          vals[n] = file.getInt32(valueOffset + 8 * n, !bigEnd) / file.getInt32(valueOffset + 4 + 8 * n, !bigEnd);
        }
        return vals;
    }
  }
  /**
   * @param {!DataView} buffer
   * @param {number} start
   * @param {number} length
   * @return {?}
   */
  function getStringFromDB(buffer, start, length) {
    /** @type {string} */
    var outstr = "";
    /** @type {number} */
    n = start;
    for (; n < start + length; n++) {
      /** @type {string} */
      outstr = outstr + String.fromCharCode(buffer.getUint8(n));
    }
    return outstr;
  }
  /**
   * @param {!DataView} file
   * @param {number} start
   * @return {?}
   */
  function readEXIFData(file, start) {
    if ("Exif" != getStringFromDB(file, start, 4)) {
      return processPercent && console.log("Not valid EXIF data! " + getStringFromDB(file, start, 4)), false;
    }
    var bigEnd;
    var tags;
    var tag;
    var exifData;
    var gpsData;
    var tiffOffset = start + 6;
    if (18761 == file.getUint16(tiffOffset)) {
      /** @type {boolean} */
      bigEnd = false;
    } else {
      if (19789 != file.getUint16(tiffOffset)) {
        return processPercent && console.log("Not valid TIFF data! (no 0x4949 or 0x4D4D)"), false;
      }
      /** @type {boolean} */
      bigEnd = true;
    }
    if (42 != file.getUint16(tiffOffset + 2, !bigEnd)) {
      return processPercent && console.log("Not valid TIFF data! (no 0x002A)"), false;
    }
    var firstIFDOffset = file.getUint32(tiffOffset + 4, !bigEnd);
    if (firstIFDOffset < 8) {
      return processPercent && console.log("Not valid TIFF data! (First offset less than 8)", file.getUint32(tiffOffset + 4, !bigEnd)), false;
    }
    if ((tags = readTags(file, tiffOffset, tiffOffset + firstIFDOffset, TiffTags, bigEnd)).ExifIFDPointer) {
      for (tag in exifData = readTags(file, tiffOffset, tiffOffset + tags.ExifIFDPointer, ExifTags, bigEnd)) {
        switch(tag) {
          case "LightSource":
          case "Flash":
          case "MeteringMode":
          case "ExposureProgram":
          case "SensingMethod":
          case "SceneCaptureType":
          case "SceneType":
          case "CustomRendered":
          case "WhiteBalance":
          case "GainControl":
          case "Contrast":
          case "Saturation":
          case "Sharpness":
          case "SubjectDistanceRange":
          case "FileSource":
            exifData[tag] = StringValues[tag][exifData[tag]];
            break;
          case "ExifVersion":
          case "FlashpixVersion":
            /** @type {string} */
            exifData[tag] = String.fromCharCode(exifData[tag][0], exifData[tag][1], exifData[tag][2], exifData[tag][3]);
            break;
          case "ComponentsConfiguration":
            exifData[tag] = StringValues.Components[exifData[tag][0]] + StringValues.Components[exifData[tag][1]] + StringValues.Components[exifData[tag][2]] + StringValues.Components[exifData[tag][3]];
        }
        tags[tag] = exifData[tag];
      }
    }
    if (tags.GPSInfoIFDPointer) {
      for (tag in gpsData = readTags(file, tiffOffset, tiffOffset + tags.GPSInfoIFDPointer, GPSTags, bigEnd)) {
        switch(tag) {
          case "GPSVersionID":
            gpsData[tag] = gpsData[tag][0] + "." + gpsData[tag][1] + "." + gpsData[tag][2] + "." + gpsData[tag][3];
        }
        tags[tag] = gpsData[tag];
      }
    }
    return tags;
  }
  /** @type {boolean} */
  var processPercent = false;
  var root = this;
  /**
   * @param {string} obj
   * @return {?}
   */
  var EXIF = function(obj) {
    return obj instanceof EXIF ? obj : this instanceof EXIF ? void(this.EXIFwrapped = obj) : new EXIF(obj);
  };
  if ("undefined" != typeof exports) {
    if ("undefined" != typeof module && module.exports) {
      /** @type {function(string): ?} */
      exports = module.exports = EXIF;
    }
    /** @type {function(string): ?} */
    exports.EXIF = EXIF;
  } else {
    /** @type {function(string): ?} */
    root.EXIF = EXIF;
  }
  var ExifTags = EXIF.Tags = {
    36864 : "ExifVersion",
    40960 : "FlashpixVersion",
    40961 : "ColorSpace",
    40962 : "PixelXDimension",
    40963 : "PixelYDimension",
    37121 : "ComponentsConfiguration",
    37122 : "CompressedBitsPerPixel",
    37500 : "MakerNote",
    37510 : "UserComment",
    40964 : "RelatedSoundFile",
    36867 : "DateTimeOriginal",
    36868 : "DateTimeDigitized",
    37520 : "SubsecTime",
    37521 : "SubsecTimeOriginal",
    37522 : "SubsecTimeDigitized",
    33434 : "ExposureTime",
    33437 : "FNumber",
    34850 : "ExposureProgram",
    34852 : "SpectralSensitivity",
    34855 : "ISOSpeedRatings",
    34856 : "OECF",
    37377 : "ShutterSpeedValue",
    37378 : "ApertureValue",
    37379 : "BrightnessValue",
    37380 : "ExposureBias",
    37381 : "MaxApertureValue",
    37382 : "SubjectDistance",
    37383 : "MeteringMode",
    37384 : "LightSource",
    37385 : "Flash",
    37396 : "SubjectArea",
    37386 : "FocalLength",
    41483 : "FlashEnergy",
    41484 : "SpatialFrequencyResponse",
    41486 : "FocalPlaneXResolution",
    41487 : "FocalPlaneYResolution",
    41488 : "FocalPlaneResolutionUnit",
    41492 : "SubjectLocation",
    41493 : "ExposureIndex",
    41495 : "SensingMethod",
    41728 : "FileSource",
    41729 : "SceneType",
    41730 : "CFAPattern",
    41985 : "CustomRendered",
    41986 : "ExposureMode",
    41987 : "WhiteBalance",
    41988 : "DigitalZoomRation",
    41989 : "FocalLengthIn35mmFilm",
    41990 : "SceneCaptureType",
    41991 : "GainControl",
    41992 : "Contrast",
    41993 : "Saturation",
    41994 : "Sharpness",
    41995 : "DeviceSettingDescription",
    41996 : "SubjectDistanceRange",
    40965 : "InteroperabilityIFDPointer",
    42016 : "ImageUniqueID"
  };
  var TiffTags = EXIF.TiffTags = {
    256 : "ImageWidth",
    257 : "ImageHeight",
    34665 : "ExifIFDPointer",
    34853 : "GPSInfoIFDPointer",
    40965 : "InteroperabilityIFDPointer",
    258 : "BitsPerSample",
    259 : "Compression",
    262 : "PhotometricInterpretation",
    274 : "Orientation",
    277 : "SamplesPerPixel",
    284 : "PlanarConfiguration",
    530 : "YCbCrSubSampling",
    531 : "YCbCrPositioning",
    282 : "XResolution",
    283 : "YResolution",
    296 : "ResolutionUnit",
    273 : "StripOffsets",
    278 : "RowsPerStrip",
    279 : "StripByteCounts",
    513 : "JPEGInterchangeFormat",
    514 : "JPEGInterchangeFormatLength",
    301 : "TransferFunction",
    318 : "WhitePoint",
    319 : "PrimaryChromaticities",
    529 : "YCbCrCoefficients",
    532 : "ReferenceBlackWhite",
    306 : "DateTime",
    270 : "ImageDescription",
    271 : "Make",
    272 : "Model",
    305 : "Software",
    315 : "Artist",
    33432 : "Copyright"
  };
  var GPSTags = EXIF.GPSTags = {
    0 : "GPSVersionID",
    1 : "GPSLatitudeRef",
    2 : "GPSLatitude",
    3 : "GPSLongitudeRef",
    4 : "GPSLongitude",
    5 : "GPSAltitudeRef",
    6 : "GPSAltitude",
    7 : "GPSTimeStamp",
    8 : "GPSSatellites",
    9 : "GPSStatus",
    10 : "GPSMeasureMode",
    11 : "GPSDOP",
    12 : "GPSSpeedRef",
    13 : "GPSSpeed",
    14 : "GPSTrackRef",
    15 : "GPSTrack",
    16 : "GPSImgDirectionRef",
    17 : "GPSImgDirection",
    18 : "GPSMapDatum",
    19 : "GPSDestLatitudeRef",
    20 : "GPSDestLatitude",
    21 : "GPSDestLongitudeRef",
    22 : "GPSDestLongitude",
    23 : "GPSDestBearingRef",
    24 : "GPSDestBearing",
    25 : "GPSDestDistanceRef",
    26 : "GPSDestDistance",
    27 : "GPSProcessingMethod",
    28 : "GPSAreaInformation",
    29 : "GPSDateStamp",
    30 : "GPSDifferential"
  };
  var StringValues = EXIF.StringValues = {
    ExposureProgram : {
      0 : "Not defined",
      1 : "Manual",
      2 : "Normal program",
      3 : "Aperture priority",
      4 : "Shutter priority",
      5 : "Creative program",
      6 : "Action program",
      7 : "Portrait mode",
      8 : "Landscape mode"
    },
    MeteringMode : {
      0 : "Unknown",
      1 : "Average",
      2 : "CenterWeightedAverage",
      3 : "Spot",
      4 : "MultiSpot",
      5 : "Pattern",
      6 : "Partial",
      255 : "Other"
    },
    LightSource : {
      0 : "Unknown",
      1 : "Daylight",
      2 : "Fluorescent",
      3 : "Tungsten (incandescent light)",
      4 : "Flash",
      9 : "Fine weather",
      10 : "Cloudy weather",
      11 : "Shade",
      12 : "Daylight fluorescent (D 5700 - 7100K)",
      13 : "Day white fluorescent (N 4600 - 5400K)",
      14 : "Cool white fluorescent (W 3900 - 4500K)",
      15 : "White fluorescent (WW 3200 - 3700K)",
      17 : "Standard light A",
      18 : "Standard light B",
      19 : "Standard light C",
      20 : "D55",
      21 : "D65",
      22 : "D75",
      23 : "D50",
      24 : "ISO studio tungsten",
      255 : "Other"
    },
    Flash : {
      0 : "Flash did not fire",
      1 : "Flash fired",
      5 : "Strobe return light not detected",
      7 : "Strobe return light detected",
      9 : "Flash fired, compulsory flash mode",
      13 : "Flash fired, compulsory flash mode, return light not detected",
      15 : "Flash fired, compulsory flash mode, return light detected",
      16 : "Flash did not fire, compulsory flash mode",
      24 : "Flash did not fire, auto mode",
      25 : "Flash fired, auto mode",
      29 : "Flash fired, auto mode, return light not detected",
      31 : "Flash fired, auto mode, return light detected",
      32 : "No flash function",
      65 : "Flash fired, red-eye reduction mode",
      69 : "Flash fired, red-eye reduction mode, return light not detected",
      71 : "Flash fired, red-eye reduction mode, return light detected",
      73 : "Flash fired, compulsory flash mode, red-eye reduction mode",
      77 : "Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected",
      79 : "Flash fired, compulsory flash mode, red-eye reduction mode, return light detected",
      89 : "Flash fired, auto mode, red-eye reduction mode",
      93 : "Flash fired, auto mode, return light not detected, red-eye reduction mode",
      95 : "Flash fired, auto mode, return light detected, red-eye reduction mode"
    },
    SensingMethod : {
      1 : "Not defined",
      2 : "One-chip color area sensor",
      3 : "Two-chip color area sensor",
      4 : "Three-chip color area sensor",
      5 : "Color sequential area sensor",
      7 : "Trilinear sensor",
      8 : "Color sequential linear sensor"
    },
    SceneCaptureType : {
      0 : "Standard",
      1 : "Landscape",
      2 : "Portrait",
      3 : "Night scene"
    },
    SceneType : {
      1 : "Directly photographed"
    },
    CustomRendered : {
      0 : "Normal process",
      1 : "Custom process"
    },
    WhiteBalance : {
      0 : "Auto white balance",
      1 : "Manual white balance"
    },
    GainControl : {
      0 : "None",
      1 : "Low gain up",
      2 : "High gain up",
      3 : "Low gain down",
      4 : "High gain down"
    },
    Contrast : {
      0 : "Normal",
      1 : "Soft",
      2 : "Hard"
    },
    Saturation : {
      0 : "Normal",
      1 : "Low saturation",
      2 : "High saturation"
    },
    Sharpness : {
      0 : "Normal",
      1 : "Soft",
      2 : "Hard"
    },
    SubjectDistanceRange : {
      0 : "Unknown",
      1 : "Macro",
      2 : "Close view",
      3 : "Distant view"
    },
    FileSource : {
      3 : "DSC"
    },
    Components : {
      0 : "",
      1 : "Y",
      2 : "Cb",
      3 : "Cr",
      4 : "R",
      5 : "G",
      6 : "B"
    }
  };
  var style = {
    120 : "caption",
    110 : "credit",
    25 : "keywords",
    55 : "dateCreated",
    80 : "byline",
    85 : "bylineTitle",
    122 : "captionWriter",
    105 : "headline",
    116 : "copyright",
    15 : "category"
  };
  /**
   * @param {!Object} img
   * @param {!Object} callback
   * @return {?}
   */
  EXIF.getData = function(img, callback) {
    return !((img instanceof Image || img instanceof HTMLImageElement) && !img.complete) && (imageHasData(img) ? callback && callback.call(img) : getImageData(img, callback), true);
  };
  /**
   * @param {!Object} img
   * @param {?} tag
   * @return {?}
   */
  EXIF.getTag = function(img, tag) {
    if (imageHasData(img)) {
      return img.exifdata[tag];
    }
  };
  /**
   * @param {!Object} img
   * @return {?}
   */
  EXIF.getAllTags = function(img) {
    if (!imageHasData(img)) {
      return {};
    }
    var a;
    var data = img.exifdata;
    var tags = {};
    for (a in data) {
      if (data.hasOwnProperty(a)) {
        tags[a] = data[a];
      }
    }
    return tags;
  };
  /**
   * @param {!Object} img
   * @return {?}
   */
  EXIF.pretty = function(img) {
    if (!imageHasData(img)) {
      return "";
    }
    var a;
    var data = img.exifdata;
    /** @type {string} */
    var strPretty = "";
    for (a in data) {
      if (data.hasOwnProperty(a)) {
        if ("object" == typeof data[a]) {
          if (data[a] instanceof Number) {
            /** @type {string} */
            strPretty = strPretty + (a + " : " + data[a] + " [" + data[a].numerator + "/" + data[a].denominator + "]\r\n");
          } else {
            /** @type {string} */
            strPretty = strPretty + (a + " : [" + data[a].length + " values]\r\n");
          }
        } else {
          /** @type {string} */
          strPretty = strPretty + (a + " : " + data[a] + "\r\n");
        }
      }
    }
    return strPretty;
  };
  /**
   * @param {(Uint8Array|string)} file
   * @return {?}
   */
  EXIF.readFromBinaryFile = function(file) {
    return findEXIFinJPEG(file);
  };
  if ("function" == typeof define && define.amd) {
    define("exif-js", [], function() {
      return EXIF;
    });
  }
}.call(this);
var respSpreadWidth;
var respPageWidth;
var respPageHeight;
var respSliderHeight;
var respTotalHeight;
var canvasHammer;
var refOffset;
var refPosition;
var loaderInterval;
var pageData;
var pagePlusOneData;
/** @type {number} */
var page = 0;
/** @type {number} */
var nowLoading = 0;
/** @type {number} */
var currentZoom = 1;
/** @type {number} */
var pageMode = 2;
/** @type {number} */
var pageModeOffset = 0;
/** @type {number} */
var userToggledPageMode = 0;
/** @type {number} */
var isLR = 0;
/** @type {boolean} */
var embedded = false;
/** @type {boolean} */
var quartileFirst = false;
/** @type {boolean} */
var quartileSecond = false;
/** @type {boolean} */
var quartileThird = false;
/** @type {boolean} */
var readerComplete = false;
/** @type {number} */
var adViewed = 0;
/** @type {boolean} */
var fullscreenMode = false;
/** @type {number} */
var respMultiplier = 1;
/** @type {number} */
var fsMultiplier = 1;
/** @type {number} */
var oldMultiplier = 0;
/** @type {number} */
var refSpreadWidth = 960;
/** @type {number} */
var refPageWidth = 480;
/** @type {number} */
var refPageHeight = 715;
/** @type {number} */
var refHeaderHeight = 50;
/** @type {number} */
var refSliderHeight = 75;
/** @type {boolean} */
var readerOpen = false;
/** @type {boolean} */
var readerOpened = false;
var slider = undefined;
var gestureCenter = {};
/** @type {number} */
var gestureDeltaX = 0;
/** @type {number} */
var gestureDeltaY = 0;
/** @type {number} */
var currentPager = 0;
/** @type {number} */
var pagerTime = 0;
/** @type {number} */
var pagerInterval = 0;
/** @type {number} */
var menuTimeout = 0;
/** @type {number} */
var hideMenuAfter = 2E3;
/** @type {number} */
var originalMousePosX = 0;
/** @type {number} */
var originalMousePosY = 0;
/** @type {number} */
var lastMousePosX = 0;
/** @type {number} */
var lastMousePosY = 0;
/** @type {!Number} */
var manga_id = new Number;
/** @type {string} */
var pageUrl = "/manga/get_manga_url?device_id=3";
/** @type {!Array} */
var pageLinks = [];
var pageList = {};
var pageImages = {};
var pageKeys = {};
/** @type {number} */
var debug = 0;
/** @type {boolean} */
var leftPageLoaded = false;
/** @type {boolean} */
var rightPageLoaded = false;
var flashtest = getUrlParameterByName("flashtest");
/** @type {boolean} */
var is_iPad = null != navigator.userAgent.match(/iPad/i);
$(document).ready(function() {
  $(document).on("forceZoom", {
    dir : "in",
    zoomTo : 1,
    animTime : 0
  }, zoom);
  manga_id = getMangaId();
  embedded = getIsChapter() && !usingFlashReader() && !preventEmbed;
  if (true === $.browser.mobile) {
    pageUrl = pageUrl + "&mobile=1";
    if (embedded) {
      $("#reader_close_control_mobile").hide();
    }
  } else {
    if (embedded) {
      $(".reader-popout").removeClass("disp-n");
      $(".reader-close").hide();
      $("#reader_tools").attr("style", "top:10px; right:16px;");
    }
  }
  if (usingFlashReader()) {
    createFlashReader();
    $(window).resize(function() {
      if (readerOpen) {
        adjustFlashReader();
        adjustChapterAdModal();
      }
    });
  } else {
    bookmarkPage = getBookmarkPage();
    isLR = getIsLeftToRight();
    $(window).resize(function() {
      if (true === $.browser.mobile) {
        if (readerOpen) {
          debugLogger("Resize event");
          orientationChanged();
        }
      } else {
        setPageMode(false);
        setupStyles();
        updateDisplayedPages();
        updateOffscreenPages();
        updateEndPages();
        setBookmarkIcon();
      }
      adjustChapterAd();
    });
  }
}), $(document).on("post_read_buttons", function() {
  if (readerOpened) {
    setBookmarkIcon(true);
  }
}), function(addedRenderer, $) {
  $(document).on("keyup", function(event) {
    if (27 == event.keyCode) {
      var mm = $(".reader[data-reader-state='on']");
      if (mm.length) {
        ModalReader.doCloseAction(mm);
      }
    }
  });
}(0, jQuery), ModalReader = {
  resetState : function() {
    $("[data-reader-state]").attr("data-reader-state", "off");
  },
  close : function() {
    $("#nav-container").attr("data-nav-state", "closed");
    $("input", ".reader[data-reader-state='on']").blur();
    ModalReader.setBackgroundScroll(true);
    ModalReader.resetState();
  },
  toggle : function(e) {
    var node = $(e);
    if ("on" == node.attr("data-reader-state")) {
      ModalReader.close();
    } else {
      $("#nav-container").attr("data-nav-state", "off");
      $("#overlay").attr("data-overlay-state", "off").off();
      ModalReader.resetState();
      node.attr("data-reader-state", "on");
      node.css({
        top : $(window).scrollTop() + "px"
      });
      node.scrollTop(0);
      ModalReader.setBackgroundScroll(false);
    }
  },
  setBackgroundScroll : function(isIron) {
    var t = $(window).scrollTop();
    if (isIron) {
      $("html").css({
        top : t + "px"
      }).removeClass("no-scroll");
    } else {
      $("html").addClass("no-scroll").css({
        top : "-" + t + "px"
      });
    }
  },
  doCloseAction : function(props) {
    var root = $(".reader-close", props);
    if (root.length) {
      root.click();
    } else {
      ModalReader.close();
    }
  }
}, function(window, document, undefined) {
  /**
   * @param {!Function} obj
   * @param {string} type
   * @return {?}
   */
  function is(obj, type) {
    return typeof obj === type;
  }
  /**
   * @return {undefined}
   */
  function testRunner() {
    var expressionArray;
    var feature;
    var aliasIdx;
    var result;
    var i;
    var name;
    var featureIdx;
    for (featureIdx in tests) {
      if (tests.hasOwnProperty(featureIdx)) {
        if (expressionArray = [], (feature = tests[featureIdx]).name && (expressionArray.push(feature.name.toLowerCase()), feature.options && feature.options.aliases && feature.options.aliases.length)) {
          /** @type {number} */
          aliasIdx = 0;
          for (; aliasIdx < feature.options.aliases.length; aliasIdx++) {
            expressionArray.push(feature.options.aliases[aliasIdx].toLowerCase());
          }
        }
        result = is(feature.fn, "function") ? feature.fn() : feature.fn;
        /** @type {number} */
        i = 0;
        for (; i < expressionArray.length; i++) {
          if (1 === (name = expressionArray[i].split(".")).length) {
            Modernizr[name[0]] = result;
          } else {
            if (!(!Modernizr[name[0]] || Modernizr[name[0]] instanceof Boolean)) {
              /** @type {!Boolean} */
              Modernizr[name[0]] = new Boolean(Modernizr[name[0]]);
            }
            Modernizr[name[0]][name[1]] = result;
          }
          classes.push((result ? "" : "no-") + name.join("-"));
        }
      }
    }
  }
  /**
   * @param {!Array} classes
   * @return {undefined}
   */
  function setClasses(classes) {
    var className = docElement.className;
    var classPrefix = Modernizr._config.classPrefix || "";
    if (isSVG && (className = className.baseVal), Modernizr._config.enableJSClass) {
      /** @type {!RegExp} */
      var reJS = new RegExp("(^|\\s)" + classPrefix + "no-js(\\s|$)");
      className = className.replace(reJS, "$1" + classPrefix + "js$2");
    }
    if (Modernizr._config.enableClasses) {
      className = className + (" " + classPrefix + classes.join(" " + classPrefix));
      if (isSVG) {
        docElement.className.baseVal = className;
      } else {
        docElement.className = className;
      }
    }
  }
  /**
   * @return {?}
   */
  function createElement() {
    return "function" != typeof document.createElement ? document.createElement(arguments[0]) : isSVG ? document.createElementNS.call(document, "http://www.w3.org/2000/svg", arguments[0]) : document.createElement.apply(document, arguments);
  }
  /**
   * @return {?}
   */
  function getBody() {
    /** @type {!HTMLBodyElement} */
    var body = document.body;
    return body || ((body = createElement(isSVG ? "svg" : "body")).fake = true), body;
  }
  /**
   * @param {string} feature
   * @param {string} callback
   * @return {?}
   */
  function addTest(feature, callback) {
    if ("object" == typeof feature) {
      var key;
      for (key in feature) {
        if (hasOwnProperty(feature, key)) {
          addTest(key, feature[key]);
        }
      }
    } else {
      var featureNameSplit = (feature = feature.toLowerCase()).split(".");
      var last = Modernizr[featureNameSplit[0]];
      if (2 == featureNameSplit.length && (last = last[featureNameSplit[1]]), void 0 !== last) {
        return Modernizr;
      }
      callback = "function" == typeof callback ? callback() : callback;
      if (1 == featureNameSplit.length) {
        /** @type {string} */
        Modernizr[featureNameSplit[0]] = callback;
      } else {
        if (!(!Modernizr[featureNameSplit[0]] || Modernizr[featureNameSplit[0]] instanceof Boolean)) {
          /** @type {!Boolean} */
          Modernizr[featureNameSplit[0]] = new Boolean(Modernizr[featureNameSplit[0]]);
        }
        /** @type {string} */
        Modernizr[featureNameSplit[0]][featureNameSplit[1]] = callback;
      }
      setClasses([(callback && 0 != callback ? "" : "no-") + featureNameSplit.join("-")]);
      Modernizr._trigger(feature, callback);
    }
    return Modernizr;
  }
  /**
   * @param {!Object} name
   * @return {?}
   */
  function cssToDOM(name) {
    return name.replace(/([a-z])-([a-z])/g, function(canCreateDiscussions, isSlidingUp, shortMonthName) {
      return isSlidingUp + shortMonthName.toUpperCase();
    }).replace(/^-/, "");
  }
  /**
   * @param {string} value
   * @param {string} key
   * @return {?}
   */
  function contains(value, key) {
    return !!~("" + value).indexOf(key);
  }
  /**
   * @param {!Function} fn
   * @param {?} that
   * @return {?}
   */
  function fnBind(fn, that) {
    return function() {
      return fn.apply(that, arguments);
    };
  }
  /**
   * @param {!Object} props
   * @param {!Object} obj
   * @param {!Object} elem
   * @return {?}
   */
  function testDOMProps(props, obj, elem) {
    var name;
    var i;
    for (i in props) {
      if (props[i] in obj) {
        return false === elem ? props[i] : is(name = obj[props[i]], "function") ? fnBind(name, elem || obj) : name;
      }
    }
    return false;
  }
  /**
   * @param {string} rule
   * @param {!Function} callback
   * @param {number} nodes
   * @param {string} testnames
   * @return {?}
   */
  function injectElementWithStyles(rule, callback, nodes, testnames) {
    var style;
    var ret;
    var el;
    var docOverflow;
    /** @type {string} */
    var mod = "modernizr";
    var div = createElement("div");
    var body = getBody();
    if (parseInt(nodes, 10)) {
      for (; nodes--;) {
        (el = createElement("div")).id = testnames ? testnames[nodes] : mod + (nodes + 1);
        div.appendChild(el);
      }
    }
    return (style = createElement("style")).type = "text/css", style.id = "s" + mod, (body.fake ? body : div).appendChild(style), body.appendChild(div), style.styleSheet ? style.styleSheet.cssText = rule : style.appendChild(document.createTextNode(rule)), div.id = mod, body.fake && (body.style.background = "", body.style.overflow = "hidden", docOverflow = docElement.style.overflow, docElement.style.overflow = "hidden", docElement.appendChild(body)), ret = callback(div, rule), body.fake ? (body.parentNode.removeChild(body),
    docElement.style.overflow = docOverflow, docElement.offsetHeight) : div.parentNode.removeChild(div), !!ret;
  }
  /**
   * @param {string} name
   * @return {?}
   */
  function domToCSS(name) {
    return name.replace(/([A-Z])/g, function(canCreateDiscussions, p_Interval) {
      return "-" + p_Interval.toLowerCase();
    }).replace(/^ms-/, "-ms-");
  }
  /**
   * @param {!Object} props
   * @param {!Object} value
   * @return {?}
   */
  function nativeTestProps(props, value) {
    var i = props.length;
    if ("CSS" in window && "supports" in window.CSS) {
      for (; i--;) {
        if (window.CSS.supports(domToCSS(props[i]), value)) {
          return true;
        }
      }
      return false;
    }
    if ("CSSSupportsRule" in window) {
      /** @type {!Array} */
      var drilldownLevelLabels = [];
      for (; i--;) {
        drilldownLevelLabels.push("(" + domToCSS(props[i]) + ":" + value + ")");
      }
      return injectElementWithStyles("@supports (" + (drilldownLevelLabels = drilldownLevelLabels.join(" or ")) + ") { #modernizr { position: absolute; } }", function(anchor) {
        return "absolute" == getComputedStyle(anchor, null).position;
      });
    }
    return undefined;
  }
  /**
   * @param {!Object} props
   * @param {string} prefixed
   * @param {!Object} value
   * @param {!Function} skipValueTest
   * @return {?}
   */
  function testProps(props, prefixed, value, skipValueTest) {
    /**
     * @return {undefined}
     */
    function cleanElems() {
      if (l) {
        delete mStyle.style;
        delete mStyle.modElem;
      }
    }
    if (skipValueTest = !is(skipValueTest, "undefined") && skipValueTest, !is(value, "undefined")) {
      var result = nativeTestProps(props, value);
      if (!is(result, "undefined")) {
        return result;
      }
    }
    var l;
    var _l;
    var propsLength;
    var prop;
    var before;
    /** @type {!Array} */
    var elems = ["modernizr", "tspan"];
    for (; !mStyle.style;) {
      /** @type {boolean} */
      l = true;
      mStyle.modElem = createElement(elems.shift());
      mStyle.style = mStyle.modElem.style;
    }
    propsLength = props.length;
    /** @type {number} */
    _l = 0;
    for (; propsLength > _l; _l++) {
      if (prop = props[_l], before = mStyle.style[prop], contains(prop, "-") && (prop = cssToDOM(prop)), mStyle.style[prop] !== undefined) {
        if (skipValueTest || is(value, "undefined")) {
          return cleanElems(), "pfx" != prefixed || prop;
        }
        try {
          /** @type {!Object} */
          mStyle.style[prop] = value;
        } catch (v) {
        }
        if (mStyle.style[prop] != before) {
          return cleanElems(), "pfx" != prefixed || prop;
        }
      }
    }
    return cleanElems(), false;
  }
  /**
   * @param {string} prop
   * @param {!Object} prefixed
   * @param {string} elem
   * @param {!Object} value
   * @param {!Function} skipValueTest
   * @return {?}
   */
  function testPropsAll(prop, prefixed, elem, value, skipValueTest) {
    var ucProp = prop.charAt(0).toUpperCase() + prop.slice(1);
    /** @type {!Array<string>} */
    var props = (prop + " " + cssomPrefixes.join(ucProp + " ") + ucProp).split(" ");
    return is(prefixed, "string") || is(prefixed, "undefined") ? testProps(props, prefixed, value, skipValueTest) : testDOMProps(props = (prop + " " + domPrefixes.join(ucProp + " ") + ucProp).split(" "), prefixed, elem);
  }
  /** @type {!Array} */
  var classes = [];
  /** @type {!Array} */
  var tests = [];
  var ModernizrProto = {
    _version : "3.2.0",
    _config : {
      classPrefix : "",
      enableClasses : true,
      enableJSClass : true,
      usePrefixes : true
    },
    _q : [],
    on : function(type, callback) {
      var providers = this;
      setTimeout(function() {
        callback(providers[type]);
      }, 0);
    },
    addTest : function(name, options, fn) {
      tests.push({
        name : name,
        fn : options,
        options : fn
      });
    },
    addAsyncTest : function(fn) {
      tests.push({
        name : null,
        fn : fn
      });
    }
  };
  /**
   * @return {undefined}
   */
  var Modernizr = function() {
  };
  Modernizr.prototype = ModernizrProto;
  (Modernizr = new Modernizr).addTest("blobconstructor", function() {
    try {
      return !!new Blob;
    } catch (e) {
      return false;
    }
  }, {
    aliases : ["blob-constructor"]
  });
  /** @type {!Element} */
  var docElement = document.documentElement;
  Modernizr.addTest("cors", "XMLHttpRequest" in window && "withCredentials" in new XMLHttpRequest);
  /** @type {boolean} */
  var isSVG = "svg" === docElement.nodeName.toLowerCase();
  Modernizr.addTest("canvas", function() {
    var e = createElement("canvas");
    return !(!e.getContext || !e.getContext("2d"));
  });
  var hasOwnProperty;
  var inputElem = createElement("input");
  /** @type {!Array<string>} */
  var captureProperties = "search tel url email datetime date month week time datetime-local number range color".split(" ");
  var I18N = {};
  Modernizr.inputtypes = function(props) {
    var inputElemType;
    var defaultView;
    var d;
    /** @type {number} */
    var length = props.length;
    /** @type {string} */
    var smile = ":)";
    /** @type {number} */
    var i = 0;
    for (; length > i; i++) {
      inputElem.setAttribute("type", inputElemType = props[i]);
      if (d = "text" !== inputElem.type && "style" in inputElem) {
        /** @type {string} */
        inputElem.value = smile;
        /** @type {string} */
        inputElem.style.cssText = "position:absolute;visibility:hidden;";
        if (/^range$/.test(inputElemType) && inputElem.style.WebkitAppearance !== undefined) {
          docElement.appendChild(inputElem);
          d = (defaultView = document.defaultView).getComputedStyle && "textfield" !== defaultView.getComputedStyle(inputElem, null).WebkitAppearance && 0 !== inputElem.offsetHeight;
          docElement.removeChild(inputElem);
        } else {
          if (!/^(search|tel)$/.test(inputElemType)) {
            d = /^(url|email|number)$/.test(inputElemType) ? inputElem.checkValidity && false === inputElem.checkValidity() : inputElem.value != smile;
          }
        }
      }
      /** @type {boolean} */
      I18N[props[i]] = !!d;
    }
    return I18N;
  }(captureProperties);
  (function() {
    /** @type {function(this:Object, *): boolean} */
    var b = {}.hasOwnProperty;
    /** @type {function(!Object, string): ?} */
    hasOwnProperty = is(b, "undefined") || is(b.call, "undefined") ? function(object, property) {
      return property in object && is(object.constructor.prototype[property], "undefined");
    } : function(parent, a) {
      return b.call(parent, a);
    };
  })();
  ModernizrProto._l = {};
  /**
   * @param {string} name
   * @param {!Function} listener
   * @return {undefined}
   */
  ModernizrProto.on = function(name, listener) {
    if (!this._l[name]) {
      /** @type {!Array} */
      this._l[name] = [];
    }
    this._l[name].push(listener);
    if (Modernizr.hasOwnProperty(name)) {
      setTimeout(function() {
        Modernizr._trigger(name, Modernizr[name]);
      }, 0);
    }
  };
  /**
   * @param {string} feature
   * @param {string} data
   * @return {undefined}
   */
  ModernizrProto._trigger = function(feature, data) {
    if (this._l[feature]) {
      var cbs = this._l[feature];
      setTimeout(function() {
        var i;
        /** @type {number} */
        i = 0;
        for (; i < cbs.length; i++) {
          (0, cbs[i])(data);
        }
      }, 0);
      delete this._l[feature];
    }
  };
  Modernizr._q.push(function() {
    /** @type {function(string, string): ?} */
    ModernizrProto.addTest = addTest;
  });
  Modernizr.addAsyncTest(function() {
    var a;
    /**
     * @param {!Object} body
     * @return {undefined}
     */
    var removeFakeBody = function(body) {
      if (body.fake && body.parentNode) {
        body.parentNode.removeChild(body);
      }
    };
    /**
     * @param {!Object} result
     * @param {!Object} embed
     * @return {undefined}
     */
    var runTest = function(result, embed) {
      /** @type {boolean} */
      var bool = !!result;
      if (bool && ((bool = new Boolean(bool)).blocked = "blocked" === result), addTest("flash", function() {
        return bool;
      }), embed && body.contains(embed)) {
        for (; embed.parentNode !== body;) {
          embed = embed.parentNode;
        }
        body.removeChild(embed);
      }
    };
    try {
      /** @type {boolean} */
      a = "ActiveXObject" in window && "Pan" in new window.ActiveXObject("ShockwaveFlash.ShockwaveFlash");
    } catch (g) {
    }
    if (!("plugins" in navigator && "Shockwave Flash" in navigator.plugins || a) || isSVG) {
      runTest(false);
    } else {
      var blockedDetect;
      var value;
      var embed = createElement("embed");
      var body = getBody();
      if (embed.type = "application/x-shockwave-flash", body.appendChild(embed), docElement.appendChild(body), !("Pan" in embed || a)) {
        return runTest("blocked", embed), void removeFakeBody(body);
      }
      /**
       * @return {?}
       */
      blockedDetect = function() {
        return docElement.contains(body) ? (docElement.contains(embed) ? (value = embed.style.cssText, runTest("" === value || "blocked", embed)) : runTest("blocked"), void removeFakeBody(body)) : (body = document.body || body, (embed = createElement("embed")).type = "application/x-shockwave-flash", body.appendChild(embed), setTimeout(blockedDetect, 1e3));
      };
      setTimeout(blockedDetect, 10);
    }
  });
  /** @type {string} */
  var excludeLink = "Moz O ms Webkit";
  /** @type {!Array} */
  var cssomPrefixes = ModernizrProto._config.usePrefixes ? excludeLink.split(" ") : [];
  /** @type {!Array} */
  ModernizrProto._cssomPrefixes = cssomPrefixes;
  /**
   * @param {string} prop
   * @return {?}
   */
  var atRule = function(prop) {
    var rule;
    var length = prefixes.length;
    var cssrule = window.CSSRule;
    if (void 0 === cssrule) {
      return undefined;
    }
    if (!prop) {
      return false;
    }
    if ((rule = (prop = prop.replace(/^@/, "")).replace(/-/g, "_").toUpperCase() + "_RULE") in cssrule) {
      return "@" + prop;
    }
    /** @type {number} */
    var j = 0;
    for (; length > j; j++) {
      var prefix = prefixes[j];
      if (prefix.toUpperCase() + "_" + rule in cssrule) {
        return "@-" + prefix.toLowerCase() + "-" + prop;
      }
    }
    return false;
  };
  /** @type {function(string): ?} */
  ModernizrProto.atRule = atRule;
  /** @type {!Array} */
  var domPrefixes = ModernizrProto._config.usePrefixes ? excludeLink.toLowerCase().split(" ") : [];
  /** @type {!Array} */
  ModernizrProto._domPrefixes = domPrefixes;
  var modElem = {
    elem : createElement("modernizr")
  };
  Modernizr._q.push(function() {
    delete modElem.elem;
  });
  var mStyle = {
    style : modElem.elem.style
  };
  Modernizr._q.unshift(function() {
    delete mStyle.style;
  });
  /** @type {function(string, !Object, string, !Object, !Function): ?} */
  ModernizrProto.testAllProps = testPropsAll;
  /** @type {function(!Object, !Object, string): ?} */
  var prefixed = ModernizrProto.prefixed = function(prop, property, value) {
    return 0 === prop.indexOf("@") ? atRule(prop) : (-1 != prop.indexOf("-") && (prop = cssToDOM(prop)), property ? testPropsAll(prop, property, value) : testPropsAll(prop, "pfx"));
  };
  Modernizr.addTest("fullscreen", !(!prefixed("exitFullscreen", document, false) && !prefixed("cancelFullScreen", document, false)));
  testRunner();
  setClasses(classes);
  delete ModernizrProto.addTest;
  delete ModernizrProto.addAsyncTest;
  /** @type {number} */
  var i = 0;
  for (; i < Modernizr._q.length; i++) {
    Modernizr._q[i]();
  }
  window.Modernizr = Modernizr;
}(window, document);
