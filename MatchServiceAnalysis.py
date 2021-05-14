# import pymssql
import pandas as pd
import numpy as np
PrimaryData = pd.read_csv('match3.csv')
# conn = pymssql.connect('stupa-testdb.cf0xlnbvxxos.us-east-1.rds.amazonaws.com',
#                        'admin',
#                        'stupa-ai-dev1',
#                        'StupaAiProdDb')
#
# cursor = conn.cursor()
def service_analysis(match_no, main_a, other_b):
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
    DataType = 'TotalPoint'
    MatchCondition = PrimaryData['Match_No'] == match_no
    ServiceByCondition = PrimaryData['SERVICE_BY'] == 'Y'
    player_a_playedCondition = PrimaryData['Played_by'] == main_a
    shotNoCondition = PrimaryData['Shot_no'] == 1
    shotCondition0 = PrimaryData['Shot_no'] == 0
    required = PrimaryData[MatchCondition & ServiceByCondition & player_a_playedCondition & (shotNoCondition | shotCondition0)]
    DataCount = len(required)

    data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
    for i in range(len(columns)):
        MatchAnalysis[columns[i]].append(data[i])


    #Point Won on Service
    DataType = 'PointWon'
    PointShot = []
    for i, row in required.iterrows():
        PointShot.append(str(row['POINT']) + '-' + str(row['Game']))
    PointShot = set(PointShot)

    MatchNoCondition = PrimaryData['Match_No'] == match_no
    wonByCondition = PrimaryData['WON_BY'] == main_a
    winningData = PrimaryData[MatchNoCondition & wonByCondition]

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
    uniquePlacement = required['Placement'].unique()
    # Iterating every placement
    for placement in uniquePlacement:
        DataSubType = placement
        placementRequired = required[required['Placement'] == placement]
        DataCount = len(placementRequired)

        # Adding data to dictionary
        data = [AnalysisType, MatchId, PlayerId, Shot_no, DataType, DataSubType, DataCount]
        for i in range(len(columns)):
            MatchAnalysis[columns[i]].append(data[i])

    # Long and Short
    DataType = 'LongAndShort'
    uniqueShot = list(required['Shot'])
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











