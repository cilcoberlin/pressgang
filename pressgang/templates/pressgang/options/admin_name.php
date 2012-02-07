<?php

/*
* Set Admin Name
*
* This gives the admin user a valid first and last name.
*/

{% load pressgang_options %}

{% execute_once %}
	update_user_meta( 1, 'first_name', 'Site' );
	update_user_meta( 1, 'last_name', 'Administrator' );
	update_user_meta( 1, 'nickname', 'Site Admin' );
	wp_update_user( array(
		'ID' => 1,
		'display_name' => 'Site Administrator'
	) );
{% endexecute_once %}

?>
