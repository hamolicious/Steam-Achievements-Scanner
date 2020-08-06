# Steam-Achievements-Scanner
A scanner that will let you narrow down your achievements by letting you search through them using a number of tools (including regex) written in Python 3

If you're using the python version then the requirements are
**Requirements:**
1. requests>=2.24.0

The executable version does not require anything other than the binary itself however I did find it to be very slow.

<pre>
    Usage:
        -  steam_achievement_scanner.py <url_to_profile_achievements> <include_term> [start_html_file]

        - steam_achievement_scanner.py https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements expert
        - steam_achievement_scanner.py https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements r-[z]
        - steam_achievement_scanner.py https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements *
        - steam_achievement_scanner.py https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements all true

    url_to_profile:
        The link that takes you to the achievements section of a game for a user
        example: https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements

    include_term:
        The term to search by

        'all' or '*' - includes any achievement
        'unlocked' - includes only unlocked achievements
        'locked' - includes only locked achievements
        'r-<REGEX_HERE>' - includes only achievements that matched the specified REGEX
        '' - any other string will only include achievements that contain that string (not case sensetive)

    start_html_file:
        Optional argument, either true or false, chooses if to start the generated HTML file of not

Created by Hamolicious, thanks for using my tool!

C:\Users\Hamolicious\Documents\Programing_Projects\Python\WIP\Steam Achievements Tracker>
</pre>

Running this command...
<img src="https://github.com/hamolicious/Steam-Achievements-Scanner/blob/master/Screenshots/command.PNG?raw=true">

...will generate an "index.html" file that upon opening (in this case automatically since the start_html_file tag has been set to true) will dipsplay a sorted list (from closest to getting to farthest) of achievements that contain the word "expert"
<img src="https://github.com/hamolicious/Steam-Achievements-Scanner/blob/master/Screenshots/index.PNG?raw=true">


