import pandas as pd
from pandas import DataFrame
import numpy as np
from tkinter import *
from tkinter import ttk
import statistics
import cmath

root = Tk()
root.title('NHL Prediction Calculator')
root.iconbitmap('/Users/jimbo/Documents/Sportsbook/exe/Skating.icns')
root.geometry("600x1000")

def webScrapeTeamStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'GP', 'W', 'L', 'OTL','Points', 'SF', 'SF/GP', 'SA', 'SA/GP', 'GF', 'GF/GP', 'GF/GP_Rank',
                                             'xGF', 'xGF_Rank', 'xGA', 'xGA_Rank', 'GA', 'GA/GP', 'GA/GP_Rank', 'CompareGF', 'OffensiveRank',
                                             'CompareGA', 'DefensiveRank', 'SCF', 'SCGF', 'SCO', 'SCO_Rank', 'SCA', 'SCGA', 'SCD', 'SCD_Rank'])

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'GF/GP'] = row['GF'] / row['GP']
        df_subset.loc[idx, 'GA/GP'] = row['GA'] / row['GP']
        df_subset.loc[idx, 'SF/GP'] = row['SF'] / row['GP']
        df_subset.loc[idx, 'SA/GP'] = row['SA'] / row['GP']

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'CompareGF'] = row['GF/GP'] / df_subset['GF/GP'].mean()
        df_subset.loc[idx, 'CompareGA'] = row['GA/GP'] / df_subset['GF/GP'].mean()
        df_subset.loc[idx, 'SCO'] = (row['SCGF'] / row['SCF']) * 100
        df_subset.loc[idx, 'SCD'] = (row['SCGA'] / row['SCA']) * 100
    
    df_subset['GF/GP_Rank'] = df_subset['CompareGF'].rank(ascending=False)
    df_subset['GA/GP_Rank'] = df_subset['CompareGA'].rank()

    df_subset['xGF_Rank'] = df_subset['xGF'].rank(ascending=False)
    df_subset['xGA_Rank'] = df_subset['xGA'].rank()

    df_subset['SCO_Rank'] = df_subset['SCO'].rank(ascending=False)
    df_subset['SCD_Rank'] = df_subset['SCD'].rank()

    for idx, row in df_subset.iterrows():
        df_subset['OffensiveRank'] = ((df_subset['xGF_Rank'] + df_subset['GF/GP_Rank'] + df_subset['SCO_Rank']) / 3)
        df_subset['DefensiveRank'] = ((df_subset['xGA_Rank'] + df_subset['GA/GP_Rank'] + df_subset['SCD_Rank']) / 3)

    df_subset['GF/GP'] = df_subset['GF/GP'].map('{:,.2f}'.format)
    df_subset['GA/GP'] = df_subset['GA/GP'].map('{:,.2f}'.format)

    df_subset['OffensiveRank'] = df_subset['OffensiveRank'].map('{:,.0f}'.format)
    df_subset['DefensiveRank'] = df_subset['DefensiveRank'].map('{:,.0f}'.format)

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
        df_subset = DataFrame(df, columns = ['Team', 'GF', 'PP', 'GF_Rank', 'PP_Rank', 'xGF', 'xGF_Rank', 'SCF', 'SCGF', 'SCO', 'SCO_Rank'])

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'PP'] = row['GF'] / df_subset['GF'].mean()
        df_subset.loc[idx, 'SCO'] = (row['SCGF'] / row['SCF']) * 100
    
    df_subset['PP'] = df_subset['PP'].map('{:,.2f}'.format)
    
    df_subset['GF_Rank'] = df_subset['PP'].rank(ascending=False)
    df_subset['xGF_Rank'] = df_subset['xGF'].rank(ascending=False)
    df_subset['SCO_Rank'] = df_subset['SCO'].rank(ascending=False)

    for idx, row in df_subset.iterrows():
        df_subset['PP_Rank'] = ((df_subset['GF_Rank'] + df_subset['xGF_Rank'] + df_subset['SCO_Rank']) / 3)
    
    df_subset['PP_Rank'] = df_subset['PP_Rank'].map('{:,.0f}'.format)

    return df_subset

def webScrapePenaltyKillStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'GA', 'PK', 'GA_Rank', 'PK_Rank', 'xGA', 'xGA_Rank', 'SCA', 'SCGA', 'SCD', 'SCA_Rank'])

    for idx, row in df_subset.iterrows():
        df_subset.loc[idx, 'PK'] = row['GA'] / df_subset['GA'].mean()
        df_subset.loc[idx, 'SCD'] = (row['SCGA'] / row['SCA']) * 100

    df_subset['PK'] = df_subset['PK'].map('{:,.2f}'.format)
    
    df_subset['GA_Rank'] = df_subset['PK'].rank()
    df_subset['xGA_Rank'] = df_subset['xGA'].rank()
    df_subset['SCA_Rank'] = df_subset['SCD'].rank()

    for idx, row in df_subset.iterrows():
        df_subset['PK_Rank'] = ((df_subset['GA_Rank'] + df_subset['xGA_Rank'] + df_subset['SCA_Rank']) / 3)
    
    df_subset['PK_Rank'] = df_subset['PK_Rank'].map('{:,.0f}'.format)

    return df_subset

def webScrapeStreakStatsUrl(StatUrl):

    dfs = pd.read_html(StatUrl)

    for df in dfs:
        df_subset = DataFrame(df, columns = ['Team', 'Wins', 'Losses', 'Home Wins', 'Home Losses', 'Road Wins', 'Road Losses'])

    return df_subset


def homeTeamSelected(homeTeam):

    global parsedHomeStats
    #homeTeam = homeTeamCombo.get()
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
    parsedHomeStreakStats = homeStreakStats[homeStreakFilter]

def awayTeamSelected(awayTeam):

    global parsedAwayStats
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
    parsedAwayStreakStats = awayStreakStats[awayStreakFilter]

def homeGoalieSelected(homeGoalie):

    global parsedHomeGoalieStats
    homeFilter = homeGoalieStats['Player'] == homeGoalie
    parsedHomeGoalieStats = homeGoalieStats[homeFilter]

def awayGoalieSelected(awayGoalie):

    global parsedAwayGoalieStats
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

    # #home team offensive strength
    # osLabelhome = Label(teamStatsFrame, text = "Offsensive Strength")
    # osLabelhome.grid(row = 5, column = 0, padx = 10, pady = 10)

    #home team offensive rank
    orLabelhome = Label(teamStatsFrame, text = "Offsensive Rank")
    orLabelhome.grid(row = 5, column = 0, padx = 10, pady = 10)

    # #home team defensive strength
    # dsLabelhome = Label(teamStatsFrame, text = "Defensive Strength")
    # dsLabelhome.grid(row = 7, column = 0, padx = 10, pady = 10)

    #home team defensive rank
    drLabelhome = Label(teamStatsFrame, text = "Defensive Rank")
    drLabelhome.grid(row = 6, column = 0, padx = 10, pady = 10)

    # #home team powerplay strength
    # ppsLabelhome = Label(teamStatsFrame, text = "Powerplay Strength")
    # ppsLabelhome.grid(row = 9, column = 0, padx = 10, pady = 10)

    #home team powerplay ranking
    pprLabelhome = Label(teamStatsFrame, text = "Powerplay Ranking")
    pprLabelhome.grid(row = 7, column = 0, padx = 10, pady = 10)

    # #home team pentaly kill strength
    # pksLabelhome = Label(teamStatsFrame, text = "Penalty Kill Strength")
    # pksLabelhome.grid(row = 11, column = 0, padx = 10, pady = 10)

    #home team pentaly kill ranking
    pkrLabelhome = Label(teamStatsFrame, text = "Penalty Kill Ranking")
    pkrLabelhome.grid(row = 8, column = 0, padx = 10, pady = 10)

    #home team win streak
    wsLabelhome = Label(teamStatsFrame, text = "Win Streak")
    wsLabelhome.grid(row = 9, column = 0, padx = 10, pady = 10)

    #home team loss streak
    lsLabelhome = Label(teamStatsFrame, text = "Loss Streak")
    lsLabelhome.grid(row = 10, column = 0, padx = 10, pady = 10)

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

    # #away team offensive strength
    # osLabelAway = Label(teamStatsFrame, text = "Offsensive Strength")
    # osLabelAway.grid(row = 5, column = 3, padx = 10, pady = 10)

    #away team offensive rank
    orLabelAway = Label(teamStatsFrame, text = "Offsensive Rank")
    orLabelAway.grid(row = 5, column = 3, padx = 10, pady = 10)

    # #away team defensive strength
    # dsLabelAway = Label(teamStatsFrame, text = "Defensive Strength")
    # dsLabelAway.grid(row = 7, column = 3, padx = 10, pady = 10)

    #away team defensive rank
    drLabelAway = Label(teamStatsFrame, text = "Defensive Rank")
    drLabelAway.grid(row = 6, column = 3, padx = 10, pady = 10)

    # #away team powerplay strength
    # ppsLabelAway = Label(teamStatsFrame, text = "Powerplay Strength")
    # ppsLabelAway.grid(row = 9, column = 3, padx = 10, pady = 10)

    #away team powerplay ranking
    pprLabelAway = Label(teamStatsFrame, text = "Powerplay Ranking")
    pprLabelAway.grid(row = 7, column = 3, padx = 10, pady = 10)

    # #away team pentaly kill strength
    # pksLabelAway = Label(teamStatsFrame, text = "Penalty Kill Strength")
    # pksLabelAway.grid(row = 11, column = 3, padx = 10, pady = 10)

    #away team pentaly kill ranking
    pkrLabelAway = Label(teamStatsFrame, text = "Penalty Kill Ranking")
    pkrLabelAway.grid(row = 8, column = 3, padx = 10, pady = 10)

    #away team win streak
    wsLabelAway = Label(teamStatsFrame, text = "Win Streak")
    wsLabelAway.grid(row = 9, column = 3, padx = 10, pady = 10)

    #away team loss streak
    lsLabelAway = Label(teamStatsFrame, text = "Loss Streak")
    lsLabelAway.grid(row = 10, column = 3, padx = 10, pady = 10)


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
    homeStreakWins = IntVar()
    homeStreakLosses = IntVar()

    homeWins.set(parsedHomeStats.iloc[0]['W'])
    homeLoss.set(parsedHomeStats.iloc[0]['L'])
    homeOTL.set(parsedHomeStats.iloc[0]['OTL'])
    homeGFGP.set(parsedHomeStats.iloc[0]['GF/GP'])
    homeGAGP.set(parsedHomeStats.iloc[0]['GA/GP'])
    homeOR.set(parsedHomeStats.iloc[0]['OffensiveRank'])
    homeDR.set(parsedHomeStats.iloc[0]['DefensiveRank'])
    homePPR.set(parsedHomePpStats.iloc[0]['PP_Rank'])
    homePKR.set(parsedHomePkStats.iloc[0]['PK_Rank'])
    homeStreakWins.set(parsedHomeStreakStats.iloc[0]['Wins'])
    homeStreakLosses.set(parsedHomeStreakStats.iloc[0]['Losses'])


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
    orHome = Label(teamStatsFrame, textvariable = homeOR)
    orHome.grid(row = 5, column = 1, padx = 10, pady = 10)
    drHome = Label(teamStatsFrame, textvariable = homeDR)
    drHome.grid(row = 6, column = 1, padx = 10, pady = 10)
    PprHome = Label(teamStatsFrame, textvariable = homePPR)
    PprHome.grid(row = 7, column = 1, padx = 10, pady = 10)
    PkrHome = Label(teamStatsFrame, textvariable = homePKR)
    PkrHome.grid(row = 8, column = 1, padx = 10, pady = 10)
    winsStreakHome = Label(teamStatsFrame, textvariable = homeStreakWins)
    winsStreakHome.grid(row = 9, column = 1, padx = 10, pady = 10)
    lossStreakHome = Label(teamStatsFrame, textvariable = homeStreakLosses)
    lossStreakHome.grid(row = 10, column = 1, padx = 10, pady = 10)

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
    awayStreakWins = IntVar()
    awayStreakLosses = IntVar()

    awayWins.set(parsedAwayStats.iloc[0]['W'])
    awayLoss.set(parsedAwayStats.iloc[0]['L'])
    awayOTL.set(parsedAwayStats.iloc[0]['OTL'])
    awayGFGP.set(parsedAwayStats.iloc[0]['GF/GP'])
    awayGAGP.set(parsedAwayStats.iloc[0]['GA/GP'])
    awayOR.set(parsedAwayStats.iloc[0]['OffensiveRank'])
    awayDR.set(parsedAwayStats.iloc[0]['DefensiveRank'])
    awayPPR.set(parsedAwayPpStats.iloc[0]['PP_Rank'])
    awayPKR.set(parsedAwayPkStats.iloc[0]['PK_Rank'])
    awayStreakWins.set(parsedAwayStreakStats.iloc[0]['Wins'])
    awayStreakLosses.set(parsedAwayStreakStats.iloc[0]['Losses'])

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
    orAway = Label(teamStatsFrame, textvariable = awayOR)
    orAway.grid(row = 5, column = 4, padx = 10, pady = 10)
    drAway = Label(teamStatsFrame, textvariable = awayDR)
    drAway.grid(row = 6, column = 4, padx = 10, pady = 10)
    PprAway = Label(teamStatsFrame, textvariable = awayPPR)
    PprAway.grid(row = 7, column = 4, padx = 10, pady = 10)
    PkrAway = Label(teamStatsFrame, textvariable = awayPKR)
    PkrAway.grid(row = 8, column = 4, padx = 10, pady = 10)
    winsStreakAway = Label(teamStatsFrame, textvariable = awayStreakWins)
    winsStreakAway.grid(row = 9, column = 4, padx = 10, pady = 10)
    lossStreakAway = Label(teamStatsFrame, textvariable = awayStreakLosses)
    lossStreakAway.grid(row = 10, column = 4, padx = 10, pady = 10)
    
def calculateStatistics():

    #home goalie stats
    #home goalie / 2.5 since the number of goalies is significantly higher than number of teams
    numOfHomeGoalies = len(homeGoalieStats)
    homeGoalieGaaCalc = (((numOfHomeGoalies - parsedHomeGoalieStats.iloc[0]['GAA Rank']) * 0.10) / 2.5)
    homeGoalieSvCalc = (((numOfHomeGoalies - parsedHomeGoalieStats.iloc[0]['SV% Rank']) * 0.10) / 2.5)

    #home strength calcs
    numOfHomeTeams = len(homeTeamStats)
    homeOffensiveStrengthCalc = ((numOfHomeTeams - int(parsedHomeStats.iloc[0]['OffensiveRank'])) * 0.30)
    homeDefensiveStrengthCalc = ((numOfHomeTeams - int(parsedHomeStats.iloc[0]['DefensiveRank'])) * 0.20)
    homePowerPlayStrengthCalc = ((numOfHomeTeams - int(parsedHomePpStats.iloc[0]['PP_Rank'])) * 0.15)
    homePentalyKillStrengthCalc = ((numOfHomeTeams - int(parsedAwayPkStats.iloc[0]['PK_Rank'])) * 0.15)

    #away goalie stats
    #away goalie / 2.5 since the number of goalies is significantly higher than number of teams
    numAwayGoalies = len(awayGoalieStats)
    awayGoalieGaaCalc = (((numAwayGoalies - parsedAwayGoalieStats.iloc[0]['GAA Rank']) * 0.10) / 2.5)
    awayGoalieSvCalc = (((numAwayGoalies - parsedAwayGoalieStats.iloc[0]['SV% Rank']) * 0.10) / 2.5)

    #away offensive strength
    numOfAwayTeams = len(awayTeamStats)
    awayOffensiveStrengthCalc = ((numOfAwayTeams - int(parsedAwayStats.iloc[0]['OffensiveRank'])) * 0.30)
    awayDefensiveStrengthCalc = ((numOfAwayTeams - int(parsedAwayStats.iloc[0]['DefensiveRank'])) * 0.20)
    awayPowerPlayStrengthCalc = ((numOfAwayTeams - int(parsedAwayPpStats.iloc[0]['PP_Rank'])) * 0.15)
    awayPentalyKillStrengthCalc = ((numOfAwayTeams - int(parsedAwayPkStats.iloc[0]['PK_Rank'])) * 0.15)

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

def calculateGoalsScored():

    homeOffensiveAdjust = 0
    awayOffensiveAdjust = 0

    if int(parsedHomeStats.iloc[0]['OffensiveRank']) <= 7:
        homeOffensiveAdjust = 1.0
    elif int(parsedHomeStats.iloc[0]['OffensiveRank']) <= 15 and int(parsedHomeStats.iloc[0]['OffensiveRank']) > 7:
        homeOffensiveAdjust = 0.5

    if int(parsedHomeStats.iloc[0]['OffensiveRank']) <= 7:
        awayOffensiveAdjust = 1.0
    elif int(parsedHomeStats.iloc[0]['OffensiveRank']) <= 15 and int(parsedHomeStats.iloc[0]['OffensiveRank']) > 7:
        awayOffensiveAdjust = 0.5

    #calculate score method one
    homeMethodOne = (statistics.mean([float(parsedHomeStats.iloc[0]['GF/GP']), float(parsedAwayStats.iloc[0]['GA/GP'])]) + homeOffensiveAdjust)
    awayMethodOne = (statistics.mean([float(parsedAwayStats.iloc[0]['GF/GP']), float(parsedHomeStats.iloc[0]['GA/GP'])]) + awayOffensiveAdjust)

    #calculate score method two
    homeExpectedShots =  statistics.mean([float(parsedHomeStats.iloc[0]['SF/GP']), float(parsedAwayStats.iloc[0]['SA/GP'])])
    awayExpectedShots =  statistics.mean([float(parsedAwayStats.iloc[0]['SF/GP']), float(parsedHomeStats.iloc[0]['SA/GP'])])
    homeMethodTwo = (((1.0 - float(parsedAwayGoalieStats.iloc[0]['SV%'])) * homeExpectedShots) + homeOffensiveAdjust)
    awayMethodTwo = (((1.0 - float(parsedHomeGoalieStats.iloc[0]['SV%'])) * awayExpectedShots) + awayOffensiveAdjust)

    #calculate score method three
    homeAvgShotsPerGoal = (float(parsedHomeStats.iloc[0]['SF/GP']) / float(parsedHomeStats.iloc[0]['GF/GP']))
    awayAvgShotsPerGoal = (float(parsedAwayStats.iloc[0]['SF/GP']) / float(parsedAwayStats.iloc[0]['GF/GP']))
    homeMethodThree = ((homeExpectedShots / homeAvgShotsPerGoal) + homeOffensiveAdjust)
    awayMethodThree = ((awayExpectedShots / awayAvgShotsPerGoal) + awayOffensiveAdjust)

    #method four
    homeMethodfour = (float(parsedAwayStats.iloc[0]['GA/GP']) + homeOffensiveAdjust)
    awayMethodFour = (float(parsedHomeStats.iloc[0]['GA/GP']) + awayOffensiveAdjust)

    #method five
    homeMethodFive = (float(parsedHomeStats.iloc[0]['GF/GP']) + homeOffensiveAdjust)
    awayMethodFive = (float(parsedAwayStats.iloc[0]['GF/GP']) + awayOffensiveAdjust)

    homeAverage = statistics.mean([homeMethodOne, homeMethodTwo, homeMethodThree, homeMethodfour, homeMethodFive])
    awayAverage = statistics.mean([awayMethodOne, awayMethodTwo, awayMethodThree, awayMethodFour, awayMethodFive])

    homeScore = homeAverage
    awayScore = awayAverage

    if int(parsedAwayStats.iloc[0]['DefensiveRank']) < (len(awayTeamStats) / 2):

        homeScore = ((1 - (((len(awayTeamStats) / 2) - int(parsedAwayStats.iloc[0]['DefensiveRank'])) / 100)) * homeAverage)

    elif int(parsedAwayStats.iloc[0]['DefensiveRank']) > (len(awayTeamStats) / 2):

        homeScore = ((1 + ((int(parsedAwayStats.iloc[0]['DefensiveRank']) - (len(awayTeamStats) / 2)) / 100)) * homeAverage)


    if int(parsedAwayStats.iloc[0]['DefensiveRank']) < (len(awayTeamStats) / 2):

        awayScore = ((1 - (((len(homeTeamStats) / 2) - int(parsedAwayStats.iloc[0]['DefensiveRank'])) / 100)) * awayAverage)

    elif int(parsedAwayStats.iloc[0]['DefensiveRank']) > (len(awayTeamStats) / 2):

        awayScore = ((1 + ((int(parsedAwayStats.iloc[0]['DefensiveRank']) - (len(homeTeamStats) / 2)) / 100)) * awayAverage)
    

    #display final calculated goals
    finalHomeGoals = StringVar()
    finalHomeGoals.set("Goals: ""{:.2f}".format(homeScore))
    homeGoalsLabel = Label(totalCalcFrame, textvariable = finalHomeGoals)
    homeGoalsLabel.grid(row = 2, column = 0, padx = 10, pady = 10)

    finalAwayGoals = StringVar()
    finalAwayGoals.set("Goals: ""{:.2f}".format(awayScore))
    homeGoalsLabel = Label(totalCalcFrame, textvariable = finalAwayGoals)
    homeGoalsLabel.grid(row = 2, column = 1, padx = 10, pady = 10)


def computeStats():

    populateHomeGoalieStats()
    populateAwayGoalieStats()
    populateHomeTeamStats()
    populateAwayTeamStats()
    calculateStatistics()
    calculateGoalsScored()

def updateHomeListBox(homeTeamValues):

    homeTeamList.delete(0, END)

    for item in homeTeamValues:
        homeTeamList.insert(END, item)

def fillOutHomeTeamList(e):

    homeTeamSearchBox.delete(0, END)
    homeTeamSearchBox.insert(0, homeTeamList.get(ANCHOR))
    homeTeamSelected(homeTeamList.get(ANCHOR))

def checkHomeTeam(e):

    typed = homeTeamSearchBox.get()
    data = homeTeamValues

    if typed == "":
        data = homeTeamValues
    else:
        data = []
        for item in homeTeamValues:
            if typed.lower() in item.lower():
                data.append(item)
    updateHomeListBox(data)

def updateAwayListBox(awayTeamValues):

    awayTeamList.delete(0, END)

    for item in awayTeamValues:
        awayTeamList.insert(END, item)

def fillOutAwayTeamList(e):

    awayTeamSearchBox.delete(0, END)
    awayTeamSearchBox.insert(0, awayTeamList.get(ANCHOR))
    awayTeamSelected(awayTeamList.get(ANCHOR))

def checkAwayTeam(e):

    typed = awayTeamSearchBox.get()
    data = awayTeamValues

    if typed == "":
        data = awayTeamValues
    else:
        data = []
        for item in awayTeamValues:
            if typed.lower() in item.lower():
                data.append(item)
    updateAwayListBox(data)

def updateHomeGoalieListBox(homeGoalieValues):

    homeGoalieList.delete(0, END)

    for item in homeGoalieValues:
        homeGoalieList.insert(END, item)

def fillOutHomeGoalieList(e):

    homeGoalieSearchBox.delete(0, END)
    homeGoalieSearchBox.insert(0, homeGoalieList.get(ANCHOR))
    homeGoalieSelected(homeGoalieList.get(ANCHOR))

def checkHomeGoalie(e):

    typed = homeGoalieSearchBox.get()
    data = homeGoalieValues

    if typed == "":
        data = homeGoalieValues
    else:
        data = []
        for item in homeGoalieValues:
            if typed.lower() in item.lower():
                data.append(item)
    updateHomeGoalieListBox(data)

def updateAwayGoalieListBox(awayGoalieValues):

    awayGoalieList.delete(0, END)

    for item in awayGoalieValues:
        awayGoalieList.insert(END, item)

def fillOutAwayGoalieList(e):

    awayGoalieSearchBox.delete(0, END)
    awayGoalieSearchBox.insert(0, awayGoalieList.get(ANCHOR))
    awayGoalieSelected(awayGoalieList.get(ANCHOR))

def checkAwayGoalie(e):

    typed = awayGoalieSearchBox.get()
    data = awayGoalieValues

    if typed == "":
        data = awayGoalieValues
    else:
        data = []
        for item in awayGoalieValues:
            if typed.lower() in item.lower():
                data.append(item)
    updateAwayGoalieListBox(data)


#web scrape links
# homeTeamStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20202021&thruseason=20202021&stype=2&sit=5v5&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
# awayTeamStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20202021&thruseason=20202021&stype=2&sit=5v5&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
# homeGoalieStatsUrl = 'http://www.naturalstattrick.com/playerteams.php?fromseason=20202021&thruseason=20202021&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=H&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
# awayGoalieStatsUrl = 'http://www.naturalstattrick.com/playerteams.php?fromseason=20202021&thruseason=20202021&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=A&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
# homePowerPlayStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20202021&thruseason=20202021&stype=2&sit=pp&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
# awayPowerPlayStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20202021&thruseason=20202021&stype=2&sit=pp&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
# homePenaltyKillStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20202021&thruseason=20202021&stype=2&sit=pk&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
# awayPenaltyKillStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20202021&thruseason=20202021&stype=2&sit=pk&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='

homeTeamStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20202021&stype=2&sit=5v5&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
awayTeamStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20202021&stype=2&sit=5v5&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
homeGoalieStatsUrl = 'http://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20202021&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=H&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
awayGoalieStatsUrl = 'http://www.naturalstattrick.com/playerteams.php?fromseason=20192020&thruseason=20202021&stype=2&sit=5v5&score=all&stdoi=g&rate=n&team=ALL&pos=S&loc=A&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=single&draftteam=ALL'
homePowerPlayStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20202021&stype=2&sit=pp&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
awayPowerPlayStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20202021&stype=2&sit=pp&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
homePenaltyKillStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20202021&stype=2&sit=pk&score=all&rate=n&team=all&loc=H&gpf=410&fd=&td='
awayPenaltyKillStatsUrl = 'http://www.naturalstattrick.com/teamtable.php?fromseason=20192020&thruseason=20202021&stype=2&sit=pk&score=all&rate=n&team=all&loc=A&gpf=410&fd=&td='
streakStatsUrl = 'http://www.naturalstattrick.com/teamstreaks.php'


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

mainFrame = LabelFrame(root)
mainFrame.pack(fill = BOTH, expand = 1)

myCanvas = Canvas(mainFrame)
myCanvas.pack(side = LEFT, fill = BOTH, expand = 1)

yscrollbar = ttk.Scrollbar(mainFrame, orient = VERTICAL, command = myCanvas.yview)
yscrollbar.pack(side = RIGHT, fill = Y)

myCanvas.configure(yscrollcommand = yscrollbar.set)
myCanvas.bind('<Configure>', lambda e: myCanvas.configure(scrollregion = myCanvas.bbox('all')))

myFrame = Frame(myCanvas)
myCanvas.create_window((0,0), window = myFrame, anchor = "nw")



#create user input frames
selectionFrame = LabelFrame(myFrame, padx = 10, pady = 10)
selectionFrame.pack(padx = 75, pady = 5)

#goalie statistics frame
goalieStatsFrame = LabelFrame(myFrame, padx = 10, pady = 10)
goalieStatsFrame.pack(padx = 75, pady = 5)

#team statistics frame
teamStatsFrame = LabelFrame(myFrame, padx = 10, pady = 10)
teamStatsFrame.pack(padx = 75, pady = 5)

#calculation frame
totalCalcFrame = LabelFrame(myFrame, padx = 10, pady = 10, width = 250, height = 150)
totalCalcFrame.pack(padx = 75, pady = 5)


homeGoalieDisplay()
awayGoalieDisplay()
homeTeamDisplay()
awayTeamDisplay()


#home team selection label
homeTeamLabel = ttk.Label(selectionFrame, text = 'Select Home Team')
homeTeamLabel.grid(row = 0, column = 0, padx = 5, pady = 10)

#home team searchbox
homeTeamValues = list(homeTeamStats['Team'].unique())
homeTeamSearchBox = Entry(selectionFrame, text = "Search")
homeTeamSearchBox.grid(row = 1, column = 0)
homeTeamList = Listbox(selectionFrame)
homeTeamList.grid(row = 2, column = 0)
updateHomeListBox(homeTeamValues)
homeTeamList.bind("<<ListboxSelect>>", fillOutHomeTeamList)
homeTeamSearchBox.bind("<KeyRelease>", checkHomeTeam)

#away team selection label
awayTeamLabel = ttk.Label(selectionFrame, text = 'Select Away Team')
awayTeamLabel.grid(row = 0, column = 1, padx = 5, pady = 10)

#away team searchbox
awayTeamValues = list(awayTeamStats['Team'].unique())
awayTeamSearchBox = Entry(selectionFrame)
awayTeamSearchBox.grid(row = 1, column = 1)
awayTeamList = Listbox(selectionFrame)
awayTeamList.grid(row = 2, column = 1)
updateAwayListBox(awayTeamValues)
awayTeamList.bind("<<ListboxSelect>>", fillOutAwayTeamList)
awayTeamSearchBox.bind("<KeyRelease>", checkAwayTeam)


#home goalie selection label
homeGoalieLabel = ttk.Label(selectionFrame, text = 'Select Home Goalie')
homeGoalieLabel.grid(row = 3, column = 0, padx = 5, pady = 10)

#home goalie combobox
homeGoalieValues = list(homeGoalieStats['Player'].unique())
homeGoalieSearchBox = Entry(selectionFrame)
homeGoalieSearchBox.grid(row = 4, column = 0)
homeGoalieList = Listbox(selectionFrame)
homeGoalieList.grid(row = 5, column = 0)
updateHomeGoalieListBox(homeGoalieValues)
homeGoalieList.bind("<<ListboxSelect>>", fillOutHomeGoalieList)
homeGoalieSearchBox.bind("<KeyRelease>", checkHomeGoalie)


#away goalie selection label
awayGoalieLabel = ttk.Label(selectionFrame, text = 'Select Away Goalie')
awayGoalieLabel.grid(row = 3, column = 1, padx = 5, pady = 10)

#away goalie combobox
awayGoalieValues = list(awayGoalieStats['Player'].unique())
awayGoalieSearchBox = Entry(selectionFrame)
awayGoalieSearchBox.grid(row = 4, column = 1)
awayGoalieList = Listbox(selectionFrame)
awayGoalieList.grid(row = 5, column = 1)
updateAwayGoalieListBox(awayGoalieValues)
awayGoalieList.bind("<<ListboxSelect>>", fillOutAwayGoalieList)
awayGoalieSearchBox.bind("<KeyRelease>", checkAwayGoalie)
# awayGoalieCombo = ttk.Combobox(selectionFrame, value = awayGoalieValues)
# awayGoalieCombo.grid(row = 4, column = 1)
# awayGoalieCombo.bind("<<ComboboxSelected>>", awayGoalieSelected)


button = ttk.Button(myFrame, text = 'Run', command=lambda : computeStats())
button.pack(pady = 10)


#GUI mainloop
root.mainloop()