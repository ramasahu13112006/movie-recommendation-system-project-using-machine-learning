from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)


try:
    data_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies_data = pd.DataFrame(data_dict)
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    print("File Error:", e)


def calculate_accuracy(recommended_list, actual_relevant_list):
    if not recommended_list:
        return 0
    hits = 0
    for movie in recommended_list:
        if movie in actual_relevant_list:
            hits += 1
    return round((hits / len(recommended_list)) * 100, 2)

def get_recommendations(movie):
    try:
        idx = movies_data[movies_data['title'] == movie].index[0]
        dist = similarity_matrix[idx]
        
        items = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]

        result = []
        for i in items:
            result.append(movies_data.iloc[i[0]].title)
        
        return result
    except:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    all_movies = movies_data['title'].values
    results = []
    user_choice = ""
    accuracy_score = 0
    
    if request.method == 'POST':
        user_choice = request.form.get('movie_name')
        results = get_recommendations(user_choice)
        
        
        test_ground_truth = ["The Amazing Spider-Man 2", "Spider-Man", "Spider-Man 2", "Spider-Man 3", "Arachnophobia"]
        accuracy_score = calculate_accuracy(results, test_ground_truth)
        
        return render_template('index.html', 
                               movie_list=all_movies, 
                               names=results, 
                               selection=user_choice, 
                               accuracy=accuracy_score)

    return render_template('index.html', movie_list=all_movies)

if __name__ == "__main__":
    app.run(debug=True)
