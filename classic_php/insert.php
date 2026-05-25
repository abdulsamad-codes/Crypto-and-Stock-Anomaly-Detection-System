<?php
$servername = "localhost";
$username = "root";
$password = "AAdd541@$"; // Using your actual DB password from Python config
$dbname = "crypto_anomaly_db";

// Create connection using procedural style my teacher likes
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Get form data
$name = $_POST['name'];
$email = $_POST['email'];
$message = $_POST['message'];

// SQL to insert data into the new feedback table
$sql = "INSERT INTO user_feedback (name, email, message) VALUES ('$name', '$email', '$message')";

if (mysqli_query($conn, $sql)) {
    echo "<div style='text-align:center; padding:50px; font-family:Arial;'>";
    echo "<h1>Data Inserted!</h1>";
    echo "<p>Your feedback has been saved to <b>crypto_anomaly_db.user_feedback</b> via PHP.</p>";
    echo "<a href='index.php'>Go Back</a> | <a href='../'>Main Dashboard</a>";
    echo "</div>";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

// Close connection
mysqli_close($conn);
?>
