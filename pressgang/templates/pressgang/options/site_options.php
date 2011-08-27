<?php

/*
* Site Options
*
* This sets any sitewide options for a WPMU or multisite installation
*/

{% load pressgang_options %}

// Only apply the site options if the blog hasn't already been customized
if ( ! get_site_option( 'pressgang_site_customized', false ) ) {
	update_site_option( 'pressgang_site_customized', true );

	// Apply each option to the site
	{% setter_function options as options_setter %}
	add_action( 'init', '{{ options_setter }}' );
	function {{ options_setter }}() {
		{{ code|safe }}
	}
}

?>
