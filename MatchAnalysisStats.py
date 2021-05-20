import pandas as pd
import math
PrimaryData = pd.read_csv('finalData.csv')
def analysis_stats(match_no, player_no, player_type, player_name):
    # Forehand Winner Rate
    # Total Forward and Win Conditions (Common)
    ShotCondition = PrimaryData['Shot'].str[:2] == 'FH'
    playedByCondition = PrimaryData['Played_by'] == player_name
    matchCondition = PrimaryData['Match_No'] == match_no

    # Total Forward Specific Condition
    ShotnoCondition = PrimaryData['Shot_no'] > 0

    TotalForwards = len(PrimaryData[ShotCondition & ShotnoCondition & playedByCondition & matchCondition])

    # Win Specific Conditions
    ReverseRowID_Condition = PrimaryData['Reverse_Row_ID'] == 2

    TotalForwardsWins = len(PrimaryData[ShotCondition & ReverseRowID_Condition & playedByCondition & matchCondition])

    # TODO: Add in the dataframe
    ForeHandWinnerRate = None
    if(TotalForwards == None or TotalForwards <= 0):
        ForeHandWinnerRate = 0
    else:
        ForeHandWinnerRate = math.ceil((TotalForwardsWins / TotalForwards) * 100)

    #Backhand Winner Rate

    # Total Forward and Win Conditions (Common)
    ShotCondition = PrimaryData['Shot'].str[:2] == 'BH'
    playedByCondition = PrimaryData['Played_by'] == player_name
    matchCondition = PrimaryData['Match_No'] == match_no

    # Total Forward Specific Condition
    ShotnoCondition = PrimaryData['Shot_no'] > 0

    TotalBackhands = len(PrimaryData[ShotCondition & ShotnoCondition & playedByCondition & matchCondition])

    # Win Specific Conditions
    ReverseRowID_Condition = PrimaryData['Reverse_Row_ID'] == 2

    TotalBackhandWins = len(PrimaryData[ShotCondition & ReverseRowID_Condition & playedByCondition & matchCondition])

    # TODO: Add in the dataframe
    BackhandWinnerRate = None
    if (TotalForwards == None or TotalForwards <= 0):
        BackhandWinnerRate = 0
    else:
        BackhandWinnerRate = math.ceil((TotalBackhandWins / TotalBackhands) * 100)




