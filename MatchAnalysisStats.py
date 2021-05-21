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

    # Serve Point

    # Service Shot Conditions
    serv_Y_Condition = PrimaryData['SERVICE_BY'] == 'Y'
    shot0_Condition = PrimaryData['Shot_no'] == 0
    shot1_Condition = PrimaryData['Shot_no'] == 1

    # Required Service Shot Data
    serviceShotFilter = PrimaryData[matchCondition & serv_Y_Condition & playedByCondition & (shot1_Condition | shot0_Condition)]

    # Wining Shot2 and Score condition
    main_win_condition = PrimaryData['WON_BY'] == player_name
    score_len_condition = PrimaryData['SCORE'].notnull()
    shot2_Condition = PrimaryData['Shot_no'] == 2
    WinShotScoreFilter = PrimaryData[matchCondition & score_len_condition & main_win_condition & shot2_Condition]
    GamePoint_ServiceShot = []
    GamePoint_WinShot = []
    for i in range(len(serviceShotFilter)):
        GamePoint_ServiceShot.append(str(serviceShotFilter['POINT'].iloc[i]) + '-' + str(serviceShotFilter['Game'].iloc[i]))

    for i in range(len(WinShotScoreFilter)):
        GamePoint_WinShot.append(str(WinShotScoreFilter['POINT'].iloc[i]) + '-' + str(WinShotScoreFilter['Game'].iloc[i]))

    GamePoint_WinShot = set(GamePoint_WinShot)
    GamePoint_ServiceShot = set(GamePoint_ServiceShot)

    # TODO: Add to dataframe
    ServePoint = len(GamePoint_ServiceShot & GamePoint_WinShot)

    # Serve Error
    # TODO: Add to Dataframe
    # TODO: Name Confirmation Serve Error
    ServerError = len(serviceShotFilter[serviceShotFilter['SCORE'].notnull()])

    # Serve Return Win

    MatchShot2Filter = PrimaryData[matchCondition & shot2_Condition & playedByCondition]

    # Shot 3 Filter
    shot3_Condition = PrimaryData['Shot_no'] == 3

    MatchScoreShot3Filter = PrimaryData[shot3_Condition & matchCondition & score_len_condition & main_win_condition]

    # Game Point Match Shot_2
    GPShot2 = []
    for i in range(len(MatchShot2Filter)):
        GPShot2.append(
            str(MatchShot2Filter['POINT'].iloc[i]) + '-' + str(MatchShot2Filter['Game'].iloc[i]))

    GPShot2 = set(GPShot2)

    GPScoreShot3 = []
    for i in range(len(MatchScoreShot3Filter)):
        GPScoreShot3.append(
            str(MatchScoreShot3Filter['POINT'].iloc[i]) + '-' + str(MatchScoreShot3Filter['Game'].iloc[i]))

    GPScoreShot3 = set(GPScoreShot3)

    # TODO: Add to Dataframe
    ServeReturnWin = len(GPShot2 & GPScoreShot3)

    # Point on 3rd Ball
    matchShot3Filter = PrimaryData[matchCondition & shot3_Condition & playedByCondition]

    # Shot 4 Filter
    shot4_Condition = PrimaryData['Shot_no'] == 4
    MatchScoreShot4Filter = PrimaryData[shot4_Condition & matchCondition & score_len_condition & main_win_condition]

    # Game Point Match Shot_3
    GPShot3 = []
    for i in range(len(matchShot3Filter)):
        GPShot3.append(
            str(matchShot3Filter['POINT'].iloc[i]) + '-' + str(matchShot3Filter['Game'].iloc[i]))

    GPShot3 = set(GPShot3)

    GPScoreShot4 = []
    for i in range(len(MatchScoreShot4Filter)):
        GPScoreShot4.append(
            str(MatchScoreShot4Filter['POINT'].iloc[i]) + '-' + str(MatchScoreShot4Filter['Game'].iloc[i]))

    GPScoreShot4 = set(GPScoreShot4)

    # TODO: Add to Dataframe
    PointsOn3rdBall = len(GPScoreShot4 & GPShot3)

    # Error on 3rd ball
    thirdShotPoint = PrimaryData['pointon3ndshot'] == 1
    otherWinCondition = PrimaryData['WON_BY'] != player_name

    # TODO: Add to Dataframe
    ErrorsOn3rdBall = len(PrimaryData[matchCondition & thirdShotPoint & otherWinCondition])

    # Biggest Lead












