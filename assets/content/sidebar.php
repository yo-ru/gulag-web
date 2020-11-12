<div class="navbar navbar-dark align-items-start col-lg-2 mt-1 mb-1 mr-1 pt-3 pb-5 pl-4 pr-4 bg-dark text-white sidebar">
    <ul class="navbar-nav flex-lg-column">
        <li class="nav-item mb-2">
            <span class="admin-title text-weight-bold"><?= $config->instanceName ?> Admin Panel</span>
        </li>
        <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/admin/index.php") { ?>active<?php } ?>">
            <a class="nav-link" href="/admin"><i class="fa fa-tachometer-alt"></i> Dashboard</a>
        </li>
        <?php if ($account->getPrivileges() & Privileges::ManageUsers) : ?>
        <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/admin/users.php") { ?>active<?php } ?>">
            <a class="nav-link" href="/admin/users.php"><i class="fa fa-users"></i> Users</a>
        </li>
        <?php endif; ?>
        <?php if ($account->getPrivileges() & Privileges::ManageBeatmaps) : ?>
        <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/admin/beatmap-management.php") { ?>active<?php } ?>">
            <a class="nav-link" href="/admin/beatmap-management.php"><i class="fa fa-fire"></i> Beatmap Management</a>
        </li>
        <?php endif; ?>
        <li class="nav-item <?php if ($_SERVER["PHP_SELF"]=="/admin/logs.php") { ?>active<?php } ?>">
            <a class="nav-link" href="/admin/logs.php"><i class="fa fa-terminal"></i> Logs</a>
        </li>
    </ul>
</div>