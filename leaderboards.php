<?php session_start();
// Config
$config = include("config.php");

// Database
include "assets/database/database.php";

// Privileges
include "assets/objects/privileges.php";

// Try session login.
include "assets/objects/account.php";
$account->sessionLogin();

/*
Let me try and explain this.
PHP multivariables are fucking terrible.
We're setting $mod and $_SESSION to the "$_POST"ed value.
Then since on submit the $_POST value is NULLed we default
to the cached value and if the cached value is NULLed we
default to the following combination:
Mod: Vanilla,
Mode: Standard,
Type: Performance.

This is the peak of cursed PHP.
*/
$mod = $_SESSION["lastMod"] = $_POST["mod"] ?? $_SESSION["lastMod"] ?? "vn"; // Options: vn, rx, ap.
$mode = $_SESSION["lastMode"] = $_POST["mode"] ?? $_SESSION["lastMode"] ?? "std"; // Options: std, taiko, catch, mania.
$type = $_SESSION["lastType"] = $_POST["type"] ?? $_SESSION["lastType"] ?? "performance"; // Options: performance, score.

// Special case for autopilot.
if ($mod == "ap") {
  $mode = $_SESSION["lastMode"] = "std";
}

// Query
$query = "SELECT users.id, users.name, users.creation_time, users.priv, users.country, ";

// Build stats rows for $query.
$stat = array(
    "tscore",
    "rscore",
    "pp",
    "plays",
    "playtime",
    "acc",
    "maxcombo"
);
foreach($stat as $s) {
    // If $s is the last item in the array, append ", ".
    if ($s != "maxcombo") {
        $query .= $db->real_escape_string("stats." . $s . "_" . $mod . "_" . $mode . ", ");
    // $s is last item in array, append " ".
    } else {
        $query .= $db->real_escape_string("stats." . $s . "_" . $mod . "_" . $mode . " ");
    }
}

// Join users with stats.
// NOTE: Ignore bot (1).
$query .= "FROM users JOIN stats USING(id) WHERE users.id != 1 ";

// Order based on $type.
if ($type == "performance") {
    $query .= $db->real_escape_string("ORDER BY stats.pp_" . $mod . "_" . $mode . " DESC;");
} else if ($type == "score") {
    $query .= $db->real_escape_string("ORDER BY stats.rscore_" . $mod . "_" . $mode . " DESC;");
}

// Fetch users from query.
$users = $db->query($query);
?>

<html>
  <head>
    <!-- Title -->
    <title><?php echo $config->instanceName ?> - Leaderboards</title>

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
      <div class="row">
        <div class="col rounded mt-3 mb-3 pt-5 pb-5 pl-5 pr-5 bg-dark text-white">
          <h1 class="text-center text-weight-bold">
            Leaderboards  
          </h1>
          <form action="" method="post">
            <div class="text-center">
              <div class="btn-group" role="group" aria-label="Mod Mode">
                <button name="mod" value="vn" type="submit" class="btn btn-secondary <?php if ($mod=="vn") { ?>active<?php } ?>">Vanilla</button>
                <button name="mod" value="rx" type="submit" class="btn btn-secondary <?php if ($mod=="rx") { ?>active<?php } ?>" <?php if ($mode=="mania") { ?>disabled<?php } ?>>Relax</button>
                <button name="mod" value="ap" type="submit" class="btn btn-secondary <?php if ($mod=="ap") { ?>active<?php } ?>">Autopilot</button>
              </div>
              <div class="btn-group" role="group" aria-label="Modes">
                <button name="mode" value="std" type="submit" class="btn btn-secondary <?php if ($mode=="std") { ?>active<?php } ?>">Standard</button>
                <button name="mode" value="taiko" type="submit" class="btn btn-secondary <?php if ($mode=="taiko") { ?>active<?php } ?>" <?php if ($mod=="ap") { ?>disabled<?php } ?>>Taiko</button>
                <button name="mode" value="catch" type="submit" class="btn btn-secondary <?php if ($mode=="catch") { ?>active<?php } ?>" <?php if ($mod=="ap") { ?>disabled<?php } ?>>Catch</button>
                <button name="mode" value="mania" type="submit" class="btn btn-secondary <?php if ($mode=="mania") { ?>active<?php } ?>" <?php if ($mod=="ap"||$mod=="rx") { ?>disabled<?php } ?>>Mania</button>
              </div>
              <div class="btn-group" role="group" aria-label="Leaderboard Type">
                <button name="type" value="performance" type="submit" class="btn btn-secondary <?php if ($type=="performance") { ?>active<?php } ?>">Performance</button>
                <button name="type" value="score" type="submit" class="btn btn-secondary <?php if ($type=="score") { ?>active<?php } ?>">Score</button>
              </div>
            </div>
          </form>
          <table class="table table-dark text-center mt-3">
            <thead>
              <tr>
                <th scope="col">Rank</th>
                <th scope="col">Name</th>

                <?php /* Performance */ if ($type == "performance") : ?>
                <th scope="col">Performance</th>
                <?php /* Score */ elseif ($type == "score") : ?>
                <th scope="col">Score</th>
                <?php endif; ?>
                
                <th scope="col">Accuracy</th>
                <th scope="col">Play Count</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach($users as $key=>$user) : ?>
              <tr>
                <th scope="row">#<?php echo $key+1 ?></th>
                <td><?php echo $user["name"]?></td>

                <?php /* Performance */ if ($type == "performance") : ?>
                <td><?php echo $user["pp_" . $mod . "_" . $mode] ?>pp</td>
                <?php /* Score */ elseif ($type == "score") : ?>
                <td><?php echo $user["rscore_" . $mod . "_" . $mode] ?></td>
                <?php endif; ?>

                <td><?php printf("%.2f", $user["acc_" . $mod . "_" . $mode]) ?>%</td>
                <td><?php echo $user["plays_" . $mod . "_" . $mode] ?></td>
              </tr>
              <?php endforeach; ?>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <?php include "assets/content/footer.php" ?>
  </body>
</html>
