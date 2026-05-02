with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_events = """
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
"""

# Find the closing ] of the events list
# It should be a line that is just ']' after the last event dict
old_end = '    {"id":27,"name":"Techkriti"'
new_end = new_events + '    {"id":27,"name":"Techkriti"'

if old_end in content:
    content = content.replace(old_end, new_end, 1)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Events added before id:27")
else:
    # Try finding the closing bracket approach
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == ']' and i > 40 and i < 60:
            lines.insert(i, new_events)
            content = '\n'.join(lines)
            with open('app.py', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"SUCCESS: Events inserted at line {i}")
            break
    else:
        print("FAILED: Could not find insertion point")
        print("Looking for ']' lines between 40-60:")
        for i, line in enumerate(lines[40:65], start=40):
            print(f"  {i}: {repr(line)}")
