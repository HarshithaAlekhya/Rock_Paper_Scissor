# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

# def player(prev_play, opponent_history=[]):
#     opponent_history.append(prev_play)

#     guess = "R"
#     if len(opponent_history) > 2:
#         guess = opponent_history[-2]

#     return guess
import random
from collections import defaultdict

def player(prev_play, opponent_history=[]):
    if prev_play != "":
        opponent_history.append(prev_play)

    # Strategies for each bot
    # Determine the likely opponent based on history patterns
    if len(opponent_history) >= 1000:
        # Assuming we might need to reset history for very long matches to avoid memory issues
        opponent_history.clear()

    # Strategy to beat Quincy (R, R, P, P, S, repeat)
    if len(opponent_history) >= 5:
        last_five = "".join(opponent_history[-5:])
        if last_five in ["RRPPS", "RPPSR", "PPSRR", "PSRRP", "SRRPP"]:
            # Quincy's sequence is R, R, P, P, S, then repeat
            # Predict next move based on position in the sequence
            pos = len(opponent_history) % 5
            if pos == 0:
                return "P"  # beats R (first move)
            elif pos == 1:
                return "P"  # beats R
            elif pos == 2:
                return "S"  # beats P
            elif pos == 3:
                return "S"  # beats P
            elif pos == 4:
                return "R"  # beats S

    # Strategy to beat Kris (mirrors our last move)
    if len(opponent_history) >= 1:
        # Kris plays what would beat our last move. So if our last move was R, Kris plays P.
        # So to counter, we need to play what beats their predicted move.
        # But since we don't track our own history in the function, we need another approach.
        # Alternatively, since Kris plays to beat our last move, their current move is based on our last move.
        # So if we can predict their move based on our last move, we can counter.
        # But without tracking our own moves, this is tricky. So perhaps assume Kris is the opponent if a pattern is detected.
        # For example, if the opponent always plays to beat what we played last, our current move can be chosen to beat their response.
        # This might require tracking our own moves, which isn't directly possible with the given function signature.
        pass

    # Default strategy: use a Markov model to predict next move based on opponent's history
    # This is more general and can adapt to various patterns
    if len(opponent_history) >= 4:
        last_three = "".join(opponent_history[-3:])
        model = defaultdict(lambda: [0, 0, 0])
        for i in range(len(opponent_history) - 3):
            triplet = "".join(opponent_history[i:i+3])
            next_move = opponent_history[i+3]
            if next_move == "R":
                model[triplet][0] += 1
            elif next_move == "P":
                model[triplet][1] += 1
            elif next_move == "S":
                model[triplet][2] += 1

        last_triplet = "".join(opponent_history[-3:])
        if last_triplet in model:
            predicted = model[last_triplet]
            max_index = predicted.index(max(predicted))
            if max_index == 0:
                guess = "P"
            elif max_index == 1:
                guess = "S"
            else:
                guess = "R"
            return guess

    # Fallback to counter Abbey's strategy (she uses a frequency-based approach)
    # Or play randomly if no pattern detected
    return random.choice(["R", "P", "S"])
