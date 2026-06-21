import collections
import random 

Card = collections.namedtuple('Card',['rank','suit'])

class blackjack_deck:
    ranks = [str(n) for n in range (2,11)] + list ('JQKA')
    suits = 'Spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self.cards = [Card(rank,suit) for suit in self.suits
                      for rank in self.ranks]
        self.shuffle()
        
    def __len__(self): 
        return len (self.cards) 
    
    def __getitem__(self,position):
        return self.cards[position]

    def shuffle(self):
        random.shuffle(self.cards)
        
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        if len(self.cards) == 0:
            raise ValueError("All cards have been dealt")
        return self.cards.pop() 
    
    