{% load pressgang_options %}

{% setter_function option as option_setter %}
// Sitewide Option: {{ name }}
function {{ option_setter }}() {
	{% block code %}update_site_option( '{{ option }}', {{ value|as_php }} );{% endblock %}
}
{{ option_setter }}();
