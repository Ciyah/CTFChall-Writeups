---
ctf: "IBOH2026 CTF"
title: "Rules of Engagement"
category: "osint"
difficulty: ""
tags: []
flag_format: "IBOH26{...}"
date: "2026-11-14"
---

## Challenge

Author: @attain938

A routine penetration test against ACME Retail took an unexpected turn when unauthorized activity was detected on its production infrastructure. The legitimate pentester claims to have stopped testing, but the evidence says otherwise.

Use the provided files to answer these questions:

    Which production edge IP Address did the pentester contact that was out-of-scope?
    During the out-of-scope assessment, the pentester submitted a proof-of-concept request that resulted in an additional operating-system command being executed on PROD-WEB01. Under which Linux user account was the injected command executed? Submit the username only.
    How many distinct diagnostics requests after the stop acknowledgement were falsely attributed to the pentester? Submit the integer only.
    Following the suspicious diagnostics activity, a Python utility was executed on PROD-WEB01. What is the exact absolute path of the executable invoked by the sample() function?
    During the incident, two outbound data transfers were attempted from PROD-WEB01. What is the SHA-256 hash of the archive associated with the rejected transfer? Submit the complete 64-character hexadecimal hash.
    A ransomware artifact was staged on the filesystem. What was the Process ID (PID) of the process that executed the staging operation? Submit the PID only.

Combine each flag to follow this format: IBOH26{redacted}

## Approach

1. Recon — what you did to understand the challenge (files examined, services probed, binary inspected). Be specific.
2. The exact vulnerability/flaw identified.
3. The exact commands/payloads/scripts used to exploit it.
4. The final step that produced the flag.

## Tools

## Lessons

## Flag

