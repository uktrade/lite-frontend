$(".app-case-header__candy__popup").show();

const popupCenter = ({ url, title, w, h }) => {
  // Fixes dual-screen position                             Most browsers      Firefox
  const dualScreenLeft =
    window.screenLeft !== undefined ? window.screenLeft : window.screenX;
  const dualScreenTop =
    window.screenTop !== undefined ? window.screenTop : window.screenY;

  const width = window.innerWidth
    ? window.innerWidth
    : document.documentElement.clientWidth
    ? document.documentElement.clientWidth
    : screen.width;
  const height = window.innerHeight
    ? window.innerHeight
    : document.documentElement.clientHeight
    ? document.documentElement.clientHeight
    : screen.height;

  const systemZoom = width / window.screen.availWidth;
  const left = (width - w) / 2 / systemZoom + dualScreenLeft;
  const top = (height - h) / 2 / systemZoom + dualScreenTop;
  const newWindow = window.open(
    url,
    title,
    `
        scrollbars=yes,
        width=${w / systemZoom},
        height=${h / systemZoom},
        top=${top},
        left=${left}
        `
  );

  if (window.focus) newWindow.focus();
};

tippy(".app-case-header__candy", {
  content(reference) {
    return document.getElementById(
      $("#" + reference.getAttribute("id"))
        .next()
        .attr("id")
    );
  },
  allowHTML: true,
  interactive: true,
  animation: "scale-subtle",
  theme: "light",
  placement: "bottom",
  hideOnClick: false,
  interactiveBorder: 15,
});

var width = 0;
$(".app-case__flags-wrapper .app-flag").each(function () {
  width += $(this).outerWidth(true);
});
if (width > $(".app-case__flags-wrapper .app-flags").outerWidth(true)) {
  $(".app-case__flags-wrapper").addClass("app-case__flags-wrapper--fade");
}

window.addEventListener("scroll", function (e) {
  if (window.innerWidth > 600) {
    var scrollPosition = window.scrollY;

    if (scrollPosition > 10) {
      $("#case-flags").css({ "pointer-events": "none" });
    } else {
      $("#case-flags").css({ "pointer-events": "all" });
    }

    if (scrollPosition > 80) {
      $("#tab-bar").addClass("app-case-tab-bar--float");
    } else {
      $("#tab-bar").removeClass("app-case-tab-bar--float");
    }

    var padding = Math.max(15, 30 - scrollPosition / 3);
    var paddingFlags = Math.max(20 - scrollPosition, -38); // 38 is the height of the shrunk case header
    $(".app-case-tab-bar").css({
      "padding-top": Math.max(0, 20 - scrollPosition / 2),
    });
    $(
      ".app-case-tab-bar .lite-tabs__tab, .app-case-tab-bar .lite-tabs__tab-parent "
    ).css({
      "padding-top": Math.max(15, Math.min(20, 15 + scrollPosition / 2)),
      "padding-bottom": Math.max(15, Math.min(20, 15 + scrollPosition / 2)),
    });
    $(".app-case-header").css({
      "padding-top": padding,
      "padding-bottom": padding,
    });
    $(".app-case-header__breadcrumbs-list").css({
      opacity: 1 - scrollPosition / 10,
      transform: "translateY(" + -(30 - padding) + "px)",
      "margin-top": -(30 - padding) + "px",
      "margin-bottom": -(20 - padding) + "px",
    });
    $("#case-flags").css({
      opacity: 1 - scrollPosition / 10,
      transform: "translateY(" + -(30 - padding) + "px)",
      "margin-top": paddingFlags + "px",
    });
  }
});

var title = document.title;

var setTitle = function () {
  var title_heading = document
    .getElementsByClassName("lite-tabs__tab--selected")[0]
    .text.trim();
  document.title = `${title_heading} ${title}`;
};
var elements = document.getElementsByClassName("lite-tabs__tab");

for (var i = 0; i < elements.length; i++) {
  elements[i].addEventListener("click", setTitle, false);
}
setTitle();
