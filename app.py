import csv
from flask import Flask, render_template, request, redirect, session, Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

CATEGORIES = ["sports","technical","cultural","gaming","workshop","seminar","entrepreneurship","professional"]

events = [
    {"id":1,"name":"All India Inter-University Boxing","date":"March 2026","venue":"Delhi","description":"National boxing championship open to all university teams.","category":"sports","image":"box.jpg","fee":0},
    {"id":2,"name":"HackTide","date":"Jan 7, 2026","venue":"Main Auditorium, Amrita University","description":"24-hour intensive hackathon to build innovative solutions.","category":"technical","image":"hacktide.png","fee":0},
    {"id":5,"name":"Elite Pitch Arena","date":"Jan 7, 2026","venue":"Innovation Hub, Amrita University","description":"Pitch your startup idea to investors. Win seed funding.","category":"entrepreneurship","image":"elite.png","fee":150},
    {"id":6,"name":"RAGNAROK — Valorant","date":"Jan 7, 2026","venue":"Gaming Arena, Amrita University","description":"Competitive Valorant tournament. 5-person squad battle.","category":"gaming","image":"valorant.jpeg","fee":0},
    {"id":7,"name":"RAGNAROK — Free Fire","date":"Jan 8, 2026","venue":"Gaming Arena, Amrita University","description":"Battle royale showdown. Form your squad.","category":"gaming","image":"freefire.jpeg","fee":0},
    {"id":8,"name":"Cine VFX Workshop","date":"Jan 9, 2026","venue":"Media Lab, Amrita University","description":"Industry-standard VFX compositing with expert guidance.","category":"cultural","image":"cinevfx.jpeg","fee":300},
    
    # Anokha Events
    {"id":9,"name":"RoboSumo - Anokha","date":"Feb 15, 2026","venue":"Amrita University, Coimbatore","description":"Design and build autonomous sumo robots to push opponents out of the ring.","category":"technical","image":"robosumo.png","fee":200},
    {"id":10,"name":"Lumiere - Anokha","date":"Feb 16, 2026","venue":"Main Stage, Amrita University","description":"The flagship cultural night of Anokha featuring fashion shows and music performances.","category":"cultural","image":"unveiling.png","fee":0},
    {"id":11,"name":"Smart City Hackathon","date":"Feb 15, 2026","venue":"Amrita University, Coimbatore","description":"Solve urban challenges using AI, IoT, and data analytics.","category":"technical","image":"root:smartcityhackathon.png","fee":100},

    # Pragati Events
    {"id":12,"name":"Pragati Pitchfest","date":"April 10, 2026","venue":"Amrita University, Amritapuri","description":"Pitch your disruptive startup ideas to top venture capitalists and angel investors.","category":"entrepreneurship","image":"buildthe.png","fee":150},
    {"id":13,"name":"Corporate Boardroom","date":"April 11, 2026","venue":"Amrita University, Amritapuri","description":"A simulated corporate boardroom experience to test your business acumen and strategy.","category":"professional","image":"strategy.png","fee":100},
    {"id":14,"name":"Pragati Trade Fair","date":"April 12, 2026","venue":"Amrita University, Amritapuri","description":"Showcase your startup products and services to thousands of students and faculty.","category":"entrepreneurship","image":"electro.png","fee":250},

    # Other Important Indian Events
    {"id":15,"name":"Techfest IIT Bombay","date":"Dec 27, 2026","venue":"IIT Bombay, Mumbai","description":"Asia's Largest Science and Technology Festival. Featuring exhibitions, lectures, and competitions.","category":"technical","image":"root:techfestiitbombay.jpg","fee":500},
    {"id":16,"name":"Mood Indigo","date":"Dec 20, 2026","venue":"IIT Bombay, Mumbai","description":"Asia's Largest College Cultural Festival. Four days of incredible performances, workshops, and competitions.","category":"cultural","image":"groove.png","fee":0},
    {"id":17,"name":"Sunburn Arena","date":"Dec 29, 2026","venue":"Vagator, Goa","description":"Asia's largest electronic dance music festival. Featuring top international DJs and artists.","category":"cultural","image":"lanparty.jpeg","fee":1500},
    {"id":18,"name":"Spardha","date":"Oct 15, 2026","venue":"IIT BHU, Varanasi","description":"Annual Sports Festival of IIT BHU. One of the largest collegiate sports festivals in India.","category":"sports","image":"root:spardha.jpg","fee":100},
    {"id":19,"name":"E-Summit IITM","date":"March 8, 2026","venue":"IIT Madras, Chennai","description":"Annual flagship entrepreneurship fest of IIT Madras, inspiring the next generation of innovators.","category":"entrepreneurship","image":"elite.png","fee":200},
    {"id":20,"name":"Smart India Hackathon","date":"Aug 15, 2026","venue":"Multiple Nodal Centers, India","description":"World's biggest open innovation model, addressing challenges faced by various ministries and departments.","category":"technical","image":"root:smartindiahackathon.jpeg","fee":0},
    {"id":21,"name":"DevFest India","date":"Nov 10, 2026","venue":"Bengaluru","description":"Community-led developer events hosted by Google Developer Groups across India.","category":"seminar","image":"mobile.png","fee":0},
    {"id":22,"name":"India Game Developer Conference","date":"Nov 5, 2026","venue":"HICC, Hyderabad","description":"India's premier game developer conference featuring talks, workshops, and awards.","category":"gaming","image":"gamedev.png","fee":500},

    # Additional 2025-2026 Events
    {"id":23,"name":"Oasis 2025","date":"Oct 24, 2025","venue":"BITS Pilani, Rajasthan","description":"One of India's largest college cultural festivals, featuring music, dance, and art.","category":"cultural","image":"https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=800&auto=format&fit=crop","fee":0},
    {"id":24,"name":"Rendezvous 2025","date":"Oct 10, 2025","venue":"IIT Delhi, New Delhi","description":"Annual cultural festival of IIT Delhi, hosting spectacular pro-nights and competitions.","category":"cultural","image":"https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=800&auto=format&fit=crop","fee":0},
    {"id":25,"name":"Inter-IIT Sports Meet","date":"Dec 14, 2025","venue":"IIT Bombay, Mumbai","description":"The annual sports tournament where all IITs compete for the General Championship.","category":"sports","image":"https://images.unsplash.com/photo-1461896836934-ffe607ba8211?q=80&w=800&auto=format&fit=crop","fee":0},
    {"id":26,"name":"Kurukshetra","date":"Feb 18, 2026","venue":"Anna University, Chennai","description":"International techno-management fest organized by CEG, Anna University under UNESCO patronage.","category":"technical","image":"root:kurukshetra.jpg","fee":100},

    # Coding Events
    {"id":28,"name":"Code Relay","date":"Feb 20, 2026","venue":"CS Lab, Amrita University","description":"Team coding relay race. Each member solves a coding programming challenge using algorithms data structures competitive programming.","category":"technical","image":"hacktide.png","fee":0},
    {"id":29,"name":"LeetCode Championship","date":"March 5, 2026","venue":"Online / Amrita","description":"Competitive coding programming contest. Solve algorithmic data structure problems. coding programming competitive algorithms.","category":"technical","image":"genai.png","fee":0},
    {"id":30,"name":"Open Source Hackathon","date":"April 2, 2026","venue":"Innovation Lab, Amrita","description":"Contribute to open source projects coding programming software development GitHub collaboration pull requests.","category":"technical","image":"build2.png","fee":0},
    {"id":31,"name":"AI & ML Bootcamp","date":"March 18, 2026","venue":"AI Lab, Amrita University","description":"Hands-on machine learning artificial intelligence deep learning coding Python TensorFlow neural networks workshop.","category":"workshop","image":"aidriven.png","fee":200},
    {"id":32,"name":"Web Dev Sprint","date":"Feb 25, 2026","venue":"CS Dept, Amrita","description":"Build a complete web application in 6 hours. coding programming HTML CSS JavaScript React frontend backend development.","category":"technical","image":"smartiot.png","fee":0},

    # Robotics Events
    {"id":33,"name":"RoboMaze Challenge","date":"March 10, 2026","venue":"Robotics Lab, Amrita","description":"Navigate an autonomous robot through a maze. robotics autonomous robot programming engineering sensors microcontroller design.","category":"technical","image":"robomastry.png","fee":300},
    {"id":34,"name":"Line Follower Bot","date":"Feb 28, 2026","venue":"Electronics Lab, Amrita","description":"Build a robot that follows a line autonomously. robotics electronics embedded systems engineering microcontroller Arduino.","category":"technical","image":"roborally.png","fee":150},
    {"id":35,"name":"Drone Racing Championship","date":"April 5, 2026","venue":"Open Ground, Amrita","description":"FPV drone racing robotics aerial engineering competition. Build and race your own drone robotics automation speed.","category":"technical","image":"flight.png","fee":500},
    {"id":36,"name":"RoboBlaze Combat","date":"Feb 15, 2026","venue":"Amrita University, Coimbatore","description":"Combat robotics battle arena. Design and build fighting robots engineering electronics battle competition championship.","category":"technical","image":"roboblaze.png","fee":400},
    {"id":37,"name":"IoT Smart Systems Workshop","date":"March 22, 2026","venue":"IoT Lab, Amrita","description":"Build Internet of Things robotics smart systems embedded electronics sensors automation programming connected devices.","category":"workshop","image":"agenticaiot.png","fee":100},

    # Music Events
    {"id":38,"name":"Battle of Bands","date":"March 15, 2026","venue":"Amphitheatre, Amrita","description":"Live band music competition. rock pop indie fusion music singing instruments guitar drums bass performance.","category":"cultural","image":"groove.png","fee":0},
    {"id":39,"name":"Solo Instrumental Night","date":"Feb 22, 2026","venue":"Music Room, Amrita","description":"Classical contemporary solo music instrumental performance guitar violin piano keyboard flute sitar music.","category":"cultural","image":"sony.png","fee":0},
    {"id":40,"name":"Music Production Workshop","date":"April 8, 2026","venue":"Media Lab, Amrita","description":"Learn music production beat making mixing mastering DJ electronic music composition software studio recording.","category":"workshop","image":"electro.png","fee":250},
    {"id":41,"name":"A Cappella Showdown","date":"March 28, 2026","venue":"Main Auditorium, Amrita","description":"Group vocal harmony singing music performance without instruments a cappella choir ensemble acapella.","category":"cultural","image":"power.png","fee":0},

    # Dance Events
    {"id":42,"name":"Dance Fusion","date":"Feb 18, 2026","venue":"Main Stage, Amrita","description":"Group dance competition. classical contemporary fusion hip hop freestyle street dance choreography performance.","category":"cultural","image":"paintyour.png","fee":0},
    {"id":43,"name":"Solo Dance Championship","date":"March 8, 2026","venue":"Open Stage, Amrita","description":"Solo dance performance Bharatanatyam Kathak western hip hop freestyle contemporary dance choreography.","category":"cultural","image":"farmfiesta.png","fee":0},
    {"id":44,"name":"Flash Mob","date":"April 10, 2026","venue":"Campus Ground, Amrita","description":"Surprise flash mob dance group choreography fun entertainment public performance synchronised dance.","category":"cultural","image":"unveiling.png","fee":0},
    {"id":45,"name":"Nukkad Natak & Dance Drama","date":"March 20, 2026","venue":"Campus Grounds, Amrita","description":"Street play combined with dance drama acting cultural performance choreography expression theatre.","category":"cultural","image":"causes.png","fee":0},

    # Singing Events
    {"id":46,"name":"Singing Star","date":"Feb 24, 2026","venue":"Auditorium, Amrita","description":"Solo singing vocal competition. Bollywood classical western pop singing voice performance talent stage.","category":"cultural","image":"quiz.png","fee":0},
    {"id":47,"name":"Antakshari","date":"March 1, 2026","venue":"Open Hall, Amrita","description":"Classic Bollywood singing song competition team antakshari voice music vocal performance entertainment.","category":"cultural","image":"campusquest.png","fee":0},
    {"id":48,"name":"Western Vocals Night","date":"April 15, 2026","venue":"Amphitheatre, Amrita","description":"Western English singing vocal performance pop rock jazz soul singing competition night.","category":"cultural","image":"winter.png","fee":0},
    {"id":49,"name":"Sur Sangam","date":"March 25, 2026","venue":"Music Hall, Amrita","description":"Classical singing Carnatic Hindustani vocal music competition devotional spiritual raga singing performance.","category":"cultural","image":"stargazing.png","fee":0},
    {"id":27,"name":"Techkriti","date":"March 12, 2026","venue":"IIT Kanpur, Uttar Pradesh","description":"Annual inter-collegiate technical and entrepreneurship festival.","category":"technical","image":"root:techkriti.jpg","fee":150},
]

# ========= DSA: Linked List Node =========
class Node:
    def __init__(self, name, roll_no, branch, department, year, email, phone, event):
        self.name=name; self.roll_no=roll_no; self.branch=branch
        self.department=department; self.year=year; self.email=email
        self.phone=phone; self.event=event; self.next=None

# ========= DSA: Hash Map (separate chaining) for duplicate detection =========
class ParticipantHashMap:
    def __init__(self, capacity=64):
        self.capacity=capacity
        self.table=[[] for _ in range(capacity)]
    def _hash(self,key):
        h=0
        for ch in key: h=(h*31+ord(ch))%self.capacity
        return h
    def put(self,roll_no,event_name):
        idx=self._hash(roll_no); bucket=self.table[idx]
        for entry in bucket:
            if entry[0]==roll_no: entry[1].add(event_name); return
        bucket.append([roll_no,{event_name}])
    def has_registered(self,roll_no,event_name):
        for entry in self.table[self._hash(roll_no)]:
            if entry[0]==roll_no: return event_name in entry[1]
        return False
    def remove_event(self,roll_no,event_name):
        for entry in self.table[self._hash(roll_no)]:
            if entry[0]==roll_no: entry[1].discard(event_name)

head=None; stack=[]; reg_map=ParticipantHashMap()

def insert_participant(data,event_name):
    global head
    n=Node(data["name"],data["roll_no"],data["branch"],data["department"],data["year"],data["email"],data["phone"],event_name)
    if head is None: head=n
    else:
        t=head
        while t.next: t=t.next
        t.next=n
    stack.append(n); reg_map.put(data["roll_no"],event_name); return n

def get_participants():
    t=head; r=[]
    while t: r.append(t); t=t.next
    return r

def undo_participant():
    global head,stack
    if not stack: return "Nothing to undo"
    last=stack.pop(); reg_map.remove_event(last.roll_no,last.event)
    if head==last: head=head.next; return f"{last.name} removed"
    t=head
    while t.next and t.next!=last: t=t.next
    if t.next==last: t.next=last.next
    return f"{last.name} removed from {last.event}"

def delete_participant(name):
    global head
    if head is None: return "List empty"
    if head.name.lower()==name.lower():
        reg_map.remove_event(head.roll_no,head.event); head=head.next; return f"{name} deleted"
    t=head
    while t.next:
        if t.next.name.lower()==name.lower():
            reg_map.remove_event(t.next.roll_no,t.next.event); t.next=t.next.next; return f"{name} deleted"
        t=t.next
    return "Participant not found"

def get_event_stats():
    stats={}; t=head
    while t: stats[t.event]=stats.get(t.event,0)+1; t=t.next
    return stats

def find_event(event_id):
    return next((e for e in events if e["id"]==event_id),None)

def check_admin(): return session.get("admin_logged_in")

@app.route("/admin/login",methods=["GET","POST"])
def admin_login():
    error=None
    if request.method=="POST":
        if request.form["username"]==ADMIN_USERNAME and request.form["password"]==ADMIN_PASSWORD:
            session["admin_logged_in"]=True; return redirect("/admin")
        error="Invalid username or password"
    return render_template("admin_login.html",error=error)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in",None); return redirect("/admin/login")

@app.route("/")
def home(): return render_template("index.html",events=events)

@app.route("/fests")
def fests(): return render_template("fests.html")

@app.route("/anokha")
def anokha(): return render_template("anokha.html")

@app.route("/pragati")
def pragati(): return render_template("pragati.html")

@app.route("/admin")
def admin_dashboard():
    if not check_admin(): return redirect("/admin/login")
    return render_template("admin_dashboard.html",events=events,participants=get_participants())

@app.route("/admin/events",methods=["GET","POST"])
def admin_events():
    if not check_admin(): return redirect("/admin/login")
    if request.method=="POST":
        cat=request.form["category"]
        if cat not in CATEGORIES: CATEGORIES.append(cat)
        fee_raw=request.form.get("fee","0").strip()
        try: fee=int(fee_raw) if fee_raw else 0
        except: fee=0
        events.append({"id":len(events)+1,"name":request.form["name"],"date":request.form["date"],"venue":request.form["venue"],"description":request.form["description"],"category":cat,"image":request.form.get("image") or "default.jpg","fee":fee})
    return render_template("admin_events.html",events=events,categories=CATEGORIES)

@app.route("/admin/delete_event/<int:event_id>")
def delete_event(event_id):
    if not check_admin(): return redirect("/admin/login")
    global events; events=[e for e in events if e["id"]!=event_id]; return redirect("/admin/events")

@app.route("/admin/edit_event/<int:event_id>",methods=["GET","POST"])
def edit_event(event_id):
    if not check_admin(): return redirect("/admin/login")
    event=find_event(event_id)
    if request.method=="POST":
        event["name"]=request.form["name"]; event["date"]=request.form["date"]
        event["venue"]=request.form["venue"]; event["description"]=request.form["description"]
        event["category"]=request.form["category"]
        try: event["fee"]=int(request.form.get("fee","0").strip() or 0)
        except: event["fee"]=0
        return redirect("/admin/events")
    return render_template("edit_event.html",event=event)

@app.route("/admin/registrations",methods=["GET","POST"])
def admin_registrations():
    if not check_admin(): return redirect("/admin/login")
    participants=get_participants(); message=None
    selected_event=request.form.get("event_filter"); search_name=request.form.get("search_name")
    if search_name:
        participants=[p for p in participants if search_name.lower() in p.name.lower()]
        message=f"Search results for '{search_name}'"
    if selected_event:
        participants=[p for p in participants if p.event==selected_event]
    return render_template("admin_registrations.html",participants=participants,total=len(participants),events=events,message=message)

@app.route("/admin/delete_participant",methods=["POST"])
def admin_delete_participant():
    if not check_admin(): return redirect("/admin/login")
    delete_participant(request.form["name"]); return redirect("/admin/registrations")

@app.route("/admin/export_csv")
def export_csv():
    if not check_admin(): return redirect("/admin/login")
    def generate():
        yield "Name,Roll No,Branch,Department,Year,Email,Phone,Event\n"
        for p in get_participants():
            yield f"{p.name},{p.roll_no},{p.branch},{p.department},{p.year},{p.email},{p.phone},{p.event}\n"
    return Response(generate(),mimetype="text/csv",headers={"Content-Disposition":"attachment;filename=participants.csv"})

@app.route("/admin/analytics")
def admin_analytics():
    if not check_admin(): return redirect("/admin/login")
    return render_template("admin_analytics.html",stats=get_event_stats())

@app.route("/category/<type>")
def category(type):
    return render_template("category.html",events=[e for e in events if e.get("category")==type],category=type)

@app.route("/event/<int:event_id>")
def event_detail(event_id):
    return render_template("events.html",event=find_event(event_id))

@app.route("/search")
def search():
    q=request.args.get("query","").lower()
    filtered=[e for e in events if q in e["name"].lower() or q in e.get("category","").lower() or q in e.get("venue","").lower()]
    return render_template("category.html",events=filtered,category="Search Results")

# ========= FIX: /registration route was MISSING =========
@app.route("/registration",methods=["GET","POST"])
def registration_home():
    profile=session.get("profile"); message=None; participants=[]
    if request.method=="POST":
        if "roll_no" in request.form:
            data={"name":request.form.get("name","").strip(),"roll_no":request.form.get("roll_no","").strip(),
                  "branch":request.form.get("branch","").strip(),"department":request.form.get("department","").strip(),
                  "year":request.form.get("year","").strip(),"email":request.form.get("email","").strip(),
                  "phone":request.form.get("phone","").strip()}
            if all(data.values()):
                session["profile"] = data
                return redirect("/registration")
            else:
                message = "All fields are required to create a profile."
                return render_template("create_profile.html", error=message)
        else:
            sn=request.form.get("search_name","").strip()
            if sn:
                participants=[p for p in get_participants() if sn.lower() in p.name.lower()]
                message=f"Results for '{sn}'"
                
    if not profile:
        return render_template("create_profile.html", error=message)
            
    registered_events = []
    if profile:
        registered_event_names = [p.event for p in get_participants() if p.roll_no == profile.get("roll_no")]
        registered_events = [e for e in events if e["name"] in registered_event_names]
        
    return render_template("registration_home.html",profile=profile,events=events,participants=participants,message=message,registered_events=registered_events)

@app.route("/register/<int:event_id>",methods=["GET","POST"])
def register_event(event_id):
    event=find_event(event_id)
    if not event: return redirect("/")
    profile=session.get("profile"); fee=event.get("fee",0)
    error=None; success=None; show_payment=False

    if request.method=="POST":
        data={"name":request.form.get("name","").strip(),"roll_no":request.form.get("roll_no","").strip(),
              "branch":request.form.get("branch","").strip(),"department":request.form.get("department","").strip(),
              "year":request.form.get("year","").strip(),"email":request.form.get("email","").strip(),
              "phone":request.form.get("phone","").strip()}

        if not all(data.values()):
            error="All fields are required."
        elif reg_map.has_registered(data["roll_no"],event["name"]):
            error="You have already registered for this event!"
        else:
            session["profile"]=data; profile=data
            if fee and fee>0:
                if request.form.get("payment_confirmed")=="yes":
                    insert_participant(data,event["name"])
                    success=f"Registered for {event['name']}! Payment confirmed."
                else:
                    show_payment=True
            else:
                insert_participant(data,event["name"])
                success=f"Registered for {event['name']}! Details sent to organiser."

    return render_template("registration.html",event=event,fee=fee,profile=profile,
                           participants=get_participants(),error=error,success=success,show_payment=show_payment)

@app.route("/undo/<int:event_id>")
def undo(event_id):
    msg=undo_participant(); event=find_event(event_id)
    fee=event.get("fee",0) if event else 0
    return render_template("registration.html",event=event,fee=fee,profile=session.get("profile"),
                           participants=get_participants(),message=msg,error=None,success=None,show_payment=False)

@app.route("/clear_profile")
def clear_profile():
    session.pop("profile",None); return redirect("/registration")

@app.route("/recommend", methods=["GET", "POST"])
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
                f"{e['name']} {e.get('category', '')} {e.get('category', '')} {e.get('description', '')}"
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

    return render_template("recommend.html", recommendations=recommendations, user_input=user_input)

if __name__=="__main__":
    app.run(debug=True)
