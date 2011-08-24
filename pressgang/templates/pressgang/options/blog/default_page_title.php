{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// If a default page exists, update its title
	$default_page = get_page_by_title( __( '{% if blog.version.major == 3 %}Sample Page{% else %}About{% endif %}' ) );
	if ( $default_page ) {
		wp_update_post( array(
			'ID' => $default_page->ID,
			'post_title' => {{ value|as_php }}
		) );
	}

{% endblock %}
