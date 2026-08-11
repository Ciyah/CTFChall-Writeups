---
ctf: HTBLabs
title: The Suspicious Domain
category: osint
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# The Suspicious Domain

## Challenge
Following the discovery of the suspicious social media profile TechReviewer2024, investigators have identified a related domain that appears to be part of the same astroturfing campaign. The domain alexmorgan-reviews.net has been flagged for hosting fake review content targeting technology companies. Your task is to investigate this domain's registration information and uncover the contact details hidden within the WHOIS records IP: 154.57.164.66:30101 .

## Approach

1. Opened the supplied DomainScope service and inspected its WHOIS, DNS, threat
   intelligence, and website preview panels for `alexmorgan-reviews.net`.
2. Extracted the registrant contact and registration details directly from the
   displayed WHOIS record.
3. Correlated the negative review content and shared analytics identifier to
   identify TechFlow as the targeted company.
4. Submitted the nine investigation answers and requested the final flag.

## Tools

- `curl`
- Browser application API (`/api/start-challenge`, `/api/submit-answer`,
  `/api/get-flag`)

## Lessons

- WHOIS contact fields provide useful pivots across related infrastructure.
- Disposable email providers, shared analytics IDs, repeated nameservers, and
  clustered registration dates are strong indicators of a coordinated campaign.
- The service expected the email provider's display name (`TempMail`) rather
  than its domain (`tempmail.com`).

## Flag

`HTB{redacted}`
