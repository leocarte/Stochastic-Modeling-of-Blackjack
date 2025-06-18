import numpy as np
from numpy.linalg import matrix_power
import setup_variables
import matplotlib.pyplot as plt

def calc_dealer_trans(deck):
    """
    Builds the dealer's transition matrix (PD) and its absorbing-power (PDinf) given the deck distribution. 
    Populates setup_variables.PD and setup_variables.PDinf.
    """
    DEALERfirst      = setup_variables.DEALERfirst
    DEALERhard       = setup_variables.DEALERhard
    DEALERsoft       = setup_variables.DEALERsoft
    DEALERstand      = setup_variables.DEALERstand
    DEALERbj         = setup_variables.DEALERbj
    DEALERbust       = setup_variables.DEALERbust

    houseRules = setup_variables.houseRules

    PD    = setup_variables.PD    # shape: (37, 37)
    PDinf = setup_variables.PDinf # shape: (37, 37)

    PD.fill(0)

    for ii in range(17, 22): 
        PD[DEALERstand[ii - 1] - 1, DEALERstand[ii - 1] - 1] = 1 

    PD[DEALERbj - 1, DEALERbj - 1] = 1
    PD[DEALERbust - 1, DEALERbust - 1] = 1
    PD[DEALERhard[17 - 1] - 1, DEALERstand[17 - 1] - 1] = 1


    # --- Set first transitions ---
    for ii in range(2, 12):         
        for dNew in range(2, 12):  
            newDtot = ii + dNew
            newDsoft = (ii == 11 or dNew == 11)
            if newDtot > 21:
                # Pair of aces
                newDtot = newDtot - 10
                newDsoft = True
            from_state = DEALERfirst[ii - 1] - 1
            if newDtot == 21:
                to_state = DEALERbj - 1 
                PD[from_state, to_state] += deck[dNew - 1]
            elif newDtot > 17:
                to_state = DEALERstand[newDtot - 1] - 1
                PD[from_state, to_state] += deck[dNew - 1]
            elif newDsoft:
                to_state = DEALERsoft[newDtot - 1] - 1
                PD[from_state, to_state] += deck[dNew - 1]
            else:
                to_state = DEALERhard[newDtot - 1] - 1
                PD[from_state, to_state] += deck[dNew - 1]



    # --- Set hard transitions for totals 4..16 ---
    for ii in range(4, 17):  
        for dNew in range(2, 12):  
            newDtot = ii + dNew
            newDsoft = (dNew == 11)
            # Handle Ace as 1 if necessary (only if sum > 21 and dNew is Ace)
            if (newDtot > 21) and newDsoft:
                newDtot -= 10
                newDsoft = False
            from_state = DEALERhard[ii - 1] - 1         
            if newDtot > 21:
                to_state = DEALERbust - 1            
                PD[from_state, to_state] += deck[dNew - 1]
            elif newDtot > 17:
                to_state = DEALERstand[newDtot - 1] - 1  
                PD[from_state, to_state] += deck[dNew - 1]
            elif newDsoft:
                to_state = DEALERsoft[newDtot - 1] - 1   
                PD[from_state, to_state] += deck[dNew - 1]
            else:
                to_state = DEALERhard[newDtot - 1] - 1   
                PD[from_state, to_state] += deck[dNew - 1]


    # --- Set soft transitions for totals 12..17 ---
    for ii in range(12, 18): 
        for dNew in range(2, 12):  
            newDtot = ii + dNew
            newDsoft = True
            if newDtot > 21:
                newDtot -= 10
                newDsoft = (dNew == 11)
            from_state = DEALERsoft[ii - 1] - 1  
            if newDtot > 17:
                to_state = DEALERstand[newDtot - 1] - 1  
                PD[from_state, to_state] += deck[dNew - 1]
            elif newDsoft:
                to_state = DEALERsoft[newDtot - 1] - 1
                PD[from_state, to_state] += deck[dNew - 1]
            else:
                to_state = DEALERhard[newDtot - 1] - 1
                PD[from_state, to_state] += deck[dNew - 1]


    # If “Dealer stands on soft 17” (DSSS), override the soft-17 row
    if houseRules.DSSS:
        PD[DEALERsoft[16] - 1, :] = 0            
        PD[DEALERsoft[16] - 1, DEALERstand[16] - 1] = 1 

    # --- Compute PDinf = PD^17 ---
    PDinf[:,:] = matrix_power(PD, 17)




    '''# Plot the dealer's transition matrix
    num_states = DEALERbust  # 37
    labels = [''] * num_states

    # first2…first11
    for i in range(2, 12):
        idx = DEALERfirst[i - 1] - 1
        labels[idx] = f"first{i}"

    # hard4…hard17
    for i in range(4, 18):
        idx = DEALERhard[i - 1] - 1
        labels[idx] = f"hard{i}"

    # soft12…soft17
    for i in range(12, 18):
        idx = DEALERsoft[i - 1] - 1
        labels[idx] = f"soft{i}"

    # stand17…stand21
    for i in range(17, 22):
        idx = DEALERstand[i - 1] - 1
        labels[idx] = f"stand{i}"

    # blackjack and bust
    labels[DEALERbj   - 1] = 'bj'
    labels[DEALERbust - 1] = 'bust'

    fig, ax = plt.subplots(figsize=(10, 10))
    cax = ax.imshow(PDinf, cmap='jet', interpolation='nearest', vmin=0, vmax=1)
    fig.colorbar(cax, ax=ax, shrink=0.75, label='')

    ax.set_xticks(np.arange(num_states))
    ax.set_yticks(np.arange(num_states))
    ax.set_xticklabels(labels, rotation=90, fontsize=6)
    ax.set_yticklabels(labels, fontsize=6)

    ax.xaxis.tick_top()                                
    ax.tick_params(axis='x', labeltop=True, labelbottom=False)  

    plt.tight_layout()
    plt.show()


setup_variables.setup_variables()

calc_dealer_trans(np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1], dtype=float) / 13)'''