import bs4 as bs
import urllib.request
import pandas as pd

Batting_dict = {
            "RANK": "https://www.espn.com/mlb/stats/player",
            "AB": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/atBats/dir/desc",
            "R": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/runs/dir/desc",
            "H": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/hits/dir/desc",
            "AVG": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/avg/dir/desc",
            "2B": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/doubles/dir/desc",
            "3B": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/triples/dir/desc",
            "HR": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/homeRuns/dir/desc",
            "RBI": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/rbi/dir/desc",
            "TB": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/totalBases/dir/desc",
            "BB": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/walks/dir/desc",
            "K": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/strikeOuts/dir/desc",
            "SB": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/stolenBases/dir/desc",
            "OBP": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/onBasePct/dir/desc",
            "SLG": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/sluggingPct/dir/desc",
            "OPS": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/onBasePlusSlugging/dir/desc",
            "WAR": "https://www.espn.com/mlb/stats/player/_/table/batting/sort/war/dir/desc"            
            }

Pitching_dict = {
                "RANK": "https://www.espn.com/mlb/stats/player/_/view/pitching" }
literals = {"GS": " /table/pitching/sort/gamesStarted/dir/desc",
                "QS": " /table/pitching/sort/qualityStarts/dir/desc",
                "ERA": " /table/pitching/sort/ERA/dir/asc",
                "W": " /table/pitching/sort/wins/dir/desc",
                "L": " /table/pitching/sort/losses/dir/desc",
                "SV": " /table/pitching/sort/saves/dir/desc",
                "HLD": " /table/pitching/sort/holds/dir/desc",
                "IP": " /table/pitching/sort/innings/dir/desc",
                "H": " /table/pitching/sort/hits/dir/desc",
                "ER": " /table/pitching/sort/earnedRuns/dir/desc",
                "HR": " /table/pitching/sort/homeRuns/dir/desc",
                "BB": " /table/pitching/sort/walks/dir/desc",
                "K": " /table/pitching/sort/strikeOuts/dir/desc",
                "K/9": " /table/pitching/sort/strikeoutsPerNineInnings/dir/desc",
                "WAR": " /table/pitching/sort/WARBR/dir/desc",
                "WHIP": " /table/pitching/sort/WHIP/dir/asc"}

for key, value in literals.items():
    Pitching_dict[key] = Pitching_dict["RANK"] + value

def get_stats_df(url: str):
    source = urllib.request.urlopen(url).read()
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

    return pd.DataFrame(data=player_stats, columns=stat_headers, index=player_list)
    
    
#rank_stats = get_stats_df('https://www.espn.com/mlb/stats/player')

bat_or_pit = []

from tkinter import *
root = Tk()
root.geometry( "200x100" )
def on_select():
  bat_or_pit.append(clicked.get())
  root.quit()
  
options = ['Batting', 'Pitching']
clicked = StringVar()
clicked.set( "Choose a link" )
drop = OptionMenu( root , clicked , *options )
drop.pack()
button = Button( root , text = "Select" , command = on_select).pack()  
root.mainloop()


link_dict = Batting_dict if bat_or_pit[0] == 'Batting' else Pitching_dict

def on_select():
    link = link_dict.get(clicked.get())
    df = get_stats_df(link)
    print(df)
    df.to_csv(f'{bat_or_pit[0]}_{clicked.get()}_stats.xlsx')
    root.quit()
    
options = link_dict.keys()
clicked = StringVar()
clicked.set( "Choose a link" )
drop = OptionMenu( root , clicked , *options )
drop.pack()
button = Button( root , text = "Select" , command = on_select).pack()
root.mainloop()
