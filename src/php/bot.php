<?php

require_once('twitteroauth/twitteroauth.php');
require_once('config.php');

$conn = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET);

$params = array(
	'status' => 'hello world!'
);

$result = $conn->post('statuses/update', $params);

//$result = $conn->get('account/verify_credentials');
//$result = $conn->get('account/verify_credentials');

var_dump($result);
