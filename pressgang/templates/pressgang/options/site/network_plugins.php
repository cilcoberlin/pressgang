{% extends "pressgang/options/site_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Get a list of active network plugins
	$active_plugins = get_site_option( 'active_sitewide_plugins' );
	if ( ! $active_plugins ) {
		$active_plugins = array();
	}
	$plugins = {{ value|as_php }};

	// Enable each inactive plugin
	foreach ( $plugins as $plugin ) {
		if ( ! in_array( $plugin, $active_plugins ) ) {

			// Include and activate the plugin
			include_once( ABSPATH . PLUGINDIR . '/' . $plugin );
			do_action( 'activate_plugin', $plugin, true );
			do_action( 'activate_' . $plugin, true );

			// Add it to the list of activated plugins
			$active_plugins[$plugin] = time();
			update_site_option( 'active_sitewide_plugins', $active_plugins );
			do_action( 'activated_plugin', $plugin, true );
		}
	}

{% endblock %}
