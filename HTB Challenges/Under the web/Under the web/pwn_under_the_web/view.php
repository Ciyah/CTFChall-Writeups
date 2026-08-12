<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Full Image View</title>
    <style>
        body {
            background-color: #001a33;
            margin: 0;
            padding: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            color: white;
        }
        img {
            max-width: 90%;
            max-height: 90%;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }

        .page-button {
            margin-top: 20px;
            text-align: center;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 5px;
            text-decoration: none;
        }
        .content {
            text-align: left;
            color: white;
            width: 80%; /* Adjust width as needed */
        }
    </style>
</head>
<body>
    <div class="content">
    <?php
    if (isset($_GET['image'])) {
        $image = urldecode($_GET['image']);
        if (file_exists($image)) {
            echo '<img src="data:image/png;base64,' . base64_encode(file_get_contents($image)) . '" alt="Full Image">';
        } else {
            echo '<p>Image not found.</p>';
        }
    } else {
        echo '<p>No image specified.</p>';
    }
    ?>
    </div>
    <div class="page-button">
        <a href="index.php" class="button">Back to Gallary</a>
    </div>
</body>
</html>