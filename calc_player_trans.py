import numpy as np
from numpy.linalg import matrix_power
import setup_variables
import matplotlib.pyplot as plt
import set_strategy

def calc_player_trans(deck, strategy):
    """
    Given the deck pdf and a strategy namespace (with PAIR, HARD, SOFT arrays),
    computes the players's transition matrix (P) and its absorbing-power (Pinf).
    Populates setup_variables.P and setup_variables.Pinf in place.
    """
    PLAYERfirst      = setup_variables.PLAYERfirst
    PLAYERtwoHard    = setup_variables.PLAYERtwoHard
    PLAYERhard       = setup_variables.PLAYERhard
    PLAYERtwoSoft    = setup_variables.PLAYERtwoSoft
    PLAYERsoft       = setup_variables.PLAYERsoft
    PLAYERpair       = setup_variables.PLAYERpair
    PLAYERstand      = setup_variables.PLAYERstand
    PLAYERdoubStand  = setup_variables.PLAYERdoubStand
    PLAYERsplit      = setup_variables.PLAYERsplit
    PLAYERbj         = setup_variables.PLAYERbj
    PLAYERsurrender  = setup_variables.PLAYERsurrender
    PLAYERbust       = setup_variables.PLAYERbust
    PLAYERdoubBust   = setup_variables.PLAYERdoubBust

    houseRules  = setup_variables.houseRules
    playerMoves = setup_variables.playerMoves

    P    = setup_variables.P      # shape: (11, 122, 122)
    Pinf = setup_variables.Pinf   # shape: (11, 122, 122)

    SRA   = houseRules.SRA

    SR = playerMoves.SR
    S  = playerMoves.S
    H  = playerMoves.H
    DB = playerMoves.DB
    DS = playerMoves.DS
    SP = playerMoves.SP

    # Strategy tables
    PAIR = strategy.PAIR
    HARD = strategy.HARD
    SOFT = strategy.SOFT

    P.fill(0)

    # --- Set absorbing states ---
    for ii in range(4, 22):
        P[:, PLAYERstand[ii - 1] - 1, PLAYERstand[ii - 1] - 1] = 1

    for ii in range(6, 22):
        P[:, PLAYERdoubStand[ii - 1] - 1, PLAYERdoubStand[ii - 1] - 1] = 1

    for ii in range(2, 12):
        P[:, PLAYERsplit[ii - 1] - 1, PLAYERsplit[ii - 1] - 1] = 1


    # Blackjack, surrender, bust, double-bust absorbing states
    P[:, PLAYERbj - 1, PLAYERbj - 1] = 1
    P[:, PLAYERsurrender - 1, PLAYERsurrender - 1] = 1
    P[:, PLAYERbust - 1, PLAYERbust - 1] = 1
    P[:, PLAYERdoubBust - 1, PLAYERdoubBust - 1] = 1


    # --- Set first‐card transitions ---
    for ii in range(2, 12):
        from_idx = PLAYERfirst[ii - 1] - 1
        for pNew in range(2, 12):
            prob = deck[pNew - 1]
            if ii == pNew:
                to_idx = PLAYERpair[ii - 1] - 1
            else:
                new_tot  = ii + pNew
                new_soft = (ii == 11 or pNew == 11)
                if new_tot > 21:
                    new_tot  -= 10
                    new_soft  = True
                if new_tot == 21:
                    to_idx = PLAYERbj - 1
                elif new_soft:
                    to_idx = PLAYERtwoSoft[new_tot - 1] - 1
                else:
                    to_idx = PLAYERtwoHard[new_tot - 1] - 1
            P[:, from_idx, to_idx] += prob

    # --- Set twoHard transitions ---
    for ii in range(4, 22):
        from_idx = PLAYERtwoHard[ii - 1] - 1
        for dCard in range(2, 12):
            d_idx = dCard - 1
            move = HARD[ii - 4, dCard - 2]
            if move == SR and not SRA:
                move = H
            if move == SR:
                to_idx = PLAYERsurrender - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == S:
                to_idx = PLAYERstand[ii - 1] - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == H:
                for pNew in range(2, 12):
                    new_tot  = ii + pNew
                    new_soft = (pNew == 11)
                    if new_tot > 21 and new_soft:
                        new_tot  -= 10
                        new_soft = False
                    prob = deck[pNew - 1]
                    if new_tot > 21:
                        to_idx = PLAYERbust - 1
                    elif new_soft:
                        to_idx = PLAYERsoft[new_tot - 1] - 1
                    else:
                        to_idx = PLAYERhard[new_tot - 1] - 1
                    P[d_idx, from_idx, to_idx] += prob
            elif move in (DB, DS):
                for pNew in range(2, 12):
                    new_tot  = ii + pNew
                    new_soft = (pNew == 11)
                    if new_tot > 21 and new_soft:
                        new_tot  -= 10
                        new_soft = False
                    prob = deck[pNew - 1]
                    if new_tot > 21:
                        to_idx = PLAYERdoubBust - 1
                    else:
                        to_idx = PLAYERdoubStand[new_tot - 1] - 1
                    P[d_idx, from_idx, to_idx] += prob
            else:
                raise ValueError(f"Unknown move {move} in twoHard")

    # --- Set hard transitions ---
    for ii in range(5, 22):
        from_idx = PLAYERhard[ii - 1] - 1
        for dCard in range(2, 12):
            d_idx = dCard - 1
            move  = HARD[ii - 4, dCard - 2] 
            if move == SR or move == DB:
                move = H
            elif move == DS:
                move = S
            if move == S:
                to_idx = PLAYERstand[ii - 1] - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == H:
                for pNew in range(2, 12):
                    new_tot  = ii + pNew
                    new_soft = (pNew == 11)
                    if new_tot > 21 and new_soft:
                        new_tot  -= 10
                        new_soft = False
                    prob = deck[pNew - 1]
                    if new_tot > 21:
                        to_idx = PLAYERbust - 1
                    elif new_soft:
                        to_idx = PLAYERsoft[new_tot - 1] - 1
                    else:
                        to_idx = PLAYERhard[new_tot - 1] - 1
                    P[d_idx, from_idx, to_idx] += prob
            else:
                raise ValueError(f"Unknown move {move} in hard")

    # --- Set twoSoft transitions ---
    for ii in range(12, 22):
        from_idx = PLAYERtwoSoft[ii - 1] - 1
        for dCard in range(2, 12):
            d_idx = dCard - 1
            move  = SOFT[ii - 12, dCard - 2]
            if move == SR and not SRA:
                move = H
            if move == SR:
                to_idx = PLAYERsurrender - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == S:
                to_idx = PLAYERstand[ii - 1] - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == H:
                for pNew in range(2, 12):
                    new_tot  = ii + pNew
                    new_soft = True
                    if new_tot > 21:
                        new_tot  -= 10
                        new_soft  = (pNew == 11)
                    prob = deck[pNew - 1]
                    to_idx = (PLAYERsoft[new_tot - 1] - 1) if new_soft else (PLAYERhard[new_tot - 1] - 1)
                    P[d_idx, from_idx, to_idx] += prob
            elif move in (DB, DS):
                for pNew in range(2, 12):
                    new_tot  = ii + pNew
                    new_soft = True
                    if new_tot > 21:
                        new_tot  -= 10
                        new_soft  = (pNew == 11)
                    prob = deck[pNew - 1]
                    to_idx = PLAYERdoubStand[new_tot - 1] - 1
                    P[d_idx, from_idx, to_idx] += prob
            else:
                raise ValueError(f"Unknown move {move} in twoSoft")

    # --- Set soft transitions ---
    for ii in range(13, 22):
        from_idx = PLAYERsoft[ii - 1] - 1
        for dCard in range(2, 12):
            d_idx = dCard - 1
            move  = SOFT[ii - 12, dCard - 2]
            if move == SR or move == DB:
                move = H
            elif move == DS:
                move = S
            if move == S:
                to_idx = PLAYERstand[ii - 1] - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == H:
                for pNew in range(2, 12):
                    new_tot  = ii + pNew
                    new_soft = True
                    if new_tot > 21:
                        new_tot  -= 10
                        new_soft  = (pNew == 11)
                    prob = deck[pNew - 1]
                    to_idx = (PLAYERsoft[new_tot - 1] - 1) if new_soft else (PLAYERhard[new_tot - 1] - 1)
                    P[d_idx, from_idx, to_idx] += prob
            else:
                raise ValueError(f"Unknown move {move} in soft")

    # --- Set pair transitions ---
    for ii in range(2, 12):
        if ii == 11:
            pTot  = 12
            pSoft = True
        else:
            pTot  = 2 * ii
            pSoft = False
        from_idx = PLAYERpair[ii - 1] - 1
        for dCard in range(2, 12):
            d_idx = dCard - 1
            move  = PAIR[ii - 2, dCard - 2]
            if move == SR and not SRA:
                move = H
            if move == SR:
                to_idx = PLAYERsurrender - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == S:
                to_idx = PLAYERstand[pTot - 1] - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == SP:
                to_idx = PLAYERsplit[ii - 1] - 1
                P[d_idx, from_idx, to_idx] = 1.0
            elif move == H:
                for pNew in range(2, 12):
                    new_tot  = pTot + pNew
                    new_soft = pSoft or (pNew == 11)
                    if new_tot > 21 and new_soft:
                        new_tot  -= 10
                        new_soft  = (pSoft and (pNew == 11))
                    prob = deck[pNew - 1]
                    if new_tot > 21:
                        to_idx = PLAYERbust - 1
                    elif new_soft:
                        to_idx = PLAYERsoft[new_tot - 1] - 1
                    else:
                        to_idx = PLAYERhard[new_tot - 1] - 1
                    P[d_idx, from_idx, to_idx] += prob
            elif move in (DB, DS):
                for pNew in range(2, 12):
                    new_tot  = pTot + pNew
                    new_soft = pSoft or (pNew == 11)
                    if new_tot > 21 and new_soft:
                        new_tot  -= 10
                        new_soft  = (pSoft and (pNew == 11))
                    prob = deck[pNew - 1]
                    if new_tot > 21:
                        to_idx = PLAYERdoubBust - 1
                    else:
                        to_idx = PLAYERdoubStand[new_tot - 1] - 1
                    P[d_idx, from_idx, to_idx] += prob
            else:
                raise ValueError(f"Unknown move {move} in pair")

    # --- Compute Pinf (absorbing probabilities) ---
    Pinf.fill(0)
    for ii in range(2, 12):
        d_idx = ii - 1
        Pinf[d_idx, :, :] = matrix_power(P[d_idx, :, :], 21)



    
    '''num_states = PLAYERdoubBust # 122
    labels = [''] * num_states

    # first2…first11
    for i in range(2, 12):
        idx = PLAYERfirst[i - 1] - 1
        labels[idx] = f"first{i}"
    # twoHard4…twoHard21
    for i in range(4, 22):
        idx = PLAYERtwoHard[i - 1] - 1
        labels[idx] = f"twoHard{i}"
    # twoSoft12…twoSoft21
    for i in range(12, 22):
        idx = PLAYERtwoSoft[i - 1] - 1
        labels[idx] = f"twoSoft{i}"
    # pair2…pair11
    for i in range(2, 12):
        idx = PLAYERpair[i - 1] - 1
        labels[idx] = f"pair{i}"
    # hard5…hard21
    for i in range(5, 22):
        idx = PLAYERhard[i - 1] - 1
        labels[idx] = f"hard{i}"
    # soft13…soft21
    for i in range(13, 22):
        idx = PLAYERsoft[i - 1] - 1
        labels[idx] = f"soft{i}"
    # stand4…stand21
    for i in range(4, 22):
        idx = PLAYERstand[i - 1] - 1
        labels[idx] = f"stand{i}"
    # doubStand6…doubStand21
    for i in range(6, 22):
        idx = PLAYERdoubStand[i - 1] - 1
        labels[idx] = f"doubStand{i}"
    # split2…split11
    for i in range(2, 12):
        idx = PLAYERsplit[i - 1] - 1
        labels[idx] = f"split{i}"
    # bj, surrender, bust, doubBust
    labels[PLAYERbj        - 1] = 'bj'
    labels[PLAYERsurrender - 1] = 'surrender'
    labels[PLAYERbust      - 1] = 'bust'
    labels[PLAYERdoubBust  - 1] = 'doubBust'


    dealer_card = 2
    d_idx = dealer_card - 1

    fig, ax = plt.subplots(figsize=(10, 10))
    cax = ax.imshow(P[d_idx, :, :], cmap='jet', interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(cax, ax=ax, shrink=0.75, label='')

    ax.set_xticks(np.arange(num_states))
    ax.set_yticks(np.arange(num_states))
    ax.set_xticklabels(labels, rotation=90, fontsize=5)
    ax.set_yticklabels(labels, fontsize=5)

    ax.xaxis.tick_top()
    ax.tick_params(axis='x', labeltop=True, labelbottom=False)

    plt.tight_layout()
    plt.show()



setup_variables.setup_variables()
strategy = set_strategy.set_strategy('basic')

calc_player_trans(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1], dtype=float) / 13, strategy)'''