<?php
$accept = isset($_SERVER['HTTP_ACCEPT']) ? $_SERVER['HTTP_ACCEPT'] : '';
$base   = 'https://www.inf.ufrgs.br/ontologies/copi/';

if (strpos($accept, 'text/turtle') !== false) {
    header('HTTP/1.1 303 See Other');
    header('Location: ' . $base . 'copi.ttl');
    header('Vary: Accept');
} elseif (strpos($accept, 'application/rdf+xml') !== false || strpos($accept, 'application/owl+xml') !== false) {
    header('HTTP/1.1 303 See Other');
    header('Location: ' . $base . 'copi.owl');
    header('Vary: Accept');
} else {
    header('HTTP/1.1 303 See Other');
    header('Location: ' . $base . 'docs.html');
    header('Vary: Accept');
}
