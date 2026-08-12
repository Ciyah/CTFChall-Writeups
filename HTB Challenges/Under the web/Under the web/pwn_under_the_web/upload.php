<?php
    $uploadDir = 'uploads/';

    $image = $uploadDir . "starry_night.png";

    function CheckPng($file) {
        // Open the uploaded file in binary mode
        $handle = fopen($file['tmp_name'], 'rb');

        // Read the first 8 bytes (magic bytes) of the file
        $magicBytes = fread($handle, 8);

        // Close the file handle
        fclose($handle);

        // Check if the magic bytes match the PNG signature
        return $magicBytes === "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A";
    }

    function is_valid_path($path) {
        // Check if the path contains any suspicious patterns
        if ( strpos($path, '..') !== false ){
            return false;
        }
        return true;
    }


    if(isset($_FILES["file"]) && $_FILES["file"]["error"] === UPLOAD_ERR_OK) {
        $file = $_FILES['file'];
        $fileType = strtolower(pathinfo($file["name"], PATHINFO_EXTENSION));
        if($fileType !== 'png') {
            echo "<script>alert('Only PNG files are allowed.');</script>";
        } else {
            if(CheckPng($file)) {
                if(is_valid_path($file["name"])) {
                    $targetFilePath = $uploadDir . $file["name"];
                    if(move_uploaded_file($file["tmp_name"], $targetFilePath)) {
                        $image = $uploadDir . $file['name'];
                        echo "<script>alert('File uploaded successfully as " . basename($targetFilePath) . "');</script>";
                    }
                }
            } else {
                echo "<script>alert('Only PNG files are allowed.');</script>";
            }
        }
    }

    $info = getImgMetadata($image);
    $data = explode("\n", $info);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arts & Artist</title>
    <style>
        body {
            background-color: #001a33;
            margin: 0;
            padding: 15px 0 0 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; /* Make the body take up the full viewport height */
        }
        .content {
            text-align: center;
            color: white;
        }
        img {
            width: 80%; /* Adjust the width of the image as needed */
            border-radius: 5px; /* Rounded corners */
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); /* Add a shadow effect */
        }

        .upload-form {
            margin-top: 20px; /* Add some spacing between sections */
        }
        .upload-label {
            background-color: #4CAF50; /* Green background for upload button */
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="content">
        <img src="<?= $image ?>" alt="Image">
        <p><?= $data[0] ?></p>
        <p><?= $data[1] ?></p>
        <p><?= $data[2] ?></p>
    </div>

    <div class="upload-form">
        <form action="upload.php" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/png">
            <button type="submit">Upload</button>
        </form>
    </div>

</body>
</html
