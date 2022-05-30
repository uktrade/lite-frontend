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
})({"99zvQ":[function(require,module,exports) {
"use strict";
var HMR_HOST = null;
var HMR_PORT = 1234;
var HMR_SECURE = false;
var HMR_ENV_HASH = "30f6e5d8ea47961b";
module.bundle.HMR_BUNDLE_ID = "5d7531f44b6c17f9";
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

},{}],"5LSAo":[function(require,module,exports) {
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

},{"@swc/helpers":"3OBsq","tokenfield":"hWHxu","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"3OBsq":[function(require,module,exports) {
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

},{"./_construct":"fWjGA","./_is_native_function":"6NiqX","./_get_prototype_of":"6HtCT","./_set_prototype_of":"lLpOg","@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}],"hWHxu":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
var _helpers = require("@swc/helpers");
/**
 * Input field with tagging/token/chip capabilities written in raw JavaScript
 * tokenfield 1.5.0 <https://github.com/KaneCohen/tokenfield>
 * Copyright 2022 Kane Cohen <https://github.com/KaneCohen>
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
                if (o.mode === 'tokenfield') this._minimizeInput()._resizeInput();
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
                    delete v.focused;
                    delete v.selected;
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

},{"@parcel/transformer-js/src/esmodule-helpers.js":"bt0mQ"}]},["99zvQ","5LSAo"], "5LSAo", "parcelRequire4557")

//# sourceMappingURL=review-good.js.map
