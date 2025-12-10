from flask import Flask, render_template, request
from collections import defaultdict
import string
import re

app = Flask(__name__)

def mapper(teks):
    mapped = []
    for c in teks.lower():
        if c in string.ascii_lowercase:
            mapped.append((c, 1))
    return mapped

def shuffle(mapped_data):
    shuffled = defaultdict(list)
    for key, value in mapped_data:
        shuffled[key].append(value)
    return shuffled

def reducer(shuffled_data):
    reduced = {}
    for key, values in shuffled_data.items():
        reduced[key] = sum(values)
    return reduced

def hadoop_freq_count(teks):
    mapped = mapper(teks)
    shuffled = shuffle(mapped)
    reduced = reducer(shuffled)
    return dict(sorted(reduced.items()))


def bersihkan(teks):
    return re.sub(r'[^A-Za-z]', '', teks).lower()

def palindrome_similarity(teks):
    clean = bersihkan(teks)
    n = len(clean)

    if n == 0:
        return 0, clean

    cocok = 0
    total = n

    for i in range(n):
        if clean[i] == clean[n - 1 - i]:
            cocok += 1

    similarity = (cocok / total) * 100
    return round(similarity, 2), clean


def caesar_encrypt(teks, shift=3):
    hasil = ""
    for c in teks:
        if c.isalpha():
            start = ord('A') if c.isupper() else ord('a')
            hasil += chr((ord(c) - start + shift) % 26 + start)
        else:
            hasil += c
    return hasil

def caesar_decrypt(teks, shift=3):
    return caesar_encrypt(teks, -shift)


def vigenere_encrypt(teks, key):
    hasil = ""
    key = key.lower()
    idx = 0

    for c in teks:
        if c.isalpha():
            shift = ord(key[idx % len(key)]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            hasil += chr((ord(c) - base + shift) % 26 + base)
            idx += 1
        else:
            hasil += c
    return hasil


def vigenere_decrypt(teks, key):
    hasil = ""
    key = key.lower()
    idx = 0

    for c in teks:
        if c.isalpha():
            shift = ord(key[idx % len(key)]) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            hasil += chr((ord(c) - base - shift) % 26 + base)
            idx += 1
        else:
            hasil += c
    return hasil


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hitung-freq", methods=["GET", "POST"])
def hitung_freq():
    hasil = {}
    teks = ""

    if request.method == "POST":
        teks = request.form.get("teks", "")
        hasil = hadoop_freq_count(teks)

    return render_template("hitung-freq.html", hasil=hasil, teks=teks)

@app.route("/palindrome-checker", methods=["GET", "POST"])
def palindrome_checker():
    hasil = None
    cleaned = ""

    if request.method == "POST":
        teks = request.form.get("teks", "")
        similarity, cleaned = palindrome_similarity(teks)
        hasil = similarity
    return render_template("palindrome-checker.html", hasil=hasil, cleaned=cleaned)

@app.route("/transformasi-kata", methods=["GET", "POST"])
def transformasi_kata():
    hasil = ""
    teks = ""
    mode = ""
    key = ""
    shift = None

    if request.method == "POST":
        teks = request.form.get("teks", "")
        mode = request.form.get("mode", "")

        if mode == "caesar_encrypt":
            shift = int(request.form.get("shift", 3))
            hasil = caesar_encrypt(teks, shift)

        elif mode == "caesar_decrypt":
            shift = int(request.form.get("shift", 3))
            hasil = caesar_decrypt(teks, shift)

        elif mode == "vigenere_encrypt":
            key = request.form.get("key", "")
            hasil = vigenere_encrypt(teks, key)

        elif mode == "vigenere_decrypt":
            key = request.form.get("key", "")
            hasil = vigenere_decrypt(teks, key)

    return render_template("transformasi-kata.html", hasil=hasil)


if __name__ == "__main__":
    app.run(debug=True)
