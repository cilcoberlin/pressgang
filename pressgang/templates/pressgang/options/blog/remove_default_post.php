{% extends "pressgang/options/blog_option.php" %}

{% block code %}

	// Remove the default post if it exists
	{% if value %}
		$post_id = 1;
		$default_post = get_post( $post_id );
		if ( $default_post ) {
			wp_delete_post( $post_id );
		}
	{% endif %}

{% endblock %}
