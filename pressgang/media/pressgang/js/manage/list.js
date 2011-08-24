(function(window, $, pressgang) {

var manage = {
	css: {
		blogList: '#all-blogs'
	}
};

$(document).ready(function() {

	// Make the blogs table sortable
	$(manage.css.blogList).tablesorter({

		// Disable sorting on the actions column
		headers: {
			4: { sorter: false }
		},

		// Search for date meta on the date columns
		textExtraction: pressgang.utils.sortTableWithMeta
	});

});

})(window, jQuery, pressgang);
