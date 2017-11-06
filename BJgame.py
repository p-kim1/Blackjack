import blackjack
from cImage import *
import sys

def main():
    print("Welcome to Blackjack!")
    print("a) 5")
    print("b) 10")
    print("c) 20")
    creditChoice=input("Please choose your starting number of credits: ")
    
    #Ensures user will input a, b, or c
    validCredit=False
    while validCredit==False:
        if creditChoice=="a":
            validCredit=True
            numCredits=5
        elif creditChoice=="b":
            validCredit=True
            numCredits=10
        elif creditChoice=="c":
            validCredit=True
            numCredits=20
        else:
            creditChoice=input("Invalid choice. Please enter 'a', 'b', or 'c': ")

    print("---GAME START---")
    deck=blackjack.Deck()
    deckList=deck.getDeck()

    #Turns is an accumulator that makes it so that the image window is only made once, at Turns==0, instead of each new turn.
    Turns=0
                
    #As long as Loop==True, or until the player runs out of credits or the deck runs out of cards, the game will continue.
    Loop=True
    while Loop==True:
        if numCredits<=0:
            print("You have no more credits.")
            print("---GAME OVER---")
            Loop=False
        else:
            if len(deckList)<=4:
                print("Not enough cards left. You ended with "+str(numCredits)+" credits. Thank you for playing.")
                Loop=False
            else:
                playerHand=deck.hand()
                dealerHand=deck.hand()
                playerCardnames=deck.cardNames(playerHand)
                dealerCardnames=deck.cardNames(dealerHand)
                fileNamesP=deck.cardFilenames(playerCardnames)
                fileNamesD=deck.cardFilenames(dealerCardnames)

                #moveCount is an accumulator that ensures double down is only printed at moveCount==0, given the player has enough credits.
                moveCount=0
            
                print("CURRENT CREDITS: ",numCredits)
                playerBet=input("How much would you like to bet?: ")

                #Ensures user will input a number
                validBet=False
                while validBet==False:
                    if playerBet.isdigit()==True:
                        playerBet=int(playerBet)
                        if playerBet<=numCredits:
                            validBet=True
                            betDif=numCredits-playerBet
                        else:
                            playerBet=input("You do not have enough credits. Enter again: ")
                    else:
                        playerBet=input("Please enter a number: ")
                    
                    
                if Turns==0:
                    table=ImageWin("Blackjack",456,300)
                    deck.displayCards(fileNamesP,table,False,False)
                    deck.displayCards(fileNamesD,table,True,False)
                else:
                    deck.displayCards(fileNamesP,table,False,False)
                    deck.displayCards(fileNamesD,table,True,False)
            

                handValue=deck.value(playerHand)
                endplayerTurn=False
                surrender=False
                double=False
                #As long as endplayerTurn==False, the subsequent lines will loop. Events such as going over 21, hitting 21, or staying will make endplayerTurn=True, moveing the game on to the dealer's turn.
                while endplayerTurn==False:
                    if handValue!=21:
                        print("a) Hit")
                        print("b) Stay")
                        print("c) Surrender")
                        if moveCount==0 and betDif>=playerBet:
                            print("d) Double Down")
                            print("e) End Game")
                        elif moveCount==0 and betDif<playerBet:
                            print("d) End Game")
                        else:
                            print("d) End Game")
                        print("HAND VALUE: ",deck.value(playerHand),"| CURRENT CREDITS: ",betDif,"| BET: ",playerBet)
                    

                        playerTurn=input("What would you like to do?: ")

                        validMove=False
                        handValue=deck.value(playerHand)
                        while validMove==False and handValue!=21:
                            if playerTurn=="a":
                                if len(deckList)<1:
                                    validMove=True
                                    print("Not enough cards left. You ended with "+str(numCredits)+" credits. Thank you for playing.")
                                    Loop=False
                                    
                                else:
                                    validMove=True
                                    newHand=deck.hit(playerHand)
                                    handValue=deck.value(newHand)
                                    newHandnames=deck.cardNames(newHand)
                                    newFilenames=deck.cardFilenames(newHandnames)
                                    deck.displayCards(newFilenames,table,False,False)
                                    moveCount+=1
                                    if handValue>21:
                                        endplayerTurn=True
                                        numCredits-=playerBet
                                        print("HAND VALUE OVER 21")
                                        print("DEALER WINS")
                                        deck.displayCards(fileNamesD,table,True,True)
                                        deck.displayCards(playerCardnames,table,False,False)
                                        input("Press 'Enter' to continue...")
                                        deck.clearTable(table)


                            elif playerTurn=="b":
                                handValue=deck.value(playerHand)
                                validMove=True
                                endplayerTurn=True
                                moveCount+=1
                    

                            elif playerTurn=="c":
                                validMove=True
                                endplayerTurn=True
                                surrender=True
                                handValue=deck.value(playerHand)
                                moveCount+=1

                            elif playerTurn=="d" and moveCount==0 and betDif>=playerBet:
                                validMove=True
                                endplayerTurn=True
                                double=True
                                newHand=deck.hit(playerHand)
                                handValue=deck.value(newHand)
                                newHandnames=deck.cardNames(newHand)
                                newFilenames=deck.cardFilenames(newHandnames)
                                deck.displayCards(fileNamesD,table,True,True)
                                deck.displayCards(newFilenames,table,False,False)
                                print("HAND VALUE: ",deck.value(playerHand),"| CURRENT CREDITS AFTER DOUBLE: ",betDif-playerBet,"| DOUBLED BET: ",playerBet*2)
                                moveCount+=1

                                if handValue>21:
                                    numCredits-=(playerBet*2)
                                    print("HAND VALUE OVER 21")
                                    print("DEALER WINS")
                                    deck.displayCards(fileNamesD,table,True,True)
                                    deck.displayCards(playerCardnames,table,False,False)
                                    input("Press 'Enter' to continue...")
                                    deck.clearTable(table)
                                

                            elif playerTurn=="e" and moveCount==0:
                                sys.exit()
                            elif playerTurn=="d":
                                sys.exit()
                            else:
                                if moveCount==0 and betDif>=playerBet:
                                    playerTurn=input("Invalid choice. Please enter 'a', 'b', 'c', 'd', or 'e': ")
                                else:
                                    playerTurn=input("Invalid choice. Please enter 'a', 'b', or 'c', or 'd': ")

                    else:
                        deck.displayCards(fileNamesD,table,True,True)
                        endplayerTurn=True
                    

            dealerValue=deck.value(dealerHand)
            hitNum=0
            while endplayerTurn==True:
                if double==True:
                    playerBet*=2
                    double=False
                if handValue<21:
                    if surrender==False:
                        while dealerValue<17:
                            if len(deckList)<1:
                                print("Not enough cards left. You ended with "+str(numCredits)+" credits. Thank you for playing.")
                                Loop=False
                            else:
                                hitNum+=1
                                newCard=deck.hit(dealerHand)
                                dealerValue=deck.value(newCard)
                                newHandnames=deck.cardNames(newCard)
                                newFilenames=deck.cardFilenames(newHandnames)
                                deck.displayCards(newFilenames,table,True,False)
                        if hitNum>0:
                            print("THE DEALER HITS "+str(hitNum)+" TIME(S)")
                        else:
                            print("THE DEALER STAYS")
                        print("DEALER'S HAND VALUE: ",dealerValue)
                        #endplayerTurn is set to False at the end of these conditions in order to properly loop the game
                        if dealerValue>21:
                            print("DEALER OVER 21")
                            print("YOU WIN")
                            deck.displayCards(fileNamesD,table,True,True)
                            input("Press 'Enter' to continue...")
                            numCredits+=playerBet
                            endplayerTurn=False
                        elif dealerValue==21:
                            print("DEALER HAS 21")
                            print("DEALER WINS")
                            deck.displayCards(fileNamesD,table,True,True)
                            input("Press 'Enter' to continue...")
                            numCredits-=playerBet
                            endplayerTurn=False
                        elif dealerValue>handValue:
                            print("DEALER WINS")
                            deck.displayCards(fileNamesD,table,True,True)
                            input("Press 'Enter' to continue...")
                            numCredits-=playerBet
                            endplayerTurn=False  
                        elif dealerValue<handValue:
                            print("YOU WIN")
                            deck.displayCards(fileNamesD,table,True,True)
                            input("Press 'Enter' to continue...")
                            numCredits+=playerBet
                            endplayerTurn=False
                        elif dealerValue==handValue:
                            print("DRAW")
                            deck.displayCards(fileNamesD,table,True,True)
                            input("Press 'Enter' to continue...")
                            endplayerTurn=False
                    else:
                        print("YOU SURRENDERED")
                        if playerBet==1:
                            numCredits-=playerBet
                            surrender=False
                            endplayerTurn=False
                        else:
                            numCredits-=playerBet//2
                            surrender=False
                            endplayerTurn=False
                elif handValue==21:
                    print("YOU HAVE 21")
                    if dealerValue!=21:
                        input("Press 'Enter' to continue...")
                        print("YOU WIN")
                        numCredits+=playerBet
                        endplayerTurn=False
                    else:
                        input("Press 'Enter' to continue...")
                        print("DRAW")
                        endplayerTurn=False
                else:
                    endplayerTurn=False
                #Clears the image window after every turn
                deck.clearTable(table)
        Turns+=1
main()
