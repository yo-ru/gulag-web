<?php

// Logout POST request.
if (isset($_POST["logout"])) {
  $account->logout();
}

?>

<head>
  <!-- Custom Style -->
  <link rel="stylesheet" href="header/header.css">
</head>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" href="/">gulag</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/index.php") { ?>active<?php } ?>">
        <a class="nav-link" href="/">Home</a>
      </li>
      <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/leaderboards.php") { ?>active<?php } ?>">
        <a class="nav-link" href="/leaderboards.php">Leaderboards</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Information
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/documentation.php") { ?>active<?php } ?>" href="/documentation.php">
            Documentation
          </a>
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/rules.php") { ?>active<?php } ?>" href="/rules.php">
            Rules
          </a>
        </div>
      </li>
    </ul>
    <ul class="navbar-nav ml-auto">
      <div class="searchbar mr-sm-2">
          <input class="search_input" type="text" name="search" placeholder="Search for a player...">
          <a class="search_icon"><i class="fa fa-search"></i></a>
      </div>
      <?php if ($account->isAuthenticated()) : ?>
      <li class="nav-item active">
        <a class="nav-link" href="/u/<?php echo $account->getID() ?>">
            <?php echo $account->getUsername() ?>
        </a>
      </li>
      <li class="nav-item">
        <form class="m-0" action="" method="post">
          <input class="nav-link link-button" name="logout" type="submit" value="Logout" />
        </form>
      </li>
      <?php else : ?>
      <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/login.php") { ?>active<?php } ?>">
        <a class="nav-link" href="/login.php">
          Login
        </a>
      </li>
      <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/register.php") { ?>active<?php } ?>">
        <a class="nav-link" href="/register.php">
          Register
        </a>
      </li>
      <?php endif; ?>
    </ul>
  </div>
</nav>