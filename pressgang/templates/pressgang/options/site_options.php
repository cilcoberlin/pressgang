<?php

/*
* Site Options
*
* This sets any sitewide options for a WPMU or multisite installation
*/

{% load pressgang_options %}

{% setter_function options as options_setter %}
add_action( 'init', '{{ options_setter }}' );
function {{ options_setter }}() {
	{{ code|safe }}
}

?>
