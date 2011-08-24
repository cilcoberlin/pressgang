{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Update the blog's description
	update_option( 'blogdescription', {{ value|as_php }} );

{% endblock %}
