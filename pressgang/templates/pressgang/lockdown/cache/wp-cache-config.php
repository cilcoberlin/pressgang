<?php
/*
PressGang WP Super Cache Lockdown Configuration

This is a configuration file for the WP Super Cache plugin, tailored for use
by PressGang to lock down a blog, rendering it minimally interactive and dynamic.
*/

// Preload everything on the blog and store it for a month before refreshing
$wp_cache_preload_on = 1;
$wp_cache_preload_email_volume = 'many';
$wp_cache_preload_email_me = 0;
$wp_cache_preload_interval = 60 * 24 * 30;
$wp_cache_preload_posts = '1';

// Enable lockdown mode to prevent comments breaking the cache
define( 'WPLOCKDOWN', '1' );

// Configure the cache to use mod_rewrite caching, keeping content for a month
$wp_cache_refresh_single_only = '1';
$wp_cache_mod_rewrite = 1;
$wp_cache_front_page_checks = 0;
$wp_supercache_304 = 0;
$wp_cache_slash_check = 1;
$cache_enabled = true;
$super_cache_enabled = true;
$cache_compression = 0;
$cache_max_time = 60 * 60 * 24 * 30;
$cache_rebuild_files = 1;
$wp_cache_not_logged_in = 0;
$wp_cache_clear_on_post_edit = 1;
$wp_cache_hello_world = 0;
$wp_cache_object_cache = 0;
$wp_cache_anon_only = 0;
$wp_supercache_cache_list = 0;
$wp_cache_hide_donation = 0;
$wp_cache_cron_check = 0;
$wp_cache_shutdown_gc = 0;
$wp_super_cache_late_init = 0;

// Set the proper paths to the cache plugin and file directories
$cache_path = WP_CONTENT_DIR . '/cache/';
if ( '/' != substr($cache_path, -1)) {
	$cache_path .= '/';
}
if ( ! defined( 'WPCACHEHOME' ) )
	define( 'WPCACHEHOME', WP_CONTENT_DIR . "/plugins/wp-super-cache/" ); //Added by WP-Cache Manager
$wp_cache_plugins_dir = WPCACHEHOME . 'plugins';
$file_prefix = 'wp-cache-';
$ossdlcdn = 0;

// Provide support for WPMU blogs
$blogcacheid = '';
if( defined( 'VHOST' ) ) {
	$blogcacheid = 'blog'; // main blog
	if( constant( 'VHOST' ) == 'yes' ) {
		$blogcacheid = $_SERVER['HTTP_HOST'];
	} else {
		$request_uri = preg_replace('/[ <>\'\"\r\n\t\(\)]/', '', str_replace( '..', '', $_SERVER['REQUEST_URI'] ) );
		if( strpos( $request_uri, '/', 1 ) ) {
			if( $base == '/' ) {
				$blogcacheid = substr( $request_uri, 1, strpos( $request_uri, '/', 1 ) - 1 );
			} else {
				$blogcacheid = str_replace( $base, '', $request_uri );
				$blogcacheid = substr( $blogcacheid, 0, strpos( $blogcacheid, '/', 1 ) );
			}
			if ( '/' == substr($blogcacheid, -1))
				$blogcacheid = substr($blogcacheid, 0, -1);
		}
		$blogcacheid = str_replace( '/', '', $blogcacheid );
	}
}

// Set the exclude and include lists for files to cache
$cache_acceptable_files = array( 'wp-comments-popup.php', 'wp-links-opml.php', 'wp-locations.php' );
$cache_rejected_uri = array ( 0 => 'wp-.*\\.php', );
$cache_rejected_user_agent = array ( 0 => 'bot', 1 => 'ia_archive', 2 => 'slurp', 3 => 'crawl', 4 => 'spider', 5 => 'Yandex' );

// Configure the file-locking system
$wp_cache_mutex_disabled = 1;
$sem_id = 5419;

// Enable support for mobile browsers
$wp_cache_mobile = 0;
$wp_cache_mobile_enabled = 1;
$wp_cache_mobile_groups = '';
$wp_cache_mobile_prefixes = 'w3c , w3c-, acs-, alav, alca, amoi, audi, avan, benq, bird, blac, blaz, brew, cell, cldc, cmd-, dang, doco, eric, hipt, htc_, inno, ipaq, ipod, jigs, kddi, keji, leno, lg-c, lg-d, lg-g, lge-, lg/u, maui, maxo, midp, mits, mmef, mobi, mot-, moto, mwbp, nec-, newt, noki, palm, pana, pant, phil, play, port, prox, qwap, sage, sams, sany, sch-, sec-, send, seri, sgh-, shar, sie-, siem, smal, smar, sony, sph-, symb, t-mo, teli, tim-, tosh, tsm-, upg1, upsi, vk-v, voda, wap-, wapa, wapi, wapp, wapr, webc, winw, winw, xda , xda-'; //Added by WP-Cache Manager
$wp_cache_mobile_whitelist = 'Stand Alone/QNws';
$wp_cache_mobile_browsers = '2.0 MMP, 240x320, 400X240, AvantGo, BlackBerry, Blazer, Cellphone, Danger, DoCoMo, Elaine/3.0, EudoraWeb, Googlebot-Mobile, hiptop, IEMobile, KYOCERA/WX310K, LG/U990, MIDP-2., MMEF20, MOT-V, NetFront, Newt, Nintendo Wii, Nitro, Nokia, Opera Mini, Palm, PlayStation Portable, portalmmm, Proxinet, ProxiNet, SHARP-TQ-GX10, SHG-i900, Small, SonyEricsson, Symbian OS, SymbianOS, TS21i-10, UP.Browser, UP.Link, webOS, Windows CE, WinWAP, YahooSeeker/M1A1-R2D2, iPhone, iPod, Android, BlackBerry9530, LG-TU915 Obigo, LGE VX, webOS, Nokia5800'; //Added by WP-Cache Manager

// Don't enable any debugging features
$wp_super_cache_debug = 0;
$wp_super_cache_advanced_debug = 0;
$wp_super_cache_front_page_text = '';
$wp_super_cache_front_page_clear = 0;
$wp_super_cache_front_page_check = 0;
$wp_super_cache_front_page_notification = '0';
$wp_cache_debug_to_file = 0;
$wp_cache_debug_level = 5;
$wp_cache_debug_ip = '';
$wp_cache_debug_log = '';
$wp_cache_debug_email = '';

// Cache every page possible
$wp_cache_pages[ "search" ] = 0;
$wp_cache_pages[ "feed" ] = 0;
$wp_cache_pages[ "category" ] = 0;
$wp_cache_pages[ "home" ] = 0;
$wp_cache_pages[ "frontpage" ] = 0;
$wp_cache_pages[ "tag" ] = 0;
$wp_cache_pages[ "archives" ] = 0;
$wp_cache_pages[ "pages" ] = 0;
$wp_cache_pages[ "single" ] = 0;
?>
