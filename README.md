# The Unofficial Guide — Project 1

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This system cover student life, events and activites for GMU students and around the DMV area. This is particularly hard for student, especially incoming freshman, since GMU is mainly commuter school. If you commute to campus, you often don't get to spend as much time around people that know the place for parties, underground venue, or other fun (ideally low cost) entertainment activies around the DMV area.


---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/gmu | Anyone have any tips for incoming GMU freshman? | https://www.reddit.com/r/gmu/comments/1k9mks/anyone_have_any_tips_for_incoming_gmu_freshman/|
| 2 | r/gmu | Looking at going to gmu, what is there to do for fun around gmu?  | https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/ |
| 3 | Bond's Escape Room | Things to do near GMU Guide | https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide |
| 4 | GMU | Patriot Perk things to do | https://patriotperks.gmu.edu/things-to-do/ |
| 5 | GMU | Patriot Perk food and drinks | https://patriotperks.gmu.edu/food-drink/ |
| 6 | Blog | My 11 Favorite Things to Do in Fairfax, VA (From a Local) | https://virginiavacationguide.com/things-to-do-in-fairfax-va/ |
| 7 | DC's Website | Music Venues in DC | https://washington.org/visit-dc/live-music-venues-washington-dc |
| 8 | DC's Website | DC Bucket List | https://washington.org/visit-dc/bucket-list |
| 9 | DC's Website | DC Bucket List 2 | https://washington.org/visit-dc/your-washington-dc-summer-bucket-list |
| 10 | Blog | Things to do in Alexandria VA | https://www.funinfairfaxva.com/things-to-do-in-alexandria-va/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

Each chunk would have metadata.
- Links to the original post
- Name of the source
- Description/title of the post

**Chunk size:**

Semantic chunking using a three-level hierarchy:
1. **Markdown headers** (`#` – `######`) — each header and its content is kept together as the primary boundary.
2. **Paragraphs** — if a header section exceeds 150 words, it is split further on blank lines.
3. **Sentences** — if a paragraph still exceeds 150 words, it is split on sentence-ending punctuation.

Segments are grouped until a target of 100 words is reached (soft ceiling: 150 words hard cap). Min chunk size: 8 words.

**Overlap:**

No overlap. Header/paragraph/sentence boundaries already preserve context naturally, so sliding-window overlap is not needed.

**Reasoning:**

Most documents are guides and reviews with clear markdown section headers. Splitting at headers keeps each topic self-contained, which improves retrieval precision. A query about dining shouldn't pull in a chunk that mixes dining and live music just because of a fixed word window. Paragraph and sentence fallbacks handle the few sections that are too long to keep whole.

**Final chunk count:**
129 chunks from 10 documents.

**Sample chunks**
```
============================================================
DOC: DC Music Venues You Have to Experience
Total chunks: 10
============================================================

--- Chunk 1 (114 words) ---
## Check out the best places to go to catch a show in Washington, DC


When it comes to DC’s music legends, the landscape is as diverse as the city itself: Duke Ellington, Chuck Brown, Marvin Gaye, Ian MacKaye, Dave Grohl and Wale all share space atop the District’s musical Rushmore. Each artist has influenced the local landscape for years, but what’s the scene like these days?


With venues all over the city, it's time to discover what the DC music scene is all about. Whether you prefer jazz, go-go, hardcore punk, hip-hop, dance or anything in between, you can find it on any given night in the District at these live music meccas.

--- Chunk 2 (131 words) ---
### 01

#### 9:30 Club


The 9:30 Club has been at the forefront of the District’s music scene since its inception, and made its bones in the ‘80s hosting soon-to-shine acts including Chuck Brown, Red Hot Chili Peppers and The Police. Since moving to its current location in 1996, world famous acts like Bob Dylan, The Beastie Boys and Radiohead have graced its stage.

**815 V Street NW, Washington, DC 20001**

### 02

#### The Anthem


The Anthem solves the age-old problem prominent rockers and hot hip-hop stars face when performing in DC: What’s bigger than the legendary 9:30 Club but more intimate than an arena? The answer is the acoustically optimized, 6,000-seat concert hall operated by I.M.P. (of 9:30 Club fame).

Upcoming shows

**901 Wharf Street SW, Washington, DC 20024**

--- Chunk 3 (61 words) ---
### 03

#### Union Stage


Also located at The Wharf, Union Stage offers a slew of shows upon its reopening, including a wide range of independent acts. The intimate setting means you’ll get to enjoy a healthy dose of sound, and you can also order beers and pizza from their Tap Room.

**740 Water Street SW, Washington, DC 20024**

### 04

...

============================================================
DOC: Your DC Bucket List
Total chunks: 4
============================================================

--- Chunk 1 (102 words) ---
## There are just some things you NEED to do in the nation’s capital.


You don’t have to experience these in any order, but you do have to experience them all. Each activity illustrates how There’s Only One DC and many can be enjoyed for free.


*What’d we leave out? Does your DC Bucket List differ? Follow us on Instagram & TikTok and let us know your favorite activities in the District.*

### 01

#### See the Charters of Freedom: the U.S. Bill of Rights, the U.S. Constitution and the Declaration of Independence.


Plan a visit to the free National Archives Building.

--- Chunk 2 (117 words) ---
### 02

#### View the Star-Spangled Banner.


National Museum of American History

Experience the National Museum of American History for free.

### 04

#### See a show in DC.


Historic theaters include The John F. Kennedy Center for the Performing Arts and Ford’s Theatre.

### 05

#### Experience two museums and a beautiful courtyard, all in one building.


The Smithsonian American Art Museum and the National Portrait Gallery reside in the same building. After you tour both, hang out and have a bite to eat and some refreshments at the Kogod Courtyard.

### 06

#### Explore DC's distinct neighborhoods.


They're all worth exploring. Popular gathering spots include Georgetown, Southwest & The Wharf, Dupont Circle and U Street.
```


### Chunking Strategy Comparison

Chunking based on markdown header resulted in better result (lower distance score). It reduces the occurance of relevant information being split accross chunk boundary, i.e. a header and its corresponding section is kept together.

#### Chunking using fixed length (chunk_size = 100, overlap = 20, min_words = 8)
182 chunks from 10 documents.
```
Query: What are some popular live music venues around the DMV area?
ChromaDB not found — ingesting documents...
Stored 182 chunks from 10 documents.

  Top 7 chunks for: "What are some popular live music venues around the DMV area?"

  [1] distance: 0.3916
      source:   DC's Website — DC Music Venues You Have to Experience
      url:      https://washington.org/visit-dc/live-music-venues-washington-dc
      text:     ## Check out the best places to go to catch a show in Washington, DC When it comes to DC’s music legends, the landscape is as diverse as the city itself: Duke Ellington, Chuck Brown, Marvin Gaye, Ian MacKaye, Dave Grohl and Wale all share space atop the District’s musical Rushmore. Each artist has i...

  [2] distance: 0.4603
      source:   DC's Website — DC Music Venues You Have to Experience
      url:      https://washington.org/visit-dc/live-music-venues-washington-dc
      text:     music scene is all about. Whether you prefer jazz, go-go, hardcore punk, hip-hop, dance or anything in between, you can find it on any given night in the District at these live music meccas. #### 01 ### 9:30 Club The 9:30 Club has been at the forefront of the District’s music scene since its incepti...
```

#### Chunking based on markdown header. (target_words = 100, max_words = 150, min_words = 8)
129 chunks from 10 documents.
```
Query: What are some popular live music venues around the DMV area?

  Top 7 chunks for: "What are some popular live music venues around the DMV area?"

  [1] distance: 0.3831
      source:   DC's Website — DC Music Venues You Have to Experience
      url:      https://washington.org/visit-dc/live-music-venues-washington-dc
      text:     ## Check out the best places to go to catch a show in Washington, DC


When it comes to DC’s music legends, the landscape is as diverse as the city itself: Duke Ellington, Chuck Brown, Marvin Gaye, Ian MacKaye, Dave Grohl and Wale all share space atop the District’s musical Rushmore. Each artist has...

  [2] distance: 0.4368
      source:   DC's Website — DC Music Venues You Have to Experience
      url:      https://washington.org/visit-dc/live-music-venues-washington-dc
      text:     #### 01

#### 9:30 Club


The 9:30 Club has been at the forefront of the District’s music scene since its inception, and made its bones in the ‘80s hosting soon-to-shine acts including Chuck Brown, Red Hot Chili Peppers and The Police. Since moving to its current location in 1996, world famous acts l...
```

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
Lower chunk reduce token cost but might give the LLM too little context. Since the chunks are quite small and user might ask broad questions, I put the top-k = 7 so that the LLM can have more context at the expense of token cost.
I went with pure sementic search currently since it is the simplest solution, but a hybrid search with a keyword index using BM25 would be better.
all-MiniLM-L6-v2 is not as accurate as larger model but it is free and can be run locally.

### Retrival Test Result

The below retrival found music venues around DC that are relevant to the query.
```
Query: What are some popular live music venues around the DMV area?

  Top 7 chunks for: "What are some popular live music venues around the DMV area?"

  [1] distance: 0.3831
      source:   DC's Website — DC Music Venues You Have to Experience
      url:      https://washington.org/visit-dc/live-music-venues-washington-dc
      text:     ## Check out the best places to go to catch a show in Washington, DC


When it comes to DC’s music legends, the landscape is as diverse as the city itself: Duke Ellington, Chuck Brown, Marvin Gaye, Ian MacKaye, Dave Grohl and Wale all share space atop the District’s musical Rushmore. Each artist has...

  [2] distance: 0.4362
      source:   DC's Website — DC Music Venues You Have to Experience
      url:      https://washington.org/visit-dc/live-music-venues-washington-dc
      text:     ### 01

#### 9:30 Club


The 9:30 Club has been at the forefront of the District’s music scene since its inception, and made its bones in the ‘80s hosting soon-to-shine acts including Chuck Brown, Red Hot Chili Peppers and The Police. Since moving to its current location in 1996, world famous acts l...
```

The retrival found tips relevant to the query suggested by users on r/gmu.
```
Query: What are some advice to incoming freshman about joining the community at GMU?

  Top 7 chunks for: "What are some advice to incoming freshman about joining the community at GMU?"

  [1] distance: 0.3261
      source:   r/gmu — Anyone have any tips for incoming GMU freshman?
      url:      https://www.reddit.com/r/gmu/comments/1k9mks/anyone_have_any_tips_for_incoming_gmu_freshman/
      text:     # Anyone have any tips for incoming GMU freshman?

**UPVOTEMECUZCAPSLOCK** (OP): Tips can be everything from saying the best places to eat at campus or just some advice.

---

**DEMAG**: Going to class will get you a degree. Going to class and studying will get you a degree with honors.

It's amazin...

  [2] distance: 0.3452
      source:   Bond's Entertainment Center — Epic Things to Do Near GMU: Student Guide
      url:      https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide
      text:     #### Ready for Your Next Adventure?

Stop scrolling and start experiencing! Book your Bonds Escape Room adventure today — it's literally the most fun you can have near campus, and with that 20% student discount, it's basically a steal.
Reserve Your Spot Now!

🎯 Remember: The best things to do near G...
```

```
Query: What are some low-cost or free things to do near GMU's Fairfax campus on a weekend?

  Top 7 chunks for: "What are some low-cost or free things to do near GMU's Fairfax campus on a weekend?"

  [1] distance: 0.2161
      source:   r/gmu — Looking at going to gmu, what is there to do for fun around gmu?
      url:      https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/
      text:     # Looking at going to gmu, what is there to do for fun around gmu?

**owoqwertyowo** (OP): Title

---

**Starfire123547**: dont listen to these kids. As someone not entierly from the area (from richmond) the entierty of dc is at your finger tips. theres a free metro bus. so metro anything. (museams,...

  [2] distance: 0.2235
      source:   Bond's Entertainment Center — Epic Things to Do Near GMU: Student Guide
      url:      https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide
      text:     ## Epic Things to Do Near GMU: Break Out of the Study Grind

Stuck in the "study-sleep-repeat" cycle? Time to shake things up! Fairfax has way more cool stuff than most GMU students realize — escape rooms, cheap eats, nature spots, and hidden gems that even upperclassmen haven't tried. Best part? Mo...
```

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

```python
"""
You are a friendly and helpful local guide for George Mason University (GMU) students and the DMV area \
(DC, Maryland, Virginia).
Your knowledge comes exclusively from the retrieved sources provided below.

Rules:
1. Only recommend locations, events, or activities that appear in the retrieved sources.
2. For every recommendation, cite the source title and URL in your answer.
3. If the retrieved sources do not contain information that answers the question, say so clearly \
   and do not make up an answer.
4. If the question is outside your domain (GMU student life, local events, DMV-area dining and \
   activities), politely decline and explain your scope is limited to GMU and the DMV area.
5. Do not invent, hallucinate, or extrapolate beyond what the sources say.
6. Use the conversation history (prior messages) to understand follow-up questions, resolve \
   pronouns, and maintain continuity — but ground every answer in the current retrieved sources.\
"""
```

**Sample interaction**
How source attribution is surfaced in the response:

```
Question:
What are some popular live music venues around the DMV area?

Answer: 
There are several popular live music venues around the DMV area. In Washington, D.C., some notable venues include the 9:30 Club (https://washington.org/visit-dc/live-music-venues-washington-dc), The Anthem (https://washington.org/visit-dc/live-music-venues-washington-dc), Echostage (https://washington.org/visit-dc/live-music-venues-washington-dc), The Hamilton Live (https://washington.org/visit-dc/live-music-venues-washington-dc), and DC9 (https://washington.org/visit-dc/live-music-venues-washington-dc). 

In Fairfax, VA, the George Mason Eagle Bank Arena (https://virginiavacationguide.com/things-to-do-in-fairfax-va/) is a top entertainment venue that hosts various events, including concerts and sporting events.

These venues offer a range of music genres and experiences, from intimate settings to larger concert halls. You can find more information about each venue, including their schedules and locations, by visiting the provided URLs.
```

```
Question:
What are some advice to incoming freshman about joining the community at GMU?

Answer:
According to the sources, here are some advice for incoming freshmen about joining the community at GMU:

* Talk to your professors and be personal with them, as they will remember you when you need help (Source 1: https://www.reddit.com/r/gmu/comments/1k9mks/anyone_have_any_tips_for_incoming_gmu_freshman/).
* Attend classes and study to get a degree with honors, and also to understand the material better (Source 1: https://www.reddit.com/r/gmu/comments/1k9mks/anyone_have_any_tips_for_incoming_gmu_freshman/).
* Join a campus organization to find consistent activities and events (Source 5: https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/).
* Take advantage of on-campus perks such as free shows at the Center for the Arts and catching a game at EagleBank Arena (Source 7: https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide).
* Explore the local area, including Fairfax, to find fun things to do and make memories with friends (Source 2: https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide, Source 3: https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide, Source 4: https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/, Source 5: https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/).

These sources suggest that getting involved in the community, attending events, and exploring the local area can help incoming freshmen make the most of their time at GMU.
```

```
Question:
What's the best professor for MATH214

Answer:
The provided sources do not contain information about the best professor for MATH 214. The sources primarily discuss tips for incoming GMU freshmen, escape rooms, and discounts on food and activities for GMU students. They do not provide specific information about professors or courses.
```


---

## Interface

### Input Fields

| Field | Label | Description |
|-------|-------|-------------|
| **Query textbox** | "Your question" | Main text input where the user types a question. Placeholder reads "Ask about things to do, food, events…". Pressing **Enter** or clicking **Ask** submits the query. The box clears automatically after each submission. |
| **Ask button** | "Ask" | Submits the current query. Equivalent to pressing Enter in the textbox. |
| **New Chat button** | "New Chat" | Resets the entire session — clears conversation history, API message history, and the sources panel. |

### Output Fields

| Field | Label | Description |
|-------|-------|-------------|
| **Chatbot display** | "Conversation" | Scrollable chat window (450 px tall) that renders the full turn-by-turn conversation. User messages appear on the right; assistant responses appear on the left. Persists across turns until **New Chat** is clicked. |
| **Sources panel** | "Retrieved from" | Read-only, 4-line textbox beneath the query row. After each response it lists the titles and URLs of every document the retriever surfaced, so the user knows exactly which sources grounded the answer. |

### Sample Interaction Transcript

The transcript below shows one complete turn: user input → retrieval → grounded response → source attribution.

---

**Query textbox input**
```
What are some low-cost or free things to do near GMU's Fairfax campus on a weekend?
```

---

**Chatbot display — User turn**
```
What are some low-cost or free things to do near GMU's Fairfax campus on a weekend?
```

**Chatbot display — Assistant turn**
```
Here are some low-cost or free things to do near GMU's Fairfax campus on a weekend:

• **Explore DC for free** — hop on the free Metro bus and visit the Smithsonian museums,
  the National Mall monuments, and the National Archives (all free admission).
  (Source: r/gmu — "Looking at going to gmu, what is there to do for fun around gmu?")

• **Fair Lakes, Fair Oaks Mall, and Fairfax Corner** — nearby walkable areas for window
  shopping, people-watching, and inexpensive eats.
  (Source: r/gmu — "Looking at going to gmu, what is there to do for fun around gmu?")

• **Center for the Arts at GMU** — Mason students can grab up to two free tickets per
  show; check the schedule for concerts and performances.
  (Source: Epic Things to Do Near GMU: Student Guide —
   https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide)

• **EagleBank Arena on campus** — student discounts on sporting events, concerts, and
  comedy shows throughout the year.
  (Source: r/gmu — "Looking at going to gmu, what is there to do for fun around gmu?")

If you'd like more details on any of these, just ask!
```

---

**Sources panel output**
```
• r/gmu — Looking at going to gmu, what is there to do for fun around gmu?
  https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/

• Bond's Entertainment Center — Epic Things to Do Near GMU: Student Guide
  https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are some student discount available for GMU students? | The system provided discount from the official GMU Patriot Perk website gmu.edu/patriot-perk  | The system provided discount from Bonds Escape Room and r/gmu | Partially relevant (Fail to retrieve discount from gmu.edu/patriot-perk) | Accurate |
| 2 | What are some popular live music venues around the DMV area? |  System should name specific venues from the DC music venues source: 9:30 Club, The Anthem, Black Cat | The system provided music venues from DC and Virginia | Relevant | Accurate |
| 3 | What are some advice to incoming freshman about joining the community at GMU? | System should surface specific tips from the r/gmu threads. E.g., joining clubs, attending on-campus events and cite the Reddit sources | System recommended talking to professors, attending around campus and local area, and utilizing students discount | Relevant | Accurate |
| 4 | What are some low-cost or free things to do near GMU's Fairfax campus on a weekend? | System should recommend specific activities from the Fairfax VA and Patriot Perks sources | The system recommend  Fair Lakes, Fair Oaks Mall, or Fairfax Corner, and the on-campus student center | Relevant | Accurate |
| 5 | What's the best professor for MATH214 | System refuse to response since the question is outside its domain | System should refuse to response since the question is outside its domain | Off-target (question is not in domain) | Accurate  |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

The question `What are some student discount available for GMU students?` should have returned an answer with discount from gmu.edu/patriot-perk.

**Question that failed:**
What are some student discount available for GMU students?

**What the system returned:**
```
According to the sources, GMU students can enjoy various discounts. For instance, students can get a 20% discount at Bonds Escape Room (Source 5: https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide). Additionally, Mason students can grab up to two free tickets per show at the Center for the Arts (Source 7: https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide). Students can also get discounts at Eagle Bank events, including concerts and comedians (Source 2: https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/). Furthermore, students can enjoy a free movie ticket every month at the movie theater in University Mall (Source 2: https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/). It's also mentioned that students can get discounts by flashing their GMU ID at various spots, and by following spots on Instagram for flash sales and student promos (Source 1: https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide).

Retrieved from:
• Epic Things to Do Near GMU: Student Guide — https://bondsescaperoom.com/epic-things-to-do-near-gmu-student-guide
• Looking at going to gmu, what is there to do for fun around gmu? — https://www.reddit.com/r/gmu/comments/tdc7tz/looking_at_going_to_gmu_what_is_there_to_do_for/
```

**Root cause (tied to a specific pipeline stage):**
This is caused by the retrival function. Querying for "discount" doesn't seem to find match with result that has description like "15% off" using sementic search.

**What you would change to fix it:**
I would improve my retrival algorithm. Adding hybrid search using BM25 might include retrival quality.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec helped me allowed me to guide the AI agent rather then letting the AI agent guide me during implementation. I was able to detect divergence from the spec and rein the AI back. Additionally, the spec provided a lot of good context to the AI agent so that it doesn't hallucinate it's own idea of an implementation.

**One way your implementation diverged from the spec, and why:**
Initally, I had it in the spec that the chunking should be done with a fixed length windows, 150 words with 8 words overlap. After testing out the chunking, I saw that it was splitting a lot of contents accross boundary. I then decided to switch to splitting across the markdown header, since it is a natural 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

I gave to the Claude the list of links that I planned to use as the sources for my RAG engine and asked it to write me a web scraper. Claude gave me a scraper that put the content of each webpage in a markdown file with a metadata field in yaml. I had to manually copy a few of the website over. I also had to rewrite the scraping function to read predowloaded reddit thread json since reddit block the scraping script. 

**Instance 2**

I gave the Claude my initial plan for chunk_document(). Claude then produced a chunk document function that used a fixed chunk_size = 100, overlap = 20, min_words = 8. I tested this chunker and found that it split relevant content accross chunk boundary. So, I updated my spec to that document are split based on based on markdown header first before splitting based on word counts. This significantly improved retrival result. A more detailed comparison is included in the Chunking Strategy section.