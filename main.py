import numpy as np
import sys
import argparse
import matplotlib.pyplot as plt

from tqdm import tqdm

from envs.blackjack import BlackJackEnv
from policy.basic_policy import ScriptedEddiePolicy
from policy.random_policy import RandomPolicy
from policy.base_mf_policy import BaseModelFreePolicy
from policy.eg_policy import EpsilonGreedyPolicy
from policy.utils import value_to_state_id, plot_strategy, plot_qvalues

def parse_args():
    parser = argparse.ArgumentParser(
        description='Play some BlackJack, learn the best strategy.')

    parser.add_argument('--policy', default='scripted', type=str, 
                            help='Which policy to use')
    parser.add_argument('--epsilon', default=0.05, type=float,
                            help='Epsilon, for epsilon greedy exploration.')
    parser.add_argument('--num_games', default=1000000, type=int, 
                            help='Number of games to play')
    parser.add_argument('--num_eval_games', default=100000, type=int,
                            help='Number of games to play for evaluation.')
    parser.add_argument('--debug', action='store_true', 
                            help='Run in debug mode. Prints tracebacks.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_args()

    # ------------------ Setup ------------------
    # Create the environment
    env = BlackJackEnv(debug=args.debug)

    # Instantiate the policy
    if args.policy == 'scripted':
        print("Player is executing Scripted")
        player_policy = ScriptedEddiePolicy()
    elif args.policy == 'random':
        print("PLayer is executing Random")
        player_policy = RandomPolicy()
    elif args.policy == 'epsilon_greedy':
        print("Player is executing Epsilon-Greedy")
        player_policy = EpsilonGreedyPolicy(args.epsilon)
    elif args.policy == 'base_mf':
        print("Player is executing Q-Learning")
        player_policy = BaseModelFreePolicy()
    else:
        raise ValueError(f"Given policy is not valid. ({args.policy})")
    
    # Play
    print("Running Training")
    record = []
    for i in tqdm(range(args.num_games)):
        r = 0
        while not env.done:
            
            # Record starting state
            s = value_to_state_id(env.player_value, env.dealer_value)

            # Player picks an action
            a = player_policy.step(env)

            # Step env given the action
            r = env.step(a)

            # Record next state
            if r > 0: # WIN
                sp = value_to_state_id(0, 0, win=True)
            elif r < 0: # LOSE
                sp = value_to_state_id(0, 0, lose=True)
            else:
                sp = value_to_state_id(env.player_value, env.dealer_value)

            if args.policy not in ['scripted', 'random']:
                player_policy.update(s, a, r, sp)

        if args.debug:
            print(f"Finished! rwd is {r}")
        record.append(r)

        env.reset()

    print(f"Average Training Reward: {np.average(record)}")
    np.save("experiment1_train.npy", record)

    print("Running Evaluation")
    eval_record = []
    player_policy.episode = 0 # No exploration on eval
    for i in tqdm(range(args.num_eval_games)):
        # Play game
        while not env.done:
            # Player picks an action
            a = player_policy.step(env)

            # Step env given the action
            r = env.step(a)

        eval_record.append(r)

        env.reset()

    print(f"Average Evaluation Reward: {np.average(eval_record)}")
    print(f"Cumulative Evaluation Reward: {np.sum(eval_record)}")
    print(f"Win Rate: {np.sum(np.array(eval_record)>0)/len(np.array(eval_record))*100:.2f}%")
    np.save("experiment1_eval.npy", eval_record)


    fig, ax = plt.subplots()
    plt.imshow(player_policy.Q, aspect='auto')
    plt.xticks([0.0, 1.0, 2.0])
    ax.set_xticklabels(['STAND',  'HIT','DOUBLE'])
    plt.colorbar()
    plt.savefig('exp_.png', dpi=500)

    if args.policy in ['scripted']:
        plot_strategy(player_policy.Q, title="Basic Strategy")
        plot_qvalues(player_policy.Q, title="Basic Strategy")
    elif args.policy in ['base_mf']:
        plot_strategy(player_policy.Q, title="Online Q-Learning Strategy")
        plot_qvalues(player_policy.Q, title="Online Q-Learning Strategy")
    elif args.policy in ['epsilon_greedy']:
        plot_strategy(player_policy.Q, title="Online Q-Learning + Epsilon Greedy Strategy")
        plot_qvalues(player_policy.Q, title="Online Q-Learning + Epsilon Greedy Strategy")
    elif args.policy in ['random']:
        plot_strategy(player_policy.Q, title="Random Strategy")
        plot_qvalues(player_policy.Q, title="Random Strategy")
    else:
        raise ValueError("Unknown policy")
    
    
    print(f"Saving learned Q values to {args.policy}.npy")
    np.save(args.policy+'.npy', player_policy.Q)