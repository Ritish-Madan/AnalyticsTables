# import pymssql
import pandas as pd
import numpy as np
from data_filter import MatchFilter, MatchWon
PrimaryData = pd.read_csv('finalData.csv')
# conn = pymssql.connect('stupa-testdb.cf0xlnbvxxos.us-east-1.rds.amazonaws.com',
#                        'admin',
#                        'stupa-ai-dev1',
#                        'StupaAiProdDb')
#
# cursor = conn.cursor()

def service_analysis(match_no, main_player, other_player):
    # TODO: Remove these comments
    #Payas Jain Player ID: 13
    # Shubh Goel Player ID: 26

    # Initializing Columns/Keys to dictionary
    MatchAnalysis = {}
    columns = ['AnalysisType', 'MatchId', 'PlayerId', 'Shot_no', 'DataType', 'DataSubType', 'DataCount']
    for col in columns:
        MatchAnalysis[col] = []

    # Point Total on Service
    # TODO: Change MatchId global variable from main
    MatchId = 717
    # TODO: Access the PlayerID from the player_a_details in main.py of loop
    # Same variables for main_a
    PlayerId = 13
    AnalysisType = 'Service'
    Shot_no = '0,1'


    DataSubType = 'NA'
    point = 'TotalPoint'
    DataType = point
    player_a_norm = MatchFilter(PrimaryData, match_no, main_player)
    normal_filter = player_a_norm.normal()
    DataCount = len(normal_filter)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])


    #Point Won on Service
    DataType = 'PointWon'
    PointShot = []
    for i, row in normal_filter.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)

    # player_a Win
    pl_a_win = MatchWon(PrimaryData, match_no, main_player)
    winningData = pl_a_win.normal()

    WinPoints = []
    for i, row in winningData.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))

    WinPoints = set(WinPoints)
    DataCount = len(PointShot & WinPoints)

    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Placement

    DataType = "Placement"
    uniquePlacement = normal_filter['Placement'].unique()
    # Iterating every placement
    for placement in uniquePlacement:
        DataSubType = placement
        placementRequired = normal_filter[normal_filter['Placement'] == placement]
        DataCount = len(placementRequired)

        # Adding data to dictionary
        data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
        for i in range(len(columns)):
            MatchAnalysis[columns[i]].append(data[i])

    # Long and Short
    DataType = 'LongAndShort'
    uniqueShot = list(normal_filter['Shot'])
    for i in range(len(uniqueShot)):
        uniqueShot[i] = uniqueShot[i][-1]
    uniqueShot = np.array(uniqueShot)
    unique, counts = np.unique(uniqueShot, return_counts=True)
    for i in range(len(unique)):
        DataSubType = unique[i]
        DataCount = counts[i]
        data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
        for i in range(len(columns)):
            MatchAnalysis[columns[i]].append(data[i])
    # Won Long
    DataType = 'WonLong'
    DataSubType = 'NA'

    rshot = MatchFilter(PrimaryData, match_no, main_player, 'L')
    rightShotFilter = rshot.rshot()
    PointShot = []
    for i, row in rightShotFilter.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)
    DataCount = len(PointShot & WinPoints) # Total Matching String
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Total WonLong
    DataType = 'TotalWonLong'
    bothwin = MatchWon(PrimaryData, match_no, main_player, other_player)
    bothWinFilter = bothwin.bothWin()
    WinPoints = []
    for i, row in bothWinFilter.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)

    RShot_S = MatchFilter(PrimaryData, match_no, main_player, 'S')
    rShot_S = RShot_S.rshot()
    PointShot = []
    for i, row in rShot_S.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)

    DataCount = len(PointShot & WinPoints)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Backhand
    DataType = 'Backhand'

    leftWin = MatchWon(PrimaryData, match_no, main_player, None, 'BH')
    left_win_BH = leftWin.leftShot()
    WinPoints = []
    for i, row in left_win_BH.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)

    # Primary Data filter
    PointShot = []
    for i, row in normal_filter.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)

    DataCount = len(PointShot & WinPoints)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Total Backhand
    DataType = 'TotalBackhand'
    both_Win_BH = MatchWon(PrimaryData, match_no, main_player, other_player, 'BH')
    bothWinLeft_BH = both_Win_BH.bothWinLeft()
    WinPoints = []
    for i, row in bothWinLeft_BH.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)
    DataCount = len(WinPoints & PointShot)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Forehand
    DataType = 'Forehand'
    leftWinFH = MatchWon(PrimaryData, match_no, main_player, None, 'FH')
    left_win_FH = leftWinFH.leftShot()
    WinPoints = []
    for i, row in left_win_FH.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)
    DataCount = len(WinPoints & PointShot)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    #Total Forehand

    DataType ='TotalForehand'
    both_Win_FH = MatchWon(PrimaryData, match_no, main_player, other_player, 'FH')
    bothWinLeft_FH = both_Win_FH.bothWinLeft()
    WinPoints = []
    for i, row in bothWinLeft_FH.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)
    DataCount = len(WinPoints & PointShot)

    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Other

    DataType = 'Other'
    otherWin_LH_BH = MatchWon(PrimaryData, match_no, main_player, None, 'FH', 'BH')
    other_LH_BH = otherWin_LH_BH.leftOtherShot()
    WinPoints = []
    for i, row in other_LH_BH.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)
    DataCount = len(PointShot & WinPoints)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Total Other
    DataType = 'TotalOther'
    # Won By Condition filtering
    MatchNoCondition = PrimaryData['Match_No'] == match_no
    wonBy_A_Condition = PrimaryData['WON_BY'] == main_player
    wonBy_B_Condition = PrimaryData['WON_BY'] == other_player
    shotLeftCondition = PrimaryData['Shot'].str[:2] != 'FH'
    shotLeftCondition2 = PrimaryData['Shot'].str[:2] != 'BH'
    winningData = PrimaryData[shotLeftCondition2 & shotLeftCondition & MatchNoCondition & (wonBy_A_Condition | wonBy_B_Condition)]
    WinPoints = []
    for i, row in winningData.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))
    WinPoints = set(WinPoints)
    DataCount = len(WinPoints & PointShot)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])
    return MatchAnalysis


