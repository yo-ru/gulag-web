<?php session_start();
// Config
$config = include("config.php");

// Try session login
include "objects/account.php";
$account->sessionLogin();
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
        <div class="col rounded mt-3 mb-3 pt-5 pb-5 pl-5 pr-5 bg-dark text-white">
          <h1 class="text-center text-weight-bold">
            Leaderboards  
          </h1>
          <div class="text-center">
            <div class="btn-group" role="group" aria-label="Mod Mode">
              <button type="button" class="btn btn-secondary">Vanilla</button>
              <button type="button" class="btn btn-secondary active">Relax</button>
            </div>
            <div class="btn-group" role="group" aria-label="Modes">
              <button type="button" class="btn btn-secondary active">Standard</button>
              <button type="button" class="btn btn-secondary">Taiko</button>
              <button type="button" class="btn btn-secondary">Catch</button>
              <button type="button" class="btn btn-secondary">Mania</button>
            </div>
            <div class="btn-group" role="group" aria-label="Leaderboard Type">
              <button type="button" class="btn btn-secondary active">Performance</button>
              <button type="button" class="btn btn-secondary">Score</button>
            </div>
          </div>
          <table class="table table-dark text-center mt-3">
            <thead>
              <tr>
                <th scope="col">Rank</th>
                <th scope="col">Name</th>
                <th scope="col">Accuracy</th>
                <th scope="col">Play Count</th>
                <th scope="col">Performance</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">#1</th>
                <td>cmyui</td>
                <td>96.57%</td>
                <td>25,657</td>
                <td>11,564</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <?php include "footer/footer.php" ?>
  </body>
</html>
