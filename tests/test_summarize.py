"""Module testing the Summarize Functions

Completed by Atticus Bross on 2024-10-29 for DS-1043"""
from summarize import *
def test_clean_text()->None:
    """test_clean_text()
    Tests the clean_text function"""
    assert clean_text(['They may be replaced by new “federated” platforms.'])==[['they','may','be','replaced','by','new','federated','platforms']]
    assert clean_text(['Illustration by Edmon de Haro','Jürgen Habermas, the German philosopher who coined the term _legitimization crisis_,'])==[['illustration','by','edmon','de','haro'],['jürgen','habermas','the','german','philosopher','who','coined','the','term','legitimization','crisis']]
    assert clean_text(['etc. and/the mr.','To/from/cube [qr] i/o?','(the#get&^where}'])==[['etc','and','the','mr'],['to','from','cube','qr','i','o'],['the','get','where']]
test_clean_text()