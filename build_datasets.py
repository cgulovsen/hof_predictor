import urllib
import csv
import pandas as pd
from bs4 import BeautifulSoup


def get_letter_pages():
    base_url = 'https://www.baseball-reference.com/players/'
    urls = []
    letters = ['a/', 'b/', 'c/', 'd/', 'e/', 'f/', 'g/', 'h/', 'i/', 'j/', 'k/', 'l/', 'm/', 'n/',
               'o/', 'p/', 'q/', 'r/', 's/', 't/', 'u/', 'v/', 'w/', 'x/', 'y/', 'z/']
    for letter in letters:
        url = base_url + letter
        urls.append(url)

    return urls


def get_players_url(url):
    with urllib.request.urlopen(url) as player_page:
        soup = BeautifulSoup(player_page, 'html.parser')

    players = []
    links = soup.find('h2').find_next('a')

    while True:
        if '/players/' in links['href']:
            players.append(links['href'])
            # print('Added ', links)
            links = links.find_next('a')
        else:
            return players


def check_player(url):
    if check_position(url) and check_years(url):
        # print('Player: Pass')
        return True
    else:
        # print('Player: Fail')
        return False


def check_position(url):
    with urllib.request.urlopen(url) as player_page:
        soup = BeautifulSoup(player_page, 'lxml')

    try:
        position = soup.find(string='Positions:').find_next(string=True)
    except:
        AttributeError

    try:
        position = soup.find(string='Position:').find_next(string=True)
    except:
        AttributeError

    if 'Pitcher' in position:
        # print('Position: Fail (Pitcher)')
        return False
    else:
        # print('Position: Pass (Position Player)')
        return True


def get_position(url):
    with urllib.request.urlopen(url) as player_page:
        soup = BeautifulSoup(player_page, 'lxml')

    try:
        position = soup.find(string='Positions:').find_next(string=True)
    except:
        AttributeError

    try:
        position = soup.find(string='Position:').find_next(string=True)
    except:
        AttributeError

    position = str(position).strip()
    pos = position.replace(',' , ' ')
    primary_pos = str(pos).split(' ')[0]
    #print('primary pos: ', primary_pos)

    if primary_pos in ('Leftfielder', 'Centerfielder', 'Rightfielder'):
        primary_pos = 'Outfielder'

    return primary_pos


def check_years(url):
    start = pd.read_html(url)
    df = start[0]
    df = df.drop(df.index[len(df) - 1])

    last_year = df['Year'].dropna().astype(int).unique().max()
    total_years = df['Age'].max() - df['Age'].min()

    years = [last_year, total_years]

    if 1980 <= last_year <=2010:
        return years
    else:
        return False


def check_hof(name):
    hof_pd = pd.read_html('https://www.baseball-reference.com/awards/hof.shtml')
    hof_list = hof_pd[0]
    hof_names = hof_list['Name']

    if name in list(hof_names):
        return 1
    else:
        return 0


def get_career_numbers(player_url):
    with urllib.request.urlopen(player_url) as player_page:
        soup = BeautifulSoup(player_page, 'lxml')

    career_numbers = []
    name = soup.find('h1').get_text()
    career_numbers.append(name)

    career1 = soup.find('div', class_='p1')
    group1 = career1.find_all('p')
    for i in enumerate(group1):
        #if len(group1) == 5:
        if len(group1) in (4,5):
            career_numbers.append((float(i[1].get_text())))
        else:
            if i[0] % 2 == 0:
                pass
            else:
                career_numbers.append((float(i[1].get_text())))

    career2 = soup.find('div', class_='p2')
    group2 = career2.find_all('p')
    for i in enumerate(group2):
        if len(group2) == 3:
            career_numbers.append((float(i[1].get_text())))
        else:
            if i[0] % 2 == 0:
                pass
            else:
                career_numbers.append(float(i[1].get_text()))

    career3 = soup.find('div', class_='p3')
    group3 = career3.find_all('p')
    for i in enumerate(group3):
        #if len(group3) == 4:
        if len(group3) in (3,4):
            career_numbers.append((float(i[1].get_text())))
        else:
            if i[0] % 2 == 0:
                pass
            else:
                career_numbers.append((float(i[1].get_text())))

    career_numbers.append(check_hof(name))

    columns = ['Name', 'WAR', 'At Bats', 'Runs', 'Hits', 'Batting Avg', 'HR', 'RBI',
               'SB', 'OBP', 'SLG', 'OPS', 'OPS+','HOF']

    player_dict = dict(zip(columns, career_numbers))

    # return player_dict
    return career_numbers

def build_player_dict(career_nums, position):
    career_numbers = career_nums

    if position == 'Pitcher':
        keys = ['Name', 'WAR', 'W', 'L', 'ERA', 'G', 'GS', 'SV', 'IP', 'K', 'WHIP' ]
        career_nums = career_nums[:-1]
    else:
        keys = ['Name', 'WAR', 'At Bats', 'Runs', 'Hits', 'Batting Avg', 'HR', 'RBI',
               'SB', 'OBP', 'SLG', 'OPS', 'OPS+']

    player_dict = dict(zip(keys, career_numbers))

    return player_dict

def build_dataset_columns():

    position_columns = ['Name', 'WAR', 'At Bats', 'Runs', 'Hits', 'Batting Avg', 'HR', 'RBI',
               'SB', 'OBP', 'SLG', 'OPS', 'OPS+']
    with open('position_players.csv', 'w') as csvfile:
        dataset_writer = csv.writer(csvfile)
        dataset_writer.writerow(position_columns)

    pitcher_columns = ['Name', 'WAR', 'W', 'L', 'ERA', 'G', 'GS', 'SV', 'IP', 'K', 'WHIP' ]
    with open('pitchers.csv', 'w') as csvfile:
        dataset_writer = csv.writer(csvfile)
        dataset_writer.writerow(pitcher_columns)


def add_to_dataset(player_dictionary, position):
    if position == 'Pitcher':
        file = 'pitchers.csv'
    else:
        file = 'position_players.csv'

    with open(file, 'a') as f:
        dataset_writer = csv.writer(f)
        dataset_writer.writerow(player_dictionary.values())



