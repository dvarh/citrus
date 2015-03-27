# coding: utf-8
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response

class CalcApi(APIView):
    def __init__(self, *args, **kwargs):
        self._stack = []
        self._op_stack = []
        self._prec = {
            '*': 3,
            '/': 3,
            '+': 2,
            '-': 2,
            '(': 1,
        }
        super(CalcApi, self).__init__(*args, **kwargs)

    def _evalute(self):
        def _execute_tokens(token, token_left, token_right):
            if token == "*":
                return token_left * token_right
            elif token == "/":
                return token_left / token_right
            elif token == "+":
                return token_left + token_right
            else:
                return token_left - token_right
        result = []
        while not self._op_stack  == []:
            self._stack.append(self._op_stack.pop())
        for token in self._stack:
            if token not in self._prec.keys(): result.append(token)
            else:
                token_right = result.pop()
                token_left = result.pop()
                result_token = _execute_tokens(token,token_left,token_right)
                result.append(result_token)
        return result.pop(), False

    def _append_token(self, token):
        if token not in self._prec.keys() and token != ')':
            try:
                token = int(token) if token.isdigit() else float(token)
            except ValueError as e:
                return 'Not a number', True
            self._stack.append(token)

        elif token == '(':
            self._op_stack.append(token)
        elif token == ')':
            topToken = self._op_stack.pop()
            while topToken != '(':
                self._stack.append(topToken)
                topToken = self._op_stack.pop()
        else:
            while not self._op_stack  == [] and \
               (self._prec[self._op_stack[-1]] >= self._prec[token]):
                  self._stack.append(self._op_stack.pop())
            self._op_stack.append(token)

        return 'Add token success', False

    def post(self, request):
        tokens = request.POST.getlist('tokens[]')
        for token in tokens:
            result, error = self._append_token(token)
            if error:
                return Response({'error': result})

        result, error = self._evalute()

        if error:
            return Response({'error': result})
        else:
            return Response({'response': result})

class CalcView(TemplateView):
    template_name = "base.html"