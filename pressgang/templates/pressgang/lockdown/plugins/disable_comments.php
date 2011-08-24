<?php

/*
Plugin Name: PressGang Comment Disabler
Plugin URI: http://languages.oberlin.edu/cilc/projects/pressgang/
Description: Disables commenting on all posts.
Version: 0.1
Author: the Oberlin Cooper International Learning Center
Author URI: http://languages.oberlin.edu/
License: GPLv2 or later
*/

class PressGang_Lockdown_DisableComments
{

	/**
	 * Registers plugin hooks
	 */
	public function __construct()
	{
		add_filter( 'comments_open', array( $this, '_disable_comments_open' ), 10, 2 );
		if ( ! is_admin() ) {
			add_filter( 'the_posts',     array( $this, '_close_comment_status' ) );
		}
	}

	/**
	 * Makes comments always appear to be off for any item on the blog
	 *
	 * @param  bool $is_open whether the comment is open
	 * @param  int  $post_id the ID of the post or page
	 * @return bool          false, to flag comments as closed
	 *
	 * @access private
	 * @since 0.1
	 */
	public function _disable_comments_open( $is_open, $post_id )
	{
		return false;
	}

	/**
	 * Makes the comment status of any post always be closed
	 *
	 * @param  array $posts the current list of posts
	 * @return array        the posts with their comment status set to closed
	 *
	 * @access private
	 * @since 0.1
	 */
	public function _close_comment_status( $posts )
	{
		foreach ( $posts as $post ) {
			$post->comment_status = 'closed';
		}
		return $posts;
	}
}

$pressgang_disable_comments = new PressGang_Lockdown_DisableComments();

?>
