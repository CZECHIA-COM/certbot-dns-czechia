# certbot-dns-czechia
# Certbot DNS plugin pro CZECHIA.COM

Tento plugin umožňuje automatickou správu **DNS TXT záznamů** u domén registrovaných u **CZECHIA.COM** pomocí jejich REST API.  
Je určen pro použití s **Certbotem** při získávání certifikátů z Let’s Encrypt pomocí **DNS-01 challenge**, včetně wildcard certifikátů.

Plugin využívá oficiální REST API CZECHIA.COM:  
https://api.czechia.com/swagger/index.html

---

## Funkce

- automatické vytváření a mazání DNS TXT záznamů
- podpora DNS-01 challenge
- podpora wildcard certifikátů
- není nutné povolovat IP adresu serveru
- funguje z libovolného stroje s platným API tokenem

---

## Požadavky

- Python 3.8+
- Certbot
- účet u CZECHIA.COM
- API token s oprávněním ke správě DNS záznamů domény

---

## Důležité informace k REST API CZECHIA.COM

CZECHIA.COM standardně vyžaduje povolení IP adresy pro použití REST API při operacích s doménami.

**Výjimka:**  
Pro **DNS TXT záznamy používané k automatizaci certifikátů (DNS-01 challenge)** povolení IP adresy **není vyžadováno**.

To znamená:
- TXT záznamy lze upravovat z jakéhokoliv stroje
- stačí platný API token
- API token musí patřit k účtu, kde je doména spravována

---

## Instalace

```bash
pip install certbot-dns-czechia
