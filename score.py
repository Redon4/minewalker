import pickle 


filename = "highscore.pkl"

def save_score(score):
    with open(filename, "wb") as f:
        pickle.dump(score, f)

def load_score():
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return 0