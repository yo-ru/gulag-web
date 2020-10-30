<?php
// Config
$config = include("config.php");

?>

<html>
  <head>
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
    <?php include "header/header.php" ?>

    <!-- Content -->
    <div class="container">
      <div class="row">
        <div class="col rounded mt-3 mb-3 pl-5 pr-5 bg-dark text-white">
          <div class="row">
            <div class="col gulag-avatar"></div>
            <div class="col pl-0 pr-0 text-center justify-content-center align-self-center">
              <h1 class="font-weight-bold">
                <?php echo $config->instanceName ?>
              </h1>
              <p>
                Welcome to 
                <span class="font-weight-bold">
                  <?php echo $config->instanceName, "." ?>
                </span>
                We are a osu! private server mainly based around the relax mod - 
                featuring score submission, leaderboards & rankings, custom pp, 
                and much more for both relax and vanilla osu!
              </p>
              <a class="btn btn-info btn-lg" href="/docs/connect.php">How to Connect</a>
              <a class="btn btn-light btn-lg" href="/register.php">Register</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <?php include "footer/footer.php" ?>
  </body>
</html>
