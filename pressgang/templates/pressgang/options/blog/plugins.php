{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Get a list of active plugins
	$active_plugins = get_option( 'active_plugins' );
	if ( ! $active_plugins ) {
		$active_plugins = array();
	}
	$plugins = {{ value|as_php }};

	// Enable each plugin
	foreach ( $plugins as $plugin ) {

		// Include the plugin's code
		include_once( ABSPATH . PLUGINDIR . '/' . $plugin );

		// Update the list of plugins if the current plugin is inactive
		if ( ! in_array( $plugin, $active_plugins ) ) {
			$active_plugins = array_merge( $active_plugins, array( $plugin ) );
			update_option( 'active_plugins', $active_plugins );
			do_action( 'activate_' . $plugin );
		}

	}

{% endblock %}
