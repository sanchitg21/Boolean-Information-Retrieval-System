# fquery means formatted query. This document takes care of the paranthesis and 
# the precedance for the boolean operators and paranthesis in the query.

def is_Lparanthesis(query_token):
    if query_token == "(":
        return True
    return False

def is_Rparanthesis(query_token):
    if query_token == ")":
        return True
    return False

def is_binaryoperator(query_token):
    if query_token == "&" or query_token == "|":
        return True
    return False

def convert(query_token):
    
    # Converts an infix query into postfix
    stack = []
    order = list()

    for token in query_token:
        if is_binaryoperator(token):
            while len(stack) and (preference(token) <= preference(stack[-1])):
                order.append(stack.pop())
            stack.append(token)
        
        elif is_Lparanthesis(token):
            stack.append(token)

        elif is_Rparanthesis(token):
            while len(stack) and stack[-1] != "(":
                order.append(stack[-1]) 
                stack.pop()
            if len(stack) and stack[-1] != "(":
                raise ValueError("Query is not formed correctly!")
            else:
                stack.pop()
                
        else:
            order.append(token)

    while len(stack):
        order.append(stack.pop())
            
    return order

def preference(query_token):
    preference_order = {"&": 1, "|": 0}
    if query_token == "&" or query_token == "|":
        return preference_order[query_token]
    return -1