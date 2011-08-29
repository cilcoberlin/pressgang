(function($, pressgang) {

var execute = {};

// Display an error to the user
execute.showError = function(text) {
	alert(text);
}

// A class to execute an action
var Executer = function(options) {

	// Get the URL to start the action
	this.executeURL = options.executeURL;

	// Get the error message to display
	this.errorMessage = options.errorMessage;

	// Create a progress monitor to track the execution of the action
	this.monitor = new ProgressMonitor(options.progressURL, options.progressContainer, options.errorMessage)
};

//Set the action in motion and poll for updates
Executer.prototype.execute = function() {
	$.ajax({
		dataType: 'json',
		error: $.proxy(this._handleError, this),
		success: $.proxy(this._monitorLog, this),
		url: this.executeURL
	});
};

// Begin monitoring the log if the action has been properly started
Executer.prototype._monitorLog = function(data) {
	this.monitor.beginUpdating();
};

// Handle an error when the action cannot be started
Executer.prototype._handleError = function(xhr, status) {
	execute.showError(pressgang.utils.getErrorText(xhr, this.errorMessage));
};

// A class to display progress updates for an action
var ProgressMonitor = function(url, container, errorMessage) {

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

	// The error message to display when updating breaks
	this.errorMessage = errorMessage;

	this._pulseCurrentActionProxy = $.proxy(this._pulseCurrentAction, this);
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

// How fast to pulse the current action
ProgressMonitor.PULSE_DURATION_MS = 250;

// Pulsing colors
ProgressMonitor.PULSE_START_COLOR = "#000000";
ProgressMonitor.PULSE_END_COLOR   = "#aa0000";

// Display the installation progress to the user
ProgressMonitor.prototype._renderUpdate = function(data) {

	// Update the markup if the content has changed
	if (data.size !== this.contentLength) {
		this.contentLength = data.size;

		// Update the progress log
		this.$log.html(data.markup.log);

		// Pulse the current action
		this.$log.find(ProgressMonitor.CSS.currentAction).stop();
		this._pulseCurrentAction();

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
		this.endUpdating();
	} else if (this.keepUpdating) {
		setTimeout(this._requestUpdateProxy, ProgressMonitor.POLL_INTERVAL_MS);
	}
};

// Pulse the current action
ProgressMonitor.prototype._pulseCurrentAction = function() {
	var $action = this.$log.find(ProgressMonitor.CSS.currentAction);
	var pulseClass = ProgressMonitor.CSS.pulseClass;
	var toColor;
	if ($action.hasClass(pulseClass)) {
		$action.removeClass(pulseClass);
		toColor = ProgressMonitor.PULSE_START_COLOR;
	} else {
		$action.addClass(pulseClass);
		toColor = ProgressMonitor.PULSE_END_COLOR;
	}
	if (this.keepUpdating) {
		$action.animate({'color': toColor}, ProgressMonitor.PULSE_DURATION_MS, this._pulseCurrentActionProxy);
	}
};

// Request an update on the installation
ProgressMonitor.prototype._requestUpdate = function() {
	$.ajax({
		dataType: 'json',
		error: this._handleErrorProxy,
		success: this._renderUpdateProxy,
		url: this.url
	});
};

// Stop polling for updates
ProgressMonitor.prototype.endUpdating = function() {
	this.keepUpdating = false;
};

// Handle an error during the polling for progress log updates
ProgressMonitor.prototype._handleError = function(xhr, status) {
	this.endUpdating();
	execute.showError(pressgang.utils.getErrorText(xhr, this.errorMessage));
};

// Begin polling for installation progress updates
ProgressMonitor.prototype.beginUpdating = function() {
	this.keepUpdating = true;
	this._renderUpdateProxy = $.proxy(this._renderUpdate, this);
	this._requestUpdateProxy = $.proxy(this._requestUpdate, this);
	this._handleErrorProxy = $.proxy(this._handleError, this);
	this._requestUpdate();
};

// Make the executer available to other scripts
pressgang.actions.Executer = Executer;

})(jQuery, pressgang);
