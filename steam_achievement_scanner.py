from requests import get
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup as Soup
from sys import argv, exit as sys_exit
import os
import re
os.system('cls')

#region functions
def map_to_range(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class Achievement():
    def __init__(self, name, desc, img_url, progress='', unlocked=True):
        self.name = name
        self.desc = desc
        self.img_url = img_url
        self.unlocked = unlocked
        self.progress = progress

    def create_progress_bar(self, width=50):
        done, to_do = self.progress.replace(',', '').split(' / ')
        done = int(done)
        to_do = int(to_do)

        str_done = 'x' * int(map_to_range(done, 0, to_do, 0, width))
        str_to_do = ' ' * \
            int(map_to_range(abs(done - to_do), 0, to_do, 0, width))

        return f'|{str_done}{str_to_do}| {self.progress}'

    def get_percentage_done(self):
        if self.unlocked:
            return 1000
        else:
            done, todo = self.progress.replace(',', '').split(' / ')
            return int(map_to_range(int(done), 0, int(todo), 0, 100))

    def __str__(self):
        if self.unlocked:
            return f'Name: {self.name}  |   Description: {self.desc}'
        else:
            return f'Name: {self.name}  |   Description: {self.desc}    {self.create_progress_bar()}'


def get_and_cook_data(url_to_steam_achievements, get_name=False):
    try:
        raw_page = get(
            url_to_steam_achievements).text
    except MissingSchema:
        print('Please enter a valid url')
        sys_exit()
    cooked_page = Soup(raw_page, 'html.parser')

    if not get_name:
        return cooked_page
    else:
        return cooked_page, cooked_page.find('a', 'persona_name_text_content').text.strip()


def format_achievment(string):
    name = string.find('h3', 'ellipsis').text.strip()
    desc = string.find('h5').text.strip()
    img = string.find('img')['src']

    unlocked = True
    if (d := string.find('div', 'achievementProgressBar')) is not None or string.find('div', 'achieveUnlockTime') is None:
        if d is not None:
            progress = d.text.strip()
        else:
            progress = '0 / 1'
        unlocked = False

    if unlocked:
        return Achievement(name, desc, img)
    else:
        return Achievement(name, desc, img, progress=progress, unlocked=unlocked)


def show_usage():
    print(f"""
    Usage:
        -  {os.path.basename(argv[0])} <url_to_profile_achievements> <include_term> [start_html_file]

        - {os.path.basename(argv[0])} https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements expert
        - {os.path.basename(argv[0])} https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements r-[z]
        - {os.path.basename(argv[0])} https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements *
        - {os.path.basename(argv[0])} https://steamcommunity.com/profiles/76561199062978041/stats/CSGO/?tab=achievements all true

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
    """)
    sys_exit()

def generate_achievment_objects(cooked_page):
    achievements = []
    for achievement in cooked_page.find_all('div', 'achieveRow'):
        achievements.append(
            format_achievment(achievement)
        )

    return achievements


def to_html(achievements, search_term, add_name=False):
    txt = """
        <!DOCTYPE html>
        <html>

        <!--https://css-tricks.com/css3-progress-bars/-->
        <style>
            .meter { 
                height: 20px;  /* Can be anything */
                position: relative;
                background: #555;
                -moz-border-radius: 25px;
                -webkit-border-radius: 25px;
                border-radius: 25px;
                padding: 10px;
                box-shadow: inset 0 -1px 1px rgba(255,255,255,0.3);
            }
            .meter > span {
                display: block;
                height: 100%;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                border-top-left-radius: 20px;
                border-bottom-left-radius: 20px;
                background-color: rgb(43,194,83);
                background-image: linear-gradient(
                center bottom,
                rgb(43,194,83) 37%,
                rgb(84,240,84) 69%
                );
                box-shadow: 
                inset 0 2px 9px  rgba(255,255,255,0.3),
                inset 0 -2px 6px rgba(0,0,0,0.4);
                position: relative;
                overflow: hidden;
            }
        </style>

        <body style="background-color:rgb(150, 150, 170);">
    """

    if add_name != False:
        txt += f'<h1 style="text-align:center">{add_name}\'s Achievement Scan Results</h1>'
    else:
        txt += '<h1 style="text-align:center">Achievement Scan Results</h1>'

    found = 0
    colour_flip_flop = True
    for achievement in achievements:
        include_only_unlocked = False
        include_only_locked = False

        if search_term in ['*', 'all']:
            pass
        elif search_term == 'unlocked':
            include_only_unlocked = True
        elif search_term == 'locked':
            include_only_locked = True
        elif search_term[0] == 'r':
            if re.search(search_term.replace('r-', ''), achievement.name) is None:
                continue
        else:
            if search_term.strip().lower() not in achievement.name.strip().lower():
                continue

        if (include_only_unlocked and not achievement.unlocked) or (include_only_locked and achievement.unlocked):
            continue

        if achievement.unlocked:
            add = 50
        else:
            add = 0

        if colour_flip_flop:
            c = f'rgb({150 + add}, {150 + add}, 150)'
        else:
            c = f'rgb({100 + add}, {100 + add}, 100)'
        colour_flip_flop = not colour_flip_flop

        loading_bar = ''
        if not achievement.unlocked:
            done, to_do = achievement.progress.replace(',', '').split(' / ')
            done = int(map_to_range(int(done), 0, int(to_do), 0, 100))

            loading_bar = f"""
            {achievement.progress}
            <div class="meter">
                <span style="width: {done}%"></span>
            </div>
            """

        html = f"""
        <div style="background-color:{c};border-style:solid;text-align:center;width:50%;margin:auto">
            <img src="{achievement.img_url}" style="padding:5px">
            <h3>{achievement.name}</h3>
            <p>{achievement.desc}</p>
            {loading_bar}
            <br>
        </div>
        """

        txt += html + '</body>\n</html>'
        found += 1

    if found == 0:
        print('No matches found :(')
    else:
        print(f'Found {found} matches')

    with open('index.html', 'w') as file:
        file.write(txt)
#endregion

#region arguments
if len(argv) < 3:
    show_usage()
elif len(argv) == 3:
    url, search_term = argv[1], argv[2]
    start_file = False
elif len(argv) == 4:
    url, search_term, start_file = argv[1], argv[2], argv[3]

    if start_file.lower().strip() not in ['true', 'false']:
        show_usage()
    else:
        if start_file.lower().strip() == 'true':
            start_file = True
        elif start_file.lower().strip() == 'false':
            start_file = False
else:
    show_usage()
#endregion

cooked_page, name = get_and_cook_data(url, True)
achievements = generate_achievment_objects(cooked_page)

achievements.sort(key=lambda elem: elem.get_percentage_done(), reverse=True)

to_html(achievements, search_term, add_name=name)

if start_file:
    os.startfile('index.html')
