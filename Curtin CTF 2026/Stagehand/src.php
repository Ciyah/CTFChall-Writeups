<?php
// Backstage pass desk for a community theatre. Crew preferences ride in a cookie.

class CrewPrefs {
    public $name = 'Guest';
    public $tagline = '';
    public $role = 'volunteer';
    public $theme = 'house-lights';
}

// Prints a line to the show report when a pass is retired.
class ShowReport {
    public $line;
    function __destruct() {
        echo "<!-- show report: " . $this->line . " -->";
    }
}

// Wraps text as a poster caption.
class Poster {
    public $content;
    function __toString() {
        return "[" . $this->content->caption() . "]";
    }
}

// Reads a cue sheet from the stage-management share.
class CueSheet {
    public $pattern = '/var/www/cues/opening.txt';
    function __call($name, $args) {
        if (strpos($this->pattern, '/var/www/') !== 0) {
            return 'cue sheets live under /var/www/';
        }
        $out = '';
        foreach (glob($this->pattern) as $f) {
            $real = realpath($f);
            if ($real === false || strpos($real, '/var/www/') !== 0) continue;
            $out .= file_get_contents($real);
        }
        return $out;
    }
}

$SECRET = getenv('PASS_SECRET') ?: 'dev-only';

// The desk abbreviates common backstage phrases to keep passes short.
function abbreviate($s) {
    return str_replace('dress rehearsal', 'DR', $s);
}

function seal($prefs) {
    global $SECRET;
    $s = abbreviate(serialize($prefs));
    return base64_encode($s) . '.' . hash_hmac('sha256', $s, $SECRET);
}

function load_prefs() {
    global $SECRET;
    if (!isset($_COOKIE['crew'])) {
        return new CrewPrefs();
    }
    list($b, $sig) = array_pad(explode('.', $_COOKIE['crew'], 2), 2, '');
    $s = base64_decode($b);
    if (!hash_equals(hash_hmac('sha256', $s, $SECRET), $sig)) {
        http_response_code(400);
        die('Tampered pass.');
    }
    $p = @unserialize($s);
    return ($p instanceof CrewPrefs) ? $p : new CrewPrefs();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $p = new CrewPrefs();
    $p->name = substr($_POST['name'] ?? 'Guest', 0, 40);
    $p->tagline = substr($_POST['tagline'] ?? '', 0, 200);
    $p->role = in_array($_POST['role'] ?? '', ['actor', 'tech', 'front-of-house']) ? $_POST['role'] : 'volunteer';
    setcookie('crew', seal($p), 0, '/');
    header('Location: /');
    exit;
}

$prefs = load_prefs();
?>
<!doctype html><meta charset="utf-8"><title>The Understudy - Backstage Desk</title>
<style>body{font-family:Georgia,serif;background:#2a0f14;color:#f3e6d0;max-width:620px;margin:3rem auto;padding:0 1rem}
input,select{display:block;margin:.5rem 0;padding:.5rem;width:100%;background:#3b1a20;color:#f3e6d0;border:1px solid #8c5a3c}
button{padding:.5rem 1rem;background:#d9a441;border:0}</style>
<h1>The Understudy Players</h1>
<p>Welcome to the backstage desk, <b><?= htmlspecialchars($prefs->name) ?></b> (<?= htmlspecialchars($prefs->role) ?>). <i><?= htmlspecialchars($prefs->tagline) ?></i>
Tonight: dress rehearsal. Costume tags and call sheets are printed at the desk.</p>
<form method="post"><input name="name" placeholder="your name"><input name="tagline" placeholder="a line for your pass"><select name="role">
<option>actor</option><option>tech</option><option>front-of-house</option></select><button>Check in</button></form>
