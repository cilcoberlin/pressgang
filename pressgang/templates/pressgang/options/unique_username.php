
// If the email is in use, use the username associated with it.  If it has not
// yet been linked with a user, create a new unique username
$email_exists = email_exists( '{{ email }}' );
if ( $email_exists ) {
	$user = get_userdata( $email_exists );
	$username = $user->user_login;
} else {
	$username = '{{ username }}';
	if ( username_exists( $username ) ) {
		$user_count = 1;
		$user_exists = true;
		while ( $user_exists ) {
			$user_count++;
			$username = '{{ username }}$user_count';
			$user_exists = username_exists( $username );
		}
	}
}
