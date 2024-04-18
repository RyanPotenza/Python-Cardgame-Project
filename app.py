from flask import Flask, render_template, request, jsonify
from random import choice

app = Flask(__name__)

# Global variables
deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
balance = 500
player_hand = []
dealer_hand = []

@app.route('/')
def index():
    return render_template('index.html', balance=balance)

@app.route('/deal', methods=['POST'])
def deal():
    global player_hand, dealer_hand, balance

    bet = int(request.json['bet'])

    if bet > balance:
        return jsonify({'error': 'Insufficient funds'})

    player_hand.clear()
    dealer_hand.clear()

    player_hand.extend([choice(deck), choice(deck)])
    dealer_hand.extend([choice(deck), choice(deck)])

    player_total = calculate_total(player_hand)
    dealer_total = calculate_total(dealer_hand)

    if player_total == 21 and len(player_hand) == 2:  # Natural blackjack
        if dealer_total == 21 :
            result = 'Push'
            return jsonify({
            'player_hand': player_hand,
            'player_total': player_total,
            'dealer_hand': dealer_hand,
            'dealer_total': dealer_total,
            'balance': balance,
            'result': result
        })
        balance += bet * 2.5
        result = 'Player wins'
        return jsonify({
            'player_hand': player_hand,
            'player_total': player_total,
            'dealer_hand': dealer_hand,
            'dealer_total': dealer_total,
            'balance': balance,
            'result': result
        })


    balance -= bet  # Subtract the bet from the balance

    return jsonify({
        'player_hand': player_hand,
        'player_total': player_total,
        'dealer_hand': [dealer_hand[0], dealer_hand[1]],
        'dealer_total': dealer_total,
        'balance': balance,  # Updated balance after subtracting the bet
        'result': 'Continue'
    })


@app.route('/hit', methods=['POST'])
def hit():
    global player_hand, balance

    player_hand.append(choice(deck))

    player_total = calculate_total(player_hand)

    return jsonify({
        'player_hand': player_hand,
        'player_total': player_total,
        'balance': balance
    })

@app.route('/stand', methods=['POST'])
def stand():
    global player_hand, dealer_hand, balance

    while calculate_total(dealer_hand) < 17:
        dealer_hand.append(choice(deck))

    player_total = calculate_total(player_hand)
    dealer_total = calculate_total(dealer_hand)

    result = determine_winner(player_total, dealer_total)

    if result == 'Player wins':
        balance += int(request.json['bet']) * 2  # Add double the bet amount if the player wins
    if result == 'Push':
        balance += int(request.json['bet'])

    return jsonify({
        'player_hand': player_hand,
        'player_total': player_total,
        'dealer_hand': dealer_hand,
        'dealer_total': dealer_total,
        'result': result,
        'balance': balance
    })

@app.route('/double', methods=['POST'])
def double():
    global player_hand, balance

    bet = int(request.json['bet'])

    if bet > balance:
        return jsonify({'error': 'Insufficient funds'})

    balance -= bet  # Subtract the current bet
    bet *= 2  # Double the bet
    
    player_hand.append(choice(deck))
    player_total = calculate_total(player_hand)
    result = determine_winner(player_total, calculate_total(dealer_hand))

    if result == 'Player wins':
        balance += bet  # Player wins, so add double the bet amount
    elif result == 'Push':
        balance += bet / 2  # Push, so add the bet amount back to the balance

    return jsonify({
        'player_hand': player_hand,
        'player_total': player_total,
        'balance': balance
    })

def calculate_total(hand):
    total = 0
    num_aces = 0

    for card in hand:
        if card.isdigit():
            total += int(card)
        elif card in ['J', 'Q', 'K']:
            total += 10
        elif card == 'A':
            num_aces += 1
            total += 11

    while total > 21 and num_aces:
        total -= 10
        num_aces -= 1

    return total

def determine_winner(player_total, dealer_total):
    if player_total > 21:
        return 'Dealer wins'
    elif dealer_total > 21:
        return 'Player wins'
    elif player_total == dealer_total:
        return 'Push'
    elif player_total > dealer_total:
        return 'Player wins'
    else:
        return 'Dealer wins'

if __name__ == '__main__':
    app.run(debug=True)




