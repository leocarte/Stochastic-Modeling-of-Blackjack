import numpy as np
import setup_variables

def compute_term_profit(pRow, pdRow):
    """
    Given player and dealer terminal distribution vectors pRow and pdRow,
    computes the expected profit per hand (no split terminations).
    """
    PLAYERstand       = setup_variables.PLAYERstand
    PLAYERdoubStand   = setup_variables.PLAYERdoubStand
    PLAYERbj          = setup_variables.PLAYERbj
    PLAYERsurrender   = setup_variables.PLAYERsurrender
    PLAYERbust        = setup_variables.PLAYERbust
    PLAYERdoubBust    = setup_variables.PLAYERdoubBust

    DEALERstand       = setup_variables.DEALERstand
    DEALERbj          = setup_variables.DEALERbj
    DEALERbust        = setup_variables.DEALERbust

    pLow = np.sum(pRow[PLAYERstand[3:16] - 1])
    pDoubLow = np.sum(pRow[PLAYERdoubStand[5:16] - 1])

    dProfit = 0.0

    # Case 1: Dealer blackjack, player no blackjack
    dProfit += -1.0 * pdRow[DEALERbj - 1] * (1 - pRow[PLAYERbj - 1])
    # Case 2: Player blackjack (no dealer BJ)
    dProfit +=  1.5 * (1 - pdRow[DEALERbj - 1]) * pRow[PLAYERbj - 1]
    # Case 3: Player surrender (no dealer BJ)
    dProfit += -0.5 * (1 - pdRow[DEALERbj - 1]) * pRow[PLAYERsurrender - 1]
    # Case 4: Player bust (no dealer BJ)
    dProfit += -1.0 * (1 - pdRow[DEALERbj - 1]) * pRow[PLAYERbust - 1]
    # Case 5: Player double-bust (no dealer BJ)
    dProfit += -2.0 * (1 - pdRow[DEALERbj - 1]) * pRow[PLAYERdoubBust - 1]

    # Case 6: Dealer busts
    #   player <=21 single
    dProfit +=  1.0 * pdRow[DEALERbust - 1] * (pLow + np.sum(pRow[PLAYERstand[16:21] - 1]))
    #   player <=21 double
    dProfit +=  2.0 * pdRow[DEALERbust - 1] * (pDoubLow + np.sum(pRow[PLAYERdoubStand[16:21] - 1]))

    # Case 7: Dealer 21
    idx21 = DEALERstand[20] - 1 
    #   player <=20 single
    dProfit += -1.0 * pdRow[idx21] * (pLow + np.sum(pRow[PLAYERstand[16:20] - 1]))
    #   player <=20 double
    dProfit += -2.0 * pdRow[idx21] * (pDoubLow + np.sum(pRow[PLAYERdoubStand[16:20] - 1]))

    # Case 8: Dealer 20
    idx20 = DEALERstand[19] - 1 
    #   player <=19 single
    dProfit += -1.0 * pdRow[idx20] * (pLow + np.sum(pRow[PLAYERstand[16:19] - 1]))
    #   player ==21 single
    dProfit +=  1.0 * pdRow[idx20] * pRow[PLAYERstand[20] - 1]
    #   player <=19 double
    dProfit += -2.0 * pdRow[idx20] * (pDoubLow + np.sum(pRow[PLAYERdoubStand[16:19] - 1]))
    #   player ==21 double
    dProfit +=  2.0 * pdRow[idx20] * pRow[PLAYERdoubStand[20] - 1]

    # Case 9: Dealer 19
    idx19 = DEALERstand[18] - 1
    #   player <=18 single
    dProfit += -1.0 * pdRow[idx19] * (pLow + pRow[PLAYERstand[16] - 1] + pRow[PLAYERstand[17] - 1])
    #   player 20-21 single
    dProfit +=  1.0 * pdRow[idx19] * (pRow[PLAYERstand[19] - 1] + pRow[PLAYERstand[20] - 1])
    #   player <=18 double
    dProfit += -2.0 * pdRow[idx19] * (pDoubLow + pRow[PLAYERdoubStand[16] - 1] + pRow[PLAYERdoubStand[17] - 1])
    #   player 20-21 double
    dProfit +=  2.0 * pdRow[idx19] * (pRow[PLAYERdoubStand[19] - 1] + pRow[PLAYERdoubStand[20] - 1])

    # Case 10: Dealer 18
    idx18 = DEALERstand[17] - 1
    #   player <=17 single
    dProfit += -1.0 * pdRow[idx18] * (pLow + pRow[PLAYERstand[16] - 1])
    #   player 19-21 single
    dProfit +=  1.0 * pdRow[idx18] * np.sum(pRow[PLAYERstand[18:21] - 1])
    #   player <=17 double
    dProfit += -2.0 * pdRow[idx18] * (pDoubLow + pRow[PLAYERdoubStand[16] - 1])
    #   player 19-21 double
    dProfit +=  2.0 * pdRow[idx18] * np.sum(pRow[PLAYERdoubStand[18:21] - 1])

    # Case 11: Dealer 17
    idx17 = DEALERstand[16] - 1
    #   player <=16 single
    dProfit += -1.0 * pdRow[idx17] * pLow
    #   player 18-21 single
    dProfit +=  1.0 * pdRow[idx17] * np.sum(pRow[PLAYERstand[17:21] - 1])
    #   player <=16 double
    dProfit += -2.0 * pdRow[idx17] * pDoubLow
    #   player 18-21 double
    dProfit +=  2.0 * pdRow[idx17] * np.sum(pRow[PLAYERdoubStand[17:21] - 1])

    return dProfit
