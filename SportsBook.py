import pandas as pd
from pandas import DataFrame
import numpy as np
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Ner SportsBook Calculator')
root.geometry("400x400")


def webScrapeGoalieStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Player', 'Team', 'GP', 'Shots Against', 'Saves', 'Goals Against', 'SV%', 'SV% Rank', 'GAA', 'GAA Rank'])

    df_subset['SV% Rank'] = df_subset['SV%'].rank(ascending=False)
    df_subset['GAA Rank'] = df_subset['GAA'].rank()

    return df_subset


def homeGoalieSelected(e):

    global parsedHomeGoalieStats
    homeGoalie = homeGoalieCombo.get()
    homeFilter = homeGoalieStats['Player'] == homeGoalie
    parsedHomeGoalieStats = homeGoalieStats[homeFilter]

def awayGoalieSelected(e):

    global parsedAwayGoalieStats
    awayGoalie = awayGoalieCombo.get()
    awayFilter = awayGoalieStats['Player'] == awayGoalie
    parsedAwayGoalieStats = awayGoalieStats[awayFilter]


def homeGoalieDisplay():

    #home goalie GAA
    gaaLabelHome = Label(goalieStatsFrame, text = "GAA")
    gaaLabelHome.grid(row = 0, column = 0, padx = 10, pady = 10)

    #home goalie GAA Rank
    gaaRankLabelHome = Label(goalieStatsFrame, text = 'GAA Rank')
    gaaRankLabelHome.grid(row = 1, column = 0, padx = 10, pady = 10)

    #home goalie SV%
    svLabelHome = Label(goalieStatsFrame, text = "SV%")
    svLabelHome.grid(row = 2, column = 0, padx = 10, pady = 10)

    #home goalie SV% Rank
    svRankLabelHome = Label(goalieStatsFrame, text = 'SV% Rank')
    svRankLabelHome.grid(row = 3, column = 0, padx = 10, pady = 10)

def awayGoalieDisplay():

    #away goalie GAA
    gaaLabelaway = Label(goalieStatsFrame, text = "GAA")
    gaaLabelaway.grid(row = 0, column = 2, padx = 10, pady = 10)

    #away goalie GAA Rank
    gaaRankLabelAway = Label(goalieStatsFrame, text = 'GAA Rank')
    gaaRankLabelAway.grid(row = 1, column = 2, padx = 10, pady = 10)

    #away goalie SV%
    svLabelAway = Label(goalieStatsFrame, text = "SV%")
    svLabelAway.grid(row = 2, column = 2, padx = 10, pady = 10)

    #away goalie SV% Rank
    svRankLabelAway = Label(goalieStatsFrame, text = 'SV% Rank')
    svRankLabelAway.grid(row = 3, column = 2, padx = 10, pady = 10)


def populateHomeGoalieStats():

    homeGaa = IntVar()
    homeGaaRank = IntVar()
    homeSV = IntVar()
    homeSvRank = IntVar()
    homeGaa.set(parsedHomeGoalieStats.iloc[0]['GAA'])
    homeGaaRank.set(parsedHomeGoalieStats.iloc[0]['GAA Rank'])
    homeSV.set(parsedHomeGoalieStats.iloc[0]['SV%'])
    homeSvRank.set(parsedHomeGoalieStats.iloc[0]['SV% Rank'])
    gaaHome = Label(goalieStatsFrame, textvariable = homeGaa)
    gaaHome.grid(row = 0, column = 1, padx = 10, pady = 10)
    gaaRankHome = Label(goalieStatsFrame, textvariable = homeGaaRank)
    gaaRankHome.grid(row = 1, column = 1, padx = 10, pady = 10)
    svHome = Label(goalieStatsFrame, textvariable = homeSV)
    svHome.grid(row = 2, column = 1, padx = 10, pady = 10)
    svRankHome = Label(goalieStatsFrame, textvariable = homeSvRank)
    svRankHome.grid(row = 3, column = 1, padx = 10, pady = 10)

def populateAwayGoalieStats():

    awayGaa = IntVar()
    awayGaaRank = IntVar()
    awaySV = IntVar()
    awaySvRank = IntVar()
    awayGaa.set(parsedAwayGoalieStats.iloc[0]['GAA'])
    awayGaaRank.set(parsedAwayGoalieStats.iloc[0]['GAA Rank'])
    awaySV.set(parsedAwayGoalieStats.iloc[0]['SV%'])
    awaySvRank.set(parsedAwayGoalieStats.iloc[0]['SV% Rank'])
    gaaAway = Label(goalieStatsFrame, textvariable = awayGaa)
    gaaAway.grid(row = 0, column = 3, padx = 10, pady = 10)
    gaaRankAway = Label(goalieStatsFrame, textvariable = awayGaaRank)
    gaaRankAway.grid(row = 1, column = 3, padx = 10, pady = 10)
    svAway = Label(goalieStatsFrame, textvariable = awaySV)
    svAway.grid(row = 2, column = 3, padx = 10, pady = 10)
    svRankAway = Label(goalieStatsFrame, textvariable = awaySvRank)
    svRankAway.grid(row = 3, column = 3, padx = 10, pady = 10)



def computeStats():

    populateHomeGoalieStats()
    populateAwayGoalieStats()
    


#web scrape links
homeGoalieStatsUrl = 'https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=H&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
awayGoalieStatsUrl = 'https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=A&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'

#web scrape to get dataframe tables in Pandas
homeGoalieStats = webScrapeGoalieStatsUrl(homeGoalieStatsUrl)
awayGoalieStats = webScrapeGoalieStatsUrl(awayGoalieStatsUrl)


#create user input frames
selectionFrame = LabelFrame(root, padx = 10, pady = 10)
selectionFrame.pack(padx = 5, pady = 5)

#goalie statistics frame
goalieStatsFrame = LabelFrame(root, padx = 10, pady = 10)
goalieStatsFrame.pack(padx = 5, pady = 5)

homeGoalieDisplay()
awayGoalieDisplay()


#home goalie selection label
homeGoalieLabel = ttk.Label(selectionFrame, text = 'Select Home Goalie')
homeGoalieLabel.grid(row = 2, column = 0, padx = 5, pady = 10)

#home goalie combobox
homeGoalieValues = list(homeGoalieStats['Player'].unique())
homeGoalieCombo = ttk.Combobox(selectionFrame, value = homeGoalieValues)
homeGoalieCombo.current(0)
homeGoalieCombo.grid(row = 3, column = 0)
homeGoalieCombo.bind("<<ComboboxSelected>>", homeGoalieSelected)


#away goalie selection label
awayGoalieLabel = ttk.Label(selectionFrame, text = 'Select Away Goalie')
awayGoalieLabel.grid(row = 2, column = 1, padx = 5, pady = 10)

#away goalie combobox
awayGoalieValues = list(awayGoalieStats['Player'].unique())
awayGoalieCombo = ttk.Combobox(selectionFrame, value = awayGoalieValues)
awayGoalieCombo.current(0)
awayGoalieCombo.grid(row = 3, column = 1)
awayGoalieCombo.bind("<<ComboboxSelected>>", awayGoalieSelected)




button = ttk.Button(root, text = 'Run', command=lambda : computeStats())
button.pack()

#GUI mainloop
root.mainloop()