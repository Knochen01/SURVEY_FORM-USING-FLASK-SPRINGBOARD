from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session;
# put here as constants so we're guaranteed to be consistent in
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
# ------------------------------------------------------------------------------
@app.route("/")
def show_survey_start():
    """Select a survey."""

    return render_template("survey_start.html", survey=survey)
# ------------------------------------------------------------------------------
@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")
# ------------------------------------------------------------------------------
@app.route('/answer', methods=["POST"])
def handle_questions():
    """Safe response and redirect to the next question"""
    #  get the response choise
    choice = request.form['answer']
    # add this response to the session. 
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
# ------------------------------------------------------------------------------
@app.route('/questions/<int:Q>')
def show_question(Q):
    responses = session.get(RESPONSES_KEY)
    question = survey.questions[Q]

    #  trying to accsess questions out of order.        
    if (len(responses) != Q):
        flash(f"Invalid question id: {Q}.")
    # They've answered all the questions! Thank them.
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    # trying to access question page too soon
    if (responses is None):
        return redirect("/")

    return render_template('questions.html', question=question, question_num=Q)

# ------------------------------------------------------------------------------
@app.route('/complete')
def complete():
    """Survey complete. Show completion page"""

    return render_template('completion.html')