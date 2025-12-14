'''
BlackJack Card Game - Terminal Based - Coded in Python
Coded by Shahroz 'Sz' Khan
'''
'''
to do:
only if split calc left
'''

#import Shuffle element
import random
import os
import time
#declare global elements
suits=('Spades','Diamonds','Clubs','Hearts')
ranks=('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values={'Two':[2,2],'Three':[3,3],'Four':[4,4],'Five':[5,5],'Six':[6,6],'Seven':[7,7],'Eight':[8,8],'Nine':[9,9],'Ten':[10,10],'Jack':[10,10],'Queen':[10,10],'King':[10,10],'Ace':[1,11]}
suits_face={'Spades':'♠','Diamonds':'♦','Clubs':'♣','Hearts':'♥'}
ranks_face={'Two':'2 ','Three':'3 ','Four':'4 ','Five':'5 ','Six':'6 ','Seven':'7 ','Eight':'8 ','Nine':'9 ','Ten':'10','Jack':'j ','Queen':'Q ','King':'K ','Ace':'A '}


#card class - makes card
class Card():
    def __init__(self,rank,suit):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]
        self.suitsymb=suits_face[suit] #for suit shape/symbol string
        self.ranksymb=ranks_face[rank] #for rank shape/symbol string

    def __str__(self):
        return f'{self.rank} of {self.suit}'

#deck class - makes, shuffles, and deals deck
class Deck():
    def __init__(self):
        self.created_deck=[]
        for suit in suits:
            for rank in ranks:
                created_card=Card(rank,suit)
                self.created_deck.append(created_card)

    def shuffle(self):
        random.shuffle(self.created_deck)

    def deal_one(self):
        return self.created_deck.pop(0)

#player class - hold player name,deck,his stake, his winning,removes/adds card and money
class Player():
    def __init__(self,name,cash=0):
        self.name=name
        self.own_deck=[]
        self.atstake=0
        self.wins=0
        self.totalcash=cash
    
    def remove_card(self):
        return self.own_deck.pop()

    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.own_deck.extend(new_cards) #for multiple cards
        else:
            self.own_deck.append(new_cards) #for single card

    def take_bet(self,amount):
        self.atstake+=amount
        self.wins+=amount
        self.totalcash-=amount

    def add_bet(self):
        self.wins+=self.atstake

    def remove_bet(self):
        self.wins-=self.atstake

    def add_win(self):
        self.totalcash+=self.wins

    def __str__(self):
        return f'\n{self.name} won {self.wins}.'

#display class - contains all table ui
class Table():

    def single_card(self,rs,ss):
        print('     _________' )
        print(f'    |{rs}       |')
        print('    |         |')
        print('    |         |')
        print(f'    |    {ss}    |')
        print('    |         |')
        print('    |         |')
        print(f'    |       {rs}|')
        print('     ¯¯¯¯¯¯¯¯¯\n')

    def dealer_after_deal(self,drs,dss):
        print('\n═════════════════════════════════════════════════')
        print("             **Sz' Blackjack Table**\n")
        print("\n                 Dealer's Hand\n")
        print('                ______ _________ ' )
        print(f'               |    _ |{drs}       |')
        print('               | ¯ ||||         |')
        print('               |  ¯||||         |')
        print(f'               | ¯ ||||    {dss}    |')
        print('               |  ¯||||         |')
        print('               | ¯ ||||         |')
        print(f'               |SZ  ¯ |       {drs}|')
        print('                ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print('\n══════════════════════════════════════════════════\n')

    def player_after_deal(self,prs,pss,prs2,pss2):
        print('                ______ _________ ' )
        print(f'               |{prs2}    |{prs}       |')
        print('               |      |         |')
        print('               |      |         |')
        print(f'               |     {pss2}|    {pss}    |')
        print('               |      |         |')
        print('               |      |         |')
        print(f'               |      |       {prs}|')
        print('                ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print("\n                  Your Current hand")
        print('\n═════════════════════════════════════════════════')

    def dealer_show(self,drs,dss,drs2,dss2):
        print('\n═════════════════════════════════════════════════')
        print("             **Sz' Blackjack Table**\n")
        print("\n                  Dealer's Hand\n")
        print('                 ______ _________ ' )
        print(f'                |{drs2}    |{drs}       |')
        print('                |      |         |')
        print('                |      |         |')
        print(f'                |     {dss2}|    {dss}    |')
        print('                |      |         |')
        print('                |      |         |')
        print(f'                |      |       {drs}|')
        print('                 ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print('\n══════════════════════════════════════════════════\n')

    def dealer_hit(self,drs,dss,drs2,dss2,drs3,dss3):
        print('\n═════════════════════════════════════════════════')
        print("             **Sz' Blackjack Table**\n")
        print(f"\n                    Dealer's Hand\n")
        print('          _________        ______ _________ ' )
        print(f'         |{drs3}       |      |{drs2}    |{drs}       |')
        print('         |         |      |      |         |')
        print('         |         |      |      |         |')
        print(f'         |    {dss3}    |      |     {dss2}|    {dss}    |')
        print('         |         |      |      |         |')
        print('         |         |      |      |         |')
        print(f'         |       {drs3}|      |      |       {drs}|')
        print('          ¯¯¯¯¯¯¯¯¯        ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print('\n══════════════════════════════════════════════════\n')

    def player_hit(self,prs,pss,prs2,pss2,prs3,pss3):
        print('             ______ ______ _________ ' )
        print(f'            |{prs3}    |{prs2}    |{prs}       |')
        print('            |      |      |         |')
        print('            |      |      |         |')
        print(f'            |     {pss3}|     {pss2}|    {pss}    |')
        print('            |      |      |         |')
        print('            |      |      |         |')
        print(f'            |      |      |       {prs}|')
        print('             ¯¯¯¯¯¯ ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print("\n                  Your Current hand")
        print('\n═════════════════════════════════════════════════')

    def player_hit2(self,prs,pss,prs2,pss2,prs3,pss3,prs4,pss4,):
        print('         _________     ______ ______ _________ ' )
        print(f'        |{prs4}       |   |{prs3}    |{prs2}    |{prs}       |')
        print('        |         |   |      |      |         |')
        print('        |         |   |      |      |         |')
        print(f'        |    {pss4}    |   |     {pss3}|     {pss2}|    {pss}    |')
        print('        |         |   |      |      |         |')
        print('        |         |   |      |      |         |')
        print(f'        |       {prs4}|   |      |      |       {prs}|')
        print('         ¯¯¯¯¯¯¯¯¯     ¯¯¯¯¯¯ ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print("\n                   Your Current hand")
        print('\n═════════════════════════════════════════════════')

    def player_hit3(self,prs,pss,prs2,pss2,prs3,pss3,prs4,pss4,prs5,pss5):
        print('   _____ _________     ______ ______ _________ ' )
        print(f'  |{prs5}   |{prs4}       |   |{prs3}    |{prs2}    |{prs}       |')
        print('  |     |         |   |      |      |         |')
        print('  |     |         |   |      |      |         |')
        print(f'  |    {pss5}|    {pss4}    |   |     {pss3}|     {pss2}|    {pss}    |')
        print('  |     |         |   |      |      |         |')
        print('  |     |         |   |      |      |         |')
        print(f'  |     |       {prs4}|   |      |      |       {prs}|')
        print('   ¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯     ¯¯¯¯¯¯ ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print("\n                   Your Current hand")
        print('\n═════════════════════════════════════════════════')

    def player_split(self,prs,pss,prs2,pss2):
        print('                ______ _________ ' )
        print(f'               |{prs2}    |{prs}       |')
        print('               |      |         |')
        print('               |      |         |')
        print(f'               |     {pss2}|    {pss}    |')
        print('               |      |         |')
        print('               |      |         |')
        print(f'               |      |       {prs}|')
        print('                ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print("\n                  Your Split hand")
        print('\n═════════════════════════════════════════════════')

    def player_split_hit(self,prs,pss,prs2,pss2,prs3,pss3):
        print('             ______ ______ _________ ' )
        print(f'            |{prs3}    |{prs2}    |{prs}       |')
        print('            |      |      |         |')
        print('            |      |      |         |')
        print(f'            |     {pss3}|     {pss2}|    {pss}    |')
        print('            |      |      |         |')
        print('            |      |      |         |')
        print(f'            |      |      |       {prs}|')
        print('             ¯¯¯¯¯¯ ¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯ ')
        print("\n                  Your Split hand")
        print('\n═════════════════════════════════════════════════')

#game functions
def clear_term(): # clears terminal
    os.system('CLS')

def pause_code(secs): #pauses code - input is in secs
    time.sleep(secs)

def play_again(): #for play again func
    pg='null'
    while pg not in ['Y','N']:
        pg=input('\nDo you want to play again? y or n: ').upper()
        if pg not in ['Y','N']:
            print('INVALID INPUT! Enter y or n?')
    if pg!='Y':
        return False
    else:
        return True
#game setup and intro
print("\n\t\t\t>>>> WELCOME TO SZ' BLACKJACK CARD GAME <<<<\n")
print(">> Check out https://bicyclecards.com/how-to-play/blackjack/ for rules before playing.")
playername=input("\n> Please Enter Your Name: ")
playercash=int(input('\n> Enter Total Worth of Your Chips: '))
print(f'\n>> NOTICE: Player {playername} will be playing against The Dealer with {playercash} worth chips.\n')
rounds=0
#while the players wants to play
game_on=True
while game_on:
    clear_term()
    rounds+=1
    print(f'\n\t\t\t>>> Starting Round {rounds}! <<<\n')
    pause_code(1) #pausing code
    game_over=False
    win=False
    player1=Player(playername,playercash)
    dealer=Player('Dealer')
    can_pay=False
    while can_pay==False:
        bet=int(input('\n> Set Bet: '))
        if type(bet)!=type(1):
            print('>> INVALID INPUT! Enter a amount in numbers.')
        if bet>player1.totalcash:
            print(">> NOTICE: You Don't Have Enough Chips")
            pause_code(1)
            ask0='null'
            while ask0 not in ['Y','N']:
                ask0=input('Do You Want To Exit The Game? y or n: ').upper()
                if ask0 not in ['Y','N']:
                    print('>> INVALID INPUT! Enter y or n.')
            if ask0=='Y':
                game_over=True
                game_on=False
                win=True
                break
        else:
            player1.take_bet(bet)
            print(f'\n>> {player1.atstake} Staked\n')
            can_pay==True
            break
    clear_term()
    print('Setting Up The Table.')
    new_table=Table()
    pause_code(1)
    clear_term()
    print('Shuffling The Cards..')
    #removibg previous cards
    new_deck=Deck()
    new_deck.shuffle()
    pause_code(1)
    clear_term()
    print('Dealing The Cards...')
    for i in range(2):
        player1.add_cards(new_deck.deal_one())
        dealer.add_cards(new_deck.deal_one())
    pause_code(1)
    clear_term()
    print('Cards Shuffled & dealt...')
    pause_code(1)
    clear_term()
    #displaying the after deal tables
    new_table.dealer_after_deal(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb)
    new_table.player_after_deal(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb)
    #check immediate win situation
    while win==False:
        if (player1.own_deck[0].rank == 'Ace' and player1.own_deck[1].value[0]==10) or (player1.own_deck[0].value[0]==10 and player1.own_deck[1].rank=='Ace'):
            pause_code(2)
            clear_term()
            new_table.dealer_show(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb, dealer.own_deck[-2].ranksymb, dealer.own_deck[-2].suitsymb)
            new_table.player_after_deal(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb)
            print(f'\n>>>> {player1.name.upper()} HAS BLACKJACK! <<<<\n')
            #check  if dealer has a blackjack too
            if (dealer.own_deck[0].rank == 'Ace' and dealer.own_deck[1].value[0]==10) or (dealer.own_deck[0].value[0]==10 and dealer.own_deck[1].rank=='Ace'):
                pause_code(2)
                clear_term()
                new_table.dealer_show(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb, dealer.own_deck[-2].ranksymb, dealer.own_deck[-2].suitsymb)
                new_table.player_after_deal(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb)
                print('\n>>>> DEALER ALSO HAS BLACKJACK! <<<<\n')
                print(f'>> NOTICE: PUSH Terms Applied, stakes given back to players')
            else:
                player1.take_bet(bet*1.5)
                player1.add_bet()
                print(f'>> 3 to 2 payout give to {player1.name}')
                print(f'\n>> {player1.name.upper()} WON!\n')
            print('\n>>> GAMEOVER <<<\n')
            win=True
            break
        '''
        #checking split and asking player if he wants to split
        split=True
        while split:
            if player1.own_deck[0].rank==player1.own_deck[1].rank:
                if player1.own_deck[0].rank==player1.own_deck[1].rank=='Ace':
                    print('>> You Got Two Aces!')
                    print("You Can't split your Aces?")
                    split=False
                    break
                else:
                    ask1='null'
                    while ask1 not in ['Y','N']:
                        ask1=input('\n> Do you want to split your cards? y or n: ').upper()
                        if ask1 not in ['Y','N']:
                            print('\n>> WRONG INPUT! Enter y or n')
                    if ask1=='N':
                        split=False
                        break
                    else: #player wants to split cards - can make better by making only one split hand and og hand
                        #adding the same bet for the other hand
                        #fix bets
                        player1.bets(bet)
                        dealer.remove_bet()
                        playersplit1=Player('Split1')
                        playersplit2=Player('Split2')
                        #split the cards
                        playersplit1.add_cards(player1.remove_card())
                        playersplit1.add_cards(new_deck.deal_one())
                        playersplit2.add_cards(player1.remove_card())
                        playersplit2.add_cards(new_deck.deal_one())
                        #showing the cards in ui
                        new_table.player_split(playersplit1.own_deck[0].rank,playersplit1.own_deck[0].suit,playersplit1.own_deck[1].rank,playersplit1.own_deck[1].suit)
                        new_table.player_split(playersplit2.own_deck[0].rank,playersplit2.own_deck[0].suit,playersplit1.own_deck[1].rank,playersplit1.own_deck[1].suit)
                        #loop for hitting those split hands
                        split_hit=True
                        while split_hit:
                            ask3='null'
                            while ask3 not in ['Y','N']:
                                ask3=input('\n> Do you want to hit any of your split hands? y or n : ').upper()
                                if ask3 not in ['Y','N']:
                                    print('\n>> INVALID INPUT! Enter y or n')
                            if ask3=='Y':
                                ask4='null'
                                while ask4 not in ['1ST','2ND','BOTH']:
                                    try:
                                        ask4=input('\n> Which hand do you want to hit: 1st, 2nd or Both: ').upper()
                                    except:
                                        print('\n>> INVALID INPUT! Enter 1st , 2nd,or Both')
                                if ask4=='1ST': #only 1st
                                    playersplit1.add_cards(new_deck.deal_one())
                                    new_table.player_split_hit(playersplit1.own_deck[0].rank,playersplit1.own_deck[0].suit,playersplit1.own_deck[1].rank,playersplit1.own_deck[1].suit,playersplit1.own_deck[2].rank,playersplit1.own_deck[2].suit)
                                elif ask4=='2ND': #only 2nd
                                    playersplit2.add_cards(new_deck.deal_one())

                                    new_table.player_split_hit(playersplit2.own_deck[0].rank,playersplit2.own_deck[0].suit,playersplit2.own_deck[1].rank,playersplit2.own_deck[1].suit,playersplit2.own_deck[2].rank,playersplit2.own_deck[2].suit)
                                else: #player wants to hit both split hands
                                    playersplit1.add_cards(new_deck.deal_one())
                                    #add single card and card name 
                                    new_table.player_split_hit(playersplit1.own_deck[0].rank,playersplit1.own_deck[0].suit,playersplit1.own_deck[1].rank,playersplit1.own_deck[1].suit,playersplit1.own_deck[2].rank,playersplit1.own_deck[2].suit)
                                    playersplit2.add_cards(new_deck.deal_one())
                                    #add single card and card name
                                    new_table.player_split_hit(playersplit2.own_deck[0].rank,playersplit2.own_deck[0].suit,playersplit2.own_deck[1].rank,playersplit2.own_deck[1].suit,playersplit2.own_deck[2].rank,playersplit2.own_deck[2].suit)      
                            else: #player doesnt want to hit anymore
                                split_hit=False
                                break
                        #might need to add and diff show dealer and calc block
                        break            
            else: #dealt cards are not same
                split=False           
        '''
        #ask if player wants to hit the og hand?
        hit=0
        ace_value_set=False
        player_hit=True
        while player_hit:
            #add here the player value check
            total_player_value=0
            higher_player_value=0
            lower_player_value=0
            for i in player1.own_deck:
                higher_player_value+=i.value[1]
                lower_player_value+=i.value[0]
            if higher_player_value==lower_player_value:
                total_player_value=higher_player_value
            elif higher_player_value!=lower_player_value:
                total_ace_value=0
                while ace_value_set==False:
                    ace_value=int(input('What value do you want to set for your ace? 1 or 11: '))
                    ace_value_set=True
                for i in player1.own_deck:
                    if i.rank=='Ace':
                        total_ace_value+=ace_value
                    else:
                        continue
                total_nonace_value=0
                for i in player1.own_deck:
                    if i.rank=='Ace':
                        continue
                    else:
                        total_nonace_value+=i.value[0]
                total_player_value=total_ace_value+total_nonace_value
            #check if that total player card value went above 21
            if total_player_value>21:
                print(f'\n{player1.name} card value has crossed 21.')
                print('\n>>> BUST! <<<\n')
                pause_code(2)
                player_hit=False
                break   
            pause_code(1)
            ask_hit='null'
            while ask_hit not in ['Y','N']:
                ask_hit=input('\n> Do You Want To Hit? y or n: ').upper()
                if ask_hit not in ['Y','N']:
                    print('INVALID INPUT! Enter y or n.')
            if ask_hit=='N':
                player_hit=False
            else:
                hit+=1
                player1.add_cards(new_deck.deal_one())
                print(f'\n>> New Card : {player1.own_deck[-1]}')
                new_table.single_card(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb)
                player_hit=True
        #add show cards here dealer show and player hits shows
        pause_code(2)
        clear_term()
        new_table.dealer_show(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb, dealer.own_deck[-2].ranksymb, dealer.own_deck[-2].suitsymb)
        if hit==0:
            new_table.player_after_deal(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb)
        elif hit==1:
            new_table.player_hit(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb, player1.own_deck[-3].ranksymb, player1.own_deck[-3].suitsymb)
        elif hit==2:
            new_table.player_hit2(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb, player1.own_deck[-3].ranksymb, player1.own_deck[-3].suitsymb, player1.own_deck[-4].ranksymb, player1.own_deck[-4].suitsymb)
        elif hit==3:
            new_table.player_hit3(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb, player1.own_deck[-3].ranksymb, player1.own_deck[-3].suitsymb, player1.own_deck[-4].ranksymb, player1.own_deck[-4].suitsymb, player1.own_deck[-5].ranksymb, player1.own_deck[-5].suitsymb)
        dealer_card_value=0
        if (dealer.own_deck[0].rank and dealer.own_deck[1].rank) != 'Ace':
            dealer_card_value=(dealer.own_deck[0].value[0]+dealer.own_deck[1].value[0])
            dealer_hit=False
            if dealer_card_value<=16:
                dealer.add_cards(new_deck.deal_one())
                print("\n>> Dealer's Total Card Value is Less Than 16\n")
                pause_code(1)
                print(f'\n>> New Card : {dealer.own_deck[-1]}')
                new_table.single_card(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb)
                dealer_hit=True
        elif (dealer.own_deck[0].rank or dealer.own_deck[1].rank) != 'Ace':
            if (dealer.own_deck[0].rank == 'Ace' and dealer.own_deck[1].value[0]==10) or (dealer.own_deck[0].value[0]==10 and dealer.own_deck[1].rank=='Ace'):
                pause_code(1)
                print('\n>>> DEALER GOT BLACKJACK! <<<\n')
                player1.remove_bet()
                print('>> Stakes taken By Dealer')
                print('>>> GAMEOVER <<<\n')
                game_over=True
                win=True
                break
            higher_dealer_value=0
            lower_dealer_value=0
            for i in dealer.own_deck:
                higher_dealer_value+=i.value[1]
                lower_dealer_value+=i.value[0]
            if (lower_dealer_value and higher_dealer_value)<=16:
                dealer.add_cards(new_deck.deal_one())
                print("\n>> Dealer's Total Card Value is Less Than 16\n")
                print(f'\n>> New Card : {dealer.own_deck[-1]}')
                pause_code(1)
                new_table.single_card(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb)
                dealer_hit=True
            else:
                dealer_hit=False
        if dealer_hit==True:
            pause_code(2)
            clear_term()
            new_table.dealer_hit(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb, dealer.own_deck[-2].ranksymb, dealer.own_deck[-2].suitsymb, dealer.own_deck[-3].ranksymb, dealer.own_deck[-3].suitsymb)
        elif dealer_hit==False:
            pause_code(2)
            clear_term()
            new_table.dealer_show(dealer.own_deck[-1].ranksymb, dealer.own_deck[-1].suitsymb, dealer.own_deck[-2].ranksymb, dealer.own_deck[-2].suitsymb)
        if hit==0:
            new_table.player_after_deal(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb)
        elif hit==1:
            new_table.player_hit(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb, player1.own_deck[-3].ranksymb, player1.own_deck[-3].suitsymb)
        elif hit==2:
            new_table.player_hit2(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb, player1.own_deck[-3].ranksymb, player1.own_deck[-3].suitsymb, player1.own_deck[-4].ranksymb, player1.own_deck[-4].suitsymb)
        elif hit==3:
            new_table.player_hit3(player1.own_deck[-1].ranksymb, player1.own_deck[-1].suitsymb, player1.own_deck[-2].ranksymb, player1.own_deck[-2].suitsymb, player1.own_deck[-3].ranksymb, player1.own_deck[-3].suitsymb, player1.own_deck[-4].ranksymb, player1.own_deck[-4].suitsymb, player1.own_deck[-5].ranksymb, player1.own_deck[-5].suitsymb)
        #check total value of dealer
        total_dealer_value=0
        higher_dealer_value=0
        lower_dealer_value=0
        for i in dealer.own_deck:
            higher_dealer_value+=i.value[1]
            lower_dealer_value+=i.value[0]
        if higher_player_value!=lower_player_value:
            if higher_dealer_value>lower_dealer_value:
                total_dealer_value=lower_dealer_value
            else:
                total_dealer_value=higher_dealer_value
        else:
            total_dealer_value=higher_dealer_value
        pause_code(2)
        while total_player_value>21:
            if total_dealer_value>21:
                pause_code(1)
                print("\nDealer's Total Card Value Crossed 21 Too")
                print('\n>>> DEALER BUST! <<<\n')
                print(f"\n>> {player1.name} Wins Round {rounds}\n")
                print('>> GAMEOVER')
                win=True
                game_over=True
                break
        if total_dealer_value>21:
            pause_code(1)
            print('\n>>> DEALER BUST! <<<\n')
            print(f"\n>> {player1.name} Wins Round {rounds}\n")
            player1.add_bet()
            print('>> GAMEOVER')
            win=True
            game_over=True
            break
        #checking win situtions
        while game_over==False:
            if total_dealer_value == total_player_value:
                pause_code(1)
                print('\n>> Push has been Declared, i.e TIE')
                print("\n>> Player's Stake Paid Back")
                print('>> GAMEOVER')
                game_over=True
                win=True
                break
            elif total_dealer_value < total_player_value:
                pause_code(1)
                print(f">> {player1.name}'s Total Card Value is Closer To 21")
                print(f'\n>> {player1.name.upper()} WON!\n')
                player1.add_bet()
                print('>> GAMEOVER')
                game_over=True
                win=True
                break
            else:
                print(">> Dealer's Total Card Value is Closer To 21.")
                print(f'\n>> DEALER WON!\n')
                player1.remove_bet()
                win=True
                game_over=True
                break
    #asking the player if he still wants to play.
    player1.add_win()
    game_on=play_again()
#if the loop gets cut off
pause_code(1)
clear_term()
print(f'\n>> Total Rounds Played - {rounds}')
print(f'\n>>NOTICE: {player1.name} won {player1.wins} and Walked out with {player1.totalcash} worth chips.')
print('\n\t\t>>>> GAME OVER! <<<<')
print('\n\t  >>>> THANK-YOU FOR PLAYING! <<<<\n')