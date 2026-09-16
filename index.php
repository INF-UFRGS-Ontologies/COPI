<?php
// Content negotiation for https://www.inf.ufrgs.br/ontologies/copi/
//
// RDF requests are answered with the file itself and an explicit Content-Type,
// rather than a 303 to copi.owl / copi.ttl: the server has no media type for
// those extensions, so a redirected client received application/octet-stream
// and could not parse the ontology (FOOPS! failed on exactly this). The
// accompanying .htaccess fixes the type for direct file links too, where
// AllowOverride permits it; this file does not depend on that.
//
// Browsers still get a 303 to the documentation.

$accept = isset($_SERVER['HTTP_ACCEPT']) ? $_SERVER['HTTP_ACCEPT'] : '';
$base   = 'https://www.inf.ufrgs.br/ontologies/copi/';

function serve_rdf($file, $type)
{
    if (!is_readable($file)) {
        header('HTTP/1.1 404 Not Found');
        header('Content-Type: text/plain; charset=utf-8');
        echo "Not found: $file\n";
        return;
    }
    header('HTTP/1.1 200 OK');
    header('Content-Type: ' . $type);
    header('Content-Length: ' . filesize($file));
    header('Vary: Accept');
    readfile($file);
}

if (strpos($accept, 'text/turtle') !== false) {
    serve_rdf(__DIR__ . '/copi.ttl', 'text/turtle; charset=utf-8');
} elseif (strpos($accept, 'application/rdf+xml') !== false || strpos($accept, 'application/owl+xml') !== false) {
    serve_rdf(__DIR__ . '/copi.owl', 'application/rdf+xml; charset=utf-8');
} else {
    header('HTTP/1.1 303 See Other');
    header('Location: ' . $base . 'docs.html');
    header('Vary: Accept');
}
