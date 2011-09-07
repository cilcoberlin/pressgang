(function($) {

/**
 * A class that adds functionality to the version-selection table.
 *
 * This primarily makes it easier to select a version by making the entire row
 * of a version select the version radio button.
 */
var VersionSelectionTable = function() {

	// Select a version when clicking on its table row
	$(VersionSelectionTable.CSS.version).click(this.selectVersionForRow);
};

/**
 * CSS identifers used with the version-selection table.
 */
VersionSelectionTable.CSS = {
	selectVersion: "input[name=snapshot]",
	version: ".version"
};

/**
 * Selects a version whenever a click is made on the row that contains its
 * form selection element.
 */
VersionSelectionTable.prototype.selectVersionForRow = function(e) {
	$(this).find(VersionSelectionTable.CSS.selectVersion).attr('checked', 'checked');
};

/**
 * Add interactivity to the version-selection page.
 */
$(document).ready(function() {
	new VersionSelectionTable();
});

})(jQuery);
