import pandas as pd
from pandas import DataFrame
import numpy as np
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Ner SportsBook Calculator')
root.geometry("600x1300")

def webScrapeTeamStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'GP', 'W', 'L', 'OTL','Points', 'SF', 'SF/GP', 'SA', 'SA/GP', 'GF', 'GF/GP', 'GA',
                                             'GA/GP', 'OffensiveStrength', 'OffensiveRank', 'DefensiveStrength', 'DefensiveRank'])

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'GF/GP'] = row['GF'] / row['GP']
        df_subset.loc[idx, 'GA/GP'] = row['GA'] / row['GP']
        df_subset.loc[idx, 'SF/GP'] = row['SF'] / row['GP']
        df_subset.loc[idx, 'SA/GP'] = row['SA'] / row['GP']

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'OffensiveStrength'] = row['GF/GP'] / df_subset['GF/GP'].mean()
        df_subset.loc[idx, 'DefensiveStrength'] = row['GA/GP'] / df_subset['GF/GP'].mean()
    
    df_subset['OffensiveRank'] = df_subset['OffensiveStrength'].rank(ascending=False)
    df_subset['DefensiveRank'] = df_subset['DefensiveStrength'].rank()

    df_subset['GF/GP'] = df_subset['GF/GP'].map('{:,.2f}'.format)
    df_subset['GA/GP'] = df_subset['GA/GP'].map('{:,.2f}'.format)
    df_subset['OffensiveStrength'] = df_subset['OffensiveStrength'].map('{:,.2f}'.format)
    df_subset['DefensiveStrength'] = df_subset['DefensiveStrength'].map('{:,.2f}'.format)

    return df_subset

def webScrapeGoalieStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Player', 'Team', 'GP', 'Shots Against', 'Saves', 'Goals Against', 'SV%', 'SV% Rank', 'GAA', 'GAA Rank'])

    df_subset['SV% Rank'] = df_subset['SV%'].rank(ascending=False)
    df_subset['GAA Rank'] = df_subset['GAA'].rank()

    return df_subset

def webScrapePowerPlayStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'GF', 'PP', 'PP Rank'])

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'PP'] = row['GF'] / df_subset['GF'].mean()
    
    df_subset['PP'] = df_subset['PP'].map('{:,.2f}'.format)
    
    df_subset['PP Rank'] = df_subset['PP'].rank(ascending=False)

    return df_subset

def webScrapePenaltyKillStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'GA', 'PK', 'PK Rank'])

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'PK'] = row['GA'] / df_subset['GA'].mean()

    df_subset['PK'] = df_subset['PK'].map('{:,.2f}'.format)
    
    df_subset['PK Rank'] = df_subset['PK'].rank()

    return df_subset

def webScrapeStreakStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'Wins', 'Losses', 'Home Wins', 'Home Losses', 'Road Wins', 'Road Losses'])

    return df_subset


def homeTeamSelected(e):

    global parsedHomeStats
    homeTeam = homeTeamCombo.get()
    homeFilter = homeTeamStats['Team'] == homeTeam
    parsedHomeStats = homeTeamStats[homeFilter]

    global parsedHomePpStats
    homePpFilter = homePowerPlayStats['Team'] == homeTeam
    parsedHomePpStats = homePowerPlayStats[homePpFilter]

    global parsedHomePkStats
    homePkFilter = homePenaltyKillStats['Team'] == homeTeam
    parsedHomePkStats = homePenaltyKillStats[homePkFilter]

    global parsedHomeStreakStats
    homeStreakFilter = homeStreakStats['Team'] == homeTeam
    parsedHomeStreakStats = homeStreakStats[homePkFilter]

def awayTeamSelected(e):

    global parsedAwayStats
    awayTeam = awayTeamCombo.get()
    awayFilter = awayTeamStats['Team'] == awayTeam
    parsedAwayStats = awayTeamStats[awayFilter]

    global parsedAwayPpStats
    awayPpFilter = awayPowerPlayStats['Team'] == awayTeam
    parsedAwayPpStats = awayPowerPlayStats[awayPpFilter]

    global parsedAwayPkStats
    awayPkFilter = awayPenaltyKillStats['Team'] == awayTeam
    parsedAwayPkStats = awayPenaltyKillStats[awayPkFilter]

    global parsedAwayStreakStats
    awayStreakFilter = awayStreakStats['Team'] == awayTeam
    parsedAwayStreakStats = awayStreakStats[awayPkFilter]

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

    #home goalie GP
    gaaLabelHome = Label(goalieStatsFrame, text = "GP")
    gaaLabelHome.grid(row = 0, column = 0, padx = 10, pady = 10)

    #home goalie GAA
    gaaLabelHome = Label(goalieStatsFrame, text = "GAA")
    gaaLabelHome.grid(row = 1, column = 0, padx = 10, pady = 10)

    #home goalie GAA Rank
    gaaRankLabelHome = Label(goalieStatsFrame, text = 'GAA Rank')
    gaaRankLabelHome.grid(row = 2, column = 0, padx = 10, pady = 10)

    #home goalie SV%
    svLabelHome = Label(goalieStatsFrame, text = "SV%")
    svLabelHome.grid(row = 3, column = 0, padx = 10, pady = 10)

    #home goalie SV% Rank
    svRankLabelHome = Label(goalieStatsFrame, text = 'SV% Rank')
    svRankLabelHome.grid(row = 4, column = 0, padx = 10, pady = 10)

def awayGoalieDisplay():

    #away goalie GP
    gaaLabelaway = Label(goalieStatsFrame, text = "GP")
    gaaLabelaway.grid(row = 0, column = 2, padx = 10, pady = 10)

    #away goalie GAA
    gaaLabelaway = Label(goalieStatsFrame, text = "GAA")
    gaaLabelaway.grid(row = 1, column = 2, padx = 10, pady = 10)

    #away goalie GAA Rank
    gaaRankLabelAway = Label(goalieStatsFrame, text = 'GAA Rank')
    gaaRankLabelAway.grid(row = 2, column = 2, padx = 10, pady = 10)

    #away goalie SV%
    svLabelAway = Label(goalieStatsFrame, text = "SV%")
    svLabelAway.grid(row = 3, column = 2, padx = 10, pady = 10)

    #away goalie SV% Rank
    svRankLabelAway = Label(goalieStatsFrame, text = 'SV% Rank')
    svRankLabelAway.grid(row = 4, column = 2, padx = 10, pady = 10)

def homeTeamDisplay():

    #home team wins
    winsLabelhome = Label(teamStatsFrame, text = "Wins")
    winsLabelhome.grid(row = 0, column = 0, padx = 10, pady = 10)

    #home team losses
    lossLabelhome = Label(teamStatsFrame, text = "Losses")
    lossLabelhome.grid(row = 1, column = 0, padx = 10, pady = 10)

    #home team OTL
    otlLabelhome = Label(teamStatsFrame, text = "OTL")
    otlLabelhome.grid(row = 2, column = 0, padx = 10, pady = 10)

    #home team GF/GP
    gfgpLabelhome = Label(teamStatsFrame, text = "GF/GP")
    gfgpLabelhome.grid(row = 3, column = 0, padx = 10, pady = 10)

    #home team GA/GP
    gagpLabelhome = Label(teamStatsFrame, text = "GA/GP")
    gagpLabelhome.grid(row = 4, column = 0, padx = 10, pady = 10)

    #home team offensive strength
    osLabelhome = Label(teamStatsFrame, text = "Offsensive Strength")
    osLabelhome.grid(row = 5, column = 0, padx = 10, pady = 10)

    #home team offensive rank
    orLabelhome = Label(teamStatsFrame, text = "Offsensive Rank")
    orLabelhome.grid(row = 6, column = 0, padx = 10, pady = 10)

    #home team defensive strength
    dsLabelhome = Label(teamStatsFrame, text = "Defensive Strength")
    dsLabelhome.grid(row = 7, column = 0, padx = 10, pady = 10)

    #home team defensive rank
    drLabelhome = Label(teamStatsFrame, text = "Defensive Rank")
    drLabelhome.grid(row = 8, column = 0, padx = 10, pady = 10)

    #home team powerplay strength
    ppsLabelhome = Label(teamStatsFrame, text = "Powerplay Strength")
    ppsLabelhome.grid(row = 9, column = 0, padx = 10, pady = 10)

    #home team powerplay ranking
    pprLabelhome = Label(teamStatsFrame, text = "Powerplay Ranking")
    pprLabelhome.grid(row = 10, column = 0, padx = 10, pady = 10)

    #home team pentaly kill strength
    pksLabelhome = Label(teamStatsFrame, text = "Penalty Kill Strength")
    pksLabelhome.grid(row = 11, column = 0, padx = 10, pady = 10)

    #home team pentaly kill ranking
    pkrLabelhome = Label(teamStatsFrame, text = "Penalty Kill Ranking")
    pkrLabelhome.grid(row = 12, column = 0, padx = 10, pady = 10)

    #home team win streak
    wsLabelhome = Label(teamStatsFrame, text = "Win Streak")
    wsLabelhome.grid(row = 13, column = 0, padx = 10, pady = 10)

    #home team loss streak
    lsLabelhome = Label(teamStatsFrame, text = "Loss Streak")
    lsLabelhome.grid(row = 14, column = 0, padx = 10, pady = 10)

def awayTeamDisplay():

    #away team wins
    winsLabelAway = Label(teamStatsFrame, text = "Wins")
    winsLabelAway.grid(row = 0, column = 3, padx = 10, pady = 10)

    #away team losses
    lossLabelAway = Label(teamStatsFrame, text = "Losses")
    lossLabelAway.grid(row = 1, column = 3, padx = 10, pady = 10)

    #away team OTL
    otlLabelAway = Label(teamStatsFrame, text = "OTL")
    otlLabelAway.grid(row = 2, column = 3, padx = 10, pady = 10)

    #away team GF/GP
    gfgpLabelAway = Label(teamStatsFrame, text = "GF/GP")
    gfgpLabelAway.grid(row = 3, column = 3, padx = 10, pady = 10)

    #away team GA/GP
    gagpLabelAway = Label(teamStatsFrame, text = "GA/GP")
    gagpLabelAway.grid(row = 4, column = 3, padx = 10, pady = 10)

    #away team offensive strength
    osLabelAway = Label(teamStatsFrame, text = "Offsensive Strength")
    osLabelAway.grid(row = 5, column = 3, padx = 10, pady = 10)

    #away team offensive rank
    orLabelAway = Label(teamStatsFrame, text = "Offsensive Rank")
    orLabelAway.grid(row = 6, column = 3, padx = 10, pady = 10)

    #away team defensive strength
    dsLabelAway = Label(teamStatsFrame, text = "Defensive Strength")
    dsLabelAway.grid(row = 7, column = 3, padx = 10, pady = 10)

    #away team defensive rank
    drLabelAway = Label(teamStatsFrame, text = "Defensive Rank")
    drLabelAway.grid(row = 8, column = 3, padx = 10, pady = 10)

    #away team powerplay strength
    ppsLabelAway = Label(teamStatsFrame, text = "Powerplay Strength")
    ppsLabelAway.grid(row = 9, column = 3, padx = 10, pady = 10)

    #away team powerplay ranking
    pprLabelAway = Label(teamStatsFrame, text = "Powerplay Ranking")
    pprLabelAway.grid(row = 10, column = 3, padx = 10, pady = 10)

    #away team pentaly kill strength
    pksLabelAway = Label(teamStatsFrame, text = "Penalty Kill Strength")
    pksLabelAway.grid(row = 11, column = 3, padx = 10, pady = 10)

    #away team pentaly kill ranking
    pkrLabelAway = Label(teamStatsFrame, text = "Penalty Kill Ranking")
    pkrLabelAway.grid(row = 12, column = 3, padx = 10, pady = 10)

    #away team win streak
    wsLabelAway = Label(teamStatsFrame, text = "Win Streak")
    wsLabelAway.grid(row = 13, column = 3, padx = 10, pady = 10)

    #away team loss streak
    lsLabelAway = Label(teamStatsFrame, text = "Loss Streak")
    lsLabelAway.grid(row = 14, column = 3, padx = 10, pady = 10)


def populateHomeGoalieStats():

    homeGp = IntVar()
    homeGaa = IntVar()
    homeGaaRank = IntVar()
    homeSV = IntVar()
    homeSvRank = IntVar()
    homeGp.set(parsedHomeGoalieStats.iloc[0]['GP'])
    homeGaa.set(parsedHomeGoalieStats.iloc[0]['GAA'])
    homeGaaRank.set(parsedHomeGoalieStats.iloc[0]['GAA Rank'])
    homeSV.set(parsedHomeGoalieStats.iloc[0]['SV%'])
    homeSvRank.set(parsedHomeGoalieStats.iloc[0]['SV% Rank'])
    gpHome = Label(goalieStatsFrame, textvariable = homeGp)
    gpHome.grid(row = 0, column = 1, padx = 10, pady = 10)
    gaaHome = Label(goalieStatsFrame, textvariable = homeGaa)
    gaaHome.grid(row = 1, column = 1, padx = 10, pady = 10)
    gaaRankHome = Label(goalieStatsFrame, textvariable = homeGaaRank)
    gaaRankHome.grid(row = 2, column = 1, padx = 10, pady = 10)
    svHome = Label(goalieStatsFrame, textvariable = homeSV)
    svHome.grid(row = 3, column = 1, padx = 10, pady = 10)
    svRankHome = Label(goalieStatsFrame, textvariable = homeSvRank)
    svRankHome.grid(row = 4, column = 1, padx = 10, pady = 10)

def populateAwayGoalieStats():

    awayGp = IntVar()
    awayGaa = IntVar()
    awayGaaRank = IntVar()
    awaySV = IntVar()
    awaySvRank = IntVar()
    awayGp.set(parsedAwayGoalieStats.iloc[0]['GP'])
    awayGaa.set(parsedAwayGoalieStats.iloc[0]['GAA'])
    awayGaaRank.set(parsedAwayGoalieStats.iloc[0]['GAA Rank'])
    awaySV.set(parsedAwayGoalieStats.iloc[0]['SV%'])
    awaySvRank.set(parsedAwayGoalieStats.iloc[0]['SV% Rank'])
    gpAway = Label(goalieStatsFrame, textvariable = awayGp)
    gpAway.grid(row = 0, column = 3, padx = 10, pady = 10)
    gaaAway = Label(goalieStatsFrame, textvariable = awayGaa)
    gaaAway.grid(row = 1, column = 3, padx = 10, pady = 10)
    gaaRankAway = Label(goalieStatsFrame, textvariable = awayGaaRank)
    gaaRankAway.grid(row = 2, column = 3, padx = 10, pady = 10)
    svAway = Label(goalieStatsFrame, textvariable = awaySV)
    svAway.grid(row = 3, column = 3, padx = 10, pady = 10)
    svRankAway = Label(goalieStatsFrame, textvariable = awaySvRank)
    svRankAway.grid(row = 4, column = 3, padx = 10, pady = 10)


def populateHomeTeamStats():

    homeWins = IntVar()
    homeLoss = IntVar()
    homeOTL = IntVar()
    homeGFGP = IntVar()
    homeGAGP = IntVar()
    homeOS = IntVar()
    homeOR = IntVar()
    homeDS = IntVar()
    homeDR = IntVar()
    homePP = IntVar()
    homePPR = IntVar()
    homePK = IntVar()
    homePKR = IntVar()
    homeWins = IntVar()
    homeLosses = IntVar()

    homeWins.set(parsedHomeStats.iloc[0]['W'])
    homeLoss.set(parsedHomeStats.iloc[0]['L'])
    homeOTL.set(parsedHomeStats.iloc[0]['OTL'])
    homeGFGP.set(parsedHomeStats.iloc[0]['GF/GP'])
    homeGAGP.set(parsedHomeStats.iloc[0]['GA/GP'])
    homeOS.set(parsedHomeStats.iloc[0]['OffensiveStrength'])
    homeOR.set(parsedHomeStats.iloc[0]['OffensiveRank'])
    homeDS.set(parsedHomeStats.iloc[0]['DefensiveStrength'])
    homeDR.set(parsedHomeStats.iloc[0]['DefensiveRank'])
    homePP.set(parsedHomePpStats.iloc[0]['PP'])
    homePPR.set(parsedHomePpStats.iloc[0]['PP Rank'])
    homePK.set(parsedHomePkStats.iloc[0]['PK'])
    homePKR.set(parsedHomePkStats.iloc[0]['PK Rank'])
    homeWins.set(parsedHomeStreakStats.iloc[0]['Wins'])
    homeLosses.set(parsedHomeStreakStats.iloc[0]['Losses'])


    winsHome = Label(teamStatsFrame, textvariable = homeWins)
    winsHome.grid(row = 0, column = 1, padx = 10, pady = 10)
    lossesHome = Label(teamStatsFrame, textvariable = homeLoss)
    lossesHome.grid(row = 1, column = 1, padx = 10, pady = 10)
    otlHome = Label(teamStatsFrame, textvariable = homeOTL)
    otlHome.grid(row = 2, column = 1, padx = 10, pady = 10)
    gfgpHome = Label(teamStatsFrame, textvariable = homeGFGP)
    gfgpHome.grid(row = 3, column = 1, padx = 10, pady = 10)
    gagpHome = Label(teamStatsFrame, textvariable = homeGAGP)
    gagpHome.grid(row = 4, column = 1, padx = 10, pady = 10)
    osHome = Label(teamStatsFrame, textvariable = homeOS)
    osHome.grid(row = 5, column = 1, padx = 10, pady = 10)
    orHome = Label(teamStatsFrame, textvariable = homeOR)
    orHome.grid(row = 6, column = 1, padx = 10, pady = 10)
    dsHome = Label(teamStatsFrame, textvariable = homeDS)
    dsHome.grid(row = 7, column = 1, padx = 10, pady = 10)
    drHome = Label(teamStatsFrame, textvariable = homeDR)
    drHome.grid(row = 8, column = 1, padx = 10, pady = 10)
    PpHome = Label(teamStatsFrame, textvariable = homePP)
    PpHome.grid(row = 9, column = 1, padx = 10, pady = 10)
    PprHome = Label(teamStatsFrame, textvariable = homePPR)
    PprHome.grid(row = 10, column = 1, padx = 10, pady = 10)
    PkHome = Label(teamStatsFrame, textvariable = homePK)
    PkHome.grid(row = 11, column = 1, padx = 10, pady = 10)
    PkrHome = Label(teamStatsFrame, textvariable = homePKR)
    PkrHome.grid(row = 12, column = 1, padx = 10, pady = 10)
    winsHome = Label(teamStatsFrame, textvariable = homeWins)
    winsHome.grid(row = 13, column = 1, padx = 10, pady = 10)
    lossHome = Label(teamStatsFrame, textvariable = homeLosses)
    lossHome.grid(row = 14, column = 1, padx = 10, pady = 10)

def populateAwayTeamStats():

    awayWins = IntVar()
    awayLoss = IntVar()
    awayOTL = IntVar()
    awayGFGP = IntVar()
    awayGAGP = IntVar()
    awayOS = IntVar()
    awayOR = IntVar()
    awayDS = IntVar()
    awayDR = IntVar()
    awayPP = IntVar()
    awayPPR = IntVar()
    awayPK = IntVar()
    awayPKR = IntVar()
    awayWins = IntVar()
    awayLosses = IntVar()

    awayWins.set(parsedAwayStats.iloc[0]['W'])
    awayLoss.set(parsedAwayStats.iloc[0]['L'])
    awayOTL.set(parsedAwayStats.iloc[0]['OTL'])
    awayGFGP.set(parsedAwayStats.iloc[0]['GF/GP'])
    awayGAGP.set(parsedAwayStats.iloc[0]['GA/GP'])
    awayOS.set(parsedAwayStats.iloc[0]['OffensiveStrength'])
    awayOR.set(parsedAwayStats.iloc[0]['OffensiveRank'])
    awayDS.set(parsedAwayStats.iloc[0]['DefensiveStrength'])
    awayDR.set(parsedAwayStats.iloc[0]['DefensiveRank'])
    awayPP.set(parsedAwayPpStats.iloc[0]['PP'])
    awayPPR.set(parsedAwayPpStats.iloc[0]['PP Rank'])
    awayPK.set(parsedAwayPkStats.iloc[0]['PK'])
    awayPKR.set(parsedAwayPkStats.iloc[0]['PK Rank'])
    awayWins.set(parsedAwayStreakStats.iloc[0]['Wins'])
    awayLosses.set(parsedAwayStreakStats.iloc[0]['Losses'])

    winsAway = Label(teamStatsFrame, textvariable = awayWins)
    winsAway.grid(row = 0, column = 4, padx = 10, pady = 10)
    lossesAway = Label(teamStatsFrame, textvariable = awayLoss)
    lossesAway.grid(row = 1, column = 4, padx = 10, pady = 10)
    otlAway = Label(teamStatsFrame, textvariable = awayOTL)
    otlAway.grid(row = 2, column = 4, padx = 10, pady = 10)
    gfgpAway = Label(teamStatsFrame, textvariable = awayGFGP)
    gfgpAway.grid(row = 3, column = 4, padx = 10, pady = 10)
    gagpAway = Label(teamStatsFrame, textvariable = awayGAGP)
    gagpAway.grid(row = 4, column = 4, padx = 10, pady = 10)
    osAway = Label(teamStatsFrame, textvariable = awayOS)
    osAway.grid(row = 5, column = 4, padx = 10, pady = 10)
    orAway = Label(teamStatsFrame, textvariable = awayOR)
    orAway.grid(row = 6, column = 4, padx = 10, pady = 10)
    dsAway = Label(teamStatsFrame, textvariable = awayDS)
    dsAway.grid(row = 7, column = 4, padx = 10, pady = 10)
    drAway = Label(teamStatsFrame, textvariable = awayDR)
    drAway.grid(row = 8, column = 4, padx = 10, pady = 10)
    PpAway = Label(teamStatsFrame, textvariable = awayPP)
    PpAway.grid(row = 9, column = 4, padx = 10, pady = 10)
    PprAway = Label(teamStatsFrame, textvariable = awayPPR)
    PprAway.grid(row = 10, column = 4, padx = 10, pady = 10)
    PkAway = Label(teamStatsFrame, textvariable = awayPK)
    PkAway.grid(row = 11, column = 4, padx = 10, pady = 10)
    PkrAway = Label(teamStatsFrame, textvariable = awayPKR)
    PkrAway.grid(row = 12, column = 4, padx = 10, pady = 10)
    winsAway = Label(teamStatsFrame, textvariable = awayWins)
    winsAway.grid(row = 13, column = 4, padx = 10, pady = 10)
    lossAway = Label(teamStatsFrame, textvariable = awayLosses)
    lossAway.grid(row = 14, column = 4, padx = 10, pady = 10)
    
def calculateStatistics():

    #home goalie stats
    #home goalie / 2.5 since the number of goalies is significantly higher than number of teams
    numOfHomeGoalies = len(homeGoalieStats)
    homeGoalieGaaCalc = (((numOfHomeGoalies - parsedHomeGoalieStats.iloc[0]['GAA Rank']) * 0.10) / 2.5)
    homeGoalieSvCalc = (((numOfHomeGoalies - parsedHomeGoalieStats.iloc[0]['SV% Rank']) * 0.10) / 2.5)

    #home strength calcs
    numOfHomeTeams = len(homeTeamStats)
    homeOffensiveStrengthCalc = ((numOfHomeTeams - parsedHomeStats.iloc[0]['OffensiveRank']) * 0.30)
    homeDefensiveStrengthCalc = ((numOfHomeTeams - parsedHomeStats.iloc[0]['DefensiveRank']) * 0.20)
    homePowerPlayStrengthCalc = ((numOfHomeTeams - parsedHomePpStats.iloc[0]['PP Rank']) * 0.15)
    homePentalyKillStrengthCalc = ((numOfHomeTeams - parsedAwayPkStats.iloc[0]['PK Rank']) * 0.15)

    #away goalie stats
    #away goalie / 2.5 since the number of goalies is significantly higher than number of teams
    numAwayGoalies = len(awayGoalieStats)
    awayGoalieGaaCalc = (((numAwayGoalies - parsedAwayGoalieStats.iloc[0]['GAA Rank']) * 0.10) / 2.5)
    awayGoalieSvCalc = (((numAwayGoalies - parsedAwayGoalieStats.iloc[0]['SV% Rank']) * 0.10) / 2.5)

    #away offensive strength
    numOfAwayTeams = len(awayTeamStats)
    awayOffensiveStrengthCalc = ((numOfAwayTeams - parsedAwayStats.iloc[0]['OffensiveRank']) * 0.30)
    awayDefensiveStrengthCalc = ((numOfAwayTeams - parsedAwayStats.iloc[0]['DefensiveRank']) * 0.20)
    awayPowerPlayStrengthCalc = ((numOfAwayTeams - parsedAwayPpStats.iloc[0]['PP Rank']) * 0.15)
    awayPentalyKillStrengthCalc = ((numOfAwayTeams - parsedAwayPkStats.iloc[0]['PK Rank']) * 0.15)

    #calculate totals
    homeTotalCount = homeGoalieGaaCalc + homeGoalieSvCalc + homeOffensiveStrengthCalc + homeDefensiveStrengthCalc + homePowerPlayStrengthCalc + homePentalyKillStrengthCalc

    awayTotalCount = awayGoalieGaaCalc + awayGoalieSvCalc + awayOffensiveStrengthCalc + awayDefensiveStrengthCalc + awayPowerPlayStrengthCalc + awayPentalyKillStrengthCalc

    totalCount = homeTotalCount + awayTotalCount

    homePercentage = ((homeTotalCount / totalCount) * 100)
    awayPercentage = ((awayTotalCount / totalCount) * 100)

    #display calculations
    finalHomePercentage = StringVar()
    finalHomePercentage.set("{:.2f}".format(homePercentage) + " %")
    homeTeam = Label(totalCalcFrame, text = parsedHomeStats.iloc[0]['Team'])
    homeTeam.grid(row = 0, column = 0, padx = 10, pady = 10)
    homePercentageLabel = Label(totalCalcFrame, textvariable = finalHomePercentage)
    homePercentageLabel.grid(row = 1, column = 0, padx = 10, pady = 10)

    finalAwayPercentage = StringVar()
    finalAwayPercentage.set("{:.2f}".format(awayPercentage) + " %")
    awayTeam = Label(totalCalcFrame, text = parsedAwayStats.iloc[0]['Team'])
    awayTeam.grid(row = 0, column = 1, padx = 10, pady = 10)
    awayPercentageLabel = Label(totalCalcFrame, textvariable = finalAwayPercentage)
    awayPercentageLabel.grid(row = 1, column = 1, padx = 10, pady = 10)


def computeStats():

    populateHomeGoalieStats()
    populateAwayGoalieStats()
    populateHomeTeamStats()
    populateAwayTeamStats()
    calculateStatistics()


#web scrape links
homeTeamStatsUrl = 'https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
awayTeamStatsUrl = 'https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
homeGoalieStatsUrl = 'https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=H&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
awayGoalieStatsUrl = 'https://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20192020&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=A&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
homePowerPlayStatsUrl = 'https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=pp&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
awayPowerPlayStatsUrl = 'https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=pp&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
homePenaltyKillStatsUrl = 'https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=pk&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
awayPenaltyKillStatsUrl = 'https://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20192020&stype=2&sit=pk&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
streakStatsUrl = 'https://www.naturalstattrick.com/teamstreaks.php'


#web scrape to get dataframe tables in Pandas
homeTeamStats = webScrapeTeamStatsUrl(homeTeamStatsUrl)
awayTeamStats = webScrapeTeamStatsUrl(awayTeamStatsUrl)
homeGoalieStats = webScrapeGoalieStatsUrl(homeGoalieStatsUrl)
awayGoalieStats = webScrapeGoalieStatsUrl(awayGoalieStatsUrl)
homePowerPlayStats = webScrapePowerPlayStatsUrl(homePowerPlayStatsUrl)
awayPowerPlayStats = webScrapePowerPlayStatsUrl(awayPowerPlayStatsUrl)
homePenaltyKillStats = webScrapePenaltyKillStatsUrl(homePenaltyKillStatsUrl)
awayPenaltyKillStats = webScrapePenaltyKillStatsUrl(awayPenaltyKillStatsUrl)
homeStreakStats = webScrapeStreakStatsUrl(streakStatsUrl)
awayStreakStats = webScrapeStreakStatsUrl(streakStatsUrl)


#create user input frames
selectionFrame = LabelFrame(root, padx = 10, pady = 10)
selectionFrame.pack(padx = 5, pady = 5)

#goalie statistics frame
goalieStatsFrame = LabelFrame(root, padx = 10, pady = 10)
goalieStatsFrame.pack(padx = 5, pady = 5)

#team statistics frame
teamStatsFrame = LabelFrame(root, padx = 10, pady = 10)
teamStatsFrame.pack(padx = 5, pady = 5)

#calculation frame
totalCalcFrame = LabelFrame(root, padx = 10, pady = 10)
totalCalcFrame.pack(padx = 5, pady = 5)


homeGoalieDisplay()
awayGoalieDisplay()
homeTeamDisplay()
awayTeamDisplay()


#home team selection label
homeTeamLabel = ttk.Label(selectionFrame, text = 'Select Home Team')
homeTeamLabel.grid(row = 0, column = 0, padx = 5, pady = 10)

#home team combobox
homeTeamValues = list(homeTeamStats['Team'].unique())
homeTeamCombo = ttk.Combobox(selectionFrame, value = homeTeamValues)
homeTeamCombo.grid(row = 1, column = 0)
homeTeamCombo.bind("<<ComboboxSelected>>", homeTeamSelected)

awayTeamLabel = ttk.Label(selectionFrame, text = 'Select Away Team')
awayTeamLabel.grid(row = 0, column = 1, padx = 5, pady = 10)

awayTeamValues = list(awayTeamStats['Team'].unique())
awayTeamCombo = ttk.Combobox(selectionFrame, value = awayTeamValues)
awayTeamCombo.grid(row = 1, column = 1)
awayTeamCombo.bind("<<ComboboxSelected>>", awayTeamSelected)


#home goalie selection label
homeGoalieLabel = ttk.Label(selectionFrame, text = 'Select Home Goalie')
homeGoalieLabel.grid(row = 2, column = 0, padx = 5, pady = 10)

#home goalie combobox
homeGoalieValues = list(homeGoalieStats['Player'].unique())
homeGoalieCombo = ttk.Combobox(selectionFrame, value = homeGoalieValues)
homeGoalieCombo.grid(row = 3, column = 0)
homeGoalieCombo.bind("<<ComboboxSelected>>", homeGoalieSelected)


#away goalie selection label
awayGoalieLabel = ttk.Label(selectionFrame, text = 'Select Away Goalie')
awayGoalieLabel.grid(row = 2, column = 1, padx = 5, pady = 10)

#away goalie combobox
awayGoalieValues = list(awayGoalieStats['Player'].unique())
awayGoalieCombo = ttk.Combobox(selectionFrame, value = awayGoalieValues)
awayGoalieCombo.grid(row = 3, column = 1)
awayGoalieCombo.bind("<<ComboboxSelected>>", awayGoalieSelected)


button = ttk.Button(root, text = 'Run', command=lambda : computeStats())
button.pack()

#GUI mainloop
root.mainloop()