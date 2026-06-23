from flask import Flask, request

app = Flask(__name__)

# -------------------------
# Naive Search
# -------------------------
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


# -------------------------
# KMP Search
# -------------------------
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)

    lps = compute_lps(pattern)

    matches = []
    comparisons = 0

    i = j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and j < m and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


# -------------------------
# Rabin Karp Search
# -------------------------
def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)

    if m > n:
        return [], 0

    d = 256

    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:

            for k in range(m):
                comparisons += 1

                if text[s + k] != pattern[k]:
                    break

            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# -------------------------
# Home Page
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    result = ""

    if request.method == "POST":

        text = request.form["text"]
        pattern = request.form["pattern"]

        if pattern and len(pattern) <= len(text):

            m1, c1 = naive_search(text, pattern)
            m2, c2 = kmp_search(text, pattern)
            m3, c3 = rabin_karp(text, pattern)

            result = f"""
Text:    {text}
Pattern: {pattern}

Naive  -> Matches at: {m1}, Comparisons: {c1}
KMP    -> Matches at: {m2}, Comparisons: {c2}
RK     -> Matches at: {m3}, Comparisons: {c3}
"""

        else:
            result = "Pattern length should be less than or equal to Text length."

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>String Matching Algorithms</title>
        <style>
            body {{
                font-family: Arial;
                margin: 40px;
            }}
            input {{
                width: 500px;
                padding: 8px;
                margin: 5px;
            }}
            button {{
                padding: 10px 20px;
            }}
            pre {{
                background: #f4f4f4;
                padding: 15px;
            }}
        </style>
    </head>
    <body>

        <h1>String Matching Algorithm Comparison</h1>

        <form method="POST">

            <label><b>Enter Text:</b></label><br>
            <input type="text" name="text" required><br><br>

            <label><b>Enter Pattern:</b></label><br>
            <input type="text" name="pattern" required><br><br>

            <button type="submit">Search</button>

        </form>

        <br>

        <pre>{result}</pre>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
