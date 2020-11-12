<?php 

abstract class Privileges {
    // Privileges intended for all normal users.
    const Normal         = 1 << 0; // An unbanned player.
    const Verified       = 1 << 1; // Has logged in to the server in-game.

    // Has bypass to low-ceiling anti-cheat measures (trusted).
    const Whitelisted    = 1 << 2;

    // Donation tiers, recieves some extra benefits.
    const Supporter      = 1 << 4;
    const Premium        = 1 << 5;

    // Notable users, recieves some extra benefits.
    const Alumni         = 1 << 7;

    // Staff permissions, able to manage server state.
    const Tournament     = 1 << 10; // Able to manage match state without host.
    const Nominator      = 1 << 11; // Able to manage maps ranked status.
    const Mod            = 1 << 12; // Able to manage users (level 1).
    const Admin          = 1 << 13; // Able to manage users (level 2).
    const Dangerous      = 1 << 14; // Able to manage full server state.

    // Permission groups, groups used throughout gulag-web to manage access to certain pages/content.
    const Donator        = self::Supporter | self::Premium; // Those who are considered donators.
    const Staff          = self::Nominator | self::Mod | self::Admin | self::Dangerous; // Those who are considered staff.
    const ManageBeatmaps = self::Nominator | self::Dangerous; // Those who are able to manage beatmaps.
    const ManageUsers    = self::Mod | self::Admin | self::Dangerous; // Those who are able to manage users.
}

?>