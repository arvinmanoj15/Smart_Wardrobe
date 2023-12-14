<?php
$scriptPath = '/home/arvin/Smart_Wardrobe/state_machine.sh';

// Change to the correct directory
chdir('/home/arvin/Smart_Wardrobe');

// Execute the script and capture the output
$output = shell_exec(escapeshellcmd($scriptPath) . ' 2>&1');

echo nl2br(htmlspecialchars($output));
?>

