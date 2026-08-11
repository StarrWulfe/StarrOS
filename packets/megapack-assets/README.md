# megapack-assets — Public Static Hosting (Wolfpack avatars)

Serves the MegaPack agent avatars from a stable public prefix:

```
https://megapack-assets.srwf.xyz/avatars/wolves/<filename>
```

Anonymous public access — no VPN / Tailscale / NetBird / Cloudflare Access / login.
Used as the `picture` field in Buzz/Nostr and Matrix agent profiles.

## Architecture

```
Public → Cloudflare (proxied A record, edge TLS, CDN) → Origin Rule :8448
       → Yoseba (Caddy :8448, static file server) → /srv/megapack-assets
```

- **Cloudflare** terminates edge TLS (Universal SSL, Google Trust Services) and
  provides DNS + CDN. Full (strict) mode.
- **Yoseba** origin: Caddy serves `/srv/megapack-assets` on `:8448` with a
  Cloudflare Origin CA certificate. Traefik (`netbird-traefik`) is **untouched** —
  Caddy owns origin TLS for this host, so the risky edge-proxy recreate is avoided.

## Cloudflare configuration

| Item | Value |
|---|---|
| Zone | `srwf.xyz` (`6d0a30b86326270bfa5906186d199170`) |
| DNS record | `A megapack-assets.srwf.xyz → 45.79.220.12`, **proxied** (orange cloud) |
| SSL mode | **Full (strict)** |
| Always Use HTTPS | **on** |
| Origin CA cert | Cloudflare Origin CA (origin-rsa), 15y, hostnames `[megapack-assets.srwf.xyz]`, issued via `/client/v4/certificates` |
| Origin Rule | `http_request_origin` ruleset `99220aba…`: `(http.host eq "megapack-assets.srwf.xyz")` → `action route`, `origin.port = 8448` |

## Yoseba layout

| Path | Purpose | Ownership |
|---|---|---|
| `/srv/megapack-assets/` | Static asset root | `root:root`, 0755 dirs / 0644 files |
| `/srv/megapack-assets/avatars/wolves/` | Avatar files | root, not world-writable |
| `/etc/ssl/megapack-assets/cert.pem` | Cloudflare Origin CA cert | root 0644 |
| `/etc/ssl/megapack-assets/private.key` | Origin private key | root 0600 |
| `/etc/caddy/megapack-assets.Caddyfile` | Caddy config | root |
| `/etc/systemd/system/caddy-megapack.service` | systemd unit | root |

Caddy binds `:8448` (loopback-agnostic; Traefik owns 80/443). Tailscaled already
owns `:8443` (`tailscale serve`), so 8448 was chosen to avoid the conflict.

Headers set by Caddy: `X-Content-Type-Options: nosniff`, `Cache-Control:
public, max-age=86400` (baseline), `-Server` stripped. `file_server` has
directory browsing off (no listing). A traversal matcher rejects `..`/`%2e%2e`.

## Deploy / redeploy

```bash
# content
cd /tmp/megapack-content && tar czf - avatars | ssh j7@yoseba.tailfaadb.ts.net \
  'sudo tar xzf - -C /srv/megapack-assets && sudo chown -R root:root /srv/megapack-assets'

# config
scp -i ~/.ssh/ssh_key_san packets/megapack-assets/Caddyfile j7@yoseba.tailfaadb.ts.net:/tmp/
scp -i ~/.ssh/ssh_key_san packets/megapack-assets/caddy-megapack.service j7@yoseba.tailfaadb.ts.net:/tmp/
ssh j7@yoseba.tailfaadb.ts.net 'sudo mv /tmp/Caddyfile /etc/caddy/megapack-assets.Caddyfile && \
  sudo mv /tmp/caddy-megapack.service /etc/systemd/system/caddy-megapack.service && \
  sudo systemctl daemon-reload && sudo systemctl restart caddy-megapack.service'

# validate
sudo /usr/bin/caddy validate --config /etc/caddy/megapack-assets.Caddyfile
```

## Validation (external, public)

```bash
curl -sSI https://megapack-assets.srwf.xyz/avatars/wolves/hermes-ops.webp
# HTTP/2 200, content-type: image/webp, cache-control: public max-age=86400, nosniff
curl -sS -o /dev/null -w "%{http_code}\n" https://megapack-assets.srwf.xyz/avatars/wolves/nope.png   # 404
curl -sS -o /dev/null -w "%{http_code}\n" https://megapack-assets.srwf.xyz/avatars/wolves/            # 404 (no listing)
curl -sSI http://megapack-assets.srwf.xyz/avatars/wolves/hermes-ops.webp                               # 301 → https
```

Verified 2026-08-11 (San): 200 / 404 / 404 / 301 / valid edge cert (Google
Trust Services) / proxied DNS (Cloudflare IPs) / content identity confirmed.

## Files

- `Caddyfile` — the live Caddy config
- `caddy-megapack.service` — the live systemd unit
- `ASSETS.md` — asset manifest (pack avatars present)
