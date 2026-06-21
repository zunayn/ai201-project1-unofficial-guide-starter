# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

**Texas State University CS & Engineering Survival Guide.** This system covers the unofficial, student-generated knowledge required to navigate the Computer Science and Engineering programs at TXST. This knowledge is valuable because official course catalogs don't reflect teaching styles, real weekly time commitments for projects, or the physical realities of the campus (like which buildings have the best study spots or worst conditions).

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | r/txstate thread | Reddit Discussion | `docs/reddit_cs3358.txt` |
| 2 | r/txstate thread | Reddit Discussion | `docs/reddit_prof_recommendations.txt` |
| 3 | r/txstate thread | Reddit Discussion | `docs/reddit_cs3339.txt` |
| 4 | r/txstate thread | Reddit Discussion | `docs/reddit_derrick_hall_demo.txt` |
| 5 | r/txstate thread | Reddit Discussion | `docs/reddit_derrick_vs_ingram.txt` |
| 6 | r/txstate thread | Reddit Discussion | `docs/reddit_parking_commute.txt` |
| 7 | r/txstate thread | Reddit Discussion | `docs/reddit_study_spots.txt` |
| 8 | Rate My Professors | Review | `docs/rmp_koh_assembly.txt` |
| 9 | CS Discord | Chat Export | `docs/discord_cs_survival.txt` |
| 10| Rate My Professors | Review | `docs/rmp_seaman_cs.txt` |

---

## Chunking Strategy

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** A character-based sliding window with overlap is ideal for this corpus. The documents consist primarily of short forum posts and professor reviews. A 300-character chunk is long enough to carry the semantic meaning of a single review or tip, but short enough to return highly targeted search results without diluting the context. A 50-character overlap ensures that if a key fact (like a course code and a professor's name) spans a chunk boundary, it remains intact for retrieval.

**Final chunk count:** 34

---

## Sample Chunks

| # | Source document | Chunk text |
|---|----------------|------------|
| 1 | `reddit_cs3358` | I took Lee Koh for Data Structures and Assembly Language. He's outstanding. He is one of the most difficult professors in the department but he will REALLY improve your programming skills. This is where everything clicked. His courses are very well planned, and his tests have creative questions |
| 2 | `reddit_parking_commute` | The primary commuter lot is packed during the first week or two. I always had to park in the stadium lots during this time. The walk from the stadium lot to Roy F. Mitte (RFM) was more like 25-30 minutes. Unless you're going in very early or in the afternoon, I wouldn't even bother trying |
| 3 | `reddit_study_spots` | Recommendations for study spots near Derek hall or Roy F. Mitte building? The CLC on the third floor of Ingram has wonderful spaces to study which is right next to Mitte. In Derrick, there's Math Cats and also Cal Central, both are great places to study as well. RFM has desks with outlets |
| 4 | `rmp_koh_assembly` | Course: CS 2318 (Assembly Language) Professor: Lee Koh Rating: 4.5/5 He's definitely not as bad as his ratings say. He's very knowledgeable and his notes are incredibly detailed. He has recordings for every class too in case you miss one. His assembly class is a well refined deep dive into assembly language |
| 5 | `reddit_derrick_hall_demo` | RIP Derrick Hall. TXST plans on demolishing Derrick and supposedly by Fall 2025. Can't be soon enough. I've graduated but I spend a lot of hours there in classes / computer lab. However it was a very old building and needed an upgrade. They don't plan to completely tear down Derrick |

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` (via sentence-transformers)

**Production tradeoff reflection:**
If cost and resources weren't a constraint, I would weigh upgrading to an API-hosted model with a larger context window (like OpenAI's `text-embedding-3-small` or a Voyage AI model). While `all-MiniLM-L6-v2` is excellent because it runs locally with zero latency and no recurring API costs, it has a limited token window and can struggle with highly technical domain jargon or specific campus slang. An API-hosted model might yield better accuracy for complex student questions but introduces latency and external dependencies.

---

## Retrieval Test Results

**Query 1:** "Who should I take for Data Structures (CS 3358)?"

Top returned chunks:
- Source: `reddit_cs3358` | "I'll report back in August but I will be taking Xiaomin Li for 3358. Li was fantastic for cs3358 but I'd recommend taking it during a full semester... Li has the best slides I've seen at TXST and tests are open book."
- Source: `reddit_prof_recommendations` | "Professors I recommend : Object oriented - Metsis. Data structures and algorithms- lakomski or koh. Assembly - koh. Comp architecture - lakomski, hinkle, or qasem."
- Source: `reddit_cs3358` | "I took Lee Koh for Data Structures and Assembly Language. He's outstanding. He is one of the most difficult professors in the department but he will REALLY improve your programming skills."

Relevance explanation: The retrieval successfully pulled exact recommendations for CS 3358 (Data Structures), identifying Xiaomin Li, Lakomski, and Lee Koh across two different source files. The semantic search effectively mapped the intent of "Who should I take" to professor recommendations.

---

**Query 2:** "Is Dr. Mylene Farias a good choice for Computer Architecture (CS 3339)?"

Top returned chunks:
- Source: `reddit_cs3339` | "CS 3339 (Computer Architecture) with Dr. Mylene Farias isn't too bad. She's still fairly new and it shows in her lectures but she does try her best to take feedback from students. Her homework isn't too bad either, and even if people find it difficult, she'll be happy to get extensions."
- Source: `reddit_prof_recommendations` | "Professors I recommend : Object oriented - Metsis. Data structures and algorithms- lakomski or koh. Assembly - koh. Comp architecture - lakomski, hinkle, or qasem."
- Source: `reddit_cs3339` | "I would recommend Dr. Vasant Ramkumar for 3339 if you see him for it, i just got finished with his class and his lectures can be a little boring but he makes sure everyone knows exactly what he's testing you on"

Relevance explanation: The top chunk is a direct, highly relevant match that directly answers the question about Dr. Mylene Farias, including her grading and homework policies. The subsequent chunks offer alternative professors for the exact same course code, which provides excellent context.

---

**Query 3:** "Where are the best places to study near Derrick Hall?"

Top returned chunks:
- Source: `reddit_study_spots` | "Recommendations for study spots near Derek hall or Roy F. Mitte building? The CLC on the third floor of Ingram has wonderful spaces to study which is right next to Mitte. In Derrick, there's Math Cats and also Cal Central, both are great places to study as well."
- Source: `reddit_derrick_vs_ingram` | "Derrick Hall. Hello. I am a girl considering doing CS as a minor because of my interest in games. However, most of those courses are in Derrick Hall. I understand that the building and the people get a bad rap. Is it REALLY that bad?"
- Source: `reddit_derrick_hall_demo` | "RIP Derrick Hall. TXST plans on demolishing Derrick and supposedly by Fall 2025. Can't be soon enough. I've graduated but I spend a lot of hours there in classes / computer lab."

Relevance explanation: The highest-ranked chunk directly answers the question by naming Math Cats, Cal Central, and the CLC in Ingram. The other chunks, while highly related to Derrick Hall, are more about the building's reputation and demolition rather than study spots, which shows a slight limitation of distance-based semantic matching when specific nouns dominate the query.

---

## Grounded Generation

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Example Responses

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

> **User:** > **System:** ---

## Evaluation Report

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

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*