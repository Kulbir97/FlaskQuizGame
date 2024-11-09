from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for sessions

# Load questions from JSON file
def load_questions():
    with open('questions.json') as file:
        questions = json.load(file)
    return questions

# Home page route with start button
@app.route('/')
def home():
    return render_template('home.html')  # This page will have the start button

# Quiz page route
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = load_questions()

    score = 0
    total = len(questions)
    user_answers = []
    feedback = []

    if request.method == 'POST':
        for i, question in enumerate(questions, 1):
            user_answer = request.form.get(f'question_{i}')
            correct_answer = question['answer']
            feedback_text = "Correct!" if user_answer == correct_answer else f"Wrong! The correct answer was {correct_answer}."
            user_answers.append(user_answer)
            feedback.append(feedback_text)
            if user_answer == correct_answer:
                score += 1

        session['score'] = score
        session['total'] = total
        session['feedback'] = feedback
        session['user_answers'] = user_answers

        return redirect(url_for('result'))

    return render_template('quiz.html', questions=questions)

# Result page route
@app.route('/result', methods=['GET'])
def result():
    score = session.get('score')
    feedback = session.get('feedback')
    total = session.get('total')
    user_answers = session.get('user_answers')

    questions = load_questions()

    # Pass 'zip' function to the template context
    return render_template('result.html', score=score, total=total, feedback=feedback, questions=questions, user_answers=user_answers, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
