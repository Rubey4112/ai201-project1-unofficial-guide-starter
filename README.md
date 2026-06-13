# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

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
5. Do not invent, hallucinate, or extrapolate beyond what the sources say.\
"""
```

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

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

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
