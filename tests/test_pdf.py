from utils.pdf_generator import generate_pdf

result = {
    "score":95,
    "bugs":1,
    "suggestions":3,
    "review":"Excellent code. Add exception handling."
}

path = generate_pdf(
    "sample_code",
    "Python",
    result
)

print(path)