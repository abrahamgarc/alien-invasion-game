# alien-invasion-game



In Alien Invasion, the player starts off in a menu screen. The menu screen contains 5 buttons, Leaderboard, Play, Easy, Medium, and Hard. Each difficulty has slight diffrences featured below. If the leaderboard button is clicked a leaderboard which is connected to a database will appear and show the current top ten rankings. To go back to the manin menu players press the back button. Once the player selects a difficutly and hits play they control a rocket ship that appears at the bottom center of the screen (IF NO DIFFICULTY IS SELECTED EASY WILL BE DEFAULT). The player can move the ship right and left using the arrow keys and shoot bullets using the spacebar. When the game begins, a fleet of aliens fills the sky and moves across and down the screen. The player shoots and destroys the aliens. If the player destroys all the aliens, a new fleet appears that moves faster than the previous fleet. If any alien hits the player's ship or reaches the bottom of the screen, the player loses a ship. If the player loses all their ships on the top left of the screen, the game ends. The middle of the screen contains the players HighScore while the application is open, the right hand side contains the current score and current level. Once the player runs out of lives the main menu will reappear with a new box requesting a username. (NOTE: If you have played the game before please use the same username and it will override your previous score if the new score is higher.) Players can hit backspace to delete keys and hit enter when done. Every time the player runs out of lives they must hit enter to save their score however wont need to write down the username again. 

Players can hit P to start the game and Q to exit. 


        IF difficulty_level == 'EASY':
            ship_limit = 3
            bullets_allowed = 10
            ship_speed = 1
            bullet_speed = 2
            alien_speed = 1
            alien_points = 10

        IF difficulty_level == 'MEDIUM':
            ship_limit = 2
            bullets_allowed = 5
            ship_speed = 2
            bullet_speed = 3
            alien_speed = 2
            alien_points = 20 

        IF difficulty_level == 'HARD':
            ship_limit = 1
            bullets_allowed = 3
            ship_speed = 3
            bullet_speed = 4
            alien_speed = 3
            alien_points = 30


The game speed is increased by * 1.1 each level increase.
Apart from being worth different values based on difficutly alien values progressivly increase per level. ALIEN SCORE SCALING is BY * 1.2



What all the aliens in the screen are worth per level, per difficulty.

 Level   Easy    Medium    Hard 
 1      450.00  900.00   1350.00
 2      540.00  1080.00   1620.00
 3      648.00  1296.00   1944.00
 4      777.60  1555.20   2332.80
 5      933.12  1866.24   2799.36
 6     1119.74  2239.49   3359.23
 7     1343.69  2687.39   4031.09
 8     1612.43  3224.86   4837.29
 9     1934.91  3869.81   5804.72
10     2321.89  4643.78   6965.67
11     2786.27  5572.54   8358.81
12     3343.53  6687.05  10030.58
13     4012.24  8024.48  12036.72
14     4814.69  9629.38  14444.07
15     5777.63 11555.26  17332.89



The Cumulative Points Calculation for Levels 1-15
Level   Easy       Medium     Hard
1       450.00     900.00     1350.00
2       990.00     1980.00    2970.00
3       1638.00    3276.00    4914.00
4       2415.60    4831.20    7246.80
5       3348.72    6697.44    10046.16
6       4468.46    8936.93    13305.39
7       5812.15    11624.32   17436.48
8       7424.58    14849.18   22273.77
9       9359.49    18719.00   28078.49
10      11681.38   23362.78   35044.16
11      14467.65   28935.32   43402.97
12      17811.18   35622.37   53433.55
13      21823.42   43646.85   65470.27
14      26638.11   53276.23   79914.34
15      32415.74   64831.49   97347.23
