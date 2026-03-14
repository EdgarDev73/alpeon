<?php
/**
 * Proxy webhook — ALPÉON
 * Reçoit les données du formulaire et les transmet à votre webhook (Make, n8n, CRM, etc.)
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit();
}

// ===== CONFIGURATION =====
// Remplacez par l'URL de votre webhook (Make.com, n8n, Zapier, etc.)
$WEBHOOK_URL = 'https://hook.eu1.make.com/VOTRE_WEBHOOK_ICI';

// Lire et valider le corps de la requête
$body = file_get_contents('php://input');
$data = json_decode($body, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON']);
    exit();
}

// Sanitiser les données
$payload = [
    'resort'         => htmlspecialchars($data['resort'] ?? '', ENT_QUOTES, 'UTF-8'),
    'resortLabel'    => htmlspecialchars($data['resortLabel'] ?? '', ENT_QUOTES, 'UTF-8'),
    'quartier'       => htmlspecialchars($data['quartier'] ?? '', ENT_QUOTES, 'UTF-8'),
    'surface'        => (float)($data['surface'] ?? 0),
    'capacity'       => (int)($data['capacity'] ?? 0),
    'renovation'     => htmlspecialchars($data['renovation'] ?? '', ENT_QUOTES, 'UTF-8'),
    'amenities'      => array_map('strval', (array)($data['amenities'] ?? [])),
    'fullName'       => htmlspecialchars($data['fullName'] ?? '', ENT_QUOTES, 'UTF-8'),
    'email'          => filter_var($data['email'] ?? '', FILTER_SANITIZE_EMAIL),
    'phone'          => preg_replace('/[^+\d]/', '', $data['phone'] ?? ''),
    'yearlyRevenue'  => (int)($data['yearlyRevenue'] ?? 0),
    'monthlyRevenue' => (int)($data['monthlyRevenue'] ?? 0),
    'source'         => 'alpeon',
    'timestamp'      => date('c'),
];

// Envoyer au webhook
$ch = curl_init($WEBHOOK_URL);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_POSTFIELDS     => json_encode($payload),
    CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
    CURLOPT_TIMEOUT        => 10,
    CURLOPT_SSL_VERIFYPEER => true,
]);

$response = curl_exec($ch);
$httpCode  = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($curlError) {
    // Log l'erreur mais ne bloque pas l'utilisateur
    error_log('[alpeon-proxy] cURL error: ' . $curlError);
    http_response_code(200);
    echo json_encode(['status' => 'ok', 'note' => 'webhook_error']);
    exit();
}

http_response_code(200);
echo json_encode(['status' => 'ok', 'webhook_code' => $httpCode]);
