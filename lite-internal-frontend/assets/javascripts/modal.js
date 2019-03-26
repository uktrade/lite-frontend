var LITECommon = LITECommon || {};

LITECommon.Modal = {
	modalBackground: {},
	modal: {},
	container: {},
	backButton: {},
	closeButton: {},
  	focusableElementsString: 'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, *[tabindex], *[contenteditable]',
	previouslyFocusedElement: {},

	showModal: function(title, content, hideCloseButton = false) {
		// Generate modal container if it doesn't exist
		if (!$("#modal-background").length) {
			let closeText = "<a id='modal-close-button' class='govuk-link' href='#'>Close<span class='govuk-visually-hidden'> popover</span></a>";

			if (hideCloseButton) {
				closeText = "";
			}

			$("body").append("<div id='modal-background'><div id='modal'><div id='modal-aria-description' class='govuk-visually-hidden'>Press escape to close this popover</div><div id='modal-header'><a id='modal-back-button' class='govuk-link' href='#'>Back</a>" + closeText + "</div><div id='modal-contents'></div></div></div>")

			// Bind
			this.modalBackground = $("#modal-background");
			this.modal = $("#modal");
			this.container = $("#modal-contents");
			this.backButton = $("#modal-back-button");
			this.closeButton = $("#modal-close-button");
		}

		// Show modal
		this.modalBackground.show();
		$("html, body").addClass("has-modal");

		// Hide existing modal content and show back button if necessary
		if ($(".modal-content").length > 0) {
			this.backButton.text("Back to " + $(".modal-content").last().children($("h2")).first().text());
			$(".modal-content").hide();
			this.backButton.show();
		} else {
			// Focus on close button if new modal
			this.previouslyFocusedElement = $(':focus');
			this.closeButton.focus();
		}

		// Append
		this.container.append("<div class='modal-content'>" + "<h2 class='govuk-heading-m'>" + title + "</h2>" + content + "</div>");

		// Bind events
		LITECommon.Modal.bindEvents();
	},

	closeTopModal: function() {
		$(".modal-content").last().remove();
		$(".modal-content").last().show();

		if ($(".modal-content").length == 1) {
			this.backButton.hide();
		} else {
			// Get element before last element
			this.backButton.text("Back to " + $(".modal-content").eq(-2).children($("h2")).first().text());
		}
	},

	closeAllModals: function() {
		this.modalBackground.remove();
		$("html, body").removeClass("has-modal");
		this.previouslyFocusedElement.focus();
	},


	focusOnFirstElement: function() {
		"use strict";

		var $elms = LITECommon.Modal.getFocusableElements();

		if ($elms.length > 0) {
			$elms[0].focus();
		}
	},

	bindEvents: function() {
		"use strict";

		// Keydown events
		$('body').off('keydown.LITECommon.Modal').on('keydown.LITECommon.Modal', function(e) {
			// Escape key closes all modals
			if (e.which === 27) {
				LITECommon.Modal.closeAllModals();
			}

			// Trap tab key
			if (e.which === 9) {
				LITECommon.Modal.trapTabKey(e);
			}
		});

		LITECommon.Modal.backButton.off('click').on("click", function() {
			LITECommon.Modal.closeTopModal();
			return false;
		});

		LITECommon.Modal.closeButton.off('click').on("click", function() {
			LITECommon.Modal.closeAllModals();
			return false;
		});


		// If anything other than the modal gets focus (eg tabbing from address bar), force focus into the modal
		$('body>*[id!=' + LITECommon.Modal.overlayID + ']').on('focusin.LITECommon.Modal', function(event) {
			LITECommon.Modal.focusOnFirstElement();
			event.stopPropagation();
		});
	},

	trapTabKey: function(event) {
		"use strict";

		var $focusableElms = LITECommon.Modal.getFocusableElements();
		var $focusedElm = $(':focus');

		var focusedElmIndex = $focusableElms.index($focusedElm);

		if (event.shiftKey && focusedElmIndex === 0) {
			// If we're going backwards (shift-tab) and we're at the first focusable element,
			// loop back to last focusable element
			$focusableElms.get($focusableElms.length - 1).focus();
			event.preventDefault();
		} else if (!event.shiftKey && focusedElmIndex === $focusableElms.length - 1) {
			// If we're going forwards and we're at the last focusable element,
			// loop forwards to the first focusable element
			$focusableElms.get(0).focus();
			event.preventDefault();
		}
		// Otherwise, allow the tab to proceed as normal because we're still in the group of
		// focusable elements in the modal
	},

	/**
	 * Finds all of the focusable elements inside the modal
	 * @returns {jQuery} collection of the focusable elements inside the modal
	 * @private
	 */
	getFocusableElements: function() {
		"use strict";

		return $('#modal').find('*').filter(LITECommon.Modal.focusableElementsString).filter(':visible');
	},

	/**
	 * Escapes a string by converting characters that could be part of HTML tags to entities
	 * @param string The string to escape
	 * @returns {string} the escaped string
	 * @private
	 */
	escapeHtml: function(string) {
		"use strict";

		var entityMap = {
			'&': '&amp;',
			'<': '&lt;',
			'>': '&gt;',
			'"': '&quot;',
			"'": '&#39;',
			'/': '&#x2F;',
			'`': '&#x60;',
			'=': '&#x3D;'
		};

		return String(string).replace(/[&<>"'`=\/]/g, function(s) {
			return entityMap[s];
		});
	}
};
