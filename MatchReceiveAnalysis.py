import pandas as pd
import numpy as np
from receive_data_filter import MatchFilter, MatchWon
PrimaryData = pd.read_csv('finalData.csv')
# conn = pymssql.connect('stupa-testdb.cf0xlnbvxxos.us-east-1.rds.amazonaws.com',
#                        'admin',
#                        'stupa-ai-dev1',
#                        'StupaAiProdDb')
#
# cursor = conn.cursor()
# Payas Jain Player ID: 13
# Shubh Goel Player ID: 26
def receive_analysis(match_no, main_player, other_player):
    # Init. Dictionary
    MatchAnalysis = {}
    #Features List
    columns = ['AnalysisType', 'MatchId', 'PlayerId', 'Shot_no', 'DataType', 'DataSubType', 'DataCount']
    # Init. Features List
    for col in columns:
        MatchAnalysis[col] = []

    AnalysisType = 'Receive'
    # TODO: Change the Match ID to dynamic
    MatchId = 717

    # TODO: Change the player ID to Dynamic
    # Main player ID
    PlayerId = 13
    Shot_no = 2

    #Point Total on Receive
    DataType = 'TotalPoint'
    DataSubType = 'NA'

    shot_2_filter = MatchFilter(PrimaryData, match_no, main_player)
    normal_filter = shot_2_filter.normal()
    DataCount = len(normal_filter)
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Point Won on Receive
    DataType = 'PointWon'
    DataSubType ='NA'

    PointShot = []
    for i, row in normal_filter.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)

    # player_a Win
    normal_win = MatchWon(PrimaryData, match_no, main_player)
    winningData = normal_win.normal()

    WinPoints = []
    for i, row in winningData.iterrows():
        WinPoints.append(str(row['POINT']) + '-' + str(row['Game']))

    WinPoints = set(WinPoints)
    DataCount = len(PointShot & WinPoints)

    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])

    # Placement
    DataType = 'Placement'
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

    right_shot_L = MatchFilter(PrimaryData, match_no, main_player, 'L')
    rightShotFilter = right_shot_L.rshot()
    PointShot = []
    for i, row in rightShotFilter.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)
    DataCount = len(PointShot & WinPoints)  # Total Matching String
    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])







