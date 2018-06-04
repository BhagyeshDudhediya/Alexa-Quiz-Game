# Alexa-Quiz-Game
I have developed a skill named Gen Quest which is a quiz game built using ASK (Alexa Skill Kit).

Following are the intents supported in this skill:
  1. AMAZON.HelpIntent - To get the help related to this skill (Built In intent)
  2. AMAZON.CancelIntent - To cancel/stop the game (Built In intent)
  3. AMAZON.StopIntent - To cancel/stop the game (Built In intent)
  4. ConfirmYesOrNo - To confirm if you really want to play the game or not
  5. CheckAnswer - Check if the answer given is right or wrong
  6. GetNextQuestion - Get the next question
  7. RepeatQuestion - Repeat the question.
  
The function which is used to handle this intents is the lambda_handler in lambda_function.py

# Understanding the how intents are handled in lambda functions:
# Welcome Response  
**How to invoke this game?**   
User says "**Alexa, open gen quest**", a *LaunchRequest* is triggered which gets us the welcome response from the function get_welcome_response
which is triggered when skill is launched.

```
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the GenQuest Game. " \
                    "Please Confirm to start the game by saying yes or no " \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please Confirm to start the game by saying yes or no"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
 ```
 
 # ConfirmYesNo
 Once launch request is fired, user is asked to confirm by saying yes/no.  
 ```
 def get_confirmation(intent, session):
    """ Set your confirmation by saying Yes or No
    """
    card_title = intent['name']
    should_end_session = False
    selected_question = get_question()
    session_attributes = create_question_attributes(selected_question)
    #reprompt_text = speech_output = ""
    if 'YesNo' in intent['slots']:
        confirmation = intent['slots']['YesNo'].get('value')
        if confirmation == "yes":
            speech_output = "Thanks for confirmation. " \
                            "While Responding, 'Say Answer, and then tell your answer'. " \
                            "Let's begin. Your First Question, '" + selected_question + "'"
            reprompt_text = "Thanks for confirmation. " \
                            "While Responding, 'Say Answer, and then tell your answer'. " \
                            "Let's begin. Your First Question, '" + selected_question + "'"
        else:
            speech_output = "Oops, Sorry to hear you don't want to Play." \
                            " Bye Bye, Hope to meet with you soon."
            reprompt_text = "Oops, Sorry to hear you don't want to Play." \
                            " Bye Bye, Hope to meet with you soon."
            should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
```

# CheckAnswer
When a user says, "**Answer, {your answer}**", a CheckAnswer intent is
triggered which calls the following function to check if the given answer is correct or not.
```
def check_answer(intent, session):
    """ Check the answer of the question
    """
    card_title = intent['name']

    session_attributes = {}
    should_end_session = False
    reprompt_text = speech_output = ""
    if 'Answer' in intent['slots']:
        answer = intent['slots']['Answer'].get('value')
        if answer.lower() in session['attributes']['selectedAnswer'].lower():
            global points
            points = points + 1
            if points == len(questions):
                speech_output = "Great !! Correct answer! Your total Bitcoins are " + str(points) + \
                                ". Congratulations, You Win!!"
                reprompt_text = "Great !! Correct answer! Your total Bitcoins are " + str(points) + \
                                ". Congratulations, You Win!!"
            else:
                next_quest = get_question()
                session_attributes = create_question_attributes(next_quest)
                speech_output = "Great !! Correct answer! Your total Bitcoins are " + str(points) + ". Next Question. " \
                            + next_quest + "."

                reprompt_text = "Great !! Correct answer! Your total Bitcoins are " + str(points) + ". Next Question. " \
                            + next_quest + "."
        else:
            speech_output = "Oops Sorry, Wrong Answer! Correct answer is " + session['attributes']['selectedAnswer'] + \
                            ". You won " + str(points) + " Bitcoins."

            reprompt_text = "Oops Sorry, Wrong Answer! Correct answer is " + session['attributes']['selectedAnswer'] + \
                            ". You won " + str(points) + " Bitcoins."

            should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
```
PS: The bitcoins here are imaginary and not the actual ones :P

# RepeatQuestion
When user says "**Alexa, repeat the question**", a RepeatQuestion intent is triggered which repeats the question back. The following
function is invoked in this case:
```
def repeat_question(intent, session):
    # Repeating the question
    card_title = intent['name']
    should_end_session = False

    selected_answer = session['attributes']['selectedAnswer']

    for each_question in questions.keys():
        if selected_answer.lower() in each_question.lower():
            break

    speech_output = each_question

    reprompt_text = each_question
    session_attributes = create_question_attributes(each_question)

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
```

# Next Question
When user says "**Alexa, next question**", Alexa picks up a random question from it's set of question and gives it to the user.  
The following function is triggered in this case:
```
def next_question(intent, session):
    """ Next question
    """
    card_title = intent['name']
    should_end_session = False
    selected_question = get_question()
    session_attributes = create_question_attributes(selected_question)

    speech_output = "Next Question. " + selected_question + "."

    reprompt_text = "Next Question. " + selected_question + "."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
```

# StopIntent
Alexa stops the game when user says "**Alexa, end the game**".

A more detailed information regarding intents, slots and utterances is given on amazon alexa website.
