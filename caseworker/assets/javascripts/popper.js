/**
 * @popperjs/core v2.0.6 - MIT License
 */

"use strict";
!(function (e, t) {
  "object" == typeof exports && "undefined" != typeof module
    ? t(exports)
    : "function" == typeof define && define.amd
    ? define(["exports"], t)
    : t(((e = e || self).Popper = {}));
})(this, function (e) {
  function t(e) {
    return {
      width: (e = e.getBoundingClientRect()).width,
      height: e.height,
      top: e.top,
      right: e.right,
      bottom: e.bottom,
      left: e.left,
      x: e.left,
      y: e.top,
    };
  }
  function r(e) {
    return "[object Window]" !== e.toString()
      ? (e = e.ownerDocument)
        ? e.defaultView
        : window
      : e;
  }
  function n(e) {
    return { scrollLeft: (e = r(e)).pageXOffset, scrollTop: e.pageYOffset };
  }
  function o(e) {
    return e instanceof r(e).Element;
  }
  function i(e) {
    return e instanceof r(e).HTMLElement;
  }
  function a(e) {
    return e ? (e.nodeName || "").toLowerCase() : null;
  }
  function s(e) {
    return (o(e) ? e.ownerDocument : e.document).documentElement;
  }
  function f(e) {
    return t(s(e)).left + n(e).scrollLeft;
  }
  function p(e, o, p) {
    void 0 === p && (p = !1), (e = t(e));
    var c = { scrollLeft: 0, scrollTop: 0 },
      u = { x: 0, y: 0 };
    return (
      p ||
        ("body" !== a(o) &&
          (c =
            o !== r(o) && i(o)
              ? { scrollLeft: o.scrollLeft, scrollTop: o.scrollTop }
              : n(o)),
        i(o)
          ? (((u = t(o)).x += o.clientLeft), (u.y += o.clientTop))
          : (o = s(o)) && (u.x = f(o))),
      {
        x: e.left + c.scrollLeft - u.x,
        y: e.top + c.scrollTop - u.y,
        width: e.width,
        height: e.height,
      }
    );
  }
  function c(e) {
    return {
      x: e.offsetLeft,
      y: e.offsetTop,
      width: e.offsetWidth,
      height: e.offsetHeight,
    };
  }
  function u(e) {
    return "html" === a(e)
      ? e
      : e.parentNode ||
          e.host ||
          document.ownerDocument ||
          document.documentElement;
  }
  function d(e) {
    return r(e).getComputedStyle(e);
  }
  function l(e, t) {
    void 0 === t && (t = []);
    var n = (function e(t) {
      if (0 <= ["html", "body", "#document"].indexOf(a(t)))
        return t.ownerDocument.body;
      if (i(t)) {
        var r = d(t);
        if (
          /auto|scroll|overlay|hidden/.test(
            r.overflow + r.overflowY + r.overflowX
          )
        )
          return t;
      }
      return e(u(t));
    })(e);
    return (
      (n = (e = "body" === a(n)) ? r(n) : n),
      (t = t.concat(n)),
      e ? t : t.concat(l(u(n)))
    );
  }
  function m(e) {
    var t;
    return !i(e) ||
      !(t = e.offsetParent) ||
      (void 0 !== window.InstallTrigger && "fixed" === d(t).position)
      ? null
      : t;
  }
  function h(e) {
    var t = r(e);
    for (e = m(e); e && 0 <= ["table", "td", "th"].indexOf(a(e)); ) e = m(e);
    return e && "body" === a(e) && "static" === d(e).position ? t : e || t;
  }
  function v(e) {
    var t = new Map(),
      r = new Set(),
      n = [];
    return (
      e.forEach(function (e) {
        t.set(e.name, e);
      }),
      e.forEach(function (e) {
        r.has(e.name) ||
          (function e(o) {
            r.add(o.name),
              []
                .concat(o.requires || [], o.requiresIfExists || [])
                .forEach(function (n) {
                  r.has(n) || ((n = t.get(n)) && e(n));
                }),
              n.push(o);
          })(e);
      }),
      n
    );
  }
  function g(e) {
    var t;
    return function () {
      return (
        t ||
          (t = new Promise(function (r) {
            Promise.resolve().then(function () {
              (t = void 0), r(e());
            });
          })),
        t
      );
    };
  }
  function b(e) {
    return e.split("-")[0];
  }
  function y() {
    for (var e = arguments.length, t = Array(e), r = 0; r < e; r++)
      t[r] = arguments[r];
    return !t.some(function (e) {
      return !(e && "function" == typeof e.getBoundingClientRect);
    });
  }
  function x(e) {
    void 0 === e && (e = {});
    var t = e.defaultModifiers,
      r = void 0 === t ? [] : t,
      n = void 0 === (e = e.defaultOptions) ? F : e;
    return function (e, t, i) {
      function a() {
        f.forEach(function (e) {
          return e();
        }),
          (f = []);
      }
      void 0 === i && (i = n);
      var s = {
          placement: "bottom",
          orderedModifiers: [],
          options: Object.assign({}, F, {}, n),
          modifiersData: {},
          elements: { reference: e, popper: t },
          attributes: {},
          styles: {},
        },
        f = [],
        u = !1,
        d = {
          state: s,
          setOptions: function (i) {
            return (
              a(),
              (s.options = Object.assign({}, n, {}, s.options, {}, i)),
              (s.scrollParents = { reference: o(e) ? l(e) : [], popper: l(t) }),
              (i = (function (e) {
                var t = v(e);
                return C.reduce(function (e, r) {
                  return e.concat(
                    t.filter(function (e) {
                      return e.phase === r;
                    })
                  );
                }, []);
              })(
                (function (e) {
                  var t = e.reduce(function (e, t) {
                    var r = e[t.name];
                    return (
                      (e[t.name] = r
                        ? Object.assign({}, r, {}, t, {
                            options: Object.assign(
                              {},
                              r.options,
                              {},
                              t.options
                            ),
                            data: Object.assign({}, r.data, {}, t.data),
                          })
                        : t),
                      e
                    );
                  }, {});
                  return Object.keys(t).map(function (e) {
                    return t[e];
                  });
                })([].concat(r, s.options.modifiers))
              )),
              (s.orderedModifiers = i.filter(function (e) {
                return e.enabled;
              })),
              s.orderedModifiers.forEach(function (e) {
                var t = e.name,
                  r = e.options;
                (r = void 0 === r ? {} : r),
                  "function" == typeof (e = e.effect) &&
                    ((t = e({ state: s, name: t, instance: d, options: r })),
                    f.push(t || function () {}));
              }),
              d.update()
            );
          },
          forceUpdate: function () {
            if (!u) {
              var e = s.elements,
                t = e.reference;
              if (y(t, (e = e.popper)))
                for (
                  s.rects = {
                    reference: p(t, h(e), "fixed" === s.options.strategy),
                    popper: c(e),
                  },
                    s.reset = !1,
                    s.placement = s.options.placement,
                    s.orderedModifiers.forEach(function (e) {
                      return (s.modifiersData[e.name] = Object.assign(
                        {},
                        e.data
                      ));
                    }),
                    t = 0;
                  t < s.orderedModifiers.length;
                  t++
                )
                  if (!0 === s.reset) (s.reset = !1), (t = -1);
                  else {
                    var r = s.orderedModifiers[t];
                    e = r.fn;
                    var n = r.options;
                    (n = void 0 === n ? {} : n),
                      (r = r.name),
                      "function" == typeof e &&
                        (s =
                          e({ state: s, options: n, name: r, instance: d }) ||
                          s);
                  }
            }
          },
          update: g(function () {
            return new Promise(function (e) {
              d.forceUpdate(), e(s);
            });
          }),
          destroy: function () {
            a(), (u = !0);
          },
        };
      return y(e, t)
        ? (d.setOptions(i).then(function (e) {
            !u && i.onFirstUpdate && i.onFirstUpdate(e);
          }),
          d)
        : d;
    };
  }
  function w(e) {
    return 0 <= ["top", "bottom"].indexOf(e) ? "x" : "y";
  }
  function O(e) {
    var t = e.reference,
      r = e.element,
      n = (e = e.placement) ? b(e) : null;
    e = e ? e.split("-")[1] : null;
    var o = t.x + t.width / 2 - r.width / 2,
      i = t.y + t.height / 2 - r.height / 2;
    switch (n) {
      case "top":
        o = { x: o, y: t.y - r.height };
        break;
      case "bottom":
        o = { x: o, y: t.y + t.height };
        break;
      case "right":
        o = { x: t.x + t.width, y: i };
        break;
      case "left":
        o = { x: t.x - r.width, y: i };
        break;
      default:
        o = { x: t.x, y: t.y };
    }
    if (null != (n = n ? w(n) : null))
      switch (((i = "y" === n ? "height" : "width"), e)) {
        case "start":
          o[n] = Math.floor(o[n]) - Math.floor(t[i] / 2 - r[i] / 2);
          break;
        case "end":
          o[n] = Math.floor(o[n]) + Math.ceil(t[i] / 2 - r[i] / 2);
      }
    return o;
  }
  function M(e) {
    var t,
      n = e.popper,
      o = e.popperRect,
      i = e.placement,
      a = e.offsets,
      f = e.position,
      p = e.gpuAcceleration,
      c = e.adaptive,
      u = window.devicePixelRatio || 1;
    (e = Math.round(a.x * u) / u || 0), (u = Math.round(a.y * u) / u || 0);
    var d = a.hasOwnProperty("x");
    a = a.hasOwnProperty("y");
    var l,
      m = "left",
      v = "top",
      g = window;
    if (c) {
      var b = h(n);
      b === r(n) && (b = s(n)),
        "top" === i &&
          ((v = "bottom"), (u -= b.clientHeight - o.height), (u *= p ? 1 : -1)),
        "left" === i &&
          ((m = "right"), (e -= b.clientWidth - o.width), (e *= p ? 1 : -1));
    }
    return (
      (n = Object.assign({ position: f }, c && N)),
      p
        ? Object.assign(
            {},
            n,
            (((l = {})[v] = a ? "0" : ""),
            (l[m] = d ? "0" : ""),
            (l.transform =
              2 > (g.devicePixelRatio || 1)
                ? "translate(" + e + "px, " + u + "px)"
                : "translate3d(" + e + "px, " + u + "px, 0)"),
            l)
          )
        : Object.assign(
            {},
            n,
            (((t = {})[v] = a ? u + "px" : ""),
            (t[m] = d ? e + "px" : ""),
            (t.transform = ""),
            t)
          )
    );
  }
  function j(e) {
    return e.replace(/left|right|bottom|top/g, function (e) {
      return _[e];
    });
  }
  function D(e) {
    return e.replace(/start|end/g, function (e) {
      return U[e];
    });
  }
  function E(e, t) {
    var r = !(!t.getRootNode || !t.getRootNode().host);
    if (e.contains(t)) return !0;
    if (r)
      do {
        if (t && e.isSameNode(t)) return !0;
        t = t.parentNode || t.host;
      } while (t);
    return !1;
  }
  function k(e) {
    return Object.assign({}, e, {
      left: e.x,
      top: e.y,
      right: e.x + e.width,
      bottom: e.y + e.height,
    });
  }
  function L(e, o) {
    if ("viewport" === o)
      e = k({
        width: (e = r(e)).innerWidth,
        height: e.innerHeight,
        x: 0,
        y: 0,
      });
    else if (i(o)) e = t(o);
    else {
      var a = s(e);
      (e = r(a)),
        (o = n(a)),
        ((a = p(s(a), e)).height = Math.max(a.height, e.innerHeight)),
        (a.width = Math.max(a.width, e.innerWidth)),
        (a.x = -o.scrollLeft),
        (a.y = -o.scrollTop),
        (e = k(a));
    }
    return e;
  }
  function P(e, t, n) {
    return (
      (t =
        "clippingParents" === t
          ? (function (e) {
              var t = l(e),
                r =
                  0 <= ["absolute", "fixed"].indexOf(d(e).position) && i(e)
                    ? h(e)
                    : e;
              return o(r)
                ? t.filter(function (e) {
                    return o(e) && E(e, r);
                  })
                : [];
            })(e)
          : [].concat(t)),
      ((n = (n = [].concat(t, [n])).reduce(function (t, n) {
        var o = L(e, n),
          p = r((n = i(n) ? n : s(e))),
          c = i(n) ? d(n) : {};
        parseFloat(c.borderTopWidth);
        var u = parseFloat(c.borderRightWidth) || 0,
          l = parseFloat(c.borderBottomWidth) || 0,
          m = parseFloat(c.borderLeftWidth) || 0;
        c = "html" === a(n);
        var h = f(n),
          v = n.clientWidth + u,
          g = n.clientHeight + l;
        return (
          c && 50 < p.innerHeight - n.clientHeight && (g = p.innerHeight - l),
          (l = c ? 0 : n.clientTop),
          (u =
            n.clientLeft > m
              ? u
              : c
              ? p.innerWidth - v - h
              : n.offsetWidth - v),
          (p = c ? p.innerHeight - g : n.offsetHeight - g),
          (n = c ? h : n.clientLeft),
          (t.top = Math.max(o.top + l, t.top)),
          (t.right = Math.min(o.right - u, t.right)),
          (t.bottom = Math.min(o.bottom - p, t.bottom)),
          (t.left = Math.max(o.left + n, t.left)),
          t
        );
      }, L(e, n[0]))).width = n.right - n.left),
      (n.height = n.bottom - n.top),
      (n.x = n.left),
      (n.y = n.top),
      n
    );
  }
  function W(e) {
    return Object.assign({}, { top: 0, right: 0, bottom: 0, left: 0 }, {}, e);
  }
  function B(e, t) {
    return t.reduce(function (t, r) {
      return (t[r] = e), t;
    }, {});
  }
  function H(e, r) {
    void 0 === r && (r = {});
    var n = r;
    r = void 0 === (r = n.placement) ? e.placement : r;
    var i = n.boundary,
      a = void 0 === i ? "clippingParents" : i,
      f = void 0 === (i = n.rootBoundary) ? "viewport" : i;
    i = void 0 === (i = n.elementContext) ? "popper" : i;
    var p = n.altBoundary,
      c = void 0 !== p && p;
    n = W(
      "number" != typeof (n = void 0 === (n = n.padding) ? 0 : n) ? n : B(n, q)
    );
    var u = e.elements.reference;
    (p = e.rects.popper),
      (a = P(
        o((c = e.elements[c ? ("popper" === i ? "reference" : "popper") : i]))
          ? c
          : s(e.elements.popper),
        a,
        f
      )),
      (c = O({
        reference: (f = t(u)),
        element: p,
        strategy: "absolute",
        placement: r,
      })),
      (p = k(Object.assign({}, p, {}, c))),
      (f = "popper" === i ? p : f);
    var d = {
      top: a.top - f.top + n.top,
      bottom: f.bottom - a.bottom + n.bottom,
      left: a.left - f.left + n.left,
      right: f.right - a.right + n.right,
    };
    if (((e = e.modifiersData.offset), "popper" === i && e)) {
      var l = e[r];
      Object.keys(d).forEach(function (e) {
        var t = 0 <= ["right", "bottom"].indexOf(e) ? 1 : -1,
          r = 0 <= ["top", "bottom"].indexOf(e) ? "y" : "x";
        d[e] += l[r] * t;
      });
    }
    return d;
  }
  function R(e, t, r) {
    return (
      void 0 === r && (r = { x: 0, y: 0 }),
      {
        top: e.top - t.height - r.y,
        right: e.right - t.width + r.x,
        bottom: e.bottom - t.height + r.y,
        left: e.left - t.width - r.x,
      }
    );
  }
  function T(e) {
    return ["top", "right", "bottom", "left"].some(function (t) {
      return 0 <= e[t];
    });
  }
  var q = ["top", "bottom", "right", "left"],
    A = q.reduce(function (e, t) {
      return e.concat([t + "-start", t + "-end"]);
    }, []),
    S = [].concat(q, ["auto"]).reduce(function (e, t) {
      return e.concat([t, t + "-start", t + "-end"]);
    }, []),
    C =
      "beforeRead read afterRead beforeMain main afterMain beforeWrite write afterWrite".split(
        " "
      ),
    F = { placement: "bottom", modifiers: [], strategy: "absolute" },
    I = { passive: !0 },
    N = { top: "auto", right: "auto", bottom: "auto", left: "auto" },
    _ = { left: "right", right: "left", bottom: "top", top: "bottom" },
    U = { start: "end", end: "start" },
    V = [
      {
        name: "eventListeners",
        enabled: !0,
        phase: "write",
        fn: function () {},
        effect: function (e) {
          var t = e.state,
            n = e.instance,
            o = (e = e.options).scroll,
            i = void 0 === o || o,
            a = void 0 === (e = e.resize) || e,
            s = r(t.elements.popper),
            f = [].concat(t.scrollParents.reference, t.scrollParents.popper);
          return (
            i &&
              f.forEach(function (e) {
                e.addEventListener("scroll", n.update, I);
              }),
            a && s.addEventListener("resize", n.update, I),
            function () {
              i &&
                f.forEach(function (e) {
                  e.removeEventListener("scroll", n.update, I);
                }),
                a && s.removeEventListener("resize", n.update, I);
            }
          );
        },
        data: {},
      },
      {
        name: "popperOffsets",
        enabled: !0,
        phase: "read",
        fn: function (e) {
          var t = e.state;
          t.modifiersData[e.name] = O({
            reference: t.rects.reference,
            element: t.rects.popper,
            strategy: "absolute",
            placement: t.placement,
          });
        },
        data: {},
      },
      {
        name: "computeStyles",
        enabled: !0,
        phase: "beforeWrite",
        fn: function (e) {
          var t = e.state,
            r = e.options;
          (e = void 0 === (e = r.gpuAcceleration) || e),
            (r = void 0 === (r = r.adaptive) || r),
            (e = {
              placement: b(t.placement),
              popper: t.elements.popper,
              popperRect: t.rects.popper,
              gpuAcceleration: e,
            }),
            (t.styles.popper = Object.assign(
              {},
              t.styles.popper,
              {},
              M(
                Object.assign({}, e, {
                  offsets: t.modifiersData.popperOffsets,
                  position: t.options.strategy,
                  adaptive: r,
                })
              )
            )),
            null != t.modifiersData.arrow &&
              (t.styles.arrow = Object.assign(
                {},
                t.styles.arrow,
                {},
                M(
                  Object.assign({}, e, {
                    offsets: t.modifiersData.arrow,
                    position: "absolute",
                    adaptive: !1,
                  })
                )
              )),
            (t.attributes.popper = Object.assign({}, t.attributes.popper, {
              "data-popper-placement": t.placement,
            }));
        },
        data: {},
      },
      {
        name: "applyStyles",
        enabled: !0,
        phase: "write",
        fn: function (e) {
          var t = e.state;
          Object.keys(t.elements).forEach(function (e) {
            var r = t.styles[e] || {},
              n = t.attributes[e] || {},
              o = t.elements[e];
            i(o) &&
              a(o) &&
              (Object.assign(o.style, r),
              Object.keys(n).forEach(function (e) {
                var t = n[e];
                !1 === t
                  ? o.removeAttribute(e)
                  : o.setAttribute(e, !0 === t ? "" : t);
              }));
          });
        },
        effect: function (e) {
          var t = e.state,
            r = {
              popper: {
                position: "absolute",
                left: "0",
                top: "0",
                margin: "0",
              },
              arrow: { position: "absolute" },
              reference: {},
            };
          return (
            Object.assign(t.elements.popper.style, r.popper),
            t.elements.arrow && Object.assign(t.elements.arrow.style, r.arrow),
            function () {
              Object.keys(t.elements).forEach(function (e) {
                var n = t.elements[e],
                  o = t.attributes[e] || {};
                (e = Object.keys(
                  t.styles.hasOwnProperty(e) ? t.styles[e] : r[e]
                ).reduce(function (e, t) {
                  return (e[t] = ""), e;
                }, {})),
                  i(n) &&
                    a(n) &&
                    (Object.assign(n.style, e),
                    Object.keys(o).forEach(function (e) {
                      n.removeAttribute(e);
                    }));
              });
            }
          );
        },
        requires: ["computeStyles"],
      },
      {
        name: "offset",
        enabled: !0,
        phase: "main",
        requires: ["popperOffsets"],
        fn: function (e) {
          var t = e.state,
            r = e.name,
            n = void 0 === (e = e.options.offset) ? [0, 0] : e,
            o = (e = S.reduce(function (e, r) {
              var o = t.rects,
                i = b(r),
                a = 0 <= ["left", "top"].indexOf(i) ? -1 : 1,
                s =
                  "function" == typeof n
                    ? n(Object.assign({}, o, { placement: r }))
                    : n;
              return (
                (o = (o = s[0]) || 0),
                (s = ((s = s[1]) || 0) * a),
                (i =
                  0 <= ["left", "right"].indexOf(i)
                    ? { x: s, y: o }
                    : { x: o, y: s }),
                (e[r] = i),
                e
              );
            }, {}))[t.placement],
            i = o.y;
          (t.modifiersData.popperOffsets.x += o.x),
            (t.modifiersData.popperOffsets.y += i),
            (t.modifiersData[r] = e);
        },
      },
      {
        name: "flip",
        enabled: !0,
        phase: "main",
        fn: function (e) {
          var t = e.state,
            r = e.options;
          if (((e = e.name), !t.modifiersData[e]._skip)) {
            var n = r.fallbackPlacements,
              o = r.padding,
              i = r.boundary,
              a = r.rootBoundary,
              s = void 0 === (r = r.flipVariations) || r,
              f = b((r = t.options.placement));
            n =
              n ||
              (f !== r && s
                ? (function (e) {
                    if ("auto" === b(e)) return [];
                    var t = j(e);
                    return [D(e), t, D(t)];
                  })(r)
                : [j(r)]);
            var p = [r].concat(n).reduce(function (e, r) {
              return e.concat(
                "auto" === b(r)
                  ? (function (e, t) {
                      void 0 === t && (t = {});
                      var r = t.boundary,
                        n = t.rootBoundary,
                        o = t.padding,
                        i = t.flipVariations,
                        a = t.placement.split("-")[1],
                        s = (
                          a
                            ? i
                              ? A
                              : A.filter(function (e) {
                                  return e.split("-")[1] === a;
                                })
                            : q
                        ).reduce(function (t, i) {
                          return (
                            (t[i] = H(e, {
                              placement: i,
                              boundary: r,
                              rootBoundary: n,
                              padding: o,
                            })[b(i)]),
                            t
                          );
                        }, {});
                      return Object.keys(s).sort(function (e, t) {
                        return s[e] - s[t];
                      });
                    })(t, {
                      placement: r,
                      boundary: i,
                      rootBoundary: a,
                      padding: o,
                      flipVariations: s,
                    })
                  : r
              );
            }, []);
            (n = t.rects.reference), (r = t.rects.popper);
            var c = new Map();
            f = !0;
            for (var u = p[0], d = 0; d < p.length; d++) {
              var l = p[d],
                m = b(l),
                h = "start" === l.split("-")[1],
                v = 0 <= ["top", "bottom"].indexOf(m),
                g = v ? "width" : "height",
                y = H(t, {
                  placement: l,
                  boundary: i,
                  rootBoundary: a,
                  padding: o,
                });
              if (
                ((h = v ? (h ? "right" : "left") : h ? "bottom" : "top"),
                n[g] > r[g] && (h = j(h)),
                (g = j(h)),
                (m = [0 >= y[m], 0 >= y[h], 0 >= y[g]]).every(function (e) {
                  return e;
                }))
              ) {
                (u = l), (f = !1);
                break;
              }
              c.set(l, m);
            }
            if (f)
              for (
                n = function (e) {
                  var t = p.find(function (t) {
                    if ((t = c.get(t)))
                      return t.slice(0, e).every(function (e) {
                        return e;
                      });
                  });
                  if (t) return (u = t), "break";
                },
                  r = s ? 3 : 1;
                0 < r && "break" !== n(r);
                r--
              );
            t.placement !== u &&
              ((t.modifiersData[e]._skip = !0),
              (t.placement = u),
              (t.reset = !0));
          }
        },
        requiresIfExists: ["offset"],
        data: { _skip: !1 },
      },
      {
        name: "preventOverflow",
        enabled: !0,
        phase: "main",
        fn: function (e) {
          var t = e.state,
            r = e.options;
          e = e.name;
          var n = r.mainAxis,
            o = void 0 === n || n;
          n = void 0 !== (n = r.altAxis) && n;
          var i = r.tether;
          i = void 0 === i || i;
          var a = r.tetherOffset,
            s = void 0 === a ? 0 : a;
          (r = H(t, {
            boundary: r.boundary,
            rootBoundary: r.rootBoundary,
            padding: r.padding,
          })),
            (a = b(t.placement));
          var f = t.placement.split("-")[1],
            p = !f,
            u = w(a);
          a = "x" === u ? "y" : "x";
          var d = t.modifiersData.popperOffsets,
            l = t.rects.reference,
            m = t.rects.popper,
            h =
              "function" == typeof s
                ? s(Object.assign({}, t.rects, { placement: t.placement }))
                : s;
          if (((s = { x: 0, y: 0 }), o)) {
            var v = "y" === u ? "top" : "left",
              g = "y" === u ? "bottom" : "right",
              y = "y" === u ? "height" : "width";
            o = d[u];
            var x = d[u] + r[v],
              O = d[u] - r[g],
              M = i ? -m[y] / 2 : 0,
              j = "start" === f ? l[y] : m[y];
            (f = "start" === f ? -m[y] : -l[y]),
              (m = t.elements.arrow),
              (m = i && m ? c(m) : { width: 0, height: 0 });
            var D = t.modifiersData["arrow#persistent"]
              ? t.modifiersData["arrow#persistent"].padding
              : { top: 0, right: 0, bottom: 0, left: 0 };
            (v = D[v]),
              (g = D[g]),
              (m = Math.max(0, Math.min(l[y], m[y]))),
              (D = t.modifiersData.offset
                ? t.modifiersData.offset[t.placement][u]
                : 0),
              (j = d[u] + (p ? l[y] / 2 - M - m - v - h : j - m - v - h) - D),
              (p = d[u] + (p ? -l[y] / 2 + M + m + g + h : f + m + g + h) - D),
              (i = Math.max(
                i ? Math.min(x, j) : x,
                Math.min(o, i ? Math.max(O, p) : O)
              )),
              (d[u] = i),
              (s[u] = i - o);
          }
          n &&
            ((n = d[a]),
            (i = Math.max(
              n + r["x" === u ? "top" : "left"],
              Math.min(n, n - r["x" === u ? "bottom" : "right"])
            )),
            (t.modifiersData.popperOffsets[a] = i),
            (s[a] = i - n)),
            (t.modifiersData[e] = s);
        },
        requiresIfExists: ["offset"],
      },
      {
        name: "arrow",
        enabled: !0,
        phase: "main",
        fn: function (e) {
          var t,
            r = e.state;
          e = e.name;
          var n = r.elements.arrow,
            o = r.modifiersData.popperOffsets,
            i = b(r.placement),
            a = w(i);
          if (
            ((i = 0 <= ["left", "right"].indexOf(i) ? "height" : "width"), n)
          ) {
            var s = r.modifiersData[e + "#persistent"].padding;
            (n = c(n)),
              (o = Math.max(
                s["y" === a ? "top" : "left"],
                Math.min(
                  r.rects.popper[i] / 2 -
                    n[i] / 2 +
                    ((r.rects.reference[i] +
                      r.rects.reference[a] -
                      o[a] -
                      r.rects.popper[i]) /
                      2 -
                      (o[a] - r.rects.reference[a]) / 2),
                  r.rects.popper[i] - n[i] - s["y" === a ? "bottom" : "right"]
                )
              )),
              (r.modifiersData[e] = (((t = {})[a] = o), t));
          }
        },
        effect: function (e) {
          var t = e.state,
            r = e.options;
          e = e.name;
          var n = r.element;
          (n = void 0 === n ? "[data-popper-arrow]" : n),
            (r = void 0 === (r = r.padding) ? 0 : r),
            ("string" != typeof n ||
              (n = t.elements.popper.querySelector(n))) &&
              E(t.elements.popper, n) &&
              ((t.elements.arrow = n),
              (t.modifiersData[e + "#persistent"] = {
                padding: W("number" != typeof r ? r : B(r, q)),
              }));
        },
        requires: ["popperOffsets"],
        requiresIfExists: ["preventOverflow"],
      },
      {
        name: "hide",
        enabled: !0,
        phase: "main",
        requiresIfExists: ["preventOverflow"],
        fn: function (e) {
          var t = e.state;
          e = e.name;
          var r = t.rects.reference,
            n = t.rects.popper,
            o = t.modifiersData.preventOverflow,
            i = H(t, { elementContext: "reference" }),
            a = H(t, { altBoundary: !0 });
          (r = R(i, r)),
            (n = R(a, n, o)),
            (o = T(r)),
            (a = T(n)),
            (t.modifiersData[e] = {
              referenceClippingOffsets: r,
              popperEscapeOffsets: n,
              isReferenceHidden: o,
              hasPopperEscaped: a,
            }),
            (t.attributes.popper = Object.assign({}, t.attributes.popper, {
              "data-popper-reference-hidden": o,
              "data-popper-escaped": a,
            }));
        },
      },
    ],
    z = x({ defaultModifiers: V });
  (e.createPopper = z),
    (e.defaultModifiers = V),
    (e.popperGenerator = x),
    Object.defineProperty(e, "__esModule", { value: !0 });
});
