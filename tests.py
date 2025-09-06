import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_remove_all_choices():
   question = Question(title='q1')
   question.add_choice('a')
   question.add_choice('b')
   question.remove_all_choices()
   assert len(question.choices) == 0

def test_remove_choice_by_id():
   question = Question(title='q1')
   c1 = question.add_choice('a')
   question.remove_choice_by_id(c1.id)
   assert len(question.choices) == 0

def test_add_choices():
   question = Question(title='q1')
   question.add_choice('a')
   question.add_choice('b')
   assert len(question.choices) == 2

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    assert len(question.choices) == 3

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)
    result = question.correct_selected_choices([c1.id, c2.id])
    assert result == [c1.id]

def test_correct_selected_choices_with_no_correct():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', False)
    c2 = question.add_choice('b', False)
    result = question.correct_selected_choices([c1.id, c2.id])
    assert result == []

def test_correct_selected_choices_with_all_correct():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', True)
    result = question.correct_selected_choices([c1.id, c2.id])
    assert result == [c1.id, c2.id]

def test_generate_choice_ids_sequentially():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3

def test_find_correct_choice_ids():
    question = Question(title='q1')
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)
    c3 = question.add_choice('c', False)
    assert question._find_correct_choice_ids() == [c1.id]

def test_add_choice_with_empty_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', True)

# Fixtures
@pytest.fixture
def simple_question():
    return Question(title='Simple Test Question')

@pytest.fixture
def question_with_choices():
    question = Question(title='Qual é o maior mamífero?')
    question.add_choice('Elefante', False)
    question.add_choice('Tubarão', False)
    question.add_choice('Cavalo', False)
    question.add_choice('Baleia', True)
    return question

@pytest.fixture
def multiple_choice_question():
    question = Question(title='Quais são linguagens de programação?', max_selections=3)
    question.add_choice('Python', True)
    question.add_choice('JavaScript', True)
    question.add_choice('HTML', False)
    question.add_choice('Java', True)
    return question

@pytest.fixture
def question_with_high_points():
    return Question(title='Questão difícil', points=10)


def test_question_with_choices_has_correct_answer(question_with_choices):
    correct_ids = question_with_choices._find_correct_choice_ids()
    assert len(correct_ids) == 1
    assert correct_ids[0] == 4

def test_multiple_choice_question_allows_multiple_selections(multiple_choice_question):
    python_id = multiple_choice_question.choices[0].id
    javascript_id = multiple_choice_question.choices[1].id
    html_id = multiple_choice_question.choices[2].id
    java_id = multiple_choice_question.choices[3].id
    
    result = multiple_choice_question.correct_selected_choices([python_id, javascript_id, java_id])
    assert len(result) == 3
    assert python_id in result
    assert javascript_id in result
    assert java_id in result
    
    result = multiple_choice_question.correct_selected_choices([python_id, html_id])
    assert result == [python_id]
