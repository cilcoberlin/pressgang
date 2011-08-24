{% extends "pressgang/options/blog_option.php" %}

{% block code %}

	// Remove the default page if it exists
	{% if value %}
		$page_title = '{% if blog.version.major == 3 %}Sample Page{% else %}About{% endif %}';
		$default_page = get_page_by_title( __( $page_title ) );
		if ( $default_page ) {
			wp_delete_post( $default_page->ID );
		}
	{% endif %}

{% endblock %}
