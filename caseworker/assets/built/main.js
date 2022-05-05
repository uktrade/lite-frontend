// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        this
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"1tmhj":[function(require,module,exports) {
"use strict";
var HMR_HOST = null;
var HMR_PORT = 1234;
var HMR_SECURE = false;
var HMR_ENV_HASH = "30f6e5d8ea47961b";
module.bundle.HMR_BUNDLE_ID = "d73af75824030688";
function _toConsumableArray(arr) {
    return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread();
}
function _nonIterableSpread() {
    throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}
function _iterableToArray(iter) {
    if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter);
}
function _arrayWithoutHoles(arr) {
    if (Array.isArray(arr)) return _arrayLikeToArray(arr);
}
function _createForOfIteratorHelper(o, allowArrayLike) {
    var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"];
    if (!it) {
        if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") {
            if (it) o = it;
            var i = 0;
            var F = function F() {};
            return {
                s: F,
                n: function n() {
                    if (i >= o.length) return {
                        done: true
                    };
                    return {
                        done: false,
                        value: o[i++]
                    };
                },
                e: function e(_e) {
                    throw _e;
                },
                f: F
            };
        }
        throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
    }
    var normalCompletion = true, didErr = false, err;
    return {
        s: function s() {
            it = it.call(o);
        },
        n: function n() {
            var step = it.next();
            normalCompletion = step.done;
            return step;
        },
        e: function e(_e2) {
            didErr = true;
            err = _e2;
        },
        f: function f() {
            try {
                if (!normalCompletion && it.return != null) it.return();
            } finally{
                if (didErr) throw err;
            }
        }
    };
}
function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === "string") return _arrayLikeToArray(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === "Object" && o.constructor) n = o.constructor.name;
    if (n === "Map" || n === "Set") return Array.from(o);
    if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen);
}
function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;
    for(var i = 0, arr2 = new Array(len); i < len; i++)arr2[i] = arr[i];
    return arr2;
}
/* global HMR_HOST, HMR_PORT, HMR_ENV_HASH, HMR_SECURE */ /*::
import type {
  HMRAsset,
  HMRMessage,
} from '@parcel/reporter-dev-server/src/HMRServer.js';
interface ParcelRequire {
  (string): mixed;
  cache: {|[string]: ParcelModule|};
  hotData: mixed;
  Module: any;
  parent: ?ParcelRequire;
  isParcelRequire: true;
  modules: {|[string]: [Function, {|[string]: string|}]|};
  HMR_BUNDLE_ID: string;
  root: ParcelRequire;
}
interface ParcelModule {
  hot: {|
    data: mixed,
    accept(cb: (Function) => void): void,
    dispose(cb: (mixed) => void): void,
    // accept(deps: Array<string> | string, cb: (Function) => void): void,
    // decline(): void,
    _acceptCallbacks: Array<(Function) => void>,
    _disposeCallbacks: Array<(mixed) => void>,
  |};
}
declare var module: {bundle: ParcelRequire, ...};
declare var HMR_HOST: string;
declare var HMR_PORT: string;
declare var HMR_ENV_HASH: string;
declare var HMR_SECURE: boolean;
*/ var OVERLAY_ID = '__parcel__error__overlay__';
var OldModule = module.bundle.Module;
function Module(moduleName) {
    OldModule.call(this, moduleName);
    this.hot = {
        data: module.bundle.hotData,
        _acceptCallbacks: [],
        _disposeCallbacks: [],
        accept: function accept(fn) {
            this._acceptCallbacks.push(fn || function() {});
        },
        dispose: function dispose(fn) {
            this._disposeCallbacks.push(fn);
        }
    };
    module.bundle.hotData = undefined;
}
module.bundle.Module = Module;
var checkedAssets, acceptedAssets, assetsToAccept /*: Array<[ParcelRequire, string]> */ ;
function getHostname() {
    return HMR_HOST || (location.protocol.indexOf('http') === 0 ? location.hostname : 'localhost');
}
function getPort() {
    return HMR_PORT || location.port;
} // eslint-disable-next-line no-redeclare
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== 'undefined') {
    var hostname = getHostname();
    var port = getPort();
    var protocol = HMR_SECURE || location.protocol == 'https:' && !/localhost|127.0.0.1|0.0.0.0/.test(hostname) ? 'wss' : 'ws';
    var ws = new WebSocket(protocol + '://' + hostname + (port ? ':' + port : '') + '/'); // $FlowFixMe
    ws.onmessage = function(event) {
        checkedAssets = {} /*: {|[string]: boolean|} */ ;
        acceptedAssets = {} /*: {|[string]: boolean|} */ ;
        assetsToAccept = [];
        var data = JSON.parse(event.data);
        if (data.type === 'update') {
            // Remove error overlay if there is one
            if (typeof document !== 'undefined') removeErrorOverlay();
            var assets = data.assets.filter(function(asset) {
                return asset.envHash === HMR_ENV_HASH;
            }); // Handle HMR Update
            var handled = assets.every(function(asset) {
                return asset.type === 'css' || asset.type === 'js' && hmrAcceptCheck(module.bundle.root, asset.id, asset.depsByBundle);
            });
            if (handled) {
                console.clear();
                assets.forEach(function(asset) {
                    hmrApply(module.bundle.root, asset);
                });
                for(var i = 0; i < assetsToAccept.length; i++){
                    var id = assetsToAccept[i][1];
                    if (!acceptedAssets[id]) hmrAcceptRun(assetsToAccept[i][0], id);
                }
            } else window.location.reload();
        }
        if (data.type === 'error') {
            // Log parcel errors to console
            var _iterator = _createForOfIteratorHelper(data.diagnostics.ansi), _step;
            try {
                for(_iterator.s(); !(_step = _iterator.n()).done;){
                    var ansiDiagnostic = _step.value;
                    var stack = ansiDiagnostic.codeframe ? ansiDiagnostic.codeframe : ansiDiagnostic.stack;
                    console.error('🚨 [parcel]: ' + ansiDiagnostic.message + '\n' + stack + '\n\n' + ansiDiagnostic.hints.join('\n'));
                }
            } catch (err) {
                _iterator.e(err);
            } finally{
                _iterator.f();
            }
            if (typeof document !== 'undefined') {
                // Render the fancy html overlay
                removeErrorOverlay();
                var overlay = createErrorOverlay(data.diagnostics.html); // $FlowFixMe
                document.body.appendChild(overlay);
            }
        }
    };
    ws.onerror = function(e) {
        console.error(e.message);
    };
    ws.onclose = function() {
        console.warn('[parcel] 🚨 Connection to the HMR server was lost');
    };
}
function removeErrorOverlay() {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
        overlay.remove();
        console.log('[parcel] ✨ Error resolved');
    }
}
function createErrorOverlay(diagnostics) {
    var overlay = document.createElement('div');
    overlay.id = OVERLAY_ID;
    var errorHTML = '<div style="background: black; opacity: 0.85; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; font-family: Menlo, Consolas, monospace; z-index: 9999;">';
    var _iterator2 = _createForOfIteratorHelper(diagnostics), _step2;
    try {
        for(_iterator2.s(); !(_step2 = _iterator2.n()).done;){
            var diagnostic = _step2.value;
            var stack = diagnostic.codeframe ? diagnostic.codeframe : diagnostic.stack;
            errorHTML += "\n      <div>\n        <div style=\"font-size: 18px; font-weight: bold; margin-top: 20px;\">\n          \uD83D\uDEA8 ".concat(diagnostic.message, "\n        </div>\n        <pre>").concat(stack, "</pre>\n        <div>\n          ").concat(diagnostic.hints.map(function(hint) {
                return '<div>💡 ' + hint + '</div>';
            }).join(''), "\n        </div>\n        ").concat(diagnostic.documentation ? "<div>\uD83D\uDCDD <a style=\"color: violet\" href=\"".concat(diagnostic.documentation, "\" target=\"_blank\">Learn more</a></div>") : '', "\n      </div>\n    ");
        }
    } catch (err) {
        _iterator2.e(err);
    } finally{
        _iterator2.f();
    }
    errorHTML += '</div>';
    overlay.innerHTML = errorHTML;
    return overlay;
}
function getParents(bundle, id) /*: Array<[ParcelRequire, string]> */ {
    var modules = bundle.modules;
    if (!modules) return [];
    var parents = [];
    var k, d, dep;
    for(k in modules)for(d in modules[k][1]){
        dep = modules[k][1][d];
        if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) parents.push([
            bundle,
            k
        ]);
    }
    if (bundle.parent) parents = parents.concat(getParents(bundle.parent, id));
    return parents;
}
function updateLink(link) {
    var newLink = link.cloneNode();
    newLink.onload = function() {
        if (link.parentNode !== null) // $FlowFixMe
        link.parentNode.removeChild(link);
    };
    newLink.setAttribute('href', link.getAttribute('href').split('?')[0] + '?' + Date.now()); // $FlowFixMe
    link.parentNode.insertBefore(newLink, link.nextSibling);
}
var cssTimeout = null;
function reloadCSS() {
    if (cssTimeout) return;
    cssTimeout = setTimeout(function() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for(var i = 0; i < links.length; i++){
            // $FlowFixMe[incompatible-type]
            var href = links[i].getAttribute('href');
            var hostname = getHostname();
            var servedFromHMRServer = hostname === 'localhost' ? new RegExp('^(https?:\\/\\/(0.0.0.0|127.0.0.1)|localhost):' + getPort()).test(href) : href.indexOf(hostname + ':' + getPort());
            var absolute = /^https?:\/\//i.test(href) && href.indexOf(window.location.origin) !== 0 && !servedFromHMRServer;
            if (!absolute) updateLink(links[i]);
        }
        cssTimeout = null;
    }, 50);
}
function hmrApply(bundle, asset) {
    var modules = bundle.modules;
    if (!modules) return;
    if (asset.type === 'css') reloadCSS();
    else if (asset.type === 'js') {
        var deps = asset.depsByBundle[bundle.HMR_BUNDLE_ID];
        if (deps) {
            if (modules[asset.id]) {
                // Remove dependencies that are removed and will become orphaned.
                // This is necessary so that if the asset is added back again, the cache is gone, and we prevent a full page reload.
                var oldDeps = modules[asset.id][1];
                for(var dep in oldDeps)if (!deps[dep] || deps[dep] !== oldDeps[dep]) {
                    var id = oldDeps[dep];
                    var parents = getParents(module.bundle.root, id);
                    if (parents.length === 1) hmrDelete(module.bundle.root, id);
                }
            }
            var fn = new Function('require', 'module', 'exports', asset.output);
            modules[asset.id] = [
                fn,
                deps
            ];
        } else if (bundle.parent) hmrApply(bundle.parent, asset);
    }
}
function hmrDelete(bundle, id1) {
    var modules = bundle.modules;
    if (!modules) return;
    if (modules[id1]) {
        // Collect dependencies that will become orphaned when this module is deleted.
        var deps = modules[id1][1];
        var orphans = [];
        for(var dep in deps){
            var parents = getParents(module.bundle.root, deps[dep]);
            if (parents.length === 1) orphans.push(deps[dep]);
        } // Delete the module. This must be done before deleting dependencies in case of circular dependencies.
        delete modules[id1];
        delete bundle.cache[id1]; // Now delete the orphans.
        orphans.forEach(function(id) {
            hmrDelete(module.bundle.root, id);
        });
    } else if (bundle.parent) hmrDelete(bundle.parent, id1);
}
function hmrAcceptCheck(bundle, id, depsByBundle) {
    if (hmrAcceptCheckOne(bundle, id, depsByBundle)) return true;
     // Traverse parents breadth first. All possible ancestries must accept the HMR update, or we'll reload.
    var parents = getParents(module.bundle.root, id);
    var accepted = false;
    while(parents.length > 0){
        var v = parents.shift();
        var a = hmrAcceptCheckOne(v[0], v[1], null);
        if (a) // If this parent accepts, stop traversing upward, but still consider siblings.
        accepted = true;
        else {
            // Otherwise, queue the parents in the next level upward.
            var p = getParents(module.bundle.root, v[1]);
            if (p.length === 0) {
                // If there are no parents, then we've reached an entry without accepting. Reload.
                accepted = false;
                break;
            }
            parents.push.apply(parents, _toConsumableArray(p));
        }
    }
    return accepted;
}
function hmrAcceptCheckOne(bundle, id, depsByBundle) {
    var modules = bundle.modules;
    if (!modules) return;
    if (depsByBundle && !depsByBundle[bundle.HMR_BUNDLE_ID]) {
        // If we reached the root bundle without finding where the asset should go,
        // there's nothing to do. Mark as "accepted" so we don't reload the page.
        if (!bundle.parent) return true;
        return hmrAcceptCheck(bundle.parent, id, depsByBundle);
    }
    if (checkedAssets[id]) return true;
    checkedAssets[id] = true;
    var cached = bundle.cache[id];
    assetsToAccept.push([
        bundle,
        id
    ]);
    if (!cached || cached.hot && cached.hot._acceptCallbacks.length) return true;
}
function hmrAcceptRun(bundle, id) {
    var cached = bundle.cache[id];
    bundle.hotData = {};
    if (cached && cached.hot) cached.hot.data = bundle.hotData;
    if (cached && cached.hot && cached.hot._disposeCallbacks.length) cached.hot._disposeCallbacks.forEach(function(cb) {
        cb(bundle.hotData);
    });
    delete bundle.cache[id];
    bundle(id);
    cached = bundle.cache[id];
    if (cached && cached.hot && cached.hot._acceptCallbacks.length) cached.hot._acceptCallbacks.forEach(function(cb) {
        var assetsToAlsoAccept = cb(function() {
            return getParents(module.bundle.root, id);
        });
        if (assetsToAlsoAccept && assetsToAccept.length) // $FlowFixMe[method-unbinding]
        assetsToAccept.push.apply(assetsToAccept, assetsToAlsoAccept);
    });
    acceptedAssets[id] = true;
}

},{}],"eqetV":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
// vendor JS
var _govukFrontend = require("govuk-frontend");
// our JS
var _definitionsJs = require("../../../core/assets/javascripts/definitions.js");
var _backLinkJs = require("../../../core/assets/javascripts/back-link.js");
var _bannerJs = require("../../../core/assets/javascripts/cookies/banner.js");
var _bannerJsDefault = parcelHelpers.interopDefault(_bannerJs);
// core
// TODO: can't rewrite these as ES6 imports yet as they are used by other templates
var _selectButtonsJs = require("../../../core/assets/javascripts/select-buttons.js");
var _filterBarJs = require("../../../core/assets/javascripts/filter-bar.js");
var _checkboxesJs = require("./checkboxes.js");
var _snackbarHideJs = require("./snackbar-hide.js");
// caseworker
var _menuTooltipsJs = require("./menu-tooltips.js");
var _menuTooltipsJsDefault = parcelHelpers.interopDefault(_menuTooltipsJs);
var _queuesMenuJs = require("./queues-menu.js");
var _queuesMenuJsDefault = parcelHelpers.interopDefault(_queuesMenuJs);
var _flagExpandersJs = require("./flag-expanders.js");
var _flagExpandersJsDefault = parcelHelpers.interopDefault(_flagExpandersJs);
var _reviewGoodJs = require("./review-good.js");
var _reviewGoodJsDefault = parcelHelpers.interopDefault(_reviewGoodJs);
var _showHideDestinationsJs = require("./show-hide-destinations.js");
var _showHideDestinationsJsDefault = parcelHelpers.interopDefault(_showHideDestinationsJs);
var _tauExporterSuggestionsJs = require("./tau-exporter-suggestions.js");
var _tauExporterSuggestionsJsDefault = parcelHelpers.interopDefault(_tauExporterSuggestionsJs);
// vendor styles
var _tippyCss = require("tippy.js/dist/tippy.css");
// our styles
var _stylesScss = require("../styles/styles.scss");
$(document).ready(function() {
    // init govuk
    _govukFrontend.initAll();
    // init our JS
    _menuTooltipsJsDefault.default();
    _queuesMenuJsDefault.default();
    _flagExpandersJsDefault.default();
    _reviewGoodJsDefault.default();
    _bannerJsDefault.default("app-cookie-banner", "js-accept-cookie");
    _showHideDestinationsJsDefault.default();
    _tauExporterSuggestionsJsDefault.default();
});

},{"govuk-frontend":"iWspS","../../../core/assets/javascripts/definitions.js":"k2qRb","../../../core/assets/javascripts/back-link.js":"8PnXz","../../../core/assets/javascripts/cookies/banner.js":"js6nW","../../../core/assets/javascripts/select-buttons.js":"7TpU4","../../../core/assets/javascripts/filter-bar.js":"VYyUs","./checkboxes.js":"6PcMs","./snackbar-hide.js":"g9cUM","./menu-tooltips.js":"2cI33","./queues-menu.js":"k6xY9","./flag-expanders.js":"eeUXK","./review-good.js":"5LSAo","./show-hide-destinations.js":"6WNFi","./tau-exporter-suggestions.js":"dZDBQ","tippy.js/dist/tippy.css":"2orud","../styles/styles.scss":"R1Zup","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"iWspS":[function(require,module,exports) {
var _helpers = require("@swc/helpers");
var global = arguments[3];
(function(global, factory) {
    factory(exports);
})(undefined, function(exports) {
    'use strict';
    var nodeListForEach = /**
 * TODO: Ideally this would be a NodeList.prototype.forEach polyfill
 * This seems to fail in IE8, requires more investigation.
 * See: https://github.com/imagitama/nodelist-foreach-polyfill
 */ function nodeListForEach(nodes, callback) {
        if (window.NodeList.prototype.forEach) return nodes.forEach(callback);
        for(var i = 0; i < nodes.length; i++)callback.call(window, nodes[i], i, nodes);
    };
    var generateUniqueID = // Used to generate a unique string, allows multiple instances of the component without
    // Them conflicting with each other.
    // https://stackoverflow.com/a/8809472
    function generateUniqueID() {
        var d = new Date().getTime();
        if (typeof window.performance !== 'undefined' && typeof window.performance.now === 'function') d += window.performance.now(); // use high-precision timer if available
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c === 'x' ? r : r & 3 | 8).toString(16);
        });
    };
    var Accordion = function Accordion($module) {
        this.$module = $module;
        this.moduleId = $module.getAttribute('id');
        this.$sections = $module.querySelectorAll('.govuk-accordion__section');
        this.$openAllButton = '';
        this.browserSupportsSessionStorage = helper.checkForSessionStorage();
        this.controlsClass = 'govuk-accordion__controls';
        this.openAllClass = 'govuk-accordion__open-all';
        this.iconClass = 'govuk-accordion__icon';
        this.sectionHeaderClass = 'govuk-accordion__section-header';
        this.sectionHeaderFocusedClass = 'govuk-accordion__section-header--focused';
        this.sectionHeadingClass = 'govuk-accordion__section-heading';
        this.sectionSummaryClass = 'govuk-accordion__section-summary';
        this.sectionButtonClass = 'govuk-accordion__section-button';
        this.sectionExpandedClass = 'govuk-accordion__section--expanded';
    };
    var Button = function Button($module) {
        this.$module = $module;
        this.debounceFormSubmitTimer = null;
    };
    var Details = function Details($module) {
        this.$module = $module;
    };
    var CharacterCount = function CharacterCount($module) {
        this.$module = $module;
        this.$textarea = $module.querySelector('.govuk-js-character-count');
        if (this.$textarea) this.$countMessage = $module.querySelector('[id="' + this.$textarea.id + '-info"]');
    };
    var Checkboxes = function Checkboxes($module) {
        this.$module = $module;
        this.$inputs = $module.querySelectorAll('input[type="checkbox"]');
    };
    var ErrorSummary = function ErrorSummary($module) {
        this.$module = $module;
    };
    var NotificationBanner = function NotificationBanner($module) {
        this.$module = $module;
    };
    var Header = function Header($module) {
        this.$module = $module;
        this.$menuButton = $module && $module.querySelector('.govuk-js-header-toggle');
        this.$menu = this.$menuButton && $module.querySelector('#' + this.$menuButton.getAttribute('aria-controls'));
    };
    var Radios = function Radios($module) {
        this.$module = $module;
        this.$inputs = $module.querySelectorAll('input[type="radio"]');
    };
    var Tabs = function Tabs($module) {
        this.$module = $module;
        this.$tabs = $module.querySelectorAll('.govuk-tabs__tab');
        this.keys = {
            left: 37,
            right: 39,
            up: 38,
            down: 40
        };
        this.jsHiddenClass = 'govuk-tabs__panel--hidden';
    };
    var initAll = function initAll(options) {
        // Set the options to an empty object by default if no options are passed.
        options = typeof options !== 'undefined' ? options : {};
        // Allow the user to initialise GOV.UK Frontend in only certain sections of the page
        // Defaults to the entire document if nothing is set.
        var scope = typeof options.scope !== 'undefined' ? options.scope : document;
        var $buttons = scope.querySelectorAll('[data-module="govuk-button"]');
        nodeListForEach($buttons, function($button) {
            new Button($button).init();
        });
        var $accordions = scope.querySelectorAll('[data-module="govuk-accordion"]');
        nodeListForEach($accordions, function($accordion) {
            new Accordion($accordion).init();
        });
        var $details = scope.querySelectorAll('[data-module="govuk-details"]');
        nodeListForEach($details, function($detail) {
            new Details($detail).init();
        });
        var $characterCounts = scope.querySelectorAll('[data-module="govuk-character-count"]');
        nodeListForEach($characterCounts, function($characterCount) {
            new CharacterCount($characterCount).init();
        });
        var $checkboxes = scope.querySelectorAll('[data-module="govuk-checkboxes"]');
        nodeListForEach($checkboxes, function($checkbox) {
            new Checkboxes($checkbox).init();
        });
        // Find first error summary module to enhance.
        var $errorSummary = scope.querySelector('[data-module="govuk-error-summary"]');
        new ErrorSummary($errorSummary).init();
        // Find first header module to enhance.
        var $toggleButton = scope.querySelector('[data-module="govuk-header"]');
        new Header($toggleButton).init();
        var $notificationBanners = scope.querySelectorAll('[data-module="govuk-notification-banner"]');
        nodeListForEach($notificationBanners, function($notificationBanner) {
            new NotificationBanner($notificationBanner).init();
        });
        var $radios = scope.querySelectorAll('[data-module="govuk-radios"]');
        nodeListForEach($radios, function($radio) {
            new Radios($radio).init();
        });
        var $tabs1 = scope.querySelectorAll('[data-module="govuk-tabs"]');
        nodeListForEach($tabs1, function($tabs) {
            new Tabs($tabs).init();
        });
    };
    (function(undefined) {
        // Detection from https://github.com/Financial-Times/polyfill-service/blob/master/packages/polyfill-library/polyfills/Object/defineProperty/detect.js
        var detect = // In IE8, defineProperty could only act on DOM elements, so full support
        // for the feature requires the ability to set a property on an arbitrary object
        'defineProperty' in Object && function() {
            try {
                var a = {};
                Object.defineProperty(a, 'test', {
                    value: 42
                });
                return true;
            } catch (e) {
                return false;
            }
        }();
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Object.defineProperty&flags=always
        (function(nativeDefineProperty) {
            var supportsAccessors = Object.prototype.hasOwnProperty('__defineGetter__');
            var ERR_ACCESSORS_NOT_SUPPORTED = 'Getters & setters cannot be defined on this javascript engine';
            var ERR_VALUE_ACCESSORS = 'A property cannot both have accessors and be writable or have a value';
            Object.defineProperty = function defineProperty(object, property, descriptor) {
                // Where native support exists, assume it
                if (nativeDefineProperty && (object === window || object === document || object === Element.prototype || object instanceof Element)) return nativeDefineProperty(object, property, descriptor);
                if (object === null || !(object instanceof Object || typeof object === 'object')) throw new TypeError('Object.defineProperty called on non-object');
                if (!(descriptor instanceof Object)) throw new TypeError('Property description must be an object');
                var propertyString = String(property);
                var hasValueOrWritable = 'value' in descriptor || 'writable' in descriptor;
                var getterType = 'get' in descriptor && _helpers.typeOf(descriptor.get);
                var setterType = 'set' in descriptor && _helpers.typeOf(descriptor.set);
                // handle descriptor.get
                if (getterType) {
                    if (getterType !== 'function') throw new TypeError('Getter must be a function');
                    if (!supportsAccessors) throw new TypeError(ERR_ACCESSORS_NOT_SUPPORTED);
                    if (hasValueOrWritable) throw new TypeError(ERR_VALUE_ACCESSORS);
                    Object.__defineGetter__.call(object, propertyString, descriptor.get);
                } else object[propertyString] = descriptor.value;
                // handle descriptor.set
                if (setterType) {
                    if (setterType !== 'function') throw new TypeError('Setter must be a function');
                    if (!supportsAccessors) throw new TypeError(ERR_ACCESSORS_NOT_SUPPORTED);
                    if (hasValueOrWritable) throw new TypeError(ERR_VALUE_ACCESSORS);
                    Object.__defineSetter__.call(object, propertyString, descriptor.set);
                }
                // OK to define value unconditionally - if a getter has been specified as well, an error would be thrown above
                if ('value' in descriptor) object[propertyString] = descriptor.value;
                return object;
            };
        })(Object.defineProperty);
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://github.com/Financial-Times/polyfill-service/blob/master/packages/polyfill-library/polyfills/Function/prototype/bind/detect.js
        var detect = 'bind' in Function.prototype;
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Function.prototype.bind&flags=always
        Object.defineProperty(Function.prototype, 'bind', {
            value: function bind(that) {
                // add necessary es5-shim utilities
                var $Array = Array;
                var $Object = Object;
                var ObjectPrototype = $Object.prototype;
                var ArrayPrototype = $Array.prototype;
                var Empty = function Empty() {};
                var to_string = ObjectPrototype.toString;
                var hasToStringTag = typeof Symbol === 'function' && _helpers.typeOf(Symbol.toStringTag) === 'symbol';
                var isCallable; /* inlined from https://npmjs.com/is-callable */ 
                var fnToStr = Function.prototype.toString, tryFunctionObject = function tryFunctionObject(value) {
                    try {
                        fnToStr.call(value);
                        return true;
                    } catch (e) {
                        return false;
                    }
                }, fnClass = '[object Function]', genClass = '[object GeneratorFunction]';
                isCallable = function isCallable(value) {
                    if (typeof value !== 'function') return false;
                    if (hasToStringTag) return tryFunctionObject(value);
                    var strClass = to_string.call(value);
                    return strClass === fnClass || strClass === genClass;
                };
                var array_slice = ArrayPrototype.slice;
                var array_concat = ArrayPrototype.concat;
                var array_push = ArrayPrototype.push;
                var max = Math.max;
                // /add necessary es5-shim utilities
                // 1. Let Target be the this value.
                var target = this;
                // 2. If IsCallable(Target) is false, throw a TypeError exception.
                if (!isCallable(target)) throw new TypeError('Function.prototype.bind called on incompatible ' + target);
                // 3. Let A be a new (possibly empty) internal list of all of the
                //   argument values provided after thisArg (arg1, arg2 etc), in order.
                // XXX slicedArgs will stand in for "A" if used
                var args = array_slice.call(arguments, 1); // for normal call
                // 4. Let F be a new native ECMAScript object.
                // 11. Set the [[Prototype]] internal property of F to the standard
                //   built-in Function prototype object as specified in 15.3.3.1.
                // 12. Set the [[Call]] internal property of F as described in
                //   15.3.4.5.1.
                // 13. Set the [[Construct]] internal property of F as described in
                //   15.3.4.5.2.
                // 14. Set the [[HasInstance]] internal property of F as described in
                //   15.3.4.5.3.
                var bound;
                var binder = function binder() {
                    if (this instanceof bound) {
                        // 15.3.4.5.2 [[Construct]]
                        // When the [[Construct]] internal method of a function object,
                        // F that was created using the bind function is called with a
                        // list of arguments ExtraArgs, the following steps are taken:
                        // 1. Let target be the value of F's [[TargetFunction]]
                        //   internal property.
                        // 2. If target has no [[Construct]] internal method, a
                        //   TypeError exception is thrown.
                        // 3. Let boundArgs be the value of F's [[BoundArgs]] internal
                        //   property.
                        // 4. Let args be a new list containing the same values as the
                        //   list boundArgs in the same order followed by the same
                        //   values as the list ExtraArgs in the same order.
                        // 5. Return the result of calling the [[Construct]] internal
                        //   method of target providing args as the arguments.
                        var result = target.apply(this, array_concat.call(args, array_slice.call(arguments)));
                        if ($Object(result) === result) return result;
                        return this;
                    } else // 15.3.4.5.1 [[Call]]
                    // When the [[Call]] internal method of a function object, F,
                    // which was created using the bind function is called with a
                    // this value and a list of arguments ExtraArgs, the following
                    // steps are taken:
                    // 1. Let boundArgs be the value of F's [[BoundArgs]] internal
                    //   property.
                    // 2. Let boundThis be the value of F's [[BoundThis]] internal
                    //   property.
                    // 3. Let target be the value of F's [[TargetFunction]] internal
                    //   property.
                    // 4. Let args be a new list containing the same values as the
                    //   list boundArgs in the same order followed by the same
                    //   values as the list ExtraArgs in the same order.
                    // 5. Return the result of calling the [[Call]] internal method
                    //   of target providing boundThis as the this value and
                    //   providing args as the arguments.
                    // equiv: target.call(this, ...boundArgs, ...args)
                    return target.apply(that, array_concat.call(args, array_slice.call(arguments)));
                };
                // 15. If the [[Class]] internal property of Target is "Function", then
                //     a. Let L be the length property of Target minus the length of A.
                //     b. Set the length own property of F to either 0 or L, whichever is
                //       larger.
                // 16. Else set the length own property of F to 0.
                var boundLength = max(0, target.length - args.length);
                // 17. Set the attributes of the length own property of F to the values
                //   specified in 15.3.5.1.
                var boundArgs = [];
                for(var i = 0; i < boundLength; i++)array_push.call(boundArgs, '$' + i);
                // XXX Build a dynamic function with desired amount of arguments is the only
                // way to set the length property of a function.
                // In environments where Content Security Policies enabled (Chrome extensions,
                // for ex.) all use of eval or Function costructor throws an exception.
                // However in all of these environments Function.prototype.bind exists
                // and so this code will never be executed.
                bound = Function('binder', 'return function (' + boundArgs.join(',') + '){ return binder.apply(this, arguments); }')(binder);
                if (target.prototype) {
                    Empty.prototype = target.prototype;
                    bound.prototype = new Empty();
                    // Clean up dangling references.
                    Empty.prototype = null;
                }
                // TODO
                // 18. Set the [[Extensible]] internal property of F to true.
                // TODO
                // 19. Let thrower be the [[ThrowTypeError]] function Object (13.2.3).
                // 20. Call the [[DefineOwnProperty]] internal method of F with
                //   arguments "caller", PropertyDescriptor {[[Get]]: thrower, [[Set]]:
                //   thrower, [[Enumerable]]: false, [[Configurable]]: false}, and
                //   false.
                // 21. Call the [[DefineOwnProperty]] internal method of F with
                //   arguments "arguments", PropertyDescriptor {[[Get]]: thrower,
                //   [[Set]]: thrower, [[Enumerable]]: false, [[Configurable]]: false},
                //   and false.
                // TODO
                // NOTE Function objects created using Function.prototype.bind do not
                // have a prototype property or the [[Code]], [[FormalParameters]], and
                // [[Scope]] internal properties.
                // XXX can't delete prototype in pure-js.
                // 22. Return F.
                return bound;
            }
        });
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://raw.githubusercontent.com/Financial-Times/polyfill-service/master/packages/polyfill-library/polyfills/DOMTokenList/detect.js
        var detect = 'DOMTokenList' in this && function(x) {
            return 'classList' in x ? !x.classList.toggle('x', false) && !x.className : true;
        }(document.createElement('x'));
        if (detect) return;
        // Polyfill from https://raw.githubusercontent.com/Financial-Times/polyfill-service/master/packages/polyfill-library/polyfills/DOMTokenList/polyfill.js
        (function(global1) {
            var nativeImpl = "DOMTokenList" in global1 && global1.DOMTokenList;
            if (!nativeImpl || !!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', 'svg') && !(document.createElementNS("http://www.w3.org/2000/svg", "svg").classList instanceof DOMTokenList)) global1.DOMTokenList = function() {
                var dpSupport = true;
                var defineGetter = function defineGetter(object, name, fn, configurable) {
                    if (Object.defineProperty) Object.defineProperty(object, name, {
                        configurable: false === dpSupport ? true : !!configurable,
                        get: fn
                    });
                    else object.__defineGetter__(name, fn);
                };
                /** Ensure the browser allows Object.defineProperty to be used on native JavaScript objects. */ try {
                    defineGetter({}, "support");
                } catch (e) {
                    dpSupport = false;
                }
                var _DOMTokenList = function _DOMTokenList(el, prop) {
                    var that = this;
                    var tokens = [];
                    var tokenMap = {};
                    var length = 0;
                    var maxLength = 0;
                    var addIndexGetter = function addIndexGetter(i) {
                        defineGetter(that, i, function() {
                            preop();
                            return tokens[i];
                        }, false);
                    };
                    var reindex = function reindex() {
                        /** Define getter functions for array-like access to the tokenList's contents. */ if (length >= maxLength) for(; maxLength < length; ++maxLength)addIndexGetter(maxLength);
                    };
                    /** Helper function called at the start of each class method. Internal use only. */ var preop = function preop() {
                        var error;
                        var i;
                        var args = arguments;
                        var rSpace = /\s+/;
                        /** Validate the token/s passed to an instance method, if any. */ if (args.length) {
                            for(i = 0; i < args.length; ++i)if (rSpace.test(args[i])) {
                                error = new SyntaxError('String "' + args[i] + '" ' + "contains" + ' an invalid character');
                                error.code = 5;
                                error.name = "InvalidCharacterError";
                                throw error;
                            }
                        }
                        /** Split the new value apart by whitespace*/ if (typeof el[prop] === "object") tokens = ("" + el[prop].baseVal).replace(/^\s+|\s+$/g, "").split(rSpace);
                        else tokens = ("" + el[prop]).replace(/^\s+|\s+$/g, "").split(rSpace);
                        /** Avoid treating blank strings as single-item token lists */ if ("" === tokens[0]) tokens = [];
                        /** Repopulate the internal token lists */ tokenMap = {};
                        for(i = 0; i < tokens.length; ++i)tokenMap[tokens[i]] = true;
                        length = tokens.length;
                        reindex();
                    };
                    /** Populate our internal token list if the targeted attribute of the subject element isn't empty. */ preop();
                    /** Return the number of tokens in the underlying string. Read-only. */ defineGetter(that, "length", function() {
                        preop();
                        return length;
                    });
                    /** Override the default toString/toLocaleString methods to return a space-delimited list of tokens when typecast. */ that.toLocaleString = that.toString = function() {
                        preop();
                        return tokens.join(" ");
                    };
                    that.item = function(idx) {
                        preop();
                        return tokens[idx];
                    };
                    that.contains = function(token) {
                        preop();
                        return !!tokenMap[token];
                    };
                    that.add = function() {
                        preop.apply(that, args = arguments);
                        for(var args, token, i = 0, l = args.length; i < l; ++i){
                            token = args[i];
                            if (!tokenMap[token]) {
                                tokens.push(token);
                                tokenMap[token] = true;
                            }
                        }
                        /** Update the targeted attribute of the attached element if the token list's changed. */ if (length !== tokens.length) {
                            length = tokens.length >>> 0;
                            if (typeof el[prop] === "object") el[prop].baseVal = tokens.join(" ");
                            else el[prop] = tokens.join(" ");
                            reindex();
                        }
                    };
                    that.remove = function() {
                        preop.apply(that, args = arguments);
                        /** Build a hash of token names to compare against when recollecting our token list. */ for(var args, ignore = {}, i = 0, t = []; i < args.length; ++i){
                            ignore[args[i]] = true;
                            delete tokenMap[args[i]];
                        }
                        /** Run through our tokens list and reassign only those that aren't defined in the hash declared above. */ for(i = 0; i < tokens.length; ++i)if (!ignore[tokens[i]]) t.push(tokens[i]);
                        tokens = t;
                        length = t.length >>> 0;
                        /** Update the targeted attribute of the attached element. */ if (typeof el[prop] === "object") el[prop].baseVal = tokens.join(" ");
                        else el[prop] = tokens.join(" ");
                        reindex();
                    };
                    that.toggle = function(token, force) {
                        preop.apply(that, [
                            token
                        ]);
                        /** Token state's being forced. */ if (undefined !== force) {
                            if (force) {
                                that.add(token);
                                return true;
                            } else {
                                that.remove(token);
                                return false;
                            }
                        }
                        /** Token already exists in tokenList. Remove it, and return FALSE. */ if (tokenMap[token]) {
                            that.remove(token);
                            return false;
                        }
                        /** Otherwise, add the token and return TRUE. */ that.add(token);
                        return true;
                    };
                    return that;
                };
                return _DOMTokenList;
            }();
            // Add second argument to native DOMTokenList.toggle() if necessary
            (function() {
                var e = document.createElement('span');
                if (!('classList' in e)) return;
                e.classList.toggle('x', false);
                if (!e.classList.contains('x')) return;
                e.classList.constructor.prototype.toggle = function toggle(token /*, force*/ ) {
                    var force = arguments[1];
                    if (force === undefined) {
                        var add = !this.contains(token);
                        this[add ? 'add' : 'remove'](token);
                        return add;
                    }
                    force = !!force;
                    this[force ? 'add' : 'remove'](token);
                    return force;
                };
            })();
            // Add multiple arguments to native DOMTokenList.add() if necessary
            (function() {
                var e = document.createElement('span');
                if (!('classList' in e)) return;
                e.classList.add('a', 'b');
                if (e.classList.contains('b')) return;
                var native = e.classList.constructor.prototype.add;
                e.classList.constructor.prototype.add = function() {
                    var args = arguments;
                    var l = arguments.length;
                    for(var i = 0; i < l; i++)native.call(this, args[i]);
                };
            })();
            // Add multiple arguments to native DOMTokenList.remove() if necessary
            (function() {
                var e = document.createElement('span');
                if (!('classList' in e)) return;
                e.classList.add('a');
                e.classList.add('b');
                e.classList.remove('a', 'b');
                if (!e.classList.contains('b')) return;
                var native = e.classList.constructor.prototype.remove;
                e.classList.constructor.prototype.remove = function() {
                    var args = arguments;
                    var l = arguments.length;
                    for(var i = 0; i < l; i++)native.call(this, args[i]);
                };
            })();
        })(this);
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://github.com/Financial-Times/polyfill-service/blob/master/packages/polyfill-library/polyfills/Document/detect.js
        var detect = "Document" in this;
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Document&flags=always
        if (typeof WorkerGlobalScope === "undefined" && typeof importScripts !== "function") {
            if (this.HTMLDocument) // HTMLDocument is an extension of Document.  If the browser has HTMLDocument but not Document, the former will suffice as an alias for the latter.
            this.Document = this.HTMLDocument;
            else {
                // Create an empty function to act as the missing constructor for the document object, attach the document object as its prototype.  The function needs to be anonymous else it is hoisted and causes the feature detect to prematurely pass, preventing the assignments below being made.
                this.Document = this.HTMLDocument = document.constructor = new Function('return function Document() {}')();
                this.Document.prototype = document;
            }
        }
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://github.com/Financial-Times/polyfill-service/blob/master/packages/polyfill-library/polyfills/Element/detect.js
        var detect = 'Element' in this && 'HTMLElement' in this;
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Element&flags=always
        (function() {
            var bodyCheck = // Apply Element prototype to the pre-existing DOM as soon as the body element appears.
            function bodyCheck() {
                if (!loopLimit--) clearTimeout(interval);
                if (document.body && !document.body.prototype && /(complete|interactive)/.test(document.readyState)) {
                    shiv(document, true);
                    if (interval && document.body.prototype) clearTimeout(interval);
                    return !!document.body.prototype;
                }
                return false;
            };
            // IE8
            if (window.Element && !window.HTMLElement) {
                window.HTMLElement = window.Element;
                return;
            }
            // create Element constructor
            window.Element = window.HTMLElement = new Function('return function Element() {}')();
            // generate sandboxed iframe
            var vbody = document.appendChild(document.createElement('body'));
            var frame = vbody.appendChild(document.createElement('iframe'));
            // use sandboxed iframe to replicate Element functionality
            var frameDocument = frame.contentWindow.document;
            var prototype = Element.prototype = frameDocument.appendChild(frameDocument.createElement('*'));
            var cache = {};
            // polyfill Element.prototype on an element
            var shiv = function(element, deep) {
                var childNodes = element.childNodes || [], index = -1, key, value, childNode;
                if (element.nodeType === 1 && element.constructor !== Element) {
                    element.constructor = Element;
                    for(key in cache){
                        value = cache[key];
                        element[key] = value;
                    }
                }
                while(childNode = deep && childNodes[++index])shiv(childNode, deep);
                return element;
            };
            var elements = document.getElementsByTagName('*');
            var nativeCreateElement = document.createElement;
            var interval;
            var loopLimit = 100;
            prototype.attachEvent('onpropertychange', function(event) {
                var propertyName = event.propertyName, nonValue = !cache.hasOwnProperty(propertyName), newValue = prototype[propertyName], oldValue = cache[propertyName], index = -1, element;
                while(element = elements[++index]){
                    if (element.nodeType === 1) {
                        if (nonValue || element[propertyName] === oldValue) element[propertyName] = newValue;
                    }
                }
                cache[propertyName] = newValue;
            });
            prototype.constructor = Element;
            if (!prototype.hasAttribute) // <Element>.hasAttribute
            prototype.hasAttribute = function hasAttribute(name) {
                return this.getAttribute(name) !== null;
            };
            if (!bodyCheck()) {
                document.onreadystatechange = bodyCheck;
                interval = setInterval(bodyCheck, 25);
            }
            // Apply to any new elements created after load
            document.createElement = function createElement(nodeName) {
                var element = nativeCreateElement(String(nodeName).toLowerCase());
                return shiv(element);
            };
            // remove sandboxed iframe
            document.removeChild(vbody);
        })();
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://raw.githubusercontent.com/Financial-Times/polyfill-service/8717a9e04ac7aff99b4980fbedead98036b0929a/packages/polyfill-library/polyfills/Element/prototype/classList/detect.js
        var detect = 'document' in this && "classList" in document.documentElement && 'Element' in this && 'classList' in Element.prototype && function() {
            var e = document.createElement('span');
            e.classList.add('a', 'b');
            return e.classList.contains('b');
        }();
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Element.prototype.classList&flags=always
        (function(global2) {
            var dpSupport = true;
            var defineGetter = function defineGetter(object, name, fn, configurable) {
                if (Object.defineProperty) Object.defineProperty(object, name, {
                    configurable: false === dpSupport ? true : !!configurable,
                    get: fn
                });
                else object.__defineGetter__(name, fn);
            };
            /** Ensure the browser allows Object.defineProperty to be used on native JavaScript objects. */ try {
                defineGetter({}, "support");
            } catch (e) {
                dpSupport = false;
            }
            /** Polyfills a property with a DOMTokenList */ var addProp = function(o, name, attr) {
                defineGetter(o.prototype, name, function() {
                    var tokenList;
                    var THIS = this, /** Prevent this from firing twice for some reason. What the hell, IE. */ gibberishProperty = "__defineGetter__DEFINE_PROPERTY" + name;
                    if (THIS[gibberishProperty]) return tokenList;
                    THIS[gibberishProperty] = true;
                    /**
           * IE8 can't define properties on native JavaScript objects, so we'll use a dumb hack instead.
           *
           * What this is doing is creating a dummy element ("reflection") inside a detached phantom node ("mirror")
           * that serves as the target of Object.defineProperty instead. While we could simply use the subject HTML
           * element instead, this would conflict with element types which use indexed properties (such as forms and
           * select lists).
           */ if (false === dpSupport) {
                        var visage;
                        var mirror = addProp.mirror || document.createElement("div");
                        var reflections = mirror.childNodes;
                        var l = reflections.length;
                        for(var i = 0; i < l; ++i)if (reflections[i]._R === THIS) {
                            visage = reflections[i];
                            break;
                        }
                        /** Couldn't find an element's reflection inside the mirror. Materialise one. */ visage || (visage = mirror.appendChild(document.createElement("div")));
                        tokenList = DOMTokenList.call(visage, THIS, attr);
                    } else tokenList = new DOMTokenList(THIS, attr);
                    defineGetter(THIS, name, function() {
                        return tokenList;
                    });
                    delete THIS[gibberishProperty];
                    return tokenList;
                }, true);
            };
            addProp(global2.Element, "classList", "className");
            addProp(global2.HTMLElement, "classList", "className");
            addProp(global2.HTMLLinkElement, "relList", "rel");
            addProp(global2.HTMLAnchorElement, "relList", "rel");
            addProp(global2.HTMLAreaElement, "relList", "rel");
        })(this);
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    // Initialize component
    Accordion.prototype.init = function() {
        // Check for module
        if (!this.$module) return;
        this.initControls();
        this.initSectionHeaders();
        // See if "Open all" button text should be updated
        var areAllSectionsOpen = this.checkIfAllSectionsOpen();
        this.updateOpenAllButton(areAllSectionsOpen);
    };
    // Initialise controls and set attributes
    Accordion.prototype.initControls = function() {
        // Create "Open all" button and set attributes
        this.$openAllButton = document.createElement('button');
        this.$openAllButton.setAttribute('type', 'button');
        this.$openAllButton.innerHTML = 'Open all <span class="govuk-visually-hidden">sections</span>';
        this.$openAllButton.setAttribute('class', this.openAllClass);
        this.$openAllButton.setAttribute('aria-expanded', 'false');
        this.$openAllButton.setAttribute('type', 'button');
        // Create control wrapper and add controls to it
        var accordionControls = document.createElement('div');
        accordionControls.setAttribute('class', this.controlsClass);
        accordionControls.appendChild(this.$openAllButton);
        this.$module.insertBefore(accordionControls, this.$module.firstChild);
        // Handle events for the controls
        this.$openAllButton.addEventListener('click', this.onOpenOrCloseAllToggle.bind(this));
    };
    // Initialise section headers
    Accordion.prototype.initSectionHeaders = function() {
        // Loop through section headers
        nodeListForEach(this.$sections, (function($section, i) {
            // Set header attributes
            var header = $section.querySelector('.' + this.sectionHeaderClass);
            this.initHeaderAttributes(header, i);
            this.setExpanded(this.isExpanded($section), $section);
            // Handle events
            header.addEventListener('click', this.onSectionToggle.bind(this, $section));
            // See if there is any state stored in sessionStorage and set the sections to
            // open or closed.
            this.setInitialState($section);
        }).bind(this));
    };
    // Set individual header attributes
    Accordion.prototype.initHeaderAttributes = function($headerWrapper, index) {
        var $module = this;
        var $span = $headerWrapper.querySelector('.' + this.sectionButtonClass);
        var $heading = $headerWrapper.querySelector('.' + this.sectionHeadingClass);
        var $summary = $headerWrapper.querySelector('.' + this.sectionSummaryClass);
        // Copy existing span element to an actual button element, for improved accessibility.
        var $button = document.createElement('button');
        $button.setAttribute('type', 'button');
        $button.setAttribute('id', this.moduleId + '-heading-' + (index + 1));
        $button.setAttribute('aria-controls', this.moduleId + '-content-' + (index + 1));
        // Copy all attributes (https://developer.mozilla.org/en-US/docs/Web/API/Element/attributes) from $span to $button
        for(var i = 0; i < $span.attributes.length; i++){
            var attr = $span.attributes.item(i);
            $button.setAttribute(attr.nodeName, attr.nodeValue);
        }
        $button.addEventListener('focusin', function(e) {
            if (!$headerWrapper.classList.contains($module.sectionHeaderFocusedClass)) $headerWrapper.className += ' ' + $module.sectionHeaderFocusedClass;
        });
        $button.addEventListener('blur', function(e) {
            $headerWrapper.classList.remove($module.sectionHeaderFocusedClass);
        });
        if (typeof $summary !== 'undefined' && $summary !== null) $button.setAttribute('aria-describedby', this.moduleId + '-summary-' + (index + 1));
        // $span could contain HTML elements (see https://www.w3.org/TR/2011/WD-html5-20110525/content-models.html#phrasing-content)
        $button.innerHTML = $span.innerHTML;
        $heading.removeChild($span);
        $heading.appendChild($button);
        // Add "+/-" icon
        var icon = document.createElement('span');
        icon.className = this.iconClass;
        icon.setAttribute('aria-hidden', 'true');
        $button.appendChild(icon);
    };
    // When section toggled, set and store state
    Accordion.prototype.onSectionToggle = function($section) {
        var expanded = this.isExpanded($section);
        this.setExpanded(!expanded, $section);
        // Store the state in sessionStorage when a change is triggered
        this.storeState($section);
    };
    // When Open/Close All toggled, set and store state
    Accordion.prototype.onOpenOrCloseAllToggle = function() {
        var $module = this;
        var $sections = this.$sections;
        var nowExpanded = !this.checkIfAllSectionsOpen();
        nodeListForEach($sections, function($section) {
            $module.setExpanded(nowExpanded, $section);
            // Store the state in sessionStorage when a change is triggered
            $module.storeState($section);
        });
        $module.updateOpenAllButton(nowExpanded);
    };
    // Set section attributes when opened/closed
    Accordion.prototype.setExpanded = function(expanded, $section) {
        var $button = $section.querySelector('.' + this.sectionButtonClass);
        $button.setAttribute('aria-expanded', expanded);
        if (expanded) $section.classList.add(this.sectionExpandedClass);
        else $section.classList.remove(this.sectionExpandedClass);
        // See if "Open all" button text should be updated
        var areAllSectionsOpen = this.checkIfAllSectionsOpen();
        this.updateOpenAllButton(areAllSectionsOpen);
    };
    // Get state of section
    Accordion.prototype.isExpanded = function($section) {
        return $section.classList.contains(this.sectionExpandedClass);
    };
    // Check if all sections are open
    Accordion.prototype.checkIfAllSectionsOpen = function() {
        // Get a count of all the Accordion sections
        var sectionsCount = this.$sections.length;
        // Get a count of all Accordion sections that are expanded
        var expandedSectionCount = this.$module.querySelectorAll('.' + this.sectionExpandedClass).length;
        var areAllSectionsOpen = sectionsCount === expandedSectionCount;
        return areAllSectionsOpen;
    };
    // Update "Open all" button
    Accordion.prototype.updateOpenAllButton = function(expanded) {
        var newButtonText = expanded ? 'Close all' : 'Open all';
        newButtonText += '<span class="govuk-visually-hidden"> sections</span>';
        this.$openAllButton.setAttribute('aria-expanded', expanded);
        this.$openAllButton.innerHTML = newButtonText;
    };
    // Check for `window.sessionStorage`, and that it actually works.
    var helper = {
        checkForSessionStorage: function checkForSessionStorage() {
            var testString = 'this is the test string';
            var result;
            try {
                window.sessionStorage.setItem(testString, testString);
                result = window.sessionStorage.getItem(testString) === testString.toString();
                window.sessionStorage.removeItem(testString);
                return result;
            } catch (exception) {
                if (typeof console === 'undefined' || typeof console.log === 'undefined') console.log('Notice: sessionStorage not available.');
            }
        }
    };
    // Set the state of the accordions in sessionStorage
    Accordion.prototype.storeState = function($section) {
        if (this.browserSupportsSessionStorage) {
            // We need a unique way of identifying each content in the accordion. Since
            // an `#id` should be unique and an `id` is required for `aria-` attributes
            // `id` can be safely used.
            var $button = $section.querySelector('.' + this.sectionButtonClass);
            if ($button) {
                var contentId = $button.getAttribute('aria-controls');
                var contentState = $button.getAttribute('aria-expanded');
                if (typeof contentId === 'undefined' && (typeof console === 'undefined' || typeof console.log === 'undefined')) console.error(new Error('No aria controls present in accordion section heading.'));
                if (typeof contentState === 'undefined' && (typeof console === 'undefined' || typeof console.log === 'undefined')) console.error(new Error('No aria expanded present in accordion section heading.'));
                // Only set the state when both `contentId` and `contentState` are taken from the DOM.
                if (contentId && contentState) window.sessionStorage.setItem(contentId, contentState);
            }
        }
    };
    // Read the state of the accordions from sessionStorage
    Accordion.prototype.setInitialState = function($section) {
        if (this.browserSupportsSessionStorage) {
            var $button = $section.querySelector('.' + this.sectionButtonClass);
            if ($button) {
                var contentId = $button.getAttribute('aria-controls');
                var contentState = contentId ? window.sessionStorage.getItem(contentId) : null;
                if (contentState !== null) this.setExpanded(contentState === 'true', $section);
            }
        }
    };
    (function(undefined) {
        // Detection from https://github.com/Financial-Times/polyfill-service/blob/master/packages/polyfill-library/polyfills/Window/detect.js
        var detect = 'Window' in this;
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Window&flags=always
        if (typeof WorkerGlobalScope === "undefined" && typeof importScripts !== "function") (function(global3) {
            if (global3.constructor) global3.Window = global3.constructor;
            else (global3.Window = global3.constructor = new Function('return function Window() {}')()).prototype = this;
        })(this);
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://github.com/Financial-Times/polyfill-service/blob/master/packages/polyfill-library/polyfills/Event/detect.js
        var detect = function(global4) {
            if (!('Event' in global4)) return false;
            if (typeof global4.Event === 'function') return true;
            try {
                // In IE 9-11, the Event object exists but cannot be instantiated
                new Event('click');
                return true;
            } catch (e) {
                return false;
            }
        }(this);
        if (detect) return;
        // Polyfill from https://cdn.polyfill.io/v2/polyfill.js?features=Event&flags=always
        (function() {
            var indexOf = function indexOf(array, element) {
                var index = -1, length = array.length;
                while(++index < length){
                    if (index in array && array[index] === element) return index;
                }
                return -1;
            };
            var unlistenableWindowEvents = {
                click: 1,
                dblclick: 1,
                keyup: 1,
                keypress: 1,
                keydown: 1,
                mousedown: 1,
                mouseup: 1,
                mousemove: 1,
                mouseover: 1,
                mouseenter: 1,
                mouseleave: 1,
                mouseout: 1,
                storage: 1,
                storagecommit: 1,
                textinput: 1
            };
            // This polyfill depends on availability of `document` so will not run in a worker
            // However, we asssume there are no browsers with worker support that lack proper
            // support for `Event` within the worker
            if (typeof document === 'undefined' || typeof window === 'undefined') return;
            var existingProto = window.Event && window.Event.prototype || null;
            window.Event = Window.prototype.Event = function Event(type, eventInitDict) {
                if (!type) throw new Error('Not enough arguments');
                var event;
                // Shortcut if browser supports createEvent
                if ('createEvent' in document) {
                    event = document.createEvent('Event');
                    var bubbles = eventInitDict && eventInitDict.bubbles !== undefined ? eventInitDict.bubbles : false;
                    var cancelable = eventInitDict && eventInitDict.cancelable !== undefined ? eventInitDict.cancelable : false;
                    event.initEvent(type, bubbles, cancelable);
                    return event;
                }
                event = document.createEventObject();
                event.type = type;
                event.bubbles = eventInitDict && eventInitDict.bubbles !== undefined ? eventInitDict.bubbles : false;
                event.cancelable = eventInitDict && eventInitDict.cancelable !== undefined ? eventInitDict.cancelable : false;
                return event;
            };
            if (existingProto) Object.defineProperty(window.Event, 'prototype', {
                configurable: false,
                enumerable: false,
                writable: true,
                value: existingProto
            });
            if (!('createEvent' in document)) {
                window.addEventListener = Window.prototype.addEventListener = Document.prototype.addEventListener = Element.prototype.addEventListener = function addEventListener() {
                    var element = this, type = arguments[0], listener = arguments[1];
                    if (element === window && type in unlistenableWindowEvents) throw new Error('In IE8 the event: ' + type + ' is not available on the window object. Please see https://github.com/Financial-Times/polyfill-service/issues/317 for more information.');
                    if (!element._events) element._events = {};
                    if (!element._events[type]) {
                        element._events[type] = function(event) {
                            var list = element._events[event.type].list, events = list.slice(), index = -1, length = events.length, eventElement;
                            event.preventDefault = function preventDefault() {
                                if (event.cancelable !== false) event.returnValue = false;
                            };
                            event.stopPropagation = function stopPropagation() {
                                event.cancelBubble = true;
                            };
                            event.stopImmediatePropagation = function stopImmediatePropagation() {
                                event.cancelBubble = true;
                                event.cancelImmediate = true;
                            };
                            event.currentTarget = element;
                            event.relatedTarget = event.fromElement || null;
                            event.target = event.target || event.srcElement || element;
                            event.timeStamp = new Date().getTime();
                            if (event.clientX) {
                                event.pageX = event.clientX + document.documentElement.scrollLeft;
                                event.pageY = event.clientY + document.documentElement.scrollTop;
                            }
                            while(++index < length && !event.cancelImmediate)if (index in events) {
                                eventElement = events[index];
                                if (indexOf(list, eventElement) !== -1 && typeof eventElement === 'function') eventElement.call(element, event);
                            }
                        };
                        element._events[type].list = [];
                        if (element.attachEvent) element.attachEvent('on' + type, element._events[type]);
                    }
                    element._events[type].list.push(listener);
                };
                window.removeEventListener = Window.prototype.removeEventListener = Document.prototype.removeEventListener = Element.prototype.removeEventListener = function removeEventListener() {
                    var element = this, type = arguments[0], listener = arguments[1], index;
                    if (element._events && element._events[type] && element._events[type].list) {
                        index = indexOf(element._events[type].list, listener);
                        if (index !== -1) {
                            element._events[type].list.splice(index, 1);
                            if (!element._events[type].list.length) {
                                if (element.detachEvent) element.detachEvent('on' + type, element._events[type]);
                                delete element._events[type];
                            }
                        }
                    }
                };
                window.dispatchEvent = Window.prototype.dispatchEvent = Document.prototype.dispatchEvent = Element.prototype.dispatchEvent = function dispatchEvent(event1) {
                    if (!arguments.length) throw new Error('Not enough arguments');
                    if (!event1 || typeof event1.type !== 'string') throw new Error('DOM Events Exception 0');
                    var element = this, type = event1.type;
                    try {
                        if (!event1.bubbles) {
                            event1.cancelBubble = true;
                            var cancelBubbleEvent = function(event) {
                                event.cancelBubble = true;
                                (element || window).detachEvent('on' + type, cancelBubbleEvent);
                            };
                            this.attachEvent('on' + type, cancelBubbleEvent);
                        }
                        this.fireEvent('on' + type, event1);
                    } catch (error) {
                        event1.target = element;
                        do {
                            event1.currentTarget = element;
                            if ('_events' in element && typeof element._events[type] === 'function') element._events[type].call(element, event1);
                            if (typeof element['on' + type] === 'function') element['on' + type].call(element, event1);
                            element = element.nodeType === 9 ? element.parentWindow : element.parentNode;
                        }while (element && !event1.cancelBubble)
                    }
                    return true;
                };
                // Add the DOMContentLoaded Event
                document.attachEvent('onreadystatechange', function() {
                    if (document.readyState === 'complete') document.dispatchEvent(new Event('DOMContentLoaded', {
                        bubbles: true
                    }));
                });
            }
        })();
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    var KEY_SPACE = 32;
    var DEBOUNCE_TIMEOUT_IN_SECONDS = 1;
    /**
* JavaScript 'shim' to trigger the click event of element(s) when the space key is pressed.
*
* Created since some Assistive Technologies (for example some Screenreaders)
* will tell a user to press space on a 'button', so this functionality needs to be shimmed
* See https://github.com/alphagov/govuk_elements/pull/272#issuecomment-233028270
*
* @param {object} event event
*/ Button.prototype.handleKeyDown = function(event) {
        // get the target element
        var target = event.target;
        // if the element has a role='button' and the pressed key is a space, we'll simulate a click
        if (target.getAttribute('role') === 'button' && event.keyCode === KEY_SPACE) {
            event.preventDefault();
            // trigger the target's click event
            target.click();
        }
    };
    /**
* If the click quickly succeeds a previous click then nothing will happen.
* This stops people accidentally causing multiple form submissions by
* double clicking buttons.
*/ Button.prototype.debounce = function(event) {
        var target = event.target;
        // Check the button that is clicked on has the preventDoubleClick feature enabled
        if (target.getAttribute('data-prevent-double-click') !== 'true') return;
        // If the timer is still running then we want to prevent the click from submitting the form
        if (this.debounceFormSubmitTimer) {
            event.preventDefault();
            return false;
        }
        this.debounceFormSubmitTimer = setTimeout((function() {
            this.debounceFormSubmitTimer = null;
        }).bind(this), DEBOUNCE_TIMEOUT_IN_SECONDS * 1000);
    };
    /**
* Initialise an event listener for keydown at document level
* this will help listening for later inserted elements with a role="button"
*/ Button.prototype.init = function() {
        this.$module.addEventListener('keydown', this.handleKeyDown);
        this.$module.addEventListener('click', this.debounce);
    };
    /**
 * JavaScript 'polyfill' for HTML5's <details> and <summary> elements
 * and 'shim' to add accessiblity enhancements for all browsers
 *
 * http://caniuse.com/#feat=details
 */ var KEY_ENTER = 13;
    var KEY_SPACE$1 = 32;
    Details.prototype.init = function() {
        if (!this.$module) return;
        // If there is native details support, we want to avoid running code to polyfill native behaviour.
        var hasNativeDetails = typeof this.$module.open === 'boolean';
        if (hasNativeDetails) return;
        this.polyfillDetails();
    };
    Details.prototype.polyfillDetails = function() {
        var $module = this.$module;
        // Save shortcuts to the inner summary and content elements
        var $summary = this.$summary = $module.getElementsByTagName('summary').item(0);
        var $content = this.$content = $module.getElementsByTagName('div').item(0);
        // If <details> doesn't have a <summary> and a <div> representing the content
        // it means the required HTML structure is not met so the script will stop
        if (!$summary || !$content) return;
        // If the content doesn't have an ID, assign it one now
        // which we'll need for the summary's aria-controls assignment
        if (!$content.id) $content.id = 'details-content-' + generateUniqueID();
        // Add ARIA role="group" to details
        $module.setAttribute('role', 'group');
        // Add role=button to summary
        $summary.setAttribute('role', 'button');
        // Add aria-controls
        $summary.setAttribute('aria-controls', $content.id);
        // Set tabIndex so the summary is keyboard accessible for non-native elements
        //
        // We have to use the camelcase `tabIndex` property as there is a bug in IE6/IE7 when we set the correct attribute lowercase:
        // See http://web.archive.org/web/20170120194036/http://www.saliences.com/browserBugs/tabIndex.html for more information.
        $summary.tabIndex = 0;
        // Detect initial open state
        var openAttr = $module.getAttribute('open') !== null;
        if (openAttr === true) {
            $summary.setAttribute('aria-expanded', 'true');
            $content.setAttribute('aria-hidden', 'false');
        } else {
            $summary.setAttribute('aria-expanded', 'false');
            $content.setAttribute('aria-hidden', 'true');
            $content.style.display = 'none';
        }
        // Bind an event to handle summary elements
        this.polyfillHandleInputs($summary, this.polyfillSetAttributes.bind(this));
    };
    /**
* Define a statechange function that updates aria-expanded and style.display
* @param {object} summary element
*/ Details.prototype.polyfillSetAttributes = function() {
        var $module = this.$module;
        var $summary = this.$summary;
        var $content = this.$content;
        var expanded = $summary.getAttribute('aria-expanded') === 'true';
        var hidden = $content.getAttribute('aria-hidden') === 'true';
        $summary.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        $content.setAttribute('aria-hidden', hidden ? 'false' : 'true');
        $content.style.display = expanded ? 'none' : '';
        var hasOpenAttr = $module.getAttribute('open') !== null;
        if (!hasOpenAttr) $module.setAttribute('open', 'open');
        else $module.removeAttribute('open');
        return true;
    };
    /**
* Handle cross-modal click events
* @param {object} node element
* @param {function} callback function
*/ Details.prototype.polyfillHandleInputs = function(node, callback) {
        node.addEventListener('keypress', function(event) {
            var target = event.target;
            // When the key gets pressed - check if it is enter or space
            if (event.keyCode === KEY_ENTER || event.keyCode === KEY_SPACE$1) {
                if (target.nodeName.toLowerCase() === 'summary') {
                    // Prevent space from scrolling the page
                    // and enter from submitting a form
                    event.preventDefault();
                    // Click to let the click event do all the necessary action
                    if (target.click) target.click();
                    else // except Safari 5.1 and under don't support .click() here
                    callback(event);
                }
            }
        });
        // Prevent keyup to prevent clicking twice in Firefox when using space key
        node.addEventListener('keyup', function(event) {
            var target = event.target;
            if (event.keyCode === KEY_SPACE$1) {
                if (target.nodeName.toLowerCase() === 'summary') event.preventDefault();
            }
        });
        node.addEventListener('click', callback);
    };
    CharacterCount.prototype.defaults = {
        characterCountAttribute: 'data-maxlength',
        wordCountAttribute: 'data-maxwords'
    };
    // Initialize component
    CharacterCount.prototype.init = function() {
        // Check for module
        var $module = this.$module;
        var $textarea = this.$textarea;
        var $countMessage = this.$countMessage;
        if (!$textarea || !$countMessage) return;
        // We move count message right after the field
        // Kept for backwards compatibility
        $textarea.insertAdjacentElement('afterend', $countMessage);
        // Read options set using dataset ('data-' values)
        this.options = this.getDataset($module);
        // Determine the limit attribute (characters or words)
        var countAttribute = this.defaults.characterCountAttribute;
        if (this.options.maxwords) countAttribute = this.defaults.wordCountAttribute;
        // Save the element limit
        this.maxLength = $module.getAttribute(countAttribute);
        // Check for limit
        if (!this.maxLength) return;
        // Remove hard limit if set
        $module.removeAttribute('maxlength');
        // When the page is restored after navigating 'back' in some browsers the
        // state of the character count is not restored until *after* the DOMContentLoaded
        // event is fired, so we need to sync after the pageshow event in browsers
        // that support it.
        if ('onpageshow' in window) window.addEventListener('pageshow', this.sync.bind(this));
        else window.addEventListener('DOMContentLoaded', this.sync.bind(this));
        this.sync();
    };
    CharacterCount.prototype.sync = function() {
        this.bindChangeEvents();
        this.updateCountMessage();
    };
    // Read data attributes
    CharacterCount.prototype.getDataset = function(element) {
        var dataset = {};
        var attributes = element.attributes;
        if (attributes) for(var i = 0; i < attributes.length; i++){
            var attribute = attributes[i];
            var match = attribute.name.match(/^data-(.+)/);
            if (match) dataset[match[1]] = attribute.value;
        }
        return dataset;
    };
    // Counts characters or words in text
    CharacterCount.prototype.count = function(text) {
        var length;
        if (this.options.maxwords) {
            var tokens = text.match(/\S+/g) || []; // Matches consecutive non-whitespace chars
            length = tokens.length;
        } else length = text.length;
        return length;
    };
    // Bind input propertychange to the elements and update based on the change
    CharacterCount.prototype.bindChangeEvents = function() {
        var $textarea = this.$textarea;
        $textarea.addEventListener('keyup', this.checkIfValueChanged.bind(this));
        // Bind focus/blur events to start/stop polling
        $textarea.addEventListener('focus', this.handleFocus.bind(this));
        $textarea.addEventListener('blur', this.handleBlur.bind(this));
    };
    // Speech recognition software such as Dragon NaturallySpeaking will modify the
    // fields by directly changing its `value`. These changes don't trigger events
    // in JavaScript, so we need to poll to handle when and if they occur.
    CharacterCount.prototype.checkIfValueChanged = function() {
        if (!this.$textarea.oldValue) this.$textarea.oldValue = '';
        if (this.$textarea.value !== this.$textarea.oldValue) {
            this.$textarea.oldValue = this.$textarea.value;
            this.updateCountMessage();
        }
    };
    // Update message box
    CharacterCount.prototype.updateCountMessage = function() {
        var countElement = this.$textarea;
        var options = this.options;
        var countMessage = this.$countMessage;
        // Determine the remaining number of characters/words
        var currentLength = this.count(countElement.value);
        var maxLength = this.maxLength;
        var remainingNumber = maxLength - currentLength;
        // Set threshold if presented in options
        var thresholdPercent = options.threshold ? options.threshold : 0;
        var thresholdValue = maxLength * thresholdPercent / 100;
        if (thresholdValue > currentLength) {
            countMessage.classList.add('govuk-character-count__message--disabled');
            // Ensure threshold is hidden for users of assistive technologies
            countMessage.setAttribute('aria-hidden', true);
        } else {
            countMessage.classList.remove('govuk-character-count__message--disabled');
            // Ensure threshold is visible for users of assistive technologies
            countMessage.removeAttribute('aria-hidden');
        }
        // Update styles
        if (remainingNumber < 0) {
            countElement.classList.add('govuk-textarea--error');
            countMessage.classList.remove('govuk-hint');
            countMessage.classList.add('govuk-error-message');
        } else {
            countElement.classList.remove('govuk-textarea--error');
            countMessage.classList.remove('govuk-error-message');
            countMessage.classList.add('govuk-hint');
        }
        // Update message
        var charVerb = 'remaining';
        var charNoun = 'character';
        var displayNumber = remainingNumber;
        if (options.maxwords) charNoun = 'word';
        charNoun = charNoun + (remainingNumber === -1 || remainingNumber === 1 ? '' : 's');
        charVerb = remainingNumber < 0 ? 'too many' : 'remaining';
        displayNumber = Math.abs(remainingNumber);
        countMessage.innerHTML = 'You have ' + displayNumber + ' ' + charNoun + ' ' + charVerb;
    };
    CharacterCount.prototype.handleFocus = function() {
        // Check if value changed on focus
        this.valueChecker = setInterval(this.checkIfValueChanged.bind(this), 1000);
    };
    CharacterCount.prototype.handleBlur = function() {
        // Cancel value checking on blur
        clearInterval(this.valueChecker);
    };
    /**
 * Initialise Checkboxes
 *
 * Checkboxes can be associated with a 'conditionally revealed' content block –
 * for example, a checkbox for 'Phone' could reveal an additional form field for
 * the user to enter their phone number.
 *
 * These associations are made using a `data-aria-controls` attribute, which is
 * promoted to an aria-controls attribute during initialisation.
 *
 * We also need to restore the state of any conditional reveals on the page (for
 * example if the user has navigated back), and set up event handlers to keep
 * the reveal in sync with the checkbox state.
 */ Checkboxes.prototype.init = function() {
        var $module = this.$module;
        var $inputs = this.$inputs;
        nodeListForEach($inputs, function($input) {
            var target = $input.getAttribute('data-aria-controls');
            // Skip checkboxes without data-aria-controls attributes, or where the
            // target element does not exist.
            if (!target || !$module.querySelector('#' + target)) return;
            // Promote the data-aria-controls attribute to a aria-controls attribute
            // so that the relationship is exposed in the AOM
            $input.setAttribute('aria-controls', target);
            $input.removeAttribute('data-aria-controls');
        });
        // When the page is restored after navigating 'back' in some browsers the
        // state of form controls is not restored until *after* the DOMContentLoaded
        // event is fired, so we need to sync after the pageshow event in browsers
        // that support it.
        if ('onpageshow' in window) window.addEventListener('pageshow', this.syncAllConditionalReveals.bind(this));
        else window.addEventListener('DOMContentLoaded', this.syncAllConditionalReveals.bind(this));
        // Although we've set up handlers to sync state on the pageshow or
        // DOMContentLoaded event, init could be called after those events have fired,
        // for example if they are added to the page dynamically, so sync now too.
        this.syncAllConditionalReveals();
        $module.addEventListener('click', this.handleClick.bind(this));
    };
    /**
 * Sync the conditional reveal states for all inputs in this $module.
 */ Checkboxes.prototype.syncAllConditionalReveals = function() {
        nodeListForEach(this.$inputs, this.syncConditionalRevealWithInputState.bind(this));
    };
    /**
 * Sync conditional reveal with the input state
 *
 * Synchronise the visibility of the conditional reveal, and its accessible
 * state, with the input's checked state.
 *
 * @param {HTMLInputElement} $input Checkbox input
 */ Checkboxes.prototype.syncConditionalRevealWithInputState = function($input) {
        var $target = this.$module.querySelector('#' + $input.getAttribute('aria-controls'));
        if ($target && $target.classList.contains('govuk-checkboxes__conditional')) {
            var inputIsChecked = $input.checked;
            $input.setAttribute('aria-expanded', inputIsChecked);
            $target.classList.toggle('govuk-checkboxes__conditional--hidden', !inputIsChecked);
        }
    };
    /**
 * Uncheck other checkboxes
 *
 * Find any other checkbox inputs with the same name value, and uncheck them.
 * This is useful for when a “None of these" checkbox is checked.
 */ Checkboxes.prototype.unCheckAllInputsExcept = function($input) {
        var allInputsWithSameName = document.querySelectorAll('input[type="checkbox"][name="' + $input.name + '"]');
        nodeListForEach(allInputsWithSameName, function($inputWithSameName) {
            var hasSameFormOwner = $input.form === $inputWithSameName.form;
            if (hasSameFormOwner && $inputWithSameName !== $input) $inputWithSameName.checked = false;
        });
        this.syncAllConditionalReveals();
    };
    /**
 * Uncheck exclusive inputs
 *
 * Find any checkbox inputs with the same name value and the 'exclusive' behaviour,
 * and uncheck them. This helps prevent someone checking both a regular checkbox and a
 * "None of these" checkbox in the same fieldset.
 */ Checkboxes.prototype.unCheckExclusiveInputs = function($input) {
        var allInputsWithSameNameAndExclusiveBehaviour = document.querySelectorAll('input[data-behaviour="exclusive"][type="checkbox"][name="' + $input.name + '"]');
        nodeListForEach(allInputsWithSameNameAndExclusiveBehaviour, function($exclusiveInput) {
            var hasSameFormOwner = $input.form === $exclusiveInput.form;
            if (hasSameFormOwner) $exclusiveInput.checked = false;
        });
        this.syncAllConditionalReveals();
    };
    /**
 * Click event handler
 *
 * Handle a click within the $module – if the click occurred on a checkbox, sync
 * the state of any associated conditional reveal with the checkbox state.
 *
 * @param {MouseEvent} event Click event
 */ Checkboxes.prototype.handleClick = function(event) {
        var $target = event.target;
        // Ignore clicks on things that aren't checkbox inputs
        if ($target.type !== 'checkbox') return;
        // If the checkbox conditionally-reveals some content, sync the state
        var hasAriaControls = $target.getAttribute('aria-controls');
        if (hasAriaControls) this.syncConditionalRevealWithInputState($target);
        // No further behaviour needed for unchecking
        if (!$target.checked) return;
        // Handle 'exclusive' checkbox behaviour (ie "None of these")
        var hasBehaviourExclusive = $target.getAttribute('data-behaviour') === 'exclusive';
        if (hasBehaviourExclusive) this.unCheckAllInputsExcept($target);
        else this.unCheckExclusiveInputs($target);
    };
    (function(undefined) {
        // Detection from https://raw.githubusercontent.com/Financial-Times/polyfill-service/1f3c09b402f65bf6e393f933a15ba63f1b86ef1f/packages/polyfill-library/polyfills/Element/prototype/matches/detect.js
        var detect = 'document' in this && "matches" in document.documentElement;
        if (detect) return;
        // Polyfill from https://raw.githubusercontent.com/Financial-Times/polyfill-service/1f3c09b402f65bf6e393f933a15ba63f1b86ef1f/packages/polyfill-library/polyfills/Element/prototype/matches/polyfill.js
        Element.prototype.matches = Element.prototype.webkitMatchesSelector || Element.prototype.oMatchesSelector || Element.prototype.msMatchesSelector || Element.prototype.mozMatchesSelector || function matches(selector) {
            var element = this;
            var elements = (element.document || element.ownerDocument).querySelectorAll(selector);
            var index = 0;
            while(elements[index] && elements[index] !== element)++index;
            return !!elements[index];
        };
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://raw.githubusercontent.com/Financial-Times/polyfill-service/1f3c09b402f65bf6e393f933a15ba63f1b86ef1f/packages/polyfill-library/polyfills/Element/prototype/closest/detect.js
        var detect = 'document' in this && "closest" in document.documentElement;
        if (detect) return;
        // Polyfill from https://raw.githubusercontent.com/Financial-Times/polyfill-service/1f3c09b402f65bf6e393f933a15ba63f1b86ef1f/packages/polyfill-library/polyfills/Element/prototype/closest/polyfill.js
        Element.prototype.closest = function closest(selector) {
            var node = this;
            while(node){
                if (node.matches(selector)) return node;
                else node = 'SVGElement' in window && node instanceof SVGElement ? node.parentNode : node.parentElement;
            }
            return null;
        };
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    ErrorSummary.prototype.init = function() {
        var $module = this.$module;
        if (!$module) return;
        $module.focus();
        $module.addEventListener('click', this.handleClick.bind(this));
    };
    /**
* Click event handler
*
* @param {MouseEvent} event - Click event
*/ ErrorSummary.prototype.handleClick = function(event) {
        var target = event.target;
        if (this.focusTarget(target)) event.preventDefault();
    };
    /**
 * Focus the target element
 *
 * By default, the browser will scroll the target into view. Because our labels
 * or legends appear above the input, this means the user will be presented with
 * an input without any context, as the label or legend will be off the top of
 * the screen.
 *
 * Manually handling the click event, scrolling the question into view and then
 * focussing the element solves this.
 *
 * This also results in the label and/or legend being announced correctly in
 * NVDA (as tested in 2018.3.2) - without this only the field type is announced
 * (e.g. "Edit, has autocomplete").
 *
 * @param {HTMLElement} $target - Event target
 * @returns {boolean} True if the target was able to be focussed
 */ ErrorSummary.prototype.focusTarget = function($target) {
        // If the element that was clicked was not a link, return early
        if ($target.tagName !== 'A' || $target.href === false) return false;
        var inputId = this.getFragmentFromUrl($target.href);
        var $input = document.getElementById(inputId);
        if (!$input) return false;
        var $legendOrLabel = this.getAssociatedLegendOrLabel($input);
        if (!$legendOrLabel) return false;
        // Scroll the legend or label into view *before* calling focus on the input to
        // avoid extra scrolling in browsers that don't support `preventScroll` (which
        // at time of writing is most of them...)
        $legendOrLabel.scrollIntoView();
        $input.focus({
            preventScroll: true
        });
        return true;
    };
    /**
 * Get fragment from URL
 *
 * Extract the fragment (everything after the hash) from a URL, but not including
 * the hash.
 *
 * @param {string} url - URL
 * @returns {string} Fragment from URL, without the hash
 */ ErrorSummary.prototype.getFragmentFromUrl = function(url) {
        if (url.indexOf('#') === -1) return false;
        return url.split('#').pop();
    };
    /**
 * Get associated legend or label
 *
 * Returns the first element that exists from this list:
 *
 * - The `<legend>` associated with the closest `<fieldset>` ancestor, as long
 *   as the top of it is no more than half a viewport height away from the
 *   bottom of the input
 * - The first `<label>` that is associated with the input using for="inputId"
 * - The closest parent `<label>`
 *
 * @param {HTMLElement} $input - The input
 * @returns {HTMLElement} Associated legend or label, or null if no associated
 *                        legend or label can be found
 */ ErrorSummary.prototype.getAssociatedLegendOrLabel = function($input) {
        var $fieldset = $input.closest('fieldset');
        if ($fieldset) {
            var legends = $fieldset.getElementsByTagName('legend');
            if (legends.length) {
                var $candidateLegend = legends[0];
                // If the input type is radio or checkbox, always use the legend if there
                // is one.
                if ($input.type === 'checkbox' || $input.type === 'radio') return $candidateLegend;
                // For other input types, only scroll to the fieldset’s legend (instead of
                // the label associated with the input) if the input would end up in the
                // top half of the screen.
                //
                // This should avoid situations where the input either ends up off the
                // screen, or obscured by a software keyboard.
                var legendTop = $candidateLegend.getBoundingClientRect().top;
                var inputRect = $input.getBoundingClientRect();
                // If the browser doesn't support Element.getBoundingClientRect().height
                // or window.innerHeight (like IE8), bail and just link to the label.
                if (inputRect.height && window.innerHeight) {
                    var inputBottom = inputRect.top + inputRect.height;
                    if (inputBottom - legendTop < window.innerHeight / 2) return $candidateLegend;
                }
            }
        }
        return document.querySelector("label[for='" + $input.getAttribute('id') + "']") || $input.closest('label');
    };
    /**
 * Initialise the component
 */ NotificationBanner.prototype.init = function() {
        var $module = this.$module;
        // Check for module
        if (!$module) return;
        this.setFocus();
    };
    /**
 * Focus the element
 *
 * If `role="alert"` is set, focus the element to help some assistive technologies
 * prioritise announcing it.
 *
 * You can turn off the auto-focus functionality by setting `data-disable-auto-focus="true"` in the
 * component HTML. You might wish to do this based on user research findings, or to avoid a clash
 * with another element which should be focused when the page loads.
 */ NotificationBanner.prototype.setFocus = function() {
        var $module = this.$module;
        if ($module.getAttribute('data-disable-auto-focus') === 'true') return;
        if ($module.getAttribute('role') !== 'alert') return;
        // Set tabindex to -1 to make the element focusable with JavaScript.
        // Remove the tabindex on blur as the component doesn't need to be focusable after the page has
        // loaded.
        if (!$module.getAttribute('tabindex')) {
            $module.setAttribute('tabindex', '-1');
            $module.addEventListener('blur', function() {
                $module.removeAttribute('tabindex');
            });
        }
        $module.focus();
    };
    /**
 * Initialise header
 *
 * Check for the presence of the header, menu and menu button – if any are
 * missing then there's nothing to do so return early.
 */ Header.prototype.init = function() {
        if (!this.$module || !this.$menuButton || !this.$menu) return;
        this.syncState(this.$menu.classList.contains('govuk-header__navigation--open'));
        this.$menuButton.addEventListener('click', this.handleMenuButtonClick.bind(this));
    };
    /**
 * Sync menu state
 *
 * Sync the menu button class and the accessible state of the menu and the menu
 * button with the visible state of the menu
 *
 * @param {boolean} isVisible Whether the menu is currently visible
 */ Header.prototype.syncState = function(isVisible) {
        this.$menuButton.classList.toggle('govuk-header__menu-button--open', isVisible);
        this.$menuButton.setAttribute('aria-expanded', isVisible);
    };
    /**
 * Handle menu button click
 *
 * When the menu button is clicked, change the visibility of the menu and then
 * sync the accessibility state and menu button state
 */ Header.prototype.handleMenuButtonClick = function() {
        var isVisible = this.$menu.classList.toggle('govuk-header__navigation--open');
        this.syncState(isVisible);
    };
    /**
 * Initialise Radios
 *
 * Radios can be associated with a 'conditionally revealed' content block – for
 * example, a radio for 'Phone' could reveal an additional form field for the
 * user to enter their phone number.
 *
 * These associations are made using a `data-aria-controls` attribute, which is
 * promoted to an aria-controls attribute during initialisation.
 *
 * We also need to restore the state of any conditional reveals on the page (for
 * example if the user has navigated back), and set up event handlers to keep
 * the reveal in sync with the radio state.
 */ Radios.prototype.init = function() {
        var $module = this.$module;
        var $inputs = this.$inputs;
        nodeListForEach($inputs, function($input) {
            var target = $input.getAttribute('data-aria-controls');
            // Skip radios without data-aria-controls attributes, or where the
            // target element does not exist.
            if (!target || !$module.querySelector('#' + target)) return;
            // Promote the data-aria-controls attribute to a aria-controls attribute
            // so that the relationship is exposed in the AOM
            $input.setAttribute('aria-controls', target);
            $input.removeAttribute('data-aria-controls');
        });
        // When the page is restored after navigating 'back' in some browsers the
        // state of form controls is not restored until *after* the DOMContentLoaded
        // event is fired, so we need to sync after the pageshow event in browsers
        // that support it.
        if ('onpageshow' in window) window.addEventListener('pageshow', this.syncAllConditionalReveals.bind(this));
        else window.addEventListener('DOMContentLoaded', this.syncAllConditionalReveals.bind(this));
        // Although we've set up handlers to sync state on the pageshow or
        // DOMContentLoaded event, init could be called after those events have fired,
        // for example if they are added to the page dynamically, so sync now too.
        this.syncAllConditionalReveals();
        // Handle events
        $module.addEventListener('click', this.handleClick.bind(this));
    };
    /**
 * Sync the conditional reveal states for all inputs in this $module.
 */ Radios.prototype.syncAllConditionalReveals = function() {
        nodeListForEach(this.$inputs, this.syncConditionalRevealWithInputState.bind(this));
    };
    /**
 * Sync conditional reveal with the input state
 *
 * Synchronise the visibility of the conditional reveal, and its accessible
 * state, with the input's checked state.
 *
 * @param {HTMLInputElement} $input Radio input
 */ Radios.prototype.syncConditionalRevealWithInputState = function($input) {
        var $target = document.querySelector('#' + $input.getAttribute('aria-controls'));
        if ($target && $target.classList.contains('govuk-radios__conditional')) {
            var inputIsChecked = $input.checked;
            $input.setAttribute('aria-expanded', inputIsChecked);
            $target.classList.toggle('govuk-radios__conditional--hidden', !inputIsChecked);
        }
    };
    /**
 * Click event handler
 *
 * Handle a click within the $module – if the click occurred on a radio, sync
 * the state of the conditional reveal for all radio buttons in the same form
 * with the same name (because checking one radio could have un-checked a radio
 * in another $module)
 *
 * @param {MouseEvent} event Click event
 */ Radios.prototype.handleClick = function(event) {
        var $clickedInput = event.target;
        // Ignore clicks on things that aren't radio buttons
        if ($clickedInput.type !== 'radio') return;
        // We only need to consider radios with conditional reveals, which will have
        // aria-controls attributes.
        var $allInputs = document.querySelectorAll('input[type="radio"][aria-controls]');
        nodeListForEach($allInputs, (function($input) {
            var hasSameFormOwner = $input.form === $clickedInput.form;
            var hasSameName = $input.name === $clickedInput.name;
            if (hasSameName && hasSameFormOwner) this.syncConditionalRevealWithInputState($input);
        }).bind(this));
    };
    (function(undefined) {
        // Detection from https://raw.githubusercontent.com/Financial-Times/polyfill-library/master/polyfills/Element/prototype/nextElementSibling/detect.js
        var detect = 'document' in this && "nextElementSibling" in document.documentElement;
        if (detect) return;
        // Polyfill from https://raw.githubusercontent.com/Financial-Times/polyfill-library/master/polyfills/Element/prototype/nextElementSibling/polyfill.js
        Object.defineProperty(Element.prototype, "nextElementSibling", {
            get: function get() {
                var el = this.nextSibling;
                while(el && el.nodeType !== 1)el = el.nextSibling;
                return el;
            }
        });
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    (function(undefined) {
        // Detection from https://raw.githubusercontent.com/Financial-Times/polyfill-library/master/polyfills/Element/prototype/previousElementSibling/detect.js
        var detect = 'document' in this && "previousElementSibling" in document.documentElement;
        if (detect) return;
        // Polyfill from https://raw.githubusercontent.com/Financial-Times/polyfill-library/master/polyfills/Element/prototype/previousElementSibling/polyfill.js
        Object.defineProperty(Element.prototype, 'previousElementSibling', {
            get: function get() {
                var el = this.previousSibling;
                while(el && el.nodeType !== 1)el = el.previousSibling;
                return el;
            }
        });
    }).call('object' === typeof window && window || 'object' === typeof self && self || 'object' === typeof global && global || {});
    Tabs.prototype.init = function() {
        if (typeof window.matchMedia === 'function') this.setupResponsiveChecks();
        else this.setup();
    };
    Tabs.prototype.setupResponsiveChecks = function() {
        this.mql = window.matchMedia('(min-width: 40.0625em)');
        this.mql.addListener(this.checkMode.bind(this));
        this.checkMode();
    };
    Tabs.prototype.checkMode = function() {
        if (this.mql.matches) this.setup();
        else this.teardown();
    };
    Tabs.prototype.setup = function() {
        var $module = this.$module;
        var $tabs = this.$tabs;
        var $tabList = $module.querySelector('.govuk-tabs__list');
        var $tabListItems = $module.querySelectorAll('.govuk-tabs__list-item');
        if (!$tabs || !$tabList || !$tabListItems) return;
        $tabList.setAttribute('role', 'tablist');
        nodeListForEach($tabListItems, function($item) {
            $item.setAttribute('role', 'presentation');
        });
        nodeListForEach($tabs, (function($tab) {
            // Set HTML attributes
            this.setAttributes($tab);
            // Save bounded functions to use when removing event listeners during teardown
            $tab.boundTabClick = this.onTabClick.bind(this);
            $tab.boundTabKeydown = this.onTabKeydown.bind(this);
            // Handle events
            $tab.addEventListener('click', $tab.boundTabClick, true);
            $tab.addEventListener('keydown', $tab.boundTabKeydown, true);
            // Remove old active panels
            this.hideTab($tab);
        }).bind(this));
        // Show either the active tab according to the URL's hash or the first tab
        var $activeTab = this.getTab(window.location.hash) || this.$tabs[0];
        this.showTab($activeTab);
        // Handle hashchange events
        $module.boundOnHashChange = this.onHashChange.bind(this);
        window.addEventListener('hashchange', $module.boundOnHashChange, true);
    };
    Tabs.prototype.teardown = function() {
        var $module = this.$module;
        var $tabs = this.$tabs;
        var $tabList = $module.querySelector('.govuk-tabs__list');
        var $tabListItems = $module.querySelectorAll('.govuk-tabs__list-item');
        if (!$tabs || !$tabList || !$tabListItems) return;
        $tabList.removeAttribute('role');
        nodeListForEach($tabListItems, function($item) {
            $item.removeAttribute('role', 'presentation');
        });
        nodeListForEach($tabs, (function($tab) {
            // Remove events
            $tab.removeEventListener('click', $tab.boundTabClick, true);
            $tab.removeEventListener('keydown', $tab.boundTabKeydown, true);
            // Unset HTML attributes
            this.unsetAttributes($tab);
        }).bind(this));
        // Remove hashchange event handler
        window.removeEventListener('hashchange', $module.boundOnHashChange, true);
    };
    Tabs.prototype.onHashChange = function(e) {
        var hash = window.location.hash;
        var $tabWithHash = this.getTab(hash);
        if (!$tabWithHash) return;
        // Prevent changing the hash
        if (this.changingHash) {
            this.changingHash = false;
            return;
        }
        // Show either the active tab according to the URL's hash or the first tab
        var $previousTab = this.getCurrentTab();
        this.hideTab($previousTab);
        this.showTab($tabWithHash);
        $tabWithHash.focus();
    };
    Tabs.prototype.hideTab = function($tab) {
        this.unhighlightTab($tab);
        this.hidePanel($tab);
    };
    Tabs.prototype.showTab = function($tab) {
        this.highlightTab($tab);
        this.showPanel($tab);
    };
    Tabs.prototype.getTab = function(hash) {
        return this.$module.querySelector('.govuk-tabs__tab[href="' + hash + '"]');
    };
    Tabs.prototype.setAttributes = function($tab) {
        // set tab attributes
        var panelId = this.getHref($tab).slice(1);
        $tab.setAttribute('id', 'tab_' + panelId);
        $tab.setAttribute('role', 'tab');
        $tab.setAttribute('aria-controls', panelId);
        $tab.setAttribute('aria-selected', 'false');
        $tab.setAttribute('tabindex', '-1');
        // set panel attributes
        var $panel = this.getPanel($tab);
        $panel.setAttribute('role', 'tabpanel');
        $panel.setAttribute('aria-labelledby', $tab.id);
        $panel.classList.add(this.jsHiddenClass);
    };
    Tabs.prototype.unsetAttributes = function($tab) {
        // unset tab attributes
        $tab.removeAttribute('id');
        $tab.removeAttribute('role');
        $tab.removeAttribute('aria-controls');
        $tab.removeAttribute('aria-selected');
        $tab.removeAttribute('tabindex');
        // unset panel attributes
        var $panel = this.getPanel($tab);
        $panel.removeAttribute('role');
        $panel.removeAttribute('aria-labelledby');
        $panel.classList.remove(this.jsHiddenClass);
    };
    Tabs.prototype.onTabClick = function(e) {
        if (!e.target.classList.contains('govuk-tabs__tab')) // Allow events on child DOM elements to bubble up to tab parent
        return false;
        e.preventDefault();
        var $newTab = e.target;
        var $currentTab = this.getCurrentTab();
        this.hideTab($currentTab);
        this.showTab($newTab);
        this.createHistoryEntry($newTab);
    };
    Tabs.prototype.createHistoryEntry = function($tab) {
        var $panel = this.getPanel($tab);
        // Save and restore the id
        // so the page doesn't jump when a user clicks a tab (which changes the hash)
        var id = $panel.id;
        $panel.id = '';
        this.changingHash = true;
        window.location.hash = this.getHref($tab).slice(1);
        $panel.id = id;
    };
    Tabs.prototype.onTabKeydown = function(e) {
        switch(e.keyCode){
            case this.keys.left:
            case this.keys.up:
                this.activatePreviousTab();
                e.preventDefault();
                break;
            case this.keys.right:
            case this.keys.down:
                this.activateNextTab();
                e.preventDefault();
                break;
        }
    };
    Tabs.prototype.activateNextTab = function() {
        var currentTab = this.getCurrentTab();
        var nextTabListItem = currentTab.parentNode.nextElementSibling;
        if (nextTabListItem) var nextTab = nextTabListItem.querySelector('.govuk-tabs__tab');
        if (nextTab) {
            this.hideTab(currentTab);
            this.showTab(nextTab);
            nextTab.focus();
            this.createHistoryEntry(nextTab);
        }
    };
    Tabs.prototype.activatePreviousTab = function() {
        var currentTab = this.getCurrentTab();
        var previousTabListItem = currentTab.parentNode.previousElementSibling;
        if (previousTabListItem) var previousTab = previousTabListItem.querySelector('.govuk-tabs__tab');
        if (previousTab) {
            this.hideTab(currentTab);
            this.showTab(previousTab);
            previousTab.focus();
            this.createHistoryEntry(previousTab);
        }
    };
    Tabs.prototype.getPanel = function($tab) {
        var $panel = this.$module.querySelector(this.getHref($tab));
        return $panel;
    };
    Tabs.prototype.showPanel = function($tab) {
        var $panel = this.getPanel($tab);
        $panel.classList.remove(this.jsHiddenClass);
    };
    Tabs.prototype.hidePanel = function(tab) {
        var $panel = this.getPanel(tab);
        $panel.classList.add(this.jsHiddenClass);
    };
    Tabs.prototype.unhighlightTab = function($tab) {
        $tab.setAttribute('aria-selected', 'false');
        $tab.parentNode.classList.remove('govuk-tabs__list-item--selected');
        $tab.setAttribute('tabindex', '-1');
    };
    Tabs.prototype.highlightTab = function($tab) {
        $tab.setAttribute('aria-selected', 'true');
        $tab.parentNode.classList.add('govuk-tabs__list-item--selected');
        $tab.setAttribute('tabindex', '0');
    };
    Tabs.prototype.getCurrentTab = function() {
        return this.$module.querySelector('.govuk-tabs__list-item--selected .govuk-tabs__tab');
    };
    // this is because IE doesn't always return the actual value but a relative full path
    // should be a utility function most prob
    // http://labs.thesedays.com/blog/2010/01/08/getting-the-href-value-with-jquery-in-ie/
    Tabs.prototype.getHref = function($tab) {
        var href = $tab.getAttribute('href');
        var hash = href.slice(href.indexOf('#'), href.length);
        return hash;
    };
    exports.initAll = initAll;
    exports.Accordion = Accordion;
    exports.Button = Button;
    exports.Details = Details;
    exports.CharacterCount = CharacterCount;
    exports.Checkboxes = Checkboxes;
    exports.ErrorSummary = ErrorSummary;
    exports.Header = Header;
    exports.Radios = Radios;
    exports.Tabs = Tabs;
});

},{"@swc/helpers":"3OBsq"}],"3OBsq":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "applyDecoratedDescriptor", ()=>_applyDecoratedDescriptorDefault.default
);
parcelHelpers.export(exports, "arrayLikeToArray", ()=>_arrayLikeToArrayDefault.default
);
parcelHelpers.export(exports, "arrayWithHoles", ()=>_arrayWithHolesDefault.default
);
parcelHelpers.export(exports, "arrayWithoutHoles", ()=>_arrayWithoutHolesDefault.default
);
parcelHelpers.export(exports, "assertThisInitialized", ()=>_assertThisInitializedDefault.default
);
parcelHelpers.export(exports, "asyncGenerator", ()=>_asyncGeneratorDefault.default
);
parcelHelpers.export(exports, "asyncGeneratorDelegate", ()=>_asyncGeneratorDelegateDefault.default
);
parcelHelpers.export(exports, "asyncIterator", ()=>_asyncIteratorDefault.default
);
parcelHelpers.export(exports, "asyncToGenerator", ()=>_asyncToGeneratorDefault.default
);
parcelHelpers.export(exports, "awaitAsyncGenerator", ()=>_awaitAsyncGeneratorDefault.default
);
parcelHelpers.export(exports, "awaitValue", ()=>_awaitValueDefault.default
);
parcelHelpers.export(exports, "checkPrivateRedeclaration", ()=>_checkPrivateRedeclarationDefault.default
);
parcelHelpers.export(exports, "classApplyDescriptorDestructureSet", ()=>_classApplyDescriptorDestructureDefault.default
);
parcelHelpers.export(exports, "classApplyDescriptorGet", ()=>_classApplyDescriptorGetDefault.default
);
parcelHelpers.export(exports, "classApplyDescriptorSet", ()=>_classApplyDescriptorSetDefault.default
);
parcelHelpers.export(exports, "classCallCheck", ()=>_classCallCheckDefault.default
);
parcelHelpers.export(exports, "classCheckPrivateStaticFieldDescriptor", ()=>_classCheckPrivateStaticFieldDescriptorDefault.default
);
parcelHelpers.export(exports, "classCheckPrivateStaticAccess", ()=>_classCheckPrivateStaticAccessDefault.default
);
parcelHelpers.export(exports, "classNameTDZError", ()=>_classNameTdzErrorDefault.default
);
parcelHelpers.export(exports, "classPrivateFieldDestructureSet", ()=>_classPrivateFieldDestructureDefault.default
);
parcelHelpers.export(exports, "classPrivateFieldGet", ()=>_classPrivateFieldGetDefault.default
);
parcelHelpers.export(exports, "classPrivateFieldInit", ()=>_classPrivateFieldInitDefault.default
);
parcelHelpers.export(exports, "classPrivateFieldLooseBase", ()=>_classPrivateFieldLooseBaseDefault.default
);
parcelHelpers.export(exports, "classPrivateFieldLooseKey", ()=>_classPrivateFieldLooseKeyDefault.default
);
parcelHelpers.export(exports, "classPrivateFieldSet", ()=>_classPrivateFieldSetDefault.default
);
parcelHelpers.export(exports, "classPrivateMethodGet", ()=>_classPrivateMethodGetDefault.default
);
parcelHelpers.export(exports, "classPrivateMethodInit", ()=>_classPrivateMethodInitDefault.default
);
parcelHelpers.export(exports, "classPrivateMethodSet", ()=>_classPrivateMethodSetDefault.default
);
parcelHelpers.export(exports, "classStaticPrivateFieldDestructureSet", ()=>_classStaticPrivateFieldDestructureDefault.default
);
parcelHelpers.export(exports, "classStaticPrivateFieldSpecGet", ()=>_classStaticPrivateFieldSpecGetDefault.default
);
parcelHelpers.export(exports, "classStaticPrivateFieldSpecSet", ()=>_classStaticPrivateFieldSpecSetDefault.default
);
parcelHelpers.export(exports, "construct", ()=>_constructDefault.default
);
parcelHelpers.export(exports, "createClass", ()=>_createClassDefault.default
);
parcelHelpers.export(exports, "createSuper", ()=>_createSuperDefault.default
);
parcelHelpers.export(exports, "decorate", ()=>_decorateDefault.default
);
parcelHelpers.export(exports, "defaults", ()=>_defaultsDefault.default
);
parcelHelpers.export(exports, "defineEnumerableProperties", ()=>_defineEnumerablePropertiesDefault.default
);
parcelHelpers.export(exports, "defineProperty", ()=>_definePropertyDefault.default
);
parcelHelpers.export(exports, "extends", ()=>_extendsDefault.default
);
parcelHelpers.export(exports, "get", ()=>_getDefault.default
);
parcelHelpers.export(exports, "getPrototypeOf", ()=>_getPrototypeOfDefault.default
);
parcelHelpers.export(exports, "inherits", ()=>_inheritsDefault.default
);
parcelHelpers.export(exports, "inheritsLoose", ()=>_inheritsLooseDefault.default
);
parcelHelpers.export(exports, "initializerDefineProperty", ()=>_initializerDefinePropertyDefault.default
);
parcelHelpers.export(exports, "initializerWarningHelper", ()=>_initializerWarningHelperDefault.default
);
parcelHelpers.export(exports, "_instanceof", ()=>_instanceofDefault.default
);
parcelHelpers.export(exports, "interopRequireDefault", ()=>_interopRequireDefaultDefault.default
);
parcelHelpers.export(exports, "interopRequireWildcard", ()=>_interopRequireWildcardDefault.default
);
parcelHelpers.export(exports, "isNativeFunction", ()=>_isNativeFunctionDefault.default
);
parcelHelpers.export(exports, "isNativeReflectConstruct", ()=>_isNativeReflectConstructDefault.default
);
parcelHelpers.export(exports, "iterableToArray", ()=>_iterableToArrayDefault.default
);
parcelHelpers.export(exports, "iterableToArrayLimit", ()=>_iterableToArrayLimitDefault.default
);
parcelHelpers.export(exports, "iterableToArrayLimitLoose", ()=>_iterableToArrayLimitLooseDefault.default
);
parcelHelpers.export(exports, "jsx", ()=>_jsxDefault.default
);
parcelHelpers.export(exports, "newArrowCheck", ()=>_newArrowCheckDefault.default
);
parcelHelpers.export(exports, "nonIterableRest", ()=>_nonIterableRestDefault.default
);
parcelHelpers.export(exports, "nonIterableSpread", ()=>_nonIterableSpreadDefault.default
);
parcelHelpers.export(exports, "objectSpread", ()=>_objectSpreadDefault.default
);
parcelHelpers.export(exports, "objectWithoutProperties", ()=>_objectWithoutPropertiesDefault.default
);
parcelHelpers.export(exports, "objectWithoutPropertiesLoose", ()=>_objectWithoutPropertiesLooseDefault.default
);
parcelHelpers.export(exports, "possibleConstructorReturn", ()=>_possibleConstructorReturnDefault.default
);
parcelHelpers.export(exports, "readOnlyError", ()=>_readOnlyErrorDefault.default
);
parcelHelpers.export(exports, "set", ()=>_setDefault.default
);
parcelHelpers.export(exports, "setPrototypeOf", ()=>_setPrototypeOfDefault.default
);
parcelHelpers.export(exports, "skipFirstGeneratorNext", ()=>_skipFirstGeneratorNextDefault.default
);
parcelHelpers.export(exports, "slicedToArray", ()=>_slicedToArrayDefault.default
);
parcelHelpers.export(exports, "slicedToArrayLoose", ()=>_slicedToArrayLooseDefault.default
);
parcelHelpers.export(exports, "superPropBase", ()=>_superPropBaseDefault.default
);
parcelHelpers.export(exports, "taggedTemplateLiteral", ()=>_taggedTemplateLiteralDefault.default
);
parcelHelpers.export(exports, "taggedTemplateLiteralLoose", ()=>_taggedTemplateLiteralLooseDefault.default
);
parcelHelpers.export(exports, "_throw", ()=>_throwDefault.default
);
parcelHelpers.export(exports, "toArray", ()=>_toArrayDefault.default
);
parcelHelpers.export(exports, "toConsumableArray", ()=>_toConsumableArrayDefault.default
);
parcelHelpers.export(exports, "toPrimitive", ()=>_toPrimitiveDefault.default
);
parcelHelpers.export(exports, "toPropertyKey", ()=>_toPropertyKeyDefault.default
);
parcelHelpers.export(exports, "typeOf", ()=>_typeOfDefault.default
);
parcelHelpers.export(exports, "unsupportedIterableToArray", ()=>_unsupportedIterableToArrayDefault.default
);
parcelHelpers.export(exports, "wrapAsyncGenerator", ()=>_wrapAsyncGeneratorDefault.default
);
parcelHelpers.export(exports, "wrapNativeSuper", ()=>_wrapNativeSuperDefault.default
);
var _applyDecoratedDescriptor = require("./_apply_decorated_descriptor");
var _applyDecoratedDescriptorDefault = parcelHelpers.interopDefault(_applyDecoratedDescriptor);
var _arrayLikeToArray = require("./_array_like_to_array");
var _arrayLikeToArrayDefault = parcelHelpers.interopDefault(_arrayLikeToArray);
var _arrayWithHoles = require("./_array_with_holes");
var _arrayWithHolesDefault = parcelHelpers.interopDefault(_arrayWithHoles);
var _arrayWithoutHoles = require("./_array_without_holes");
var _arrayWithoutHolesDefault = parcelHelpers.interopDefault(_arrayWithoutHoles);
var _assertThisInitialized = require("./_assert_this_initialized");
var _assertThisInitializedDefault = parcelHelpers.interopDefault(_assertThisInitialized);
var _asyncGenerator = require("./_async_generator");
var _asyncGeneratorDefault = parcelHelpers.interopDefault(_asyncGenerator);
var _asyncGeneratorDelegate = require("./_async_generator_delegate");
var _asyncGeneratorDelegateDefault = parcelHelpers.interopDefault(_asyncGeneratorDelegate);
var _asyncIterator = require("./_async_iterator");
var _asyncIteratorDefault = parcelHelpers.interopDefault(_asyncIterator);
var _asyncToGenerator = require("./_async_to_generator");
var _asyncToGeneratorDefault = parcelHelpers.interopDefault(_asyncToGenerator);
var _awaitAsyncGenerator = require("./_await_async_generator");
var _awaitAsyncGeneratorDefault = parcelHelpers.interopDefault(_awaitAsyncGenerator);
var _awaitValue = require("./_await_value");
var _awaitValueDefault = parcelHelpers.interopDefault(_awaitValue);
var _checkPrivateRedeclaration = require("./_check_private_redeclaration");
var _checkPrivateRedeclarationDefault = parcelHelpers.interopDefault(_checkPrivateRedeclaration);
var _classApplyDescriptorDestructure = require("./_class_apply_descriptor_destructure");
var _classApplyDescriptorDestructureDefault = parcelHelpers.interopDefault(_classApplyDescriptorDestructure);
var _classApplyDescriptorGet = require("./_class_apply_descriptor_get");
var _classApplyDescriptorGetDefault = parcelHelpers.interopDefault(_classApplyDescriptorGet);
var _classApplyDescriptorSet = require("./_class_apply_descriptor_set");
var _classApplyDescriptorSetDefault = parcelHelpers.interopDefault(_classApplyDescriptorSet);
var _classCallCheck = require("./_class_call_check");
var _classCallCheckDefault = parcelHelpers.interopDefault(_classCallCheck);
var _classCheckPrivateStaticFieldDescriptor = require("./_class_check_private_static_field_descriptor");
var _classCheckPrivateStaticFieldDescriptorDefault = parcelHelpers.interopDefault(_classCheckPrivateStaticFieldDescriptor);
var _classCheckPrivateStaticAccess = require("./_class_check_private_static_access");
var _classCheckPrivateStaticAccessDefault = parcelHelpers.interopDefault(_classCheckPrivateStaticAccess);
var _classNameTdzError = require("./_class_name_tdz_error");
var _classNameTdzErrorDefault = parcelHelpers.interopDefault(_classNameTdzError);
var _classPrivateFieldDestructure = require("./_class_private_field_destructure");
var _classPrivateFieldDestructureDefault = parcelHelpers.interopDefault(_classPrivateFieldDestructure);
var _classPrivateFieldGet = require("./_class_private_field_get");
var _classPrivateFieldGetDefault = parcelHelpers.interopDefault(_classPrivateFieldGet);
var _classPrivateFieldInit = require("./_class_private_field_init");
var _classPrivateFieldInitDefault = parcelHelpers.interopDefault(_classPrivateFieldInit);
var _classPrivateFieldLooseBase = require("./_class_private_field_loose_base");
var _classPrivateFieldLooseBaseDefault = parcelHelpers.interopDefault(_classPrivateFieldLooseBase);
var _classPrivateFieldLooseKey = require("./_class_private_field_loose_key");
var _classPrivateFieldLooseKeyDefault = parcelHelpers.interopDefault(_classPrivateFieldLooseKey);
var _classPrivateFieldSet = require("./_class_private_field_set");
var _classPrivateFieldSetDefault = parcelHelpers.interopDefault(_classPrivateFieldSet);
var _classPrivateMethodGet = require("./_class_private_method_get");
var _classPrivateMethodGetDefault = parcelHelpers.interopDefault(_classPrivateMethodGet);
var _classPrivateMethodInit = require("./_class_private_method_init");
var _classPrivateMethodInitDefault = parcelHelpers.interopDefault(_classPrivateMethodInit);
var _classPrivateMethodSet = require("./_class_private_method_set");
var _classPrivateMethodSetDefault = parcelHelpers.interopDefault(_classPrivateMethodSet);
var _classStaticPrivateFieldDestructure = require("./_class_static_private_field_destructure");
var _classStaticPrivateFieldDestructureDefault = parcelHelpers.interopDefault(_classStaticPrivateFieldDestructure);
var _classStaticPrivateFieldSpecGet = require("./_class_static_private_field_spec_get");
var _classStaticPrivateFieldSpecGetDefault = parcelHelpers.interopDefault(_classStaticPrivateFieldSpecGet);
var _classStaticPrivateFieldSpecSet = require("./_class_static_private_field_spec_set");
var _classStaticPrivateFieldSpecSetDefault = parcelHelpers.interopDefault(_classStaticPrivateFieldSpecSet);
var _construct = require("./_construct");
var _constructDefault = parcelHelpers.interopDefault(_construct);
var _createClass = require("./_create_class");
var _createClassDefault = parcelHelpers.interopDefault(_createClass);
var _createSuper = require("./_create_super");
var _createSuperDefault = parcelHelpers.interopDefault(_createSuper);
var _decorate = require("./_decorate");
var _decorateDefault = parcelHelpers.interopDefault(_decorate);
var _defaults = require("./_defaults");
var _defaultsDefault = parcelHelpers.interopDefault(_defaults);
var _defineEnumerableProperties = require("./_define_enumerable_properties");
var _defineEnumerablePropertiesDefault = parcelHelpers.interopDefault(_defineEnumerableProperties);
var _defineProperty = require("./_define_property");
var _definePropertyDefault = parcelHelpers.interopDefault(_defineProperty);
var _extends = require("./_extends");
var _extendsDefault = parcelHelpers.interopDefault(_extends);
var _get = require("./_get");
var _getDefault = parcelHelpers.interopDefault(_get);
var _getPrototypeOf = require("./_get_prototype_of");
var _getPrototypeOfDefault = parcelHelpers.interopDefault(_getPrototypeOf);
var _inherits = require("./_inherits");
var _inheritsDefault = parcelHelpers.interopDefault(_inherits);
var _inheritsLoose = require("./_inherits_loose");
var _inheritsLooseDefault = parcelHelpers.interopDefault(_inheritsLoose);
var _initializerDefineProperty = require("./_initializer_define_property");
var _initializerDefinePropertyDefault = parcelHelpers.interopDefault(_initializerDefineProperty);
var _initializerWarningHelper = require("./_initializer_warning_helper");
var _initializerWarningHelperDefault = parcelHelpers.interopDefault(_initializerWarningHelper);
var _instanceof = require("./_instanceof");
var _instanceofDefault = parcelHelpers.interopDefault(_instanceof);
var _interopRequireDefault = require("./_interop_require_default");
var _interopRequireDefaultDefault = parcelHelpers.interopDefault(_interopRequireDefault);
var _interopRequireWildcard = require("./_interop_require_wildcard");
var _interopRequireWildcardDefault = parcelHelpers.interopDefault(_interopRequireWildcard);
var _isNativeFunction = require("./_is_native_function");
var _isNativeFunctionDefault = parcelHelpers.interopDefault(_isNativeFunction);
var _isNativeReflectConstruct = require("./_is_native_reflect_construct");
var _isNativeReflectConstructDefault = parcelHelpers.interopDefault(_isNativeReflectConstruct);
var _iterableToArray = require("./_iterable_to_array");
var _iterableToArrayDefault = parcelHelpers.interopDefault(_iterableToArray);
var _iterableToArrayLimit = require("./_iterable_to_array_limit");
var _iterableToArrayLimitDefault = parcelHelpers.interopDefault(_iterableToArrayLimit);
var _iterableToArrayLimitLoose = require("./_iterable_to_array_limit_loose");
var _iterableToArrayLimitLooseDefault = parcelHelpers.interopDefault(_iterableToArrayLimitLoose);
var _jsx = require("./_jsx");
var _jsxDefault = parcelHelpers.interopDefault(_jsx);
var _newArrowCheck = require("./_new_arrow_check");
var _newArrowCheckDefault = parcelHelpers.interopDefault(_newArrowCheck);
var _nonIterableRest = require("./_non_iterable_rest");
var _nonIterableRestDefault = parcelHelpers.interopDefault(_nonIterableRest);
var _nonIterableSpread = require("./_non_iterable_spread");
var _nonIterableSpreadDefault = parcelHelpers.interopDefault(_nonIterableSpread);
var _objectSpread = require("./_object_spread");
var _objectSpreadDefault = parcelHelpers.interopDefault(_objectSpread);
var _objectWithoutProperties = require("./_object_without_properties");
var _objectWithoutPropertiesDefault = parcelHelpers.interopDefault(_objectWithoutProperties);
var _objectWithoutPropertiesLoose = require("./_object_without_properties_loose");
var _objectWithoutPropertiesLooseDefault = parcelHelpers.interopDefault(_objectWithoutPropertiesLoose);
var _possibleConstructorReturn = require("./_possible_constructor_return");
var _possibleConstructorReturnDefault = parcelHelpers.interopDefault(_possibleConstructorReturn);
var _readOnlyError = require("./_read_only_error");
var _readOnlyErrorDefault = parcelHelpers.interopDefault(_readOnlyError);
var _set = require("./_set");
var _setDefault = parcelHelpers.interopDefault(_set);
var _setPrototypeOf = require("./_set_prototype_of");
var _setPrototypeOfDefault = parcelHelpers.interopDefault(_setPrototypeOf);
var _skipFirstGeneratorNext = require("./_skip_first_generator_next");
var _skipFirstGeneratorNextDefault = parcelHelpers.interopDefault(_skipFirstGeneratorNext);
var _slicedToArray = require("./_sliced_to_array");
var _slicedToArrayDefault = parcelHelpers.interopDefault(_slicedToArray);
var _slicedToArrayLoose = require("./_sliced_to_array_loose");
var _slicedToArrayLooseDefault = parcelHelpers.interopDefault(_slicedToArrayLoose);
var _superPropBase = require("./_super_prop_base");
var _superPropBaseDefault = parcelHelpers.interopDefault(_superPropBase);
var _taggedTemplateLiteral = require("./_tagged_template_literal");
var _taggedTemplateLiteralDefault = parcelHelpers.interopDefault(_taggedTemplateLiteral);
var _taggedTemplateLiteralLoose = require("./_tagged_template_literal_loose");
var _taggedTemplateLiteralLooseDefault = parcelHelpers.interopDefault(_taggedTemplateLiteralLoose);
var _throw = require("./_throw");
var _throwDefault = parcelHelpers.interopDefault(_throw);
var _toArray = require("./_to_array");
var _toArrayDefault = parcelHelpers.interopDefault(_toArray);
var _toConsumableArray = require("./_to_consumable_array");
var _toConsumableArrayDefault = parcelHelpers.interopDefault(_toConsumableArray);
var _toPrimitive = require("./_to_primitive");
var _toPrimitiveDefault = parcelHelpers.interopDefault(_toPrimitive);
var _toPropertyKey = require("./_to_property_key");
var _toPropertyKeyDefault = parcelHelpers.interopDefault(_toPropertyKey);
var _typeOf = require("./_type_of");
var _typeOfDefault = parcelHelpers.interopDefault(_typeOf);
var _unsupportedIterableToArray = require("./_unsupported_iterable_to_array");
var _unsupportedIterableToArrayDefault = parcelHelpers.interopDefault(_unsupportedIterableToArray);
var _wrapAsyncGenerator = require("./_wrap_async_generator");
var _wrapAsyncGeneratorDefault = parcelHelpers.interopDefault(_wrapAsyncGenerator);
var _wrapNativeSuper = require("./_wrap_native_super");
var _wrapNativeSuperDefault = parcelHelpers.interopDefault(_wrapNativeSuper);

},{"./_apply_decorated_descriptor":"6CN9G","./_array_like_to_array":"7Umy3","./_array_with_holes":"hdkVj","./_array_without_holes":"l74UH","./_assert_this_initialized":"dDPCT","./_async_generator":"QOozV","./_async_generator_delegate":"bRjNP","./_async_iterator":"k3zdg","./_async_to_generator":"haZ5l","./_await_async_generator":"g0Uuv","./_await_value":"lwzsi","./_check_private_redeclaration":"51d6f","./_class_apply_descriptor_destructure":"85KVk","./_class_apply_descriptor_get":"eLkW7","./_class_apply_descriptor_set":"9bTrJ","./_class_call_check":"shXft","./_class_check_private_static_field_descriptor":"kj3yn","./_class_check_private_static_access":"kOlqI","./_class_name_tdz_error":"ckl2u","./_class_private_field_destructure":"bM75M","./_class_private_field_get":"4JR18","./_class_private_field_init":"egg00","./_class_private_field_loose_base":"4NSm8","./_class_private_field_loose_key":"cDWgp","./_class_private_field_set":"hX85l","./_class_private_method_get":"9KzT9","./_class_private_method_init":"bHngr","./_class_private_method_set":"jHiKU","./_class_static_private_field_destructure":"5434S","./_class_static_private_field_spec_get":"9QisI","./_class_static_private_field_spec_set":"40MD5","./_construct":"fWjGA","./_create_class":"ixmVh","./_create_super":"8yCC8","./_decorate":"c3d6m","./_defaults":"4i4zb","./_define_enumerable_properties":"cXWLD","./_define_property":"6oPi2","./_extends":"j68CL","./_get":"3Ctd3","./_get_prototype_of":"6HtCT","./_inherits":"bxQnN","./_inherits_loose":"klWjZ","./_initializer_define_property":"1oAt5","./_initializer_warning_helper":"9PAfr","./_instanceof":"jTvrY","./_interop_require_default":"95JHK","./_interop_require_wildcard":"3WUUn","./_is_native_function":"6NiqX","./_is_native_reflect_construct":"fAab4","./_iterable_to_array":"84rWR","./_iterable_to_array_limit":"i9TMH","./_iterable_to_array_limit_loose":"bcCsX","./_jsx":"jXjsO","./_new_arrow_check":"el295","./_non_iterable_rest":"eJPaJ","./_non_iterable_spread":"ihzXr","./_object_spread":"aLguo","./_object_without_properties":"clNOR","./_object_without_properties_loose":"2AAov","./_possible_constructor_return":"eO41G","./_read_only_error":"25q9F","./_set":"lYl68","./_set_prototype_of":"lLpOg","./_skip_first_generator_next":"1oSeh","./_sliced_to_array":"cILUy","./_sliced_to_array_loose":"icOVf","./_super_prop_base":"1UTk2","./_tagged_template_literal":"ddLTO","./_tagged_template_literal_loose":"bYUuZ","./_throw":"9U50I","./_to_array":"iaZDG","./_to_consumable_array":"4aEni","./_to_primitive":"ixgwi","./_to_property_key":"61H7i","./_type_of":"jj0G7","./_unsupported_iterable_to_array":"kbV8u","./_wrap_async_generator":"9mZxY","./_wrap_native_super":"gTQpL","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"6CN9G":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _applyDecoratedDescriptor(target, property, decorators, descriptor, context) {
    var desc1 = {};
    Object["keys"](descriptor).forEach(function(key) {
        desc1[key] = descriptor[key];
    });
    desc1.enumerable = !!desc1.enumerable;
    desc1.configurable = !!desc1.configurable;
    if ('value' in desc1 || desc1.initializer) desc1.writable = true;
    desc1 = decorators.slice().reverse().reduce(function(desc, decorator) {
        return decorator ? decorator(target, property, desc) || desc : desc;
    }, desc1);
    if (context && desc1.initializer !== void 0) {
        desc1.value = desc1.initializer ? desc1.initializer.call(context) : void 0;
        desc1.initializer = undefined;
    }
    if (desc1.initializer === void 0) {
        Object["defineProperty"](target, property, desc1);
        desc1 = null;
    }
    return desc1;
}
exports.default = _applyDecoratedDescriptor;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bt0mQ":[function(require,module,exports) {
exports.interopDefault = function(a) {
    return a && a.__esModule ? a : {
        default: a
    };
};
exports.defineInteropFlag = function(a) {
    Object.defineProperty(a, '__esModule', {
        value: true
    });
};
exports.exportAll = function(source, dest) {
    Object.keys(source).forEach(function(key) {
        if (key === 'default' || key === '__esModule' || dest.hasOwnProperty(key)) return;
        Object.defineProperty(dest, key, {
            enumerable: true,
            get: function get() {
                return source[key];
            }
        });
    });
    return dest;
};
exports.export = function(dest, destName, get) {
    Object.defineProperty(dest, destName, {
        enumerable: true,
        get: get
    });
};

},{}],"7Umy3":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;
    for(var i = 0, arr2 = new Array(len); i < len; i++)arr2[i] = arr[i];
    return arr2;
}
exports.default = _arrayLikeToArray;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hdkVj":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _arrayWithHoles(arr) {
    if (Array.isArray(arr)) return arr;
}
exports.default = _arrayWithHoles;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"l74UH":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _arrayLikeToArray = require("./_array_like_to_array");
var _arrayLikeToArrayDefault = parcelHelpers.interopDefault(_arrayLikeToArray);
function _arrayWithoutHoles(arr) {
    if (Array.isArray(arr)) return _arrayLikeToArrayDefault.default(arr);
}
exports.default = _arrayWithoutHoles;

},{"./_array_like_to_array":"7Umy3","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"dDPCT":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _assertThisInitialized(self) {
    if (self === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    return self;
}
exports.default = _assertThisInitialized;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"QOozV":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _awaitValue = require("./_await_value");
var _awaitValueDefault = parcelHelpers.interopDefault(_awaitValue);
function AsyncGenerator(gen) {
    var front, back;
    function send(key, arg) {
        return new Promise(function(resolve, reject) {
            var request = {
                key: key,
                arg: arg,
                resolve: resolve,
                reject: reject,
                next: null
            };
            if (back) back = back.next = request;
            else {
                front = back = request;
                resume(key, arg);
            }
        });
    }
    function resume(key, arg1) {
        try {
            var result = gen[key](arg1);
            var value = result.value;
            var wrappedAwait = value instanceof _awaitValueDefault.default;
            Promise.resolve(wrappedAwait ? value.wrapped : value).then(function(arg) {
                if (wrappedAwait) {
                    resume("next", arg);
                    return;
                }
                settle(result.done ? "return" : "normal", arg);
            }, function(err) {
                resume("throw", err);
            });
        } catch (err) {
            settle("throw", err);
        }
    }
    function settle(type, value) {
        switch(type){
            case "return":
                front.resolve({
                    value: value,
                    done: true
                });
                break;
            case "throw":
                front.reject(value);
                break;
            default:
                front.resolve({
                    value: value,
                    done: false
                });
                break;
        }
        front = front.next;
        if (front) resume(front.key, front.arg);
        else back = null;
    }
    this._invoke = send;
    if (typeof gen.return !== "function") this.return = undefined;
}
exports.default = AsyncGenerator;
if (typeof Symbol === "function" && Symbol.asyncIterator) AsyncGenerator.prototype[Symbol.asyncIterator] = function() {
    return this;
};
AsyncGenerator.prototype.next = function(arg) {
    return this._invoke("next", arg);
};
AsyncGenerator.prototype.throw = function(arg) {
    return this._invoke("throw", arg);
};
AsyncGenerator.prototype.return = function(arg) {
    return this._invoke("return", arg);
};

},{"./_await_value":"lwzsi","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"lwzsi":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _AwaitValue(value) {
    this.wrapped = value;
}
exports.default = _AwaitValue;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bRjNP":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _asyncGeneratorDelegate(inner, awaitWrap) {
    var iter = {}, waiting = false;
    function pump(key, value) {
        waiting = true;
        value = new Promise(function(resolve) {
            resolve(inner[key](value));
        });
        return {
            done: false,
            value: awaitWrap(value)
        };
    }
    if (typeof Symbol === "function" && Symbol.iterator) iter[Symbol.iterator] = function() {
        return this;
    };
    iter.next = function(value) {
        if (waiting) {
            waiting = false;
            return value;
        }
        return pump("next", value);
    };
    if (typeof inner.throw === "function") iter.throw = function(value) {
        if (waiting) {
            waiting = false;
            throw value;
        }
        return pump("throw", value);
    };
    if (typeof inner.return === "function") iter.return = function(value) {
        return pump("return", value);
    };
    return iter;
}
exports.default = _asyncGeneratorDelegate;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"k3zdg":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _asyncIterator(iterable) {
    var method;
    if (typeof Symbol === "function") {
        if (Symbol.asyncIterator) {
            method = iterable[Symbol.asyncIterator];
            if (method != null) return method.call(iterable);
        }
        if (Symbol.iterator) {
            method = iterable[Symbol.iterator];
            if (method != null) return method.call(iterable);
        }
    }
    throw new TypeError("Object is not async iterable");
}
exports.default = _asyncIterator;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"haZ5l":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function asyncGeneratorStep(gen, resolve, reject, _next, _throw, key, arg) {
    try {
        var info = gen[key](arg);
        var value = info.value;
    } catch (error) {
        reject(error);
        return;
    }
    if (info.done) resolve(value);
    else Promise.resolve(value).then(_next, _throw);
}
function _asyncToGenerator(fn) {
    return function() {
        var self = this, args = arguments;
        return new Promise(function(resolve, reject) {
            var gen = fn.apply(self, args);
            function _next(value) {
                asyncGeneratorStep(gen, resolve, reject, _next, _throw, "next", value);
            }
            function _throw(err) {
                asyncGeneratorStep(gen, resolve, reject, _next, _throw, "throw", err);
            }
            _next(undefined);
        });
    };
}
exports.default = _asyncToGenerator;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"g0Uuv":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _awaitValue = require("./_await_value");
var _awaitValueDefault = parcelHelpers.interopDefault(_awaitValue);
function _awaitAsyncGenerator(value) {
    return new _awaitValueDefault.default(value);
}
exports.default = _awaitAsyncGenerator;

},{"./_await_value":"lwzsi","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"51d6f":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _checkPrivateRedeclaration(obj, privateCollection) {
    if (privateCollection.has(obj)) throw new TypeError("Cannot initialize the same private elements twice on an object");
}
exports.default = _checkPrivateRedeclaration;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"85KVk":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classApplyDescriptorDestructureSet(receiver, descriptor) {
    if (descriptor.set) {
        if (!("__destrObj" in descriptor)) descriptor.__destrObj = {
            set value (v){
                descriptor.set.call(receiver, v);
            }
        };
        return descriptor.__destrObj;
    } else {
        if (!descriptor.writable) // This should only throw in strict mode, but class bodies are
        // always strict and private fields can only be used inside
        // class bodies.
        throw new TypeError("attempted to set read only private field");
        return descriptor;
    }
}
exports.default = _classApplyDescriptorDestructureSet;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"eLkW7":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classApplyDescriptorGet(receiver, descriptor) {
    if (descriptor.get) return descriptor.get.call(receiver);
    return descriptor.value;
}
exports.default = _classApplyDescriptorGet;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9bTrJ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classApplyDescriptorSet(receiver, descriptor, value) {
    if (descriptor.set) descriptor.set.call(receiver, value);
    else {
        if (!descriptor.writable) // This should only throw in strict mode, but class bodies are
        // always strict and private fields can only be used inside
        // class bodies.
        throw new TypeError("attempted to set read only private field");
        descriptor.value = value;
    }
}
exports.default = _classApplyDescriptorSet;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"shXft":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) throw new TypeError("Cannot call a class as a function");
}
exports.default = _classCallCheck;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"kj3yn":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classCheckPrivateStaticFieldDescriptor(descriptor, action) {
    if (descriptor === undefined) throw new TypeError("attempted to " + action + " private static field before its declaration");
}
exports.default = _classCheckPrivateStaticFieldDescriptor;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"kOlqI":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classCheckPrivateStaticAccess(receiver, classConstructor) {
    if (receiver !== classConstructor) throw new TypeError("Private static access of wrong provenance");
}
exports.default = _classCheckPrivateStaticAccess;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ckl2u":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classNameTDZError(name) {
    throw new Error("Class \"" + name + "\" cannot be referenced in computed property keys.");
}
exports.default = _classNameTDZError;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bM75M":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _classExtractFieldDescriptor = require("./_class_extract_field_descriptor");
var _classExtractFieldDescriptorDefault = parcelHelpers.interopDefault(_classExtractFieldDescriptor);
var _classApplyDescriptorDestructure = require("./_class_apply_descriptor_destructure");
var _classApplyDescriptorDestructureDefault = parcelHelpers.interopDefault(_classApplyDescriptorDestructure);
function _classPrivateFieldDestructureSet(receiver, privateMap) {
    var descriptor = _classExtractFieldDescriptorDefault.default(receiver, privateMap, "set");
    return _classApplyDescriptorDestructureDefault.default(receiver, descriptor);
}
exports.default = _classPrivateFieldDestructureSet;

},{"./_class_extract_field_descriptor":"ADMXO","./_class_apply_descriptor_destructure":"85KVk","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ADMXO":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classExtractFieldDescriptor(receiver, privateMap, action) {
    if (!privateMap.has(receiver)) throw new TypeError("attempted to " + action + " private field on non-instance");
    return privateMap.get(receiver);
}
exports.default = _classExtractFieldDescriptor;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4JR18":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _classExtractFieldDescriptor = require("./_class_extract_field_descriptor");
var _classExtractFieldDescriptorDefault = parcelHelpers.interopDefault(_classExtractFieldDescriptor);
var _classApplyDescriptorGet = require("./_class_apply_descriptor_get");
var _classApplyDescriptorGetDefault = parcelHelpers.interopDefault(_classApplyDescriptorGet);
function _classPrivateFieldGet(receiver, privateMap) {
    var descriptor = _classExtractFieldDescriptorDefault.default(receiver, privateMap, "get");
    return _classApplyDescriptorGetDefault.default(receiver, descriptor);
}
exports.default = _classPrivateFieldGet;

},{"./_class_extract_field_descriptor":"ADMXO","./_class_apply_descriptor_get":"eLkW7","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"egg00":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _checkPrivateRedeclaration = require("./_check_private_redeclaration");
var _checkPrivateRedeclarationDefault = parcelHelpers.interopDefault(_checkPrivateRedeclaration);
function _classPrivateFieldInit(obj, privateMap, value) {
    _checkPrivateRedeclarationDefault.default(obj, privateMap);
    privateMap.set(obj, value);
}
exports.default = _classPrivateFieldInit;

},{"./_check_private_redeclaration":"51d6f","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4NSm8":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classPrivateFieldBase(receiver, privateKey) {
    if (!Object.prototype.hasOwnProperty.call(receiver, privateKey)) throw new TypeError("attempted to use private field on non-instance");
    return receiver;
}
exports.default = _classPrivateFieldBase;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"cDWgp":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var id = 0;
function _classPrivateFieldLooseKey(name) {
    return "__private_" + id++ + "_" + name;
}
exports.default = _classPrivateFieldLooseKey;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hX85l":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _classExtractFieldDescriptor = require("./_class_extract_field_descriptor");
var _classExtractFieldDescriptorDefault = parcelHelpers.interopDefault(_classExtractFieldDescriptor);
var _classApplyDescriptorSet = require("./_class_apply_descriptor_set");
var _classApplyDescriptorSetDefault = parcelHelpers.interopDefault(_classApplyDescriptorSet);
function _classPrivateFieldSet(receiver, privateMap, value) {
    var descriptor = _classExtractFieldDescriptorDefault.default(receiver, privateMap, "set");
    _classApplyDescriptorSetDefault.default(receiver, descriptor, value);
    return value;
}
exports.default = _classPrivateFieldSet;

},{"./_class_extract_field_descriptor":"ADMXO","./_class_apply_descriptor_set":"9bTrJ","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9KzT9":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classPrivateMethodGet(receiver, privateSet, fn) {
    if (!privateSet.has(receiver)) throw new TypeError("attempted to get private field on non-instance");
    return fn;
}
exports.default = _classPrivateMethodGet;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bHngr":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _checkPrivateRedeclaration = require("./_check_private_redeclaration");
var _checkPrivateRedeclarationDefault = parcelHelpers.interopDefault(_checkPrivateRedeclaration);
function _classPrivateMethodInit(obj, privateSet) {
    _checkPrivateRedeclarationDefault.default(obj, privateSet);
    privateSet.add(obj);
}
exports.default = _classPrivateMethodInit;

},{"./_check_private_redeclaration":"51d6f","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jHiKU":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _classPrivateMethodSet() {
    throw new TypeError("attempted to reassign private method");
}
exports.default = _classPrivateMethodSet;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"5434S":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _classCheckPrivateStaticAccess = require("./_class_check_private_static_access");
var _classCheckPrivateStaticAccessDefault = parcelHelpers.interopDefault(_classCheckPrivateStaticAccess);
var _classApplyDescriptorDestructure = require("./_class_apply_descriptor_destructure");
var _classApplyDescriptorDestructureDefault = parcelHelpers.interopDefault(_classApplyDescriptorDestructure);
function _classStaticPrivateFieldDestructureSet(receiver, classConstructor, descriptor) {
    _classCheckPrivateStaticAccessDefault.default(receiver, classConstructor);
    _classCheckPrivateStaticAccessDefault.default(descriptor, "set");
    return _classApplyDescriptorDestructureDefault.default(receiver, descriptor);
}
exports.default = _classStaticPrivateFieldDestructureSet;

},{"./_class_check_private_static_access":"kOlqI","./_class_apply_descriptor_destructure":"85KVk","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9QisI":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _classCheckPrivateStaticAccess = require("./_class_check_private_static_access");
var _classCheckPrivateStaticAccessDefault = parcelHelpers.interopDefault(_classCheckPrivateStaticAccess);
var _classApplyDescriptorGet = require("./_class_apply_descriptor_get");
var _classApplyDescriptorGetDefault = parcelHelpers.interopDefault(_classApplyDescriptorGet);
function _classStaticPrivateFieldSpecGet(receiver, classConstructor, descriptor) {
    _classCheckPrivateStaticAccessDefault.default(receiver, classConstructor);
    _classCheckPrivateStaticAccessDefault.default(descriptor, "get");
    return _classApplyDescriptorGetDefault.default(receiver, descriptor);
}
exports.default = _classStaticPrivateFieldSpecGet;

},{"./_class_check_private_static_access":"kOlqI","./_class_apply_descriptor_get":"eLkW7","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"40MD5":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _classCheckPrivateStaticAccess = require("./_class_check_private_static_access");
var _classCheckPrivateStaticAccessDefault = parcelHelpers.interopDefault(_classCheckPrivateStaticAccess);
var _classApplyDescriptorSet = require("./_class_apply_descriptor_set");
var _classApplyDescriptorSetDefault = parcelHelpers.interopDefault(_classApplyDescriptorSet);
function _classStaticPrivateFieldSpecSet(receiver, classConstructor, descriptor, value) {
    _classCheckPrivateStaticAccessDefault.default(receiver, classConstructor);
    _classCheckPrivateStaticAccessDefault.default(descriptor, "set");
    _classApplyDescriptorSetDefault.default(receiver, descriptor, value);
    return value;
}
exports.default = _classStaticPrivateFieldSpecSet;

},{"./_class_check_private_static_access":"kOlqI","./_class_apply_descriptor_set":"9bTrJ","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"fWjGA":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _setPrototypeOf = require("./_set_prototype_of");
var _setPrototypeOfDefault = parcelHelpers.interopDefault(_setPrototypeOf);
function isNativeReflectConstruct() {
    if (typeof Reflect === "undefined" || !Reflect.construct) return false;
    if (Reflect.construct.sham) return false;
    if (typeof Proxy === "function") return true;
    try {
        Date.prototype.toString.call(Reflect.construct(Date, [], function() {}));
        return true;
    } catch (e) {
        return false;
    }
}
function construct(Parent1, args1, Class1) {
    if (isNativeReflectConstruct()) construct = Reflect.construct;
    else construct = function construct(Parent, args, Class) {
        var a = [
            null
        ];
        a.push.apply(a, args);
        var Constructor = Function.bind.apply(Parent, a);
        var instance = new Constructor();
        if (Class) _setPrototypeOfDefault.default(instance, Class.prototype);
        return instance;
    };
    return construct.apply(null, arguments);
}
function _construct(Parent, args, Class) {
    return construct.apply(null, arguments);
}
exports.default = _construct;

},{"./_set_prototype_of":"lLpOg","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"lLpOg":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function setPrototypeOf(o1, p1) {
    setPrototypeOf = Object.setPrototypeOf || function setPrototypeOf(o, p) {
        o.__proto__ = p;
        return o;
    };
    return setPrototypeOf(o1, p1);
}
function _setPrototypeOf(o, p) {
    return setPrototypeOf(o, p);
}
exports.default = _setPrototypeOf;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ixmVh":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _defineProperties(target, props) {
    for(var i = 0; i < props.length; i++){
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}
function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    return Constructor;
}
exports.default = _createClass;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"8yCC8":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _isNativeReflectConstruct = require("./_is_native_reflect_construct");
var _isNativeReflectConstructDefault = parcelHelpers.interopDefault(_isNativeReflectConstruct);
var _getPrototypeOf = require("./_get_prototype_of");
var _getPrototypeOfDefault = parcelHelpers.interopDefault(_getPrototypeOf);
var _possibleConstructorReturn = require("./_possible_constructor_return");
var _possibleConstructorReturnDefault = parcelHelpers.interopDefault(_possibleConstructorReturn);
function _createSuper(Derived) {
    var hasNativeReflectConstruct = _isNativeReflectConstructDefault.default();
    return function _createSuperInternal() {
        var Super = _getPrototypeOfDefault.default(Derived), result;
        if (hasNativeReflectConstruct) {
            var NewTarget = _getPrototypeOfDefault.default(this).constructor;
            result = Reflect.construct(Super, arguments, NewTarget);
        } else result = Super.apply(this, arguments);
        return _possibleConstructorReturnDefault.default(this, result);
    };
}
exports.default = _createSuper;

},{"./_is_native_reflect_construct":"fAab4","./_get_prototype_of":"6HtCT","./_possible_constructor_return":"eO41G","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"fAab4":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _isNativeReflectConstruct() {
    if (typeof Reflect === "undefined" || !Reflect.construct) return false;
    if (Reflect.construct.sham) return false;
    if (typeof Proxy === "function") return true;
    try {
        Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {}));
        return true;
    } catch (e) {
        return false;
    }
}
exports.default = _isNativeReflectConstruct;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"6HtCT":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getPrototypeOf(o1) {
    getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function getPrototypeOf(o) {
        return o.__proto__ || Object.getPrototypeOf(o);
    };
    return getPrototypeOf(o1);
}
function _getPrototypeOf(o) {
    return getPrototypeOf(o);
}
exports.default = _getPrototypeOf;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"eO41G":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _assertThisInitialized = require("./_assert_this_initialized");
var _assertThisInitializedDefault = parcelHelpers.interopDefault(_assertThisInitialized);
var _typeOf = require("./_type_of");
var _typeOfDefault = parcelHelpers.interopDefault(_typeOf);
function _possibleConstructorReturn(self, call) {
    if (call && (_typeOfDefault.default(call) === "object" || typeof call === "function")) return call;
    return _assertThisInitializedDefault.default(self);
}
exports.default = _possibleConstructorReturn;

},{"./_assert_this_initialized":"dDPCT","./_type_of":"jj0G7","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jj0G7":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _typeof(obj) {
    return obj && obj.constructor === Symbol ? "symbol" : typeof obj;
}
exports.default = _typeof;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"c3d6m":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _toArray = require("./_to_array");
var _toArrayDefault = parcelHelpers.interopDefault(_toArray);
var _toPropertyKey = require("./_to_property_key");
var _toPropertyKeyDefault = parcelHelpers.interopDefault(_toPropertyKey);
function _decorate(decorators, factory, superClass) {
    var r = factory(function initialize(O) {
        _initializeInstanceElements(O, decorated.elements);
    }, superClass);
    var decorated = _decorateClass(_coalesceClassElements(r.d.map(_createElementDescriptor)), decorators);
    _initializeClassElements(r.F, decorated.elements);
    return _runClassFinishers(r.F, decorated.finishers);
}
exports.default = _decorate;
function _createElementDescriptor(def) {
    var key = _toPropertyKeyDefault.default(def.key);
    var descriptor;
    if (def.kind === "method") {
        descriptor = {
            value: def.value,
            writable: true,
            configurable: true,
            enumerable: false
        };
        Object.defineProperty(def.value, "name", {
            value: _typeof(key) === "symbol" ? "" : key,
            configurable: true
        });
    } else if (def.kind === "get") descriptor = {
        get: def.value,
        configurable: true,
        enumerable: false
    };
    else if (def.kind === "set") descriptor = {
        set: def.value,
        configurable: true,
        enumerable: false
    };
    else if (def.kind === "field") descriptor = {
        configurable: true,
        writable: true,
        enumerable: true
    };
    var element = {
        kind: def.kind === "field" ? "field" : "method",
        key: key,
        placement: def.static ? "static" : def.kind === "field" ? "own" : "prototype",
        descriptor: descriptor
    };
    if (def.decorators) element.decorators = def.decorators;
    if (def.kind === "field") element.initializer = def.value;
    return element;
}
function _coalesceGetterSetter(element, other) {
    if (element.descriptor.get !== undefined) other.descriptor.get = element.descriptor.get;
    else other.descriptor.set = element.descriptor.set;
}
function _coalesceClassElements(elements) {
    var newElements = [];
    var isSameElement = function isSameElement(other) {
        return other.kind === "method" && other.key === element.key && other.placement === element.placement;
    };
    for(var i = 0; i < elements.length; i++){
        var element = elements[i];
        var other1;
        if (element.kind === "method" && (other1 = newElements.find(isSameElement))) {
            if (_isDataDescriptor(element.descriptor) || _isDataDescriptor(other1.descriptor)) {
                if (_hasDecorators(element) || _hasDecorators(other1)) throw new ReferenceError("Duplicated methods (" + element.key + ") can't be decorated.");
                other1.descriptor = element.descriptor;
            } else {
                if (_hasDecorators(element)) {
                    if (_hasDecorators(other1)) throw new ReferenceError("Decorators can't be placed on different accessors with for the same property (" + element.key + ").");
                    other1.decorators = element.decorators;
                }
                _coalesceGetterSetter(element, other1);
            }
        } else newElements.push(element);
    }
    return newElements;
}
function _hasDecorators(element) {
    return element.decorators && element.decorators.length;
}
function _isDataDescriptor(desc) {
    return desc !== undefined && !(desc.value === undefined && desc.writable === undefined);
}
function _initializeClassElements(F, elements) {
    var proto = F.prototype;
    [
        "method",
        "field"
    ].forEach(function(kind) {
        elements.forEach(function(element) {
            var placement = element.placement;
            if (element.kind === kind && (placement === "static" || placement === "prototype")) {
                var receiver = placement === "static" ? F : proto;
                _defineClassElement(receiver, element);
            }
        });
    });
}
function _initializeInstanceElements(O, elements) {
    [
        "method",
        "field"
    ].forEach(function(kind) {
        elements.forEach(function(element) {
            if (element.kind === kind && element.placement === "own") _defineClassElement(O, element);
        });
    });
}
function _defineClassElement(receiver, element) {
    var descriptor = element.descriptor;
    if (element.kind === "field") {
        var initializer = element.initializer;
        descriptor = {
            enumerable: descriptor.enumerable,
            writable: descriptor.writable,
            configurable: descriptor.configurable,
            value: initializer === void 0 ? void 0 : initializer.call(receiver)
        };
    }
    Object.defineProperty(receiver, element.key, descriptor);
}
function _decorateClass(elements, decorators) {
    var newElements = [];
    var finishers = [];
    var placements = {
        static: [],
        prototype: [],
        own: []
    };
    elements.forEach(function(element) {
        _addElementPlacement(element, placements);
    });
    elements.forEach(function(element) {
        if (!_hasDecorators(element)) return newElements.push(element);
        var elementFinishersExtras = _decorateElement(element, placements);
        newElements.push(elementFinishersExtras.element);
        newElements.push.apply(newElements, elementFinishersExtras.extras);
        finishers.push.apply(finishers, elementFinishersExtras.finishers);
    });
    if (!decorators) return {
        elements: newElements,
        finishers: finishers
    };
    var result = _decorateConstructor(newElements, decorators);
    finishers.push.apply(finishers, result.finishers);
    result.finishers = finishers;
    return result;
}
function _addElementPlacement(element, placements, silent) {
    var keys = placements[element.placement];
    if (!silent && keys.indexOf(element.key) !== -1) throw new TypeError("Duplicated element (" + element.key + ")");
    keys.push(element.key);
}
function _decorateElement(element, placements) {
    var extras = [];
    var finishers = [];
    for(var decorators = element.decorators, i = decorators.length - 1; i >= 0; i--){
        var keys = placements[element.placement];
        keys.splice(keys.indexOf(element.key), 1);
        var elementObject = _fromElementDescriptor(element);
        var elementFinisherExtras = _toElementFinisherExtras((0, decorators[i])(elementObject) || elementObject);
        element = elementFinisherExtras.element;
        _addElementPlacement(element, placements);
        if (elementFinisherExtras.finisher) finishers.push(elementFinisherExtras.finisher);
        var newExtras = elementFinisherExtras.extras;
        if (newExtras) {
            for(var j = 0; j < newExtras.length; j++)_addElementPlacement(newExtras[j], placements);
            extras.push.apply(extras, newExtras);
        }
    }
    return {
        element: element,
        finishers: finishers,
        extras: extras
    };
}
function _decorateConstructor(elements, decorators) {
    var finishers = [];
    for(var i = decorators.length - 1; i >= 0; i--){
        var obj = _fromClassDescriptor(elements);
        var elementsAndFinisher = _toClassDescriptor((0, decorators[i])(obj) || obj);
        if (elementsAndFinisher.finisher !== undefined) finishers.push(elementsAndFinisher.finisher);
        if (elementsAndFinisher.elements !== undefined) {
            elements = elementsAndFinisher.elements;
            for(var j = 0; j < elements.length - 1; j++)for(var k = j + 1; k < elements.length; k++){
                if (elements[j].key === elements[k].key && elements[j].placement === elements[k].placement) throw new TypeError("Duplicated element (" + elements[j].key + ")");
            }
        }
    }
    return {
        elements: elements,
        finishers: finishers
    };
}
function _fromElementDescriptor(element) {
    var obj = {
        kind: element.kind,
        key: element.key,
        placement: element.placement,
        descriptor: element.descriptor
    };
    var desc = {
        value: "Descriptor",
        configurable: true
    };
    Object.defineProperty(obj, Symbol.toStringTag, desc);
    if (element.kind === "field") obj.initializer = element.initializer;
    return obj;
}
function _toElementDescriptors(elementObjects) {
    if (elementObjects === undefined) return;
    return _toArrayDefault.default(elementObjects).map(function(elementObject) {
        var element = _toElementDescriptor(elementObject);
        _disallowProperty(elementObject, "finisher", "An element descriptor");
        _disallowProperty(elementObject, "extras", "An element descriptor");
        return element;
    });
}
function _toElementDescriptor(elementObject) {
    var kind = String(elementObject.kind);
    if (kind !== "method" && kind !== "field") throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "' + kind + '"');
    var key = _toPropertyKeyDefault.default(elementObject.key);
    var placement = String(elementObject.placement);
    if (placement !== "static" && placement !== "prototype" && placement !== "own") throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "' + placement + '"');
    var descriptor = elementObject.descriptor;
    _disallowProperty(elementObject, "elements", "An element descriptor");
    var element = {
        kind: kind,
        key: key,
        placement: placement,
        descriptor: Object.assign({}, descriptor)
    };
    if (kind !== "field") _disallowProperty(elementObject, "initializer", "A method descriptor");
    else {
        _disallowProperty(descriptor, "get", "The property descriptor of a field descriptor");
        _disallowProperty(descriptor, "set", "The property descriptor of a field descriptor");
        _disallowProperty(descriptor, "value", "The property descriptor of a field descriptor");
        element.initializer = elementObject.initializer;
    }
    return element;
}
function _toElementFinisherExtras(elementObject) {
    var element = _toElementDescriptor(elementObject);
    var finisher = _optionalCallableProperty(elementObject, "finisher");
    var extras = _toElementDescriptors(elementObject.extras);
    return {
        element: element,
        finisher: finisher,
        extras: extras
    };
}
function _fromClassDescriptor(elements) {
    var obj = {
        kind: "class",
        elements: elements.map(_fromElementDescriptor)
    };
    var desc = {
        value: "Descriptor",
        configurable: true
    };
    Object.defineProperty(obj, Symbol.toStringTag, desc);
    return obj;
}
function _toClassDescriptor(obj) {
    var kind = String(obj.kind);
    if (kind !== "class") throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "' + kind + '"');
    _disallowProperty(obj, "key", "A class descriptor");
    _disallowProperty(obj, "placement", "A class descriptor");
    _disallowProperty(obj, "descriptor", "A class descriptor");
    _disallowProperty(obj, "initializer", "A class descriptor");
    _disallowProperty(obj, "extras", "A class descriptor");
    var finisher = _optionalCallableProperty(obj, "finisher");
    var elements = _toElementDescriptors(obj.elements);
    return {
        elements: elements,
        finisher: finisher
    };
}
function _disallowProperty(obj, name, objectType) {
    if (obj[name] !== undefined) throw new TypeError(objectType + " can't have a ." + name + " property.");
}
function _optionalCallableProperty(obj, name) {
    var value = obj[name];
    if (value !== undefined && typeof value !== "function") throw new TypeError("Expected '" + name + "' to be a function");
    return value;
}
function _runClassFinishers(constructor, finishers) {
    for(var i = 0; i < finishers.length; i++){
        var newConstructor = (0, finishers[i])(constructor);
        if (newConstructor !== undefined) {
            if (typeof newConstructor !== "function") throw new TypeError("Finishers must return a constructor.");
            constructor = newConstructor;
        }
    }
    return constructor;
}

},{"./_to_array":"iaZDG","./_to_property_key":"61H7i","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"iaZDG":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _arrayWithHoles = require("./_array_with_holes");
var _arrayWithHolesDefault = parcelHelpers.interopDefault(_arrayWithHoles);
var _iterableToArray = require("./_iterable_to_array");
var _iterableToArrayDefault = parcelHelpers.interopDefault(_iterableToArray);
var _nonIterableRest = require("./_non_iterable_rest");
var _nonIterableRestDefault = parcelHelpers.interopDefault(_nonIterableRest);
var _unsupportedIterableToArray = require("./_unsupported_iterable_to_array");
var _unsupportedIterableToArrayDefault = parcelHelpers.interopDefault(_unsupportedIterableToArray);
function _toArray(arr) {
    return _arrayWithHolesDefault.default(arr) || _iterableToArrayDefault.default(arr) || _unsupportedIterableToArrayDefault.default(arr, i) || _nonIterableRestDefault.default();
}
exports.default = _toArray;

},{"./_array_with_holes":"hdkVj","./_iterable_to_array":"84rWR","./_non_iterable_rest":"eJPaJ","./_unsupported_iterable_to_array":"kbV8u","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"84rWR":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _iterableToArray(iter) {
    if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter);
}
exports.default = _iterableToArray;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"eJPaJ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _nonIterableRest() {
    throw new TypeError("Invalid attempt to destructure non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}
exports.default = _nonIterableRest;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"kbV8u":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _arrayLikeToArray = require("./_array_like_to_array");
var _arrayLikeToArrayDefault = parcelHelpers.interopDefault(_arrayLikeToArray);
function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === "string") return _arrayLikeToArrayDefault.default(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === "Object" && o.constructor) n = o.constructor.name;
    if (n === "Map" || n === "Set") return Array.from(n);
    if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArrayDefault.default(o, minLen);
}
exports.default = _unsupportedIterableToArray;

},{"./_array_like_to_array":"7Umy3","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"61H7i":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _typeOf = require("./_type_of");
var _typeOfDefault = parcelHelpers.interopDefault(_typeOf);
var _toPrimitive = require("./_to_primitive");
var _toPrimitiveDefault = parcelHelpers.interopDefault(_toPrimitive);
function _toPropertyKey(arg) {
    var key = _toPrimitiveDefault.default(arg, "string");
    return _typeOfDefault.default(key) === "symbol" ? key : String(key);
}
exports.default = _toPropertyKey;

},{"./_type_of":"jj0G7","./_to_primitive":"ixgwi","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ixgwi":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _typeOf = require("./_type_of");
var _typeOfDefault = parcelHelpers.interopDefault(_typeOf);
function _toPrimitive(input, hint) {
    if (_typeOfDefault.default(input) !== "object" || input === null) return input;
    var prim = input[Symbol.toPrimitive];
    if (prim !== undefined) {
        var res = prim.call(input, hint || "default");
        if (_typeOfDefault.default(res) !== "object") return res;
        throw new TypeError("@@toPrimitive must return a primitive value.");
    }
    return (hint === "string" ? String : Number)(input);
}
exports.default = _toPrimitive;

},{"./_type_of":"jj0G7","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4i4zb":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _defaults(obj, defaults) {
    var keys = Object.getOwnPropertyNames(defaults);
    for(var i = 0; i < keys.length; i++){
        var key = keys[i];
        var value = Object.getOwnPropertyDescriptor(defaults, key);
        if (value && value.configurable && obj[key] === undefined) Object.defineProperty(obj, key, value);
    }
    return obj;
}
exports.default = _defaults;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"cXWLD":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _defineEnumerableProperties(obj, descs) {
    for(var key in descs){
        var desc = descs[key];
        desc.configurable = desc.enumerable = true;
        if ("value" in desc) desc.writable = true;
        Object.defineProperty(obj, key, desc);
    }
    if (Object.getOwnPropertySymbols) {
        var objectSymbols = Object.getOwnPropertySymbols(descs);
        for(var i = 0; i < objectSymbols.length; i++){
            var sym = objectSymbols[i];
            var desc = descs[sym];
            desc.configurable = desc.enumerable = true;
            if ("value" in desc) desc.writable = true;
            Object.defineProperty(obj, sym, desc);
        }
    }
    return obj;
}
exports.default = _defineEnumerableProperties;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"6oPi2":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _defineProperty(obj, key, value) {
    if (key in obj) Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
    });
    else obj[key] = value;
    return obj;
}
exports.default = _defineProperty;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"j68CL":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function extends_() {
    extends_ = Object.assign || function(target) {
        for(var i = 1; i < arguments.length; i++){
            var source = arguments[i];
            for(var key in source)if (Object.prototype.hasOwnProperty.call(source, key)) target[key] = source[key];
        }
        return target;
    };
    return extends_.apply(this, arguments);
}
function _extends() {
    return extends_.apply(this, arguments);
}
exports.default = _extends;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"3Ctd3":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _superPropBase = require("./_super_prop_base");
var _superPropBaseDefault = parcelHelpers.interopDefault(_superPropBase);
function get(target1, property1, receiver1) {
    if (typeof Reflect !== "undefined" && Reflect.get) get = Reflect.get;
    else get = function get(target, property, receiver) {
        var base = _superPropBaseDefault.default(target, property);
        if (!base) return;
        var desc = Object.getOwnPropertyDescriptor(base, property);
        if (desc.get) return desc.get.call(receiver || target);
        return desc.value;
    };
    return get(target1, property1, receiver1);
}
function _get(target, property, reciever) {
    return get(target, property, reciever);
}
exports.default = _get;

},{"./_super_prop_base":"1UTk2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"1UTk2":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getPrototypeOf = require("./_get_prototype_of");
var _getPrototypeOfDefault = parcelHelpers.interopDefault(_getPrototypeOf);
function _superPropBase(object, property) {
    while(!Object.prototype.hasOwnProperty.call(object, property)){
        object = _getPrototypeOfDefault.default(object);
        if (object === null) break;
    }
    return object;
}
exports.default = _superPropBase;

},{"./_get_prototype_of":"6HtCT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bxQnN":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _setPrototypeOf = require("./_set_prototype_of");
var _setPrototypeOfDefault = parcelHelpers.interopDefault(_setPrototypeOf);
function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) throw new TypeError("Super expression must either be null or a function");
    subClass.prototype = Object.create(superClass && superClass.prototype, {
        constructor: {
            value: subClass,
            writable: true,
            configurable: true
        }
    });
    if (superClass) _setPrototypeOfDefault.default(subClass, superClass);
}
exports.default = _inherits;

},{"./_set_prototype_of":"lLpOg","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"klWjZ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _inheritsLoose(subClass, superClass) {
    subClass.prototype = Object.create(superClass.prototype);
    subClass.prototype.constructor = subClass;
    subClass.__proto__ = superClass;
}
exports.default = _inheritsLoose;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"1oAt5":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _initializerDefineProperty(target, property, descriptor, context) {
    if (!descriptor) return;
    Object.defineProperty(target, property, {
        enumerable: descriptor.enumerable,
        configurable: descriptor.configurable,
        writable: descriptor.writable,
        value: descriptor.initializer ? descriptor.initializer.call(context) : void 0
    });
}
exports.default = _initializerDefineProperty;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9PAfr":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _initializerWarningHelper(descriptor, context) {
    throw new Error("Decorating class property failed. Please ensure that proposal-class-properties is enabled and set to use loose mode. To use proposal-class-properties in spec mode with decorators, wait for the next major version of decorators in stage 2.");
}
exports.default = _initializerWarningHelper;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jTvrY":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _instanceof(left, right) {
    if (right != null && typeof Symbol !== "undefined" && right[Symbol.hasInstance]) return !!right[Symbol.hasInstance](left);
    else return left instanceof right;
}
exports.default = _instanceof;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"95JHK":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _interopRequireDefault(obj) {
    return obj && obj.__esModule ? obj : {
        default: obj
    };
}
exports.default = _interopRequireDefault;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"3WUUn":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _interopRequireWildcard(obj) {
    if (obj && obj.__esModule) return obj;
    else {
        var newObj = {};
        if (obj != null) {
            for(var key in obj)if (Object.prototype.hasOwnProperty.call(obj, key)) {
                var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {};
                if (desc.get || desc.set) Object.defineProperty(newObj, key, desc);
                else newObj[key] = obj[key];
            }
        }
        newObj.default = obj;
        return newObj;
    }
}
exports.default = _interopRequireWildcard;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"6NiqX":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _isNativeFunction(fn) {
    return Function.toString.call(fn).indexOf("[native code]") !== -1;
}
exports.default = _isNativeFunction;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"i9TMH":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _iterableToArrayLimit(arr, i) {
    var _i = arr == null ? null : typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"];
    if (_i == null) return;
    var _arr = [];
    var _n = true;
    var _d = false;
    var _s, _e;
    try {
        for(_i = _i.call(arr); !(_n = (_s = _i.next()).done); _n = true){
            _arr.push(_s.value);
            if (i && _arr.length === i) break;
        }
    } catch (err) {
        _d = true;
        _e = err;
    } finally{
        try {
            if (!_n && _i["return"] != null) _i["return"]();
        } finally{
            if (_d) throw _e;
        }
    }
    return _arr;
}
exports.default = _iterableToArrayLimit;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bcCsX":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _iterableToArrayLimitLoose(arr, i) {
    var _i = arr && (typeof Symbol !== "undefined" && arr[Symbol.iterator] || arr["@@iterator"]);
    if (_i == null) return;
    var _arr = [];
    for(_i = _i.call(arr); !(_step = _i.next()).done;){
        _arr.push(_step.value);
        if (i && _arr.length === i) break;
    }
    return _arr;
}
exports.default = _iterableToArrayLimitLoose;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jXjsO":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var REACT_ELEMENT_TYPE;
function _createRawReactElement(type, props, key, children) {
    if (!REACT_ELEMENT_TYPE) REACT_ELEMENT_TYPE = typeof Symbol === "function" && Symbol.for && Symbol.for("react.element") || 60103;
    var defaultProps = type && type.defaultProps;
    var childrenLength = arguments.length - 3;
    if (!props && childrenLength !== 0) props = {
        children: void 0
    };
    if (props && defaultProps) {
        for(var propName in defaultProps)if (props[propName] === void 0) props[propName] = defaultProps[propName];
    } else if (!props) props = defaultProps || {};
    if (childrenLength === 1) props.children = children;
    else if (childrenLength > 1) {
        var childArray = new Array(childrenLength);
        for(var i = 0; i < childrenLength; i++)childArray[i] = arguments[i + 3];
        props.children = childArray;
    }
    return {
        $$typeof: REACT_ELEMENT_TYPE,
        type: type,
        key: key === undefined ? null : '' + key,
        ref: null,
        props: props,
        _owner: null
    };
}
exports.default = _createRawReactElement;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"el295":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _newArrowCheck(innerThis, boundThis) {
    if (innerThis !== boundThis) throw new TypeError("Cannot instantiate an arrow function");
}
exports.default = _newArrowCheck;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ihzXr":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _nonIterableSpread() {
    throw new TypeError("Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
}
exports.default = _nonIterableSpread;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"aLguo":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _defineProperty = require("./_define_property");
var _definePropertyDefault = parcelHelpers.interopDefault(_defineProperty);
function _objectSpread(target) {
    for(var i = 1; i < arguments.length; i++){
        var source = arguments[i] != null ? arguments[i] : {};
        var ownKeys = Object.keys(source);
        if (typeof Object.getOwnPropertySymbols === 'function') ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function(sym) {
            return Object.getOwnPropertyDescriptor(source, sym).enumerable;
        }));
        ownKeys.forEach(function(key) {
            _definePropertyDefault.default(target, key, source[key]);
        });
    }
    return target;
}
exports.default = _objectSpread;

},{"./_define_property":"6oPi2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"clNOR":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _objectWithoutPropertiesLoose = require("./_object_without_properties_loose");
var _objectWithoutPropertiesLooseDefault = parcelHelpers.interopDefault(_objectWithoutPropertiesLoose);
function _objectWithoutProperties(source, excluded) {
    if (source == null) return {};
    var target = _objectWithoutPropertiesLooseDefault.default(source, excluded);
    var key, i;
    if (Object.getOwnPropertySymbols) {
        var sourceSymbolKeys = Object.getOwnPropertySymbols(source);
        for(i = 0; i < sourceSymbolKeys.length; i++){
            key = sourceSymbolKeys[i];
            if (excluded.indexOf(key) >= 0) continue;
            if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
            target[key] = source[key];
        }
    }
    return target;
}
exports.default = _objectWithoutProperties;

},{"./_object_without_properties_loose":"2AAov","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"2AAov":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _objectWithoutPropertiesLoose(source, excluded) {
    if (source == null) return {};
    var target = {};
    var sourceKeys = Object.keys(source);
    var key, i;
    for(i = 0; i < sourceKeys.length; i++){
        key = sourceKeys[i];
        if (excluded.indexOf(key) >= 0) continue;
        target[key] = source[key];
    }
    return target;
}
exports.default = _objectWithoutPropertiesLoose;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"25q9F":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _readOnlyError(name) {
    throw new Error("\"" + name + "\" is read-only");
}
exports.default = _readOnlyError;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"lYl68":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _defineProperty = require("./_define_property");
var _definePropertyDefault = parcelHelpers.interopDefault(_defineProperty);
var _superPropBase = require("./_super_prop_base");
var _superPropBaseDefault = parcelHelpers.interopDefault(_superPropBase);
function set(target1, property1, value1, receiver1) {
    if (typeof Reflect !== "undefined" && Reflect.set) set = Reflect.set;
    else set = function set(target, property, value, receiver) {
        var base = _superPropBaseDefault.default(target, property);
        var desc;
        if (base) {
            desc = Object.getOwnPropertyDescriptor(base, property);
            if (desc.set) {
                desc.set.call(receiver, value);
                return true;
            } else if (!desc.writable) return false;
        }
        desc = Object.getOwnPropertyDescriptor(receiver, property);
        if (desc) {
            if (!desc.writable) return false;
            desc.value = value;
            Object.defineProperty(receiver, property, desc);
        } else _definePropertyDefault.default(receiver, property, value);
        return true;
    };
    return set(target1, property1, value1, receiver1);
}
function _set(target, property, value, receiver, isStrict) {
    var s = set(target, property, value, receiver || target);
    if (!s && isStrict) throw new Error('failed to set property');
    return value;
}
exports.default = _set;

},{"./_define_property":"6oPi2","./_super_prop_base":"1UTk2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"1oSeh":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _skipFirstGeneratorNext(fn) {
    return function() {
        var it = fn.apply(this, arguments);
        it.next();
        return it;
    };
}
exports.default = _skipFirstGeneratorNext;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"cILUy":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _arrayWithHoles = require("./_array_with_holes");
var _arrayWithHolesDefault = parcelHelpers.interopDefault(_arrayWithHoles);
var _iterableToArray = require("./_iterable_to_array");
var _iterableToArrayDefault = parcelHelpers.interopDefault(_iterableToArray);
var _nonIterableRest = require("./_non_iterable_rest");
var _nonIterableRestDefault = parcelHelpers.interopDefault(_nonIterableRest);
var _unsupportedIterableToArray = require("./_unsupported_iterable_to_array");
var _unsupportedIterableToArrayDefault = parcelHelpers.interopDefault(_unsupportedIterableToArray);
function _slicedToArray(arr, i) {
    return _arrayWithHolesDefault.default(arr) || _iterableToArrayDefault.default(arr, i) || _unsupportedIterableToArrayDefault.default(arr, i) || _nonIterableRestDefault.default();
}
exports.default = _slicedToArray;

},{"./_array_with_holes":"hdkVj","./_iterable_to_array":"84rWR","./_non_iterable_rest":"eJPaJ","./_unsupported_iterable_to_array":"kbV8u","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"icOVf":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _arrayWithHoles = require("./_array_with_holes");
var _arrayWithHolesDefault = parcelHelpers.interopDefault(_arrayWithHoles);
var _iterableToArrayLimitLoose = require("./_iterable_to_array_limit_loose");
var _iterableToArrayLimitLooseDefault = parcelHelpers.interopDefault(_iterableToArrayLimitLoose);
var _nonIterableRest = require("./_non_iterable_rest");
var _nonIterableRestDefault = parcelHelpers.interopDefault(_nonIterableRest);
var _unsupportedIterableToArray = require("./_unsupported_iterable_to_array");
var _unsupportedIterableToArrayDefault = parcelHelpers.interopDefault(_unsupportedIterableToArray);
function _slicedToArrayLoose(arr, i) {
    return _arrayWithHolesDefault.default(arr) || _iterableToArrayLimitLooseDefault.default(arr, i) || _unsupportedIterableToArrayDefault.default(arr, i) || _nonIterableRestDefault.default();
}
exports.default = _slicedToArrayLoose;

},{"./_array_with_holes":"hdkVj","./_iterable_to_array_limit_loose":"bcCsX","./_non_iterable_rest":"eJPaJ","./_unsupported_iterable_to_array":"kbV8u","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ddLTO":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _taggedTemplateLiteral(strings, raw) {
    if (!raw) raw = strings.slice(0);
    return Object.freeze(Object.defineProperties(strings, {
        raw: {
            value: Object.freeze(raw)
        }
    }));
}
exports.default = _taggedTemplateLiteral;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bYUuZ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _taggedTemplateLiteralLoose(strings, raw) {
    if (!raw) raw = strings.slice(0);
    strings.raw = raw;
    return strings;
}
exports.default = _taggedTemplateLiteralLoose;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9U50I":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function _throw(e) {
    throw e;
}
exports.default = _throw;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4aEni":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _arrayWithoutHoles = require("./_array_without_holes");
var _arrayWithoutHolesDefault = parcelHelpers.interopDefault(_arrayWithoutHoles);
var _iterableToArray = require("./_iterable_to_array");
var _iterableToArrayDefault = parcelHelpers.interopDefault(_iterableToArray);
var _nonIterableSpread = require("./_non_iterable_spread");
var _nonIterableSpreadDefault = parcelHelpers.interopDefault(_nonIterableSpread);
var _unsupportedIterableToArray = require("./_unsupported_iterable_to_array");
var _unsupportedIterableToArrayDefault = parcelHelpers.interopDefault(_unsupportedIterableToArray);
function _toConsumableArray(arr) {
    return _arrayWithoutHolesDefault.default(arr) || _iterableToArrayDefault.default(arr) || _unsupportedIterableToArrayDefault.default(arr) || _nonIterableSpreadDefault.default();
}
exports.default = _toConsumableArray;

},{"./_array_without_holes":"l74UH","./_iterable_to_array":"84rWR","./_non_iterable_spread":"ihzXr","./_unsupported_iterable_to_array":"kbV8u","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9mZxY":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _asyncGenerator = require("./_async_generator");
var _asyncGeneratorDefault = parcelHelpers.interopDefault(_asyncGenerator);
function _wrapAsyncGenerator(fn) {
    return function() {
        return new _asyncGeneratorDefault.default(fn.apply(this, arguments));
    };
}
exports.default = _wrapAsyncGenerator;

},{"./_async_generator":"QOozV","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"gTQpL":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _construct = require("./_construct");
var _constructDefault = parcelHelpers.interopDefault(_construct);
var _isNativeFunction = require("./_is_native_function");
var _isNativeFunctionDefault = parcelHelpers.interopDefault(_isNativeFunction);
var _getPrototypeOf = require("./_get_prototype_of");
var _getPrototypeOfDefault = parcelHelpers.interopDefault(_getPrototypeOf);
var _setPrototypeOf = require("./_set_prototype_of");
var _setPrototypeOfDefault = parcelHelpers.interopDefault(_setPrototypeOf);
function wrapNativeSuper(Class1) {
    var _cache = typeof Map === "function" ? new Map() : undefined;
    wrapNativeSuper = function wrapNativeSuper(Class) {
        if (Class === null || !_isNativeFunctionDefault.default(Class)) return Class;
        if (typeof Class !== "function") throw new TypeError("Super expression must either be null or a function");
        if (typeof _cache !== "undefined") {
            if (_cache.has(Class)) return _cache.get(Class);
            _cache.set(Class, Wrapper);
        }
        function Wrapper() {
            return _constructDefault.default(Class, arguments, _getPrototypeOfDefault.default(this).constructor);
        }
        Wrapper.prototype = Object.create(Class.prototype, {
            constructor: {
                value: Wrapper,
                enumerable: false,
                writable: true,
                configurable: true
            }
        });
        return _setPrototypeOfDefault.default(Wrapper, Class);
    };
    return wrapNativeSuper(Class1);
}
function _wrapNativeSuper(Class) {
    return wrapNativeSuper(Class);
}
exports.default = _wrapNativeSuper;

},{"./_construct":"fWjGA","./_is_native_function":"6NiqX","./_get_prototype_of":"6HtCT","./_set_prototype_of":"lLpOg","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"k2qRb":[function(require,module,exports) {
$.fn.changeElementType = function(newType) {
    var attrs = {};
    $.each(this[0].attributes, function(idx, attr) {
        attrs[attr.nodeName] = attr.nodeValue;
    });
    var newelement = $("<" + newType + "/>", attrs).append($(this).contents());
    this.replaceWith(newelement);
    return newelement;
};
$("[data-max-length]").each(function() {
    var originalText = $(this).html();
    var shrunkText = $(this).html().substring(0, $(this).data("max-length"));
    if (originalText.length != shrunkText.length) {
        $(this).html(shrunkText + "...");
        var $more = $("<a href='#' class='govuk-link govuk-link--no-visited-state govuk-!-margin-left-2'>More</a>").appendTo($(this));
        $more.attr("data-more-text", originalText);
    }
});
$("[data-more-text]").click(function() {
    $(this).parent().html($(this).data("more-text"));
    return false;
});
$("[data-definition-title]").each(function() {
    $(this).addClass("lite-link--definition");
    $(this).changeElementType("a").attr("href", "#");
});
$("[data-definition-title]").click(function() {
    var subtitle = $(this).data("definition-subtitle");
    var text = $(this).data("definition-text");
    var list = $(this).data("definition-list");
    if (list) list = list.split(",");
    var htmlList = "<ol class='govuk-list govuk-list--number'>";
    if (list) for(var i = 0; i < list.length; i++)htmlList += "<li>" + list[i] + "</li>";
    htmlList = htmlList + "</ol>";
    if (subtitle) {
        subtitle = "<p class='govuk-heading-s'>" + subtitle + "</p>";
        if (text) text = subtitle + text;
        else htmlList = subtitle + htmlList;
    }
    LITECommon.Modal.showModal($(this).data("definition-title"), text || htmlList, false, true, {
        maxWidth: "500px"
    });
    return false;
});

},{}],"8PnXz":[function(require,module,exports) {
$(".govuk-back-link").on("click", function() {
    var address = $(this).attr("href");
    if (address != "#") window.location.href = address;
    else window.history.go(-1);
    return false;
});

},{}],"js6nW":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _helpers = require("@swc/helpers");
var _consts = require("./consts");
var _utils = require("./utils");
var COOKIE_PREFERENCES_CLASS_NAME = "cookie-preferences";
var SHOW_BANNER_CLASS_NAME = "app-cookie-banner--show";
var CookieBanner = /*#__PURE__*/ function() {
    "use strict";
    function CookieBanner(bannerClassName, acceptAllButtonClassName) {
        _helpers.classCallCheck(this, CookieBanner);
        this.bannerClassName = bannerClassName;
        this.banner = document.querySelector(".".concat(this.bannerClassName));
        this.acceptAllButtonClassName = acceptAllButtonClassName;
    }
    _helpers.createClass(CookieBanner, [
        {
            key: "hasAcceptedCookePreferences",
            value: function hasAcceptedCookePreferences() {
                var cookie = _utils.getCookie(_consts.PREFERENCES_COOKIE_NAME);
                return Boolean(cookie);
            }
        },
        {
            key: "isExcludedPage",
            value: function isExcludedPage() {
                var cookiePreferencesEl = document.querySelector(".".concat(COOKIE_PREFERENCES_CLASS_NAME));
                return Boolean(cookiePreferencesEl);
            }
        },
        {
            key: "shouldDisplay",
            value: function shouldDisplay() {
                return Boolean(this.banner) && !this.hasAcceptedCookePreferences() && !this.isExcludedPage();
            }
        },
        {
            key: "acceptAllCookies",
            value: function acceptAllCookies() {
                _utils.setPoliciesCookie(false, true, false);
                _utils.setPreferencesCookie();
            }
        },
        {
            key: "hide",
            value: function hide() {
                this.banner.classList.remove(SHOW_BANNER_CLASS_NAME);
            }
        },
        {
            key: "attachEvents",
            value: function attachEvents(banner) {
                var _this = this;
                var button = banner.querySelector(".".concat(this.acceptAllButtonClassName));
                button.addEventListener("click", function() {
                    _this.acceptAllCookies();
                    _this.hide();
                });
            }
        },
        {
            key: "display",
            value: function display() {
                this.banner.classList.add(SHOW_BANNER_CLASS_NAME);
                this.attachEvents(this.banner);
            }
        }
    ]);
    return CookieBanner;
}();
var initCookieBanner = function(bannerClassName, acceptAllButtonClassName) {
    var cookieBanner = new CookieBanner(bannerClassName, acceptAllButtonClassName);
    if (cookieBanner.shouldDisplay()) cookieBanner.display();
};
exports.default = initCookieBanner;

},{"@swc/helpers":"3OBsq","./consts":"8nHwb","./utils":"lT1Jx","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"8nHwb":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "POLICY_COOKIE_NAME", function() {
    return POLICY_COOKIE_NAME;
});
parcelHelpers.export(exports, "POLICY_COOKIE_DURATION_DAYS", function() {
    return POLICY_COOKIE_DURATION_DAYS;
});
parcelHelpers.export(exports, "PREFERENCES_COOKIE_NAME", function() {
    return PREFERENCES_COOKIE_NAME;
});
parcelHelpers.export(exports, "PREFERENCES_COOKIE_DURATION_DAYS", function() {
    return PREFERENCES_COOKIE_DURATION_DAYS;
});
var POLICY_COOKIE_NAME = "cookies_policy";
var POLICY_COOKIE_DURATION_DAYS = 365;
var PREFERENCES_COOKIE_NAME = "cookie_preferences_set";
var PREFERENCES_COOKIE_DURATION_DAYS = 365;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"lT1Jx":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "getCookie", function() {
    return getCookie;
});
parcelHelpers.export(exports, "setCookie", function() {
    return setCookie;
});
parcelHelpers.export(exports, "getDefaultPolicy", function() {
    return getDefaultPolicy;
});
parcelHelpers.export(exports, "setPoliciesCookie", function() {
    return setPoliciesCookie;
});
parcelHelpers.export(exports, "setPreferencesCookie", function() {
    return setPreferencesCookie;
});
var _consts = require("./consts");
var getCookie = function(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(";");
    for(var i = 0, len = cookies.length; i < len; i++){
        var cookie = cookies[i];
        while(cookie.charAt(0) === " ")cookie = cookie.substring(1, cookie.length);
        if (cookie.indexOf(nameEQ) === 0) return decodeURIComponent(cookie.substring(nameEQ.length));
    }
    return null;
};
var setCookie = function(name, value, options) {
    if (typeof options === "undefined") options = {};
    var cookieString = name + "=" + value + "; path=/";
    if (options.days) {
        var date = new Date();
        date.setTime(date.getTime() + options.days * 86400000);
        cookieString = cookieString + "; expires=" + date.toGMTString();
    }
    if (document.location.protocol === "https:") cookieString = cookieString + "; Secure";
    document.cookie = cookieString;
};
var getDefaultPolicy = function() {
    return {
        essential: true,
        settings: false,
        usage: false,
        campaigns: false
    };
};
var setPoliciesCookie = function(settings, usage, campaigns) {
    var policy = getDefaultPolicy();
    policy.settings = settings || false;
    policy.usage = usage || false;
    policy.campaigns = campaigns || false;
    var json = JSON.stringify(policy);
    setCookie(_consts.POLICY_COOKIE_NAME, json, {
        days: _consts.POLICY_COOKIE_DURATION_DAYS
    });
    return policy;
};
var setPreferencesCookie = function() {
    setCookie(_consts.PREFERENCES_COOKIE_NAME, "true", {
        days: _consts.PREFERENCES_COOKIE_DURATION_DAYS
    });
};

},{"./consts":"8nHwb","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"7TpU4":[function(require,module,exports) {
$("input:checkbox").change(function() {
    setSelectButtonsState();
});
$(".lite-button-checkbox").click(function() {
    var $table = $(this).closest("table");
    if ($table.find("input:checkbox:checked").length == $table.find("input:checkbox").length) $table.find("input:checkbox").prop("checked", false).change();
    else $table.find("input:checkbox").prop("checked", true).change();
    setSelectButtonsState();
});
function setSelectButtonsState() {
    $("table").each(function(i, obj) {
        $(obj).find(".lite-button-checkbox").attr("class", "lite-button-checkbox");
        if ($(obj).find("input:checkbox:checked").length == $(obj).find("input:checkbox").length) $(obj).find(".lite-button-checkbox").addClass("lite-button-checkbox--checked");
        else if ($(obj).find("input:checkbox:checked").length != 0) $(obj).find(".lite-button-checkbox").addClass("lite-button-checkbox--indeterminate");
        // Force Webkit to repaint the button
        // DON'T REMOVE!
        $(obj).find(".lite-button-checkbox").css("display", "none").height();
        $(obj).find(".lite-button-checkbox").css("display", "block");
    });
}

},{}],"VYyUs":[function(require,module,exports) {
function tryShowFilterBar() {
    $(".lite-filter-bar").each(function() {
        var $filters = $(this).parent();
        $filters.hide();
        $filters.prev().find("#show-filters-link").show();
        $filters.prev().find("#hide-filters-link").hide();
        $(this).find("input, select").each(function() {
            if ($(this).val() != "" && $(this).val() != "Select" && $(this).val() != "blank" && $(this).attr("type") != "hidden" && ($(this).attr("type") != "checkbox" || $(this).attr("type") == "checkbox" && $(this).attr("checked"))) {
                $filters.show();
                $filters.prev().find("#show-filters-link").hide();
                $filters.prev().find("#hide-filters-link").show();
                $(this).parents(".govuk-details").attr("open", "");
            }
        });
    });
}
tryShowFilterBar();
$(".lite-filter-toggle-link").unbind().click(function() {
    var $filters = $(this).parent().next();
    $filters.toggle();
    $(this).parent().find("> *").toggle();
    return false;
});

},{}],"6PcMs":[function(require,module,exports) {
function enableControls($selector) {
    $selector.find(".govuk-button").each(function() {
        enableButton($(this));
    });
}
function disableControls($selector) {
    $selector.find(".govuk-button").each(function() {
        disableButton($(this));
    });
}
$("[data-enable-on-checkboxes]").each(function() {
    var $controls = $(this);
    var $parentSelector = $($(this).data("enable-on-checkboxes"));
    var $checkboxesSelector = $($(this).data("enable-on-checkboxes") + " .govuk-checkboxes__input");
    if ($parentSelector.find(":checked").length > 0) enableControls($controls);
    else disableControls($controls);
    $checkboxesSelector.change(function() {
        if ($parentSelector.find(":checked").length > 0) enableControls($controls);
        else disableControls($controls);
    });
});

},{}],"g9cUM":[function(require,module,exports) {
$(".app-snackbar__close-link").click(function() {
    $(this).parent().parent().hide();
    return false;
});

},{}],"2cI33":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _tippyJs = require("tippy.js");
var _tippyJsDefault = parcelHelpers.interopDefault(_tippyJs);
function initMenuTooltips() {
    $("#link-menu").removeAttr("href");
    // deliberately written in vanilla JS not jquery
    var menu = document.getElementById("lite-menu");
    if (!menu) return;
    menu.style.display = "block";
    _tippyJsDefault.default("#link-menu", {
        content: menu,
        allowHTML: true,
        interactive: true,
        animation: "scale-subtle",
        trigger: "click",
        theme: "light",
        placement: "bottom"
    });
    _tippyJsDefault.default("*[data-tooltip]", {
        content: function(reference) {
            return reference.getAttribute("data-tooltip");
        },
        allowHTML: true,
        animation: "scale-subtle"
    });
    _tippyJsDefault.default(".app-flag--label", {
        content: function(reference) {
            return reference.getAttribute("data-label");
        }
    });
}
exports.default = initMenuTooltips;

},{"tippy.js":"kxABc","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"kxABc":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "animateFill", function() {
    return animateFill;
});
parcelHelpers.export(exports, "createSingleton", function() {
    return createSingleton;
});
parcelHelpers.export(exports, "delegate", function() {
    return delegate;
});
parcelHelpers.export(exports, "followCursor", function() {
    return followCursor;
});
parcelHelpers.export(exports, "hideAll", function() {
    return hideAll;
});
parcelHelpers.export(exports, "inlinePositioning", function() {
    return inlinePositioning;
});
parcelHelpers.export(exports, "roundArrow", function() {
    return ROUND_ARROW;
});
parcelHelpers.export(exports, "sticky", function() {
    return sticky;
});
/**!
* tippy.js v6.2.6
* (c) 2017-2020 atomiks
* MIT License
*/ var _core = require("@popperjs/core");
var ROUND_ARROW = '<svg width="16" height="6" xmlns="http://www.w3.org/2000/svg"><path d="M0 6s1.796-.013 4.67-3.615C5.851.9 6.93.006 8 0c1.07-.006 2.148.887 3.343 2.385C14.233 6.005 16 6 16 6H0z"></svg>';
var BOX_CLASS = "tippy-box";
var CONTENT_CLASS = "tippy-content";
var BACKDROP_CLASS = "tippy-backdrop";
var ARROW_CLASS = "tippy-arrow";
var SVG_ARROW_CLASS = "tippy-svg-arrow";
var TOUCH_OPTIONS = {
    passive: true,
    capture: true
};
function hasOwnProperty(obj, key) {
    return ({}).hasOwnProperty.call(obj, key);
}
function getValueAtIndexOrReturn(value, index, defaultValue) {
    if (Array.isArray(value)) {
        var v = value[index];
        return v == null ? Array.isArray(defaultValue) ? defaultValue[index] : defaultValue : v;
    }
    return value;
}
function isType(value, type) {
    var str = ({}).toString.call(value);
    return str.indexOf('[object') === 0 && str.indexOf(type + "]") > -1;
}
function invokeWithArgsOrReturn(value, args) {
    return typeof value === 'function' ? value.apply(void 0, args) : value;
}
function debounce(fn, ms) {
    // Avoid wrapping in `setTimeout` if ms is 0 anyway
    if (ms === 0) return fn;
    var timeout;
    return function(arg) {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            fn(arg);
        }, ms);
    };
}
function removeProperties(obj, keys) {
    var clone = Object.assign({}, obj);
    keys.forEach(function(key) {
        delete clone[key];
    });
    return clone;
}
function splitBySpaces(value) {
    return value.split(/\s+/).filter(Boolean);
}
function normalizeToArray(value) {
    return [].concat(value);
}
function pushIfUnique(arr, value) {
    if (arr.indexOf(value) === -1) arr.push(value);
}
function unique(arr) {
    return arr.filter(function(item, index) {
        return arr.indexOf(item) === index;
    });
}
function getBasePlacement(placement) {
    return placement.split('-')[0];
}
function arrayFrom(value) {
    return [].slice.call(value);
}
function removeUndefinedProps(obj) {
    return Object.keys(obj).reduce(function(acc, key) {
        if (obj[key] !== undefined) acc[key] = obj[key];
        return acc;
    }, {});
}
function div() {
    return document.createElement('div');
}
function isElement(value) {
    return [
        'Element',
        'Fragment'
    ].some(function(type) {
        return isType(value, type);
    });
}
function isNodeList(value) {
    return isType(value, 'NodeList');
}
function isMouseEvent(value) {
    return isType(value, 'MouseEvent');
}
function isReferenceElement(value) {
    return !!(value && value._tippy && value._tippy.reference === value);
}
function getArrayOfElements(value) {
    if (isElement(value)) return [
        value
    ];
    if (isNodeList(value)) return arrayFrom(value);
    if (Array.isArray(value)) return value;
    return arrayFrom(document.querySelectorAll(value));
}
function setTransitionDuration(els, value) {
    els.forEach(function(el) {
        if (el) el.style.transitionDuration = value + "ms";
    });
}
function setVisibilityState(els, state) {
    els.forEach(function(el) {
        if (el) el.setAttribute('data-state', state);
    });
}
function getOwnerDocument(elementOrElements) {
    var _normalizeToArray = normalizeToArray(elementOrElements), element = _normalizeToArray[0];
    return element ? element.ownerDocument || document : document;
}
function isCursorOutsideInteractiveBorder(popperTreeData, event) {
    var clientX = event.clientX, clientY = event.clientY;
    return popperTreeData.every(function(_ref) {
        var popperRect = _ref.popperRect, popperState = _ref.popperState, props = _ref.props;
        var interactiveBorder = props.interactiveBorder;
        var basePlacement = getBasePlacement(popperState.placement);
        var offsetData = popperState.modifiersData.offset;
        if (!offsetData) return true;
        var topDistance = basePlacement === 'bottom' ? offsetData.top.y : 0;
        var bottomDistance = basePlacement === 'top' ? offsetData.bottom.y : 0;
        var leftDistance = basePlacement === 'right' ? offsetData.left.x : 0;
        var rightDistance = basePlacement === 'left' ? offsetData.right.x : 0;
        var exceedsTop = popperRect.top - clientY + topDistance > interactiveBorder;
        var exceedsBottom = clientY - popperRect.bottom - bottomDistance > interactiveBorder;
        var exceedsLeft = popperRect.left - clientX + leftDistance > interactiveBorder;
        var exceedsRight = clientX - popperRect.right - rightDistance > interactiveBorder;
        return exceedsTop || exceedsBottom || exceedsLeft || exceedsRight;
    });
}
function updateTransitionEndListener(box, action, listener) {
    var method = action + "EventListener"; // some browsers apparently support `transition` (unprefixed) but only fire
    // `webkitTransitionEnd`...
    [
        'transitionend',
        'webkitTransitionEnd'
    ].forEach(function(event) {
        box[method](event, listener);
    });
}
var currentInput = {
    isTouch: false
};
var lastMouseMoveTime = 0;
/**
 * When a `touchstart` event is fired, it's assumed the user is using touch
 * input. We'll bind a `mousemove` event listener to listen for mouse input in
 * the future. This way, the `isTouch` property is fully dynamic and will handle
 * hybrid devices that use a mix of touch + mouse input.
 */ function onDocumentTouchStart() {
    if (currentInput.isTouch) return;
    currentInput.isTouch = true;
    if (window.performance) document.addEventListener('mousemove', onDocumentMouseMove);
}
/**
 * When two `mousemove` event are fired consecutively within 20ms, it's assumed
 * the user is using mouse input again. `mousemove` can fire on touch devices as
 * well, but very rarely that quickly.
 */ function onDocumentMouseMove() {
    var now = performance.now();
    if (now - lastMouseMoveTime < 20) {
        currentInput.isTouch = false;
        document.removeEventListener('mousemove', onDocumentMouseMove);
    }
    lastMouseMoveTime = now;
}
/**
 * When an element is in focus and has a tippy, leaving the tab/window and
 * returning causes it to show again. For mouse users this is unexpected, but
 * for keyboard use it makes sense.
 * TODO: find a better technique to solve this problem
 */ function onWindowBlur() {
    var activeElement = document.activeElement;
    if (isReferenceElement(activeElement)) {
        var instance = activeElement._tippy;
        if (activeElement.blur && !instance.state.isVisible) activeElement.blur();
    }
}
function bindGlobalEventListeners() {
    document.addEventListener('touchstart', onDocumentTouchStart, TOUCH_OPTIONS);
    window.addEventListener('blur', onWindowBlur);
}
var isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';
var ua = isBrowser ? navigator.userAgent : '';
var isIE = /MSIE |Trident\//.test(ua);
function createMemoryLeakWarning(method) {
    var txt = method === 'destroy' ? 'n already-' : ' ';
    return [
        method + "() was called on a" + txt + "destroyed instance. This is a no-op but",
        'indicates a potential memory leak.'
    ].join(' ');
}
function clean(value) {
    var spacesAndTabs = /[ \t]{2,}/g;
    var lineStartWithSpaces = /^[ \t]*/gm;
    return value.replace(spacesAndTabs, ' ').replace(lineStartWithSpaces, '').trim();
}
function getDevMessage(message) {
    return clean("\n  %ctippy.js\n\n  %c" + clean(message) + "\n\n  %c\uD83D\uDC77\u200D This is a development-only message. It will be removed in production.\n  ");
}
function getFormattedMessage(message) {
    return [
        getDevMessage(message),
        'color: #00C584; font-size: 1.3em; font-weight: bold;',
        'line-height: 1.5',
        'color: #a6a095;'
    ];
} // Assume warnings and errors never have the same message
var visitedMessages;
resetVisitedMessages();
function resetVisitedMessages() {
    visitedMessages = new Set();
}
function warnWhen(condition, message) {
    if (condition && !visitedMessages.has(message)) {
        var _console;
        visitedMessages.add(message);
        (_console = console).warn.apply(_console, getFormattedMessage(message));
    }
}
function errorWhen(condition, message) {
    if (condition && !visitedMessages.has(message)) {
        var _console2;
        visitedMessages.add(message);
        (_console2 = console).error.apply(_console2, getFormattedMessage(message));
    }
}
function validateTargets(targets) {
    var didPassFalsyValue = !targets;
    var didPassPlainObject = Object.prototype.toString.call(targets) === '[object Object]' && !targets.addEventListener;
    errorWhen(didPassFalsyValue, [
        'tippy() was passed',
        '`' + String(targets) + '`',
        'as its targets (first) argument. Valid types are: String, Element,',
        'Element[], or NodeList.'
    ].join(' '));
    errorWhen(didPassPlainObject, [
        'tippy() was passed a plain object which is not supported as an argument',
        'for virtual positioning. Use props.getReferenceClientRect instead.'
    ].join(' '));
}
var pluginProps = {
    animateFill: false,
    followCursor: false,
    inlinePositioning: false,
    sticky: false
};
var renderProps = {
    allowHTML: false,
    animation: 'fade',
    arrow: true,
    content: '',
    inertia: false,
    maxWidth: 350,
    role: 'tooltip',
    theme: '',
    zIndex: 9999
};
var defaultProps = Object.assign({
    appendTo: function appendTo() {
        return document.body;
    },
    aria: {
        content: 'auto',
        expanded: 'auto'
    },
    delay: 0,
    duration: [
        300,
        250
    ],
    getReferenceClientRect: null,
    hideOnClick: true,
    ignoreAttributes: false,
    interactive: false,
    interactiveBorder: 2,
    interactiveDebounce: 0,
    moveTransition: '',
    offset: [
        0,
        10
    ],
    onAfterUpdate: function onAfterUpdate() {},
    onBeforeUpdate: function onBeforeUpdate() {},
    onCreate: function onCreate() {},
    onDestroy: function onDestroy() {},
    onHidden: function onHidden() {},
    onHide: function onHide() {},
    onMount: function onMount() {},
    onShow: function onShow() {},
    onShown: function onShown() {},
    onTrigger: function onTrigger() {},
    onUntrigger: function onUntrigger() {},
    onClickOutside: function onClickOutside() {},
    placement: 'top',
    plugins: [],
    popperOptions: {},
    render: null,
    showOnCreate: false,
    touch: true,
    trigger: 'mouseenter focus',
    triggerTarget: null
}, pluginProps, {}, renderProps);
var defaultKeys = Object.keys(defaultProps);
var setDefaultProps = function setDefaultProps(partialProps) {
    validateProps(partialProps, []);
    var keys = Object.keys(partialProps);
    keys.forEach(function(key) {
        defaultProps[key] = partialProps[key];
    });
};
function getExtendedPassedProps(passedProps) {
    var plugins = passedProps.plugins || [];
    var pluginProps1 = plugins.reduce(function(acc, plugin) {
        var name = plugin.name, defaultValue = plugin.defaultValue;
        if (name) acc[name] = passedProps[name] !== undefined ? passedProps[name] : defaultValue;
        return acc;
    }, {});
    return Object.assign({}, passedProps, {}, pluginProps1);
}
function getDataAttributeProps(reference, plugins) {
    var propKeys = plugins ? Object.keys(getExtendedPassedProps(Object.assign({}, defaultProps, {
        plugins: plugins
    }))) : defaultKeys;
    var props = propKeys.reduce(function(acc, key) {
        var valueAsString = (reference.getAttribute("data-tippy-" + key) || '').trim();
        if (!valueAsString) return acc;
        if (key === 'content') acc[key] = valueAsString;
        else try {
            acc[key] = JSON.parse(valueAsString);
        } catch (e) {
            acc[key] = valueAsString;
        }
        return acc;
    }, {});
    return props;
}
function evaluateProps(reference, props) {
    var out = Object.assign({}, props, {
        content: invokeWithArgsOrReturn(props.content, [
            reference
        ])
    }, props.ignoreAttributes ? {} : getDataAttributeProps(reference, props.plugins));
    out.aria = Object.assign({}, defaultProps.aria, {}, out.aria);
    out.aria = {
        expanded: out.aria.expanded === 'auto' ? props.interactive : out.aria.expanded,
        content: out.aria.content === 'auto' ? props.interactive ? null : 'describedby' : out.aria.content
    };
    return out;
}
function validateProps(partialProps, plugins) {
    if (partialProps === void 0) partialProps = {};
    if (plugins === void 0) plugins = [];
    var keys = Object.keys(partialProps);
    keys.forEach(function(prop) {
        var nonPluginProps = removeProperties(defaultProps, Object.keys(pluginProps));
        var didPassUnknownProp = !hasOwnProperty(nonPluginProps, prop); // Check if the prop exists in `plugins`
        if (didPassUnknownProp) didPassUnknownProp = plugins.filter(function(plugin) {
            return plugin.name === prop;
        }).length === 0;
        warnWhen(didPassUnknownProp, [
            "`" + prop + "`",
            "is not a valid prop. You may have spelled it incorrectly, or if it's",
            'a plugin, forgot to pass it in an array as props.plugins.',
            '\n\n',
            'All props: https://atomiks.github.io/tippyjs/v6/all-props/\n',
            'Plugins: https://atomiks.github.io/tippyjs/v6/plugins/'
        ].join(' '));
    });
}
var innerHTML = function innerHTML() {
    return 'innerHTML';
};
function dangerouslySetInnerHTML(element, html) {
    element[innerHTML()] = html;
}
function createArrowElement(value) {
    var arrow = div();
    if (value === true) arrow.className = ARROW_CLASS;
    else {
        arrow.className = SVG_ARROW_CLASS;
        if (isElement(value)) arrow.appendChild(value);
        else dangerouslySetInnerHTML(arrow, value);
    }
    return arrow;
}
function setContent1(content, props) {
    if (isElement(props.content)) {
        dangerouslySetInnerHTML(content, '');
        content.appendChild(props.content);
    } else if (typeof props.content !== 'function') {
        if (props.allowHTML) dangerouslySetInnerHTML(content, props.content);
        else content.textContent = props.content;
    }
}
function getChildren(popper) {
    var box = popper.firstElementChild;
    var boxChildren = arrayFrom(box.children);
    return {
        box: box,
        content: boxChildren.find(function(node) {
            return node.classList.contains(CONTENT_CLASS);
        }),
        arrow: boxChildren.find(function(node) {
            return node.classList.contains(ARROW_CLASS) || node.classList.contains(SVG_ARROW_CLASS);
        }),
        backdrop: boxChildren.find(function(node) {
            return node.classList.contains(BACKDROP_CLASS);
        })
    };
}
function render(instance) {
    var onUpdate = function onUpdate(prevProps, nextProps) {
        var _getChildren = getChildren(popper), box = _getChildren.box, content = _getChildren.content, arrow = _getChildren.arrow;
        if (nextProps.theme) box.setAttribute('data-theme', nextProps.theme);
        else box.removeAttribute('data-theme');
        if (typeof nextProps.animation === 'string') box.setAttribute('data-animation', nextProps.animation);
        else box.removeAttribute('data-animation');
        if (nextProps.inertia) box.setAttribute('data-inertia', '');
        else box.removeAttribute('data-inertia');
        box.style.maxWidth = typeof nextProps.maxWidth === 'number' ? nextProps.maxWidth + "px" : nextProps.maxWidth;
        if (nextProps.role) box.setAttribute('role', nextProps.role);
        else box.removeAttribute('role');
        if (prevProps.content !== nextProps.content || prevProps.allowHTML !== nextProps.allowHTML) setContent1(content, instance.props);
        if (nextProps.arrow) {
            if (!arrow) box.appendChild(createArrowElement(nextProps.arrow));
            else if (prevProps.arrow !== nextProps.arrow) {
                box.removeChild(arrow);
                box.appendChild(createArrowElement(nextProps.arrow));
            }
        } else if (arrow) box.removeChild(arrow);
    };
    var popper = div();
    var box1 = div();
    box1.className = BOX_CLASS;
    box1.setAttribute('data-state', 'hidden');
    box1.setAttribute('tabindex', '-1');
    var content1 = div();
    content1.className = CONTENT_CLASS;
    content1.setAttribute('data-state', 'hidden');
    setContent1(content1, instance.props);
    popper.appendChild(box1);
    box1.appendChild(content1);
    onUpdate(instance.props, instance.props);
    return {
        popper: popper,
        onUpdate: onUpdate
    };
} // Runtime check to identify if the render function is the default one; this
// way we can apply default CSS transitions logic and it can be tree-shaken away
render.$$tippy = true;
var idCounter = 1;
var mouseMoveListeners = []; // Used by `hideAll()`
var mountedInstances = [];
function createTippy(reference, passedProps) {
    var getNormalizedTouchSettings = // 🔒 Private methods
    // ===========================================================================
    function getNormalizedTouchSettings() {
        var touch = instance1.props.touch;
        return Array.isArray(touch) ? touch : [
            touch,
            0
        ];
    };
    var getIsCustomTouchBehavior = function getIsCustomTouchBehavior() {
        return getNormalizedTouchSettings()[0] === 'hold';
    };
    var getIsDefaultRenderFn = function getIsDefaultRenderFn() {
        var _instance$props$rende;
        // @ts-ignore
        return !!((_instance$props$rende = instance1.props.render) == null ? void 0 : _instance$props$rende.$$tippy);
    };
    var getCurrentTarget = function getCurrentTarget() {
        return currentTarget || reference;
    };
    var getDefaultTemplateChildren = function getDefaultTemplateChildren() {
        return getChildren(popper1);
    };
    var getDelay = function getDelay(isShow) {
        // For touch or keyboard input, force `0` delay for UX reasons
        // Also if the instance is mounted but not visible (transitioning out),
        // ignore delay
        if (instance1.state.isMounted && !instance1.state.isVisible || currentInput.isTouch || lastTriggerEvent && lastTriggerEvent.type === 'focus') {
            return 0;
        }
        return getValueAtIndexOrReturn(instance1.props.delay, isShow ? 0 : 1, defaultProps.delay);
    };
    var handleStyles = function handleStyles() {
        popper1.style.pointerEvents = instance1.props.interactive && instance1.state.isVisible ? '' : 'none';
        popper1.style.zIndex = "" + instance1.props.zIndex;
    };
    var invokeHook = function invokeHook(hook, args, shouldInvokePropsHook) {
        if (shouldInvokePropsHook === void 0) {
            shouldInvokePropsHook = true;
        }
        pluginsHooks.forEach(function(pluginHooks) {
            if (pluginHooks[hook]) {
                pluginHooks[hook].apply(void 0, args);
            }
        });
        if (shouldInvokePropsHook) {
            var _instance$props;
            (_instance$props = instance1.props)[hook].apply(_instance$props, args);
        }
    };
    var handleAriaContentAttribute = function handleAriaContentAttribute() {
        var aria = instance1.props.aria;
        if (!aria.content) {
            return;
        }
        var attr = "aria-" + aria.content;
        var id = popper1.id;
        var nodes = normalizeToArray(instance1.props.triggerTarget || reference);
        nodes.forEach(function(node) {
            var currentValue = node.getAttribute(attr);
            if (instance1.state.isVisible) {
                node.setAttribute(attr, currentValue ? currentValue + " " + id : id);
            } else {
                var nextValue = currentValue && currentValue.replace(id, '').trim();
                if (nextValue) {
                    node.setAttribute(attr, nextValue);
                } else {
                    node.removeAttribute(attr);
                }
            }
        });
    };
    var handleAriaExpandedAttribute = function handleAriaExpandedAttribute() {
        if (hasAriaExpanded || !instance1.props.aria.expanded) {
            return;
        }
        var nodes = normalizeToArray(instance1.props.triggerTarget || reference);
        nodes.forEach(function(node) {
            if (instance1.props.interactive) {
                node.setAttribute('aria-expanded', instance1.state.isVisible && node === getCurrentTarget() ? 'true' : 'false');
            } else {
                node.removeAttribute('aria-expanded');
            }
        });
    };
    var cleanupInteractiveMouseListeners = function cleanupInteractiveMouseListeners() {
        doc.removeEventListener('mousemove', debouncedOnMouseMove);
        mouseMoveListeners = mouseMoveListeners.filter(function(listener) {
            return listener !== debouncedOnMouseMove;
        });
    };
    var onDocumentPress = function onDocumentPress(event) {
        // Moved finger to scroll instead of an intentional tap outside
        if (currentInput.isTouch) {
            if (didTouchMove || event.type === 'mousedown') {
                return;
            }
        } // Clicked on interactive popper
        if (instance1.props.interactive && popper1.contains(event.target)) {
            return;
        } // Clicked on the event listeners target
        if (getCurrentTarget().contains(event.target)) {
            if (currentInput.isTouch) {
                return;
            }
            if (instance1.state.isVisible && instance1.props.trigger.indexOf('click') >= 0) {
                return;
            }
        } else {
            invokeHook('onClickOutside', [
                instance1,
                event
            ]);
        }
        if (instance1.props.hideOnClick === true) {
            instance1.clearDelayTimeouts();
            instance1.hide(); // `mousedown` event is fired right before `focus` if pressing the
            // currentTarget. This lets a tippy with `focus` trigger know that it
            // should not show
            didHideDueToDocumentMouseDown = true;
            setTimeout(function() {
                didHideDueToDocumentMouseDown = false;
            }); // The listener gets added in `scheduleShow()`, but this may be hiding it
            // before it shows, and hide()'s early bail-out behavior can prevent it
            // from being cleaned up
            if (!instance1.state.isMounted) {
                removeDocumentPress();
            }
        }
    };
    var onTouchMove = function onTouchMove() {
        didTouchMove = true;
    };
    var onTouchStart = function onTouchStart() {
        didTouchMove = false;
    };
    var addDocumentPress = function addDocumentPress() {
        doc.addEventListener('mousedown', onDocumentPress, true);
        doc.addEventListener('touchend', onDocumentPress, TOUCH_OPTIONS);
        doc.addEventListener('touchstart', onTouchStart, TOUCH_OPTIONS);
        doc.addEventListener('touchmove', onTouchMove, TOUCH_OPTIONS);
    };
    var removeDocumentPress = function removeDocumentPress() {
        doc.removeEventListener('mousedown', onDocumentPress, true);
        doc.removeEventListener('touchend', onDocumentPress, TOUCH_OPTIONS);
        doc.removeEventListener('touchstart', onTouchStart, TOUCH_OPTIONS);
        doc.removeEventListener('touchmove', onTouchMove, TOUCH_OPTIONS);
    };
    var onTransitionedOut = function onTransitionedOut(duration, callback) {
        onTransitionEnd(duration, function() {
            if (!instance1.state.isVisible && popper1.parentNode && popper1.parentNode.contains(popper1)) {
                callback();
            }
        });
    };
    var onTransitionedIn = function onTransitionedIn(duration, callback) {
        onTransitionEnd(duration, callback);
    };
    var onTransitionEnd = function onTransitionEnd(duration, callback) {
        var box = getDefaultTemplateChildren().box;
        function listener(event) {
            if (event.target === box) {
                updateTransitionEndListener(box, 'remove', listener);
                callback();
            }
        } // Make callback synchronous if duration is 0
        // `transitionend` won't fire otherwise
        if (duration === 0) {
            return callback();
        }
        updateTransitionEndListener(box, 'remove', currentTransitionEndListener);
        updateTransitionEndListener(box, 'add', listener);
        currentTransitionEndListener = listener;
    };
    var on = function on(eventType, handler, options) {
        if (options === void 0) {
            options = false;
        }
        var nodes = normalizeToArray(instance1.props.triggerTarget || reference);
        nodes.forEach(function(node) {
            node.addEventListener(eventType, handler, options);
            listeners.push({
                node: node,
                eventType: eventType,
                handler: handler,
                options: options
            });
        });
    };
    var addListeners = function addListeners() {
        if (getIsCustomTouchBehavior()) {
            on('touchstart', onTrigger, {
                passive: true
            });
            on('touchend', onMouseLeave, {
                passive: true
            });
        }
        splitBySpaces(instance1.props.trigger).forEach(function(eventType) {
            if (eventType === 'manual') {
                return;
            }
            on(eventType, onTrigger);
            switch(eventType){
                case 'mouseenter':
                    on('mouseleave', onMouseLeave);
                    break;
                case 'focus':
                    on(isIE ? 'focusout' : 'blur', onBlurOrFocusOut);
                    break;
                case 'focusin':
                    on('focusout', onBlurOrFocusOut);
                    break;
            }
        });
    };
    var removeListeners = function removeListeners() {
        listeners.forEach(function(_ref) {
            var node = _ref.node, eventType = _ref.eventType, handler = _ref.handler, options = _ref.options;
            node.removeEventListener(eventType, handler, options);
        });
        listeners = [];
    };
    var onTrigger = function onTrigger(event) {
        var _lastTriggerEvent;
        var shouldScheduleClickHide = false;
        if (!instance1.state.isEnabled || isEventListenerStopped(event) || didHideDueToDocumentMouseDown) {
            return;
        }
        var wasFocused = ((_lastTriggerEvent = lastTriggerEvent) == null ? void 0 : _lastTriggerEvent.type) === 'focus';
        lastTriggerEvent = event;
        currentTarget = event.currentTarget;
        handleAriaExpandedAttribute();
        if (!instance1.state.isVisible && isMouseEvent(event)) {
            // If scrolling, `mouseenter` events can be fired if the cursor lands
            // over a new target, but `mousemove` events don't get fired. This
            // causes interactive tooltips to get stuck open until the cursor is
            // moved
            mouseMoveListeners.forEach(function(listener) {
                return listener(event);
            });
        } // Toggle show/hide when clicking click-triggered tooltips
        if (event.type === 'click' && (instance1.props.trigger.indexOf('mouseenter') < 0 || isVisibleFromClick) && instance1.props.hideOnClick !== false && instance1.state.isVisible) {
            shouldScheduleClickHide = true;
        } else {
            scheduleShow(event);
        }
        if (event.type === 'click') {
            isVisibleFromClick = !shouldScheduleClickHide;
        }
        if (shouldScheduleClickHide && !wasFocused) {
            scheduleHide(event);
        }
    };
    var onMouseMove = function onMouseMove(event) {
        var target = event.target;
        var isCursorOverReferenceOrPopper = getCurrentTarget().contains(target) || popper1.contains(target);
        if (event.type === 'mousemove' && isCursorOverReferenceOrPopper) {
            return;
        }
        var popperTreeData = getNestedPopperTree().concat(popper1).map(function(popper) {
            var _instance$popperInsta;
            var instance = popper._tippy;
            var state = (_instance$popperInsta = instance.popperInstance) == null ? void 0 : _instance$popperInsta.state;
            if (state) {
                return {
                    popperRect: popper.getBoundingClientRect(),
                    popperState: state,
                    props: props
                };
            }
            return null;
        }).filter(Boolean);
        if (isCursorOutsideInteractiveBorder(popperTreeData, event)) {
            cleanupInteractiveMouseListeners();
            scheduleHide(event);
        }
    };
    var onMouseLeave = function onMouseLeave(event) {
        var shouldBail = isEventListenerStopped(event) || instance1.props.trigger.indexOf('click') >= 0 && isVisibleFromClick;
        if (shouldBail) {
            return;
        }
        if (instance1.props.interactive) {
            instance1.hideWithInteractivity(event);
            return;
        }
        scheduleHide(event);
    };
    var onBlurOrFocusOut = function onBlurOrFocusOut(event) {
        if (instance1.props.trigger.indexOf('focusin') < 0 && event.target !== getCurrentTarget()) {
            return;
        } // If focus was moved to within the popper
        if (instance1.props.interactive && event.relatedTarget && popper1.contains(event.relatedTarget)) {
            return;
        }
        scheduleHide(event);
    };
    var isEventListenerStopped = function isEventListenerStopped(event) {
        return currentInput.isTouch ? getIsCustomTouchBehavior() !== event.type.indexOf('touch') >= 0 : false;
    };
    var createPopperInstance = function createPopperInstance() {
        destroyPopperInstance();
        var _instance$props2 = instance1.props, popperOptions = _instance$props2.popperOptions, placement = _instance$props2.placement, offset = _instance$props2.offset, getReferenceClientRect = _instance$props2.getReferenceClientRect, moveTransition = _instance$props2.moveTransition;
        var arrow = getIsDefaultRenderFn() ? getChildren(popper1).arrow : null;
        var computedReference = getReferenceClientRect ? {
            getBoundingClientRect: getReferenceClientRect,
            contextElement: getReferenceClientRect.contextElement || getCurrentTarget()
        } : reference;
        var tippyModifier = {
            name: '$$tippy',
            enabled: true,
            phase: 'beforeWrite',
            requires: [
                'computeStyles'
            ],
            fn: function fn(_ref2) {
                var state = _ref2.state;
                if (getIsDefaultRenderFn()) {
                    var _getDefaultTemplateCh = getDefaultTemplateChildren(), box = _getDefaultTemplateCh.box;
                    [
                        'placement',
                        'reference-hidden',
                        'escaped'
                    ].forEach(function(attr) {
                        if (attr === 'placement') {
                            box.setAttribute('data-placement', state.placement);
                        } else {
                            if (state.attributes.popper["data-popper-" + attr]) {
                                box.setAttribute("data-" + attr, '');
                            } else {
                                box.removeAttribute("data-" + attr);
                            }
                        }
                    });
                    state.attributes.popper = {};
                }
            }
        };
        var modifiers = [
            {
                name: 'offset',
                options: {
                    offset: offset
                }
            },
            {
                name: 'preventOverflow',
                options: {
                    padding: {
                        top: 2,
                        bottom: 2,
                        left: 5,
                        right: 5
                    }
                }
            },
            {
                name: 'flip',
                options: {
                    padding: 5
                }
            },
            {
                name: 'computeStyles',
                options: {
                    adaptive: !moveTransition
                }
            },
            tippyModifier
        ];
        if (getIsDefaultRenderFn() && arrow) {
            modifiers.push({
                name: 'arrow',
                options: {
                    element: arrow,
                    padding: 3
                }
            });
        }
        modifiers.push.apply(modifiers, (popperOptions == null ? void 0 : popperOptions.modifiers) || []);
        instance1.popperInstance = _core.createPopper(computedReference, popper1, Object.assign({}, popperOptions, {
            placement: placement,
            onFirstUpdate: onFirstUpdate,
            modifiers: modifiers
        }));
    };
    var destroyPopperInstance = function destroyPopperInstance() {
        if (instance1.popperInstance) {
            instance1.popperInstance.destroy();
            instance1.popperInstance = null;
        }
    };
    var mount = function mount() {
        var appendTo = instance1.props.appendTo;
        var parentNode; // By default, we'll append the popper to the triggerTargets's parentNode so
        // it's directly after the reference element so the elements inside the
        // tippy can be tabbed to
        // If there are clipping issues, the user can specify a different appendTo
        // and ensure focus management is handled correctly manually
        var node = getCurrentTarget();
        if (instance1.props.interactive && appendTo === defaultProps.appendTo || appendTo === 'parent') {
            parentNode = node.parentNode;
        } else {
            parentNode = invokeWithArgsOrReturn(appendTo, [
                node
            ]);
        } // The popper element needs to exist on the DOM before its position can be
        // updated as Popper needs to read its dimensions
        if (!parentNode.contains(popper1)) {
            parentNode.appendChild(popper1);
        }
        createPopperInstance();
        /* istanbul ignore else */ if (true) {
            // Accessibility check
            warnWhen(instance1.props.interactive && appendTo === defaultProps.appendTo && node.nextElementSibling !== popper1, [
                'Interactive tippy element may not be accessible via keyboard',
                'navigation because it is not directly after the reference element',
                'in the DOM source order.',
                '\n\n',
                'Using a wrapper <div> or <span> tag around the reference element',
                'solves this by creating a new parentNode context.',
                '\n\n',
                'Specifying `appendTo: document.body` silences this warning, but it',
                'assumes you are using a focus management solution to handle',
                'keyboard navigation.',
                '\n\n',
                'See: https://atomiks.github.io/tippyjs/v6/accessibility/#interactivity'
            ].join(' '));
        }
    };
    var getNestedPopperTree = function getNestedPopperTree() {
        return arrayFrom(popper1.querySelectorAll('[data-tippy-root]'));
    };
    var scheduleShow = function scheduleShow(event) {
        instance1.clearDelayTimeouts();
        if (event) {
            invokeHook('onTrigger', [
                instance1,
                event
            ]);
        }
        addDocumentPress();
        var delay = getDelay(true);
        var _getNormalizedTouchSe = getNormalizedTouchSettings(), touchValue = _getNormalizedTouchSe[0], touchDelay = _getNormalizedTouchSe[1];
        if (currentInput.isTouch && touchValue === 'hold' && touchDelay) {
            delay = touchDelay;
        }
        if (delay) {
            showTimeout = setTimeout(function() {
                instance1.show();
            }, delay);
        } else {
            instance1.show();
        }
    };
    var scheduleHide = function scheduleHide(event) {
        instance1.clearDelayTimeouts();
        invokeHook('onUntrigger', [
            instance1,
            event
        ]);
        if (!instance1.state.isVisible) {
            removeDocumentPress();
            return;
        } // For interactive tippies, scheduleHide is added to a document.body handler
        // from onMouseLeave so must intercept scheduled hides from mousemove/leave
        // events when trigger contains mouseenter and click, and the tip is
        // currently shown as a result of a click.
        if (instance1.props.trigger.indexOf('mouseenter') >= 0 && instance1.props.trigger.indexOf('click') >= 0 && [
            'mouseleave',
            'mousemove'
        ].indexOf(event.type) >= 0 && isVisibleFromClick) {
            return;
        }
        var delay = getDelay(false);
        if (delay) {
            hideTimeout = setTimeout(function() {
                if (instance1.state.isVisible) {
                    instance1.hide();
                }
            }, delay);
        } else {
            // Fixes a `transitionend` problem when it fires 1 frame too
            // late sometimes, we don't want hide() to be called.
            scheduleHideAnimationFrame = requestAnimationFrame(function() {
                instance1.hide();
            });
        }
    } // ===========================================================================
    ;
    var enable = // 🔑 Public methods
    // ===========================================================================
    function enable() {
        instance1.state.isEnabled = true;
    };
    var disable = function disable() {
        // Disabling the instance should also hide it
        // https://github.com/atomiks/tippy.js-react/issues/106
        instance1.hide();
        instance1.state.isEnabled = false;
    };
    var clearDelayTimeouts = function clearDelayTimeouts() {
        clearTimeout(showTimeout);
        clearTimeout(hideTimeout);
        cancelAnimationFrame(scheduleHideAnimationFrame);
    };
    var setProps = function setProps(partialProps) {
        /* istanbul ignore else */ if (true) {
            warnWhen(instance1.state.isDestroyed, createMemoryLeakWarning('setProps'));
        }
        if (instance1.state.isDestroyed) {
            return;
        }
        invokeHook('onBeforeUpdate', [
            instance1,
            partialProps
        ]);
        removeListeners();
        var prevProps = instance1.props;
        var nextProps = evaluateProps(reference, Object.assign({}, instance1.props, {}, partialProps, {
            ignoreAttributes: true
        }));
        instance1.props = nextProps;
        addListeners();
        if (prevProps.interactiveDebounce !== nextProps.interactiveDebounce) {
            cleanupInteractiveMouseListeners();
            debouncedOnMouseMove = debounce(onMouseMove, nextProps.interactiveDebounce);
        } // Ensure stale aria-expanded attributes are removed
        if (prevProps.triggerTarget && !nextProps.triggerTarget) {
            normalizeToArray(prevProps.triggerTarget).forEach(function(node) {
                node.removeAttribute('aria-expanded');
            });
        } else if (nextProps.triggerTarget) {
            reference.removeAttribute('aria-expanded');
        }
        handleAriaExpandedAttribute();
        handleStyles();
        if (onUpdate) {
            onUpdate(prevProps, nextProps);
        }
        if (instance1.popperInstance) {
            createPopperInstance(); // Fixes an issue with nested tippies if they are all getting re-rendered,
            // and the nested ones get re-rendered first.
            // https://github.com/atomiks/tippyjs-react/issues/177
            // TODO: find a cleaner / more efficient solution(!)
            getNestedPopperTree().forEach(function(nestedPopper) {
                // React (and other UI libs likely) requires a rAF wrapper as it flushes
                // its work in one
                requestAnimationFrame(nestedPopper._tippy.popperInstance.forceUpdate);
            });
        }
        invokeHook('onAfterUpdate', [
            instance1,
            partialProps
        ]);
    };
    var setContent = function setContent(content) {
        instance1.setProps({
            content: content
        });
    };
    var show = function show() {
        /* istanbul ignore else */ if (true) {
            warnWhen(instance1.state.isDestroyed, createMemoryLeakWarning('show'));
        } // Early bail-out
        var isAlreadyVisible = instance1.state.isVisible;
        var isDestroyed = instance1.state.isDestroyed;
        var isDisabled = !instance1.state.isEnabled;
        var isTouchAndTouchDisabled = currentInput.isTouch && !instance1.props.touch;
        var duration = getValueAtIndexOrReturn(instance1.props.duration, 0, defaultProps.duration);
        if (isAlreadyVisible || isDestroyed || isDisabled || isTouchAndTouchDisabled) {
            return;
        } // Normalize `disabled` behavior across browsers.
        // Firefox allows events on disabled elements, but Chrome doesn't.
        // Using a wrapper element (i.e. <span>) is recommended.
        if (getCurrentTarget().hasAttribute('disabled')) {
            return;
        }
        invokeHook('onShow', [
            instance1
        ], false);
        if (instance1.props.onShow(instance1) === false) {
            return;
        }
        instance1.state.isVisible = true;
        if (getIsDefaultRenderFn()) {
            popper1.style.visibility = 'visible';
        }
        handleStyles();
        addDocumentPress();
        if (!instance1.state.isMounted) {
            popper1.style.transition = 'none';
        } // If flipping to the opposite side after hiding at least once, the
        // animation will use the wrong placement without resetting the duration
        if (getIsDefaultRenderFn()) {
            var _getDefaultTemplateCh2 = getDefaultTemplateChildren(), box = _getDefaultTemplateCh2.box, content = _getDefaultTemplateCh2.content;
            setTransitionDuration([
                box,
                content
            ], 0);
        }
        onFirstUpdate = function onFirstUpdate() {
            if (!instance1.state.isVisible || ignoreOnFirstUpdate) {
                return;
            }
            ignoreOnFirstUpdate = true; // reflow
            void popper1.offsetHeight;
            popper1.style.transition = instance1.props.moveTransition;
            if (getIsDefaultRenderFn() && instance1.props.animation) {
                var _getDefaultTemplateCh3 = getDefaultTemplateChildren(), _box = _getDefaultTemplateCh3.box, _content = _getDefaultTemplateCh3.content;
                setTransitionDuration([
                    _box,
                    _content
                ], duration);
                setVisibilityState([
                    _box,
                    _content
                ], 'visible');
            }
            handleAriaContentAttribute();
            handleAriaExpandedAttribute();
            pushIfUnique(mountedInstances, instance1);
            instance1.state.isMounted = true;
            invokeHook('onMount', [
                instance1
            ]);
            if (instance1.props.animation && getIsDefaultRenderFn()) {
                onTransitionedIn(duration, function() {
                    instance1.state.isShown = true;
                    invokeHook('onShown', [
                        instance1
                    ]);
                });
            }
        };
        mount();
    };
    var hide = function hide() {
        /* istanbul ignore else */ if (true) {
            warnWhen(instance1.state.isDestroyed, createMemoryLeakWarning('hide'));
        } // Early bail-out
        var isAlreadyHidden = !instance1.state.isVisible;
        var isDestroyed = instance1.state.isDestroyed;
        var isDisabled = !instance1.state.isEnabled;
        var duration = getValueAtIndexOrReturn(instance1.props.duration, 1, defaultProps.duration);
        if (isAlreadyHidden || isDestroyed || isDisabled) {
            return;
        }
        invokeHook('onHide', [
            instance1
        ], false);
        if (instance1.props.onHide(instance1) === false) {
            return;
        }
        instance1.state.isVisible = false;
        instance1.state.isShown = false;
        ignoreOnFirstUpdate = false;
        isVisibleFromClick = false;
        if (getIsDefaultRenderFn()) {
            popper1.style.visibility = 'hidden';
        }
        cleanupInteractiveMouseListeners();
        removeDocumentPress();
        handleStyles();
        if (getIsDefaultRenderFn()) {
            var _getDefaultTemplateCh4 = getDefaultTemplateChildren(), box = _getDefaultTemplateCh4.box, content = _getDefaultTemplateCh4.content;
            if (instance1.props.animation) {
                setTransitionDuration([
                    box,
                    content
                ], duration);
                setVisibilityState([
                    box,
                    content
                ], 'hidden');
            }
        }
        handleAriaContentAttribute();
        handleAriaExpandedAttribute();
        if (instance1.props.animation) {
            if (getIsDefaultRenderFn()) {
                onTransitionedOut(duration, instance1.unmount);
            }
        } else {
            instance1.unmount();
        }
    };
    var hideWithInteractivity = function hideWithInteractivity(event) {
        /* istanbul ignore else */ if (true) {
            warnWhen(instance1.state.isDestroyed, createMemoryLeakWarning('hideWithInteractivity'));
        }
        doc.addEventListener('mousemove', debouncedOnMouseMove);
        pushIfUnique(mouseMoveListeners, debouncedOnMouseMove);
        debouncedOnMouseMove(event);
    };
    var unmount = function unmount() {
        /* istanbul ignore else */ if (true) {
            warnWhen(instance1.state.isDestroyed, createMemoryLeakWarning('unmount'));
        }
        if (instance1.state.isVisible) {
            instance1.hide();
        }
        if (!instance1.state.isMounted) {
            return;
        }
        destroyPopperInstance(); // If a popper is not interactive, it will be appended outside the popper
        // tree by default. This seems mainly for interactive tippies, but we should
        // find a workaround if possible
        getNestedPopperTree().forEach(function(nestedPopper) {
            nestedPopper._tippy.unmount();
        });
        if (popper1.parentNode) {
            popper1.parentNode.removeChild(popper1);
        }
        mountedInstances = mountedInstances.filter(function(i) {
            return i !== instance1;
        });
        instance1.state.isMounted = false;
        invokeHook('onHidden', [
            instance1
        ]);
    };
    var destroy = function destroy() {
        /* istanbul ignore else */ if (true) {
            warnWhen(instance1.state.isDestroyed, createMemoryLeakWarning('destroy'));
        }
        if (instance1.state.isDestroyed) {
            return;
        }
        instance1.clearDelayTimeouts();
        instance1.unmount();
        removeListeners();
        delete reference._tippy;
        instance1.state.isDestroyed = true;
        invokeHook('onDestroy', [
            instance1
        ]);
    };
    var props = evaluateProps(reference, Object.assign({}, defaultProps, {}, getExtendedPassedProps(removeUndefinedProps(passedProps)))); // ===========================================================================
    // 🔒 Private members
    // ===========================================================================
    var showTimeout;
    var hideTimeout;
    var scheduleHideAnimationFrame;
    var isVisibleFromClick = false;
    var didHideDueToDocumentMouseDown = false;
    var didTouchMove = false;
    var ignoreOnFirstUpdate = false;
    var lastTriggerEvent;
    var currentTransitionEndListener;
    var onFirstUpdate;
    var listeners = [];
    var debouncedOnMouseMove = debounce(onMouseMove, props.interactiveDebounce);
    var currentTarget;
    var doc = getOwnerDocument(props.triggerTarget || reference); // ===========================================================================
    // 🔑 Public members
    // ===========================================================================
    var id1 = idCounter++;
    var popperInstance = null;
    var plugins = unique(props.plugins);
    var state1 = {
        // Is the instance currently enabled?
        isEnabled: true,
        // Is the tippy currently showing and not transitioning out?
        isVisible: false,
        // Has the instance been destroyed?
        isDestroyed: false,
        // Is the tippy currently mounted to the DOM?
        isMounted: false,
        // Has the tippy finished transitioning in?
        isShown: false
    };
    var instance1 = {
        // properties
        id: id1,
        reference: reference,
        popper: div(),
        popperInstance: popperInstance,
        props: props,
        state: state1,
        plugins: plugins,
        // methods
        clearDelayTimeouts: clearDelayTimeouts,
        setProps: setProps,
        setContent: setContent,
        show: show,
        hide: hide,
        hideWithInteractivity: hideWithInteractivity,
        enable: enable,
        disable: disable,
        unmount: unmount,
        destroy: destroy
    }; // TODO: Investigate why this early return causes a TDZ error in the tests —
    // it doesn't seem to happen in the browser
    /* istanbul ignore if */ if (!props.render) {
        errorWhen(true, 'render() function has not been supplied.');
        return instance1;
    } // ===========================================================================
    // Initial mutations
    // ===========================================================================
    var _props$render = props.render(instance1), popper1 = _props$render.popper, onUpdate = _props$render.onUpdate;
    popper1.setAttribute('data-tippy-root', '');
    popper1.id = "tippy-" + instance1.id;
    instance1.popper = popper1;
    reference._tippy = instance1;
    popper1._tippy = instance1;
    var pluginsHooks = plugins.map(function(plugin) {
        return plugin.fn(instance1);
    });
    var hasAriaExpanded = reference.hasAttribute('aria-expanded');
    addListeners();
    handleAriaExpandedAttribute();
    handleStyles();
    invokeHook('onCreate', [
        instance1
    ]);
    if (props.showOnCreate) scheduleShow();
     // Prevent a tippy with a delay from hiding if the cursor left then returned
    // before it started hiding
    popper1.addEventListener('mouseenter', function() {
        if (instance1.props.interactive && instance1.state.isVisible) instance1.clearDelayTimeouts();
    });
    popper1.addEventListener('mouseleave', function(event) {
        if (instance1.props.interactive && instance1.props.trigger.indexOf('mouseenter') >= 0) {
            doc.addEventListener('mousemove', debouncedOnMouseMove);
            debouncedOnMouseMove(event);
        }
    });
    return instance1; // ===========================================================================
}
function tippy(targets, optionalProps) {
    if (optionalProps === void 0) optionalProps = {};
    var plugins = defaultProps.plugins.concat(optionalProps.plugins || []);
    validateTargets(targets);
    validateProps(optionalProps, plugins);
    bindGlobalEventListeners();
    var passedProps = Object.assign({}, optionalProps, {
        plugins: plugins
    });
    var elements = getArrayOfElements(targets);
    var isSingleContentElement = isElement(passedProps.content);
    var isMoreThanOneReferenceElement = elements.length > 1;
    warnWhen(isSingleContentElement && isMoreThanOneReferenceElement, [
        'tippy() was passed an Element as the `content` prop, but more than',
        'one tippy instance was created by this invocation. This means the',
        'content element will only be appended to the last tippy instance.',
        '\n\n',
        'Instead, pass the .innerHTML of the element, or use a function that',
        'returns a cloned version of the element instead.',
        '\n\n',
        '1) content: element.innerHTML\n',
        '2) content: () => element.cloneNode(true)'
    ].join(' '));
    var instances = elements.reduce(function(acc, reference) {
        var instance = reference && createTippy(reference, passedProps);
        if (instance) acc.push(instance);
        return acc;
    }, []);
    return isElement(targets) ? instances[0] : instances;
}
tippy.defaultProps = defaultProps;
tippy.setDefaultProps = setDefaultProps;
tippy.currentInput = currentInput;
var hideAll = function hideAll(_temp) {
    var _ref = _temp === void 0 ? {} : _temp, excludedReferenceOrInstance = _ref.exclude, duration = _ref.duration;
    mountedInstances.forEach(function(instance) {
        var isExcluded = false;
        if (excludedReferenceOrInstance) isExcluded = isReferenceElement(excludedReferenceOrInstance) ? instance.reference === excludedReferenceOrInstance : instance.popper === excludedReferenceOrInstance.popper;
        if (!isExcluded) {
            var originalDuration = instance.props.duration;
            instance.setProps({
                duration: duration
            });
            instance.hide();
            if (!instance.state.isDestroyed) instance.setProps({
                duration: originalDuration
            });
        }
    });
};
var createSingleton = function createSingleton(tippyInstances, optionalProps) {
    var setReferences = function setReferences() {
        references = mutTippyInstances.map(function(instance) {
            return instance.reference;
        });
    };
    var enableInstances = function enableInstances(isEnabled) {
        mutTippyInstances.forEach(function(instance) {
            if (isEnabled) instance.enable();
            else instance.disable();
        });
    };
    if (optionalProps === void 0) optionalProps = {};
    errorWhen(!Array.isArray(tippyInstances), [
        'The first argument passed to createSingleton() must be an array of',
        'tippy instances. The passed value was',
        String(tippyInstances)
    ].join(' '));
    var mutTippyInstances = tippyInstances;
    var references = [];
    var currentTarget;
    var overrides = optionalProps.overrides;
    enableInstances(false);
    setReferences();
    var singleton = {
        fn: function fn() {
            return {
                onDestroy: function onDestroy() {
                    enableInstances(true);
                },
                onTrigger: function onTrigger(instance, event) {
                    var target = event.currentTarget;
                    var index = references.indexOf(target); // bail-out
                    if (target === currentTarget) return;
                    currentTarget = target;
                    var overrideProps = (overrides || []).concat('content').reduce(function(acc, prop) {
                        acc[prop] = mutTippyInstances[index].props[prop];
                        return acc;
                    }, {});
                    instance.setProps(Object.assign({}, overrideProps, {
                        getReferenceClientRect: function getReferenceClientRect() {
                            return target.getBoundingClientRect();
                        }
                    }));
                }
            };
        }
    };
    var instance2 = tippy(div(), Object.assign({}, removeProperties(optionalProps, [
        'overrides'
    ]), {
        plugins: [
            singleton
        ].concat(optionalProps.plugins || []),
        triggerTarget: references
    }));
    var originalSetProps = instance2.setProps;
    instance2.setProps = function(props) {
        overrides = props.overrides || overrides;
        originalSetProps(props);
    };
    instance2.setInstances = function(nextInstances) {
        enableInstances(true);
        mutTippyInstances = nextInstances;
        enableInstances(false);
        setReferences();
        instance2.setProps({
            triggerTarget: references
        });
    };
    return instance2;
};
var BUBBLING_EVENTS_MAP = {
    mouseover: 'mouseenter',
    focusin: 'focus',
    click: 'click'
};
/**
 * Creates a delegate instance that controls the creation of tippy instances
 * for child elements (`target` CSS selector).
 */ function delegate(targets, props) {
    var onTrigger = function onTrigger(event) {
        if (!event.target) return;
        var targetNode = event.target.closest(target);
        if (!targetNode) return;
         // Get relevant trigger with fallbacks:
        // 1. Check `data-tippy-trigger` attribute on target node
        // 2. Fallback to `trigger` passed to `delegate()`
        // 3. Fallback to `defaultProps.trigger`
        var trigger = targetNode.getAttribute('data-tippy-trigger') || props.trigger || defaultProps.trigger; // @ts-ignore
        if (targetNode._tippy) return;
        if (event.type === 'touchstart' && typeof childProps.touch === 'boolean') return;
        if (event.type !== 'touchstart' && trigger.indexOf(BUBBLING_EVENTS_MAP[event.type]) < 0) return;
        var instance = tippy(targetNode, childProps);
        if (instance) childTippyInstances = childTippyInstances.concat(instance);
    };
    var on = function on(node, eventType, handler, options) {
        if (options === void 0) options = false;
        node.addEventListener(eventType, handler, options);
        listeners.push({
            node: node,
            eventType: eventType,
            handler: handler,
            options: options
        });
    };
    var addEventListeners = function addEventListeners(instance) {
        var reference = instance.reference;
        on(reference, 'touchstart', onTrigger);
        on(reference, 'mouseover', onTrigger);
        on(reference, 'focusin', onTrigger);
        on(reference, 'click', onTrigger);
    };
    var removeEventListeners = function removeEventListeners() {
        listeners.forEach(function(_ref) {
            var node = _ref.node, eventType = _ref.eventType, handler = _ref.handler, options = _ref.options;
            node.removeEventListener(eventType, handler, options);
        });
        listeners = [];
    };
    var applyMutations = function applyMutations(instance3) {
        var originalDestroy = instance3.destroy;
        instance3.destroy = function(shouldDestroyChildInstances) {
            if (shouldDestroyChildInstances === void 0) shouldDestroyChildInstances = true;
            if (shouldDestroyChildInstances) childTippyInstances.forEach(function(instance) {
                instance.destroy();
            });
            childTippyInstances = [];
            removeEventListeners();
            originalDestroy();
        };
        addEventListeners(instance3);
    };
    errorWhen(!(props && props.target), [
        'You must specity a `target` prop indicating a CSS selector string matching',
        'the target elements that should receive a tippy.'
    ].join(' '));
    var listeners = [];
    var childTippyInstances = [];
    var target = props.target;
    var nativeProps = removeProperties(props, [
        'target'
    ]);
    var parentProps = Object.assign({}, nativeProps, {
        trigger: 'manual',
        touch: false
    });
    var childProps = Object.assign({}, nativeProps, {
        showOnCreate: true
    });
    var returnValue = tippy(targets, parentProps);
    var normalizedReturnValue = normalizeToArray(returnValue);
    normalizedReturnValue.forEach(applyMutations);
    return returnValue;
}
var animateFill = {
    name: 'animateFill',
    defaultValue: false,
    fn: function fn(instance) {
        var _instance$props$rende;
        // @ts-ignore
        if (!((_instance$props$rende = instance.props.render) == null ? void 0 : _instance$props$rende.$$tippy)) {
            errorWhen(instance.props.animateFill, 'The `animateFill` plugin requires the default render function.');
            return {};
        }
        var _getChildren = getChildren(instance.popper), box = _getChildren.box, content = _getChildren.content;
        var backdrop = instance.props.animateFill ? createBackdropElement() : null;
        return {
            onCreate: function onCreate() {
                if (backdrop) {
                    box.insertBefore(backdrop, box.firstElementChild);
                    box.setAttribute('data-animatefill', '');
                    box.style.overflow = 'hidden';
                    instance.setProps({
                        arrow: false,
                        animation: 'shift-away'
                    });
                }
            },
            onMount: function onMount() {
                if (backdrop) {
                    var transitionDuration = box.style.transitionDuration;
                    var duration = Number(transitionDuration.replace('ms', '')); // The content should fade in after the backdrop has mostly filled the
                    // tooltip element. `clip-path` is the other alternative but is not
                    // well-supported and is buggy on some devices.
                    content.style.transitionDelay = Math.round(duration / 10) + "ms";
                    backdrop.style.transitionDuration = transitionDuration;
                    setVisibilityState([
                        backdrop
                    ], 'visible');
                }
            },
            onShow: function onShow() {
                if (backdrop) backdrop.style.transitionDuration = '0ms';
            },
            onHide: function onHide() {
                if (backdrop) setVisibilityState([
                    backdrop
                ], 'hidden');
            }
        };
    }
};
function createBackdropElement() {
    var backdrop = div();
    backdrop.className = BACKDROP_CLASS;
    setVisibilityState([
        backdrop
    ], 'hidden');
    return backdrop;
}
var mouseCoords = {
    clientX: 0,
    clientY: 0
};
var activeInstances = [];
function storeMouseCoords(_ref) {
    var clientX = _ref.clientX, clientY = _ref.clientY;
    mouseCoords = {
        clientX: clientX,
        clientY: clientY
    };
}
function addMouseCoordsListener(doc) {
    doc.addEventListener('mousemove', storeMouseCoords);
}
function removeMouseCoordsListener(doc) {
    doc.removeEventListener('mousemove', storeMouseCoords);
}
var followCursor = {
    name: 'followCursor',
    defaultValue: false,
    fn: function fn(instance) {
        var getIsInitialBehavior = function getIsInitialBehavior() {
            return instance.props.followCursor === 'initial' && instance.state.isVisible;
        };
        var addListener = function addListener() {
            doc.addEventListener('mousemove', onMouseMove);
        };
        var removeListener = function removeListener() {
            doc.removeEventListener('mousemove', onMouseMove);
        };
        var unsetGetReferenceClientRect = function unsetGetReferenceClientRect() {
            isInternalUpdate = true;
            instance.setProps({
                getReferenceClientRect: null
            });
            isInternalUpdate = false;
        };
        var onMouseMove = function onMouseMove(event) {
            // If the instance is interactive, avoid updating the position unless it's
            // over the reference element
            var isCursorOverReference = event.target ? reference.contains(event.target) : true;
            var followCursor1 = instance.props.followCursor;
            var clientX = event.clientX, clientY = event.clientY;
            var rect1 = reference.getBoundingClientRect();
            var relativeX = clientX - rect1.left;
            var relativeY = clientY - rect1.top;
            if (isCursorOverReference || !instance.props.interactive) instance.setProps({
                getReferenceClientRect: function getReferenceClientRect() {
                    var rect = reference.getBoundingClientRect();
                    var x = clientX;
                    var y = clientY;
                    if (followCursor1 === 'initial') {
                        x = rect.left + relativeX;
                        y = rect.top + relativeY;
                    }
                    var top = followCursor1 === 'horizontal' ? rect.top : y;
                    var right = followCursor1 === 'vertical' ? rect.right : x;
                    var bottom = followCursor1 === 'horizontal' ? rect.bottom : y;
                    var left = followCursor1 === 'vertical' ? rect.left : x;
                    return {
                        width: right - left,
                        height: bottom - top,
                        top: top,
                        right: right,
                        bottom: bottom,
                        left: left
                    };
                }
            });
        };
        var create = function create() {
            if (instance.props.followCursor) {
                activeInstances.push({
                    instance: instance,
                    doc: doc
                });
                addMouseCoordsListener(doc);
            }
        };
        var destroy = function destroy() {
            activeInstances = activeInstances.filter(function(data) {
                return data.instance !== instance;
            });
            if (activeInstances.filter(function(data) {
                return data.doc === doc;
            }).length === 0) removeMouseCoordsListener(doc);
        };
        var reference = instance.reference;
        var doc = getOwnerDocument(instance.props.triggerTarget || reference);
        var isInternalUpdate = false;
        var wasFocusEvent = false;
        var isUnmounted = true;
        var prevProps = instance.props;
        return {
            onCreate: create,
            onDestroy: destroy,
            onBeforeUpdate: function onBeforeUpdate() {
                prevProps = instance.props;
            },
            onAfterUpdate: function onAfterUpdate(_, _ref2) {
                var followCursor2 = _ref2.followCursor;
                if (isInternalUpdate) return;
                if (followCursor2 !== undefined && prevProps.followCursor !== followCursor2) {
                    destroy();
                    if (followCursor2) {
                        create();
                        if (instance.state.isMounted && !wasFocusEvent && !getIsInitialBehavior()) addListener();
                    } else {
                        removeListener();
                        unsetGetReferenceClientRect();
                    }
                }
            },
            onMount: function onMount() {
                if (instance.props.followCursor && !wasFocusEvent) {
                    if (isUnmounted) {
                        onMouseMove(mouseCoords);
                        isUnmounted = false;
                    }
                    if (!getIsInitialBehavior()) addListener();
                }
            },
            onTrigger: function onTrigger(_, event) {
                if (isMouseEvent(event)) mouseCoords = {
                    clientX: event.clientX,
                    clientY: event.clientY
                };
                wasFocusEvent = event.type === 'focus';
            },
            onHidden: function onHidden() {
                if (instance.props.followCursor) {
                    unsetGetReferenceClientRect();
                    removeListener();
                    isUnmounted = true;
                }
            }
        };
    }
};
function getProps(props, modifier) {
    var _props$popperOptions;
    return {
        popperOptions: Object.assign({}, props.popperOptions, {
            modifiers: [].concat((((_props$popperOptions = props.popperOptions) == null ? void 0 : _props$popperOptions.modifiers) || []).filter(function(_ref) {
                var name = _ref.name;
                return name !== modifier.name;
            }), [
                modifier
            ])
        })
    };
}
var inlinePositioning = {
    name: 'inlinePositioning',
    defaultValue: false,
    fn: function fn(instance) {
        var isEnabled = function isEnabled() {
            return !!instance.props.inlinePositioning;
        };
        var _getReferenceClientRect = function _getReferenceClientRect(placement) {
            return getInlineBoundingClientRect(getBasePlacement(placement), reference.getBoundingClientRect(), arrayFrom(reference.getClientRects()), cursorRectIndex);
        };
        var setInternalProps = function setInternalProps(partialProps) {
            isInternalUpdate = true;
            instance.setProps(partialProps);
            isInternalUpdate = false;
        };
        var addModifier = function addModifier() {
            if (!isInternalUpdate) setInternalProps(getProps(instance.props, modifier));
        };
        var reference = instance.reference;
        var placement1;
        var cursorRectIndex = -1;
        var isInternalUpdate = false;
        var modifier = {
            name: 'tippyInlinePositioning',
            enabled: true,
            phase: 'afterWrite',
            fn: function fn(_ref2) {
                var state = _ref2.state;
                if (isEnabled()) {
                    if (placement1 !== state.placement) instance.setProps({
                        getReferenceClientRect: function getReferenceClientRect() {
                            return _getReferenceClientRect(state.placement);
                        }
                    });
                    placement1 = state.placement;
                }
            }
        };
        return {
            onCreate: addModifier,
            onAfterUpdate: addModifier,
            onTrigger: function onTrigger(_, event) {
                if (isMouseEvent(event)) {
                    var rects = arrayFrom(instance.reference.getClientRects());
                    var cursorRect = rects.find(function(rect) {
                        return rect.left - 2 <= event.clientX && rect.right + 2 >= event.clientX && rect.top - 2 <= event.clientY && rect.bottom + 2 >= event.clientY;
                    });
                    cursorRectIndex = rects.indexOf(cursorRect);
                }
            },
            onUntrigger: function onUntrigger() {
                cursorRectIndex = -1;
            }
        };
    }
};
function getInlineBoundingClientRect(currentBasePlacement, boundingRect, clientRects, cursorRectIndex) {
    // Not an inline element, or placement is not yet known
    if (clientRects.length < 2 || currentBasePlacement === null) return boundingRect;
     // There are two rects and they are disjoined
    if (clientRects.length === 2 && cursorRectIndex >= 0 && clientRects[0].left > clientRects[1].right) return clientRects[cursorRectIndex] || boundingRect;
    switch(currentBasePlacement){
        case 'top':
        case 'bottom':
            var firstRect = clientRects[0];
            var lastRect = clientRects[clientRects.length - 1];
            var isTop = currentBasePlacement === 'top';
            var top = firstRect.top;
            var bottom = lastRect.bottom;
            var left = isTop ? firstRect.left : lastRect.left;
            var right = isTop ? firstRect.right : lastRect.right;
            var width = right - left;
            var height = bottom - top;
            return {
                top: top,
                bottom: bottom,
                left: left,
                right: right,
                width: width,
                height: height
            };
        case 'left':
        case 'right':
            var minLeft = Math.min.apply(Math, clientRects.map(function(rects) {
                return rects.left;
            }));
            var maxRight = Math.max.apply(Math, clientRects.map(function(rects) {
                return rects.right;
            }));
            var measureRects = clientRects.filter(function(rect) {
                return currentBasePlacement === 'left' ? rect.left === minLeft : rect.right === maxRight;
            });
            var _top = measureRects[0].top;
            var _bottom = measureRects[measureRects.length - 1].bottom;
            var _left = minLeft;
            var _right = maxRight;
            var _width = _right - _left;
            var _height = _bottom - _top;
            return {
                top: _top,
                bottom: _bottom,
                left: _left,
                right: _right,
                width: _width,
                height: _height
            };
        default:
            return boundingRect;
    }
}
var sticky = {
    name: 'sticky',
    defaultValue: false,
    fn: function fn(instance) {
        var getReference = function getReference() {
            return instance.popperInstance ? instance.popperInstance.state.elements.reference : reference;
        };
        var shouldCheck = function shouldCheck(value) {
            return instance.props.sticky === true || instance.props.sticky === value;
        };
        var reference = instance.reference, popper = instance.popper;
        var prevRefRect = null;
        var prevPopRect = null;
        function updatePosition() {
            var currentRefRect = shouldCheck('reference') ? getReference().getBoundingClientRect() : null;
            var currentPopRect = shouldCheck('popper') ? popper.getBoundingClientRect() : null;
            if (currentRefRect && areRectsDifferent(prevRefRect, currentRefRect) || currentPopRect && areRectsDifferent(prevPopRect, currentPopRect)) {
                if (instance.popperInstance) instance.popperInstance.update();
            }
            prevRefRect = currentRefRect;
            prevPopRect = currentPopRect;
            if (instance.state.isMounted) requestAnimationFrame(updatePosition);
        }
        return {
            onMount: function onMount() {
                if (instance.props.sticky) updatePosition();
            }
        };
    }
};
function areRectsDifferent(rectA, rectB) {
    if (rectA && rectB) return rectA.top !== rectB.top || rectA.right !== rectB.right || rectA.bottom !== rectB.bottom || rectA.left !== rectB.left;
    return true;
}
tippy.setDefaultProps({
    render: render
});
exports.default = tippy;

},{"@popperjs/core":"lxYxu","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"lxYxu":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "createPopper", function() {
    return createPopper;
});
parcelHelpers.export(exports, "popperGenerator", function() {
    return _indexJs.popperGenerator;
});
parcelHelpers.export(exports, "defaultModifiers", function() {
    return defaultModifiers;
});
parcelHelpers.export(exports, "detectOverflow", function() {
    return _indexJs.detectOverflow;
});
var _indexJs = require("./index.js");
var _eventListenersJs = require("./modifiers/eventListeners.js");
var _eventListenersJsDefault = parcelHelpers.interopDefault(_eventListenersJs);
var _popperOffsetsJs = require("./modifiers/popperOffsets.js");
var _popperOffsetsJsDefault = parcelHelpers.interopDefault(_popperOffsetsJs);
var _computeStylesJs = require("./modifiers/computeStyles.js");
var _computeStylesJsDefault = parcelHelpers.interopDefault(_computeStylesJs);
var _applyStylesJs = require("./modifiers/applyStyles.js");
var _applyStylesJsDefault = parcelHelpers.interopDefault(_applyStylesJs);
var _offsetJs = require("./modifiers/offset.js");
var _offsetJsDefault = parcelHelpers.interopDefault(_offsetJs);
var _flipJs = require("./modifiers/flip.js");
var _flipJsDefault = parcelHelpers.interopDefault(_flipJs);
var _preventOverflowJs = require("./modifiers/preventOverflow.js");
var _preventOverflowJsDefault = parcelHelpers.interopDefault(_preventOverflowJs);
var _arrowJs = require("./modifiers/arrow.js");
var _arrowJsDefault = parcelHelpers.interopDefault(_arrowJs);
var _hideJs = require("./modifiers/hide.js");
var _hideJsDefault = parcelHelpers.interopDefault(_hideJs);
var defaultModifiers = [
    _eventListenersJsDefault.default,
    _popperOffsetsJsDefault.default,
    _computeStylesJsDefault.default,
    _applyStylesJsDefault.default,
    _offsetJsDefault.default,
    _flipJsDefault.default,
    _preventOverflowJsDefault.default,
    _arrowJsDefault.default,
    _hideJsDefault.default
];
var createPopper = /*#__PURE__*/ _indexJs.popperGenerator({
    defaultModifiers: defaultModifiers
}); // eslint-disable-next-line import/no-unused-modules

},{"./index.js":"he8kM","./modifiers/eventListeners.js":"bGFH1","./modifiers/popperOffsets.js":"gx0If","./modifiers/computeStyles.js":"jLSZu","./modifiers/applyStyles.js":"hz8MT","./modifiers/offset.js":"ei7o5","./modifiers/flip.js":"iuE8D","./modifiers/preventOverflow.js":"4F5cZ","./modifiers/arrow.js":"3355Z","./modifiers/hide.js":"bnIFG","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"he8kM":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "popperGenerator", function() {
    return popperGenerator;
});
parcelHelpers.export(exports, "createPopper", function() {
    return createPopper;
});
parcelHelpers.export(exports, "detectOverflow", function() {
    return _detectOverflowJsDefault.default;
});
var _getCompositeRectJs = require("./dom-utils/getCompositeRect.js");
var _getCompositeRectJsDefault = parcelHelpers.interopDefault(_getCompositeRectJs);
var _getLayoutRectJs = require("./dom-utils/getLayoutRect.js");
var _getLayoutRectJsDefault = parcelHelpers.interopDefault(_getLayoutRectJs);
var _listScrollParentsJs = require("./dom-utils/listScrollParents.js");
var _listScrollParentsJsDefault = parcelHelpers.interopDefault(_listScrollParentsJs);
var _getOffsetParentJs = require("./dom-utils/getOffsetParent.js");
var _getOffsetParentJsDefault = parcelHelpers.interopDefault(_getOffsetParentJs);
var _getComputedStyleJs = require("./dom-utils/getComputedStyle.js");
var _getComputedStyleJsDefault = parcelHelpers.interopDefault(_getComputedStyleJs);
var _orderModifiersJs = require("./utils/orderModifiers.js");
var _orderModifiersJsDefault = parcelHelpers.interopDefault(_orderModifiersJs);
var _debounceJs = require("./utils/debounce.js");
var _debounceJsDefault = parcelHelpers.interopDefault(_debounceJs);
var _validateModifiersJs = require("./utils/validateModifiers.js");
var _validateModifiersJsDefault = parcelHelpers.interopDefault(_validateModifiersJs);
var _uniqueByJs = require("./utils/uniqueBy.js");
var _uniqueByJsDefault = parcelHelpers.interopDefault(_uniqueByJs);
var _getBasePlacementJs = require("./utils/getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var _mergeByNameJs = require("./utils/mergeByName.js");
var _mergeByNameJsDefault = parcelHelpers.interopDefault(_mergeByNameJs);
var _detectOverflowJs = require("./utils/detectOverflow.js");
var _detectOverflowJsDefault = parcelHelpers.interopDefault(_detectOverflowJs);
var _instanceOfJs = require("./dom-utils/instanceOf.js");
var _enumsJs = require("./enums.js");
parcelHelpers.exportAll(_enumsJs, exports);
var INVALID_ELEMENT_ERROR = 'Popper: Invalid reference or popper argument provided. They must be either a DOM element or virtual element.';
var INFINITE_LOOP_ERROR = 'Popper: An infinite loop in the modifiers cycle has been detected! The cycle has been interrupted to prevent a browser crash.';
var DEFAULT_OPTIONS = {
    placement: 'bottom',
    modifiers: [],
    strategy: 'absolute'
};
function areValidElements() {
    for(var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++)args[_key] = arguments[_key];
    return !args.some(function(element) {
        return !(element && typeof element.getBoundingClientRect === 'function');
    });
}
function popperGenerator(generatorOptions) {
    if (generatorOptions === void 0) generatorOptions = {};
    var _generatorOptions = generatorOptions, _generatorOptions$def = _generatorOptions.defaultModifiers, defaultModifiers = _generatorOptions$def === void 0 ? [] : _generatorOptions$def, _generatorOptions$def2 = _generatorOptions.defaultOptions, defaultOptions = _generatorOptions$def2 === void 0 ? DEFAULT_OPTIONS : _generatorOptions$def2;
    return function createPopper(reference, popper, options1) {
        var runModifierEffects = // update cycle runs. They will be executed in the same order as the update
        // cycle. This is useful when a modifier adds some persistent data that
        // other modifiers need to use, but the modifier is run after the dependent
        // one.
        function runModifierEffects() {
            state1.orderedModifiers.forEach(function(_ref3) {
                var name = _ref3.name, _ref3$options = _ref3.options, _$options = _ref3$options === void 0 ? {} : _ref3$options, effect = _ref3.effect;
                if (typeof effect === 'function') {
                    var cleanupFn = effect({
                        state: state1,
                        name: name,
                        instance: instance,
                        options: _$options
                    });
                    var noopFn = function noopFn() {};
                    effectCleanupFns.push(cleanupFn || noopFn);
                }
            });
        };
        var cleanupModifierEffects = function cleanupModifierEffects() {
            effectCleanupFns.forEach(function(fn) {
                return fn();
            });
            effectCleanupFns = [];
        };
        if (options1 === void 0) options1 = defaultOptions;
        var state1 = {
            placement: 'bottom',
            orderedModifiers: [],
            options: Object.assign(Object.assign({}, DEFAULT_OPTIONS), defaultOptions),
            modifiersData: {},
            elements: {
                reference: reference,
                popper: popper
            },
            attributes: {},
            styles: {}
        };
        var effectCleanupFns = [];
        var isDestroyed = false;
        var instance = {
            state: state1,
            setOptions: function setOptions(options) {
                cleanupModifierEffects();
                state1.options = Object.assign(Object.assign(Object.assign({}, defaultOptions), state1.options), options);
                state1.scrollParents = {
                    reference: _instanceOfJs.isElement(reference) ? _listScrollParentsJsDefault.default(reference) : reference.contextElement ? _listScrollParentsJsDefault.default(reference.contextElement) : [],
                    popper: _listScrollParentsJsDefault.default(popper)
                }; // Orders the modifiers based on their dependencies and `phase`
                // properties
                var orderedModifiers = _orderModifiersJsDefault.default(_mergeByNameJsDefault.default([].concat(defaultModifiers, state1.options.modifiers))); // Strip out disabled modifiers
                state1.orderedModifiers = orderedModifiers.filter(function(m) {
                    return m.enabled;
                }); // Validate the provided modifiers so that the consumer will get warned
                var modifiers = _uniqueByJsDefault.default([].concat(orderedModifiers, state1.options.modifiers), function(_ref) {
                    var name = _ref.name;
                    return name;
                });
                _validateModifiersJsDefault.default(modifiers);
                if (_getBasePlacementJsDefault.default(state1.options.placement) === _enumsJs.auto) {
                    var flipModifier = state1.orderedModifiers.find(function(_ref2) {
                        var name = _ref2.name;
                        return name === 'flip';
                    });
                    if (!flipModifier) console.error([
                        'Popper: "auto" placements require the "flip" modifier be',
                        'present and enabled to work.'
                    ].join(' '));
                }
                var _getComputedStyle = _getComputedStyleJsDefault.default(popper), marginTop = _getComputedStyle.marginTop, marginRight = _getComputedStyle.marginRight, marginBottom = _getComputedStyle.marginBottom, marginLeft = _getComputedStyle.marginLeft; // We no longer take into account `margins` on the popper, and it can
                // cause bugs with positioning, so we'll warn the consumer
                if ([
                    marginTop,
                    marginRight,
                    marginBottom,
                    marginLeft
                ].some(function(margin) {
                    return parseFloat(margin);
                })) console.warn([
                    'Popper: CSS "margin" styles cannot be used to apply padding',
                    'between the popper and its reference element or boundary.',
                    'To replicate margin, use the `offset` modifier, as well as',
                    'the `padding` option in the `preventOverflow` and `flip`',
                    'modifiers.'
                ].join(' '));
                runModifierEffects();
                return instance.update();
            },
            // Sync update – it will always be executed, even if not necessary. This
            // is useful for low frequency updates where sync behavior simplifies the
            // logic.
            // For high frequency updates (e.g. `resize` and `scroll` events), always
            // prefer the async Popper#update method
            forceUpdate: function forceUpdate() {
                if (isDestroyed) return;
                var _state$elements = state1.elements, _$reference = _state$elements.reference, _$popper = _state$elements.popper; // Don't proceed if `reference` or `popper` are not valid elements
                // anymore
                if (!areValidElements(_$reference, _$popper)) {
                    console.error(INVALID_ELEMENT_ERROR);
                    return;
                } // Store the reference and popper rects to be read by modifiers
                state1.rects = {
                    reference: _getCompositeRectJsDefault.default(_$reference, _getOffsetParentJsDefault.default(_$popper), state1.options.strategy === 'fixed'),
                    popper: _getLayoutRectJsDefault.default(_$popper)
                }; // Modifiers have the ability to reset the current update cycle. The
                // most common use case for this is the `flip` modifier changing the
                // placement, which then needs to re-run all the modifiers, because the
                // logic was previously ran for the previous placement and is therefore
                // stale/incorrect
                state1.reset = false;
                state1.placement = state1.options.placement; // On each update cycle, the `modifiersData` property for each modifier
                // is filled with the initial data specified by the modifier. This means
                // it doesn't persist and is fresh on each update.
                // To ensure persistent data, use `${name}#persistent`
                state1.orderedModifiers.forEach(function(modifier) {
                    return state1.modifiersData[modifier.name] = Object.assign({}, modifier.data);
                });
                var __debug_loops__ = 0;
                for(var index = 0; index < state1.orderedModifiers.length; index++){
                    __debug_loops__ += 1;
                    if (__debug_loops__ > 100) {
                        console.error(INFINITE_LOOP_ERROR);
                        break;
                    }
                    if (state1.reset === true) {
                        state1.reset = false;
                        index = -1;
                        continue;
                    }
                    var _state$orderedModifie = state1.orderedModifiers[index], fn = _state$orderedModifie.fn, _state$orderedModifie2 = _state$orderedModifie.options, _options = _state$orderedModifie2 === void 0 ? {} : _state$orderedModifie2, name = _state$orderedModifie.name;
                    if (typeof fn === 'function') state1 = fn({
                        state: state1,
                        options: _options,
                        name: name,
                        instance: instance
                    }) || state1;
                }
            },
            // Async and optimistically optimized update – it will not be executed if
            // not necessary (debounced to run at most once-per-tick)
            update: _debounceJsDefault.default(function() {
                return new Promise(function(resolve) {
                    instance.forceUpdate();
                    resolve(state1);
                });
            }),
            destroy: function destroy() {
                cleanupModifierEffects();
                isDestroyed = true;
            }
        };
        if (!areValidElements(reference, popper)) {
            console.error(INVALID_ELEMENT_ERROR);
            return instance;
        }
        instance.setOptions(options1).then(function(state) {
            if (!isDestroyed && options1.onFirstUpdate) options1.onFirstUpdate(state);
        }); // Modifiers have the ability to execute arbitrary code before the first
        return instance;
    };
}
var createPopper = /*#__PURE__*/ popperGenerator(); // eslint-disable-next-line import/no-unused-modules

},{"./dom-utils/getCompositeRect.js":"koJdl","./dom-utils/getLayoutRect.js":"bb9Mh","./dom-utils/listScrollParents.js":"488js","./dom-utils/getOffsetParent.js":"apRsT","./dom-utils/getComputedStyle.js":"k2rR5","./utils/orderModifiers.js":"51P9w","./utils/debounce.js":"dx96h","./utils/validateModifiers.js":"hffS2","./utils/uniqueBy.js":"7U8Zn","./utils/getBasePlacement.js":"c3ZMV","./utils/mergeByName.js":"jk9oU","./utils/detectOverflow.js":"gNzja","./dom-utils/instanceOf.js":"9bvfh","./enums.js":"daeOT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"koJdl":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getBoundingClientRectJs = require("./getBoundingClientRect.js");
var _getBoundingClientRectJsDefault = parcelHelpers.interopDefault(_getBoundingClientRectJs);
var _getNodeScrollJs = require("./getNodeScroll.js");
var _getNodeScrollJsDefault = parcelHelpers.interopDefault(_getNodeScrollJs);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _instanceOfJs = require("./instanceOf.js");
var _getWindowScrollBarXJs = require("./getWindowScrollBarX.js");
var _getWindowScrollBarXJsDefault = parcelHelpers.interopDefault(_getWindowScrollBarXJs);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _isScrollParentJs = require("./isScrollParent.js"); // Returns the composite rect of an element relative to its offsetParent.
var _isScrollParentJsDefault = parcelHelpers.interopDefault(_isScrollParentJs);
function getCompositeRect(elementOrVirtualElement, offsetParent, isFixed) {
    if (isFixed === void 0) isFixed = false;
    var documentElement = _getDocumentElementJsDefault.default(offsetParent);
    var rect = _getBoundingClientRectJsDefault.default(elementOrVirtualElement);
    var isOffsetParentAnElement = _instanceOfJs.isHTMLElement(offsetParent);
    var scroll = {
        scrollLeft: 0,
        scrollTop: 0
    };
    var offsets = {
        x: 0,
        y: 0
    };
    if (isOffsetParentAnElement || !isOffsetParentAnElement && !isFixed) {
        if (_getNodeNameJsDefault.default(offsetParent) !== 'body' || _isScrollParentJsDefault.default(documentElement)) scroll = _getNodeScrollJsDefault.default(offsetParent);
        if (_instanceOfJs.isHTMLElement(offsetParent)) {
            offsets = _getBoundingClientRectJsDefault.default(offsetParent);
            offsets.x += offsetParent.clientLeft;
            offsets.y += offsetParent.clientTop;
        } else if (documentElement) offsets.x = _getWindowScrollBarXJsDefault.default(documentElement);
    }
    return {
        x: rect.left + scroll.scrollLeft - offsets.x,
        y: rect.top + scroll.scrollTop - offsets.y,
        width: rect.width,
        height: rect.height
    };
}
exports.default = getCompositeRect;

},{"./getBoundingClientRect.js":"kRcrc","./getNodeScroll.js":"h5F0B","./getNodeName.js":"92CvH","./instanceOf.js":"9bvfh","./getWindowScrollBarX.js":"9hIdB","./getDocumentElement.js":"ltWTM","./isScrollParent.js":"9Imrt","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"kRcrc":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getBoundingClientRect(element) {
    var rect = element.getBoundingClientRect();
    return {
        width: rect.width,
        height: rect.height,
        top: rect.top,
        right: rect.right,
        bottom: rect.bottom,
        left: rect.left,
        x: rect.left,
        y: rect.top
    };
}
exports.default = getBoundingClientRect;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"h5F0B":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getWindowScrollJs = require("./getWindowScroll.js");
var _getWindowScrollJsDefault = parcelHelpers.interopDefault(_getWindowScrollJs);
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
var _instanceOfJs = require("./instanceOf.js");
var _getHTMLElementScrollJs = require("./getHTMLElementScroll.js");
var _getHTMLElementScrollJsDefault = parcelHelpers.interopDefault(_getHTMLElementScrollJs);
function getNodeScroll(node) {
    if (node === _getWindowJsDefault.default(node) || !_instanceOfJs.isHTMLElement(node)) return _getWindowScrollJsDefault.default(node);
    else return _getHTMLElementScrollJsDefault.default(node);
}
exports.default = getNodeScroll;

},{"./getWindowScroll.js":"i6J1Y","./getWindow.js":"4BVw2","./instanceOf.js":"9bvfh","./getHTMLElementScroll.js":"39fm0","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"i6J1Y":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
function getWindowScroll(node) {
    var win = _getWindowJsDefault.default(node);
    var scrollLeft = win.pageXOffset;
    var scrollTop = win.pageYOffset;
    return {
        scrollLeft: scrollLeft,
        scrollTop: scrollTop
    };
}
exports.default = getWindowScroll;

},{"./getWindow.js":"4BVw2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4BVw2":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getWindow(node) {
    if (node.toString() !== '[object Window]') {
        var ownerDocument = node.ownerDocument;
        return ownerDocument ? ownerDocument.defaultView : window;
    }
    return node;
}
exports.default = getWindow;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9bvfh":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "isElement", function() {
    return isElement;
});
parcelHelpers.export(exports, "isHTMLElement", function() {
    return isHTMLElement;
});
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
/*:: declare function isElement(node: mixed): boolean %checks(node instanceof
  Element); */ function isElement(node) {
    var OwnElement = _getWindowJsDefault.default(node).Element;
    return node instanceof OwnElement || node instanceof Element;
}
/*:: declare function isHTMLElement(node: mixed): boolean %checks(node instanceof
  HTMLElement); */ function isHTMLElement(node) {
    var OwnElement = _getWindowJsDefault.default(node).HTMLElement;
    return node instanceof OwnElement || node instanceof HTMLElement;
}

},{"./getWindow.js":"4BVw2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"39fm0":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getHTMLElementScroll(element) {
    return {
        scrollLeft: element.scrollLeft,
        scrollTop: element.scrollTop
    };
}
exports.default = getHTMLElementScroll;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"92CvH":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getNodeName(element) {
    return element ? (element.nodeName || '').toLowerCase() : null;
}
exports.default = getNodeName;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9hIdB":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getBoundingClientRectJs = require("./getBoundingClientRect.js");
var _getBoundingClientRectJsDefault = parcelHelpers.interopDefault(_getBoundingClientRectJs);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _getWindowScrollJs = require("./getWindowScroll.js");
var _getWindowScrollJsDefault = parcelHelpers.interopDefault(_getWindowScrollJs);
function getWindowScrollBarX(element) {
    // If <html> has a CSS width greater than the viewport, then this will be
    // incorrect for RTL.
    // Popper 1 is broken in this case and never had a bug report so let's assume
    // it's not an issue. I don't think anyone ever specifies width on <html>
    // anyway.
    // Browsers where the left scrollbar doesn't cause an issue report `0` for
    // this (e.g. Edge 2019, IE11, Safari)
    return _getBoundingClientRectJsDefault.default(_getDocumentElementJsDefault.default(element)).left + _getWindowScrollJsDefault.default(element).scrollLeft;
}
exports.default = getWindowScrollBarX;

},{"./getBoundingClientRect.js":"kRcrc","./getDocumentElement.js":"ltWTM","./getWindowScroll.js":"i6J1Y","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ltWTM":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _instanceOfJs = require("./instanceOf.js");
function getDocumentElement(element) {
    // $FlowFixMe: assume body is always available
    return (_instanceOfJs.isElement(element) ? element.ownerDocument : element.document).documentElement;
}
exports.default = getDocumentElement;

},{"./instanceOf.js":"9bvfh","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9Imrt":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getComputedStyleJs = require("./getComputedStyle.js");
var _getComputedStyleJsDefault = parcelHelpers.interopDefault(_getComputedStyleJs);
function isScrollParent(element) {
    // Firefox wants us to check `-x` and `-y` variations as well
    var _getComputedStyle = _getComputedStyleJsDefault.default(element), overflow = _getComputedStyle.overflow, overflowX = _getComputedStyle.overflowX, overflowY = _getComputedStyle.overflowY;
    return /auto|scroll|overlay|hidden/.test(overflow + overflowY + overflowX);
}
exports.default = isScrollParent;

},{"./getComputedStyle.js":"k2rR5","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"k2rR5":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
function getComputedStyle(element) {
    return _getWindowJsDefault.default(element).getComputedStyle(element);
}
exports.default = getComputedStyle;

},{"./getWindow.js":"4BVw2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bb9Mh":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getLayoutRect(element) {
    return {
        x: element.offsetLeft,
        y: element.offsetTop,
        width: element.offsetWidth,
        height: element.offsetHeight
    };
}
exports.default = getLayoutRect;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"488js":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getScrollParentJs = require("./getScrollParent.js");
var _getScrollParentJsDefault = parcelHelpers.interopDefault(_getScrollParentJs);
var _getParentNodeJs = require("./getParentNode.js");
var _getParentNodeJsDefault = parcelHelpers.interopDefault(_getParentNodeJs);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
var _isScrollParentJs = require("./isScrollParent.js");
var _isScrollParentJsDefault = parcelHelpers.interopDefault(_isScrollParentJs);
function listScrollParents(element, list) {
    if (list === void 0) list = [];
    var scrollParent = _getScrollParentJsDefault.default(element);
    var isBody = _getNodeNameJsDefault.default(scrollParent) === 'body';
    var win = _getWindowJsDefault.default(scrollParent);
    var target = isBody ? [
        win
    ].concat(win.visualViewport || [], _isScrollParentJsDefault.default(scrollParent) ? scrollParent : []) : scrollParent;
    var updatedList = list.concat(target);
    return isBody ? updatedList : updatedList.concat(listScrollParents(_getParentNodeJsDefault.default(target)));
}
exports.default = listScrollParents;

},{"./getScrollParent.js":"geufa","./getParentNode.js":"8gwQz","./getNodeName.js":"92CvH","./getWindow.js":"4BVw2","./isScrollParent.js":"9Imrt","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"geufa":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getParentNodeJs = require("./getParentNode.js");
var _getParentNodeJsDefault = parcelHelpers.interopDefault(_getParentNodeJs);
var _isScrollParentJs = require("./isScrollParent.js");
var _isScrollParentJsDefault = parcelHelpers.interopDefault(_isScrollParentJs);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _instanceOfJs = require("./instanceOf.js");
function getScrollParent(node) {
    if ([
        'html',
        'body',
        '#document'
    ].indexOf(_getNodeNameJsDefault.default(node)) >= 0) // $FlowFixMe: assume body is always available
    return node.ownerDocument.body;
    if (_instanceOfJs.isHTMLElement(node) && _isScrollParentJsDefault.default(node)) return node;
    return getScrollParent(_getParentNodeJsDefault.default(node));
}
exports.default = getScrollParent;

},{"./getParentNode.js":"8gwQz","./isScrollParent.js":"9Imrt","./getNodeName.js":"92CvH","./instanceOf.js":"9bvfh","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"8gwQz":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
function getParentNode(element) {
    if (_getNodeNameJsDefault.default(element) === 'html') return element;
    return element.assignedSlot || element.parentNode || // $FlowFixMe: need a better way to handle this...
    element.host || // $FlowFixMe: HTMLElement is a Node
    _getDocumentElementJsDefault.default(element) // fallback
    ;
}
exports.default = getParentNode;

},{"./getNodeName.js":"92CvH","./getDocumentElement.js":"ltWTM","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"apRsT":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _getComputedStyleJs = require("./getComputedStyle.js");
var _getComputedStyleJsDefault = parcelHelpers.interopDefault(_getComputedStyleJs);
var _instanceOfJs = require("./instanceOf.js");
var _isTableElementJs = require("./isTableElement.js");
var _isTableElementJsDefault = parcelHelpers.interopDefault(_isTableElementJs);
var _getParentNodeJs = require("./getParentNode.js");
var _getParentNodeJsDefault = parcelHelpers.interopDefault(_getParentNodeJs);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
function getTrueOffsetParent(element) {
    if (!_instanceOfJs.isHTMLElement(element) || _getComputedStyleJsDefault.default(element).position === 'fixed') return null;
    var offsetParent = element.offsetParent;
    if (offsetParent) {
        var html = _getDocumentElementJsDefault.default(offsetParent);
        if (_getNodeNameJsDefault.default(offsetParent) === 'body' && _getComputedStyleJsDefault.default(offsetParent).position === 'static' && _getComputedStyleJsDefault.default(html).position !== 'static') return html;
    }
    return offsetParent;
} // `.offsetParent` reports `null` for fixed elements, while absolute elements
// return the containing block
function getContainingBlock(element) {
    var currentNode = _getParentNodeJsDefault.default(element);
    while(_instanceOfJs.isHTMLElement(currentNode) && [
        'html',
        'body'
    ].indexOf(_getNodeNameJsDefault.default(currentNode)) < 0){
        var css = _getComputedStyleJsDefault.default(currentNode); // This is non-exhaustive but covers the most common CSS properties that
        // create a containing block.
        if (css.transform !== 'none' || css.perspective !== 'none' || css.willChange && css.willChange !== 'auto') return currentNode;
        else currentNode = currentNode.parentNode;
    }
    return null;
} // Gets the closest ancestor positioned element. Handles some edge cases,
function getOffsetParent(element) {
    var window = _getWindowJsDefault.default(element);
    var offsetParent = getTrueOffsetParent(element);
    while(offsetParent && _isTableElementJsDefault.default(offsetParent) && _getComputedStyleJsDefault.default(offsetParent).position === 'static')offsetParent = getTrueOffsetParent(offsetParent);
    if (offsetParent && _getNodeNameJsDefault.default(offsetParent) === 'body' && _getComputedStyleJsDefault.default(offsetParent).position === 'static') return window;
    return offsetParent || getContainingBlock(element) || window;
}
exports.default = getOffsetParent;

},{"./getWindow.js":"4BVw2","./getNodeName.js":"92CvH","./getComputedStyle.js":"k2rR5","./instanceOf.js":"9bvfh","./isTableElement.js":"gpz44","./getParentNode.js":"8gwQz","./getDocumentElement.js":"ltWTM","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"gpz44":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
function isTableElement(element) {
    return [
        'table',
        'td',
        'th'
    ].indexOf(_getNodeNameJsDefault.default(element)) >= 0;
}
exports.default = isTableElement;

},{"./getNodeName.js":"92CvH","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"51P9w":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _enumsJs = require("../enums.js"); // source: https://stackoverflow.com/questions/49875255
function order(modifiers) {
    var map = new Map();
    var visited = new Set();
    var result = [];
    modifiers.forEach(function(modifier) {
        map.set(modifier.name, modifier);
    }); // On visiting object, check for its dependencies and visit them recursively
    function sort(modifier) {
        visited.add(modifier.name);
        var requires = [].concat(modifier.requires || [], modifier.requiresIfExists || []);
        requires.forEach(function(dep) {
            if (!visited.has(dep)) {
                var depModifier = map.get(dep);
                if (depModifier) sort(depModifier);
            }
        });
        result.push(modifier);
    }
    modifiers.forEach(function(modifier) {
        if (!visited.has(modifier.name)) // check for visited object
        sort(modifier);
    });
    return result;
}
function orderModifiers(modifiers) {
    // order based on dependencies
    var orderedModifiers = order(modifiers); // order based on phase
    return _enumsJs.modifierPhases.reduce(function(acc, phase) {
        return acc.concat(orderedModifiers.filter(function(modifier) {
            return modifier.phase === phase;
        }));
    }, []);
}
exports.default = orderModifiers;

},{"../enums.js":"daeOT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"daeOT":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "top", function() {
    return top;
});
parcelHelpers.export(exports, "bottom", function() {
    return bottom;
});
parcelHelpers.export(exports, "right", function() {
    return right;
});
parcelHelpers.export(exports, "left", function() {
    return left;
});
parcelHelpers.export(exports, "auto", function() {
    return auto;
});
parcelHelpers.export(exports, "basePlacements", function() {
    return basePlacements;
});
parcelHelpers.export(exports, "start", function() {
    return start;
});
parcelHelpers.export(exports, "end", function() {
    return end;
});
parcelHelpers.export(exports, "clippingParents", function() {
    return clippingParents;
});
parcelHelpers.export(exports, "viewport", function() {
    return viewport;
});
parcelHelpers.export(exports, "popper", function() {
    return popper;
});
parcelHelpers.export(exports, "reference", function() {
    return reference;
});
parcelHelpers.export(exports, "variationPlacements", function() {
    return variationPlacements;
});
parcelHelpers.export(exports, "placements", function() {
    return placements;
});
parcelHelpers.export(exports, "beforeRead", function() {
    return beforeRead;
});
parcelHelpers.export(exports, "read", function() {
    return read;
});
parcelHelpers.export(exports, "afterRead", function() {
    return afterRead;
});
parcelHelpers.export(exports, "beforeMain", function() {
    return beforeMain;
});
parcelHelpers.export(exports, "main", function() {
    return main;
});
parcelHelpers.export(exports, "afterMain", function() {
    return afterMain;
});
parcelHelpers.export(exports, "beforeWrite", function() {
    return beforeWrite;
});
parcelHelpers.export(exports, "write", function() {
    return write;
});
parcelHelpers.export(exports, "afterWrite", function() {
    return afterWrite;
});
parcelHelpers.export(exports, "modifierPhases", function() {
    return modifierPhases;
});
var top = 'top';
var bottom = 'bottom';
var right = 'right';
var left = 'left';
var auto = 'auto';
var basePlacements = [
    top,
    bottom,
    right,
    left
];
var start = 'start';
var end = 'end';
var clippingParents = 'clippingParents';
var viewport = 'viewport';
var popper = 'popper';
var reference = 'reference';
var variationPlacements = /*#__PURE__*/ basePlacements.reduce(function(acc, placement) {
    return acc.concat([
        placement + "-" + start,
        placement + "-" + end
    ]);
}, []);
var placements = /*#__PURE__*/ [].concat(basePlacements, [
    auto
]).reduce(function(acc, placement) {
    return acc.concat([
        placement,
        placement + "-" + start,
        placement + "-" + end
    ]);
}, []); // modifiers that need to read the DOM
var beforeRead = 'beforeRead';
var read = 'read';
var afterRead = 'afterRead'; // pure-logic modifiers
var beforeMain = 'beforeMain';
var main = 'main';
var afterMain = 'afterMain'; // modifier with the purpose to write to the DOM (or write into a framework state)
var beforeWrite = 'beforeWrite';
var write = 'write';
var afterWrite = 'afterWrite';
var modifierPhases = [
    beforeRead,
    read,
    afterRead,
    beforeMain,
    main,
    afterMain,
    beforeWrite,
    write,
    afterWrite
];

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"dx96h":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function debounce(fn) {
    var pending;
    return function() {
        if (!pending) pending = new Promise(function(resolve) {
            Promise.resolve().then(function() {
                pending = undefined;
                resolve(fn());
            });
        });
        return pending;
    };
}
exports.default = debounce;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hffS2":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _formatJs = require("./format.js");
var _formatJsDefault = parcelHelpers.interopDefault(_formatJs);
var _enumsJs = require("../enums.js");
var INVALID_MODIFIER_ERROR = 'Popper: modifier "%s" provided an invalid %s property, expected %s but got %s';
var MISSING_DEPENDENCY_ERROR = 'Popper: modifier "%s" requires "%s", but "%s" modifier is not available';
var VALID_PROPERTIES = [
    'name',
    'enabled',
    'phase',
    'fn',
    'effect',
    'requires',
    'options'
];
function validateModifiers(modifiers) {
    modifiers.forEach(function(modifier) {
        Object.keys(modifier).forEach(function(key) {
            switch(key){
                case 'name':
                    if (typeof modifier.name !== 'string') console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, String(modifier.name), '"name"', '"string"', "\"" + String(modifier.name) + "\""));
                    break;
                case 'enabled':
                    if (typeof modifier.enabled !== 'boolean') console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, modifier.name, '"enabled"', '"boolean"', "\"" + String(modifier.enabled) + "\""));
                case 'phase':
                    if (_enumsJs.modifierPhases.indexOf(modifier.phase) < 0) console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, modifier.name, '"phase"', "either " + _enumsJs.modifierPhases.join(', '), "\"" + String(modifier.phase) + "\""));
                    break;
                case 'fn':
                    if (typeof modifier.fn !== 'function') console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, modifier.name, '"fn"', '"function"', "\"" + String(modifier.fn) + "\""));
                    break;
                case 'effect':
                    if (typeof modifier.effect !== 'function') console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, modifier.name, '"effect"', '"function"', "\"" + String(modifier.fn) + "\""));
                    break;
                case 'requires':
                    if (!Array.isArray(modifier.requires)) console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, modifier.name, '"requires"', '"array"', "\"" + String(modifier.requires) + "\""));
                    break;
                case 'requiresIfExists':
                    if (!Array.isArray(modifier.requiresIfExists)) console.error(_formatJsDefault.default(INVALID_MODIFIER_ERROR, modifier.name, '"requiresIfExists"', '"array"', "\"" + String(modifier.requiresIfExists) + "\""));
                    break;
                case 'options':
                case 'data':
                    break;
                default:
                    console.error("PopperJS: an invalid property has been provided to the \"" + modifier.name + "\" modifier, valid properties are " + VALID_PROPERTIES.map(function(s) {
                        return "\"" + s + "\"";
                    }).join(', ') + "; but \"" + key + "\" was provided.");
            }
            modifier.requires && modifier.requires.forEach(function(requirement) {
                if (modifiers.find(function(mod) {
                    return mod.name === requirement;
                }) == null) console.error(_formatJsDefault.default(MISSING_DEPENDENCY_ERROR, String(modifier.name), requirement, requirement));
            });
        });
    });
}
exports.default = validateModifiers;

},{"./format.js":"7pfZW","../enums.js":"daeOT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"7pfZW":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function format(str) {
    for(var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++)args[_key - 1] = arguments[_key];
    return [].concat(args).reduce(function(p, c) {
        return p.replace(/%s/, c);
    }, str);
}
exports.default = format;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"7U8Zn":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function uniqueBy(arr, fn) {
    var identifiers = new Set();
    return arr.filter(function(item) {
        var identifier = fn(item);
        if (!identifiers.has(identifier)) {
            identifiers.add(identifier);
            return true;
        }
    });
}
exports.default = uniqueBy;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"c3ZMV":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _enumsJs = require("../enums.js");
function getBasePlacement(placement) {
    return placement.split('-')[0];
}
exports.default = getBasePlacement;

},{"../enums.js":"daeOT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jk9oU":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function mergeByName(modifiers) {
    var merged1 = modifiers.reduce(function(merged, current) {
        var existing = merged[current.name];
        merged[current.name] = existing ? Object.assign(Object.assign(Object.assign({}, existing), current), {}, {
            options: Object.assign(Object.assign({}, existing.options), current.options),
            data: Object.assign(Object.assign({}, existing.data), current.data)
        }) : current;
        return merged;
    }, {}); // IE11 does not support Object.values
    return Object.keys(merged1).map(function(key) {
        return merged1[key];
    });
}
exports.default = mergeByName;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"gNzja":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getBoundingClientRectJs = require("../dom-utils/getBoundingClientRect.js");
var _getBoundingClientRectJsDefault = parcelHelpers.interopDefault(_getBoundingClientRectJs);
var _getClippingRectJs = require("../dom-utils/getClippingRect.js");
var _getClippingRectJsDefault = parcelHelpers.interopDefault(_getClippingRectJs);
var _getDocumentElementJs = require("../dom-utils/getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _computeOffsetsJs = require("./computeOffsets.js");
var _computeOffsetsJsDefault = parcelHelpers.interopDefault(_computeOffsetsJs);
var _rectToClientRectJs = require("./rectToClientRect.js");
var _rectToClientRectJsDefault = parcelHelpers.interopDefault(_rectToClientRectJs);
var _enumsJs = require("../enums.js");
var _instanceOfJs = require("../dom-utils/instanceOf.js");
var _mergePaddingObjectJs = require("./mergePaddingObject.js");
var _mergePaddingObjectJsDefault = parcelHelpers.interopDefault(_mergePaddingObjectJs);
var _expandToHashMapJs = require("./expandToHashMap.js"); // eslint-disable-next-line import/no-unused-modules
var _expandToHashMapJsDefault = parcelHelpers.interopDefault(_expandToHashMapJs);
function detectOverflow(state, options) {
    if (options === void 0) options = {};
    var _options = options, _options$placement = _options.placement, placement = _options$placement === void 0 ? state.placement : _options$placement, _options$boundary = _options.boundary, boundary = _options$boundary === void 0 ? _enumsJs.clippingParents : _options$boundary, _options$rootBoundary = _options.rootBoundary, rootBoundary = _options$rootBoundary === void 0 ? _enumsJs.viewport : _options$rootBoundary, _options$elementConte = _options.elementContext, elementContext = _options$elementConte === void 0 ? _enumsJs.popper : _options$elementConte, _options$altBoundary = _options.altBoundary, altBoundary = _options$altBoundary === void 0 ? false : _options$altBoundary, _options$padding = _options.padding, padding = _options$padding === void 0 ? 0 : _options$padding;
    var paddingObject = _mergePaddingObjectJsDefault.default(typeof padding !== 'number' ? padding : _expandToHashMapJsDefault.default(padding, _enumsJs.basePlacements));
    var altContext = elementContext === _enumsJs.popper ? _enumsJs.reference : _enumsJs.popper;
    var referenceElement = state.elements.reference;
    var popperRect = state.rects.popper;
    var element = state.elements[altBoundary ? altContext : elementContext];
    var clippingClientRect = _getClippingRectJsDefault.default(_instanceOfJs.isElement(element) ? element : element.contextElement || _getDocumentElementJsDefault.default(state.elements.popper), boundary, rootBoundary);
    var referenceClientRect = _getBoundingClientRectJsDefault.default(referenceElement);
    var popperOffsets = _computeOffsetsJsDefault.default({
        reference: referenceClientRect,
        element: popperRect,
        strategy: 'absolute',
        placement: placement
    });
    var popperClientRect = _rectToClientRectJsDefault.default(Object.assign(Object.assign({}, popperRect), popperOffsets));
    var elementClientRect = elementContext === _enumsJs.popper ? popperClientRect : referenceClientRect; // positive = overflowing the clipping rect
    // 0 or negative = within the clipping rect
    var overflowOffsets = {
        top: clippingClientRect.top - elementClientRect.top + paddingObject.top,
        bottom: elementClientRect.bottom - clippingClientRect.bottom + paddingObject.bottom,
        left: clippingClientRect.left - elementClientRect.left + paddingObject.left,
        right: elementClientRect.right - clippingClientRect.right + paddingObject.right
    };
    var offsetData = state.modifiersData.offset; // Offsets can be applied only to the popper element
    if (elementContext === _enumsJs.popper && offsetData) {
        var offset = offsetData[placement];
        Object.keys(overflowOffsets).forEach(function(key) {
            var multiply = [
                _enumsJs.right,
                _enumsJs.bottom
            ].indexOf(key) >= 0 ? 1 : -1;
            var axis = [
                _enumsJs.top,
                _enumsJs.bottom
            ].indexOf(key) >= 0 ? 'y' : 'x';
            overflowOffsets[key] += offset[axis] * multiply;
        });
    }
    return overflowOffsets;
}
exports.default = detectOverflow;

},{"../dom-utils/getBoundingClientRect.js":"kRcrc","../dom-utils/getClippingRect.js":"7oznE","../dom-utils/getDocumentElement.js":"ltWTM","./computeOffsets.js":"9jIFj","./rectToClientRect.js":"3Nry1","../enums.js":"daeOT","../dom-utils/instanceOf.js":"9bvfh","./mergePaddingObject.js":"cq9Cu","./expandToHashMap.js":"bHci0","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"7oznE":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _enumsJs = require("../enums.js");
var _getViewportRectJs = require("./getViewportRect.js");
var _getViewportRectJsDefault = parcelHelpers.interopDefault(_getViewportRectJs);
var _getDocumentRectJs = require("./getDocumentRect.js");
var _getDocumentRectJsDefault = parcelHelpers.interopDefault(_getDocumentRectJs);
var _listScrollParentsJs = require("./listScrollParents.js");
var _listScrollParentsJsDefault = parcelHelpers.interopDefault(_listScrollParentsJs);
var _getOffsetParentJs = require("./getOffsetParent.js");
var _getOffsetParentJsDefault = parcelHelpers.interopDefault(_getOffsetParentJs);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _getComputedStyleJs = require("./getComputedStyle.js");
var _getComputedStyleJsDefault = parcelHelpers.interopDefault(_getComputedStyleJs);
var _instanceOfJs = require("./instanceOf.js");
var _getBoundingClientRectJs = require("./getBoundingClientRect.js");
var _getBoundingClientRectJsDefault = parcelHelpers.interopDefault(_getBoundingClientRectJs);
var _getParentNodeJs = require("./getParentNode.js");
var _getParentNodeJsDefault = parcelHelpers.interopDefault(_getParentNodeJs);
var _containsJs = require("./contains.js");
var _containsJsDefault = parcelHelpers.interopDefault(_containsJs);
var _getNodeNameJs = require("./getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _rectToClientRectJs = require("../utils/rectToClientRect.js");
var _rectToClientRectJsDefault = parcelHelpers.interopDefault(_rectToClientRectJs);
function getInnerBoundingClientRect(element) {
    var rect = _getBoundingClientRectJsDefault.default(element);
    rect.top = rect.top + element.clientTop;
    rect.left = rect.left + element.clientLeft;
    rect.bottom = rect.top + element.clientHeight;
    rect.right = rect.left + element.clientWidth;
    rect.width = element.clientWidth;
    rect.height = element.clientHeight;
    rect.x = rect.left;
    rect.y = rect.top;
    return rect;
}
function getClientRectFromMixedType(element, clippingParent) {
    return clippingParent === _enumsJs.viewport ? _rectToClientRectJsDefault.default(_getViewportRectJsDefault.default(element)) : _instanceOfJs.isHTMLElement(clippingParent) ? getInnerBoundingClientRect(clippingParent) : _rectToClientRectJsDefault.default(_getDocumentRectJsDefault.default(_getDocumentElementJsDefault.default(element)));
} // A "clipping parent" is an overflowable container with the characteristic of
// clipping (or hiding) overflowing elements with a position different from
// `initial`
function getClippingParents(element) {
    var clippingParents = _listScrollParentsJsDefault.default(_getParentNodeJsDefault.default(element));
    var canEscapeClipping = [
        'absolute',
        'fixed'
    ].indexOf(_getComputedStyleJsDefault.default(element).position) >= 0;
    var clipperElement = canEscapeClipping && _instanceOfJs.isHTMLElement(element) ? _getOffsetParentJsDefault.default(element) : element;
    if (!_instanceOfJs.isElement(clipperElement)) return [];
     // $FlowFixMe: https://github.com/facebook/flow/issues/1414
    return clippingParents.filter(function(clippingParent) {
        return _instanceOfJs.isElement(clippingParent) && _containsJsDefault.default(clippingParent, clipperElement) && _getNodeNameJsDefault.default(clippingParent) !== 'body';
    });
} // Gets the maximum area that the element is visible in due to any number of
function getClippingRect(element, boundary, rootBoundary) {
    var mainClippingParents = boundary === 'clippingParents' ? getClippingParents(element) : [].concat(boundary);
    var clippingParents = [].concat(mainClippingParents, [
        rootBoundary
    ]);
    var firstClippingParent = clippingParents[0];
    var clippingRect = clippingParents.reduce(function(accRect, clippingParent) {
        var rect = getClientRectFromMixedType(element, clippingParent);
        accRect.top = Math.max(rect.top, accRect.top);
        accRect.right = Math.min(rect.right, accRect.right);
        accRect.bottom = Math.min(rect.bottom, accRect.bottom);
        accRect.left = Math.max(rect.left, accRect.left);
        return accRect;
    }, getClientRectFromMixedType(element, firstClippingParent));
    clippingRect.width = clippingRect.right - clippingRect.left;
    clippingRect.height = clippingRect.bottom - clippingRect.top;
    clippingRect.x = clippingRect.left;
    clippingRect.y = clippingRect.top;
    return clippingRect;
}
exports.default = getClippingRect;

},{"../enums.js":"daeOT","./getViewportRect.js":"4vkqe","./getDocumentRect.js":"aUzsp","./listScrollParents.js":"488js","./getOffsetParent.js":"apRsT","./getDocumentElement.js":"ltWTM","./getComputedStyle.js":"k2rR5","./instanceOf.js":"9bvfh","./getBoundingClientRect.js":"kRcrc","./getParentNode.js":"8gwQz","./contains.js":"iUMbF","./getNodeName.js":"92CvH","../utils/rectToClientRect.js":"3Nry1","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4vkqe":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getWindowJs = require("./getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _getWindowScrollBarXJs = require("./getWindowScrollBarX.js");
var _getWindowScrollBarXJsDefault = parcelHelpers.interopDefault(_getWindowScrollBarXJs);
function getViewportRect(element) {
    var win = _getWindowJsDefault.default(element);
    var html = _getDocumentElementJsDefault.default(element);
    var visualViewport = win.visualViewport;
    var width = html.clientWidth;
    var height = html.clientHeight;
    var x = 0;
    var y = 0; // NB: This isn't supported on iOS <= 12. If the keyboard is open, the popper
    // can be obscured underneath it.
    // Also, `html.clientHeight` adds the bottom bar height in Safari iOS, even
    // if it isn't open, so if this isn't available, the popper will be detected
    // to overflow the bottom of the screen too early.
    if (visualViewport) {
        width = visualViewport.width;
        height = visualViewport.height; // Uses Layout Viewport (like Chrome; Safari does not currently)
        // In Chrome, it returns a value very close to 0 (+/-) but contains rounding
        // errors due to floating point numbers, so we need to check precision.
        // Safari returns a number <= 0, usually < -1 when pinch-zoomed
        // Feature detection fails in mobile emulation mode in Chrome.
        // Math.abs(win.innerWidth / visualViewport.scale - visualViewport.width) <
        // 0.001
        // Fallback here: "Not Safari" userAgent
        if (!/^((?!chrome|android).)*safari/i.test(navigator.userAgent)) {
            x = visualViewport.offsetLeft;
            y = visualViewport.offsetTop;
        }
    }
    return {
        width: width,
        height: height,
        x: x + _getWindowScrollBarXJsDefault.default(element),
        y: y
    };
}
exports.default = getViewportRect;

},{"./getWindow.js":"4BVw2","./getDocumentElement.js":"ltWTM","./getWindowScrollBarX.js":"9hIdB","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"aUzsp":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getDocumentElementJs = require("./getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _getComputedStyleJs = require("./getComputedStyle.js");
var _getComputedStyleJsDefault = parcelHelpers.interopDefault(_getComputedStyleJs);
var _getWindowScrollBarXJs = require("./getWindowScrollBarX.js");
var _getWindowScrollBarXJsDefault = parcelHelpers.interopDefault(_getWindowScrollBarXJs);
var _getWindowScrollJs = require("./getWindowScroll.js"); // Gets the entire size of the scrollable document area, even extending outside
var _getWindowScrollJsDefault = parcelHelpers.interopDefault(_getWindowScrollJs);
function getDocumentRect(element) {
    var html = _getDocumentElementJsDefault.default(element);
    var winScroll = _getWindowScrollJsDefault.default(element);
    var body = element.ownerDocument.body;
    var width = Math.max(html.scrollWidth, html.clientWidth, body ? body.scrollWidth : 0, body ? body.clientWidth : 0);
    var height = Math.max(html.scrollHeight, html.clientHeight, body ? body.scrollHeight : 0, body ? body.clientHeight : 0);
    var x = -winScroll.scrollLeft + _getWindowScrollBarXJsDefault.default(element);
    var y = -winScroll.scrollTop;
    if (_getComputedStyleJsDefault.default(body || html).direction === 'rtl') x += Math.max(html.clientWidth, body ? body.clientWidth : 0) - width;
    return {
        width: width,
        height: height,
        x: x,
        y: y
    };
}
exports.default = getDocumentRect;

},{"./getDocumentElement.js":"ltWTM","./getComputedStyle.js":"k2rR5","./getWindowScrollBarX.js":"9hIdB","./getWindowScroll.js":"i6J1Y","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"iUMbF":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function contains(parent, child) {
    // $FlowFixMe: hasOwnProperty doesn't seem to work in tests
    var isShadow = Boolean(child.getRootNode && child.getRootNode().host); // First, attempt with faster native method
    if (parent.contains(child)) return true;
    else if (isShadow) {
        var next = child;
        do {
            if (next && parent.isSameNode(next)) return true;
             // $FlowFixMe: need a better way to handle this...
            next = next.parentNode || next.host;
        }while (next)
    } // Give up, the result is false
    return false;
}
exports.default = contains;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"3Nry1":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function rectToClientRect(rect) {
    return Object.assign(Object.assign({}, rect), {}, {
        left: rect.x,
        top: rect.y,
        right: rect.x + rect.width,
        bottom: rect.y + rect.height
    });
}
exports.default = rectToClientRect;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9jIFj":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getBasePlacementJs = require("./getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var _getVariationJs = require("./getVariation.js");
var _getVariationJsDefault = parcelHelpers.interopDefault(_getVariationJs);
var _getMainAxisFromPlacementJs = require("./getMainAxisFromPlacement.js");
var _getMainAxisFromPlacementJsDefault = parcelHelpers.interopDefault(_getMainAxisFromPlacementJs);
var _enumsJs = require("../enums.js");
function computeOffsets(_ref) {
    var reference = _ref.reference, element = _ref.element, placement = _ref.placement;
    var basePlacement = placement ? _getBasePlacementJsDefault.default(placement) : null;
    var variation = placement ? _getVariationJsDefault.default(placement) : null;
    var commonX = reference.x + reference.width / 2 - element.width / 2;
    var commonY = reference.y + reference.height / 2 - element.height / 2;
    var offsets;
    switch(basePlacement){
        case _enumsJs.top:
            offsets = {
                x: commonX,
                y: reference.y - element.height
            };
            break;
        case _enumsJs.bottom:
            offsets = {
                x: commonX,
                y: reference.y + reference.height
            };
            break;
        case _enumsJs.right:
            offsets = {
                x: reference.x + reference.width,
                y: commonY
            };
            break;
        case _enumsJs.left:
            offsets = {
                x: reference.x - element.width,
                y: commonY
            };
            break;
        default:
            offsets = {
                x: reference.x,
                y: reference.y
            };
    }
    var mainAxis = basePlacement ? _getMainAxisFromPlacementJsDefault.default(basePlacement) : null;
    if (mainAxis != null) {
        var len = mainAxis === 'y' ? 'height' : 'width';
        switch(variation){
            case _enumsJs.start:
                offsets[mainAxis] = Math.floor(offsets[mainAxis]) - Math.floor(reference[len] / 2 - element[len] / 2);
                break;
            case _enumsJs.end:
                offsets[mainAxis] = Math.floor(offsets[mainAxis]) + Math.ceil(reference[len] / 2 - element[len] / 2);
                break;
            default:
        }
    }
    return offsets;
}
exports.default = computeOffsets;

},{"./getBasePlacement.js":"c3ZMV","./getVariation.js":"8GAE6","./getMainAxisFromPlacement.js":"60uJ4","../enums.js":"daeOT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"8GAE6":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getVariation(placement) {
    return placement.split('-')[1];
}
exports.default = getVariation;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"60uJ4":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getMainAxisFromPlacement(placement) {
    return [
        'top',
        'bottom'
    ].indexOf(placement) >= 0 ? 'x' : 'y';
}
exports.default = getMainAxisFromPlacement;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"cq9Cu":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getFreshSideObjectJs = require("./getFreshSideObject.js");
var _getFreshSideObjectJsDefault = parcelHelpers.interopDefault(_getFreshSideObjectJs);
function mergePaddingObject(paddingObject) {
    return Object.assign(Object.assign({}, _getFreshSideObjectJsDefault.default()), paddingObject);
}
exports.default = mergePaddingObject;

},{"./getFreshSideObject.js":"1S23V","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"1S23V":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getFreshSideObject() {
    return {
        top: 0,
        right: 0,
        bottom: 0,
        left: 0
    };
}
exports.default = getFreshSideObject;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bHci0":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function expandToHashMap(value, keys) {
    return keys.reduce(function(hashMap, key) {
        hashMap[key] = value;
        return hashMap;
    }, {});
}
exports.default = expandToHashMap;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bGFH1":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getWindowJs = require("../dom-utils/getWindow.js"); // eslint-disable-next-line import/no-unused-modules
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
var passive = {
    passive: true
};
function effect(_ref) {
    var state = _ref.state, instance = _ref.instance, options = _ref.options;
    var _options$scroll = options.scroll, scroll = _options$scroll === void 0 ? true : _options$scroll, _options$resize = options.resize, resize = _options$resize === void 0 ? true : _options$resize;
    var window = _getWindowJsDefault.default(state.elements.popper);
    var scrollParents = [].concat(state.scrollParents.reference, state.scrollParents.popper);
    if (scroll) scrollParents.forEach(function(scrollParent) {
        scrollParent.addEventListener('scroll', instance.update, passive);
    });
    if (resize) window.addEventListener('resize', instance.update, passive);
    return function() {
        if (scroll) scrollParents.forEach(function(scrollParent) {
            scrollParent.removeEventListener('scroll', instance.update, passive);
        });
        if (resize) window.removeEventListener('resize', instance.update, passive);
    };
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'eventListeners',
    enabled: true,
    phase: 'write',
    fn: function fn() {},
    effect: effect,
    data: {}
};

},{"../dom-utils/getWindow.js":"4BVw2","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"gx0If":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _computeOffsetsJs = require("../utils/computeOffsets.js");
var _computeOffsetsJsDefault = parcelHelpers.interopDefault(_computeOffsetsJs);
function popperOffsets(_ref) {
    var state = _ref.state, name = _ref.name;
    // Offsets are the actual position the popper needs to have to be
    // properly positioned near its reference element
    // This is the most basic placement, and will be adjusted by
    // the modifiers in the next step
    state.modifiersData[name] = _computeOffsetsJsDefault.default({
        reference: state.rects.reference,
        element: state.rects.popper,
        strategy: 'absolute',
        placement: state.placement
    });
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'popperOffsets',
    enabled: true,
    phase: 'read',
    fn: popperOffsets,
    data: {}
};

},{"../utils/computeOffsets.js":"9jIFj","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jLSZu":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "mapToStyles", function() {
    return mapToStyles;
});
var _enumsJs = require("../enums.js");
var _getOffsetParentJs = require("../dom-utils/getOffsetParent.js");
var _getOffsetParentJsDefault = parcelHelpers.interopDefault(_getOffsetParentJs);
var _getWindowJs = require("../dom-utils/getWindow.js");
var _getWindowJsDefault = parcelHelpers.interopDefault(_getWindowJs);
var _getDocumentElementJs = require("../dom-utils/getDocumentElement.js");
var _getDocumentElementJsDefault = parcelHelpers.interopDefault(_getDocumentElementJs);
var _getComputedStyleJs = require("../dom-utils/getComputedStyle.js");
var _getComputedStyleJsDefault = parcelHelpers.interopDefault(_getComputedStyleJs);
var _getBasePlacementJs = require("../utils/getBasePlacement.js"); // eslint-disable-next-line import/no-unused-modules
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var unsetSides = {
    top: 'auto',
    right: 'auto',
    bottom: 'auto',
    left: 'auto'
}; // Round the offsets to the nearest suitable subpixel based on the DPR.
// Zooming can change the DPR, but it seems to report a value that will
// cleanly divide the values into the appropriate subpixels.
function roundOffsets(_ref) {
    var x = _ref.x, y = _ref.y;
    var win = window;
    var dpr = win.devicePixelRatio || 1;
    return {
        x: Math.round(x * dpr) / dpr || 0,
        y: Math.round(y * dpr) / dpr || 0
    };
}
function mapToStyles(_ref2) {
    var _Object$assign2;
    var popper = _ref2.popper, popperRect = _ref2.popperRect, placement = _ref2.placement, offsets = _ref2.offsets, position = _ref2.position, gpuAcceleration = _ref2.gpuAcceleration, adaptive = _ref2.adaptive;
    var _roundOffsets = roundOffsets(offsets), x = _roundOffsets.x, y = _roundOffsets.y;
    var hasX = offsets.hasOwnProperty('x');
    var hasY = offsets.hasOwnProperty('y');
    var sideX = _enumsJs.left;
    var sideY = _enumsJs.top;
    var win = window;
    if (adaptive) {
        var offsetParent = _getOffsetParentJsDefault.default(popper);
        if (offsetParent === _getWindowJsDefault.default(popper)) offsetParent = _getDocumentElementJsDefault.default(popper);
         // $FlowFixMe: force type refinement, we compare offsetParent with window above, but Flow doesn't detect it
        /*:: offsetParent = (offsetParent: Element); */ if (placement === _enumsJs.top) {
            sideY = _enumsJs.bottom;
            y -= offsetParent.clientHeight - popperRect.height;
            y *= gpuAcceleration ? 1 : -1;
        }
        if (placement === _enumsJs.left) {
            sideX = _enumsJs.right;
            x -= offsetParent.clientWidth - popperRect.width;
            x *= gpuAcceleration ? 1 : -1;
        }
    }
    var commonStyles = Object.assign({
        position: position
    }, adaptive && unsetSides);
    if (gpuAcceleration) {
        var _Object$assign;
        return Object.assign(Object.assign({}, commonStyles), {}, (_Object$assign = {}, _Object$assign[sideY] = hasY ? '0' : '', _Object$assign[sideX] = hasX ? '0' : '', _Object$assign.transform = (win.devicePixelRatio || 1) < 2 ? "translate(" + x + "px, " + y + "px)" : "translate3d(" + x + "px, " + y + "px, 0)", _Object$assign));
    }
    return Object.assign(Object.assign({}, commonStyles), {}, (_Object$assign2 = {}, _Object$assign2[sideY] = hasY ? y + "px" : '', _Object$assign2[sideX] = hasX ? x + "px" : '', _Object$assign2.transform = '', _Object$assign2));
}
function computeStyles(_ref3) {
    var state = _ref3.state, options = _ref3.options;
    var _options$gpuAccelerat = options.gpuAcceleration, gpuAcceleration = _options$gpuAccelerat === void 0 ? true : _options$gpuAccelerat, _options$adaptive = options.adaptive, adaptive = _options$adaptive === void 0 ? true : _options$adaptive;
    var transitionProperty = _getComputedStyleJsDefault.default(state.elements.popper).transitionProperty || '';
    if (adaptive && [
        'transform',
        'top',
        'right',
        'bottom',
        'left'
    ].some(function(property) {
        return transitionProperty.indexOf(property) >= 0;
    })) console.warn([
        'Popper: Detected CSS transitions on at least one of the following',
        'CSS properties: "transform", "top", "right", "bottom", "left".',
        '\n\n',
        'Disable the "computeStyles" modifier\'s `adaptive` option to allow',
        'for smooth transitions, or remove these properties from the CSS',
        'transition declaration on the popper element if only transitioning',
        'opacity or background-color for example.',
        '\n\n',
        'We recommend using the popper element as a wrapper around an inner',
        'element that can have any CSS property transitioned for animations.'
    ].join(' '));
    var commonStyles = {
        placement: _getBasePlacementJsDefault.default(state.placement),
        popper: state.elements.popper,
        popperRect: state.rects.popper,
        gpuAcceleration: gpuAcceleration
    };
    if (state.modifiersData.popperOffsets != null) state.styles.popper = Object.assign(Object.assign({}, state.styles.popper), mapToStyles(Object.assign(Object.assign({}, commonStyles), {}, {
        offsets: state.modifiersData.popperOffsets,
        position: state.options.strategy,
        adaptive: adaptive
    })));
    if (state.modifiersData.arrow != null) state.styles.arrow = Object.assign(Object.assign({}, state.styles.arrow), mapToStyles(Object.assign(Object.assign({}, commonStyles), {}, {
        offsets: state.modifiersData.arrow,
        position: 'absolute',
        adaptive: false
    })));
    state.attributes.popper = Object.assign(Object.assign({}, state.attributes.popper), {}, {
        'data-popper-placement': state.placement
    });
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'computeStyles',
    enabled: true,
    phase: 'beforeWrite',
    fn: computeStyles,
    data: {}
};

},{"../enums.js":"daeOT","../dom-utils/getOffsetParent.js":"apRsT","../dom-utils/getWindow.js":"4BVw2","../dom-utils/getDocumentElement.js":"ltWTM","../dom-utils/getComputedStyle.js":"k2rR5","../utils/getBasePlacement.js":"c3ZMV","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hz8MT":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getNodeNameJs = require("../dom-utils/getNodeName.js");
var _getNodeNameJsDefault = parcelHelpers.interopDefault(_getNodeNameJs);
var _instanceOfJs = require("../dom-utils/instanceOf.js"); // This modifier takes the styles prepared by the `computeStyles` modifier
// and applies them to the HTMLElements such as popper and arrow
function applyStyles(_ref) {
    var state = _ref.state;
    Object.keys(state.elements).forEach(function(name1) {
        var style = state.styles[name1] || {};
        var attributes = state.attributes[name1] || {};
        var element = state.elements[name1]; // arrow is optional + virtual elements
        if (!_instanceOfJs.isHTMLElement(element) || !_getNodeNameJsDefault.default(element)) return;
         // Flow doesn't support to extend this property, but it's the most
        // effective way to apply styles to an HTMLElement
        // $FlowFixMe
        Object.assign(element.style, style);
        Object.keys(attributes).forEach(function(name) {
            var value = attributes[name];
            if (value === false) element.removeAttribute(name);
            else element.setAttribute(name, value === true ? '' : value);
        });
    });
}
function effect(_ref2) {
    var state = _ref2.state;
    var initialStyles = {
        popper: {
            position: state.options.strategy,
            left: '0',
            top: '0',
            margin: '0'
        },
        arrow: {
            position: 'absolute'
        },
        reference: {}
    };
    Object.assign(state.elements.popper.style, initialStyles.popper);
    if (state.elements.arrow) Object.assign(state.elements.arrow.style, initialStyles.arrow);
    return function() {
        Object.keys(state.elements).forEach(function(name) {
            var element = state.elements[name];
            var attributes = state.attributes[name] || {};
            var styleProperties = Object.keys(state.styles.hasOwnProperty(name) ? state.styles[name] : initialStyles[name]); // Set all values to an empty string to unset them
            var style1 = styleProperties.reduce(function(style, property) {
                style[property] = '';
                return style;
            }, {}); // arrow is optional + virtual elements
            if (!_instanceOfJs.isHTMLElement(element) || !_getNodeNameJsDefault.default(element)) return;
             // Flow doesn't support to extend this property, but it's the most
            // effective way to apply styles to an HTMLElement
            // $FlowFixMe
            Object.assign(element.style, style1);
            Object.keys(attributes).forEach(function(attribute) {
                element.removeAttribute(attribute);
            });
        });
    };
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'applyStyles',
    enabled: true,
    phase: 'write',
    fn: applyStyles,
    effect: effect,
    requires: [
        'computeStyles'
    ]
};

},{"../dom-utils/getNodeName.js":"92CvH","../dom-utils/instanceOf.js":"9bvfh","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"ei7o5":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "distanceAndSkiddingToXY", function() {
    return distanceAndSkiddingToXY;
});
var _getBasePlacementJs = require("../utils/getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var _enumsJs = require("../enums.js");
function distanceAndSkiddingToXY(placement, rects, offset1) {
    var basePlacement = _getBasePlacementJsDefault.default(placement);
    var invertDistance = [
        _enumsJs.left,
        _enumsJs.top
    ].indexOf(basePlacement) >= 0 ? -1 : 1;
    var _ref = typeof offset1 === 'function' ? offset1(Object.assign(Object.assign({}, rects), {}, {
        placement: placement
    })) : offset1, skidding = _ref[0], distance = _ref[1];
    skidding = skidding || 0;
    distance = (distance || 0) * invertDistance;
    return [
        _enumsJs.left,
        _enumsJs.right
    ].indexOf(basePlacement) >= 0 ? {
        x: distance,
        y: skidding
    } : {
        x: skidding,
        y: distance
    };
}
function offset(_ref2) {
    var state = _ref2.state, options = _ref2.options, name = _ref2.name;
    var _options$offset = options.offset, _$offset = _options$offset === void 0 ? [
        0,
        0
    ] : _options$offset;
    var data = _enumsJs.placements.reduce(function(acc, placement) {
        acc[placement] = distanceAndSkiddingToXY(placement, state.rects, _$offset);
        return acc;
    }, {});
    var _data$state$placement = data[state.placement], x = _data$state$placement.x, y = _data$state$placement.y;
    if (state.modifiersData.popperOffsets != null) {
        state.modifiersData.popperOffsets.x += x;
        state.modifiersData.popperOffsets.y += y;
    }
    state.modifiersData[name] = data;
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'offset',
    enabled: true,
    phase: 'main',
    requires: [
        'popperOffsets'
    ],
    fn: offset
};

},{"../utils/getBasePlacement.js":"c3ZMV","../enums.js":"daeOT","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"iuE8D":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getOppositePlacementJs = require("../utils/getOppositePlacement.js");
var _getOppositePlacementJsDefault = parcelHelpers.interopDefault(_getOppositePlacementJs);
var _getBasePlacementJs = require("../utils/getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var _getOppositeVariationPlacementJs = require("../utils/getOppositeVariationPlacement.js");
var _getOppositeVariationPlacementJsDefault = parcelHelpers.interopDefault(_getOppositeVariationPlacementJs);
var _detectOverflowJs = require("../utils/detectOverflow.js");
var _detectOverflowJsDefault = parcelHelpers.interopDefault(_detectOverflowJs);
var _computeAutoPlacementJs = require("../utils/computeAutoPlacement.js");
var _computeAutoPlacementJsDefault = parcelHelpers.interopDefault(_computeAutoPlacementJs);
var _enumsJs = require("../enums.js");
var _getVariationJs = require("../utils/getVariation.js"); // eslint-disable-next-line import/no-unused-modules
var _getVariationJsDefault = parcelHelpers.interopDefault(_getVariationJs);
function getExpandedFallbackPlacements(placement) {
    if (_getBasePlacementJsDefault.default(placement) === _enumsJs.auto) return [];
    var oppositePlacement = _getOppositePlacementJsDefault.default(placement);
    return [
        _getOppositeVariationPlacementJsDefault.default(placement),
        oppositePlacement,
        _getOppositeVariationPlacementJsDefault.default(oppositePlacement)
    ];
}
function flip(_ref) {
    var state = _ref.state, options = _ref.options, name = _ref.name;
    if (state.modifiersData[name]._skip) return;
    var _options$mainAxis = options.mainAxis, checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis, _options$altAxis = options.altAxis, checkAltAxis = _options$altAxis === void 0 ? true : _options$altAxis, specifiedFallbackPlacements = options.fallbackPlacements, padding = options.padding, boundary = options.boundary, rootBoundary = options.rootBoundary, altBoundary = options.altBoundary, _options$flipVariatio = options.flipVariations, flipVariations = _options$flipVariatio === void 0 ? true : _options$flipVariatio, allowedAutoPlacements = options.allowedAutoPlacements;
    var preferredPlacement = state.options.placement;
    var basePlacement = _getBasePlacementJsDefault.default(preferredPlacement);
    var isBasePlacement = basePlacement === preferredPlacement;
    var fallbackPlacements = specifiedFallbackPlacements || (isBasePlacement || !flipVariations ? [
        _getOppositePlacementJsDefault.default(preferredPlacement)
    ] : getExpandedFallbackPlacements(preferredPlacement));
    var placements = [
        preferredPlacement
    ].concat(fallbackPlacements).reduce(function(acc, placement) {
        return acc.concat(_getBasePlacementJsDefault.default(placement) === _enumsJs.auto ? _computeAutoPlacementJsDefault.default(state, {
            placement: placement,
            boundary: boundary,
            rootBoundary: rootBoundary,
            padding: padding,
            flipVariations: flipVariations,
            allowedAutoPlacements: allowedAutoPlacements
        }) : placement);
    }, []);
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var checksMap = new Map();
    var makeFallbackChecks = true;
    var firstFittingPlacement = placements[0];
    for(var i = 0; i < placements.length; i++){
        var placement1 = placements[i];
        var _basePlacement = _getBasePlacementJsDefault.default(placement1);
        var isStartVariation = _getVariationJsDefault.default(placement1) === _enumsJs.start;
        var isVertical = [
            _enumsJs.top,
            _enumsJs.bottom
        ].indexOf(_basePlacement) >= 0;
        var len = isVertical ? 'width' : 'height';
        var overflow = _detectOverflowJsDefault.default(state, {
            placement: placement1,
            boundary: boundary,
            rootBoundary: rootBoundary,
            altBoundary: altBoundary,
            padding: padding
        });
        var mainVariationSide = isVertical ? isStartVariation ? _enumsJs.right : _enumsJs.left : isStartVariation ? _enumsJs.bottom : _enumsJs.top;
        if (referenceRect[len] > popperRect[len]) mainVariationSide = _getOppositePlacementJsDefault.default(mainVariationSide);
        var altVariationSide = _getOppositePlacementJsDefault.default(mainVariationSide);
        var checks = [];
        if (checkMainAxis) checks.push(overflow[_basePlacement] <= 0);
        if (checkAltAxis) checks.push(overflow[mainVariationSide] <= 0, overflow[altVariationSide] <= 0);
        if (checks.every(function(check) {
            return check;
        })) {
            firstFittingPlacement = placement1;
            makeFallbackChecks = false;
            break;
        }
        checksMap.set(placement1, checks);
    }
    if (makeFallbackChecks) {
        // `2` may be desired in some cases – research later
        var numberOfChecks = flipVariations ? 3 : 1;
        var _loop = function _loop(_i) {
            var fittingPlacement = placements.find(function(placement) {
                var checks = checksMap.get(placement);
                if (checks) return checks.slice(0, _i).every(function(check) {
                    return check;
                });
            });
            if (fittingPlacement) {
                firstFittingPlacement = fittingPlacement;
                return "break";
            }
        };
        for(var _i1 = numberOfChecks; _i1 > 0; _i1--){
            var _ret = _loop(_i1);
            if (_ret === "break") break;
        }
    }
    if (state.placement !== firstFittingPlacement) {
        state.modifiersData[name]._skip = true;
        state.placement = firstFittingPlacement;
        state.reset = true;
    }
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'flip',
    enabled: true,
    phase: 'main',
    fn: flip,
    requiresIfExists: [
        'offset'
    ],
    data: {
        _skip: false
    }
};

},{"../utils/getOppositePlacement.js":"fHT0T","../utils/getBasePlacement.js":"c3ZMV","../utils/getOppositeVariationPlacement.js":"jpe4f","../utils/detectOverflow.js":"gNzja","../utils/computeAutoPlacement.js":"1g43a","../enums.js":"daeOT","../utils/getVariation.js":"8GAE6","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"fHT0T":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var hash = {
    left: 'right',
    right: 'left',
    bottom: 'top',
    top: 'bottom'
};
function getOppositePlacement(placement) {
    return placement.replace(/left|right|bottom|top/g, function(matched) {
        return hash[matched];
    });
}
exports.default = getOppositePlacement;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"jpe4f":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var hash = {
    start: 'end',
    end: 'start'
};
function getOppositeVariationPlacement(placement) {
    return placement.replace(/start|end/g, function(matched) {
        return hash[matched];
    });
}
exports.default = getOppositeVariationPlacement;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"1g43a":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getVariationJs = require("./getVariation.js");
var _getVariationJsDefault = parcelHelpers.interopDefault(_getVariationJs);
var _enumsJs = require("../enums.js");
var _detectOverflowJs = require("./detectOverflow.js");
var _detectOverflowJsDefault = parcelHelpers.interopDefault(_detectOverflowJs);
var _getBasePlacementJs = require("./getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
function computeAutoPlacement(state, options) {
    if (options === void 0) options = {};
    var _options = options, placement1 = _options.placement, boundary = _options.boundary, rootBoundary = _options.rootBoundary, padding = _options.padding, flipVariations = _options.flipVariations, _options$allowedAutoP = _options.allowedAutoPlacements, allowedAutoPlacements = _options$allowedAutoP === void 0 ? _enumsJs.placements : _options$allowedAutoP;
    var variation = _getVariationJsDefault.default(placement1);
    var placements = variation ? flipVariations ? _enumsJs.variationPlacements : _enumsJs.variationPlacements.filter(function(placement) {
        return _getVariationJsDefault.default(placement) === variation;
    }) : _enumsJs.basePlacements; // $FlowFixMe
    var allowedPlacements = placements.filter(function(placement) {
        return allowedAutoPlacements.indexOf(placement) >= 0;
    });
    if (allowedPlacements.length === 0) {
        allowedPlacements = placements;
        console.error([
            'Popper: The `allowedAutoPlacements` option did not allow any',
            'placements. Ensure the `placement` option matches the variation',
            'of the allowed placements.',
            'For example, "auto" cannot be used to allow "bottom-start".',
            'Use "auto-start" instead.'
        ].join(' '));
    } // $FlowFixMe: Flow seems to have problems with two array unions...
    var overflows = allowedPlacements.reduce(function(acc, placement) {
        acc[placement] = _detectOverflowJsDefault.default(state, {
            placement: placement,
            boundary: boundary,
            rootBoundary: rootBoundary,
            padding: padding
        })[_getBasePlacementJsDefault.default(placement)];
        return acc;
    }, {});
    return Object.keys(overflows).sort(function(a, b) {
        return overflows[a] - overflows[b];
    });
}
exports.default = computeAutoPlacement;

},{"./getVariation.js":"8GAE6","../enums.js":"daeOT","./detectOverflow.js":"gNzja","./getBasePlacement.js":"c3ZMV","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"4F5cZ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _enumsJs = require("../enums.js");
var _getBasePlacementJs = require("../utils/getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var _getMainAxisFromPlacementJs = require("../utils/getMainAxisFromPlacement.js");
var _getMainAxisFromPlacementJsDefault = parcelHelpers.interopDefault(_getMainAxisFromPlacementJs);
var _getAltAxisJs = require("../utils/getAltAxis.js");
var _getAltAxisJsDefault = parcelHelpers.interopDefault(_getAltAxisJs);
var _withinJs = require("../utils/within.js");
var _withinJsDefault = parcelHelpers.interopDefault(_withinJs);
var _getLayoutRectJs = require("../dom-utils/getLayoutRect.js");
var _getLayoutRectJsDefault = parcelHelpers.interopDefault(_getLayoutRectJs);
var _getOffsetParentJs = require("../dom-utils/getOffsetParent.js");
var _getOffsetParentJsDefault = parcelHelpers.interopDefault(_getOffsetParentJs);
var _detectOverflowJs = require("../utils/detectOverflow.js");
var _detectOverflowJsDefault = parcelHelpers.interopDefault(_detectOverflowJs);
var _getVariationJs = require("../utils/getVariation.js");
var _getVariationJsDefault = parcelHelpers.interopDefault(_getVariationJs);
var _getFreshSideObjectJs = require("../utils/getFreshSideObject.js");
var _getFreshSideObjectJsDefault = parcelHelpers.interopDefault(_getFreshSideObjectJs);
function preventOverflow(_ref) {
    var state = _ref.state, options = _ref.options, name = _ref.name;
    var _options$mainAxis = options.mainAxis, checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis, _options$altAxis = options.altAxis, checkAltAxis = _options$altAxis === void 0 ? false : _options$altAxis, boundary = options.boundary, rootBoundary = options.rootBoundary, altBoundary = options.altBoundary, padding = options.padding, _options$tether = options.tether, tether = _options$tether === void 0 ? true : _options$tether, _options$tetherOffset = options.tetherOffset, tetherOffset = _options$tetherOffset === void 0 ? 0 : _options$tetherOffset;
    var overflow = _detectOverflowJsDefault.default(state, {
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding,
        altBoundary: altBoundary
    });
    var basePlacement = _getBasePlacementJsDefault.default(state.placement);
    var variation = _getVariationJsDefault.default(state.placement);
    var isBasePlacement = !variation;
    var mainAxis = _getMainAxisFromPlacementJsDefault.default(basePlacement);
    var altAxis = _getAltAxisJsDefault.default(mainAxis);
    var popperOffsets = state.modifiersData.popperOffsets;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var tetherOffsetValue = typeof tetherOffset === 'function' ? tetherOffset(Object.assign(Object.assign({}, state.rects), {}, {
        placement: state.placement
    })) : tetherOffset;
    var data = {
        x: 0,
        y: 0
    };
    if (!popperOffsets) return;
    if (checkMainAxis) {
        var mainSide = mainAxis === 'y' ? _enumsJs.top : _enumsJs.left;
        var altSide = mainAxis === 'y' ? _enumsJs.bottom : _enumsJs.right;
        var len = mainAxis === 'y' ? 'height' : 'width';
        var offset = popperOffsets[mainAxis];
        var min = popperOffsets[mainAxis] + overflow[mainSide];
        var max = popperOffsets[mainAxis] - overflow[altSide];
        var additive = tether ? -popperRect[len] / 2 : 0;
        var minLen = variation === _enumsJs.start ? referenceRect[len] : popperRect[len];
        var maxLen = variation === _enumsJs.start ? -popperRect[len] : -referenceRect[len]; // We need to include the arrow in the calculation so the arrow doesn't go
        // outside the reference bounds
        var arrowElement = state.elements.arrow;
        var arrowRect = tether && arrowElement ? _getLayoutRectJsDefault.default(arrowElement) : {
            width: 0,
            height: 0
        };
        var arrowPaddingObject = state.modifiersData['arrow#persistent'] ? state.modifiersData['arrow#persistent'].padding : _getFreshSideObjectJsDefault.default();
        var arrowPaddingMin = arrowPaddingObject[mainSide];
        var arrowPaddingMax = arrowPaddingObject[altSide]; // If the reference length is smaller than the arrow length, we don't want
        // to include its full size in the calculation. If the reference is small
        // and near the edge of a boundary, the popper can overflow even if the
        // reference is not overflowing as well (e.g. virtual elements with no
        // width or height)
        var arrowLen = _withinJsDefault.default(0, referenceRect[len], arrowRect[len]);
        var minOffset = isBasePlacement ? referenceRect[len] / 2 - additive - arrowLen - arrowPaddingMin - tetherOffsetValue : minLen - arrowLen - arrowPaddingMin - tetherOffsetValue;
        var maxOffset = isBasePlacement ? -referenceRect[len] / 2 + additive + arrowLen + arrowPaddingMax + tetherOffsetValue : maxLen + arrowLen + arrowPaddingMax + tetherOffsetValue;
        var arrowOffsetParent = state.elements.arrow && _getOffsetParentJsDefault.default(state.elements.arrow);
        var clientOffset = arrowOffsetParent ? mainAxis === 'y' ? arrowOffsetParent.clientTop || 0 : arrowOffsetParent.clientLeft || 0 : 0;
        var offsetModifierValue = state.modifiersData.offset ? state.modifiersData.offset[state.placement][mainAxis] : 0;
        var tetherMin = popperOffsets[mainAxis] + minOffset - offsetModifierValue - clientOffset;
        var tetherMax = popperOffsets[mainAxis] + maxOffset - offsetModifierValue;
        var preventedOffset = _withinJsDefault.default(tether ? Math.min(min, tetherMin) : min, offset, tether ? Math.max(max, tetherMax) : max);
        popperOffsets[mainAxis] = preventedOffset;
        data[mainAxis] = preventedOffset - offset;
    }
    if (checkAltAxis) {
        var _mainSide = mainAxis === 'x' ? _enumsJs.top : _enumsJs.left;
        var _altSide = mainAxis === 'x' ? _enumsJs.bottom : _enumsJs.right;
        var _offset = popperOffsets[altAxis];
        var _min = _offset + overflow[_mainSide];
        var _max = _offset - overflow[_altSide];
        var _preventedOffset = _withinJsDefault.default(_min, _offset, _max);
        popperOffsets[altAxis] = _preventedOffset;
        data[altAxis] = _preventedOffset - _offset;
    }
    state.modifiersData[name] = data;
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'preventOverflow',
    enabled: true,
    phase: 'main',
    fn: preventOverflow,
    requiresIfExists: [
        'offset'
    ]
};

},{"../enums.js":"daeOT","../utils/getBasePlacement.js":"c3ZMV","../utils/getMainAxisFromPlacement.js":"60uJ4","../utils/getAltAxis.js":"9Kk5X","../utils/within.js":"2TtiZ","../dom-utils/getLayoutRect.js":"bb9Mh","../dom-utils/getOffsetParent.js":"apRsT","../utils/detectOverflow.js":"gNzja","../utils/getVariation.js":"8GAE6","../utils/getFreshSideObject.js":"1S23V","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"9Kk5X":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function getAltAxis(axis) {
    return axis === 'x' ? 'y' : 'x';
}
exports.default = getAltAxis;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"2TtiZ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function within(min, value, max) {
    return Math.max(min, Math.min(value, max));
}
exports.default = within;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"3355Z":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _getBasePlacementJs = require("../utils/getBasePlacement.js");
var _getBasePlacementJsDefault = parcelHelpers.interopDefault(_getBasePlacementJs);
var _getLayoutRectJs = require("../dom-utils/getLayoutRect.js");
var _getLayoutRectJsDefault = parcelHelpers.interopDefault(_getLayoutRectJs);
var _containsJs = require("../dom-utils/contains.js");
var _containsJsDefault = parcelHelpers.interopDefault(_containsJs);
var _getOffsetParentJs = require("../dom-utils/getOffsetParent.js");
var _getOffsetParentJsDefault = parcelHelpers.interopDefault(_getOffsetParentJs);
var _getMainAxisFromPlacementJs = require("../utils/getMainAxisFromPlacement.js");
var _getMainAxisFromPlacementJsDefault = parcelHelpers.interopDefault(_getMainAxisFromPlacementJs);
var _withinJs = require("../utils/within.js");
var _withinJsDefault = parcelHelpers.interopDefault(_withinJs);
var _mergePaddingObjectJs = require("../utils/mergePaddingObject.js");
var _mergePaddingObjectJsDefault = parcelHelpers.interopDefault(_mergePaddingObjectJs);
var _expandToHashMapJs = require("../utils/expandToHashMap.js");
var _expandToHashMapJsDefault = parcelHelpers.interopDefault(_expandToHashMapJs);
var _enumsJs = require("../enums.js");
var _instanceOfJs = require("../dom-utils/instanceOf.js"); // eslint-disable-next-line import/no-unused-modules
function arrow(_ref) {
    var _state$modifiersData$;
    var state = _ref.state, name = _ref.name;
    var arrowElement = state.elements.arrow;
    var popperOffsets = state.modifiersData.popperOffsets;
    var basePlacement = _getBasePlacementJsDefault.default(state.placement);
    var axis = _getMainAxisFromPlacementJsDefault.default(basePlacement);
    var isVertical = [
        _enumsJs.left,
        _enumsJs.right
    ].indexOf(basePlacement) >= 0;
    var len = isVertical ? 'height' : 'width';
    if (!arrowElement || !popperOffsets) return;
    var paddingObject = state.modifiersData[name + "#persistent"].padding;
    var arrowRect = _getLayoutRectJsDefault.default(arrowElement);
    var minProp = axis === 'y' ? _enumsJs.top : _enumsJs.left;
    var maxProp = axis === 'y' ? _enumsJs.bottom : _enumsJs.right;
    var endDiff = state.rects.reference[len] + state.rects.reference[axis] - popperOffsets[axis] - state.rects.popper[len];
    var startDiff = popperOffsets[axis] - state.rects.reference[axis];
    var arrowOffsetParent = _getOffsetParentJsDefault.default(arrowElement);
    var clientSize = arrowOffsetParent ? axis === 'y' ? arrowOffsetParent.clientHeight || 0 : arrowOffsetParent.clientWidth || 0 : 0;
    var centerToReference = endDiff / 2 - startDiff / 2; // Make sure the arrow doesn't overflow the popper if the center point is
    // outside of the popper bounds
    var min = paddingObject[minProp];
    var max = clientSize - arrowRect[len] - paddingObject[maxProp];
    var center = clientSize / 2 - arrowRect[len] / 2 + centerToReference;
    var offset = _withinJsDefault.default(min, center, max); // Prevents breaking syntax highlighting...
    var axisProp = axis;
    state.modifiersData[name] = (_state$modifiersData$ = {}, _state$modifiersData$[axisProp] = offset, _state$modifiersData$.centerOffset = offset - center, _state$modifiersData$);
}
function effect(_ref2) {
    var state = _ref2.state, options = _ref2.options, name = _ref2.name;
    var _options$element = options.element, arrowElement = _options$element === void 0 ? '[data-popper-arrow]' : _options$element, _options$padding = options.padding, padding = _options$padding === void 0 ? 0 : _options$padding;
    if (arrowElement == null) return;
     // CSS selector
    if (typeof arrowElement === 'string') {
        arrowElement = state.elements.popper.querySelector(arrowElement);
        if (!arrowElement) return;
    }
    if (!_instanceOfJs.isHTMLElement(arrowElement)) console.error([
        'Popper: "arrow" element must be an HTMLElement (not an SVGElement).',
        'To use an SVG arrow, wrap it in an HTMLElement that will be used as',
        'the arrow.'
    ].join(' '));
    if (!_containsJsDefault.default(state.elements.popper, arrowElement)) {
        console.error([
            'Popper: "arrow" modifier\'s `element` must be a child of the popper',
            'element.'
        ].join(' '));
        return;
    }
    state.elements.arrow = arrowElement;
    state.modifiersData[name + "#persistent"] = {
        padding: _mergePaddingObjectJsDefault.default(typeof padding !== 'number' ? padding : _expandToHashMapJsDefault.default(padding, _enumsJs.basePlacements))
    };
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'arrow',
    enabled: true,
    phase: 'main',
    fn: arrow,
    effect: effect,
    requires: [
        'popperOffsets'
    ],
    requiresIfExists: [
        'preventOverflow'
    ]
};

},{"../utils/getBasePlacement.js":"c3ZMV","../dom-utils/getLayoutRect.js":"bb9Mh","../dom-utils/contains.js":"iUMbF","../dom-utils/getOffsetParent.js":"apRsT","../utils/getMainAxisFromPlacement.js":"60uJ4","../utils/within.js":"2TtiZ","../utils/mergePaddingObject.js":"cq9Cu","../utils/expandToHashMap.js":"bHci0","../enums.js":"daeOT","../dom-utils/instanceOf.js":"9bvfh","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"bnIFG":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _enumsJs = require("../enums.js");
var _detectOverflowJs = require("../utils/detectOverflow.js");
var _detectOverflowJsDefault = parcelHelpers.interopDefault(_detectOverflowJs);
function getSideOffsets(overflow, rect, preventedOffsets) {
    if (preventedOffsets === void 0) preventedOffsets = {
        x: 0,
        y: 0
    };
    return {
        top: overflow.top - rect.height - preventedOffsets.y,
        right: overflow.right - rect.width + preventedOffsets.x,
        bottom: overflow.bottom - rect.height + preventedOffsets.y,
        left: overflow.left - rect.width - preventedOffsets.x
    };
}
function isAnySideFullyClipped(overflow) {
    return [
        _enumsJs.top,
        _enumsJs.right,
        _enumsJs.bottom,
        _enumsJs.left
    ].some(function(side) {
        return overflow[side] >= 0;
    });
}
function hide(_ref) {
    var state = _ref.state, name = _ref.name;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var preventedOffsets = state.modifiersData.preventOverflow;
    var referenceOverflow = _detectOverflowJsDefault.default(state, {
        elementContext: 'reference'
    });
    var popperAltOverflow = _detectOverflowJsDefault.default(state, {
        altBoundary: true
    });
    var referenceClippingOffsets = getSideOffsets(referenceOverflow, referenceRect);
    var popperEscapeOffsets = getSideOffsets(popperAltOverflow, popperRect, preventedOffsets);
    var isReferenceHidden = isAnySideFullyClipped(referenceClippingOffsets);
    var hasPopperEscaped = isAnySideFullyClipped(popperEscapeOffsets);
    state.modifiersData[name] = {
        referenceClippingOffsets: referenceClippingOffsets,
        popperEscapeOffsets: popperEscapeOffsets,
        isReferenceHidden: isReferenceHidden,
        hasPopperEscaped: hasPopperEscaped
    };
    state.attributes.popper = Object.assign(Object.assign({}, state.attributes.popper), {}, {
        'data-popper-reference-hidden': isReferenceHidden,
        'data-popper-escaped': hasPopperEscaped
    });
} // eslint-disable-next-line import/no-unused-modules
exports.default = {
    name: 'hide',
    enabled: true,
    phase: 'main',
    requiresIfExists: [
        'preventOverflow'
    ],
    fn: hide
};

},{"../enums.js":"daeOT","../utils/detectOverflow.js":"gNzja","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"k6xY9":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _tippyJs = require("tippy.js");
var _tippyJsDefault = parcelHelpers.interopDefault(_tippyJs);
function initQueuesMenu() {
    $("#filter-queues").on("input", function() {
        var txt = $("#filter-queues").val();
        var anyVisible = false;
        $("#queues a").hide(); // queue name
        $("#queues > span").hide();
        $("#queues a").each(function() {
            if ($(this).text().toUpperCase().indexOf(txt.toUpperCase()) != -1) {
                $(this).show();
                anyVisible = true;
            }
        });
        if (!anyVisible) $("#queues > span").show();
    });
    $("#link-queue").removeAttr("href");
    // deliberately written in vanilla JS not jquery
    var queuesMenu = document.getElementById("queues");
    if (!queuesMenu) return;
    queuesMenu.style.display = "block";
    _tippyJsDefault.default("#link-queue", {
        content: queuesMenu,
        allowHTML: true,
        interactive: true,
        animation: "scale-subtle",
        trigger: "click",
        theme: "light",
        placement: "bottom-start",
        arrow: null,
        onShown: function(instance) {
            $("#filter-queues").val("");
            $("#filter-queues").focus();
        }
    });
}
exports.default = initQueuesMenu;

},{"tippy.js":"kxABc","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"eeUXK":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function initFlagListExpanders() {
    var $flagsLists = $(".app-flags--list");
    var chevronSVG = $("#js-chevron-svg").html();
    $flagsLists.each(function() {
        var $flags = $(this).find(".app-flag");
        $flags.each(function(i) {
            if (i > 2) $(this).addClass("app-hidden--force").attr("aria-hidden", true);
        });
        if ($flags.length > 3) {
            var $button = $("<button></button>");
            var $buttonText = $("<span>3 of ".concat($flags.length, "</span>"));
            $button.attr({
                class: "app-flags__expander",
                type: "button",
                "aria-label": "Show more"
            }).append(chevronSVG).append($buttonText);
            $(this).parent().append($button);
        }
    });
    var $flagExpanders = $(".app-flags__expander");
    $flagExpanders.on("click keypress", function(e) {
        $(this).prev() // in the flags list preceding the button
        .find(".app-hidden--force").removeClass("app-hidden--force").attr("aria-hidden", false).addClass("app-flag--animate");
        $(this).attr("aria-hidden", true).hide();
    });
}
exports.default = initFlagListExpanders;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"5LSAo":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _urlSearchParamsPolyfill = require("url-search-params-polyfill");
var _fetchPolyfill = require("fetch-polyfill");
var _autocompleteJs = require("@tarekraafat/autocomplete.js");
var _autocompleteJsDefault = parcelHelpers.interopDefault(_autocompleteJs);
var _liteTokenfieldJs = require("./lite-tokenfield.js");
var _liteTokenfieldJsDefault = parcelHelpers.interopDefault(_liteTokenfieldJs);
function initReviewGood() {
    var progressivelyEnhanceMultipleSelectField = function progressivelyEnhanceMultipleSelectField(element) {
        element.parentElement.classList.add("tokenfield-container");
        var items = [];
        var selected = [];
        for(var i = 0; i < element.options.length; i++){
            var option = element.options.item(i);
            var item = {
                id: option.value,
                name: option.value,
                classes: []
            };
            if (option.selected) selected.push(item);
            items.push(item);
        }
        var tokenField = new _liteTokenfieldJsDefault.default({
            el: element,
            items: items,
            newItems: false,
            addItemOnBlur: true,
            filterSetItems: false,
            addItemsOnPaste: true,
            minChars: 1,
            itemName: element.name,
            setItems: selected,
            keepItemsOrder: false
        });
        tokenField._renderItems();
        tokenField._html.container.id = element.id;
        element.remove();
        return tokenField;
    };
    // make ARS dropdown autocompletable
    var inputElementId = "report_summary";
    var inputElement = document.getElementById(inputElementId);
    if (inputElement) new _autocompleteJsDefault.default({
        trigger: {
            event: [
                "input"
            ]
        },
        data: {
            src: function src() {
                var query = inputElement.value.toLowerCase();
                return fetch("/team/picklists/.json?type=report_summary&name=" + query).then(function(response) {
                    return response.json().then(function(parsed) {
                        return parsed.results.map(function(item) {
                            return {
                                value: item["name"],
                                text: item["text"]
                            };
                        });
                    });
                });
            },
            key: [
                "value"
            ],
            cache: false
        },
        selector: "#" + inputElementId,
        threshold: 1,
        debounce: 300,
        resultsList: {
            render: true,
            element: "table",
            // when version 8 is released we can remove this: https://github.com/TarekRaafat/autoComplete.js/issues/105
            container: function(source) {
                source.setAttribute("id", "autoComplete_list");
                inputElement.addEventListener("autoComplete", function(event) {
                    function hideSearchResults() {
                        var searchResults = document.getElementById("autoComplete_list");
                        while(searchResults.firstChild)searchResults.removeChild(searchResults.firstChild);
                        document.removeEventListener("click", hideSearchResults);
                    }
                    document.addEventListener("click", hideSearchResults);
                });
            }
        },
        resultItem: {
            content: function content(data, source) {
                source.innerHTML = '<td><div class="govuk-heading-s govuk-!-margin-0">' + data.value.value + "</div>" + '<div class="govuk-caption-xs govuk-!-margin-0">' + data.value.text + "</div>" + "</td>";
            },
            element: "tr"
        },
        searchEngine: function searchEngine(query, record) {
            return record;
        },
        onSelection: function(feedback) {
            inputElement.value = feedback.selection.value.text;
        },
        maxResults: 15
    });
    var controlListEntriesField = document.getElementById("control_list_entries");
    var controlRationgField = document.getElementById("control_rating");
    if (!(controlListEntriesField || controlRationgField)) return;
    if (controlRationgField) {
        controlRationgField.style.display = "none";
        progressivelyEnhanceMultipleSelectField(controlRationgField);
    }
    // adding place for "rating may need alternative CLC"
    var controlListEntriesTokenFieldInfo = document.createElement("div");
    controlListEntriesField.parentElement.appendChild(controlListEntriesTokenFieldInfo);
    var controlListEntriesTokenField = progressivelyEnhanceMultipleSelectField(controlListEntriesField);
    // faking the feature so we can get user fedback: for some ratings show the message about alternative CLCs
    controlListEntriesTokenField.on("change", function(tokenField) {
        var note = " may need an alternative control list entry because of its destination";
        var messages = tokenField.getItems().filter(function(item) {
            return item.name.match(/[a-zA-Z]$/) !== null;
        }).map(function(item) {
            return "<div>" + item.name + note + "</div>";
        });
        if (messages.length > 0) controlListEntriesTokenFieldInfo.innerHTML = "<div class='govuk-inset-text'>" + messages.join("") + "</div>";
        else controlListEntriesTokenFieldInfo.innerHTML = "";
    });
}
exports.default = initReviewGood;

},{"url-search-params-polyfill":"hqIuz","fetch-polyfill":"dXUcw","@tarekraafat/autocomplete.js":"fjGnP","./lite-tokenfield.js":"jamAK","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hqIuz":[function(require,module,exports) {
var global = arguments[3];
/**
 *
 *
 * @author Jerry Bendy <jerry@icewingcc.com>
 * @licence MIT
 *
 */ (function(self) {
    var encode = function encode(str) {
        var replace = {
            '!': '%21',
            "'": '%27',
            '(': '%28',
            ')': '%29',
            '~': '%7E',
            '%20': '+',
            '%00': '\x00'
        };
        return encodeURIComponent(str).replace(/[!'\(\)~]|%20|%00/g, function(match) {
            return replace[match];
        });
    };
    var decode = function decode(str) {
        return str.replace(/[ +]/g, '%20').replace(/(%[a-f0-9]{2})+/ig, function(match) {
            return decodeURIComponent(match);
        });
    };
    var makeIterator = function makeIterator(arr) {
        var iterator = {
            next: function next() {
                var value = arr.shift();
                return {
                    done: value === undefined,
                    value: value
                };
            }
        };
        if (iterable) iterator[self.Symbol.iterator] = function() {
            return iterator;
        };
        return iterator;
    };
    var parseToDict = function parseToDict(search) {
        var dict = {};
        if (typeof search === "object") {
            // if `search` is an array, treat it as a sequence
            if (isArray(search)) for(var i = 0; i < search.length; i++){
                var item = search[i];
                if (isArray(item) && item.length === 2) appendTo(dict, item[0], item[1]);
                else throw new TypeError("Failed to construct 'URLSearchParams': Sequence initializer must only contain pair elements");
            }
            else {
                for(var key in search)if (search.hasOwnProperty(key)) appendTo(dict, key, search[key]);
            }
        } else {
            // remove first '?'
            if (search.indexOf("?") === 0) search = search.slice(1);
            var pairs = search.split("&");
            for(var j = 0; j < pairs.length; j++){
                var value = pairs[j], index = value.indexOf('=');
                if (-1 < index) appendTo(dict, decode(value.slice(0, index)), decode(value.slice(index + 1)));
                else if (value) appendTo(dict, decode(value), '');
            }
        }
        return dict;
    };
    var appendTo = function appendTo(dict, name, value) {
        var val = typeof value === 'string' ? value : value !== null && value !== undefined && typeof value.toString === 'function' ? value.toString() : JSON.stringify(value);
        // #47 Prevent using `hasOwnProperty` as a property name
        if (hasOwnProperty(dict, name)) dict[name].push(val);
        else dict[name] = [
            val
        ];
    };
    var isArray = function isArray(val) {
        return !!val && '[object Array]' === Object.prototype.toString.call(val);
    };
    var hasOwnProperty = function hasOwnProperty(obj, prop) {
        return Object.prototype.hasOwnProperty.call(obj, prop);
    };
    var nativeURLSearchParams = function() {
        // #41 Fix issue in RN
        try {
            if (self.URLSearchParams && new self.URLSearchParams('foo=bar').get('foo') === 'bar') return self.URLSearchParams;
        } catch (e) {}
        return null;
    }(), isSupportObjectConstructor = nativeURLSearchParams && new nativeURLSearchParams({
        a: 1
    }).toString() === 'a=1', // There is a bug in safari 10.1 (and earlier) that incorrectly decodes `%2B` as an empty space and not a plus.
    decodesPlusesCorrectly = nativeURLSearchParams && new nativeURLSearchParams('s=%2B').get('s') === '+', __URLSearchParams__ = "__URLSearchParams__", // Fix bug in Edge which cannot encode ' &' correctly
    encodesAmpersandsCorrectly = nativeURLSearchParams ? function() {
        var ampersandTest = new nativeURLSearchParams();
        ampersandTest.append('s', ' &');
        return ampersandTest.toString() === 's=+%26';
    }() : true, prototype = URLSearchParamsPolyfill.prototype, iterable = !!(self.Symbol && self.Symbol.iterator);
    if (nativeURLSearchParams && isSupportObjectConstructor && decodesPlusesCorrectly && encodesAmpersandsCorrectly) return;
    /**
     * Make a URLSearchParams instance
     *
     * @param {object|string|URLSearchParams} search
     * @constructor
     */ function URLSearchParamsPolyfill(search) {
        search = search || "";
        // support construct object with another URLSearchParams instance
        if (search instanceof URLSearchParams || search instanceof URLSearchParamsPolyfill) search = search.toString();
        this[__URLSearchParams__] = parseToDict(search);
    }
    /**
     * Appends a specified key/value pair as a new search parameter.
     *
     * @param {string} name
     * @param {string} value
     */ prototype.append = function(name, value) {
        appendTo(this[__URLSearchParams__], name, value);
    };
    /**
     * Deletes the given search parameter, and its associated value,
     * from the list of all search parameters.
     *
     * @param {string} name
     */ prototype['delete'] = function(name) {
        delete this[__URLSearchParams__][name];
    };
    /**
     * Returns the first value associated to the given search parameter.
     *
     * @param {string} name
     * @returns {string|null}
     */ prototype.get = function(name) {
        var dict = this[__URLSearchParams__];
        return this.has(name) ? dict[name][0] : null;
    };
    /**
     * Returns all the values association with a given search parameter.
     *
     * @param {string} name
     * @returns {Array}
     */ prototype.getAll = function(name) {
        var dict = this[__URLSearchParams__];
        return this.has(name) ? dict[name].slice(0) : [];
    };
    /**
     * Returns a Boolean indicating if such a search parameter exists.
     *
     * @param {string} name
     * @returns {boolean}
     */ prototype.has = function(name) {
        return hasOwnProperty(this[__URLSearchParams__], name);
    };
    /**
     * Sets the value associated to a given search parameter to
     * the given value. If there were several values, delete the
     * others.
     *
     * @param {string} name
     * @param {string} value
     */ prototype.set = function set(name, value) {
        this[__URLSearchParams__][name] = [
            '' + value
        ];
    };
    /**
     * Returns a string containg a query string suitable for use in a URL.
     *
     * @returns {string}
     */ prototype.toString = function() {
        var dict = this[__URLSearchParams__], query = [], i, key, name, value;
        for(key in dict){
            name = encode(key);
            for(i = 0, value = dict[key]; i < value.length; i++)query.push(name + '=' + encode(value[i]));
        }
        return query.join('&');
    };
    // There is a bug in Safari 10.1 and `Proxy`ing it is not enough.
    var forSureUsePolyfill = !decodesPlusesCorrectly;
    var useProxy = !forSureUsePolyfill && nativeURLSearchParams && !isSupportObjectConstructor && self.Proxy;
    /*
     * Apply polifill to global object and append other prototype into it
     */ Object.defineProperty(self, 'URLSearchParams', {
        value: useProxy ? // Safari 10.0 doesn't support Proxy, so it won't extend URLSearchParams on safari 10.0
        new Proxy(nativeURLSearchParams, {
            construct: function construct(target, args) {
                return new target(new URLSearchParamsPolyfill(args[0]).toString());
            }
        }) : URLSearchParamsPolyfill
    });
    var USPProto = self.URLSearchParams.prototype;
    USPProto.polyfill = true;
    /**
     *
     * @param {function} callback
     * @param {object} thisArg
     */ USPProto.forEach = USPProto.forEach || function(callback, thisArg) {
        var dict = parseToDict(this.toString());
        Object.getOwnPropertyNames(dict).forEach(function(name) {
            dict[name].forEach(function(value) {
                callback.call(thisArg, value, name, this);
            }, this);
        }, this);
    };
    /**
     * Sort all name-value pairs
     */ USPProto.sort = USPProto.sort || function() {
        var dict = parseToDict(this.toString()), keys = [], k, i, j;
        for(k in dict)keys.push(k);
        keys.sort();
        for(i = 0; i < keys.length; i++)this['delete'](keys[i]);
        for(i = 0; i < keys.length; i++){
            var key = keys[i], values = dict[key];
            for(j = 0; j < values.length; j++)this.append(key, values[j]);
        }
    };
    /**
     * Returns an iterator allowing to go through all keys of
     * the key/value pairs contained in this object.
     *
     * @returns {function}
     */ USPProto.keys = USPProto.keys || function() {
        var items = [];
        this.forEach(function(item, name) {
            items.push(name);
        });
        return makeIterator(items);
    };
    /**
     * Returns an iterator allowing to go through all values of
     * the key/value pairs contained in this object.
     *
     * @returns {function}
     */ USPProto.values = USPProto.values || function() {
        var items = [];
        this.forEach(function(item) {
            items.push(item);
        });
        return makeIterator(items);
    };
    /**
     * Returns an iterator allowing to go through all key/value
     * pairs contained in this object.
     *
     * @returns {function}
     */ USPProto.entries = USPProto.entries || function() {
        var items = [];
        this.forEach(function(item, name) {
            items.push([
                name,
                item
            ]);
        });
        return makeIterator(items);
    };
    if (iterable) USPProto[self.Symbol.iterator] = USPProto[self.Symbol.iterator] || USPProto.entries;
})(typeof global !== 'undefined' ? global : typeof window !== 'undefined' ? window : this);

},{}],"dXUcw":[function(require,module,exports) {
(function() {
    var normalizeName = function normalizeName(name) {
        if (typeof name !== 'string') name = name.toString();
        if (/[^a-z0-9\-#$%&'*+.\^_`|~]/i.test(name)) throw new TypeError('Invalid character in header field name');
        return name.toLowerCase();
    };
    var normalizeValue = function normalizeValue(value) {
        if (typeof value !== 'string') value = value.toString();
        return value;
    };
    var consumed = function consumed(body) {
        if (body.bodyUsed) return fetch.Promise.reject(new TypeError('Already read'));
        body.bodyUsed = true;
    };
    var fileReaderReady = function fileReaderReady(reader) {
        return new fetch.Promise(function(resolve, reject) {
            reader.onload = function() {
                resolve(reader.result);
            };
            reader.onerror = function() {
                reject(reader.error);
            };
        });
    };
    var readBlobAsArrayBuffer = function readBlobAsArrayBuffer(blob) {
        var reader = new FileReader();
        reader.readAsArrayBuffer(blob);
        return fileReaderReady(reader);
    };
    var readBlobAsText = function readBlobAsText(blob) {
        var reader = new FileReader();
        reader.readAsText(blob);
        return fileReaderReady(reader);
    };
    var Body = function Body() {
        this.bodyUsed = false;
        this._initBody = function(body) {
            this._bodyInit = body;
            if (typeof body === 'string') this._bodyText = body;
            else if (support.blob && Blob.prototype.isPrototypeOf(body)) this._bodyBlob = body;
            else if (support.formData && FormData.prototype.isPrototypeOf(body)) this._bodyFormData = body;
            else if (!body) this._bodyText = '';
            else throw new Error('unsupported BodyInit type');
        };
        if (support.blob) {
            this.blob = function() {
                var rejected = consumed(this);
                if (rejected) return rejected;
                if (this._bodyBlob) return fetch.Promise.resolve(this._bodyBlob);
                else if (this._bodyFormData) throw new Error('could not read FormData body as blob');
                else return fetch.Promise.resolve(new Blob([
                    this._bodyText
                ]));
            };
            this.arrayBuffer = function() {
                return this.blob().then(readBlobAsArrayBuffer);
            };
            this.text = function() {
                var rejected = consumed(this);
                if (rejected) return rejected;
                if (this._bodyBlob) return readBlobAsText(this._bodyBlob);
                else if (this._bodyFormData) throw new Error('could not read FormData body as text');
                else return fetch.Promise.resolve(this._bodyText);
            };
        } else this.text = function() {
            var rejected = consumed(this);
            return rejected ? rejected : fetch.Promise.resolve(this._bodyText);
        };
        if (support.formData) this.formData = function() {
            return this.text().then(decode);
        };
        this.json = function() {
            return this.text().then(function(text) {
                return JSON.parse(text);
            });
        };
        return this;
    };
    var normalizeMethod = function normalizeMethod(method) {
        var upcased = method.toUpperCase();
        return methods.indexOf(upcased) > -1 ? upcased : method;
    };
    var Request = function Request(url, options) {
        options = options || {};
        this.url = url;
        this.credentials = options.credentials || 'omit';
        this.headers = new Headers(options.headers);
        this.method = normalizeMethod(options.method || 'GET');
        this.mode = options.mode || null;
        this.referrer = null;
        if ((this.method === 'GET' || this.method === 'HEAD') && options.body) throw new TypeError('Body not allowed for GET or HEAD requests');
        this._initBody(options.body);
    };
    var decode = function decode(body) {
        var form = new FormData();
        body.trim().split('&').forEach(function(bytes) {
            if (bytes) {
                var split = bytes.split('=');
                var name = split.shift().replace(/\+/g, ' ');
                var value = split.join('=').replace(/\+/g, ' ');
                form.append(decodeURIComponent(name), decodeURIComponent(value));
            }
        });
        return form;
    };
    var headers = function headers(xhr) {
        var head = new Headers();
        var pairs = xhr.getAllResponseHeaders().trim().split('\n');
        pairs.forEach(function(header) {
            var split = header.trim().split(':');
            var key = split.shift().trim();
            var value = split.join(':').trim();
            head.append(key, value);
        });
        return head;
    };
    var getXhr = function getXhr() {
        // from backbone.js 1.1.2
        // https://github.com/jashkenas/backbone/blob/1.1.2/backbone.js#L1181
        if (noXhrPatch && !/^(get|post|head|put|delete|options)$/i.test(this.method)) {
            this.usingActiveXhr = true;
            return new ActiveXObject("Microsoft.XMLHTTP");
        }
        return new XMLHttpRequest();
    };
    var Response = function Response(bodyInit, options) {
        if (!options) options = {};
        this._initBody(bodyInit);
        this.type = 'default';
        this.url = null;
        this.status = options.status;
        this.ok = this.status >= 200 && this.status < 300;
        this.statusText = options.statusText;
        this.headers = options.headers instanceof Headers ? options.headers : new Headers(options.headers);
        this.url = options.url || '';
    };
    if (self.fetch) return;
    function Headers(headers) {
        this.map = {};
        var _$self = this;
        if (headers instanceof Headers) headers.forEach(function(name, values) {
            values.forEach(function(value) {
                _$self.append(name, value);
            });
        });
        else if (headers) Object.getOwnPropertyNames(headers).forEach(function(name) {
            _$self.append(name, headers[name]);
        });
    }
    Headers.prototype.append = function(name, value) {
        name = normalizeName(name);
        value = normalizeValue(value);
        var list = this.map[name];
        if (!list) {
            list = [];
            this.map[name] = list;
        }
        list.push(value);
    };
    Headers.prototype['delete'] = function(name) {
        delete this.map[normalizeName(name)];
    };
    Headers.prototype.get = function(name) {
        var values = this.map[normalizeName(name)];
        return values ? values[0] : null;
    };
    Headers.prototype.getAll = function(name) {
        return this.map[normalizeName(name)] || [];
    };
    Headers.prototype.has = function(name) {
        return this.map.hasOwnProperty(normalizeName(name));
    };
    Headers.prototype.set = function(name, value) {
        this.map[normalizeName(name)] = [
            normalizeValue(value)
        ];
    };
    // Instead of iterable for now.
    Headers.prototype.forEach = function(callback) {
        var _$self = this;
        Object.getOwnPropertyNames(this.map).forEach(function(name) {
            callback(name, _$self.map[name]);
        });
    };
    var support = {
        blob: 'FileReader' in self && 'Blob' in self && function() {
            try {
                new Blob();
                return true;
            } catch (e) {
                return false;
            }
        }(),
        formData: 'FormData' in self
    };
    // HTTP methods whose capitalization should be normalized
    var methods = [
        'DELETE',
        'GET',
        'HEAD',
        'OPTIONS',
        'POST',
        'PUT'
    ];
    var noXhrPatch = typeof window !== 'undefined' && !!window.ActiveXObject && !(window.XMLHttpRequest && (new XMLHttpRequest).dispatchEvent);
    Body.call(Request.prototype);
    Body.call(Response.prototype);
    self.Headers = Headers;
    self.Request = Request;
    self.Response = Response;
    self.fetch = function(input, init) {
        // TODO: Request constructor should accept input, init
        var request;
        if (Request.prototype.isPrototypeOf(input) && !init) request = input;
        else request = new Request(input, init);
        return new fetch.Promise(function(resolve, reject) {
            var responseURL = function responseURL() {
                if ('responseURL' in xhr) return xhr.responseURL;
                // Avoid security warnings on getResponseHeader when not allowed by CORS
                if (/^X-Request-URL:/m.test(xhr.getAllResponseHeaders())) return xhr.getResponseHeader('X-Request-URL');
                return;
            };
            var onload = function onload() {
                if (xhr.readyState !== 4) return;
                var status = xhr.status === 1223 ? 204 : xhr.status;
                if (status < 100 || status > 599) {
                    reject(new TypeError('Network request failed'));
                    return;
                }
                var options = {
                    status: status,
                    statusText: xhr.statusText,
                    headers: headers(xhr),
                    url: responseURL()
                };
                var body = 'response' in xhr ? xhr.response : xhr.responseText;
                resolve(new Response(body, options));
            };
            var xhr = getXhr();
            if (request.credentials === 'cors') xhr.withCredentials = true;
            xhr.onreadystatechange = onload;
            if (!self.usingActiveXhr) {
                xhr.onload = onload;
                xhr.onerror = function() {
                    reject(new TypeError('Network request failed'));
                };
            }
            xhr.open(request.method, request.url, true);
            if ('responseType' in xhr && support.blob) xhr.responseType = 'blob';
            request.headers.forEach(function(name, values) {
                values.forEach(function(value) {
                    xhr.setRequestHeader(name, value);
                });
            });
            xhr.send(typeof request._bodyInit === 'undefined' ? null : request._bodyInit);
        });
    };
    fetch.Promise = self.Promise; // you could change it to your favorite alternative
    self.fetch.polyfill = true;
})();

},{}],"fjGnP":[function(require,module,exports) {
var a1, b1;
a1 = this, b1 = function b1() {
    var e1 = function e1(e, t) {
        for(var n = 0; n < t.length; n++){
            var i = t[n];
            i.enumerable = i.enumerable || !1, i.configurable = !0, "value" in i && (i.writable = !0), Object.defineProperty(e, i.key, i);
        }
    };
    var t1 = function t1(t, e2) {
        var n, i = Object.keys(t);
        return Object.getOwnPropertySymbols && (n = Object.getOwnPropertySymbols(t), e2 && (n = n.filter(function(e) {
            return Object.getOwnPropertyDescriptor(t, e).enumerable;
        })), i.push.apply(i, n)), i;
    };
    var c = function c(i) {
        var _arguments = arguments, _loop = function(e3) {
            var r = null != _arguments[e3] ? _arguments[e3] : {};
            e3 % 2 ? t1(Object(r), !0).forEach(function(e) {
                var t, n;
                t = i, e = r[n = e], n in t ? Object.defineProperty(t, n, {
                    value: e,
                    enumerable: !0,
                    configurable: !0,
                    writable: !0
                }) : t[n] = e;
            }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(i, Object.getOwnPropertyDescriptors(r)) : t1(Object(r)).forEach(function(e) {
                Object.defineProperty(i, e, Object.getOwnPropertyDescriptor(r, e));
            });
        };
        for(var e3 = 1; e3 < arguments.length; e3++)_loop(e3);
        return i;
    };
    var a = function a(e, t) {
        (null == t || t > e.length) && (t = e.length);
        for(var n = 0, i = new Array(t); n < t; n++)i[n] = e[n];
        return i;
    };
    var l = function l(e5, t2) {
        var n2;
        if ("undefined" == typeof Symbol || null == e5[Symbol.iterator]) {
            if (Array.isArray(e5) || (n2 = function(e, t) {
                if (e) {
                    if ("string" == typeof e) return a(e, t);
                    var n = Object.prototype.toString.call(e).slice(8, -1);
                    return "Map" === (n = "Object" === n && e.constructor ? e.constructor.name : n) || "Set" === n ? Array.from(e) : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? a(e, t) : void 0;
                }
            }(e5)) || t2 && e5 && "number" == typeof e5.length) {
                n2 && (e5 = n2);
                var i = 0, t2 = function t2() {};
                return {
                    s: t2,
                    n: function n() {
                        return i >= e5.length ? {
                            done: !0
                        } : {
                            done: !1,
                            value: e5[i++]
                        };
                    },
                    e: function e6(e) {
                        throw e;
                    },
                    f: t2
                };
            }
            throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
        }
        var r, o = !0, s = !1;
        return {
            s: function s() {
                n2 = e5[Symbol.iterator]();
            },
            n: function n() {
                var _$e = n2.next();
                return o = _$e.done, _$e;
            },
            e: function e6(e) {
                s = !0, r = e;
            },
            f: function f() {
                try {
                    o || null == n2.return || n2.return();
                } finally{
                    if (s) throw r;
                }
            }
        };
    };
    var u = function u(e, t) {
        for(var n = document.getElementsByClassName(e.resultsList.className), i = 0; i < n.length; i++)t !== n[i] && t !== e.inputField && n[i].parentNode.removeChild(n[i]);
        e.inputField.removeAttribute("aria-activedescendant"), e.inputField.setAttribute("aria-expanded", !1);
    };
    var r1 = function r1(s, a, l) {
        var e7, t4, u = (e7 = s, (t4 = document.createElement(e7.resultsList.element)).setAttribute("id", e7.resultsList.idName), t4.setAttribute("aria-label", e7.name), t4.setAttribute("class", e7.resultsList.className), t4.setAttribute("role", "listbox"), t4.setAttribute("tabindex", "-1"), e7.resultsList.container && e7.resultsList.container(t4), ("string" == typeof e7.resultsList.destination ? document.querySelector(e7.resultsList.destination) : e7.resultsList.destination()).insertAdjacentElement(e7.resultsList.position, t4), t4);
        s.inputField.setAttribute("aria-expanded", !0);
        for(var n = function n(t) {
            var e8, n3, i, r, o = a.results[t], r = (e8 = o, n3 = t, i = s, (r = document.createElement(i.resultItem.element)).setAttribute("id", "".concat(i.resultItem.idName, "_").concat(n3)), r.setAttribute("class", i.resultItem.className), r.setAttribute("role", "option"), r.innerHTML = e8.match, i.resultItem.content && i.resultItem.content(e8, r), r);
            r.addEventListener("click", function(e) {
                e = {
                    event: e,
                    matches: l,
                    input: a.input,
                    query: a.query,
                    results: a.results,
                    selection: c(c({}, o), {}, {
                        index: t
                    })
                };
                s.onSelection && s.onSelection(e);
            }), u.appendChild(r);
        }, i2 = 0; i2 < a.results.length; i2++)n(i2);
        return u;
    };
    var d = function d(e, t, n) {
        e.dispatchEvent(new CustomEvent(n, {
            bubbles: !0,
            detail: t,
            cancelable: !0
        }));
    };
    var o1 = function o1(n4, r) {
        function i3(e, t, n, i) {
            e.preventDefault(), n ? o++ : o--, s(t), i.inputField.setAttribute("aria-activedescendant", t[o].id), d(e.srcElement, c(c({
                event: e
            }, r), {}, {
                selection: r.results[o]
            }), "navigation");
        }
        var o = -1, s = function s(e9) {
            if (!e9) return !1;
            !function(e) {
                for(var t = 0; t < e.length; t++)e[t].removeAttribute("aria-selected"), e[t].classList.remove("autoComplete_selected");
            }(e9), e9[o = (o = o >= e9.length ? 0 : o) < 0 ? e9.length - 1 : o].setAttribute("aria-selected", "true"), e9[o].classList.add("autoComplete_selected");
        }, a = n4.resultsList.navigation || function(e) {
            var t = document.getElementById(n4.resultsList.idName);
            if (!t) return n4.inputField.removeEventListener("keydown", a);
            t = t.getElementsByTagName(n4.resultItem.element), 27 === e.keyCode ? (n4.inputField.value = "", u(n4)) : 40 === e.keyCode || 9 === e.keyCode ? i3(e, t, !0, n4) : 38 === e.keyCode || 9 === e.keyCode ? i3(e, t, !1, n4) : 13 === e.keyCode && (e.preventDefault(), -1 < o && t && t[o].click());
        };
        n4.inputField.autoCompleteNavigate && n4.inputField.removeEventListener("keydown", n4.inputField.autoCompleteNavigate), n4.inputField.autoCompleteNavigate = a, n4.inputField.addEventListener("keydown", a);
    };
    var s1 = function s1(o, s) {
        for(var a2 = [], e11 = function e11(n5) {
            function e10(e13) {
                var t7 = (e13 ? i4[e13] : i4).toString();
                t7 && ((t7 = "function" == typeof o.searchEngine ? o.searchEngine(s, t7) : function(e, t, n) {
                    var i = n.diacritics ? t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").normalize("NFC") : t.toLowerCase();
                    if ("loose" === n.searchEngine) {
                        e = e.replace(/ /g, "");
                        for(var r = [], _$o = 0, _$s = 0; _$s < i.length; _$s++){
                            var a = t[_$s];
                            _$o < e.length && i[_$s] === e[_$o] && (a = n.highlight ? '<span class="autoComplete_highlighted">'.concat(a, "</span>") : a, _$o++), r.push(a);
                        }
                        if (_$o === e.length) return r.join("");
                    } else if (i.includes(e)) return e = new RegExp("".concat(e), "i").exec(t), n.highlight ? t.replace(e, '<span class="autoComplete_highlighted">'.concat(e, "</span>")) : t;
                }(s, t7, o)) && e13 ? a2.push({
                    key: e13,
                    index: n5,
                    match: t7,
                    value: i4
                }) : t7 && !e13 && a2.push({
                    index: n5,
                    match: t7,
                    value: i4
                }));
            }
            var i4 = o.data.store[n5];
            if (o.data.key) {
                var t6, r2 = l(o.data.key);
                try {
                    for(r2.s(); !(t6 = r2.n()).done;)e10(t6.value);
                } catch (e) {
                    r2.e(e);
                } finally{
                    r2.f();
                }
            } else e10();
        }, t5 = 0; t5 < o.data.store.length; t5++)e11(t5);
        return o.sort ? a2.sort(o.sort) : a2;
    };
    var n1, i1, h1;
    function T(e14) {
        !function(e) {
            if (!(e instanceof T)) throw new TypeError("Cannot call a class as a function");
        }(this);
        var t = e14.name, n = void 0 === t ? "Search" : t, i = e14.selector, r = void 0 === i ? "#autoComplete" : i, o = e14.observer, s = void 0 !== o && o, a = e14.data, l = a.src, u = a.key, c = a.cache, d = void 0 !== c && c, h = a.store, p = a.results, f = e14.query, v = e14.trigger, m = (v = void 0 === v ? {} : v).event, b2 = void 0 === m ? [
            "input"
        ] : m, y = v.condition, g = void 0 !== y && y, F = e14.searchEngine, L = void 0 === F ? "strict" : F, k = e14.diacritics, C = void 0 !== k && k, E = e14.threshold, A = void 0 === E ? 1 : E, w = e14.debounce, N = void 0 === w ? 0 : w, O = e14.resultsList, j = (O = void 0 === O ? {} : O).render, x = void 0 === j || j, S = O.container, I = void 0 !== S && S, P = O.destination, t = O.position, i = void 0 === t ? "afterend" : t, o = O.element, c = void 0 === o ? "ul" : o, a = O.idName, m = void 0 === a ? "autoComplete_list" : a, v = O.className, y = void 0 === v ? "autoComplete_list" : v, F = O.navigation, k = void 0 !== F && F, E = e14.sort, w = void 0 !== E && E, j = e14.placeHolder, S = e14.maxResults, t = void 0 === S ? 5 : S, o = e14.resultItem, a = (o = void 0 === o ? {} : o).content, v = void 0 !== a && a, O = o.element, F = void 0 === O ? "li" : O, E = o.idName, S = void 0 === E ? "autoComplete_result" : E, a = o.className, O = void 0 === a ? "autoComplete_result" : a, E = e14.noResults, o = e14.highlight, a = void 0 !== o && o, o = e14.feedback, e14 = e14.onSelection;
        this.name = n, this.selector = r, this.observer = s, this.data = {
            src: l,
            key: u,
            cache: d,
            store: h,
            results: p
        }, this.query = f, this.trigger = {
            event: b2,
            condition: g
        }, this.searchEngine = L, this.diacritics = C, this.threshold = A, this.debounce = N, this.resultsList = {
            render: x,
            container: I,
            destination: P || this.selector,
            position: i,
            element: c,
            idName: m,
            className: y,
            navigation: k
        }, this.sort = w, this.placeHolder = j, this.maxResults = t, this.resultItem = {
            content: v,
            element: F,
            idName: S,
            className: O
        }, this.noResults = E, this.highlight = a, this.feedback = o, this.onSelection = e14, this.inputField = "string" == typeof this.selector ? document.querySelector(this.selector) : this.selector(), this.observer ? this.preInit() : this.init();
    }
    return n1 = T, i1 = [
        {
            key: "start",
            value: function value(e15, t) {
                var n = this, i = this.data.results ? this.data.results(s1(this, t)) : s1(this, t), t = {
                    input: e15,
                    query: t,
                    matches: i,
                    results: i.slice(0, this.maxResults)
                };
                return d(this.inputField, t, "results"), i.length ? this.resultsList.render ? (i.length && r1(this, t, i), d(this.inputField, t, "rendered"), o1(this, t), void document.addEventListener("click", function(e) {
                    return u(n, e.target);
                })) : this.feedback(t) : this.noResults ? this.noResults(t, r1) : null;
            }
        },
        {
            key: "dataStore",
            value: function value() {
                var i = this;
                return new Promise(function(t8, n) {
                    return i.data.cache && i.data.store ? t8(null) : new Promise(function(e, t) {
                        return "function" == typeof i.data.src ? i.data.src().then(e, t) : e(i.data.src);
                    }).then(function(e) {
                        try {
                            return i.data.store = e, d(i.inputField, i.data.store, "fetch"), t8();
                        } catch (e16) {
                            return n(e16);
                        }
                    }, n);
                });
            }
        },
        {
            key: "compose",
            value: function value() {
                var a = this;
                return new Promise(function(e, t) {
                    var s = function s() {
                        return e();
                    };
                    var n, i, r, o;
                    return o = a.inputField, n = (o instanceof HTMLInputElement || o instanceof HTMLTextAreaElement ? o.value : o.innerHTML).toLowerCase(), r = n, i = (o = a).query && o.query.manipulate ? o.query.manipulate(r) : o.diacritics ? r.normalize("NFD").replace(/[\u0300-\u036f]/g, "").normalize("NFC") : r, o = i, ((r = a).trigger.condition ? r.trigger.condition(o) : o.length >= r.threshold && o.replace(/ /g, "").length) ? a.dataStore().then(function(e) {
                        try {
                            return u(a), a.start(n, i), s.call(a);
                        } catch (e17) {
                            return t(e17);
                        }
                    }, t) : (u(a), s.call(a));
                });
            }
        },
        {
            key: "init",
            value: function value() {
                var e18, n, i, r, t9 = this;
                (e18 = this).inputField.setAttribute("type", "text"), e18.inputField.setAttribute("role", "combobox"), e18.inputField.setAttribute("aria-haspopup", !0), e18.inputField.setAttribute("aria-expanded", !1), e18.inputField.setAttribute("aria-controls", e18.resultsList.idName), e18.inputField.setAttribute("aria-autocomplete", "both"), this.placeHolder && this.inputField.setAttribute("placeholder", this.placeHolder), this.hook = (n = function n() {
                    t9.compose();
                }, i = this.debounce, function() {
                    var e = this, t = arguments;
                    clearTimeout(r), r = setTimeout(function() {
                        return n.apply(e, t);
                    }, i);
                }), this.trigger.event.forEach(function(e) {
                    t9.inputField.removeEventListener(e, t9.hook), t9.inputField.addEventListener(e, t9.hook);
                }), d(this.inputField, null, "init");
            }
        },
        {
            key: "preInit",
            value: function value() {
                var r = this;
                new MutationObserver(function(e, t) {
                    var n, i = l(e);
                    try {
                        for(i.s(); !(n = i.n()).done;){
                            n.value;
                            r.inputField && (t.disconnect(), d(r.inputField, null, "connect"), r.init());
                        }
                    } catch (e19) {
                        i.e(e19);
                    } finally{
                        i.f();
                    }
                }).observe(document, {
                    childList: !0,
                    subtree: !0
                });
            }
        },
        {
            key: "unInit",
            value: function value() {
                this.inputField.removeEventListener("input", this.hook), d(this.inputField, null, "unInit");
            }
        }
    ], e1(n1.prototype, i1), h1 && e1(n1, h1), T;
}, module.exports = b1();

},{}],"jamAK":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _helpers = require("@swc/helpers");
var _tokenfield = require("tokenfield");
var _tokenfieldDefault = parcelHelpers.interopDefault(_tokenfield);
var LiteTokenField = /*#__PURE__*/ function(Tokenfield) {
    "use strict";
    _helpers.inherits(LiteTokenField, Tokenfield);
    var _super = _helpers.createSuper(LiteTokenField);
    function LiteTokenField() {
        _helpers.classCallCheck(this, LiteTokenField);
        var _this;
        _this = _super.apply(this, arguments);
        /**
   * Override _renderItem not to append [] to end of input name
   * @param item the selected item from the list
   * @param k index of selected item, not used here but kept for compatibility with superclass
   */ _helpers.defineProperty(_helpers.assertThisInitialized(_this), "_renderItem", function(item, k) {
            var o = this._options;
            var itemHtml = this.renderSetItemHtml(item);
            var label = itemHtml.querySelector(".item-label");
            var input = itemHtml.querySelector(".item-input");
            var remove = itemHtml.querySelector(".item-remove");
            itemHtml.key = item[this.key];
            remove.key = item[this.key];
            input.setAttribute("name", item.isNew ? o.newItemName : o.itemName);
            input.value = item[item.isNew ? o.newItemValue : o.itemValue] || null;
            label.textContent = this.renderSetItemLabel(item);
            if (item.focused) itemHtml.classList.add("focused");
            return itemHtml;
        });
        return _this;
    }
    return LiteTokenField;
}(_tokenfieldDefault.default);
exports.default = window.TokenField = LiteTokenField;

},{"@swc/helpers":"3OBsq","tokenfield":"hWHxu","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hWHxu":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _helpers = require("@swc/helpers");
/**
 * Input field with tagging/token/chip capabilities written in raw JavaScript
 * tokenfield 1.4.4 <https://github.com/KaneCohen/tokenfield>
 * Copyright 2018 Kane Cohen <https://github.com/KaneCohen>
 * Available under BSD-3-Clause license
 */ var _events = require("events");
var _eventsDefault = parcelHelpers.interopDefault(_events);
var _ajaxJs = require("./ajax.js");
var _ajaxJsDefault = parcelHelpers.interopDefault(_ajaxJs);
var _tokenfields = {};
var reRegExpChar = /[\\^$.*+?()[\]{}|]/g;
var reHasRegExpChar = RegExp(reRegExpChar.source);
var _factory = document.createElement('div');
var _templates = {
    containerTokenfield: '<div class="tokenfield tokenfield-mode-tokens">\n      <input class="tokenfield-copy-helper"\n        style="display:none;position:fixed;top:-1000px;right:1000px;"\n        tabindex="-1"\n        type="text"\n      />\n      <div class="tokenfield-set">\n        <ul></ul>\n      </div>\n      <input class="tokenfield-input" />\n      <div class="tokenfield-suggest">\n        <ul class="tokenfield-suggest-list"></ul>\n      </div>\n    </div>',
    containerList: '<div class="tokenfield tokenfield-mode-list">\n      <input class="tokenfield-input" />\n      <div class="tokenfield-suggest">\n        <ul class="tokenfield-suggest-list"></ul>\n      </div>\n      <div class="tokenfield-set">\n        <ul></ul>\n      </div>\n    </div>',
    suggestItem: '<li class="tokenfield-suggest-item"></li>',
    setItem: '<li class="tokenfield-set-item">\n      <span class="item-label"></span>\n      <a href="#" class="item-remove" tabindex="-1">\xd7</a>\n      <input class="item-input" type="hidden" />\n    </li>'
};
function guid() {
    return ((1 + Math.random()) * 65536 | 0).toString(16) + ((1 + Math.random()) * 65536 | 0).toString(16);
}
function includes(arr, item) {
    return arr.indexOf(item) >= 0;
}
function getPath(node) {
    var nodes = [
        node
    ];
    while(node.parentNode){
        node = node.parentNode;
        nodes.push(node);
    }
    return nodes;
}
function findElement(input) {
    if (input.nodeName) return input;
    else if (typeof input === 'string') return document.querySelector(input);
    return null;
}
function build(html, all) {
    if (html.nodeName) return html;
    html = html.replace(/(\t|\n$)/g, '');
    _factory.innerHTML = '';
    _factory.innerHTML = html;
    if (all === true) return _factory.childNodes;
    else return _factory.childNodes[0];
}
function toString(value) {
    if (typeof value == 'string') return value;
    if (value === null) return '';
    var result = value + '';
    return result === '0' && 1 / value === -Infinity ? '-0' : result;
}
function keyToChar(e) {
    if (e.key || e.keyIdentifier) return e.key || String.fromCharCode(parseInt(e.keyIdentifier.substr(2), 16));
    return null;
}
function escapeRegex(string) {
    string = toString(string);
    return string && reHasRegExpChar.test(string) ? string.replace(reRegExpChar, '\\$&') : string;
}
function makeDefaultsAndOptions() {
    var _defaults = {
        focusedItem: null,
        cache: {},
        timer: null,
        xhr: null,
        suggested: false,
        suggestedItems: [],
        setItems: [],
        events: {},
        delimiters: {}
    };
    var _options = {
        el: null,
        form: true,
        // immediate parent form. Also accepts selectors or elements.
        mode: 'tokenfield',
        addItemOnBlur: false,
        addItemsOnPaste: false,
        keepItemsOrder: true,
        // in the list so that you can retreive correct position on the backend.
        setItems: [],
        items: [],
        // Example: [{id: 143, value: 'Hello World'}, {id: 144, value: 'Foo Bar'}].
        newItems: true,
        multiple: true,
        maxItems: 0,
        minLength: 0,
        keys: {
            17: 'ctrl',
            16: 'shift',
            91: 'meta',
            8: 'delete',
            27: 'esc',
            37: 'left',
            38: 'up',
            39: 'right',
            40: 'down',
            46: 'delete',
            65: 'select',
            67: 'copy',
            88: 'cut',
            9: 'delimiter',
            13: 'delimiter',
            108: 'delimiter' // Numpad Enter
        },
        matchRegex: '{value}',
        matchFlags: 'i',
        matchStart: false,
        matchEnd: false,
        delimiters: [],
        copyProperty: 'name',
        copyDelimiter: ', ',
        remote: {
            type: 'GET',
            url: null,
            queryParam: 'q',
            delay: 300,
            timestampParam: 't',
            params: {},
            headers: {}
        },
        placeholder: null,
        inputType: 'text',
        // Accepts text, email, url, and others.
        minChars: 2,
        maxSuggest: 10,
        maxSuggestWindow: 10,
        filterSetItems: true,
        filterMatchCase: false,
        singleInput: false,
        // When set to true - would use tokenfield target element as an input to fill.
        singleInputValue: 'id',
        singleInputDelimiter: ', ',
        itemLabel: 'name',
        itemName: 'items',
        // input field with array property name:
        // name="items[]".
        newItemName: 'items_new',
        // case it was not available from the server:
        // name="items_new[]".
        itemValue: 'id',
        newItemValue: 'name',
        itemData: 'name',
        validateNewItem: null // Run a function to test if new item is valid and can be added.
    };
    return {
        _defaults: _defaults,
        _options: _options
    };
}
var Tokenfield = /*#__PURE__*/ function(EventEmitter) {
    "use strict";
    _helpers.inherits(Tokenfield, EventEmitter);
    var _super = _helpers.createSuper(Tokenfield);
    function Tokenfield() {
        var options = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
        _helpers.classCallCheck(this, Tokenfield);
        var _this;
        _this = _super.call(this);
        var ref = makeDefaultsAndOptions(), _defaults = ref._defaults, _options = ref._options;
        _this.id = guid();
        _this.key = "key_".concat(_this.id);
        _this._vars = Object.assign({}, _defaults);
        _this._options = Object.assign({}, _options, options);
        _this._options.keys = Object.assign({}, _options.keys, options.keys);
        _this._options.remote = Object.assign({}, _options.remote, options.remote);
        _this._templates = Object.assign({}, _templates, options.templates);
        _this._vars.setItems = _this._prepareData(_this.remapData(_this._options.setItems || []));
        _this._focused = false;
        _this._input = null;
        _this._form = false;
        _this._html = {};
        var o = _this._options;
        // Make a hash map to simplify filtering later.
        o.delimiters.forEach(function(delimiter) {
            _this._vars.delimiters[delimiter] = true;
        });
        var el = findElement(o.el);
        if (el) _this.el = el;
        else throw new Error("Selector: DOM Element ".concat(o.el, " not found."));
        if (o.singleInput) {
            var el1 = findElement(o.singleInput);
            if (el1) _this._input = el1;
            else _this._input = _this.el;
        }
        _this.el.tokenfield = _helpers.assertThisInitialized(_this);
        if (o.placeholder === null) o.placeholder = o.el.placeholder || '';
        if (o.form) {
            var form = false;
            if (o.form.nodeName) form = o.form;
            else if (o.form === true) {
                var node = _this.el;
                while(node.parentNode){
                    if (node.nodeName === 'FORM') {
                        form = node;
                        break;
                    }
                    node = node.parentNode;
                }
            } else if (typeof form == 'string') {
                form = document.querySelector(form);
                if (!form) throw new Error("Selector: DOM Element ".concat(o.form, " not found."));
            }
            _this._form = form;
        } else throw new Error("Cannot create tokenfield without DOM Element.");
        _tokenfields[_this.id] = _helpers.assertThisInitialized(_this);
        _this._render();
        return _this;
    }
    _helpers.createClass(Tokenfield, [
        {
            key: "_render",
            value: function _render() {
                var o = this._options;
                var html = this._html;
                if (o.mode === 'tokenfield') html.container = build(this._templates.containerTokenfield);
                else html.container = build(this._templates.containerList);
                html.suggest = html.container.querySelector('.tokenfield-suggest');
                html.suggestList = html.container.querySelector('.tokenfield-suggest-list');
                html.items = html.container.querySelector('.tokenfield-set > ul');
                html.input = html.container.querySelector('.tokenfield-input');
                html.input.setAttribute('type', o.inputType);
                if (o.mode === 'tokenfield') html.input.placeholder = this._vars.setItems.length ? '' : o.placeholder;
                else html.input.placeholder = o.placeholder;
                html.copyHelper = html.container.querySelector('.tokenfield-copy-helper');
                o.el.style.display = 'none';
                html.suggest.style.display = 'none';
                this._renderSizer();
                // Set tokenfield in DOM.
                html.container.tokenfield = this;
                o.el.parentElement.insertBefore(html.container, o.el);
                html.container.insertBefore(o.el, html.container.firstChild);
                this._setEvents();
                this._renderItems();
                if (o.mode === 'tokenfield') this._resizeInput();
                return this;
            }
        },
        {
            key: "_renderSizer",
            value: function _renderSizer() {
                var html = this._html;
                var b = this._getBounds();
                var style = window.getComputedStyle(html.container);
                var compensate = parseInt(style.paddingLeft, 10) + parseInt(style.paddingRight, 10);
                var styles = {
                    width: 'auto',
                    height: 'auto',
                    overflow: 'hidden',
                    whiteSpace: 'pre',
                    maxWidth: b.width - compensate + 'px',
                    position: 'fixed',
                    top: "-10000px",
                    left: "10000px",
                    fontSize: style.fontSize,
                    paddingLeft: style.paddingLeft,
                    paddingRight: style.paddingRight
                };
                html.sizer = document.createElement('div');
                html.sizer.id = 'tokenfield-sizer-' + this.id;
                for(var key in styles)html.sizer.style[key] = styles[key];
                html.container.appendChild(html.sizer);
            }
        },
        {
            key: "_minimizeInput",
            value: function _minimizeInput() {
                this._html.input.style.width = '20px';
                return this;
            }
        },
        {
            key: "_refreshInput",
            value: function _refreshInput() {
                var empty = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : true;
                var v = this._vars;
                var html = this._html;
                if (empty) html.input.value = '';
                if (this._options.mode === 'tokenfield') {
                    this._resizeInput();
                    var placeholder = v.setItems.length ? '' : this._options.placeholder;
                    html.input.setAttribute('placeholder', placeholder);
                } else if (this._options.mode === 'list') html.input.setAttribute('placeholder', this._options.placeholder);
                return this;
            }
        },
        {
            key: "_resizeInput",
            value: function _resizeInput() {
                var val = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : '';
                var html = this._html;
                var b = this._getBounds();
                var style = window.getComputedStyle(html.container);
                var compensate = parseInt(style.paddingRight, 10) + parseInt(style.borderRightWidth, 10);
                var fullCompensate = compensate + parseInt(style.paddingLeft, 10) + parseInt(style.borderLeftWidth, 10);
                html.sizer.innerHTML = val;
                html.sizer.style.maxWidth = b.width - compensate + 'px';
                if (b.width === 0) {
                    html.input.style.width = '100%';
                    return;
                } else html.input.style.width = '20px';
                var sb = html.sizer.getBoundingClientRect();
                var ib = html.input.getBoundingClientRect();
                var rw = b.width - (ib.left - b.left) - compensate;
                if (sb.width > rw) html.input.style.width = b.width - fullCompensate - 1 + 'px';
                else html.input.style.width = rw - 1 + 'px';
            }
        },
        {
            key: "_fetchData",
            value: function _fetchData(val) {
                var _this = this;
                var v = this._vars;
                var o = this._options;
                var r = o.remote;
                var reqData = Object.assign({}, o.params);
                for(var key in r.params)reqData[key] = r.params[key];
                if (r.limit) reqData[r.limit] = o.remote.limit;
                reqData[r.queryParam] = val;
                reqData[r.timestampParam] = Math.round(new Date().getTime() / 1000);
                v.xhr = _ajaxJsDefault.default(reqData, o.remote, function() {
                    if (v.xhr && v.xhr.readyState == 4) {
                        if (v.xhr.status == 200) {
                            var response = JSON.parse(v.xhr.responseText);
                            v.cache[val] = response;
                            var data = _this._prepareData(_this.remapData(response));
                            var items = _this._filterData(val, data);
                            v.suggestedItems = o.filterSetItems ? _this._filterSetItems(items) : items;
                            _this.showSuggestions();
                        } else if (v.xhr.status > 0) throw new Error('Error while loading remote data.');
                        _this._abortXhr();
                    }
                });
            }
        },
        {
            // Overwriteable method where you can change given data to appropriate format.
            key: "remapData",
            value: function remapData(data) {
                return data;
            }
        },
        {
            key: "_prepareData",
            value: function _prepareData(data) {
                var _this = this;
                return data.map(function(item) {
                    return Object.assign({}, item, _helpers.defineProperty({}, _this.key, guid()));
                });
            }
        },
        {
            key: "_filterData",
            value: function _filterData(val, data) {
                var o = this._options;
                var regex = o.matchRegex.replace('{value}', escapeRegex(val));
                if (o.matchStart) regex = '^' + regex;
                else if (o.matchEnd) regex = regex + '$';
                var pattern = new RegExp(regex, o.matchFlags);
                return data.filter(function(item) {
                    return pattern.test(item[o.itemData]);
                });
            }
        },
        {
            key: "_abortXhr",
            value: function _abortXhr() {
                var v = this._vars;
                if (v.xhr !== null) {
                    v.xhr.abort();
                    v.xhr = null;
                }
            }
        },
        {
            key: "_filterSetItems",
            value: function _filterSetItems(items) {
                var key = this._options.itemValue;
                var v = this._vars;
                if (!v.setItems.length) return items;
                var setKeys = v.setItems.map(function(item) {
                    return item[key];
                });
                return items.filter(function(item) {
                    if (setKeys.indexOf(item[key]) === -1) return true;
                    return false;
                });
            }
        },
        {
            key: "_setEvents",
            value: function _setEvents() {
                var v = this._vars;
                var html = this._html;
                v.events.onClick = this._onClick.bind(this);
                v.events.onMouseDown = this._onMouseDown.bind(this);
                v.events.onMouseOver = this._onMouseOver.bind(this);
                v.events.onFocus = this._onFocus.bind(this);
                v.events.onResize = this._onResize.bind(this);
                v.events.onReset = this._onReset.bind(this);
                v.events.onKeyDown = this._onKeyDown.bind(this);
                v.events.onFocusOut = this._onFocusOut.bind(this);
                html.container.addEventListener('click', v.events.onClick);
                // Attach document event only once.
                if (Object.keys(_tokenfields).length === 1) {
                    document.addEventListener('mousedown', v.events.onMouseDown);
                    window.addEventListener('resize', v.events.onResize);
                }
                if (this._form && this._form.nodeName) this._form.addEventListener('reset', v.events.onReset);
                html.suggestList.addEventListener('mouseover', v.events.onMouseOver);
                html.input.addEventListener('focus', v.events.onFocus);
            }
        },
        {
            key: "_onMouseOver",
            value: function _onMouseOver(e) {
                var target = e.target;
                if (target.classList.contains('tokenfield-suggest-item')) {
                    var selected = [].slice.call(this._html.suggestList.querySelectorAll('.selected'));
                    selected.forEach(function(item) {
                        if (item !== target) item.classList.remove('selected');
                    });
                    target.classList.add('selected');
                    this._selectItem(target.key, false);
                    this._refreshItemsSelection();
                }
            }
        },
        {
            key: "_onReset",
            value: function _onReset() {
                this.setItems(this._options.setItems);
            }
        },
        {
            key: "_onFocus",
            value: function _onFocus() {
                var v = this._vars;
                var html = this._html;
                var o = this._options;
                html.input.removeEventListener('keydown', v.events.onKeyDown);
                html.input.addEventListener('keydown', v.events.onKeyDown);
                html.input.addEventListener('focusout', v.events.onFocusOut);
                if (o.addItemsOnPaste) {
                    v.events.onPaste = this._onPaste.bind(this);
                    html.input.addEventListener('paste', v.events.onPaste);
                }
                this._focused = true;
                this._html.container.classList.add('focused');
                this._resizeInput();
                if (html.input.value.trim().length >= o.minChars) this.showSuggestions();
            }
        },
        {
            key: "_onFocusOut",
            value: function _onFocusOut(e) {
                var v = this._vars;
                var o = this._options;
                var html = this._html;
                html.input.removeEventListener('keydown', v.events.onKeyDown);
                html.input.removeEventListener('focusout', v.events.onFocusOut);
                if (typeof v.events.onPaste !== 'undefined') html.input.removeEventListener('paste', v.events.onPaste);
                if (e.relatedTarget && e.relatedTarget === html.copyHelper) return;
                var canAddItem = o.multiple && !o.maxItems || !o.multiple && !v.setItems.length || o.multiple && o.maxItems && v.setItems.length < o.maxItems;
                if (this._focused && o.addItemOnBlur && canAddItem && this._newItem(html.input.value)) this._renderItems()._refreshInput();
                else this._defocusItems()._renderItems();
                this._focused = false;
                this._html.container.classList.remove('focused');
            }
        },
        {
            key: "_onMouseDown",
            value: function _onMouseDown(e) {
                var tokenfield = null;
                for(var key in _tokenfields)if (_tokenfields[key]._html.container.contains(e.target)) {
                    tokenfield = _tokenfields[key];
                    break;
                }
                if (tokenfield) {
                    for(var key1 in _tokenfields)if (key1 !== tokenfield.id) {
                        _tokenfields[key1].hideSuggestions();
                        _tokenfields[key1].blur();
                    }
                    // Prevent input blur.
                    if (e.target !== tokenfield._html.input) e.preventDefault();
                } else for(var key2 in _tokenfields){
                    _tokenfields[key2].hideSuggestions();
                    _tokenfields[key2].blur();
                }
            }
        },
        {
            key: "_onResize",
            value: function _onResize() {
                for(var key in _tokenfields)_tokenfields[key]._resizeInput(_tokenfields[key]._html.input.value);
            }
        },
        {
            key: "_onPaste",
            value: function _onPaste(e) {
                var _this = this;
                var v = this._vars;
                var o = this._options;
                var val = e.clipboardData.getData('text');
                var tokens = [
                    val
                ];
                // Break input using delimiters option.
                if (o.delimiters.length) {
                    var search = o.delimiters.join('|');
                    var splitRegex = new RegExp("(".concat(search, ")"), 'ig');
                    tokens = val.split(splitRegex);
                }
                var items = tokens.map(function(token) {
                    return token.trim();
                }).filter(function(token) {
                    return token.length > 0 && token.length >= o.minLength && typeof v.delimiters[token] === 'undefined';
                }).map(function(token) {
                    return _this._newItem(token);
                });
                if (items.length) {
                    var _this1 = this;
                    setTimeout(function() {
                        _this1._renderItems()._refreshInput()._deselectItems().hideSuggestions();
                    }, 1);
                    e.preventDefault();
                }
            }
        },
        {
            key: "_onKeyDown",
            value: function _onKeyDown(e) {
                var _this = this;
                var v = this._vars;
                var o = this._options;
                var html = this._html;
                if (o.maxItems && v.setItems.length >= o.maxItems) e.preventDefault();
                if (o.mode === 'tokenfield') setTimeout(function() {
                    _this._resizeInput(html.input.value);
                }, 1);
                var key = keyToChar(e);
                if (typeof o.keys[e.keyCode] !== 'undefined' || includes(o.delimiters, key)) {
                    if (this._keyAction(e)) return true;
                } else this._defocusItems()._refreshItems();
                clearTimeout(v.timer);
                this._abortXhr();
                if (!o.maxItems || v.setItems.length < o.maxItems) setTimeout(function() {
                    _this._keyInput(e);
                }, 1);
            }
        },
        {
            key: "_keyAction",
            value: function _keyAction(e) {
                var key = this.key;
                var item1 = null;
                var v = this._vars;
                var o = this._options;
                var html = this._html;
                var keyName = o.keys[e.keyCode];
                var val = html.input.value.trim();
                var keyChar = keyToChar(e);
                if (includes(o.delimiters, keyChar) && typeof keyName === 'undefined') keyName = 'delimiter';
                var selected = this._getSelectedItems();
                if (selected.length) item1 = selected[0];
                switch(keyName){
                    case 'esc':
                        this._deselectItems()._defocusItems()._renderItems().hideSuggestions();
                        break;
                    case 'up':
                        if (this._vars.suggested) {
                            this._selectPrevItem()._refreshItemsSelection();
                            e.preventDefault();
                        }
                        this._defocusItems()._renderItems();
                        break;
                    case 'down':
                        if (this._vars.suggested) {
                            this._selectNextItem()._refreshItemsSelection();
                            e.preventDefault();
                        }
                        this._defocusItems()._renderItems();
                        break;
                    case 'left':
                        if (this.getFocusedItems().length || !html.input.selectionStart && !html.input.selectionEnd) {
                            this._focusPrevItem(e.shiftKey);
                            e.preventDefault();
                        }
                        break;
                    case 'right':
                        if (this.getFocusedItems().length || html.input.selectionStart === val.length) {
                            this._focusNextItem(e.shiftKey);
                            e.preventDefault();
                        }
                        break;
                    case 'delimiter':
                        this._abortXhr();
                        this._defocusItems();
                        if (!o.multiple && v.setItems.length >= 1) return false;
                        val = this.onInput(val, e);
                        if (item1) this._addItem(item1);
                        else if (val.length) item1 = this._newItem(val);
                        if (item1) this._minimizeInput()._renderItems().focus()._refreshInput()._refreshSuggestions()._deselectItems();
                        e.preventDefault();
                        break;
                    case 'select':
                        if (!val.length && (e.ctrlKey || e.metaKey)) {
                            this._vars.setItems.forEach(function(item) {
                                item.focused = true;
                            });
                            this._refreshItems();
                        } else return false;
                        break;
                    case 'cut':
                        {
                            var focusedItems = this.getFocusedItems();
                            if (focusedItems.length && (e.ctrlKey || e.metaKey)) this._copy()._delete(e);
                            else return false;
                            break;
                        }
                    case 'copy':
                        {
                            var focusedItems1 = this.getFocusedItems();
                            if (focusedItems1.length && (e.ctrlKey || e.metaKey)) this._copy();
                            else return false;
                            break;
                        }
                    case 'delete':
                        {
                            var _this = this;
                            this._abortXhr();
                            var focusedItems2 = this.getFocusedItems();
                            if (!html.input.selectionEnd && e.keyCode === 8 || html.input.selectionStart === val.length && e.keyCode === 46 || focusedItems2.length) this._delete(e);
                            else v.timer = setTimeout(function() {
                                _this._keyInput(e);
                            }, o.delay);
                            break;
                        }
                    default:
                        break;
                }
                return true;
            }
        },
        {
            key: "_copy",
            value: function _copy() {
                var o = this._options;
                var html = this._html;
                var copyString = this.getFocusedItems().map(function(item) {
                    return item[o.copyProperty];
                }).join(o.copyDelimiter);
                html.copyHelper.style.display = 'block';
                html.copyHelper.value = copyString;
                html.copyHelper.focus();
                html.copyHelper.select();
                document.execCommand('copy');
                html.copyHelper.style.display = 'none';
                html.copyHelper.value = '';
                html.input.focus();
                return this;
            }
        },
        {
            key: "_delete",
            value: function _delete(e) {
                var v = this._vars;
                var o = this._options;
                var key = this.key;
                var html = this._html;
                var focusedItems = this.getFocusedItems();
                if (o.mode === 'tokenfield' && v.setItems.length) {
                    if (focusedItems.length) {
                        var _this = this;
                        focusedItems.forEach(function(item) {
                            _this._removeItem(item[key]);
                        });
                        this._refreshSuggestions()._keyInput(e);
                    } else if (!html.input.selectionStart) this._focusItem(v.setItems[v.setItems.length - 1][key]);
                } else if (focusedItems.length) {
                    var _this2 = this;
                    focusedItems.forEach(function(item) {
                        _this2._removeItem(item[key]);
                    });
                    this._refreshSuggestions()._keyInput(e);
                }
                this._minimizeInput()._renderItems()._refreshInput(false);
                return this;
            }
        },
        {
            key: "_keyInput",
            value: function _keyInput(e) {
                var v = this._vars;
                var o = this._options;
                var html = this._html;
                this._defocusItems()._refreshItems();
                var val = this.onInput(html.input.value.trim(), e);
                if (e.type === 'keydown') this.emit('input', this, val, e);
                if (val.length < o.minChars) {
                    this.hideSuggestions();
                    return false;
                }
                if (!o.multiple && v.setItems.length >= 1) return false;
                // Check if we have cache with this val.
                if (typeof v.cache[val] === 'undefined') {
                    var _this = this;
                    // Get new data.
                    if (o.remote.url) v.timer = setTimeout(function() {
                        _this._fetchData(val);
                    }, o.delay);
                    else if (!o.remote.url && o.items.length) {
                        var data = this._prepareData(o.items);
                        var items = this._filterData(val, data);
                        v.suggestedItems = o.filterSetItems ? this._filterSetItems(items) : items;
                        this.showSuggestions();
                    }
                } else {
                    // Work with cached data.
                    var data1 = this._prepareData(this.remapData(v.cache[val]));
                    var items1 = this._filterData(val, data1);
                    v.suggestedItems = o.filterSetItems ? this._filterSetItems(items1) : items1;
                    this.showSuggestions();
                }
                return this;
            }
        },
        {
            key: "_onClick",
            value: function _onClick(e) {
                var target = e.target;
                if (target.classList.contains('item-remove')) {
                    e.preventDefault();
                    this._removeItem(target.key)._defocusItems()._minimizeInput()._renderItems()._refreshInput(false)._keyInput(e);
                } else if (target.classList.contains('tokenfield-suggest-item')) {
                    var item = this._getSuggestedItem(target.key);
                    this._addItem(item)._minimizeInput()._renderItems()._refreshInput()._refreshSuggestions();
                } else {
                    var setItem = getPath(target).filter(function(node) {
                        return node.classList && node.classList.contains('tokenfield-set-item');
                    })[0];
                    if (setItem) {
                        this._focusItem(setItem.key, e.shiftKey, e.ctrlKey || e.metaKey, true);
                        this._refreshItems();
                    } else this._keyInput(e);
                }
                this.focus();
            }
        },
        {
            key: "_selectPrevItem",
            value: function _selectPrevItem() {
                var key = this.key;
                var o = this._options;
                var items = this._vars.suggestedItems;
                var index = this._getSelectedItemIndex();
                if (!items.length) return this;
                if (index !== null) {
                    if (index === 0) {
                        if (o.newItems) this._deselectItems();
                        else this._selectItem(items[items.length - 1][key]);
                    } else this._selectItem(items[index - 1][key]);
                } else this._selectItem(items[items.length - 1][key]);
                return this;
            }
        },
        {
            key: "_selectNextItem",
            value: function _selectNextItem() {
                var key = this.key;
                var o = this._options;
                var items = this._vars.suggestedItems;
                var index = this._getSelectedItemIndex();
                if (!items.length) return this;
                if (index !== null) {
                    if (index === items.length - 1) {
                        if (o.newItems) this._deselectItems();
                        else this._selectItem(items[0][key]);
                    } else this._selectItem(items[index + 1][key]);
                } else this._selectItem(items[0][key]);
                return this;
            }
        },
        {
            key: "_focusPrevItem",
            value: function _focusPrevItem() {
                var multiple = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : false;
                var key = this.key;
                var items = this._vars.setItems;
                var index = this._getFocusedItemIndex();
                if (!items.length) return this;
                if (index !== null) {
                    if (index === 0 && !multiple) this._defocusItems();
                    else if (index === 0 && multiple) {
                        var lastFocused = this._getFocusedItemIndex(true);
                        this._defocusItem(items[lastFocused][key]);
                    } else this._focusItem(items[index - 1][key], multiple, false, true);
                } else this._focusItem(items[items.length - 1][key], false, false, true);
                this._refreshItems();
                return this;
            }
        },
        {
            key: "_focusNextItem",
            value: function _focusNextItem() {
                var multiple = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : false;
                var key = this.key;
                var items = this._vars.setItems;
                var index = this._getFocusedItemIndex(true);
                if (!items.length) return this;
                if (index !== null) {
                    if (index === items.length - 1 && !multiple) this._defocusItems();
                    else if (index === items.length - 1 && multiple) this._focusItem(items[0][key], multiple);
                    else this._focusItem(items[index + 1][key], multiple);
                } else this._focusItem(items[0][key], false);
                this._refreshItems();
                return this;
            }
        },
        {
            key: "_getSelectedItems",
            value: function _getSelectedItems() {
                var key = this.key;
                var setIds = this._vars.setItems.map(function(item) {
                    return item[key];
                });
                return this._vars.suggestedItems.filter(function(v) {
                    return v.selected && setIds.indexOf(v[key]) < 0;
                });
            }
        },
        {
            key: "_selectItem",
            value: function _selectItem(key) {
                var scroll = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : false;
                var _this = this;
                this._vars.suggestedItems.forEach(function(v) {
                    v.selected = v[_this.key] === key;
                    if (v.selected && scroll) {
                        var height = parseInt(_this._html.suggest.style.maxHeight, 10);
                        if (height) {
                            var listBounds = _this._html.suggestList.getBoundingClientRect();
                            var elBounds = v.el.getBoundingClientRect();
                            var top = elBounds.top - listBounds.top;
                            var bottom = top + elBounds.height;
                            if (bottom >= height + _this._html.suggest.scrollTop) _this._html.suggest.scrollTop = bottom - height;
                            else if (top < _this._html.suggest.scrollTop) _this._html.suggest.scrollTop = top;
                        }
                    }
                });
            }
        },
        {
            key: "_deselectItem",
            value: function _deselectItem(key) {
                var _this = this;
                this._vars.suggestedItems.every(function(v) {
                    if (v[_this.key] === key) {
                        v.selected = false;
                        return false;
                    }
                    return true;
                });
                return this;
            }
        },
        {
            key: "_deselectItems",
            value: function _deselectItems() {
                this._vars.suggestedItems.forEach(function(v) {
                    v.selected = false;
                });
                return this;
            }
        },
        {
            key: "_refreshItemsSelection",
            value: function _refreshItemsSelection() {
                this._vars.suggestedItems.forEach(function(v) {
                    if (v.selected && v.el) v.el.classList.add('selected');
                    else if (v.el) v.el.classList.remove('selected');
                });
            }
        },
        {
            key: "_getSelectedItemIndex",
            value: function _getSelectedItemIndex() {
                var index = null;
                this._vars.suggestedItems.every(function(v, k) {
                    if (v.selected) {
                        index = k;
                        return false;
                    }
                    return true;
                });
                return index;
            }
        },
        {
            key: "_getFocusedItemIndex",
            value: function _getFocusedItemIndex() {
                var last = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : false;
                var index = null;
                this._vars.setItems.every(function(v, k) {
                    if (v.focused) {
                        index = k;
                        if (!last) return false;
                    }
                    return true;
                });
                return index;
            }
        },
        {
            key: "_getItem",
            value: function _getItem(val) {
                var prop = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : null;
                if (prop === null) prop = this.key;
                var items = this._filterItems(this._vars.setItems, val, prop);
                return items.length ? items[0] : null;
            }
        },
        {
            key: "_getSuggestedItem",
            value: function _getSuggestedItem(val) {
                var prop = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : null;
                if (prop === null) prop = this.key;
                var items = this._filterItems(this._vars.suggestedItems, val, prop);
                return items.length ? items[0] : null;
            }
        },
        {
            key: "_getAvailableItem",
            value: function _getAvailableItem(val) {
                var prop = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : null;
                if (prop === null) prop = this.key;
                var items = this._filterItems(this._options.items, val, prop);
                return items.length ? items[0] : null;
            }
        },
        {
            key: "_filterItems",
            value: function _filterItems(items, val, prop) {
                var matchCase = this._options.filterMatchCase;
                return items.filter(function(v) {
                    if (typeof v[prop] === 'string' && typeof val === 'string') {
                        if (matchCase) return v[prop] === val;
                        return v[prop].toLowerCase() == val.toLowerCase();
                    }
                    return v[prop] == val;
                });
            }
        },
        {
            key: "_removeItem",
            value: function _removeItem(key) {
                var _this = this;
                this._vars.setItems.every(function(item, k) {
                    if (item[_this.key] === key) {
                        _this.emit('removeToken', _this, item);
                        _this._vars.setItems.splice(k, 1);
                        _this.emit('removedToken', _this, item);
                        _this.emit('change', _this);
                        return false;
                    }
                    return true;
                });
                return this;
            }
        },
        {
            key: "_addItem",
            value: function _addItem(item) {
                item.focused = false;
                var o = this._options;
                // Check if item already exists in a given list.
                if (item.isNew && !this._getItem(item[o.itemData], o.itemData) || !this._getItem(item[o.itemValue], o.itemValue)) {
                    this.emit('addToken', this, item);
                    if (!this._options.maxItems || this._options.maxItems && this._vars.setItems.length < this._options.maxItems) {
                        item.selected = false;
                        var clonedItem = Object.assign({}, item);
                        this._vars.setItems.push(clonedItem);
                        this.emit('addedToken', this, clonedItem);
                        this.emit('change', this);
                    }
                }
                return this;
            }
        },
        {
            key: "getFocusedItem",
            value: function getFocusedItem() {
                var items = this._vars.setItems.filter(function(item) {
                    return item.focused;
                })[0];
                if (items.length) return items[0];
                return null;
            }
        },
        {
            key: "getFocusedItems",
            value: function getFocusedItems() {
                return this._vars.setItems.filter(function(item) {
                    return item.focused;
                });
            }
        },
        {
            key: "_focusItem",
            value: function _focusItem(key) {
                var shift = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : false, ctrl = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : false, add = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : false;
                var _this = this;
                if (shift) {
                    var _this3 = this;
                    var first = null;
                    var last = null;
                    var target = null;
                    var length = this._vars.setItems.length;
                    this._vars.setItems.forEach(function(item, k) {
                        if (item[_this3.key] === key) target = k;
                        if (first === null && item.focused) first = k;
                        if (item.focused) last = k;
                    });
                    if ((target === 0 || target === length - 1) && first === null && last === null) return;
                    else if (first === null && last === null) this._vars.setItems[target].focused = true;
                    else if (target === 0 && last === length - 1 && !add) this._vars.setItems[first].focused = false;
                    else {
                        first = Math.min(target, first);
                        last = Math.max(target, last);
                        this._vars.setItems.forEach(function(item, k) {
                            item.focused = target === k || k >= first && k <= last;
                        });
                    }
                } else this._vars.setItems.forEach(function(item) {
                    if (ctrl) item.focused = item[_this.key] === key ? !item.focused : item.focused;
                    else item.focused = item[_this.key] === key;
                });
                return this;
            }
        },
        {
            key: "_defocusItem",
            value: function _defocusItem(key) {
                var _this = this;
                return this._vars.setItems.filter(function(item) {
                    if (item[_this.key] === key) item.focused = false;
                });
            }
        },
        {
            key: "_defocusItems",
            value: function _defocusItems() {
                this._vars.setItems.forEach(function(item) {
                    item.focused = false;
                });
                return this;
            }
        },
        {
            key: "_newItem",
            value: function _newItem(value) {
                var o = this._options;
                if (typeof value === 'string' && (!value.length || value.length < o.minLength)) return null;
                var item = this._getItem(value, o.itemData) || this._getSuggestedItem(value, o.itemData) || this._getAvailableItem(value, o.itemData);
                if (!item && o.newItems) {
                    // If validation is set and returns false - item should not be added.
                    if (typeof o.validateNewItem === 'function' && !o.validateNewItem(value)) return null;
                    var _obj;
                    item = (_obj = {
                        isNew: true
                    }, _helpers.defineProperty(_obj, this.key, guid()), _helpers.defineProperty(_obj, o.itemData, value), _obj);
                    this.emit('newToken', this, item);
                }
                if (item) {
                    this._addItem(item);
                    return item;
                }
                return null;
            }
        },
        {
            // Wrapper for build function in case some of the functions are overwritten.
            key: "_buildEl",
            value: function _buildEl(html) {
                return build(html);
            }
        },
        {
            key: "_getBounds",
            value: function _getBounds() {
                return this._html.container.getBoundingClientRect();
            }
        },
        {
            key: "_renderItems",
            value: function _renderItems() {
                var _this = this;
                var v = this._vars;
                var o = this._options;
                var html = this._html;
                html.items.innerHTML = '';
                v.setItems.forEach(function(item, k) {
                    var itemEl = _this._renderItem(item, k);
                    html.items.appendChild(itemEl);
                    item.el = itemEl;
                    if (item.focused) item.el.classList.add('focused');
                    else item.el.classList.remove('focused');
                });
                if (v.setItems.length > 1 && o.mode === 'tokenfield') html.input.setAttribute('placeholder', '');
                else if (o.mode === 'list') html.input.setAttribute('placeholder', o.placeholder);
                if (this._input) this._input.value = v.setItems.map(function(item) {
                    return item[o.singleInputValue];
                }).join(o.singleInputDelimiter);
                return this;
            }
        },
        {
            key: "_refreshItems",
            value: function _refreshItems() {
                var v = this._vars;
                v.setItems.forEach(function(item) {
                    if (item.el) {
                        if (item.focused) item.el.classList.add('focused');
                        else item.el.classList.remove('focused');
                    }
                });
            }
        },
        {
            key: "_renderItem",
            value: function _renderItem(item, k) {
                var o = this._options;
                var itemHtml = this.renderSetItemHtml(item);
                var label = itemHtml.querySelector('.item-label');
                var input = itemHtml.querySelector('.item-input');
                var remove = itemHtml.querySelector('.item-remove');
                var position = o.keepItemsOrder ? "[".concat(k, "]") : '[]';
                itemHtml.key = item[this.key];
                remove.key = item[this.key];
                input.setAttribute('name', (item.isNew ? o.newItemName : o.itemName) + position);
                input.value = item[item.isNew ? o.newItemValue : o.itemValue] || null;
                label.textContent = this.renderSetItemLabel(item);
                if (item.focused) itemHtml.classList.add('focused');
                return itemHtml;
            }
        },
        {
            key: "onInput",
            value: function onInput(value, e) {
                return value;
            }
        },
        {
            key: "renderSetItemHtml",
            value: function renderSetItemHtml() {
                return this._buildEl(this._templates.setItem);
            }
        },
        {
            key: "renderSetItemLabel",
            value: function renderSetItemLabel(item) {
                return item[this._options.itemLabel];
            }
        },
        {
            key: "renderSuggestions",
            value: function renderSuggestions(items) {
                var _this = this;
                var v = this._vars;
                var o = this._options;
                var html = this._html;
                var index = this._getSelectedItemIndex();
                if (!items.length) return this;
                if (o.maxSuggestWindow === 0) html.suggest.style.maxHeight = null;
                if (!v.suggestedItems.length) return this;
                if (!o.newItems && index === null) items[0].selected = true;
                var maxHeight = 0;
                items.every(function(item, k) {
                    if (k >= o.maxSuggest) return false;
                    var child = html.suggestList.childNodes[k];
                    var el = item.el = _this.renderSuggestedItem(item);
                    if (child) {
                        if (child.itemValue === item[o.itemValue]) {
                            child.key = item[_this.key];
                            item.el = child;
                        } else html.suggestList.replaceChild(el, child);
                    } else if (!child) html.suggestList.appendChild(el);
                    if (o.maxSuggestWindow > 0 && k < o.maxSuggestWindow) maxHeight += html.suggestList.childNodes[k].getBoundingClientRect().height;
                    if (o.maxSuggestWindow > 0 && k === o.maxSuggestWindow) html.suggest.style.maxHeight = maxHeight + 'px';
                    return true;
                });
                var overflow = html.suggestList.childElementCount - items.length;
                if (overflow > 0) for(var i = overflow - 1; i >= 0; i--)html.suggestList.removeChild(html.suggestList.childNodes[items.length + i]);
                return this;
            }
        },
        {
            key: "renderSuggestedItem",
            value: function renderSuggestedItem(item) {
                var o = this._options;
                var el = this._buildEl(this._templates.suggestItem);
                el.key = item[this.key];
                el.itemValue = item[o.itemValue];
                el.innerHTML = this.renderSuggestedItemContent(item);
                el.setAttribute('title', item[o.itemData]);
                if (item.selected) el.classList.add('selected');
                if (!o.filterSetItems) {
                    var setItem = this._getItem(item[o.itemValue], o.itemValue) || this._getItem(item[o.itemData], o.itemData);
                    if (setItem) el.classList.add('set');
                }
                return el;
            }
        },
        {
            key: "renderSuggestedItemContent",
            value: function renderSuggestedItemContent(item) {
                return item[this._options.itemData];
            }
        },
        {
            key: "_refreshSuggestions",
            value: function _refreshSuggestions() {
                var v = this._vars;
                var o = this._options;
                if (this._html.input.value.length < o.minChars) {
                    this.hideSuggestions();
                    return this;
                }
                var data = this._prepareData(o.items);
                var items = this._filterData(this._html.input.value, data);
                v.suggestedItems = o.filterSetItems ? this._filterSetItems(items) : items;
                if (v.suggestedItems.length) {
                    if (!o.maxItems || o.maxItems && v.setItems.length < o.maxItems) {
                        this.renderSuggestions(v.suggestedItems);
                        return this;
                    }
                }
                this.hideSuggestions();
                return this;
            }
        },
        {
            key: "showSuggestions",
            value: function showSuggestions() {
                var v = this._vars;
                var o = this._options;
                if (v.suggestedItems.length) {
                    this.emit('showSuggestions', this);
                    if (!o.maxItems || o.maxItems && v.setItems.length < o.maxItems) {
                        this._html.suggest.style.display = 'block';
                        v.suggested = true;
                        this.renderSuggestions(v.suggestedItems);
                    }
                    this.emit('shownSuggestions', this);
                } else this.hideSuggestions();
                return this;
            }
        },
        {
            key: "hideSuggestions",
            value: function hideSuggestions() {
                this.emit('hideSuggestions', this);
                this._vars.suggested = false;
                this._html.suggest.style.display = 'none';
                this._html.suggestList.innerHTML = '';
                this.emit('hiddenSuggestions', this);
                return this;
            }
        },
        {
            key: "setSuggestedItems",
            value: function setSuggestedItems(items) {
                if (!Array.isArray(items)) throw new Error('Argument must be an array of objects.');
                this._options.items = items;
                this._refreshSuggestions();
            }
        },
        {
            key: "getItems",
            value: function getItems() {
                var _this = this;
                return this._vars.setItems.map(function(item) {
                    var v = Object.assign({}, item);
                    delete v[_this.key];
                    delete v.el;
                    return v;
                });
            }
        },
        {
            key: "setItems",
            value: function setItems() {
                var items = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
                this._vars.setItems = [];
                this.addItems(items);
                return this;
            }
        },
        {
            key: "addItems",
            value: function addItems() {
                var items = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
                var _this = this;
                var key = this._options.itemValue;
                if (!Array.isArray(items)) items = [
                    items
                ];
                this._prepareData(items).forEach(function(item) {
                    if (item.isNew || typeof item[key] !== 'undefined') _this._addItem(item);
                });
                this._minimizeInput()._renderItems()._refreshInput().hideSuggestions();
                return this;
            }
        },
        {
            key: "sortItems",
            value: function sortItems() {
                var _this = this;
                var items = [];
                _helpers.toConsumableArray(this._html.items.childNodes).forEach(function(el) {
                    var item = _this._getItem(el.key);
                    if (item) items.push(item);
                });
                this.setItems(items);
            }
        },
        {
            key: "removeItem",
            value: function removeItem(value) {
                var o = this._options;
                if (typeof value === 'object' && (value[o.itemValue] || value[o.newItemValue])) value = value[o.itemValue] || value[o.newItemValue];
                var item = this._getItem(value, o.itemValue) || this._getItem(value, o.newItemValue);
                if (!item) return this;
                this._removeItem(item[this.key])._renderItems();
                return this;
            }
        },
        {
            key: "emptyItems",
            value: function emptyItems() {
                this._vars.setItems = [];
                this._renderItems()._refreshInput().hideSuggestions();
                this.emit('change', this);
                return this;
            }
        },
        {
            key: "getSuggestedItems",
            value: function getSuggestedItems() {
                return this._vars.suggestedItems.map(function(item) {
                    return Object.assign({}, item);
                });
            }
        },
        {
            key: "focus",
            value: function focus() {
                this._html.container.classList.add('focused');
                if (!this._focused) this._html.input.focus();
                return this;
            }
        },
        {
            key: "blur",
            value: function blur() {
                this._html.container.classList.remove('focused');
                if (this._focused) this._html.input.blur();
                return this;
            }
        },
        {
            key: "remove",
            value: function remove() {
                var html = this._html;
                html.container.parentElement.insertBefore(this.el, html.container);
                html.container.remove();
                this.el.style.display = 'block';
                if (Object.keys(_tokenfields).length === 1) {
                    document.removeEventListener('mousedown', this._vars.events.onMouseDown);
                    window.removeEventListener('resize', this._vars.events.onResize);
                }
                if (this._form && this._form.nodeName) this._form.removeEventListener('reset', this._vars.events.onReset);
                delete _tokenfields[this.id];
                delete this.el.tokenfield;
            }
        }
    ]);
    return Tokenfield;
}(_eventsDefault.default);
exports.default = Tokenfield;

},{"@swc/helpers":"3OBsq","events":"gMB6n","./ajax.js":"7c25u","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"gMB6n":[function(require,module,exports) {
var _helpers = require("@swc/helpers");
// Copyright Joyent, Inc. and other Node contributors.
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to permit
// persons to whom the Software is furnished to do so, subject to the
// following conditions:
//
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
// OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
// NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
// USE OR OTHER DEALINGS IN THE SOFTWARE.
'use strict';
var R = typeof Reflect === 'object' ? Reflect : null;
var ReflectApply = R && typeof R.apply === 'function' ? R.apply : function ReflectApply(target, receiver, args) {
    return Function.prototype.apply.call(target, receiver, args);
};
var ReflectOwnKeys;
if (R && typeof R.ownKeys === 'function') ReflectOwnKeys = R.ownKeys;
else if (Object.getOwnPropertySymbols) ReflectOwnKeys = function ReflectOwnKeys(target) {
    return Object.getOwnPropertyNames(target).concat(Object.getOwnPropertySymbols(target));
};
else ReflectOwnKeys = function ReflectOwnKeys(target) {
    return Object.getOwnPropertyNames(target);
};
function ProcessEmitWarning(warning) {
    if (console && console.warn) console.warn(warning);
}
var NumberIsNaN = Number.isNaN || function NumberIsNaN(value) {
    return value !== value;
};
function EventEmitter() {
    EventEmitter.init.call(this);
}
module.exports = EventEmitter;
module.exports.once = once;
// Backwards-compat with node 0.10.x
EventEmitter.EventEmitter = EventEmitter;
EventEmitter.prototype._events = undefined;
EventEmitter.prototype._eventsCount = 0;
EventEmitter.prototype._maxListeners = undefined;
// By default EventEmitters will print a warning if more than 10 listeners are
// added to it. This is a useful default which helps finding memory leaks.
var defaultMaxListeners = 10;
function checkListener(listener) {
    if (typeof listener !== 'function') throw new TypeError('The "listener" argument must be of type Function. Received type ' + (typeof listener === "undefined" ? "undefined" : _helpers.typeOf(listener)));
}
Object.defineProperty(EventEmitter, 'defaultMaxListeners', {
    enumerable: true,
    get: function get() {
        return defaultMaxListeners;
    },
    set: function set(arg) {
        if (typeof arg !== 'number' || arg < 0 || NumberIsNaN(arg)) throw new RangeError('The value of "defaultMaxListeners" is out of range. It must be a non-negative number. Received ' + arg + '.');
        defaultMaxListeners = arg;
    }
});
EventEmitter.init = function() {
    if (this._events === undefined || this._events === Object.getPrototypeOf(this)._events) {
        this._events = Object.create(null);
        this._eventsCount = 0;
    }
    this._maxListeners = this._maxListeners || undefined;
};
// Obviously not all Emitters should be limited to 10. This function allows
// that to be increased. Set to zero for unlimited.
EventEmitter.prototype.setMaxListeners = function setMaxListeners(n) {
    if (typeof n !== 'number' || n < 0 || NumberIsNaN(n)) throw new RangeError('The value of "n" is out of range. It must be a non-negative number. Received ' + n + '.');
    this._maxListeners = n;
    return this;
};
function _getMaxListeners(that) {
    if (that._maxListeners === undefined) return EventEmitter.defaultMaxListeners;
    return that._maxListeners;
}
EventEmitter.prototype.getMaxListeners = function getMaxListeners() {
    return _getMaxListeners(this);
};
EventEmitter.prototype.emit = function emit(type) {
    var args = [];
    for(var i = 1; i < arguments.length; i++)args.push(arguments[i]);
    var doError = type === 'error';
    var events = this._events;
    if (events !== undefined) doError = doError && events.error === undefined;
    else if (!doError) return false;
    // If there is no 'error' event listener then throw.
    if (doError) {
        var er;
        if (args.length > 0) er = args[0];
        if (er instanceof Error) // Note: The comments on the `throw` lines are intentional, they show
        // up in Node's output if this results in an unhandled exception.
        throw er; // Unhandled 'error' event
        // At least give some kind of context to the user
        var err = new Error('Unhandled error.' + (er ? ' (' + er.message + ')' : ''));
        err.context = er;
        throw err; // Unhandled 'error' event
    }
    var handler = events[type];
    if (handler === undefined) return false;
    if (typeof handler === 'function') ReflectApply(handler, this, args);
    else {
        var len = handler.length;
        var listeners = arrayClone(handler, len);
        for(var i = 0; i < len; ++i)ReflectApply(listeners[i], this, args);
    }
    return true;
};
function _addListener(target, type, listener, prepend) {
    var m;
    var events;
    var existing;
    checkListener(listener);
    events = target._events;
    if (events === undefined) {
        events = target._events = Object.create(null);
        target._eventsCount = 0;
    } else {
        // To avoid recursion in the case that type === "newListener"! Before
        // adding it to the listeners, first emit "newListener".
        if (events.newListener !== undefined) {
            target.emit('newListener', type, listener.listener ? listener.listener : listener);
            // Re-assign `events` because a newListener handler could have caused the
            // this._events to be assigned to a new object
            events = target._events;
        }
        existing = events[type];
    }
    if (existing === undefined) {
        // Optimize the case of one listener. Don't need the extra array object.
        existing = events[type] = listener;
        ++target._eventsCount;
    } else {
        if (typeof existing === 'function') // Adding the second element, need to change to array.
        existing = events[type] = prepend ? [
            listener,
            existing
        ] : [
            existing,
            listener
        ];
        else if (prepend) existing.unshift(listener);
        else existing.push(listener);
        // Check for listener leak
        m = _getMaxListeners(target);
        if (m > 0 && existing.length > m && !existing.warned) {
            existing.warned = true;
            // No error code for this since it is a Warning
            // eslint-disable-next-line no-restricted-syntax
            var w = new Error('Possible EventEmitter memory leak detected. ' + existing.length + ' ' + String(type) + ' listeners ' + 'added. Use emitter.setMaxListeners() to ' + 'increase limit');
            w.name = 'MaxListenersExceededWarning';
            w.emitter = target;
            w.type = type;
            w.count = existing.length;
            ProcessEmitWarning(w);
        }
    }
    return target;
}
EventEmitter.prototype.addListener = function addListener(type, listener) {
    return _addListener(this, type, listener, false);
};
EventEmitter.prototype.on = EventEmitter.prototype.addListener;
EventEmitter.prototype.prependListener = function prependListener(type, listener) {
    return _addListener(this, type, listener, true);
};
function onceWrapper() {
    if (!this.fired) {
        this.target.removeListener(this.type, this.wrapFn);
        this.fired = true;
        if (arguments.length === 0) return this.listener.call(this.target);
        return this.listener.apply(this.target, arguments);
    }
}
function _onceWrap(target, type, listener) {
    var state = {
        fired: false,
        wrapFn: undefined,
        target: target,
        type: type,
        listener: listener
    };
    var wrapped = onceWrapper.bind(state);
    wrapped.listener = listener;
    state.wrapFn = wrapped;
    return wrapped;
}
EventEmitter.prototype.once = function once(type, listener) {
    checkListener(listener);
    this.on(type, _onceWrap(this, type, listener));
    return this;
};
EventEmitter.prototype.prependOnceListener = function prependOnceListener(type, listener) {
    checkListener(listener);
    this.prependListener(type, _onceWrap(this, type, listener));
    return this;
};
// Emits a 'removeListener' event if and only if the listener was removed.
EventEmitter.prototype.removeListener = function removeListener(type, listener) {
    var list, events, position, i, originalListener;
    checkListener(listener);
    events = this._events;
    if (events === undefined) return this;
    list = events[type];
    if (list === undefined) return this;
    if (list === listener || list.listener === listener) {
        if (--this._eventsCount === 0) this._events = Object.create(null);
        else {
            delete events[type];
            if (events.removeListener) this.emit('removeListener', type, list.listener || listener);
        }
    } else if (typeof list !== 'function') {
        position = -1;
        for(i = list.length - 1; i >= 0; i--)if (list[i] === listener || list[i].listener === listener) {
            originalListener = list[i].listener;
            position = i;
            break;
        }
        if (position < 0) return this;
        if (position === 0) list.shift();
        else spliceOne(list, position);
        if (list.length === 1) events[type] = list[0];
        if (events.removeListener !== undefined) this.emit('removeListener', type, originalListener || listener);
    }
    return this;
};
EventEmitter.prototype.off = EventEmitter.prototype.removeListener;
EventEmitter.prototype.removeAllListeners = function removeAllListeners(type) {
    var listeners, events, i;
    events = this._events;
    if (events === undefined) return this;
    // not listening for removeListener, no need to emit
    if (events.removeListener === undefined) {
        if (arguments.length === 0) {
            this._events = Object.create(null);
            this._eventsCount = 0;
        } else if (events[type] !== undefined) {
            if (--this._eventsCount === 0) this._events = Object.create(null);
            else delete events[type];
        }
        return this;
    }
    // emit removeListener for all listeners on all events
    if (arguments.length === 0) {
        var keys = Object.keys(events);
        var key;
        for(i = 0; i < keys.length; ++i){
            key = keys[i];
            if (key === 'removeListener') continue;
            this.removeAllListeners(key);
        }
        this.removeAllListeners('removeListener');
        this._events = Object.create(null);
        this._eventsCount = 0;
        return this;
    }
    listeners = events[type];
    if (typeof listeners === 'function') this.removeListener(type, listeners);
    else if (listeners !== undefined) // LIFO order
    for(i = listeners.length - 1; i >= 0; i--)this.removeListener(type, listeners[i]);
    return this;
};
function _listeners(target, type, unwrap) {
    var events = target._events;
    if (events === undefined) return [];
    var evlistener = events[type];
    if (evlistener === undefined) return [];
    if (typeof evlistener === 'function') return unwrap ? [
        evlistener.listener || evlistener
    ] : [
        evlistener
    ];
    return unwrap ? unwrapListeners(evlistener) : arrayClone(evlistener, evlistener.length);
}
EventEmitter.prototype.listeners = function listeners(type) {
    return _listeners(this, type, true);
};
EventEmitter.prototype.rawListeners = function rawListeners(type) {
    return _listeners(this, type, false);
};
EventEmitter.listenerCount = function(emitter, type) {
    if (typeof emitter.listenerCount === 'function') return emitter.listenerCount(type);
    else return listenerCount.call(emitter, type);
};
EventEmitter.prototype.listenerCount = listenerCount;
function listenerCount(type) {
    var events = this._events;
    if (events !== undefined) {
        var evlistener = events[type];
        if (typeof evlistener === 'function') return 1;
        else if (evlistener !== undefined) return evlistener.length;
    }
    return 0;
}
EventEmitter.prototype.eventNames = function eventNames() {
    return this._eventsCount > 0 ? ReflectOwnKeys(this._events) : [];
};
function arrayClone(arr, n) {
    var copy = new Array(n);
    for(var i = 0; i < n; ++i)copy[i] = arr[i];
    return copy;
}
function spliceOne(list, index) {
    for(; index + 1 < list.length; index++)list[index] = list[index + 1];
    list.pop();
}
function unwrapListeners(arr) {
    var ret = new Array(arr.length);
    for(var i = 0; i < ret.length; ++i)ret[i] = arr[i].listener || arr[i];
    return ret;
}
function once(emitter, name) {
    return new Promise(function(resolve, reject) {
        var errorListener = function errorListener(err) {
            emitter.removeListener(name, resolver);
            reject(err);
        };
        var resolver = function resolver() {
            if (typeof emitter.removeListener === 'function') emitter.removeListener('error', errorListener);
            resolve([].slice.call(arguments));
        };
        eventTargetAgnosticAddListener(emitter, name, resolver, {
            once: true
        });
        if (name !== 'error') addErrorHandlerIfEventEmitter(emitter, errorListener, {
            once: true
        });
    });
}
function addErrorHandlerIfEventEmitter(emitter, handler, flags) {
    if (typeof emitter.on === 'function') eventTargetAgnosticAddListener(emitter, 'error', handler, flags);
}
function eventTargetAgnosticAddListener(emitter, name, listener, flags) {
    if (typeof emitter.on === 'function') {
        if (flags.once) emitter.once(name, listener);
        else emitter.on(name, listener);
    } else if (typeof emitter.addEventListener === 'function') // EventTarget does not have `error` event semantics like Node
    // EventEmitters, we do not listen for `error` events here.
    emitter.addEventListener(name, function wrapListener(arg) {
        // IE does not have builtin `{ once: true }` support so we
        // have to do it manually.
        if (flags.once) emitter.removeEventListener(name, wrapListener);
        listener(arg);
    });
    else throw new TypeError('The "emitter" argument must be of type EventEmitter. Received type ' + (typeof emitter === "undefined" ? "undefined" : _helpers.typeOf(emitter)));
}

},{"@swc/helpers":"3OBsq"}],"7c25u":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
function ajax(params) {
    var options = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, callback = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : null;
    var xhr = new XMLHttpRequest();
    var url = options.url;
    var paramsArr = [];
    for(var key in params)paramsArr.push("".concat(key, "=").concat(encodeURIComponent(params[key])));
    var paramsString = paramsArr.join('&');
    if (options.type.toLowerCase() === 'get') url += '?' + paramsString;
    xhr.open(options.type, url, true);
    for(var header in options.headers){
        var value = options.headers[header];
        if (typeof value === 'function') value = value(params, options);
        xhr.setRequestHeader(header, value);
    }
    if (callback) xhr.onreadystatechange = callback;
    xhr.send(params);
    return xhr;
}
exports.default = ajax;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"6WNFi":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
// Hide show destinations list.
var MAX_COUNTRIES_TO_DISPLAY = 3;
var hideItems = function(countries) {
    return countries.forEach(function(country, index) {
        if (index > MAX_COUNTRIES_TO_DISPLAY - 1) country.classList.add("app-hidden--force");
    });
};
var initDestinationsList = function() {
    var destinationsList = document.querySelectorAll(".destinations__list");
    destinationsList.forEach(function(destinations) {
        var items = destinations.querySelectorAll("li");
        if (items.length <= MAX_COUNTRIES_TO_DISPLAY) return;
        hideItems(items);
        var hidden = true;
        var td = destinations.parentElement;
        var button = document.createElement("button");
        button.className = "lite-button--link";
        button.innerText = "View all (".concat(items.length, ")");
        td.appendChild(button);
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (hidden) {
                items.forEach(function(item) {
                    return item.classList.remove("app-hidden--force");
                });
                hidden = false;
                button.innerText = "View less";
            } else {
                hideItems(items);
                hidden = true;
                button.innerText = "View all (".concat(items.length, ")");
            }
        });
    });
};
exports.default = initDestinationsList;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"dZDBQ":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var createTokenFieldSetItem = function(cleName) {
    suggestionSplit = cleName.split(" ");
    suggestion = suggestionSplit[suggestionSplit.length - 1];
    var inputSuggestion = document.querySelector("#control_list_entries").querySelector(".tokenfield-set").querySelector("ul");
    var newLi = document.createElement("li");
    newLi.classList.add("tokenfield-set-item");
    var newSpan = document.createElement("span");
    newSpan.classList.add("item-label");
    newSpan.innerText = suggestion;
    var newHref = document.createElement("a");
    newHref.classList.add("item-remove");
    newHref.tabIndex = -1;
    newHref.innerText = "×";
    newHref.href = "#";
    var newInput = document.createElement("input");
    newInput.classList.add("item-input");
    newInput.type = "hidden";
    newInput.name = "control_list_entries";
    newInput.value = suggestion;
    newLi.append(newSpan, newHref, newInput);
    inputSuggestion.appendChild(newLi);
};
var initTauControlListEntry = function() {
    var cleList = document.querySelectorAll(".control-list__list");
    var checkboxProducts = document.querySelectorAll("[id^='id_goods_']");
    cleList.forEach(function(cle) {
        return cle.addEventListener("click", function(event) {
            createTokenFieldSetItem(event.target.innerText);
        });
    });
    checkboxProducts.forEach(function(product) {
        product.addEventListener("click", function() {
            checked = product.checked;
            id = product.value;
            cleList.forEach(function(cle) {
                if (checked) {
                    id === cle.getAttribute("name") && cle.classList.remove("app-hidden--force");
                    return;
                }
                cle.classList.add("app-hidden--force");
            });
        });
    });
};
exports.default = initTauControlListEntry;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"2orud":[function() {},{}],"R1Zup":[function() {},{}]},["1tmhj","eqetV"], "eqetV", "parcelRequire4557")

//# sourceMappingURL=main.js.map
