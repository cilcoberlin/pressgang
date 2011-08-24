{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Update the Akismet API key
	update_option( 'wordpress_api_key', {{ value|as_php }} );

{% endblock %}
