from enum import Enum

class Verb(Enum):
    GA='GA'
    BU='BU'
    ZO='ZO'
    MEU='MEU'

    def sum_inventory():
        return {
            'GA': {
                  'GA' : {'val': Verb.GA,   'keep': False }
                , 'BU' : {'val': Verb.BU,   'keep': False }
                , 'ZO' : {'val': Verb.ZO,   'keep': False }
                , 'MEU': {'val': Verb.MEU,  'keep': False }
            }
            , 'BU': {
                  'GA' : {'val': Verb.BU,  'keep': False }
                , 'BU' : {'val': Verb.ZO,  'keep': False }
                , 'ZO' : {'val': Verb.MEU, 'keep': False }
                , 'MEU': {'val': Verb.GA,  'keep': True  }
            }
            , 'ZO': {
                  'GA' : {'val': Verb.ZO,  'keep': False }
                , 'BU' : {'val': Verb.MEU, 'keep': False }
                , 'ZO' : {'val': Verb.GA,  'keep': True  }
                , 'MEU': {'val': Verb.BU,  'keep': True  }
            }
            , 'MEU': {
                  'GA' : {'val': Verb.MEU, 'keep': False }
                , 'BU' : {'val': Verb.GA,  'keep': True }
                , 'ZO' : {'val': Verb.BU,  'keep': True }
                , 'MEU': {'val': Verb.ZO,  'keep': True }
            }
        }


class ShadokNumber():
    def __init__(self, verbs):
        self.number = verbs

    def sum(self, target):
        math_sum = MathematicSum(Verb.GA, Verb.BU, Verb.sum_inventory())
        return ShadokNumber(math_sum.apply_on(self.number, target.number))

    def __add__(self, other):
        return self.sum(other)

class MathematicSum:
    def __init__(self, neutral, unit, inventory):
        self.unit = unit
        self.neutral = neutral
        self.inventory = inventory

    def apply_on(self, left, right):
        left_reverse  = left[::-1]
        right_reverse = right[::-1]

        sum_terms = self.equalize_list_length(left_reverse, right_reverse)

        final_number = []
        keep = False

        for left, right in zip(sum_terms[0], sum_terms[1]):
            sum_info = self.digit_sum_info(left, right)
            temp_result = sum_info['val']

            keep_val = self.unit if keep else self.neutral
            next_val_info = self.digit_sum_info(temp_result, keep_val)

            next_val = next_val_info['val']
            keep     = sum_info['keep']

            final_number += [next_val]

        if keep:
            final_number += [self.unit]

        return final_number[::-1]

    def equalize_list_length(self, list1, list2):
        length_diff = abs(len(list1) - len(list2))

        list1_equalized = list1 + [self.neutral] * length_diff
        list2_equalized = list2 + [self.neutral] * length_diff

        return [list1_equalized, list2_equalized]

    def digit_sum_info(self, left, right):
        return self.from_inventory(left, right)


    def from_inventory(self, verb1, verb2):
        return self.inventory[verb1.name][verb2.name]

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
