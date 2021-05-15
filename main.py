import pandas as pd
# import pymssql
from MatchServiceAnalysis import service_analysis

# conn = pymssql.connect('stupa-testdb.cf0xlnbvxxos.us-east-1.rds.amazonaws.com',
#                        'admin',
#                        'stupa-ai-dev1',
#                        'StupaAiProdDb')
#
# cursor = conn.cursor()

primaryData = pd.read_csv('finalData.csv')  # importing Primary Data
uniqueMatches = primaryData['Match_No'].unique()
tempPrimaryData = []
for match in uniqueMatches:
    matchDict = {}
    uniqueMatchData = primaryData[primaryData['Match_No'] == match]
    matchDict['Match_No'] = uniqueMatchData.iloc[0]['Match_No']
    matchDict['PLAYERA_ID'] = uniqueMatchData.iloc[0]['PLAYERA_ID']
    matchDict['PLAYERB_ID'] = uniqueMatchData.iloc[0]['PLAYERB_ID']
    matchDict['Player_A_Name'] = uniqueMatchData.iloc[0]['Player_A_Name']
    matchDict['Player_B_Name'] = uniqueMatchData.iloc[0]['Player_B_Name']
    matchDict['MatchType'] = uniqueMatchData.iloc[0]['MatchType']
    tempPrimaryData.append(matchDict)


for data in tempPrimaryData:
    service_analysis(data['Match_No'], data['Player_A_Name'], data['Player_B_Name'])


