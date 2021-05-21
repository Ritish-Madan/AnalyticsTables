import numpy as np
import pandas as pd
import math
PrimaryData = pd.read_csv('finalData.csv')


def analysis_stats(match_no, player_no, player_type, player_name):
    # Forehand Winner Rate
    # Total Forward and Win Conditions (Common)
    ForehandShotCondition = PrimaryData['Shot'].str[:2] == 'FH'
    playedByCondition = PrimaryData['Played_by'] == player_name
    matchCondition = PrimaryData['Match_No'] == match_no

    # Total Forward Specific Condition
    ShotnoCondition = PrimaryData['Shot_no'] > 0

    TotalForwards = len(PrimaryData[ForehandShotCondition & ShotnoCondition & playedByCondition & matchCondition])

    # Win Specific Conditions
    ReverseRowID_Condition = PrimaryData['Reverse_Row_ID'] == 2

    TotalForwardsWins = len(PrimaryData[ForehandShotCondition & ReverseRowID_Condition & playedByCondition & matchCondition])

    # TODO: Add in the dataframe
    ForeHandWinnerRate = None
    if TotalForwards is None or TotalForwards <= 0:
        ForeHandWinnerRate = 0
    else:
        ForeHandWinnerRate = math.ceil((TotalForwardsWins / TotalForwards) * 100)

    #Backhand Winner Rate
    # Total Backhand and Win Conditions (Common)
    BackhandShotCondition = PrimaryData['Shot'].str[:2] == 'BH'

    # Total Backhand Specific Condition
    ShotnoCondition = PrimaryData['Shot_no'] > 0

    TotalBackhands = len(PrimaryData[BackhandShotCondition & ShotnoCondition & playedByCondition & matchCondition])

    # Win Specific Conditions
    ReverseRowID_Condition = PrimaryData['Reverse_Row_ID'] == 2

    TotalBackhandWins = len(PrimaryData[BackhandShotCondition & ReverseRowID_Condition & playedByCondition & matchCondition])

    # TODO: Add in the dataframe
    BackhandWinnerRate = None
    if TotalBackhands is None or TotalBackhands <= 0:
        BackhandWinnerRate = 0
    else:
        BackhandWinnerRate = math.ceil((TotalBackhandWins / TotalBackhands) * 100)

    # Forehand Error Rate

    # Total Forehand Errors Condition
    notNullErrorType = PrimaryData['ErrorType'].notnull()
    TotalForehandErrors = len(PrimaryData[ForehandShotCondition & notNullErrorType & playedByCondition & matchCondition])

    # "TotalForwards" taken from Forehand Winner Rate
    TotalForehandStrokes = TotalForwards

    # TODO: Add in the dataframe
    ForehandErrorRate = None
    if TotalForehandStrokes is None or TotalForehandStrokes <= 0:
        ForehandErrorRate = 0
    else:
        ForehandErrorRate = math.ceil((TotalForehandErrors / TotalForehandStrokes) * 100)

    # Backhand Error Rate

    TotalBackhandErrors = len(PrimaryData[BackhandShotCondition & notNullErrorType & playedByCondition & matchCondition])

    # "TotalBackhands" taken from Backhand Winner Rate
    TotalBackhandStrokes = TotalBackhands

    # TODO: Add in the dataframe
    BackhandErrorRate = None
    if TotalBackhandStrokes is None or TotalBackhandStrokes <= 0:
        BackhandErrorRate = 0
    else:
        BackhandErrorRate = math.ceil((TotalBackhandErrors / TotalBackhandStrokes) * 100)




