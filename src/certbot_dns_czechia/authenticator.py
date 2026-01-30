from __future__ import annotations

import time
from dataclasses import dataclass

import requests
from certbot import errors
from certbot.plugins import dns_common


@dataclass(frozen=True)
class CzechiaConfig:
    api_base: str
    zone: str
    token: str
    ttl: int
    publish_zone: int
    timeout: int


class Authenticator(dns_common.DNSAuthenticator):
    """
    Certbot DNS authenticator for Czechia/ZONER DNS API.

    Endpoint:
      POST/DELETE https://api.czechia.com/api/DNS/<zone>/TXT

    Header:
      authorizationToken: <token>

    Body:
      {"hostName":"...","text":"...","ttl":3600,"publishZone":1}
    """

    description = "Obtain certificates using a DNS TXT record via Czechia/ZONER DNS API."

    @classmethod
    def add_parser_arguments(cls, add):  # type: ignore[override]
        # IMPORTANT:
        # Call super() to keep Certbot's standard DNS options including:
        #   --dns-czechia-propagation-seconds
        # We do NOT define propagation-seconds ourselves.
        super().add_parser_arguments(add)

        add("credentials", help="INI file with Czechia DNS API token")
        add("zone", help="Apex DNS zone (domainName), e.g. example.com")
        add("api-base", default="https://api.czechia.com", help="API base URL")
        add("ttl", type=int, default=3600, help="TTL for the TXT record")
        add("publish-zone", type=int, default=1, help="publishZone value (usually 1)")
        add("timeout", type=int, default=30, help="HTTP timeout seconds")

    def more_info(self) -> str:
        return "Adds and removes DNS TXT records via Czechia/ZONER DNS API."

    def _setup_credentials(self) -> None:
        # certbot reads keys with prefix: dns_czechia_*
        self.credentials = self._configure_credentials(
            "credentials",
            "Czechia/ZONER DNS API credentials INI file",
            {"authorization_token": "API token for Czechia DNS API"},
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        cfg = self._get_cfg()
        host = self._relative_host(validation_name, cfg.zone)

        self._call_api("POST", cfg, host, validation)

        # Standard Certbot flag from DNSAuthenticator:
        # --dns-czechia-propagation-seconds
        time.sleep(int(self.conf("propagation-seconds")))

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        cfg = self._get_cfg()
        host = self._relative_host(validation_name, cfg.zone)

        try:
            self._call_api("DELETE", cfg, host, validation)
        except Exception:
            # cleanup should not fail the run
            pass

    def _get_cfg(self) -> CzechiaConfig:
        token = self.credentials.conf("authorization_token")
        api_base = str(self.conf("api-base")).rstrip("/")
        zone = str(self.conf("zone")).strip(".").lower()

        if not zone:
            raise errors.PluginError("Missing --dns-czechia-zone (apex domainName).")

        return CzechiaConfig(
            api_base=api_base,
            zone=zone,
            token=token,
            ttl=int(self.conf("ttl")),
            publish_zone=int(self.conf("publish-zone")),
            timeout=int(self.conf("timeout")),
        )

    @staticmethod
    def _relative_host(validation_name: str, zone: str) -> str:
        name = validation_name.rstrip(".").lower()
        zone = zone.rstrip(".").lower()

        if name == zone:
            return "@"

        suffix = "." + zone
        if not name.endswith(suffix):
            raise errors.PluginError(f"Validation name '{name}' is not under zone '{zone}'.")

        rel = name[: -len(suffix)]
        return rel if rel else "@"

    @staticmethod
    def _call_api(method: str, cfg: CzechiaConfig, host: str, txt: str) -> None:
        url = f"{cfg.api_base}/api/DNS/{cfg.zone}/TXT"
        headers = {"authorizationToken": cfg.token, "Content-Type": "application/json"}
        payload = {"hostName": host, "text": txt, "ttl": cfg.ttl, "publishZone": cfg.publish_zone}

        try:
            resp = requests.request(method=method, url=url, headers=headers, json=payload, timeout=cfg.timeout)
        except requests.RequestException as e:
            raise errors.PluginError(f"Czechia API request failed: {e}") from e

        if not (200 <= resp.status_code < 300):
            body = (resp.text or "").strip()
            raise errors.PluginError(f"Czechia API error {resp.status_code} for {method} {url}: {body}")

