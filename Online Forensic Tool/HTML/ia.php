<?php
    if (isset($_GET['status'])) {
        $sta = $_GET['status'];
        echo "<script type='text/javascript'>alert('$sta');</script>";
    }
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css" 
            integrity="sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm" crossorigin="anonymous">
        <link rel="stylesheet" href="../CSS/ia.css">

        <title>OWL | IA</title>
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
                        <a href="eha.php" class="navbar_links">EHA</a>
                    </li>
                    <li class="navbar_item">
                        <a href="ia.php" class="navbar_links" style="color: #ffd900;">IA</a>
                    </li>
                </ul>
            </div>
        </nav>
        <div class="wrapper">
            <div class="grid-container" style="border: 2px solid #B22222;">
                <div class="grid-container" style="margin-top: 10px; margin-bottom: 10px; margin-left: 10px; margin-right: 10px;">
                <h2>Start a new analysis</h2>
                    
                    <form action="../PHP/upload_image.php" method="POST" enctype="multipart/form-data">
                        <div class="row" style="margin-top: 10px; margin-bottom: 20px;">
                            <div class="row">
                                <label for="picture_file">Upload Image File</label>
                            </div>
                            <div class="row">
                                <input type="file" accept="image/png, image/jpeg, image/jpg, image/bmp" name="uploaded_image_file" id="uploaded_image_file" class="form-control" style="margin-top: 2%; color: black;" required>
                            </div>
                        </div>
                        
                        <div class="row">
                            <input type="submit" name="upload" value="Upload Image File">
                        </div>
                    </form>
                </div>
            </div>

            <div class="grid-container" style="margin-top: 30px; border: 2px solid #B22222;">
                <div class="grid-container" style="margin-top: 10px; margin-bottom: 10px; margin-left: 10px; margin-right: 10px;">
                <h2>Fetch old analysis status</h2>
                    
                    <form action="../PHP/fetch_image.php" method="POST" enctype="multipart/form-data">
                        <div class="row" style="margin-top: 10px; margin-bottom: 20px;">
                            <div class="row">
                                <label for="analysis_id">Enter Analysis ID Number</label>
                            </div>
                            <div class="row">
                                <input type="text" name="analysis_id" id="analysis_id" class="form-control" style="color: black;" required>
                            </div>
                        </div>
                        
                        <div class="row">
                            <input type="submit" name="search" value="Fetch Image Analysis Status">
                        </div>
                    </form>
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