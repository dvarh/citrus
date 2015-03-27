from django.test import SimpleTestCase

from calc.views import CalcApi

class CalcApiTest(SimpleTestCase):
    def setUp(self):
        self.calc = CalcApi()

    def test_append_token(self):
        self.assertEqual([], self.calc._stack)

        result, error = self.calc._append_token('123,54')
        self.assertTrue(error)
        self.assertEqual('Not a number', result)

        result, error = self.calc._append_token('123.54')
        self.assertFalse(error)
        self.assertEqual('Add token success', result)
        self.assertEqual([123.54], self.calc._stack)

        result, error = self.calc._append_token('-')
        self.assertFalse(error)
        self.assertEqual('Add token success', result)

        result, error = self.calc._append_token('-157')
        self.assertFalse(error)
        self.assertEqual('Add token success', result)
        self.assertEqual([123.54, -157.0], self.calc._stack)
        self.assertEqual(['-'], self.calc._op_stack)

        for token in ['*', '(', '12.34', '+', '2', ')']:
            self.calc._append_token(token)
        self.assertEqual([123.54, -157.0, 12.34, 2, '+'], self.calc._stack)
        self.assertEqual(['-', '*'], self.calc._op_stack)

    def test_evalute(self):
        for token in ['123.54', '-', '-157', '*', '(', '12.34', '+', '2', ')']:
            self.calc._append_token(token)

        self.assertEqual((2374.92, False), self.calc._evalute())