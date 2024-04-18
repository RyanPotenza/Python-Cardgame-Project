$(document).ready(function() {
    $('#deal-btn').click(function() {
        var bet = $('#bet').val();

        $.ajax({
            url: '/deal',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ bet: bet }),
            success: function(data) {
                $('#player-hand').empty().append('<h3>Player\'s Hand:</h3>');
                $('#dealer-hand').empty().append('<h3>Dealer\'s Hand:</h3>');
                $('#message').text('');

                data.player_hand.forEach(function(card) {
                    $('#player-hand').append('<div class="card">' + card + '</div>');
                });

                data.dealer_hand.forEach(function(card, index) {
                    if (index === 0) {
                        $('#dealer-hand').append('<div class="card"> </div>');
                    } else {
                        $('#dealer-hand').append('<div class="card">' + card + '</div>');
                    }
                });

                if (data.result === 'Player wins') {
                    // Reveal Dealer's Cards
                    $('#dealer-hand').empty().append('<h3>Dealer\'s Hand:</h3>');
                    data.dealer_hand.forEach(function(card) {
                        $('#dealer-hand').append('<div class="card">' + card + '</div>');
                    });

                    $('#message').text('Blackjack! You win 2.5x!');
                    $('#balance').text('Balance: $' + data.balance);

                    $('#hit-btn').prop('disabled', true);
                    $('#stand-btn').prop('disabled', true);
                    $('#double-btn').prop('disabled', true);
                } else if (data.result === 'Push') {
                    // Reveal Dealer's Cards
                    $('#dealer-hand').empty().append('<h3>Dealer\'s Hand:</h3>');
                    data.dealer_hand.forEach(function(card) {
                        $('#dealer-hand').append('<div class="card">' + card + '</div>');
                    });
                    
                    $('#message').text('Push!');
                    $('#balance').text('Balance: $' + data.balance);

                    $('#hit-btn').prop('disabled', true);
                    $('#stand-btn').prop('disabled', true);
                    $('#double-btn').prop('disabled', true);
                } else {
                    $('#hit-btn').prop('disabled', false);
                    $('#stand-btn').prop('disabled', false);
                    $('#double-btn').prop('disabled', false);

                    $('#balance').text('Balance: $' + data.balance);
                }  
            }
        });
    });

    $('#hit-btn').click(function() {
        $.ajax({
            url: '/hit',
            method: 'POST',
            contentType: 'application/json',
            success: function(data) {
                $('#player-hand').empty().append('<h3>Player\'s Hand:</h3>');
                data.player_hand.forEach(function(card) {
                    $('#player-hand').append('<div class="card">' + card + '</div>');
                });
                $('#balance').text('Balance: $' + data.balance);
                $('#double-btn').prop('disabled', true);

                // Check if player busted
                if (data.player_total > 21) {
                    $('#message').text('You busted!');
                    $('#hit-btn').prop('disabled', true);
                    $('#stand-btn').prop('disabled', true);
                    $('#double-btn').prop('disabled', true);
                }
            }
        });
    });

    $('#stand-btn').click(function() {
        $.ajax({
            url: '/stand',
            method: 'POST',
            contentType: 'application/json',
            success: function(data) {
                $('#dealer-hand').empty().append('<h3>Dealer\'s Hand:</h3>');
                data.dealer_hand.forEach(function(card) {
                    $('#dealer-hand').append('<div class="card">' + card + '</div>');
                });
                $('#balance').text('Balance: $' + data.balance);

                // Display result message
                if (data.result === 'Player wins') {
                    $('#message').text('You win!');
                } else if (data.result === 'Dealer wins') {
                    $('#message').text('Dealer wins!');
                } else {
                    $('#message').text('Push!');
                }

                // Disable buttons
                $('#hit-btn').prop('disabled', true);
                $('#stand-btn').prop('disabled', true);
                $('#double-btn').prop('disabled', true);
            }
        });
    });

    $('#double-btn').click(function() {
        $.ajax({
            url: '/double',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ bet: $('#bet').val() }),  // Pass the bet amount for double down
            success: function(data) {
                $('#player-hand').empty();
                data.player_hand.forEach(function(card) {
                    $('#player-hand').append('<div class="card">' + card + '</div>');
                });
                $('#balance').text('Balance: $' + data.balance);

                // Check if player busted
                if (data.player_total > 21) {
                    $('#message').text('You busted!');
                    $('#hit-btn').prop('disabled', true);
                    $('#stand-btn').prop('disabled', true);
                    $('#double-btn').prop('disabled', true);
                } else {
                    // Auto-stand after double down
                    $('#stand-btn').trigger('click');
                }
            }
        });
    });
});




