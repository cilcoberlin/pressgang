<?php

/*
* Create Blog
*
* This creates a blog for the user {{ username }} ({{ email }})
*/

{% load pressgang_options %}

{% execute_once %}

	// If a user with the given email already exists, don't add a new blog
	if ( email_exists( '{{ email }}' ) ) {
		return;
	}

	// Get a username for the user, which will be available as $username
	{% get_username username email %}

	// Create an account for the user if they don't have one, and get their
	// user ID of they do have one
	$user_id = username_exists( $username );
	$password = '';
	if ( ! $user_id ) {
		$password = '{% random_password %}';
		$user_id = wp_create_user( $username, $password, '{{ email }}' );
	}

	// Make sure that the blog doesn't conflict with other users' blogs, using
	// the fact that the blog's path is passed from PressGang with a "%s" in it
	// that will contain the child blog's ID
	$blog_path = sprintf( '{{ path }}', '{{ blog_id }}' );
	{% if blog.version.is_multi %}
		global $wpdb;
		$conflicts = true;
		$counter = 1;
		while ( $conflicts ) {
			if ( $wpdb->get_results( $wpdb->prepare( "SELECT path FROM $wpdb->blogs WHERE path=%s", $blog_path ) ) ) {
				$counter++;
				$blog_path = sprintf( '{{ path }}', '{{ blog_id }}' . $counter );
			} else {
				$conflicts = false;
			}
		}
	{% endif %}

	// Create the new blog for the user
	$blog_title = {{ title|as_php }};
	$blog_id = wpmu_create_blog( '{{ domain }}', $blog_path, $blog_title, $user_id );
	wpmu_welcome_notification( $blog_id, $user_id, $password, $blog_title );

{% endexecute_once %}

?>
