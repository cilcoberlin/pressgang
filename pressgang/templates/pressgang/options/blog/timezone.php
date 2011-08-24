{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Use the requested time zone
	update_option( 'timezone_string', {{ value|as_php }} );

{% endblock %}
