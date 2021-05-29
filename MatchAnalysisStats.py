import pandas as pd
import math
import numpy as np
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
        GamePoint_ServiceShot.append(str(match_no) + '-' + str(serviceShotFilter['Game'].iloc[i]) + '-' + str(serviceShotFilter['POINT'].iloc[i]))

    for i in range(len(WinShotScoreFilter)):
        GamePoint_WinShot.append(str(match_no) + '-' + str(WinShotScoreFilter['Game'].iloc[i]) + '-' + str(WinShotScoreFilter['POINT'].iloc[i]))

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
        GPShot2.append(str(match_no) + '-' +
            str(MatchShot2Filter['Game'].iloc[i]) + '-' + str(MatchShot2Filter['POINT'].iloc[i]))

    GPShot2 = set(GPShot2)

    GPScoreShot3 = []
    for i in range(len(MatchScoreShot3Filter)):
        GPScoreShot3.append(str(match_no) + '-' +
            str(MatchScoreShot3Filter['Game'].iloc[i]) + '-' + str(MatchScoreShot3Filter['POINT'].iloc[i]))

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
        GPShot3.append(str(match_no) + '-' + str(matchShot3Filter['Game'].iloc[i]) + '-' + str(matchShot3Filter['POINT'].iloc[i]))

    GPShot3 = set(GPShot3)

    GPScoreShot4 = []
    for i in range(len(MatchScoreShot4Filter)):
        GPScoreShot4.append(str(match_no) + '-' + str(MatchScoreShot4Filter['Game'].iloc[i]) + '-' + str(MatchScoreShot4Filter['POINT'].iloc[i]))

    GPScoreShot4 = set(GPScoreShot4)

    # TODO: Add to Dataframe
    PointsOn3rdBall = len(GPScoreShot4 & GPShot3)

    # Error on 3rd ball
    thirdShotPoint = PrimaryData['pointon3ndshot'] == 1
    otherWinCondition = PrimaryData['WON_BY'] != player_name

    # TODO: Add to Dataframe
    ErrorsOn3rdBall = len(PrimaryData[matchCondition & thirdShotPoint & otherWinCondition])

    # Biggest Lead
    BiggestLead = None
    ScoreA = []
    ScoreB = []
    # Game Point Saved
    pl_a_num = []
    pl_b_num = []

    for game in PrimaryData['Game'].unique():
        sum_a = 0
        sum_b = 0
        count_a = 0
        count_b = 0
        gameFilter = PrimaryData[(PrimaryData['Game'] == game) & PrimaryData['SCORE'].notnull()]
        for i, row in gameFilter.iterrows():
            sum_a += row['SCOREA']
            sum_b += row['SCOREB']
            ScoreA.append(sum_a)
            ScoreB.append(sum_b)
            if(sum_a == 10):
                count_a += 1
            if(sum_b == 10):
                count_b += 1

        pl_a_num.append(count_a - 1)
        pl_b_num.append(count_b - 1)
    ScoreA = np.array(ScoreA)
    ScoreB = np.array(ScoreB)

    # Todo: Add BiggestLead to dataframe
    if(PrimaryData['Player_A_Name'].iloc[0] == player_name):
        lead = np.absolute(ScoreA - ScoreB)
        BiggestLead = max(lead)
    else:
        lead = np.absolute(ScoreB - ScoreA)
        BiggestLead = max(lead)

    # Game Points Saved
    GamePointsSaved = None
    if(player_type == 1):
        if(len(pl_b_num) > 0):
            GamePointsSaved = sum(pl_b_num)
    else:
        if (len(pl_a_num) > 0):
            GamePointsSaved = sum(pl_a_num)


    # Most Used Serve
    MostUserdServe = serviceShotFilter['Shot'].value_counts().index[0]

    # Most Effective Serve

    RefDict = {}
    for i in range(len(serviceShotFilter)):
        RefDict[str(match_no) + '-' + str(serviceShotFilter['Game'].iloc[i]) + '-' + str(serviceShotFilter['POINT'].iloc[i])] = serviceShotFilter['Shot'].iloc[i]

    commonShots = (GamePoint_WinShot & GamePoint_ServiceShot)
    EffectiveServe = {}
    # Frequency of each shot
    for i in commonShots:
        if(RefDict[i] in EffectiveServe):
            EffectiveServe[RefDict[i]] += 1
        else:
            EffectiveServe[RefDict[i]] = 1
    # Sort the dictionary in descending order
    sortedShots = {k: v for k, v in sorted(EffectiveServe.items(), key=lambda item: item[1], reverse=True)}

    # TODO: Add to Dataframe
    MostEffectiveServe = (list(sortedShots.keys())[0])

    # Maximum Frequency Count
    max_val = list(sortedShots.values())[0]
    # Least Effective Serve

    # Minimum Frequency Count
    min_val = list(sortedShots.values())[-1]
    # TODO: Add to Dataframe
    if (min_val == max_val):
        LeastEffectiveServe = MostEffectiveServe
    else:
        LeastEffectiveServe = list(sortedShots.keys())[-1]

    # Most Used serve return
    shot2Filter = PrimaryData[matchCondition & shot2_Condition & playedByCondition]

    # TODO: Add to Dataframe
    MostUsedServeReturn = shot2Filter['Shot'].value_counts().index[0]

    # Most Effective serve return
    gamePoint_shot2 = {}

    wonBy_Filter = PrimaryData[matchCondition & main_win_condition]
    for i in range(len(wonBy_Filter)):
        gamePoint_Concat = str(match_no) + '-' + str(wonBy_Filter['Game'].iloc[i]) + '-' + str(wonBy_Filter['POINT'].iloc[i])

        if (gamePoint_Concat in gamePoint_shot2):
            gamePoint_shot2[gamePoint_Concat] += 1
        else:
            gamePoint_shot2[gamePoint_Concat] = 1
    shotFreq = {}
    for i in range(len(shot2Filter)):
        gamePoint_Concat = str(match_no) + '-' + str(shot2Filter['Game'].iloc[i]) + '-' + str(shot2Filter['POINT'].iloc[i])
        if(gamePoint_shot2.get(gamePoint_Concat)):
            eachShot = shot2Filter.iloc[i]['Shot']
            if(eachShot in shotFreq):
                shotFreq[eachShot] += 1

            else:
                shotFreq[eachShot] = 1
    sortedShots = {k: v for k, v in sorted(shotFreq.items(), key=lambda item: item[1], reverse=True)}
    # TODO: Add to Dataframe
    MostEffectiveReturn = list(sortedShots.keys())[0]
    # Least Effective return
    # TODO: Add to Dataframe
    LeastEffectiveReturn = list(sortedShots.keys())[-1]

    # Top 2 Error Zone Placement
    otherPlayedCondition = PrimaryData['Played_by'] != player_name
    notnullErrorFilter = PrimaryData[matchCondition & notNullErrorType & otherPlayedCondition & PrimaryData['Second_Last_Placement'].notnull()]
    top_1 = notnullErrorFilter['Second_Last_Placement'].value_counts().keys()[0]
    top_2 = notnullErrorFilter['Second_Last_Placement'].value_counts().keys()[1]

    # TODO: Add to Dataframe
    Top2ErrorZonePlacement = top_1 + ',' + top_2

    # Top 2 Highest Error Rate Placement
    uniqueSLPlacements = notnullErrorFilter['Second_Last_Placement'].unique()
    notnullPlacements = dict(notnullErrorFilter['Second_Last_Placement'].value_counts())
    ErrorRatePlacement = {}
    # Complete data without placement filter
    shotnot0Filter = PrimaryData[matchCondition & playedByCondition & (PrimaryData['Shot_no'] > 0)]
    # Fetch Total Count on Placement = Second_Last_placement
    for placement in uniqueSLPlacements:
        eachSame = shotnot0Filter[shotnot0Filter['Placement'] == placement]
        # print(placement, sum(eachSame))
        TotalShots = len(eachSame)
        # When TotalShots <= 0
        perc = 0
        if(TotalShots > 0):
            perc = math.ceil((notnullPlacements[placement] / TotalShots) * 100)
        ErrorRatePlacement[placement] = perc
    sortedPerc = {k: v for k, v in sorted(ErrorRatePlacement.items(), key=lambda item: item[1], reverse=True)}

    considerIndex = 0
    if(list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement1 = list(sortedPerc.keys())[considerIndex + 1]
    else:
        topPlacement1 = list(sortedPerc.keys())[considerIndex]

    if (list(sortedPerc.keys())[considerIndex + 1] == 'NC' or list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 2]
    else:
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 1]
        # TODO: Add to Dataframe
    Top2HighestErrorRatePlacement = topPlacement1 + ',' + topPlacement2


    # # Top 2 Lowest Error Rate Placement
    sortedPerc = {k: v for k, v in sorted(ErrorRatePlacement.items(), key=lambda item: item[1])}

    considerIndex = 0
    if (list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement1 = list(sortedPerc.keys())[considerIndex + 1]
    else:
        topPlacement1 = list(sortedPerc.keys())[considerIndex]

    if (list(sortedPerc.keys())[considerIndex + 1] == 'NC' or list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 2]
    else:
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 1]
        # TODO: Add to Dataframe
    Top2LowestErrorRatePlacement = topPlacement1 + ',' + topPlacement2

    # Top2WinningOtherSidePlacements

    mainPlayerErrorFilter = PrimaryData[matchCondition & notNullErrorType & playedByCondition & PrimaryData['Second_Last_Placement'].notnull()]
    mainPlayerErrorPlacement = mainPlayerErrorFilter['Second_Last_Placement'].value_counts()
    if(mainPlayerErrorPlacement.keys()[0] != 'NC'):
        top_main_player_placement1 = mainPlayerErrorPlacement.keys()[0]
    else:
        top_main_player_placement1 = mainPlayerErrorPlacement.keys()[1]

    if (mainPlayerErrorPlacement.keys()[1] != 'NC'):
        top_main_player_placement2 = mainPlayerErrorPlacement.keys()[1]
    else:
        top_main_player_placement2 = mainPlayerErrorPlacement.keys()[2]
    # TODO: Add to Dataframe
    Top2WinningOtherSidePlacements = top_main_player_placement1 + ',' + top_main_player_placement2

    # Top2HighestWinningOtherSideRatePlacement

    uniqueSLPlacements_main = mainPlayerErrorFilter['Second_Last_Placement'].unique()
    mainPlayerErrorPlacement = dict(mainPlayerErrorFilter['Second_Last_Placement'].value_counts())
    ErrorRatePlacement_main = {}
    shotnot0Filter = PrimaryData[matchCondition & playedByCondition & (PrimaryData['Shot_no'] > 0)]
    for placement in uniqueSLPlacements_main:
        eachSame = shotnot0Filter[shotnot0Filter['Placement'] == placement]
        # print(placement, len(eachSame))
        TotalShots = len(eachSame)
        # When TotalShots <= 0
        perc = 0
        if (TotalShots > 0):
            perc = math.ceil((mainPlayerErrorPlacement[placement] / TotalShots) * 100)
        ErrorRatePlacement_main[placement] = perc
    sortedPerc = {k: v for k, v in sorted(ErrorRatePlacement_main.items(), key=lambda item: item[1], reverse=True)}
    considerIndex = 0
    if (list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement1 = list(sortedPerc.keys())[considerIndex + 1]
    else:
        topPlacement1 = list(sortedPerc.keys())[considerIndex]

    if (list(sortedPerc.keys())[considerIndex + 1] == 'NC' or list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 2]
    else:
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 1]
        # TODO: Add to Dataframe
    Top2HighestWinningOtherSideRatePlacement = topPlacement1 + ',' + topPlacement2

    # Top2LowestWinningOtherSideRatePlacement

    sortedPerc = {k: v for k, v in sorted(ErrorRatePlacement_main.items(), key=lambda item: item[1])}
    considerIndex = 0
    if (list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement1 = list(sortedPerc.keys())[considerIndex + 1]
    else:
        topPlacement1 = list(sortedPerc.keys())[considerIndex]

    if (list(sortedPerc.keys())[considerIndex + 1] == 'NC' or list(sortedPerc.keys())[considerIndex] == 'NC'):
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 2]
    else:
        topPlacement2 = list(sortedPerc.keys())[considerIndex + 1]
        # TODO: Add to Dataframe
    Top2LowestWinningOtherSideRatePlacement = topPlacement1 + ',' + topPlacement2

    # Top1WinningSameSidePlacement

    reverse_row_id_3_condition = PrimaryData['Reverse_Row_ID'] == 3
    reverseRowID3Filter = PrimaryData[matchCondition & reverse_row_id_3_condition & otherPlayedCondition & PrimaryData['Placement'].notnull()]

    # TODO: Add to Dataframe
    # TODO: Query Returning 'H' expected 'CH'
    Top1WinningSameSidePlacement = reverseRowID3Filter['Placement'].value_counts().keys()[0]

    # MostEffectiveWinningPlacement
    gamePointWinShot = {}
    wonByScoreFilter = PrimaryData[matchCondition & main_win_condition & score_len_condition]
    for i in range(len(wonByScoreFilter)):
        gamePoint_Concat = str(match_no) + '-' + str(wonByScoreFilter['Game'].iloc[i]) + '-' + str(wonByScoreFilter['POINT'].iloc[i])
        if(gamePoint_Concat in gamePointWinShot):
            gamePointWinShot[gamePoint_Concat] += 1
        else:
            gamePointWinShot[gamePoint_Concat] = 1

    reverse_row_id_2_condition = PrimaryData['Reverse_Row_ID'] == 2

    MatchReverseRowID2 = PrimaryData[matchCondition & reverse_row_id_2_condition & playedByCondition]
    MatchReverseRowID2Placement = {}
    for i in range(len(MatchReverseRowID2)):
        gamePoint_Concat = str(match_no) + '-' + str(MatchReverseRowID2['Game'].iloc[i]) + '-' + str(MatchReverseRowID2['POINT'].iloc[i])
        if(gamePointWinShot.get(gamePoint_Concat) != None):
            if(MatchReverseRowID2['Placement'].iloc[i] in MatchReverseRowID2Placement):
                MatchReverseRowID2Placement[MatchReverseRowID2['Placement'].iloc[i]] += 1
            else:
                MatchReverseRowID2Placement[MatchReverseRowID2['Placement'].iloc[i]] = 1
    sortedPlacement = {k: v for k, v in sorted(MatchReverseRowID2Placement.items(), key=lambda item: item[1], reverse=True)}
    # TODO: Add to Dataframe
    MostEffectiveWinningPlacement = list(sortedPlacement.keys())[0]

    # LeastEffectiveWinningPlacement

    # TODO: Add to Dataframe
    LeastEffectiveWinningPlacement = list(sortedPlacement.keys())[-1]

    # MostEffectiveStroke
    MatchReverseRowID2Shot = {}
    for i in range(len(MatchReverseRowID2)):
        gamePoint_Concat = str(match_no) + '-' + str(MatchReverseRowID2['Game'].iloc[i]) + '-' + str(MatchReverseRowID2['POINT'].iloc[i])
        if(gamePoint_shot2.get(gamePoint_Concat) != None):
            if(MatchReverseRowID2['Shot'].iloc[i] in MatchReverseRowID2Shot):
                MatchReverseRowID2Shot[MatchReverseRowID2['Shot'].iloc[i]] += 1
            else:
                MatchReverseRowID2Shot[MatchReverseRowID2['Shot'].iloc[i]] = 1
    sortedShotsReverseRow2 = {k: v for k, v in sorted(MatchReverseRowID2Shot.items(), key=lambda item: item[1], reverse=True)}

    # TODO: Add to Dataframe
    MostEffectiveStroke = list(sortedShotsReverseRow2.keys())[0]

    # LeastEffectiveStroke
    # TODO: Add to Dataframe
    LeastEffectiveStroke = list(sortedShotsReverseRow2.keys())[-1]

    # MostUsedStroke

    playerFilter = PrimaryData[matchCondition & playedByCondition]
    # TODO: Add to Dataframe
    MostUsedStroke = playerFilter['Shot'].value_counts().keys()[0]
    print(MostUsedStroke)









































