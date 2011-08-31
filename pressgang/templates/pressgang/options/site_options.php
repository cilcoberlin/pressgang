<?php

/*
* Site Options
*
* This sets any sitewide options for a WPMU or multisite installation
*/

{% load pressgang_options %}

{% execute_once %}

	// Only apply the site options if the blog hasn't already been customized
	{% if not force %}
		if ( ! get_site_option( 'pressgang_site_customized', false ) ) {
			update_site_option( 'pressgang_site_customized', true );
	{% endif %}

		{{ code|safe }}

	{% if not force %}
		}
	{% endif %}

{% endexecute_once %}


?>
