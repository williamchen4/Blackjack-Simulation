import random
import numpy as np
import matplotlib.pyplot as plt

def createDeck():
    ''' Returns a non-shuffled 52-card deck ''' 
    deck = [11] * 4             # add four aces
    for num in range(2, 11):    # add four copies of 2 - 10
        deck += [num] * 4
    deck += [10] * 12           # add four jacks, queens, kings
    return deck

def drawCard(deck, version):
    ''' Returns card from deck '''
    # version 1 is infinite deck, version 2 is single deck
    return random.choice(deck) if version == 1 else deck.pop(0)

def turn(deck, hand, policy, version):
    ''' Draw cards given policy '''
    if(sum(hand) == 21):
        return 21
    while(policy(hand)):
        hand.append(drawCard(deck, version))
        if(sum(hand) == 21):
            break
        elif(sum(hand) > 21 and 11 in hand):
            hand[hand.index(11)] = 1
        elif(sum(hand) > 21):
            break
    return sum(hand)

def playGame(playerPolicy, version):
    ''' Play one blackjack game '''
    # initialize deck
    deck = createDeck()
    random.shuffle(deck)
    dealerPolicy = lambda dealerHand: sum(dealerHand) < 17

    # initialize hands
    playerHand = []
    dealerHand = []
    playerHand.append(drawCard(deck, version))
    playerHand.append(drawCard(deck, version))
    dealerHand.append(drawCard(deck, version))
    dealerHand.append(drawCard(deck, version))

    # player takes turn
    playerResult = turn(deck, playerHand, playerPolicy, version)
    if playerResult == 21:  # player won
        return 100
    elif playerResult > 21: # player lost
        return -100
    else:
        dealerResult = turn(deck, dealerHand, dealerPolicy, version)
        if dealerResult > 21:   # dealer lost
            return 1
        return playerResult - dealerResult


def simulate():
    ''' Monte Carlo simulation using defined policies'''

    # define policies
    policy1 = lambda playerHand: not(sum(playerHand) >= 17)
    policy2 = lambda playerHand: not(sum(playerHand) >= 17 and 11 not in playerHand)
    policy3 = lambda playerHand: False if sum(playerHand) >= 17 and 11 not in playerHand else random.randint(0,1)==0 if     sum(playerHand) >= 17 else True
    policy4 = lambda playerHand: False
    policy5 = lambda playerHand: sum(playerHand) <= 15
    policy6 = lambda playerHand: sum(playerHand) <= 16 and 11 in playerHand
    policies = [policy1, policy2, policy3, policy4, policy5, policy6]

    iterations = 50000
    winRates, lossRates, drawRates, bustRates, blackjackRates, overallBlackjack = [[], []], [[], []], [[], []], [[], []], [[], []], [[], []]

    for version in [1, 2]:
        for policy in range(len(policies)):
            #print('------------------- ')
            #print('| Policy %d' % (policy+1), end = ' ')
            #print('Infinite Deck' if version == 1 else 'Single Deck')
            numWon, numLoss, numDraw = 0, 0, 0
            numBust = 0
            numBlackjack = 0

            for _ in range(iterations):
                result = playGame(policies[policy], version)
                if result > 0:
                    numWon += 1
                    if result == 100:
                        numBlackjack += 1
                elif result < 0:
                    numLoss += 1
                    if result == -100:
                        numBust += 1
                else:
                    numDraw += 1

            winRates[version - 1].append(numWon / iterations * 100)
            lossRates[version - 1].append(numLoss / iterations * 100)
            drawRates[version - 1].append(numDraw / iterations * 100)
            bustRates[version - 1].append(numBust / numLoss * 100)
            blackjackRates[version - 1].append(numBlackjack / numWon * 100)
            overallBlackjack[version-1].append(numBlackjack / iterations * 100)

            print('Policy %d won %.2f%% of the time' % (policy + 1, winRates[version-1][-1]))

    print(winRates[0].index(max(winRates[0]))+1, winRates[1].index(max(winRates[1]))+1)
    print(lossRates[0].index(max(lossRates[0]))+1, lossRates[1].index(max(lossRates[1]))+1)
    print(drawRates[0].index(max(drawRates[0]))+1, drawRates[1].index(max(drawRates[1]))+1)
    
    # plot win/loss/draw rates
    policyNumber = range(1, 7)
    _, (ax1, ax2) = plt.subplots(1, 2)

    winBar = ax1.bar(policyNumber, winRates[0], color='#0d9930')
    lossBar = ax1.bar(policyNumber, lossRates[0], bottom = winRates[0], color='#e22222')
    drawBar = ax1.bar(policyNumber, drawRates[0], bottom = np.add(winRates[0], lossRates[0]).tolist(), color='#595b59')
    ax1.set_ylim([0, 100])
    ax1.set_xlabel('Policy')
    ax1.set_ylabel('Percentage')
    ax1.set_title('Infinite Deck')
    for i in policyNumber:
        ax1.text(i-0.25, 20, round(winRates[0][i-1],2))
        ax1.text(i-0.25, 70, round(lossRates[0][i-1],2))
        ax1.text(i-0.25, 96, round(drawRates[0][i-1],2))

    ax2.bar(policyNumber, winRates[1], color='#0d9930')
    ax2.bar(policyNumber, lossRates[1], bottom = winRates[1], color='#e22222')
    ax2.bar(policyNumber, drawRates[1], bottom = np.add(winRates[1], lossRates[1]).tolist(), color='#595b59')
    ax2.set_ylim([0, 100])
    ax2.set_xlabel('Policy')
    ax2.set_ylabel('Percentage')
    ax2.set_title('Single Deck')
    for i in policyNumber:
        ax2.text(i-0.25, 20, round(winRates[1][i-1],2))
        ax2.text(i-0.25, 70, round(lossRates[1][i-1],2))
        ax2.text(i-0.25, 96, round(drawRates[1][i-1],2))

    plt.legend((winBar[0], lossBar[0], drawBar[0]), ('Win', 'Loss', 'Draw'))

    # plot bust
    _, (ax3, ax4) = plt.subplots(1, 2)
    ax3.bar(policyNumber, bustRates[0], color='#8A2BE2')
    ax3.set_ylim([0, 100])
    ax3.set_xlabel('Policy')
    ax3.set_ylabel('Percentage Bust')
    ax3.set_title('Infinite Deck Losses')
    for i in policyNumber:
        ax3.text(i-0.25, round(bustRates[0][i-1],2) + 2, round(bustRates[0][i-1],2))

    ax4.bar(policyNumber, bustRates[1], color='#8A2BE2')
    ax4.set_ylim([0, 100])
    ax4.set_xlabel('Policy')
    ax4.set_ylabel('Percentage Bust')
    ax4.set_title('Single Deck Losses')
    for i in policyNumber:
        ax4.text(i-0.25, round(bustRates[1][i-1],2) + 2, round(bustRates[1][i-1],2))

    # plot blackjack
    _, (ax5, ax6) = plt.subplots(1, 2)
    ax5.bar(policyNumber, blackjackRates[0], color='#1c6bea')
    ax5.set_ylim([0, 100])
    ax5.set_xlabel('Policy')
    ax5.set_ylabel('Percentage Blackjack')
    ax5.set_title('Infinite Deck Wins')
    for i in policyNumber:
        ax5.text(i-0.25, round(blackjackRates[0][i-1],2) + 2, round(blackjackRates[0][i-1],2))

    ax6.bar(policyNumber, blackjackRates[1], color='#1c6bea')
    ax6.set_ylim([0, 100])
    ax6.set_xlabel('Policy')
    ax6.set_ylabel('Percentage Blackjack')
    ax6.set_title('Single Deck Wins')
    for i in policyNumber:
        ax6.text(i-0.25, round(blackjackRates[1][i-1],2) + 2, round(blackjackRates[1][i-1],2))  


    # plot overall blackjack
    _, (ax7, ax8) = plt.subplots(1, 2)
    ax7.bar(policyNumber, overallBlackjack[0], color='#ed17e9')
    ax7.set_ylim([0, 100])
    ax7.set_xlabel('Policy')
    ax7.set_ylabel('Percentage Blackjack')
    ax7.set_title('Infinite Deck Blackjack')
    for i in policyNumber:
        ax7.text(i-0.25, round(overallBlackjack[0][i-1],2) + 2, round(overallBlackjack[0][i-1],2))

    ax8.bar(policyNumber, overallBlackjack[1], color='#ed17e9')
    ax8.set_ylim([0, 100])
    ax8.set_xlabel('Policy')
    ax8.set_ylabel('Percentage Blackjack')
    ax8.set_title('Single Deck Blackjack')
    for i in policyNumber:
        ax8.text(i-0.25, round(overallBlackjack[1][i-1],2) + 2, round(overallBlackjack[1][i-1],2))  
    plt.show()
    
simulate()

