from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    num_simulations = data.get('simulations', 100)
    strategy = data.get('strategy', 'stay')  # 'stay' or 'switch'
    
    wins = 0
    for _ in range(num_simulations):
        # Set up the doors: 0 = goat, 1 = car
        doors = [0, 0, 0]
        car_index = random.randint(0, 2)
        doors[car_index] = 1
        
        # Contestant's initial choice
        choice = random.randint(0, 2)
        
        # Monty opens a door with a goat that wasn't chosen
        monty_options = [i for i in range(3) if i != choice and doors[i] == 0]
        monty_opens = random.choice(monty_options)
        
        if strategy == 'stay':
            # Contestant stays with original choice
            if doors[choice] == 1:
                wins += 1
        else:
            # Contestant switches to the other unopened door
            remaining = [i for i in range(3) if i != choice and i != monty_opens][0]
            if doors[remaining] == 1:
                wins += 1
    
    win_percentage = (wins / num_simulations) * 100
    return jsonify({
        'wins': wins,
        'total': num_simulations,
        'win_percentage': win_percentage
    })

if __name__ == '__main__':
    app.run(debug=True)