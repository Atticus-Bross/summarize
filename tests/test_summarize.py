"""Module testing the Summarize Functions

Completed by Atticus Bross on 2024-10-29 for DS-1043"""
from summarize import *
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
def test_clean_text()->None:
    """test_clean_text()
    Tests the clean_text function"""
    assert clean_text(['They may be replaced by new “federated” platforms.'])==[['they','may','be','replaced','by','new','federated','platforms']]
    assert clean_text(['Illustration by Edmon de Haro','Jürgen Habermas, the German philosopher who coined the term _legitimization crisis_,'])==[['illustration','by','edmon','de','haro'],['jürgen','habermas','the','german','philosopher','who','coined','the','term','legitimization','crisis']]
    assert clean_text(['etc. and/the mr.','To/from/cube [qr] i/o?','(the#get&^where}'])==[['etc','and','the','mr'],['to','from','cube','qr','i','o'],['the','get','where']]
test_non_alnums()
test_many_split()
test_clean_word()
test_deep_unpack()