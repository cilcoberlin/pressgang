{% extends "pressgang/options/blog_option.php" %}

{% block code %}

	// Enable gravatars with sensible defaults
	{% if value %}
		update_option( 'show_avatars', 1);
		update_option( 'avatar_default', 'mystery');
		update_option( 'avatar_rating', 'PG');
	{% endif %}

{% endblock %}
