from .BaseDB import BaseDB
import random
import string
import os

class NaiveDB(BaseDB):
    def __init__(self):
        print("call init")

    def init_db(self):
        print("call_init")

    def load(self, file_path):
        print("call_load")

    def search(self, vector, n_results):
        print("call search")

    def init_from_docs(self, vectors, documents):
        print("call init from docs")