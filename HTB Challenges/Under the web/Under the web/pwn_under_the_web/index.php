<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arts & Artist - Gallery</title>
    <style>
        body {
            background-color: #001a33;
            margin: 0;
            padding: 15px 0 0 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        .content {
            text-align: left;
            color: white;
            width: 80%; /* Adjust width as needed */
        }
        .image-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        img {
            width: 150px; /* Thumbnail size */
            height: auto;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            margin-right: 20px; /* Spacing between image and text */
        }
        .info {
            flex: 1;
        }
        .upload-page-button {
            margin-top: 20px;
            text-align: center;
        }
        .upload-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            text-decoration: none;
        }
        a {
            text-decoration: none;
            color: white;
        }
    </style>
</head>
<body>
    <div class="content">
        <?php
        $directory = 'uploads/';
        $images = glob($directory . "*.png"); // Get all .png files from the directory

        foreach ($images as $image) {
            $info = getImgMetadata($image);
            $data = explode("\n", $info);

            echo '<a href=/view.php?image=' . $image . '>';
            echo '<div class="image-container">';
            echo '<img src="data:image/png;base64,' . base64_encode(file_get_contents($image)) . '" alt="Full Image">';
            echo '<div class="info">' . 
                $data[0] . "<br>" .
                $data[1] . "<br>" .
                $data[2] . "<br>"
            . '</div>';
            echo '</div></a>';
        }
        ?>
    </div>

    <div class="upload-page-button">
        <a href="upload.php" class="upload-button">Upload Image</a>
    </div>
</body>
</html>
