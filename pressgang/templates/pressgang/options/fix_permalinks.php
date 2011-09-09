<?php

/*
* Fix Blog Permalinks
*
* This sets all child-blog permalinks to their correct values
*/

{% load pressgang_options %}

{% execute_once %}

	// Restore the correct defaults for every non-root blog's permalink structure
	// by clearing the cached rewrite rules from the database.  This will force
	// the blog to refresh its rewrite rules the next time a page on it is loaded,
	// allowing WordPress to handle the fix instead of PressGang.
	global $wpdb;
	foreach ( $wpdb->get_results( $wpdb->prepare( "SELECT blog_id from $wpdb->blogs WHERE blog_id <> 1" ) ) as $blog ) {
		switch_to_blog( $blog->blog_id );
		delete_option( 'rewrite_rules' );
		restore_current_blog();
	}

{% endexecute_once %}

?>
