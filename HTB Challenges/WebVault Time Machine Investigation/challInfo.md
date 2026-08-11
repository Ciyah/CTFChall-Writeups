---
ctf: HTBLabs
title: WebVault Time Machine Investigation
category: osint
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# WebVault Time Machine Investigation

## Challenge
Following the discovery of suspicious negative reviews targeting TechCorp's XyloPhone product line, investigators have identified a website alexmorgan-reviews.net that appears to be the source of coordinated negative review campaigns. The reviews are well-written and appear legitimate, but the consistently negative sentiment across all TechCorp products raises suspicions of corporate espionage. Your task is to investigate this website's history using the WebVault Internet Archive and uncover any hidden connections that might explain the bias against TechCorp products. IP: 154.57.164.67:30616

## Approach
- Reviewed all four WebVault snapshots in chronological order.
- The August 15, 2023 snapshot's "About Me" section identifies Alex Morgan as a former RivalTech Marketing Specialist.
- Later snapshots show the site pivoting into product analysis/review services and then publishing consistently negative TechCorp XyloPhone reviews, establishing the conflict of interest.

## Tools
- WebVault snapshot timeline
- `curl` and frontend source inspection to verify the archived content

## Lessons
- Historical snapshots can reveal affiliations removed during later rebranding.
- The earliest capture provided the former company and role required by the flag format.

## Flag
HTB{redacted}
