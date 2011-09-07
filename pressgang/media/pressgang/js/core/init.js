(function(window) {

/**
 * Core namespaces used by PressGang.
 */
var pressgang = {
	actions: {},
	install: {},
	utils:   {}
};

/**
 * Create an alias for django's JavaScript i18n functions.
 */
pressgang.gettext = window.gettext;
pressgang.ngettext = window.ngettext;

/**
 * The prefix used to indicate sorting metadata contained in a class, which is
 * read when a table is made sortable using the sortTableWithMeta function.
 */
pressgang.utils.SORT_META_PREFIX = "sort__";

/**
 * A function that can be assigned as the value of textExtraction in the options
 * of a sortable table created using the jQuery tablesorter plugin.
 *
 * This examines the classes of any sorted cells and looks for a class named
 * sort__DATA.  If such a class is found, the value of DATA is used to sort
 * the cell.  Otherwise, the inner HTML of the cell is used.
 */
pressgang.utils.sortTableWithMeta = function(node) {
	var text = node.innerHTML;
	var prefixPos = node.className.indexOf(pressgang.utils.SORT_META_PREFIX);
	if (prefixPos > -1) {
		sortClass = node.className.substr(prefixPos + pressgang.utils.SORT_META_PREFIX.length);
		text = sortClass.split(' ')[0];
	}
	return text;
};

/**
 * Get the error text from a jqXHR response if there is response text.  If there
 * isn't any, use the default error message.
 */
pressgang.utils.getErrorText = function(xhr, errorText) {
	if (xhr.hasOwnProperty('responseText') && xhr.responseText) {
		errorText = xhr.responseText;
	}
	return errorText;
};

/**
 * Return true when the given object is empty.
 */
pressgang.utils.objectIsEmpty = function(obj) {
	for (var prop in obj) {
		if (obj.hasOwnProperty(prop)) {
			return false;
		}
	}
	return true;
};

// Expose PressGang to the global namespace
window.pressgang = pressgang;

})(window);
