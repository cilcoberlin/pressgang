
add_action( 'init', '{{ function }}' );
function {{ function }}() {

	// Get our stored list of executed pressgang options functions
	$executed_functions = get_option( 'pressgang_functions' );
	if ( empty( $executed_functions ) ) {
		$executed_functions = array();
	}

	// Only run the code if it has not yet been flagged as run
	if ( ! in_array( '{{ function }}', $executed_functions ) ) {
		{{ code|safe }}

		// Add the function to our list of executed ones
		$executed_functions[] = '{{ function }}';
		update_option( 'pressgang_functions', $executed_functions );
	}
}
