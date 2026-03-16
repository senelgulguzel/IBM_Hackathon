from sentence_transformers import SentenceTransformer
model= SentenceTransformer('all-MiniLM-L6-v2')

vector = model.encode("This is a test sentence.")

print("vector length:" ,len(vector))