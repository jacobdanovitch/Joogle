import nltk
import os

# https://stackoverflow.com/a/22255432
root_dir = os.path.join(os.path.abspath(os.sep), "nltk_data")

nltk.download('wordnet', download_dir=root_dir)
nltk.download('stopwords', download_dir=root_dir)

