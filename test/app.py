
@app.route('/play', methods=['POST'])
def play():
    word_to_guess = request.form['word_to_guess']
    guessed_letters = set(request.form['guessed_letters'])
    attempts_left = int(request.form['attempts_left'])
    guess = request.form['guess'].upper()

    if guess not in guessed_letters:
        guessed_letters.add(guess)
        if guess not in word_to_guess:
            attempts_left -= 1

    game_state = ''.join(letter if letter in guessed_letters else '_' for letter in word_to_guess)

    if '_' not in game_state:
        return render_template('pendu.html', win=True, word_to_guess=word_to_guess)

    if attempts_left == 0:
        return render_template('pendu.html', lose=True, word_to_guess=word_to_guess)

    return render_template('pendu.html', word_to_guess=word_to_guess, game_state=game_state, attempts_left=attempts_left, guessed_letters=guessed_letters)
