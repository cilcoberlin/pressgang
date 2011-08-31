<?php

/*
 * Add User
 *
 * This adds an account for the user {{ username }} ({{ email }}) to the blog
 */

{% load pressgang_options %}

{% execute_once %}

	// Get a username for the user, which will be available as $username
	{% get_username username email %}

	// Create the new user account
	$user_id = wp_create_user(
		$username,
		'{% random_password %}',
		'{{ email }}'
	);

	// Apply the requested role
	wp_insert_user(
		array(
			'ID'   => $user_id,
			'role' => '{{ role }}'
		)
	);

{% endexecute_once %}

?>
