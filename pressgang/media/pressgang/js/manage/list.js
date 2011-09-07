(function($, pressgang) {

/**
 * CSS identifiers used for the blog management page.
 */
var css = {
	blogList: '#all-blogs'
};

/**
 * Makes the list of installed blogs sortable.
 */
var makeBlogListSortable = function() {
	$(css.blogList).tablesorter({

		// Disable sorting on the actions column
		headers: {
			0: { sorter: false }
		},

		// Search for date meta on the date columns
		textExtraction: pressgang.utils.sortTableWithMeta
	});
};

/**
 * Add interactivity to the blog management page
 */
$(document).ready(function() {
	makeBlogListSortable();
});

})(jQuery, pressgang);
