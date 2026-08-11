---
ctf: HTBLabs
title: Follow The Money
category: osint
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Follow The Money

## Challenge
Following the discovery of coordinated social media activity and suspicious domain registrations, investigators have uncovered evidence of cryptocurrency payments being used to fund the fake review campaign. Reddit posts from TechReviewer2024 mention Payment sent to usual wallet and Next batch payment due Friday, suggesting a systematic payment structure. Your task is to investigate the CryptoTrace blockchain to trace the money flow and identify the main funding wallet behind this operation IP: 154.57.164.82:31720.

## Approach
- Started a challenge session and inspected the Evidence Terminal. The primary
  suspect address was `bc1q7x4a9m2k8j5p3r9s1t6u8v2w7x4z9a1b2c3d4e5`.
- Correlated the address with Chainalysis, Crystal, and Arkham data. The inbound
  funding source was Binance, while KYC/intelligence data identified James
  Mitchell Chen (`james.crypto.2024@proton.me`) in San Francisco at
  `37.774929, -122.419416`.
- Summed the seven Cluster Charlie payments:
  `0.00234567 + 0.00189234 + 0.00345123 + 0.00278945 + 0.00156789 +
  0.00298734 + 0.00387612 = 0.01891004 BTC`.
- Analyzed transaction `q7r8s9t0u1v2345678901234567890123456789012` with
  OXT, which identified the obfuscation protocol as Wasabi (CoinJoin).
- Submitted all six answers sequentially and requested the final flag.

## Tools
- CryptoTrace Evidence Terminal
- Chainalysis KYT
- Blockscout
- Crystal Analytics
- Arkham Intelligence
- OXT Advanced

## Lessons
- Tool usage must be recorded in the session, and the investigation flags must
  be submitted in order.
- Cross-platform wallet attribution joined the blockchain flow, KYC identity,
  mixing method, and geographic evidence.

## Flag
`HTB{redacted}`
