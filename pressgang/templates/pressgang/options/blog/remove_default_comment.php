{% extends "pressgang/options/blog_option.php" %}

{% block code %}

	// Remove the default comment if it exists
	{% if value %}
		$comment_id = 1;
		$default_comment = get_comment( $comment_id );
		if ( $default_comment ) {
			wp_delete_comment( $comment_id );
		}
	{% endif %}

{% endblock %}
