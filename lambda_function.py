"""
Quiz Game skill built with the Amazon Alexa Skills Kit.
"""

from __future__ import print_function
import random


# --------------- Helpers that build all of the responses ----------------------
points = 0


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

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


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying GenQuest. " \
                    "Hope to play with you soon. Bye Bye!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_question_attributes(selected_question):
    #answer = ""
    if '15th August Celebrated as in India' in selected_question:
        answer = 'Independence Day'
    elif 'capital of India' in selected_question:
        answer = 'New Delhi'
    elif 'captain of current Indian Cricket Team' in selected_question:
        answer = 'Virat Kohli'
    elif 'Entomology' in selected_question:
        answer = 'Insects'
    elif 'Hitler party' in selected_question:
        answer = 'Nazi Party'
    elif 'father of geometry' in selected_question:
        answer = 'Euclid'
    elif 'B. C. Roy award' in selected_question:
        answer = 'Medicine'
    elif 'National Income estimates in India' in selected_question:
        answer = 'Central Statistical Organisation'
    elif 'latitude passes through the middle of India' in selected_question:
        answer = 'Tropic of Cancer'
    elif 'Fathometer is used to measure' in selected_question:
        answer = 'Ocean depth'
    elif 'Ctrl, Shift and Alt' in selected_question:
        answer = 'Modifier Keys'

    return {"selectedAnswer": answer}

questions = {}
questions["What is capital of India? A: New Delhi. B: Mumbai. C: Nagpur. D: Bangalore."] = 0
questions["What is 15th August Celebrated as in India? A: Republic Day. B: Independence Day. C: Gandhi Jayanti. D: Ambedkar Jayanti."] = 0
questions["Who is captain of current Indian Cricket Team? A: M. S. Dhoni. B: Rohit Sharma. C: Virat Kohli. D: Suresh Raina."] = 0
questions["Entomology is the science that studies. A: Human Behavior. B: Insects. C: The origin and history of technical and scientific terms. D: The formation of rocks."] = 0
questions["Hitler party which came into power in 1933 is known as. A: Labour Party. B: Nazi Party. C: Democratic Party. D: Congress Party."] = 0
questions["Who is father of geometry. A: Aristotle. B: Euclid. C: Pythagoras. D: Kepler."] = 0
questions["B. C. Roy award is given in the field of. A: Music. B: Journalism. C: Medicine. D: Environment."] = 0
questions["National Income estimates in India are prepared by? A: Planning Commission. B: Reserve Bank of India. C: Central statistical organisation. D: Indian statistical Institute."] = 0
questions["Which latitude passes through the middle of India? A: Equator. B: Arctic Circle. C: Tropic of Capricorn. D: Tropic of Cancer."] = 0
questions["Fathometer is used to measure? A: Earthquakes. B: Rainfall. C: Ocean depth. D: Sound intensity."] = 0
questions["Ctrl, Shift and Alt are which keys? A: Modifier Keys. B: Function Keys. C: Alphanumeric Keys. D: Adjustment Keys."] = 0

def get_question():
    sel_quest = random.choice(questions.keys())
    # Make sure that question is not repeated
    while 1:
        if questions[sel_quest] != 0:
            sel_quest = random.choice(questions.keys())
        else:
            break
    questions[sel_quest] = 1
    return sel_quest

def check_answer(intent, session):
    """ Check the answer of the question
    """
    card_title = intent['name']

    session_attributes = {}
    should_end_session = False
    reprompt_text = speech_output = ""
    if 'Answer' in intent['slots']:
        answer = intent['slots']['Answer'].get('value')
        if answer.lower() == session['attributes']['selectedAnswer'].lower():
            global points
            points = points + 1
            next_quest = get_question()
            session_attributes = create_question_attributes(next_quest)
            speech_output = "Great !! Correct answer! Your total Bitcoins are " + str(points) + ". Next Question. " \
                            + next_quest + "."

            reprompt_text = "Great !! Correct answer! Your total Bitcoins are " + str(points) + ". Next Question. " \
                            + next_quest + "."

        else:
            speech_output = "Oops Sorry, Wrong Answer! Correct answer is " + session['attributes']['selectedAnswer'] + ". You won " + str(points) + " Bitcoins."

            reprompt_text = "Oops Sorry, Wrong Answer! Correct answer is " + session['attributes']['selectedAnswer'] + ". You won " + str(points) + " Bitcoins."

            should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


"""def repeat_question(intent, session):
    # Repeating the question
    
    card_title = intent['name']
    should_end_session = False

    selected_answer = session['attributes']['selectedAnswer']
    session_attributes = create_question_attributes(selected_answer)

    speech_output = selected_answer

    reprompt_text = selected_answer

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
"""

def next_question(intent, session):
    """ Next question
    """
    card_title = intent['name']
    should_end_session = False
    selected_question = get_question()
    session_attributes = create_question_attributes(selected_question)

    speech_output = "Next Question " + selected_question + "."

    reprompt_text = "Next Question " + selected_question + "."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


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


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ConfirmYesOrNo":
        return get_confirmation(intent, session)
    elif intent_name == "CheckAnswer":
        return check_answer(intent, session)
    elif intent_name == "GetNextQuestion":
        return next_question(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
