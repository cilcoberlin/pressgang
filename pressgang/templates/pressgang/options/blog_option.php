{% load pressgang_options %}

{% setter_function option as option_setter %}
// Blog Option: {{ name }}
if ( ! function_exists( '{{ option_setter }}' ) ) {
	function {{ option_setter }}() {
		{% block code %}{% endblock %}
	}
}
{{ option_setter }}();
