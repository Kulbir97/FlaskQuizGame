from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load questions from JSON file
def load_questions():
    with open('questions.json') as file:
        questions = json.load(file)
    return questions

# Display the quiz
@app.route('/', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()
    
    # If the form is submitted, show the score
    if request.method == 'POST':
        score = 0
        total = len(questions)

        for i, question in enumerate(questions, 1):
            user_answer = request.form.get(f'question_{i}')
            if user_answer == question['answer']:
                score += 1

        # Return the same page with the score shown
        return render_template('quiz.html', questions=questions, score=score, total=total)

    return render_template('quiz.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
