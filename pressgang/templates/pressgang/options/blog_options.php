<?php

/*
* Blog Options
*
* This sets blog-level options for one or more WordPress blogs
*/

{% load pressgang_options %}

{% execute_once %}

	// Apply the option-setting code to each blog if on multisite / WPMU, or
	// simply to the only blog on a non-multi-blog installation
	{% if blog.version.is_multi %}

		$blog_ids = array();
		$for_root = {{ for_root|as_php }};
		$for_non_root = {{ for_non_root|as_php }};

		// Determine the correct blog IDs based upon the type of options being set
		if ( $for_root ) {
			$blog_ids[] = 1;
		}
		if ( $for_non_root ) {
			global $wpdb;
			foreach ( $wpdb->get_results( "SELECT blog_id FROM $wpdb->blogs WHERE blog_id <> 1" ) as $blog ) {
				$blog_ids[] = $blog->blog_id;
			}
		}

		foreach ( $blog_ids as $blog_id ):
			switch_to_blog( $blog_id );
	{% endif %}

	// Only apply the options if the options haven't already been set
	{% if not force %}
		if ( ! get_option( '{{ options }}_set', false ) ) {
			update_option( '{{ options }}_set', true );
	{% endif %}

		{{ code|safe }}

	{% if not force %}
		}
	{% endif %}

	{% if blog.version.is_multi %}
			restore_current_blog();
		endforeach;
	{% endif %}

{% endexecute_once %}

?>
