
// Wrap the given code in a function to prevent name clashes
if ( ! function_exists( '{{ function }}' ) ) {
	function {{ function }}() {
		{{ code|safe }}
	}
}
{{ function }}();
