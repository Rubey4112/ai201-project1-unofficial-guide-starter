# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Student review of the physics classes at GMU. Engineering majors are required to take physics (up to physics 3) as part of their degree requirement. Words goes arround that the physics classes can be a bit "interesting," and for a foundational class such as physics, you really want a good instructors that maintain your interest while teaching.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | GMU | Physics Requirements for Electrical Engineer | https://catalog.gmu.edu/colleges-schools/engineering-computing/engineering/electrical-computer/electrical-engineering-bs/index.html#requirementstext |
| 2 | r/GMU |  | https://www.reddit.com/r/gmu/comments/7kfrp6/physics_major_at_gmu/ |
| 3 |Rate My Professor | Physics Professors Review| https://www.ratemyprofessors.com/search/professors/352?q=*&did=44 |
| 4 | GMU Physics Professor | Spring 2022 Phys 262 Syllabus | http://complex.gmu.edu/www-phys/phys262/ |
| 5 | Coursicle | Phys 262 Reviews | https://www.coursicle.com/gmu/courses/PHYS/262/ |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

Each chunk would have metadata.
- Links to the original post
- Name of the source
- Description/title of the post

**Chunk size:**

Recursive chunking with a size of 125 words.
Min words count of 8 words


**Overlap:**

8 words overlap

**Reasoning:**
RMP reviews would be fixed chunk, fitting the whole review. 
Syllabus would use recursive since the the syllabus is organized by topics.
Long Reddit post would likely get sementic since there is a shared themed through out the post but it might not be clearly defined.

But to keep it simple. I am going to use recursive chunking

Most of the document will be reviews, maybe some syllabus. Reviews are often short, less than 150 words. So each chunk should just be one reviews. Overlap really needed but it is there for the rare long reviews and the syllabus documents.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

I would use a hybrid serach model. Since if the user searches for a specific course with a course number i.e Phys 262, the retrival would need to find all document related to Phys 262.

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers

**Top-k:**
5-chunks

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What topics is covered in GMU Phys 262 | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Noisy and inconsistent documents is my biggest worry. The difference between a syllabus, a RMP review, and a reddit thread will likely cause my indexer to to index irrelevant content and fill the database.

2. My current plan for the chunking system is not that robust, it might split information, like the instructor who taught the class, between chunking.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

I am plannign to use Claude as myy AI peer coder. I plan to give it this planning document and have it poke holes into my plan so that I can see where in the plan I need to improve.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
