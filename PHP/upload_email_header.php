<?php
    include 'connect.php';

    $dest_file_name = "";

    if(isset($_FILES['uploaded_email_header_file']['error'])){
        if($_FILES['uploaded_email_header_file']['error'] == 0){

            $target_dir = "../UPLOADS/EMAIL_HEADERS/";
            $orig_file_name = $_FILES["uploaded_email_header_file"]["name"];
            $temp_file_source = $_FILES["uploaded_email_header_file"]["tmp_name"];

            $dest_file_name = str_replace(" ", "_", $orig_file_name);
            $destination = $target_dir.$dest_file_name;

            for ($i=1; file_exists($destination); $i++)
            {
                $dest_file_name = $i.str_replace(" ", "_", $orig_file_name);
                $destination = $target_dir.$dest_file_name;
            }

            if(move_uploaded_file($temp_file_source, $destination)){
                $sql = "INSERT INTO email_header(uploaded_email_header_file, verdict) VALUES('{$dest_file_name}', 'Processing')";

                if($con->query($sql)){
                    $sql = "SELECT analysis_id FROM email_header ORDER BY analysis_id DESC LIMIT 1";
                    $res = mysqli_query($con,$sql);

                    $row_count = mysqli_fetch_array($res);
                    $analysis_id = $row_count["analysis_id"];

                    header("location: ../html/eha_analysis_results.php?analysis_id=".$analysis_id);
                }
                else {
                    $status = "Failed to start Email Header Analysis. Please reupload the file.";
                    header("location: ../html/eha.php?status=".$status);
                }
            }
            else {
                $status = "Failed to upload Email Header File";
                header("location: ../html/eha.php?status=".$status);
            }
        }
    }
    mysqli_close($con);
    die();
?> 