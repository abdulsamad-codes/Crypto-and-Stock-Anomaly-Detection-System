<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Feedback | Classic PHP</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 50px; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        input[type="submit"] { background-color: #58A6FF; color: white; border: none; cursor: pointer; font-weight: bold; }
        input[type="submit"]:hover { background-color: #1f6feb; }
        h2 { color: #333; text-align: center; }
    </style>
</head>
<body>

<div class="container">
    <h2>System Feedback (PHP)</h2>
    <p style="font-size: 0.8em; color: #666; text-align: center;">This module uses Traditional PHP as per Lab requirements.</p>
    <form action="insert.php" method="POST">
        <label>Developer Name:</label>
        <input type="text" name="name" required placeholder="Enter name">
        
        <label>Email Address:</label>
        <input type="email" name="email" required placeholder="Enter email">
        
        <label>Message/Issue:</label>
        <textarea name="message" rows="4" required placeholder="Describe the anomaly feedback..."></textarea>
        
        <input type="submit" value="Submit to Database">
    </form>
    <br>
    <a href="../" style="display: block; text-align: center; color: #58A6FF; text-decoration: none;">← Back to AI Dashboard</a>
</div>

</body>
</html>
