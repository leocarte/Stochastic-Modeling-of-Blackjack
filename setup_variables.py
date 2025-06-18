import numpy as np
from types import SimpleNamespace

def setup_variables():

    global PLAYERfirst, PLAYERtwoHard, PLAYERhard, PLAYERtwoSoft, PLAYERsoft
    global PLAYERpair, PLAYERstand, PLAYERdoubStand, PLAYERsplit
    global PLAYERbj, PLAYERsurrender, PLAYERbust, PLAYERdoubBust, numPlayerStates

    global DEALERfirst, DEALERhard, DEALERsoft, DEALERstand
    global DEALERbj, DEALERbust, numDealerStates

    global houseRules
    global playerMoves
    global P, PD, Pinf, PSinf, PDinf
    global basic

    #%% Define playing rules
    houseRules = SimpleNamespace()
    houseRules.DSSS = 1    # Dealer stands on soft 17
    houseRules.DASA = 1    # Double after split allowed
    houseRules.MSA = 0     # Multiple splits allowed (CODE NOT CONFIGURED FOR "YES")
    houseRules.HASAA = 0   # Hit after split aces allowed (resplitting also allowed)
    houseRules.SRA = 0     # Surrender allowed (after dealer checks for bj and before player draws cards)

    # State names for player transitions
    PLAYERfirst      = np.array([0] + list(range(1, 11)))               
    PLAYERtwoHard    = np.array([0, 0, 0] + list(range(11, 29)))         
    PLAYERhard       = np.array([0, 0, 0, 0] + list(range(29, 46)))       
    PLAYERtwoSoft    = np.array([0]*11 + list(range(46, 56)))           
    PLAYERsoft       = np.array([0]*12 + list(range(56, 65)))               
    PLAYERpair       = np.array([0] + list(range(65, 75)))                  
    PLAYERstand      = np.array([0, 0, 0] + list(range(75, 93)))          
    PLAYERdoubStand  = np.array([0]*5 + list(range(93, 109)))         
    PLAYERsplit      = np.array([0] + list(range(109, 119)))             
    PLAYERbj         = 119
    PLAYERsurrender  = 120
    PLAYERbust       = 121
    PLAYERdoubBust   = 122

    numPlayerStates = PLAYERdoubBust  # 122 

    # State names for dealer transitions
    DEALERfirst      = np.array([0] + list(range(1, 11)))                    
    DEALERhard       = np.array([0, 0, 0] + list(range(11, 25)))             
    DEALERsoft       = np.array([0]*11 + list(range(25, 31)))                
    DEALERstand      = np.array([0]*16 + list(range(31, 36)))             
    DEALERbj         = 36
    DEALERbust       = 37

    numDealerStates = DEALERbust  # 37 

    # Possible moves for the player (elements of strategy tables)
    playerMoves = SimpleNamespace()
    playerMoves.S  = 0   # Stand
    playerMoves.DB = 1   # Double (else Hit)
    playerMoves.DS = 2   # Double (else Stand)
    playerMoves.H  = 3   # Hit
    playerMoves.SP = 4   # Split
    playerMoves.SR = 5   # Surrender (else Hit)

    # Transition matrices
    P  = np.zeros((11, numPlayerStates, numPlayerStates))   # Player's hand
    PD = np.zeros((numDealerStates, numDealerStates))       # Dealer's hand

    # "Infinite matrices" (all probability in absorbing states)
    Pinf  = np.zeros((11, numPlayerStates, numPlayerStates))   # Player's hand
    PSinf = np.zeros((11, numPlayerStates, numPlayerStates))   # Player's hand after splitting a pair
    PDinf = np.zeros((numDealerStates, numDealerStates))       # Dealer's hand

    #%% Basic Strategy Tables
    S  = 0 
    DB = 1  
    DS = 2  
    H  = 3  
    SP = 4  
    SR = 5  

    basic = SimpleNamespace()

    #   2  3  4  5  6  7  8  9 10  A
    basic.pairStrategyDASA = np.array([
        [ SP, SP, SP, SP, SP, SP,  H,  H,  H,  H],  # 2-2
        [ SP, SP, SP, SP, SP, SP,  H,  H,  H,  H],  # 3-3
        [  H,  H,  H, SP, SP,  H,  H,  H,  H,  H],  # 4-4
        [ DB, DB, DB, DB, DB, DB, DB, DB,  H,  H],  # 5-5
        [ SP, SP, SP, SP, SP,  H,  H,  H,  H,  H],  # 6-6
        [ SP, SP, SP, SP, SP, SP,  H,  H,  H,  H],  # 7-7
        [ SP, SP, SP, SP, SP, SP, SP, SP, SP, SP],  # 8-8
        [ SP, SP, SP, SP, SP,  S, SP, SP,  S,  S],  # 9-9
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 10-10
        [ SP, SP, SP, SP, SP, SP, SP, SP, SP, SP],  # A-A
    ], dtype=int)

    #   2  3  4  5  6  7  8  9 10  A
    basic.pairStrategyNoDASA = np.array([
        [  H,  H, SP, SP, SP, SP,  H,  H,  H,  H],  # 2-2
        [  H,  H, SP, SP, SP, SP,  H,  H,  H,  H],  # 3-3
        [  H,  H,  H,  H,  H,  H,  H,  H,  H,  H],  # 4-4
        [ DB, DB, DB, DB, DB, DB, DB, DB,  H,  H],  # 5-5
        [  H, SP, SP, SP, SP,  H,  H,  H,  H,  H],  # 6-6
        [ SP, SP, SP, SP, SP, SP,  H,  H,  H,  H],  # 7-7
        [ SP, SP, SP, SP, SP, SP, SP, SP, SP, SP],  # 8-8
        [ SP, SP, SP, SP, SP,  S, SP, SP,  S,  S],  # 9-9
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 10-10
        [ SP, SP, SP, SP, SP, SP, SP, SP, SP, SP],  # A-A
    ], dtype=int)

    #   2  3  4  5  6  7  8  9 10  A
    basic.softStrategy = np.array([
        [  H,  H,  H,  H, DB,  H,  H,  H,  H,  H],  # 12
        [  H,  H,  H,  H, DB,  H,  H,  H,  H,  H],  # 13
        [  H,  H,  H, DB, DB,  H,  H,  H,  H,  H],  # 14
        [  H,  H, DB, DB, DB,  H,  H,  H,  H,  H],  # 15
        [  H,  H, DB, DB, DB,  H,  H,  H,  H,  H],  # 16
        [  H, DB, DB, DB, DB,  H,  H,  H,  H,  H],  # 17
        [  S, DS, DS, DS, DS,  S,  S,  H,  H,  H],  # 18
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 19
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 20
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 21
    ], dtype=int)

    #   2  3  4  5  6  7  8  9 10  A
    basic.hardStrategy = np.array([
        [  H,  H,  H,  H,  H,  H,  H,  H,  H,  H],  # 4
        [  H,  H,  H,  H,  H,  H,  H,  H,  H,  H],  # 5
        [  H,  H,  H,  H,  H,  H,  H,  H,  H,  H],  # 6
        [  H,  H,  H,  H,  H,  H,  H,  H,  H,  H],  # 7
        [  H,  H,  H,  H,  H,  H,  H,  H,  H,  H],  # 8
        [  H, DB, DB, DB, DB,  H,  H,  H,  H,  H],  # 9
        [ DB, DB, DB, DB, DB, DB, DB, DB,  H,  H],  # 10
        [ DB, DB, DB, DB, DB, DB, DB, DB, DB,  H],  # 11
        [  H,  H,  S,  S,  S,  H,  H,  H,  H,  H],  # 12
        [  S,  S,  S,  S,  S,  H,  H,  H,  H,  H],  # 13
        [  S,  S,  S,  S,  S,  H,  H,  H,  H,  H],  # 14
        [  S,  S,  S,  S,  S,  H,  H,  H, SR,  H],  # 15
        [  S,  S,  S,  S,  S,  H,  H, SR, SR, SR],  # 16
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 17
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 18
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 19
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 20
        [  S,  S,  S,  S,  S,  S,  S,  S,  S,  S],  # 21
    ], dtype=int)

