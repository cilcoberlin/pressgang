{% extends "pressgang/options/blog_option.php" %}

{% load pressgang_options %}

{% block code %}

	// Switch to the requested theme
	switch_theme( {{ value|as_php }}, {{ value|as_php }} );

{% endblock %}
