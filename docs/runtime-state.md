# Runtime State — Mononoke (live)

> **Purpose:** ephemeral facts that change often: ports, services, broken items, drift. Audit-trail-only; not architecture.
> **Owner:** San (writer) + Kohroku (memory owner) + Ishii (NixOS authority)
> **Update rhythm:** re-audited weekly; ad-hoc when something breaks. This file is **not** a planning artifact.

## 0. What belongs here vs the canonical spec

| Concern | Goes to |
|---|---|
| "Mission Control is currently paused" | `docs/runtime-state.md` (this file) — runtime fact |
| "Mission Control is a Next.js 15 shell with 6 tabs" | `specs/starros-stack-spec.md` §7 — architecture |
| "Ashitaka should bind `:8643`" | `specs/starros-stack-spec.md` (architectural intent) |
| "Ashitaka PID 20888 is alive but unbound" | `docs/runtime-state.md` (current state) |
| "Karakeep is live at keep.starrwulfe.xyz" | `specs/starros-stack-spec.md` (architecture) |
| "Karakeep OIDC end-to-end smoke test is pending" | `docs/runtime-state.md` (current state) |
| "Definition of GBrain" | `specs/gbrain-substrate.md` (architecture) |
| "GBrain spec not yet written" | `docs/runtime-state.md` (current state) |

## 1. Hosts

| Host | Role | Tailnet IP | Public IP |
|---|---|---|---|
| Mononoke | Primary NixOS host | 100.77.7.1 | via Tailscale Funnel |
| Outpost | VPS — Synapse, Traefik, Pocket ID, Pocket ID OIDC, Karakeep, AC shims | 100.77.7.2 | 96.30.205.112 |
| Yoseba | Arch Linux — Headscale, Stalwart, YOURLS | 100.77.7.3 | 45.79.220.12 |

## 2. Mononoke service map (live)

| Port | Bind | Service | Status |
|---|---|---|---|
| 443 | Tailscale Funnel | public TLS termination | OK |
| 80 | 0.0.0.0 | Traefik (NixOS) | OK |
| 11080 | 0.0.0.0 | Nextcloud nginx | OK |
| 11081 | 0.0.0.0 | Nextcloud app | OK |
| 3000 | 0.0.0.0 | AdGuard Home admin | OK |
| 3001 | 0.0.0.0 | Forgejo | OK (LAN); public 404 (Outpost Traefik bug — see Top 5) |
| 3002 | (should be 0.0.0.0) | Mission Control (Hermes Workspace) | **DEAD** — service not running |
| 3005 | 127.0.0.1 | Free Model Roundup (Python) | OK |
| 6380 | 127.0.0.1 | AMB (Redis broker, agent mesh bus) | partial — Phase 1A live; Phase 1C ACL finalization in progress (P8) |
| 8000 | 0.0.0.0 | Honcho API (podman) | **DECOMMISSION PENDING** — J7 confirmed 2026-07-09: no migration to Mnemosyne needed (Mnemosyne is the surviving canonical memory layer); container still running, needs stop + reclaim. Action: Toki/Ishii. |
| 8001 | 127.0.0.1 | Sanctuary Launcher | OK |
| 8081 | 0.0.0.0 | it-tools (podman) | OK |
| 8096 | 0.0.0.0 | Jellyfin | OK |
| 8642 | 0.0.0.0 | Multiplex (system) | OK (PID 490006; `multiplex_profiles: false`) |
| 8643 | (should be 0.0.0.0) | Ashitaka per-wolf | **MISSING** — PID 20888 alive but unbound (P0) |
| 8644-8652 | 0.0.0.0 | 9 per-wolf gateways | OK (ishii, jigo, kohroku, mokku, moro, nago, okkoto, toki, yakkuru) |
| 8765 | (should be 0.0.0.0) | Mnemosyne dashboard | **DOWN** — service crashed. Restart procedure: see §3 item 1 below for the single canonical restart command (this row intentionally does not duplicate it). |
| 9119 | 0.0.0.0 | Hermes Dashboard | OK (basic-auth `j7`/scrypt) |
| 9120 | 127.0.0.1 (proxied /widget/) | Eye-of-Hermes PWA | OK |
| 9377 | 127.0.0.1 | Camofox HTTP API | OK |
| 11080/11081 | — | (see Nextcloud above) | — |

**Outpost:** Synapse 8008 (proxied via Traefik at `mtrx.starrwulfe.xyz`); Traefik 80/443; Pocket ID 1411; Karakeep on its own bind (port not on Mononoke).

**Yoseba:** Headscale 8080; Stalwart 25/465/587/993; YOURLS 80.

## 3. Major broken / degraded items (top 5 by impact)

1. **Mnemosyne dashboard `:8765` down.** Memory write-side works, audit/read-side dark. **Phase P4.** Restart procedure: use the `mnemosyne_dashboard_start` Hermes tool (canonical source: `operations/mononoke-systems-check/SKILL.md:226`). Sequence:
   ```bash
   ss -tlnp | grep 8765      # check if running
   mnemosyne_dashboard_start  # starts dashboard on 0.0.0.0:8765
   curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8765/  # expect 200
   ```
   The Mnemosyne SQLite DB at `~/.hermes/mnemosyne/data/mnemosyne.db` persists across crashes — only the UI process needs restart. **Note:** The `bsm-secret-fetch-for-environmentfile.sh` script is unrelated — it is the `ExecStartPre=` template for loading BWS secrets into systemd environment files, not a Mnemosyne restart helper.
2. **Ashitaka port `:8643` unbound.** PID 20888 alive but no listener. The default port assignment in `wolfpack.nix` places ashitaka on `:8643`. Other 9 wolves bind correctly. **Phase P0.**
3. **`code.starrwulfe.xyz` 404.** Outpost Traefik `dynamic.toml` points to `127.0.0.1:3001` instead of `100.77.7.1:3001`. One-line sed + Traefik HUP. **Phase P10.**
4. **Mission Control dead (target: paused).** Per J7 directive 2026-07-09: do not allocate resources now. Source kept at `hermes-workspace-src/`. **Phase P2 deferred.**
5. **CryptPad not enabled.** Module written; `enable = true` line absent. **Phase P7.**

## 4. Routing / proxy issues (live)

- **Talk (`talk.gatewood.xyz`)**: Cloudflare tunnel DNS resolves to IPv6 ULA on cloudflared, breaking the public route. Workaround: use `cloud.mononoke.local` for Spreed app via Spreed-on-same-Nextcloud; Talk video requires STUN/TURN not yet wired.
- **Outpost Traefik → Forgejo**: routes 127.0.0.1 instead of 100.77.7.1 (see Top 5 #3).
- **agent-shared Forgejo path** (linuxserver container on Mononoke): not deployed; only NixOS Forgejo on `:3001` is the canonical instance.

## 5. Deployment drift (live)

- **wolfpack.nix** is imported in `mononoke/default.nix` but `services.wolfpack.enable = false`. Per-wolf units today are managed by ad-hoc `hermes-cli install`; P1 will flip to the NixOS module.
- **Multiplex + per-wolf coexistence**: multiplex on `:8642` (PID 490006, started 2026-07-07 02:01:57Z) coexists with 9 per-wolf units on `8644-8652`. P0 will resolve.
- **Per-wolf Nextcloud identity**: only `san` has one; wolves would auth as `san` if they wrote to Nextcloud. P3.
- **agent-card YAMLs**: 2/11 written (`san.yaml`, `ashitaka.yaml`); 9 missing. P9.

## 6. Active known drift (for J7 review)

- AGENTS.md / README.md / STATUS.md / notes/ / decisions/ in `starros-v1/` (parent of `repo/`) are the pre-canonical scratchpad. They predate the canonical spec; do not sync. The canonical contents live in `repo/decisions/`, `repo/docs/`, etc.
- `~/.hermes/wolf-souls/<wolf>/` is a second SOUL.md location, sibling to `~/.hermes/profiles/<wolf>/SOUL.md`. The profiles tree is canonical; the wolf-souls tree is staging.
- `keep.starrwulfe.xyz` resolves to Outpost (or external); not on Mononoke podman list. Phase P5 needs the OIDC end-to-end smoke.

## 7. Audit log

- 2026-07-07: initial San audit dossier (`~/.hermes/cron/output/2026-07-07_mononoke_superapp_architecture_dossier.md`)
- 2026-07-07: wolfpack round-2 audit (`~/.hermes/cron/output/2026-07-07_wolfpack_audit_round2.md`)
- 2026-07-09: spec canonicalization (PR #1, commit `21dee6d`)
- 2026-07-09: doc-canon pass (PR #2, this file)
