import numpy as np
import setup_variables
from calc_player_trans import calc_player_trans
from calc_player_trans_split import calc_player_trans_split
from calc_dealer_trans import calc_dealer_trans
from compute_term_profit import compute_term_profit

def adv_single_hand(deck, strategy):
    """
    Computes player's advantage per hand, given the deck distribution
    and the player's strategy.  Must call setup_variables.setup_variables() first.
    """
    PLAYERfirst      = setup_variables.PLAYERfirst
    PLAYERsplit      = setup_variables.PLAYERsplit
    PLAYERbj         = setup_variables.PLAYERbj
    PLAYERdoubBust   = setup_variables.PLAYERdoubBust

    DEALERfirst      = setup_variables.DEALERfirst
    DEALERbj         = setup_variables.DEALERbj

    Pinf  = setup_variables.Pinf   
    PSinf = setup_variables.PSinf  
    PDinf = setup_variables.PDinf  


    deck = np.array(deck, dtype=float)

    deck = np.append(deck, deck[0])


    calc_player_trans(deck, strategy)
    calc_player_trans_split(deck, strategy)
    calc_dealer_trans(deck)


    dProfits   = np.zeros(11, dtype=float)
    splitProfits = np.zeros(11, dtype=float)

    for dCard_idx in range(1, 11):
        if deck[dCard_idx] > 0:
            pdRow = PDinf[DEALERfirst[dCard_idx] - 1, :]

            pRow = np.zeros(PLAYERdoubBust, dtype=float)
            for pCard_idx in range(1, 11):  
                p_states = Pinf[dCard_idx, PLAYERfirst[pCard_idx] - 1, :]
                pRow += deck[pCard_idx] * p_states

            probDealerBJ = pdRow[DEALERbj - 1]

    
            profitDealerBJ = -1.0 * (1.0 - pRow[PLAYERbj - 1])

            pdRowNoBJ = pdRow.copy()
            pdRowNoBJ[DEALERbj - 1] = 0.0
            pdRowNoBJ = pdRowNoBJ / np.sum(pdRowNoBJ)

            for ii_idx in range(1, 11):
                pRowSplit = PSinf[dCard_idx, PLAYERfirst[ii_idx] - 1, :]
                splitProfits[ii_idx] = compute_term_profit(pRowSplit, pdRowNoBJ)

            profitNoDealerBJ = compute_term_profit(pRow, pdRowNoBJ)

            for ii_idx in range(1, 11):
                prob_split = pRow[PLAYERsplit[ii_idx] - 1]
                profitNoDealerBJ += 2.0 * prob_split * splitProfits[ii_idx]

            dProfits[dCard_idx] = (
                probDealerBJ * profitDealerBJ
                + (1.0 - probDealerBJ) * profitNoDealerBJ
            )

    playerAdvantage = np.sum(dProfits * deck)
    return playerAdvantage