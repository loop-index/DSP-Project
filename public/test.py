from gensim.models import KeyedVectors

# Load the original file
model = KeyedVectors.load_word2vec_format('public\GoogleNews-vectors-negative300.bin', binary=True, limit=50000)
model.save_word2vec_format('public\w2v.bin', binary=True)