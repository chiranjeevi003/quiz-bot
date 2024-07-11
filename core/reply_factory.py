
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    questions = {
        q['id']: q for q in PYTHON_QUESTION_LIST
    }

    
    if current_question_id not in questions:
        return False, "Invalid question ID."

    
    if not isinstance(answer, str) or not answer.strip():
        return False, "Invalid answer. Answer cannot be empty and must be a string."

    
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}

    correct_answer = questions[current_question_id]['answer']
    session['quiz_answers'][current_question_id] = {
        'answer': answer,
        'is_correct': answer.strip().lower() == correct_answer.lower()
    }

   
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0]['question'], PYTHON_QUESTION_LIST[0]['id']

    for i, q in enumerate(PYTHON_QUESTION_LIST):
        if q['id'] == current_question_id and i + 1 < len(PYTHON_QUESTION_LIST):
            next_question = PYTHON_QUESTION_LIST[i + 1]
            return next_question['question'], next_question['id']
    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total = len(PYTHON_QUESTION_LIST)
    correct = sum(1 for answer in session['quiz_answers'].values() if answer['is_correct'])

    return f'Your scored {correct} out of {total}.'
    
