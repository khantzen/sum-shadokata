from enum import Enum

class Verb(Enum):
    GA='GA'
    BU='BU'
    ZO='ZO'
    MEU='MEU'

    def sum_inventory():
        return {
            'GA': {
                  'GA' : {'val': Verb.GA,   'keepBU': False }
                , 'BU' : {'val': Verb.BU,   'keepBU': False }
                , 'ZO' : {'val': Verb.ZO,   'keepBU': False }
                , 'MEU': {'val': Verb.MEU,  'keepBU': False }
            }
            , 'BU': {
                  'GA' : {'val': Verb.BU,  'keepBU': False }
                , 'BU' : {'val': Verb.ZO,  'keepBU': False }
                , 'ZO' : {'val': Verb.MEU, 'keepBU': False }
                , 'MEU': {'val': Verb.GA,  'keepBU': True  }
            }
            , 'ZO': {
                  'GA' : {'val': Verb.ZO,  'keepBU': False }
                , 'BU' : {'val': Verb.MEU, 'keepBU': False }
                , 'ZO' : {'val': Verb.GA,  'keepBU': True  }
                , 'MEU': {'val': Verb.BU,  'keepBU': True  }
            }
            , 'MEU': {
                  'GA' : {'val': Verb.MEU, 'keepBU': False }
                , 'BU' : {'val': Verb.GA,  'keepBU': True }
                , 'ZO' : {'val': Verb.BU,  'keepBU': True }
                , 'MEU': {'val': Verb.ZO,  'keepBU': True }
            }
        }

class ShadokNumber():
    def __init__(self, verbs):
        self.number = verbs

    def sum(self, shadok):
        left_reverse = self.number[::-1]
        right_reverse = shadok.number[::-1]

        sum_terms = ShadokNumber.equalize_list_length(left_reverse,
                                                      right_reverse)

        final_number = []
        keep_val = Verb.GA

        for left, right in zip(sum_terms[0], sum_terms[1]):
            sum_info = ShadokNumber.from_inventory(left, right)
            next_val = ShadokNumber.from_inventory(sum_info['val'], keep_val)

            keep_val = Verb.BU if sum_info['keepBU'] else Verb.GA

            final_number += [next_val['val']]

        if keep_val != Verb.GA:
            final_number += [keep_val]

        return ShadokNumber(final_number[::-1])

    def equalize_list_length(list1, list2):
        length_diff = abs(len(list1) - len(list2))

        list1_equalized = list1 + [Verb.GA] * length_diff
        list2_equalized = list2 + [Verb.GA] * length_diff

        return [list1_equalized, list2_equalized]

    def from_inventory(verb1, verb2):
        sum_inventory = Verb.sum_inventory()
        return sum_inventory[verb1.name][verb2.name]

### Unit Test ###

def test_sum_with_neutral_yield_other_term():
    assert_are_equals(ga().sum(bu()), bu())
    assert_are_equals(zo().sum(ga()), zo())

def test_sum_with_no_keep():
    assert_are_equals(bu().sum(zo()), meu())
    assert_are_equals(bu().sum(bu()), zo())

def test_sum_with_single_keep_new_digit():
    assert_are_equals(bu().sum(meu()), ShadokNumber([Verb.BU, Verb.GA]))
    assert_are_equals(meu().sum(meu()), ShadokNumber([Verb.BU, Verb.ZO]))

def test_same_length_sum_with_no_keep():
    left = ShadokNumber([Verb.BU, Verb.ZO, Verb.GA])
    right = ShadokNumber([Verb.BU, Verb.BU, Verb.ZO])
    expected = ShadokNumber([Verb.ZO, Verb.MEU, Verb.ZO])
    assert_are_equals(left.sum(right), expected)

def test_same_length_sum_with_a_single_keep():
    left = ShadokNumber([Verb.BU, Verb.MEU])
    right = ShadokNumber([Verb.BU, Verb.BU])
    expected = ShadokNumber([Verb.MEU, Verb.GA])
    assert_are_equals(left.sum(right), expected)

def test_same_length_sum_with_multiple_keep():
    number = ShadokNumber([Verb.MEU, Verb.MEU, Verb.MEU])
    expected = ShadokNumber([Verb.BU, Verb.MEU, Verb.MEU, Verb.ZO])
    assert_are_equals(number.sum(number), expected)

def test_different_length_sum():
    left = ShadokNumber([Verb.BU, Verb.MEU])
    right = meu()
    expected = ShadokNumber([Verb.ZO, Verb.ZO])
    assert_are_equals(left.sum(right), expected)

def test_limit():
    left = ShadokNumber([Verb.ZO, Verb.MEU, Verb.MEU, Verb.GA,
                         Verb.ZO])
    right = ShadokNumber([Verb.ZO, Verb.ZO, Verb.ZO, Verb.ZO, Verb.MEU,
                          Verb.BU, Verb.ZO])
    expected = ShadokNumber([Verb.ZO, Verb.MEU, Verb.BU, Verb.ZO, Verb.ZO,
                             Verb.ZO, Verb.GA])
    assert_are_equals(left.sum(right), expected)

### Unit Test Helper ###

def assert_are_equals(actual, expected):
    actualValue = actual.number
    targetValue = expected.number
    assert actualValue == targetValue

def ga():
    return ShadokNumber([Verb.GA])

def bu():
    return ShadokNumber([Verb.BU])

def zo():
    return ShadokNumber([Verb.ZO])

def meu():
    return ShadokNumber([Verb.MEU])
