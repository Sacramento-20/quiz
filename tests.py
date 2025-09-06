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