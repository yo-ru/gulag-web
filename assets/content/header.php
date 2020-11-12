<?php
// Logout POST request.
if (isset($_POST["logout"])) {
  $account->logout();
}
?>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <a class="navbar-brand" href="/"><?= $config->instanceName ?></a>
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
        <a class="nav-link" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Information
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/docs") { ?>active<?php } ?>" href="/docs">
            Documentation
          </a>
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/docs/rules.php") { ?>active<?php } ?>" href="/docs/rules.php">
            Rules
          </a>
        </div>
      </li>

      <?php if ($account->isAuthenticated() && ($account->getPrivileges() & Privileges::Staff)) : ?>
      <li class="nav-item <?php if (strpos($_SERVER["PHP_SELF"], "/admin/") !== false) { ?>active<?php } ?>">
        <a class="nav-link" href="/admin">Admin Panel</a>
      </li>
      <?php endif; ?>
    </ul>
    <ul class="navbar-nav ml-auto">
      <div class="searchbar mr-sm-2">
          <input class="search_input" type="text" name="search" placeholder="Search for a player...">
          <a class="search_icon"><i class="fa fa-search"></i></a>
      </div>
      <?php if ($account->isAuthenticated()) : ?>
      <li class="nav-item dropleft">
        <a class="nav-link active" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <?= $account->getUsername() ?>
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/user?id=" . $account->getID()) { ?>active<?php } ?>" href="/user?id=<?= $account->getID() ?>">
            Profile
          </a>
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/friends.php") { ?>active<?php } ?>" href="/friends.php">
            Friends
          </a>
          <a class="dropdown-item <?php if ($_SERVER["PHP_SELF"]=="/settings.php") { ?>active<?php } ?>" href="/settings.php">
            Settings
          </a>
        </div>
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