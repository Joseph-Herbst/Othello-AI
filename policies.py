def policy(state):
    while not state.isTerminal():
        try:
            state = state.takeAction(state.board.decentMove())
        except:
            pass
        try:
            state = state.takeAction(state.board.dumbMove())
        except:
            pass

    return state.getReward()
