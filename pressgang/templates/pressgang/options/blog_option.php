{% load pressgang_options %}

// Blog Option: {{ name }}
{% safe_scope %}
	{% block code %}{% endblock %}
{% endsafe_scope %}
