from envs.deck import Deck

# Action Space 
# 0: Stay
# 1: Hit
# 2: Double Down (only available if player hand has value 10 or 11)
# 3: Split -- not doing this for now

class BlackJackEnv():
    def __init__(self, num_players:int = 2, debug:bool=False):
        
        self.num_players = num_players
        self.debug_flag = debug

        if num_players != 2:
            raise NotImplementedError("More than 2 players not implemented")
        
        # Reset the game
        self.reset()

        return
    
    def reset(self) -> None:
        
        if self.debug_flag:
            print("New Game")
            
        # Step 1: Spawn a deck and shuffle it
        self.deck = Deck()
        self.bet_multiplier = 1

        # Step 2: Deal cards
        self.dealer_cards = [self.deck.draw() for _ in range(2)]
        self.player_cards = [self.deck.draw() for _ in range(2)]

        # Step 3: Mask one of the dealer's cards
        self.dealer_hidden_card = self.dealer_cards.pop()

        # Step 4: Initialize the score
        self.dealer_value = self._compute_hand_value(self.dealer_cards)
        self.player_value = self._compute_hand_value(self.player_cards)

        # Handle 21. Sometimes, player just wins
        if self.player_value == 21:
            self.done = True
            return 1*self.bet_multiplier
        
        # Handle aces. Sometimes, 2 aces issued. 
        if self._check_loss():
            return -1*self.bet_multiplier # Player lost, lose the bet

        # Step 5: If we just started, we are not done
        self.done = False

        if self.debug_flag:
            print(f"Dealer visible value: {self.dealer_value}, hand: {self.dealer_cards}")
            print(f"Player visible value: {self.player_value}, hand: {self.player_cards}")

        return 


    def _compute_hand_value(self, hand:list) -> int:
        """ Computes the score of each player. """
        hand_value = sum([card.value for card in hand])
        return hand_value


    def step(self, action:int) -> float:
        """ Parse the action specified and execute. 
        
        """

        # Do the action specified
        if action == 0: # Player chooses to STAY
            self.done = True
            # Perform final actions -- Dealer reveals & plays game out 
            rwd = self._perform_action_final()
            return rwd*self.bet_multiplier
        elif action == 1: # Player chooses to HIT
            # Perform hit actions -- Draw a card & accumulate player value
            self._perform_action_hit()
        elif action == 2: # Player chooses to DOUBLE-DOWN
            self.bet_multiplier *= 2
            # Perform hit actions -- Draw a card & accumulate player value
            self._perform_action_hit()

        # Check if the player has lost. Can be too high.
        if self._check_loss():
            return -1*self.bet_multiplier # Player lost, lose the bet

        # Check if the player won
        if self.player_value == 21:
            self.done = True
            return 1*self.bet_multiplier
        
        return 0*self.bet_multiplier # Player did not lose and did not stay
    
    def _check_loss(self):
        if self.player_value > 21:
            # Player went over -- check Ace edge case
            if self.replace_ace(self.player_cards):
                # Ace in hand. Swap to value 1 and continue
                self.player_value = self._compute_hand_value(self.player_cards)
                if self.debug_flag:
                    print(f"[PLAYER -- ACE-REPLACE] value: {self.player_value} hand: {self.player_cards}")
                return False # Did not fail
            else:
                # No Ace in had, game is done. 
                self.done=True
                if self.debug_flag:
                    print(f"[INFO] Player has {self.player_value}. Player loses :(")
                return True # Failed 
        return
    
    def _perform_action_hit(self):
        """ Do a HIT action
        
        """
        # Draw a card
        self.player_cards.append(self.deck.draw())

        # Recompute the player's hand value
        self.player_value = self._compute_hand_value(self.player_cards)

        if self.debug_flag:
            print(f"[PLAYER -- HIT] value: {self.player_value} hand: {self.player_cards}")

        return

    def _perform_action_final(self):
        """ Player chose to stay. Dealer plays it out.
        
        """
        if self.debug_flag:
            print("Executing dealer's actions")

        # Flip the hidden dealer card
        self.dealer_cards.append(self.dealer_hidden_card)
        self.dealer_value = self._compute_hand_value(self.dealer_cards)

        if self.debug_flag:
            print(f"[DEALER] value: {self.dealer_value} hand: {self.dealer_cards}")
            
        dealer_done = False
        while not dealer_done:

            if self.dealer_value > 21:

                # Handle Ace edge case
                if self.replace_ace(self.dealer_cards):
                    # Ace in hand. Swap to value 1 and continue
                    self.dealer_value = self._compute_hand_value(self.dealer_cards)
                    if self.debug_flag:
                        print(f"[DEALER] value: {self.dealer_value} hand: {self.dealer_cards}")
                else:
                    # No Ace in had, game is done. 
                    dealer_done = True

                    if self.debug_flag:
                        print(f"[INFO] Dealer has {self.dealer_value}. Player wins!")
                    return 1 # Player wins!

            # Criteria 1 -- STAND on 17 or more
            if self.dealer_value >= 17:
                dealer_done = True

                try:
                    if self.check_player_win():
                        if self.debug_flag:
                            print(f"[INFO] Player has {self.player_value}. Dealer has {self.dealer_value}. Player wins!")
                        return 1
                    else:
                        if self.debug_flag:
                            print(f"[INFO] Player has {self.player_value}. Dealer has {self.dealer_value}. Dealer wins!")
                        return -1
                except:
                    import pdb; pdb.set_trace()

            # Criteria 2 -- HIT on 16 or less
            if self.dealer_value <= 16:
                dealer_done = False
                self.dealer_cards.append(self.deck.draw())
                self.dealer_value = self._compute_hand_value(self.dealer_cards)

                if self.debug_flag:
                    print(f"[DEALER] value: {self.dealer_value} hand: {self.dealer_cards}")

        return


    def check_player_win(self):
        """ Checks if the player has won. """
        assert self.player_value <= 21
        assert self.dealer_value <= 21

        if self.player_value == 21:
            return True
        return self.player_value >= self.dealer_value
    

    def replace_ace(self, hand:list):
        """ If there is an ace in the hand, and the hand goes over 21, we need 
        to swap its value to 1. 
        
        """

        for card in hand:
            if (card.rank in ['ace']) and (card.value == 11):
                # Ace-11 found. Replace with 1.
                card.value = 1
                
                if self.debug_flag:
                    print(f"[INFO] Ace found in hand")
                return True
    
        if self.debug_flag:
            print(f"[INFO] Ace NOT found in hand")
        return False