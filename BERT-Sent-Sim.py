#!pip install -U sentence-transformers

#download a pretrained model.
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

# Example in semantic search
from sentence_transformers import SentenceTransformer, util
import torch

embedder = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

# Corpus with example sentences (Tweets collected)
corpus = ['meidastouch payperview you dont have enough to pay me to listen to tuckers verbal flatulation halitosis',
          'a proven solution to naturally eliminate tonsil stones httpstcoldcndqzalt tonsilstones halitosis oralcare',
          'the genuinehalitosis coming from the mouth is also called intraoral halitosis oralmalodor or oralhalitosis',
          'dentist halitosis teeth how to get rid of bad breath.',
          'how to free yourself from halitosis forever',
          'tonsilloliths may produce no symptoms or they may be associated with halitosis bad breath or produce pain when swallowing',
          'halitosis is also associated with depression and symptoms of obsessive compulsive disorder',
          'halitosis can result in anxiety among those affected',
          'badbreath also known as halitosis is a symptom in which a noticeably unpleasant breathodour is present',
          'a timetested and natural remedy for gum disease one of the leading causes of badbreath',
          'are you self conscious of your bad breath a very common cause is dry mouth  learn how to manage your dry mouth symptoms amp keep your mouth healthy here',
          'bad breath learn how regular dental visits can help',
          'badbreath medically known as halitosis can be caused by poororalhygiene and can also be an indication of other healthissues you can detect the problem by purchasing badbreathmeasurement to have such products contact analyticalinnovations'
          ]
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

# Query sentences (Definitions)
queries = ['An offensive, foul breath odor resulting from a variety of causes such as poor oral hygiene, dental or oral infections, or the ingestion of certain foods. Noticeably unpleasant odors exhaled in breathing.']


# Find the closest sentences of the corpus for each query sentence based on cosine similarity
top_k = len(corpus)   # it depends on us
for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()

    #We use torch.topk to find the highest 5 scores
    top_results = torch.topk(cos_scores, k=top_k)

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop most similar sentences in corpus:")

    for score, idx in zip(top_results[0], top_results[1]):
        print(corpus[idx], "(Score: %.4f)" % (score))