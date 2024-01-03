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

window.addEventListener("scroll", function () {
  if (window.innerWidth > 600) {
    let scrollPosition = window.scrollY;

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

    let padding = Math.max(15, 30 - scrollPosition / 3);
    let paddingFlags = Math.max(20 - scrollPosition, -38); // 38 is the height of the shrunk case header
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

let title = document.title;

let getFormattedTitle = (titleHeading) => {
  let formattedTitle = `${titleHeading} - ${title}`;

  if (titleHeading === "Quick summary") {
    formattedTitle = `View quick summary for case - ${title}`;
  } else if (titleHeading === "Details") {
    formattedTitle = `Details for this case - ${title}`;
  } else if (titleHeading === "Licences") {
    formattedTitle = `View any licences on this case - ${title}`;
  } else if (titleHeading === "Contacts") {
    formattedTitle = `Add a contact to this case - ${title}`;
  } else if (titleHeading === "Queries") {
    formattedTitle = `Manage requests for information for this case - ${title}`;
  } else if (titleHeading === "Documents") {
    formattedTitle = `Attach or generate a document for this case - ${title}`;
  } else if (titleHeading === "Notes and timeline") {
    formattedTitle = `View notes and timeline for this case - ${title}`;
  } else if (titleHeading === "Product assessment") {
    formattedTitle = `Make or edit product assessments for this case - ${title}`;
  }

  return formattedTitle;
};

let setTitle = function () {
  let titleHeading = document.getElementsByClassName(
    "lite-tabs__tab--selected"
  )[0];
  if (titleHeading) {
    titleHeading = titleHeading.text.trim();
    document.title = getFormattedTitle(titleHeading);
  }
};
let elements = document.getElementsByClassName("lite-tabs__tab");

for (let i = 0; i < elements.length; i++) {
  elements[i].addEventListener("click", setTitle, false);
}
setTitle();

// this is used by case.html, this line solves the eslint issues
window.popupCenter = popupCenter;
