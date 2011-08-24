
var pressgang = {
	actions: {},
	install: {},
	utils:   {}
};

// The prefix used to indicate sorting metadata
pressgang.utils.SORT_META_PREFIX = "sort__";

/*
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
