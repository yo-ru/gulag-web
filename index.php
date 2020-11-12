<?php session_start();
// Config
$config = include("config.php");

// Privileges
include "assets/objects/privileges.php";

// Try session login.
include "assets/objects/account.php";
$account->sessionLogin();

/*
Message
Try and get session defined message
(usually set on login), otherwise default
to empty message array then NULL out session message.
*/
$msg = $_SESSION["msg"] ?? array(
  "type" => "", 
  "msg" => ""
);
unset($_SESSION["msg"]);
?>

<html>
  <head>
    <!-- Title -->
    <title><?= $config->instanceName ?> - Home</title>

    <!-- JQuery and Popper -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <!-- Font Awesome -->
    <script src="https://kit.fontawesome.com/e5971878b8.js" crossorigin="anonymous"></script>

    <!-- Custom Style -->
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <!-- Header -->
    <?php include "assets/content/header.php" ?>

    <!-- Content -->
    <div class="container">
      <?php if (array_filter($msg)) : ?>
      <div class="alert alert-<?= $msg["type"] ?> mt-3 mb-0" role="alert">
        <?= $msg["msg"] ?>
      </div>
      <?php endif; ?>
      <div class="row">
        <div class="col rounded mt-3 mb-3 pl-5 pr-5 bg-dark text-white">
          <div class="row">
            <div class="gulag-avatar"></div>
            <div class="col pl-0 pr-0 text-center justify-content-center align-self-center">
              <h1 class="font-weight-bold">
                <?= $config->instanceName ?>
              </h1>
              <p>
                Welcome to 
                <span class="font-weight-bold">
                  <?= $config->instanceName, "." ?>
                </span>
                We are a osu! private server mainly based around the relax mod - 
                featuring score submission, leaderboards & rankings, custom pp, 
                and much more for both relax and vanilla osu!
              </p>
              <?php if ($account->isAuthenticated()) : ?>
              <a class="btn btn-info btn-lg" href="/u/<?= $account->getID() ?>">View Profile</a>
              <a class="btn btn-light btn-lg" href="/leaderboards.php">View Leaderboards</a>
              <?php else : ?>
              <a class="btn btn-info btn-lg" href="/docs/connect.php">How to Connect</a>
              <a class="btn btn-light btn-lg" href="/register.php">Register</a>
              <?php endif; ?>

            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <?php include "assets/content/footer.php" ?>
  </body>
</html>
