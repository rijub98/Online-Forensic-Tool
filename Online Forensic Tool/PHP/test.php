<!DOCTYPE html>
<html lang="en">
    <body>
        <div class="wrapper">
            <div class="container">
                <h2>Email Header Analysis Status</h2>
            </div>
            <?php
            $my_command = escapeshellcmd('python ..\PYTHON\test.py');
            $command_output = shell_exec($my_command);

            $line1 = preg_split('#\r?\n#', $command_output, 0)[0];
            $line2 = preg_split('#\r?\n#', $command_output, 0)[1];
            echo $line1;
            echo "<br>";
            echo $line2;
            echo "<br>";
            $command_output = substr($command_output, strpos($command_output, "\n") + 1);
            $command_output = substr($command_output, strpos($command_output, "\n") + 1);
            echo $command_output;
            ?>
        </div>
        
    </body>
</html>