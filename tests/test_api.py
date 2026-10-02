from utils.ai_review import review_code


code = """
def add(a,b):
    return a+b

print(add(2,3))
"""


result = review_code(
    code,
    "Python"
)


print(result)