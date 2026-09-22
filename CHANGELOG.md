# Changelog

All notable changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/) and the
project uses semantic-ish version numbers (v0.x during delivery, v1.0 at handover).

## [Unreleased]

### Added

- 2026-09-20 — Repository bootstrap: README, .gitignore, requirements.
- 2026-09-20 — Project scaffold: Flask application factory, SQLite models for
  clients, animals, properties and the two kinds of appointments, consulting
  timetable rules and booking validation helpers, pytest suite, GitHub Actions
  CI, pull request template, and a seed script with the case study's sample data.
- 2026-09-21 — Deployment configuration: `.env` support with a checked-in
  `.env.example`, bootstrap and run scripts for Windows and Unix, a WSGI entry
  point, and a deployment guide (`docs/DEPLOYMENT.md`).
