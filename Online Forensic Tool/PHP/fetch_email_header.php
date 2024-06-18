<?php
    include 'connect.php';

    $analysis_id = $_POST['analysis_id'];

    $sql = "SELECT analysis_id FROM email_header WHERE email_header.analysis_id=$analysis_id";

    $res = mysqli_query($con,$sql);

    while($row = mysqli_fetch_array($res)){

        header("location: ../html/eha_analysis_results.php?analysis_id=".$analysis_id);
        die();
    }

    $status = "Failed to find unique analysis number";
    header("location: ../html/eha.php?status=".$status);

    die();
?> 