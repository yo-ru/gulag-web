<?php session_start();
// Config
$config = include("config.php");

// Privileges
include "assets/objects/privileges.php";

// Try session login.
include "assets/objects/account.php";
$account->sessionLogin();

// We're already authenticated; Redirect home.
if ($account->isAuthenticated()) {
    header("Location: /");
}

// Try form login
$msg = "";
if (isset($_POST["login"]) && !empty($_POST["username"]) && !empty($_POST["password"])) {
    try {
        $account->login($_POST["username"], $_POST["password"]);
    } catch (Exception $e) {
        $msg = $e->getMessage();
    }
}
?>

<html>
  <head>
    <!-- Title -->
    <title><?php echo $config->instanceName ?> - Login</title>

    <!-- JQuery and Popper -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">

    <!-- Custom Style -->
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <!-- Header -->
    <?php include "assets/content/header.php" ?>

    <!-- Content -->
    <div class="container">
      <div class="row w-50 mx-auto">
        <div class="col rounded mt-3 mb-3 p-5 bg-dark text-white text-center">
          <?php if ($msg) : ?>
          <div class="alert alert-danger" role="alert">
            <?php echo $msg ?>
          </div>
          <?php endif; ?>
          <form action="" method="post">
            <div class="form-group">
              <label for="usernameInput">Username</label>
              <input name="username" type="text" class="form-control" id="usernameInput" aria-describedby="usernameHelp" placeholder="Username">
              <small id="usernameHelp" class="form-text text-muted">Currently only username logins are available.</small>
            </div>
            <div class="form-group">
              <label for="passwordInput">Password</label>
              <input name="password" type="password" class="form-control" id="passwordInput" placeholder="Password">
            </div>
            <button name="login" type="submit" class="btn btn-secondary">Login</button>
          </form>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <?php include "assets/content/footer.php" ?>
  </body>
</html>
