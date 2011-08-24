<?php

/*
* Create Blog
*
* This creates a blog for the user {{ username }} ({{ email }})
*/

{% load pressgang_options %}

{% setter_function blog_id as blog_setter %}
add_action( 'init', '{{ blog_setter }}' );
function {{ blog_setter }}() {

	// Get a username for the user, which will be available as $username
	{% get_username username email %}

	// Create an account for the user if they don't have one, and get their
	// user ID of they do have one
	$user_id = username_exists( $username );
	if ( ! $user_id ) {
		$user_id = wp_create_user(
			$username,
			'{% random_password %}',
			'{{ email }}'
		);
	}

	// Create the new blog for the user
	$blog_id = wpmu_create_blog(
		'{{ domain }}',
		'{{ path }}',
		{{ title|as_php }},
		$user_id
	);
}

?>
