import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

STAND = 0
HIT = 1
DOUBLE = 2

ACT_ID_TO_NAME = {0: 'S',
                  1: 'H',
                  2: 'D'}

def value_to_state_id(pv, dv, win=False, lose=False) -> int:

    if win:
        return 170
    elif lose:
        return 171
    state_id = (dv-2)*17 + (pv-4)

    if state_id > 170:
        raise ValueError(f"Somehow, state_id mapping did something wrong. \
                                state_id={state_id}")

    return state_id

def state_id_to_value(state_id):

    dv = state_id // 17 + 2
    pv = state_id % 17 + 4

    if state_id == 170:
        return None, None # WIN state
    if state_id == 171:
        return None, None # LOSS state

    return pv, dv

def plot_strategy(state_map, title='Default Strategy'):

    # strategy = {dv+2:[] for dv in range(10)}
    strategy = np.zeros((17, 10))
    labels = ["U"]*170
    labels = np.array(labels).reshape(17,10)

    actions = np.argmax(state_map, axis=1)
    for i, act in enumerate(actions):
        pv, dv = state_id_to_value(i)
        if pv is not None:

            # Apply double contraint
            if (act == DOUBLE) and (pv not in [10, 11]):
                # Double is not a valid action atm. 
                act = np.argmax(state_map[i, :-1])

            strategy[pv-4, dv-2] = act
            labels[pv-4][dv-2] = ACT_ID_TO_NAME[act]


    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    ax.set_title(f"{title}")
    s = sns.heatmap(strategy, annot=labels, fmt="", 
                    yticklabels=list(range(4,21)), 
                    xticklabels=list(range(2, 12)),
                    vmax=3.0,
                    cmap='BuPu', cbar=False)
    ax.xaxis.tick_top()
    s.set(xlabel='Dealer Up-Card Value', ylabel='Player Hand Value')

    plt.savefig(f'{title}.png', dpi=500)
    plt.show()


def plot_qvalues(state_map, title='Default Strategy'):

    strategy = np.zeros((17, 10))
    labels = ["U"]*170
    labels = np.array(labels).reshape(17,10)

    actions = np.argmax(state_map, axis=1)
    for i, act in enumerate(actions):
        pv, dv = state_id_to_value(i)
        if pv is not None:

            # Apply double contraint
            if (act == DOUBLE) and (pv not in [10, 11]):
                # Double is not a valid action atm. 
                act = np.argmax(state_map[i, :-1])

            strategy[pv-4, dv-2] = np.max(state_map[i, :-1])
            labels[pv-4][dv-2] = ACT_ID_TO_NAME[act]
            
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    ax.set_title(f"{title}")
    s = sns.heatmap(strategy, annot=labels, fmt="", 
                    yticklabels=list(range(4,21)), 
                    xticklabels=list(range(2, 12)),
                    cmap='BuPu', cbar=False)
    ax.xaxis.tick_top()
    s.set(xlabel='Dealer Up-Card Value', ylabel='Player Hand Value')

    plt.savefig(f'Q-Values_{title}.png', dpi=500)
    plt.show()
