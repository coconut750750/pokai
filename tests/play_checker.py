"""
Module specifically designed to check if a play is valid
"""

from pokai.src.game.card import SMALL_JOKER_VALUE, BIG_JOKER_VALUE

def _check_single(single):
    """
    Checks if valid single
    single -- list of cards from the single play
    """
    assert single
    assert len(single) == 1

def _check_double(double):
    """
    Checks if valid double
    double -- list of cards from the double play
    """
    assert double
    assert len(double) == 2
    assert double[0].value == double[1].value

def _check_triple(triple):
    """
    Checks if valid triple
    triple -- list of cards from the triple play
    """
    assert triple
    l = len(triple)
    assert triple[0].value == triple[1].value and triple[0].value == triple[2].value
    if l >= 4:
        assert triple[0].value != triple[3].value
    if l == 5:
        assert triple[3].value == triple[4].value

def _check_adj_triple(adj_trip, extras):
    """
    Checks if valid adj triple
    adj_triple -- list of cards from the adj triple play
    extras -- number of extra cards
    """
    assert adj_trip
    l = len(adj_trip)
    assert l == 6 + extras
    _check_triple(adj_trip[0: 3])
    _check_triple(adj_trip[3: 6])
    assert adj_trip[0].value == adj_trip[3].value - 1
    if l == 6:
        return
    first = 6
    second = 7 if l == 8 else 8
    if l == 10:
        _check_double(adj_trip[first: second])
        _check_double(adj_trip[second:])
    assert adj_trip[first].value != adj_trip[second].value

    assert adj_trip[0].value != adj_trip[first].value\
        and adj_trip[0].value != adj_trip[second].value
    assert adj_trip[3].value != adj_trip[first].value\
        and adj_trip[3].value != adj_trip[second].value

def _check_quadruples(quad):
    """
    Checks if valid quad
    quad -- list of cards from the quad play
    """
    assert quad
    l = len(quad)
    assert l == 4 or l == 6 or l == 8
    assert quad[0].value == quad[1].value and\
        quad[0].value == quad[2].value and\
        quad[0].value == quad[3].value
    if l == 6:
        assert quad[4].value != quad[5].value
        assert quad[0].value != quad[4].value
        assert quad[0].value != quad[5].value
    if l == 8:
        _check_double(quad[4: 6])
        _check_double(quad[6: 8])
        assert quad[4].value != quad[6].value
        assert quad[0].value != quad[4].value
        assert quad[0].value != quad[6].value

def _check_straight(straight, each_count):
    """
    Checks if valid straight
    straight -- list of cards from the straight play
    each_count -- occurance of each card in the straight
    """
    assert straight
    l = len(straight)
    if each_count == 1:
        assert l >= 5
    elif each_count == 2:
        assert l >= 6
        assert l % 2 == 0
    elif each_count == 3:
        assert l >= 6
        assert l % 3 == 0
    for i in range(0, l - each_count, each_count):
        assert straight[i].value == straight[i + each_count].value - 1
        assert straight[i].value == straight[i + each_count - 1].value
        assert straight[i].value == straight[i + each_count // 3].value

def _check_wild(wild):
    """
    Checks if valid wild
    wild -- list of cards from the wild play
    """
    assert wild
    l = len(wild)
    assert l == 2 or l == 4
    if l == 4:
        _check_quadruples(wild)
    elif l == 2:
        assert wild[0].value == SMALL_JOKER_VALUE or wild[1].value == SMALL_JOKER_VALUE
        assert wild[0].value == BIG_JOKER_VALUE or wild[1].value == BIG_JOKER_VALUE
