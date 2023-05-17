import bs4 as bs

import urllib.request

source = urllib.request.urlopen('https://www.espn.com/mlb/stats/player').read()

soup = bs.BeautifulSoup(source, 'lxml')


# get stats headers
headers = soup.find_all("th", class_="Table__TH")

# get header_names list
stat_headers = []
for i in headers:
    j = i.find_all("div")
    for k in j:
        stat_headers.append(k.text)
    j = i.find_all("a")
    for k in j:
        stat_headers.append(k.text)

# get table thingy
table = soup.find_all("tr", class_="Table__TR Table__TR--sm Table__even")

# get player rank name and team from table section 1
player_list = []
playa_stats = []
playas_table = table[0:50]  # 50
for player in playas_table:
    rank = player.find('td', class_="Table__TD").text
    name = player.find('a').text
    team = player.find('span').text
    player_list.append(name)
    playa_stats.append([rank, team])

# get player stats from table section 2
player_s_stats = []
stats = table[50:100]  # 50-100
for stat in stats:
    player_stats = []
    j = stat.find_all("td", class_="Table__TD")
    for k in j:
        player_stats.append(k.text)
    player_s_stats.append(player_stats)

#combine rank and team with other stats
for i in range(len(player_s_stats)):
    for j in playa_stats[i][::-1]:
        player_s_stats[i].insert(0, j)
player_stats = player_s_stats

#replace header Name with Team
stat_headers = [s.replace('Name', 'Team') for s in stat_headers]

print('\n', player_list)
print('\n', player_stats)
print('\n', stat_headers)

import pandas as pd

print('\n\n\n')

df = pd.DataFrame(data=player_stats, columns=stat_headers, index=player_list)
print(df.head(50))