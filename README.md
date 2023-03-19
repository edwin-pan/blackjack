# Blackjack: Are the "Basic Strategies" Sufficient?
[![report](https://img.shields.io/badge/Google%20Drive-PDF-yellow)](https://corgiorgy.com/) [![report](https://img.shields.io/badge/CS238-Website-red)](https://aa228.stanford.edu/)

### Author Contact:
Edwin Pan <edwinpan@cs.stanford.edu>

## Directory Structure
    .
    ├── envs                    
        ├── blackjack.py        # Blackjack Environment
        ├── card.py             # 
        ├── deck.py             # 
        ├── player.py           # 
        └── utils.py            # Environment utilities
    ├── policy                     
        ├── base_mf_policy.py   # Online Q-Learning policy
        ├── basic_policy.py     # Basic strategy policy
        ├── eg_policy.py        # Epsilon Greedy
        ├── random_policy.py    # Random actions
        └── utils.py            # Policy utilities
    ├── .gitignore
    ├── main.py                 # Runs train/eval
    ├── README.md 
    └── setup.py                # Setup script


## Getting Started
Clone the repository and install requirements.

```bash
git clone git@github.com:edwin-pan/blackjack.git
pip install -e .
```


## Running the Script
This implementation supports 4 different strategies, which can be run using the following. 

### Random Strategy
```bash
python main.py --policy random --num_games 1000000
```

### Scripted Strategy
```bash
python main.py --policy scripted --num_games 1000000
```

### Online Q-Learning Strategy 
```bash
python main.py --policy base_mf --num_games 1000000 
```

### Online Q-Learning Strategy w/ Epsilon Greedy Exploration
```bash
python main.py --policy epsilon_greedy --num_games 1000000 --epsilon 0.05
```




## Acknowledgement
The author gives thanks to Professor Mykel Kochenderfer and the course staff in AA228/CS238: Decision Making Under Uncertainty for their instruction.


## Citation
```bibtex
@inproceedings{cs238w23_ep_blackjack,
  title={Blackjack: Are the "Basic Strategies" Sufficient?},
  author={Pan, Edwin},
  month={March},
  year={2023}
}
```

## References
A full list of references for this project can be found in the report. 