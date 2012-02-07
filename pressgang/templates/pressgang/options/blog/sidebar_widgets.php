{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Since the widgetized areas defined by a theme can vary quite a bit,
	// we use a list of common area identifiers to take the user's widgets
	$widget_areas = array(
		'sidebar',
		'sidebar-1',
		'primary-widget-area'
	);
	$new_widgets = array();
	foreach ( $widget_areas as $widget_area ) {
		$new_widgets[$widget_area] = {{ value|as_php }};
	}

	// Enable the requested widgets
	$current_widgets = get_option( 'sidebars_widgets' );
	$final_widgets = array_merge( $current_widgets, $new_widgets );
	wp_set_sidebars_widgets( $final_widgets );

{% endblock %}
