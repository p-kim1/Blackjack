import os
import random
from cImage import *

class Deck:
    def __init__(self):
    #Creates a list of dictionaries with the card names as the keys and corresponding numbers as the values. Also makes a list of the card names.
        self.__deck=[]
        self.__cardNames=[]
        letterList=["j","q","k","a","b"]
        for card in os.listdir("cards/"):
            cardname=card[:-4]
            self.__cardNames.append(cardname)
            if cardname[0] not in letterList:
                self.__deck.append({cardname:int(cardname[:-1])})
            elif cardname[0]=="j" or cardname[0]=="q" or cardname[0]=="k":
                self.__deck.append({cardname:10})
            elif cardname[0]=="a":
                self.__deck.append({cardname:[1,11]})
            else:
            #This is to account for the backs of the cards, which shouldn't be appended to the list
                pass
    
    def getDeck(self):
    #Returns the deck
        return self.__deck


    def hand(self):
    #Creates the player's and dealer's hands at the beginning of the game
        self.__hand=[]
        for i in range(2):
            card=random.choice(self.__deck)
            self.__hand.append(card)
            self.__deck.pop(self.__deck.index(card))
        return self.__hand
        

    def value(self,hand):
    #Returns the sum of all the cards in the hand
        handSum=[]
        aceList=["as","ah","ac","ad"]
        for numCards in range(len(hand)):
            for card in self.__cardNames:
                currentCard=hand[numCards]
                if card in currentCard and card not in aceList:
                    handSum.append(currentCard[card])
                elif card in currentCard and card in aceList:
                    ace=Deck.aceValue(self,hand,sum(handSum),currentCard,card)
                    handSum.append(ace)
        if sum(handSum)>21 and 11 in handSum:
            idx11=handSum.index(11)
            handSum[idx11]=1
        return sum(handSum)


    def cardNames(self,hand):
    #Returns a list of the names of the cards in the hand
        cards=[]
        for numCards in range(len(hand)):
            for card in self.__cardNames:
                if card in hand[numCards] and card not in cards:
                    cards.append(card)
        return cards


    def aceValue(self,hand,handSum,currentCard,card):
    #Sets the ace value as either 1 or 11 based on the hand value
        a11=handSum+currentCard[card][1]
        a1=handSum+currentCard[card][0]
        if a11<=21:
            return 11
        elif a11>21:
            return 1
        else:
            return 11


    def hit(self,hand):
    #Adds a card to the hand and removes it from the deck
        newCard=random.choice(self.__deck)
        hand.append(newCard)
        self.__deck.pop(self.__deck.index(newCard))
        return hand


    def cardFilenames(self,cardNames):
    #Creates a list of filenames by adding ".gif" to the cards in the cardNames list
        fileNames=[]
        for card in cardNames:
            if card+".gif" in os.listdir("cards/"):
                cardFile=card+".gif"
                fileNames.append(cardFile)
        return fileNames
        

    def displayCards(self,cardFileNames,table,isDealer,flip):
    #Draws the cards in the cardFileNames list and checks if it is the dealer's hand. If so, then the first card is drawn as the back of the card until the parameter "flip" is True. Otehrwise, the player's cards are drawn.
        cardOffSet=0
        for card in cardFileNames:
            for root, dirs, files in os.walk("cards/"):
                for file in files:
                    if file==card and isDealer==False:
                        cardImage=FileImage(os.path.join(root, file))
                        cardImage.setPosition(cardOffSet,200)
                        cardImage.draw(table)
                    elif file==card and isDealer==True:
                        if card==cardFileNames[0] and flip==False:
                            if "h" in card or "d" in card:
                                file="br.gif"
                                cardImage=FileImage(os.path.join(root,file))
                                cardImage.setPosition(cardOffSet,0)
                                cardImage.draw(table)
                            elif "c" in card or "s" in card:
                                file="bb.gif"
                                cardImage=FileImage(os.path.join(root,file))
                                cardImage.setPosition(cardOffSet,0)
                                cardImage.draw(table)
                        else:
                            cardImage=FileImage(os.path.join(root, file))
                            cardImage.setPosition(cardOffSet,0)
                            cardImage.draw(table)
                cardOffSet+=76

    def clearTable(self,table):
    #Clears the table after each turn by drawing gray over the entire window
        pixel=Pixel(217,217,217)
        emptyTable=EmptyImage(456,300)
        for row in range(456):
            for col in range(300):
                emptyTable.setPixel(row,col,pixel)
        emptyTable.draw(table)
