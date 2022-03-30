var LITECommon = LITECommon || {};
import "./import-jquery";
import {
  enableLink,
  enableButton,
  disableButton,
  disableLink,
} from "./helpers";
window.enableLink = enableLink;
window.enableButton = enableButton;
window.disableLink = disableLink;
window.disableButton = disableButton;

import Modal from "../../../core/assets/javascripts/modal.js";
LITECommon.Modal = Modal;

window.LITECommon = LITECommon;
