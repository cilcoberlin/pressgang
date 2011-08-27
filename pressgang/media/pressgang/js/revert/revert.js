(function($, pressgang) {

var revert = {
	css: {
		version: ".version",
		selectVersion: "input[name=snapshot]"
	}
};

// Make clicking on a table row select that version
revert.selectVersion = function(e) {
	$(this).find(revert.css.selectVersion).attr('checked', 'checked');
}

$(document).ready(function() {

	// Select a version when clicking on its table row
	$(revert.css.version).click(revert.selectVersion);
});

})(jQuery, pressgang);
