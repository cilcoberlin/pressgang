
// Wrap the given code in a function to prevent name clashes
function {{ function }}() {
	{{ code|safe }}
}
{{ function }}();
