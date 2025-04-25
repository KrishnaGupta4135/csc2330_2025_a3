#!/bin/bash

# Create directories
mkdir -p frontend/certs backend/certs

# Generate CA key and certificate
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj "//CN=CSC2330 CA"

# Generate frontend key and CSR
openssl genrsa -out frontend/certs/frontend.key 2048
openssl req -new -key frontend/certs/frontend.key -out frontend.csr -subj "//CN=frontend"
openssl x509 -req -in frontend.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out frontend/certs/frontend.crt -days 365 -sha256

# Generate backend key and CSR
openssl genrsa -out backend/certs/backend.key 2048
openssl req -new -key backend/certs/backend.key -out backend.csr -subj "//CN=backend"
openssl x509 -req -in backend.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out backend/certs/backend.crt -days 365 -sha256

# Generate www certificate for Flask frontend HTTPS (optional)
openssl genrsa -out frontend/certs/www.key 2048
openssl req -x509 -new -nodes -key frontend/certs/www.key -sha256 -days 365 -out frontend/certs/www.crt -subj "//CN=localhost"

# Copy CA certificate to both frontend and backend
cp ca.crt frontend/certs/
cp ca.crt backend/certs/

# Clean up temporary files
rm -f frontend.csr backend.csr ca.srl

echo "✅ Certificates generated successfully."
