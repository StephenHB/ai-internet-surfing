"""
The module is used to extract web information 
into text, and summarize to an abstract.
"""
from heapq import nlargest
from numpy import extract
import requests
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from bs4 import BeautifulSoup

class extractandsummary:
    def __init__(self):
        self.url = None

    def get_web_info(self,content_to_return:str)->str:
        """
        Use re to extract the content from the url
        Input: 
            content_to_return (str): "title", "content"
        Output:
            extract_info (str): output based on selection
        """
        url = self.url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if content_to_return == "title":
            extract_info = soup.find(id="firstHeading")
        elif content_to_return == "content":
            extract_info = ""
            for paragraph in soup.find_all('p'):
                extract_info += paragraph.text

        return extract_info

    def summarize(self, text:str, per:float = 0.01)->str:
        """
        Summarize the str from the get_web_info, and summarize
        Inputs:
            text: input text
            per: the percentage (0 to 1) of sentences you want to extract, 
                the default is 1%.
        Outputs:
            summary (str): summarized results
        """
        nlp = spacy.load('en_core_web_sm')
        doc= nlp(text)
        tokens=[token.text for token in doc]
        word_frequencies={}
        for word in doc:
            if word.text.lower() not in list(STOP_WORDS):
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        max_frequency=max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word]=word_frequencies[word]/max_frequency
        sentence_tokens= [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():                            
                        sentence_scores[sent]=word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent]+=word_frequencies[word.text.lower()]
        select_length=int(len(sentence_tokens)*per)
        summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)

        return summary

