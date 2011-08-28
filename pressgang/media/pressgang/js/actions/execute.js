(function($, pressgang) {

// A class to execute an action
var Executer = function(options) {

	// Get the URL to start the action
	this.executeURL = options.executeURL;

	// Create a progress monitor to track the execution of the action
	this.monitor = new ProgressMonitor(options.progressURL, options.progressContainer)
};

//Set the action in motion and poll for updates
Executer.prototype.execute = function() {
	$.ajax({
		dataType: 'json',
		url: this.executeURL
	});
	this.monitor.beginUpdating();
};

// A class to display progress updates for an action
var ProgressMonitor = function(url, container) {

	// Get the URL that will give us progress reports
	this.url = url;

	// Get a reference to the element that will display the progress updates
	this.$log = $(container);

	// Cache the viewport height
	this.windowHeight = $(window).height();

	// Whether or not to keep polling for updates
	this.keepUpdating = false;

	// Keep track of the content length of the returned markup
	this.contentLength = 0;
};

// CSS identifiers
ProgressMonitor.CSS = {
	activeStep:    ".follow",
	currentAction: ".action.in-progress",
	pulseClass:    "pulse"
};

// How often to poll for updates
ProgressMonitor.POLL_INTERVAL_MS = 1000;

// How fast to scroll to the newest log step
ProgressMonitor.SCROLL_SPEED_MS = 250;

// Display the installation progress to the user
ProgressMonitor.prototype._renderUpdate = function(data) {

	// Update the markup if the content has changed
	if (data.size != this.contentLength) {
		this.contentLength = data.size;

		// Update the progress log
		this.$log.html(data.markup.log);

		// Pulse the text of the current step
		this.$log.find(ProgressMonitor.CSS.currentAction).stop().
			switchClass("", ProgressMonitor.CSS.pulseClass, ProgressMonitor.POLL_INTERVAL_MS / 2).
			switchClass(ProgressMonitor.CSS.pulseClass, "", ProgressMonitor.POLL_INTERVAL_MS / 2);

		// Scroll the page to the most recent step
		var $follow = this.$log.find(ProgressMonitor.CSS.activeStep);
		if ($follow.length) {
			var followBottom = $follow.offset().top + $follow.outerHeight();
			var scrollTo = followBottom - this.windowHeight;
			$("html:not(:animated),body:not(:animated)").animate(
				{scrollTop: scrollTo + 50}, ProgressMonitor.SCROLL_SPEED_MS);
		}
	}

	// If the installation has ended, stop refreshing the log, otherwise
	// continue polling for updates
	if (data.ended) {
		this._endUpdating();
	} else if (this.keepUpdating) {
		setTimeout(this._requestUpdateProxy, ProgressMonitor.POLL_INTERVAL_MS);
	}
};

// Request an update on the installation
ProgressMonitor.prototype._requestUpdate = function() {
	$.ajax({
		dataType: 'json',
		success: this._renderUpdateProxy,
		url: this.url
	});
};

// Stop polling for updates
ProgressMonitor.prototype._endUpdating = function() {
	this.keepUpdating = false;
};

// Begin polling for installation progress updates
ProgressMonitor.prototype.beginUpdating = function() {
	this.keepUpdating = true;
	this._renderUpdateProxy = $.proxy(this._renderUpdate, this);
	this._requestUpdateProxy = $.proxy(this._requestUpdate, this);
	this._requestUpdate();
};

// Make the executer available to other scripts
pressgang.actions.Executer = Executer;

})(jQuery, pressgang);
