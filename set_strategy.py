from types import SimpleNamespace
import setup_variables

def set_strategy(type):
    """
    Returns strategy: a namespace with fields 'bet', 'PAIR', 'SOFT', 'HARD'
    """
    # Pull the already-initialized objects out of setup_variables
    houseRules = setup_variables.houseRules
    basic       = setup_variables.basic

    if type == 'basic':
        strategy = SimpleNamespace()
        strategy.bet = 1

        if houseRules.DASA:
            strategy.PAIR = basic.pairStrategyDASA
        else:
            strategy.PAIR = basic.pairStrategyNoDASA

        strategy.HARD = basic.hardStrategy
        strategy.SOFT = basic.softStrategy
        return strategy

    else:
        print("Unknown type!")
        return None

