"""Defines functions for searching Google Books for book metadata.

"""
import string
import urllib.request
import json

API_KEY = "AIzaSyDwhT5rGIeLErTnNLdm8bOKgVHXa8-ev4I"

HOST = "https://www.googleapis.com"


def remove_punctuation(in_string):
    """Strips punctuation out of a string.
    
    Helper for get_isbn.
    
    """
    return "".join(ch for ch in in_string if not ch in string.punctuation)


def get_isbn(book):
    """Searches google books for the book in question and returns 
    the isbn of the closest match.

    """
    query = "/books/v1/volumes?q="
    search_terms = []

    for word in book.title.split():
        term = remove_punctuation(word)
        search_terms.append("intitle:"+term)

    for author in book.authors:
        term = remove_punctuation(author.first_name)
        search_terms.append("inauthor:"+term)
        term = remove_punctuation(author.last_name)
        search_terms.append("inauthor:"+term)

    search_string = "+".join(search_terms)
    key_string = "&key=" + API_KEY

    query += search_string
    query += "&maxResults=1"
    query += key_string
    
    con = urllib.request.urlopen(HOST+query)
    data = json.loads(con.read().decode())
    book = data['items'][0]
    book_info = book['volumeInfo']
    ids = book_info['industryIdentifiers']
    for identifier in ids:
        if identifier['type'] == "ISBN_13":
            isbn = identifier['identifier']

    return isbn
