<?php
    if (isset($_GET['analysis_id'])) {
        $analysis_id = $_GET['analysis_id'];
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css" 
            integrity="sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm" crossorigin="anonymous">
        <link rel="stylesheet" href="../CSS/eha.css">

        <title>OWL | EHA Status</title>
    </head>
    <body>
        <nav class="navbar">
            <div class="navbar_container">
                <a href="index.html" id="navbar_logo" class="navbar_logo">
                    <img src="../IMAGE/owl logo.png" alt="logo" class="logo"/>
                </a>
                <div class="navbar_toggle" id="mobile-menu">
                    <span class="bar"></span>
                    <span class="bar"></span>
                    <span class="bar"></span>
                </div>
                <ul class="navbar_menu">
                    <li class="navbar_item">
                        <a href="eha.php" class="navbar_links" style="color: #ffd900;">EHA</a>
                    </li>
                    <li class="navbar_item">
                        <a href="ia.php" class="navbar_links">IA</a>
                    </li>
                </ul>
            </div>
        </nav>
        <div class="wrapper">
            <div class="container">
                <h2>Email Header Analysis Details</h2>
                <?php
                    include '../php/connect.php';
                    $sql = "SELECT * FROM email_header WHERE email_header.analysis_id=$analysis_id";
                    $res = mysqli_query($con,$sql);
                    $row = mysqli_fetch_array($res);

                    $results_dir = "../RESULTS/EMAIL_HEADERS/";
                    $uploaded_file = $row['uploaded_email_header_file'];
                    $analysis_report_file = $row['analysis_report_file'];
                    $verdict = $row['verdict'];

                    if(empty($analysis_report_file)){
                        $my_command = escapeshellcmd('python ../PYTHON/email_auth.py '.$uploaded_file);
                        $command_output = shell_exec($my_command);

                        # Get the different values
                        $verdict = preg_split('#\r?\n#', $command_output, 0)[0];
                        if($verdict == "Authentic" || $verdict == "Tampered"){
                            $analysis_report_file = preg_split('#\r?\n#', $command_output, 0)[1];
                            $sql = "UPDATE email_header SET analysis_report_file='{$analysis_report_file}', verdict='{$verdict}' WHERE email_header.analysis_id=$analysis_id";
                            $res = mysqli_query($con,$sql);

                            if(mysqli_affected_rows($con) == 0){
                                trigger_error("Unable to update database", E_USER_ERROR);
                            }
                        }
                        else{
                            trigger_error("Unable to update database", E_USER_ERROR);
                        }
                    }
                    mysqli_close($con);
                ?>
                <style>
                    tr, td {
                    padding: 15px;
                    }
                </style>
                <h3 style="margin-top: 30px;">
                    <div class="row">
                        <label for="email_header_id">
                            <?php
                                echo "Your Email Header Analysis ID Number is: ".$analysis_id; 
                            ?>
                        </label>
                    </div>
                </h3>
                <h3 style="margin-top: 30px;">
                    <div class="row">
                        <label for="email_header_id">
                            <?php
                                echo "Authentication Verdict: ".$verdict;
                            ?>
                        </label>
                    </div>
                </h3>
                <h3 style="margin-top: 30px;">
                    <div class="row">
                        <label for="detailed_report">
                            Detailed Report:
                        </label>
                    </div>
                </h3>
                <div class="row" style="margin-top: 30px;">
                    <?php 
                        echo "<pre>";
                        if(!empty($analysis_report_file)){
                            echo file_get_contents($results_dir.$analysis_report_file);
                        }
                        echo "</pre>";
                    ?>
                </div>
            </div>
        </div>
        <div class="btns">
            <button class="btn btn--subtle"></button>
        </div>
        <script src="../JAVASCRIPT/app.js"></script>
        <script src="../JAVASCRIPT/input.js"></script>
    </body>
</html>