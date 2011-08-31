{% load pressgang_options %}

// Sitewide Option: {{ name }}
{% safe_scope %}
	{% block code %}update_site_option( '{{ option }}', {{ value|as_php }} );{% endblock %}
{% endsafe_scope %}
