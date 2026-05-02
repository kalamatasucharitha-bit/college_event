with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_route = '''@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    recommendations = []
    user_input = ""

    if request.method == "POST":
        user_input = request.form.get("interest", "").strip()

        if user_input:
            # Build a description for each event by combining its fields
            event_descriptions = [
                f"{e[\'name\']} {e.get(\'category\', \'\')} {e.get(\'description\', \'\')}"
                for e in events
            ]

            # Add user input as the first document
            all_text = [user_input] + event_descriptions

            # TF-IDF vectorization
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(all_text)

            # Cosine similarity: user input vs all events
            scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            # Attach score to each event and sort
            scored_events = [
                {**events[i], "score": round(float(scores[i]), 2)}
                for i in range(len(events))
            ]
            recommendations = sorted(scored_events, key=lambda x: x["score"], reverse=True)
            recommendations = [r for r in recommendations if r["score"] > 0.05][:4]

    return render_template("recommend.html", recommendations=recommendations, user_input=user_input)'''

new_route = '''@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    recommendations = []
    user_input = ""

    # Keyword expansion: maps user terms to richer domain keywords
    KEYWORD_EXPANSIONS = {
        "coding": "coding programming algorithm data structures competitive code software development",
        "code": "coding programming algorithm data structures competitive code software development",
        "programming": "coding programming algorithm competitive code software development",
        "robotics": "robotics robot autonomous engineering embedded sensors microcontroller",
        "robot": "robotics robot autonomous engineering embedded sensors microcontroller",
        "music": "music singing instrumental band guitar drums piano performance melody",
        "singing": "singing vocal voice song Bollywood classical music performance",
        "dance": "dance choreography performance classical hip hop contemporary freestyle",
        "gaming": "gaming esports tournament game competitive multiplayer",
        "hackathon": "hackathon hacking coding programming innovation build",
        "ai": "artificial intelligence machine learning deep learning neural network",
        "ml": "machine learning artificial intelligence deep learning Python TensorFlow",
        "web": "web development HTML CSS JavaScript React frontend backend",
        "drone": "drone robotics aerial flying engineering",
        "sport": "sports tournament athletic competition",
        "startup": "startup entrepreneurship pitch innovation business",
    }

    if request.method == "POST":
        user_input = request.form.get("interest", "").strip()

        if user_input:
            # Expand user input with synonym keywords
            expanded_input = user_input.lower()
            for keyword, expansion in KEYWORD_EXPANSIONS.items():
                if keyword in expanded_input:
                    expanded_input += " " + expansion

            # Build rich document per event (repeat category for weight)
            event_descriptions = [
                f"{e[\'name\']} {e.get(\'category\', \'\')} {e.get(\'category\', \'\')} {e.get(\'description\', \'\')}"
                for e in events
            ]

            all_text = [expanded_input] + event_descriptions

            # TF-IDF with bigrams for better phrase matching
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(all_text)
            scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            # Category boost: +0.15 if expansion keyword matches category
            scored_events = []
            for i, e in enumerate(events):
                score = float(scores[i])
                cat = e.get("category", "").lower()
                for keyword, expansion in KEYWORD_EXPANSIONS.items():
                    if keyword in expanded_input and keyword in (cat + " " + e.get("description","").lower()):
                        score = min(score + 0.12, 1.0)
                        break
                scored_events.append({**e, "score": round(score, 2)})

            recommendations = sorted(scored_events, key=lambda x: x["score"], reverse=True)
            recommendations = [r for r in recommendations if r["score"] > 0.02][:6]

    return render_template("recommend.html", recommendations=recommendations, user_input=user_input)'''

if old_route in content:
    content = content.replace(old_route, new_route, 1)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Recommend route updated")
else:
    # Try to find and show what's actually there
    idx = content.find('@app.route("/recommend"')
    if idx != -1:
        print("Found route at index", idx)
        print(repr(content[idx:idx+200]))
    else:
        print("FAILED: Could not find recommend route")
