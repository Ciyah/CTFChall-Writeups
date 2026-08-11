---
ctf: HTBLabs
title: Social Media Investigation Hub
category: osint
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Social Media Investigation Hub

## Challenge
A tech company has reported suspicious negative reviews appearing across multiple platforms for their new product, the XyloPhone Pro. Initial investigations suggest these reviews might be part of a coordinated campaign by a competitor. The reviews appear authentic and well-written, but the consistently negative sentiment and coordinated timing across multiple social media platforms raises red flags. Your task is to investigate the username TechReviewer2024 across multiple social media platforms and uncover evidence of this coordinated activity using cross-platform OSINT techniques IP: 154.57.164.82:31640 .

## Solution

The investigation started by correlating the username `TechReviewer2024`
across ConnectPro, ChirpNet, and ForumHub. Reused identity details and activity
on those platforms connected the reviewer account to Alex Morgan and exposed
the coordinated campaign.

1. **Real name — Alex Morgan:** The ConnectPro headline identifies the user as
   "Alex Morgan (Tech Reviewer)."
2. **Previous employer — RivalTech Inc.:** ConnectPro lists Alex as a Marketing
   Specialist at RivalTech Inc. from January 2021 through December 2023.
3. **Operation codename — `operation_social_storm_2024`:** Alex's ForumHub post
   titled "XyloPhone Pro Campaign Coordination" explicitly names the operation.
4. **Account-creation period — February 2024:** ChirpNet shows that the account
   began following suspicious reviewer accounts such as `@ReviewMaster_Bob`
   and `@TechTruth_Sally` in February 2024.
5. **Targeted product — XyloPhone Pro:** The ForumHub coordination post contains
   the planned negative-review talking points for this product.
6. **ForumHub role — moderator:** The ForumHub profile identifies
   `u/TechReviewer2024` as a moderator of `r/TechReviews` and shows 24 posts in
   the current month.
7. **Education — University of California, Berkeley:** ConnectPro lists a
   Bachelor of Science in Marketing completed from 2017 to 2021.
8. **ConnectPro connections — 89:** The profile displays exactly 89 connections.
9. **ForumHub post karma — 1247:** The ForumHub profile displays 1,247 post
   karma, showing substantial activity over a short period.

After all nine answers were accepted, a `POST` request to `/api/get-flag` with
the active session ID returned the final flag.

## Tools

- Browser developer tools for inspecting the challenge application
- Cross-platform profile correlation
- HTTP requests to `/api/submit-answer` and `/api/get-flag`

## Lessons

- Reused usernames and biographical details can connect identities across
  otherwise separate platforms.
- Employment history, education, account age, and activity metrics provide
  useful corroborating evidence.
- Coordination posts can expose campaign attribution, intent, timing, and the
  specific target.

## Flag

`HTB{redacted}`
