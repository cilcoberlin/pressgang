{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Update the blog's description
	update_option( 'is_public', {{ value|as_php }} );

{% endblock %}
