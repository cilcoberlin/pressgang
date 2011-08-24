{% extends "pressgang/options/blog_option.php" %}

{% block code %}

	// Enable threaded comments
	{% if value %}
		update_option( 'thread_comments', 1 );
		update_option( 'thread_comments_depth', 5 );
	{% endif %}

{% endblock %}
