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

	// Create the new user account and notify the user of their account
	$password = '{% random_password %}';
	$user_id = wp_create_user( $username, $password, '{{ email }}' );
	wp_new_user_notification( $user_id, $password );

	// Apply the requested role
	$user_data = array(
		'ID'   => $user_id,
		'role' => '{{ role }}' );
	wp_update_user( $user_data );

{% endexecute_once %}

?>
