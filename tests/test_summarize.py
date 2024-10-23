"""Module testing the Summarize Functions

Completed by Atticus Bross on 2024-10-29 for DS-1043"""

from summarize import *
from math import isclose
from random import randint,choice
def test_non_alnums()->None:
    """test_non_alnums()
    Tests the non_alnums function"""
    assert non_alnums('the rabbit')==' '
    assert non_alnums('t[6}!ty')=='[}!'
    assert non_alnums('|thy&')=='|&'
    assert non_alnums('{{{***^&^&')=='{*^&'
def test_many_split()->None:
    """test_many_split()
    Tests the many_split function"""
    assert many_split('abc|efg|hij',['|'])==['abc','efg','hij']
    assert many_split('abc|efg!hij',['|','!'])==['abc','efg','hij']
    assert many_split('ab?cd|ef%gh|ij?kl|mn%op',['%','|','?'])==['ab','cd','ef','gh','ij','kl','mn','op']
    assert many_split('abcdef',['9','p','['])==['abcdef']
    assert many_split('[}|:*&',[])==['[}|:*&']
def test_clean_word()->None:
    """test_clean_word()
    Tests the clean_word function"""
    assert clean_word('|abc|efg|hij|')==['abc','efg','hij']
    assert clean_word('{}{}|}{}abc|efg!hij%^&*')==['abc','efg','hij']
    assert clean_word('[}|:*&')==['']
def test_deep_unpack() -> None:
    """test_deep_unpack()
    Tests the deep_unpack function"""
    assert deep_unpack([[None, 'abc', 1.2], [True, 3], ['ghf']]) == [None, 'abc', 1.2, True, 3, 'ghf']
    assert deep_unpack([[['abc', None], [], 2.34], [[], [True, 3]]]) == ['abc', None, 2.34, True, 3]
    assert deep_unpack([[(1, 2, 3), ('abc', 'efg')], ['abc']], tuple) == [(1, 2, 3), ('abc', 'efg'), 'a', 'b', 'c']
    assert deep_unpack([[(1, 2, 3), ('abc', 'efg')], ['abc']], tuple | str) == [(1, 2, 3), ('abc', 'efg'), 'abc']
def test_remove_all()->None:
    """test_remove_all()
    Tests the remove_all function"""
    assert remove_all([1,2,3,4],4)==[1,2,3]
    assert remove_all([1,2,3,3,3,4],5)==[1,2,3,3,3,4]
    assert remove_all([1],1)==[]
    assert remove_all([1,1,1,1],1)==[]
    assert remove_all([1,2,3,3,3,4],3)==[1,2,4]
def test_clean_sentence()->None:
    """test_clean_sentence()
    Tests the clean_sentence function"""
    assert clean_sentence([word.casefold() for word in nltk.word_tokenize('They may be replaced by new “federated” platforms.')])==['they','may','be','replaced','by','new','federated','platforms']
    assert clean_sentence([word.casefold() for word in nltk.word_tokenize('Jürgen Habermas, the German philosopher who coined the term _legitimization crisis_,')])==['jürgen','habermas','the','german','philosopher','who','coined','the','term','legitimization','crisis']
    assert clean_sentence([word.casefold() for word in nltk.word_tokenize('etc. and/the mr.')])==['etc','and','the','mr']
def test_clean_text()->None:
    """test_clean_text()
    Tests the clean_text function"""
    assert clean_text(['They may be replaced by new “federated” platforms.'])==[['they','may','be','replaced','by','new','federated','platforms']]
    assert clean_text(['Illustration by Edmon de Haro','Jürgen Habermas, the German philosopher who coined the term _legitimization crisis_,'])==[['illustration','by','edmon','de','haro'],['jürgen','habermas','the','german','philosopher','who','coined','the','term','legitimization','crisis']]
    assert clean_text(['etc. and/the mr.','To/from/cube [qr] i/o?','(the#get&^where}'])==[['etc','and','the','mr'],['to','from','cube','qr','i','o'],['the','get','where']]
def test_calculate_tf()->None:
    """test_calculate_tf()
    Tests the calculate_tf function"""
    with open(r'C:\Users\user\PycharmProjects\summarize\examples\social.md','r',encoding='utf-8') as mdfile:
        test:list=load_document(mdfile)
    test=clean_text(test)
    test2:list=calculate_tf(test)
    assert isclose(test2[0]['created'],1/194)
    assert isclose(test2[10]['as'],3/66)
    assert isclose(test2[20]['no'],3/64)
    assert len(test2)==len(test)
    index:int=randint(0,len(test)-1)
    test_choice:list=test[index]
    test2_choice:dict=test2[index]
    for word in test2_choice.keys():
        assert word in test_choice
def test_calculate_idf()->None:
    """test_calculate_idf()
    Tests the calculate_idf function"""
    with open(r'C:\Users\user\PycharmProjects\summarize\examples\social.md','r',encoding='utf-8') as mdfile:
        test:list=load_document(mdfile)
    test=clean_text(test)
    test2:dict=calculate_idf(test)
    assert isclose(test2['https'],log(112/30))
    assert isclose(test2['social'],log(112/22))
    assert isclose(test2['a'],log(112/51))
    assert choice(list(test2.keys())) in deep_unpack(test)
def test_calculate_tf_idf()->None:
    """test_calculate_tf_idf()
    Tests the calculate_tf_idf function"""
    assert calculate_tf_idf({'a':1.0},{'a':2.0})=={'a':2.0}
    assert calculate_tf_idf({'back':3.0,'line':2.0,'test':4.0},{'test':2.0,'back':1.0,'line':3.0})=={'back':3.0,'line':6.0,'test':8.0}
    assert calculate_tf_idf({'back': 3.0, 'line': 2.0, 'test': 4.0}, {'skd':1.2,'test': 2.0,'sda':5.4, 'back': 1.0, 'line': 3.0,'lkj':9.8}) == {
        'back': 3.0, 'line': 6.0, 'test': 8.0}
test_non_alnums()
test_many_split()
test_clean_word()
test_deep_unpack()
test_remove_all()
test_clean_sentence()
test_clean_text()
test_calculate_tf()
test_calculate_idf()
test_calculate_tf_idf()
