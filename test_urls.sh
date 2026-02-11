#!/bin/bash

echo "🔍 TEST DES URLS DE LA PLATEFORME"
echo "=================================="
echo ""

urls=(
    "http://127.0.0.1:8000/"
    "http://127.0.0.1:8000/api/fournisseurs/"
    "http://127.0.0.1:8000/api/conteneurs/"
    "http://127.0.0.1:8000/dashboard/"
    "http://127.0.0.1:8000/contact/"
)

for url in "${urls[@]}"; do
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$response" = "200" ]; then
        echo "✅ $url"
    else
        echo "❌ $url (HTTP $response)"
    fi
done

echo ""
echo "✅ Tests terminés"
