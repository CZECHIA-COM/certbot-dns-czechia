# Certbot DNS plugin for CZECHIA.COM

This plugin provides automatic management of **DNS TXT records** using the **CZECHIA.COM** REST API.  
Its primary purpose is to automate obtaining TLS certificates from Let’s Encrypt using **DNS-01 challenges** with **Certbot**, including support for wildcard certificates.

Official CZECHIA.COM REST API documentation:  
https://api.czechia.com/swagger/index.html

---

## Features

- automatic creation of DNS TXT records for DNS-01 challenges
- automatic removal of TXT records after validation
- support for wildcard certificates
- no IP address whitelisting required for TXT record management
- can be used from any server with a valid API token

---

## Requirements

- Python 3.8 or newer
- Certbot
- CZECHIA.COM account
- API token with permission to manage DNS records of the domain

---

## CZECHIA.COM REST API behavior and limitations

CZECHIA.COM generally **requires IP address whitelisting** for using its REST API when performing domain-related operations.

### Exception for DNS TXT records

For **DNS TXT records used for certificate automation (DNS-01 challenge)**, IP address whitelisting **is not required**.

This means:
- TXT records can be modified from any machine
- no IP address needs to be allowed
- a valid API token is sufficient
- the API token must belong to the account where the domain is managed

---

## Installation

The plugin is distributed as a standalone Python package.

```bash
pip install certbot-dns-czechia
```

---

## Configuration

The plugin uses a configuration file in `.ini` format to store the API token.

### 1. Create the configuration file

Create a file, for example `czechia.ini`, with the following content:

```ini
dns_czechia_authorization_token = YOUR_API_TOKEN
```

- `dns_czechia_authorization_token` – API token from your CZECHIA.COM account
- the token must have permission to manage DNS records for the domain

### 2. Set secure file permissions

For security reasons, **Certbot requires** the credentials file to be readable only by the owner:

```bash
chmod 600 czechia.ini
```

---

## Usage with Certbot

### Obtain a certificate for a domain

```bash
certbot certonly \
  --authenticator dns-czechia \
  --dns-czechia-credentials ./czechia.ini \
  -d example.com
```

### Obtain a wildcard certificate

```bash
certbot certonly \
  --authenticator dns-czechia \
  --dns-czechia-credentials ./czechia.ini \
  -d example.com \
  -d '*.example.com'
```

During execution, the plugin:
1. creates the required `_acme-challenge` TXT record
2. waits for the record to become available
3. removes the TXT record after successful validation

---

## Security considerations

- the API token is stored only in the local credentials file
- the token is never written to logs
- the plugin only operates on TXT records required for DNS-01 challenges

---

## Troubleshooting

### Domain validation fails

- verify that the API token belongs to the same account as the domain
- check that the domain uses CZECHIA.COM DNS servers
- allow time for DNS propagation of TXT records

---

## Support

Official CZECHIA.COM technical support:  
**admin@zoner.com**

---

## License

MIT licence.
