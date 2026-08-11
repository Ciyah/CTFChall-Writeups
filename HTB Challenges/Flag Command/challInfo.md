---
ctf: HTBLabs
title: Flag Command
category: web
difficulty: unknown
tags: []
flag_format: HTB{...}
date: 2026-08-11
---

# Flag Command

## Challenge
Embark on the Dimensional Escape Quest where you wake up in a mysterious forest maze that's not quite of this world. Navigate singing squirrels, mischievous nymphs, and grumpy wizards in a whimsical labyrinth that may lead to otherworldly surprises. Will you conquer the enchanted maze or find yourself lost in a different dimension of magical challenges? The journey unfolds in this mystical escape IP:154.57.164.75:31481 

## Approach
1. Requested the application and inspected its JavaScript assets.
2. `main.js` revealed that valid commands are fetched from `/api/options` and
   submitted as JSON to `/api/monitor`.
3. The options response contained a separate `secret` command:
   `Blip-blop, in a pickle with a hiccup! Shmiggity-shmack`.
4. Submitted that command directly to the monitor endpoint:

   ```bash
   curl -X POST http://154.57.164.75:31481/api/monitor \
     -H 'Content-Type: application/json' \
     --data '{"command":"Blip-blop, in a pickle with a hiccup! Shmiggity-shmack"}'
   ```

   The JSON response disclosed the flag.

## Tools

- `curl`
- Browser/client-side JavaScript inspection

## Lessons

- Client-accessible API responses should not contain secret game commands.
- Frontend validation is not an authorization boundary; API endpoints can be
  called directly.

## Flag

`HTB{D3v3l0p3r_t00l5_4r3_b35t__t0015_wh4t_d0_y0u_Th1nk??}`
