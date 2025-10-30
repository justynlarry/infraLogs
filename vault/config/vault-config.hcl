ui = true

storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address		= "0.0.0.0:8200"
  tls_cert_file		= "/vault/certs/vault.crt"
  tls_key_file		= "/vault/certs/vault.key"
  tls_client_ca_file	= "/vault/certs/ca.pem"
}

default_lease_ttl = "168h"
max_lease_ttl = "720h"
