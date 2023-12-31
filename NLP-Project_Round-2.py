# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1el1utCgTeA-Ti9efqI5JnvLJIYJk7nl3
"""

#importing the libraries
import spacy
import pandas as pd
from tabulate import tabulate
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
import re
from spacy import displacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Read the content of the book from the-kite-runner.txt
file = open("the-kite-runner.txt",encoding='utf-8')
wordslists = file.read().splitlines()
wordslists = [i for i in wordslists if i != ' ']
text = " "
text = text.join(wordslists)

#removing links from the text
text = re.sub(r'http\S+', '',text, flags=re.MULTILINE)
#removing unwanted email-ids from the text
text=re.sub(r'[A-Za-z0-9]*@[A-Za-z]*\.?[A-Za-z0-9]*', "", text)
#remove unwanted spaces
res = re.sub(' +', ' ', text)
text = str(res)


#removing all punctuationns from our text file
punctuations = '''!()-[]{};:'"\,<>./‘’?“”@#$%^&*_~'''
newtext = ""
for char in text:
    if char not in punctuations:
        newtext = newtext + char

newtext = newtext.lower()

# Process the text using spaCy
doc = nlp(newtext)


# Define entity types of interest
entity_types_of_interest = [
    "PER",
    "ORG",
    "LOC",
    "GPE",
    "FAC",
    "VEH",
]

# Extract entities and their types
entities = []
for ent in doc.ents:
    if ent.label_ in entity_types_of_interest:
        entities.append((ent.text, ent.label_))

# Sort entities by entity type
entities.sort(key=lambda x: x[1])

# Print the entities and their types in a tabular form
print(tabulate(entities, headers=["Entity", "Entity Type"], tablefmt="pretty"))

from IPython.core.display import display, HTML

randomPassageIndex = 6000
randomPassageIndex2 = 1000

passage = newtext[randomPassageIndex:randomPassageIndex + 3000] + " " + newtext[randomPassageIndex2:randomPassageIndex2+3000]
from google.colab.output import eval_js

from IPython.core.display import display, HTML
display(HTML(f"<div style='white-space: pre-wrap;'>{passage}</div>"))

passageEntityText = nlp(passage)
displacy.render(passageEntityText, style="ent", jupyter=True)

#total predicted entities = 53
correctEntities = 47
actualEntities = 50
predictedEntities = len(passageEntityText.ents)
# print(predictedEntities)
precision = correctEntities/predictedEntities
recall = correctEntities/actualEntities

F_Score = 2*precision*recall/(precision+recall);

print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F_Score: " + str(F_Score))

# Extract chapters
formatted_text = newtext.replace('the kite runner by khaled hosseini','#jaskaran#chapter')
formatted_text[:2000]


chapters = formatted_text.split("#jaskaran#")
print(chapters)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(chapters)

# Print the entire TF-IDF matrix
terms = vectorizer.get_feature_names_out()
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=terms, index=[f"Chapter {i+1}" for i in range(len(chapters))])

print("TF-IDF values for each chapter and term:")
print(tfidf_df)

# Calculate cosine similarity between chapters
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Visualize the similarity matrix as a gradient table

plt.figure(figsize=(15, 12))

# Subset of chapters (adjust the range accordingly)
subset_chapters = range(1, 20)

# Plot a subset of the similarity matrix
sns.heatmap(similarity_matrix[subset_chapters, :][:, subset_chapters], annot=True, cmap="viridis", xticklabels=subset_chapters, yticklabels=subset_chapters, fmt=".2f")

# Reduce font size
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.title("Chapter Similarity Matrix (Subset)")
plt.xlabel("Chapter")
plt.ylabel("Chapter")

plt.show()

