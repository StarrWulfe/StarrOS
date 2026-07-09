# StarrOS Stack Spec

## Purpose
StarrOS is an AI workspace and control plane built around Hermes-Agent, San, and the wolfpack. Its purpose is to provide a Mission Control environment for planning, execution, review, collaboration, artifact handling, and agent-driven work across projects.

## Core architecture
- San is the sovereign orchestrator.
- The wolfpack consists of ten specialized wolves with separate Hermes profiles, skills, memory scopes, and tool configurations.
- Wolves are real runtime identities, not just prompt personas.
- Mission Control is the main workspace shell.
- The stock Hermes dashboard remains a subsystem/tab inside the wider Mission Control experience.
- Mononoke is the primary NixOS host for deployment and runtime operations.

## Execution model
- Requests flow to San first.
- San normalizes requests into structured tasks/cards.
- San dispatches wolves one-by-one or in groups.
- Progress, status changes, and outcomes should be logged to a DB/kanban system.
- Work is spec-driven, repo-backed, reviewable, and approval-gated.

## Repo and tasking model
- Forgejo is the canonical planning and execution surface.
- Specs, playbooks, prompts, backlog definitions, and packet templates live in the repo.
- External coding workers are allowed only for bounded, approved leaf cards.

## Secrets and config model
- Nix manages structural deployment and service topology.
- Hermes manages runtime secrets through the built-in Bitwarden skill.
- Secrets should not require rebuilds to rotate.
- Runtime `.env` state is Bitwarden-backed, not SOPS-owned.

## UX / workspace model
- Mission Control should feel like an AI-native workspace.
- It should support dashboarding, artifact interaction, collaborative/project work, and agent-assisted operations.
- Web-first is preferred; desktop wrapping is optional later.

## Known uncertainty / needs confirmation
- Exact ownership boundaries for GBrain, Mnemosyne, Nextcloud, and any other workspace subsystems.
- Final runtime topology on Mononoke after multiplex cleanup.
- Exact kanban schema and DB contract.
- Exact wolf roster, dimensions, and review lanes.
- Phase order for rollout from current state to full StarrOS.