# Project 1 Planning: The Unofficial Guide

## Domain
**Texas State University CS & Engineering Survival Guide.** This system covers the unofficial, student-generated knowledge required to navigate the Computer Science and Engineering programs at TXST. This knowledge is valuable because official course catalogs don't reflect teaching styles, real weekly time commitments for software and hardware projects, or practical advice on campus facilities (like lab access).

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | r/txstate thread | Data Structures Profs | `docs/reddit_cs3358.txt` |
| 2 | r/txstate thread | Prof Recommendations | `docs/reddit_prof_recommendations.txt` |
| 3 | r/txstate thread | Computer Architecture Profs | `docs/reddit_cs3339.txt` |
| 4 | r/txstate thread | Derrick Hall Demolition | `docs/reddit_derrick_hall_demo.txt` |
| 5 | r/txstate thread | Derrick Hall vs Ingram | `docs/reddit_derrick_vs_ingram.txt` |
| 6 | r/txstate thread | Parking and Commuting | `docs/reddit_parking_commute.txt` |
| 7 | r/txstate thread | Best Study Spots | `docs/reddit_study_spots.txt` |
| 8 | Rate My Professors | Lee Koh Review | `docs/rmp_koh_assembly.txt` |
| 9 | CS Discord Export | Elective Course Advice | `docs/discord_cs_survival.txt` |
| 10| Rate My Professors | Becky Reichenau Review | `docs/rmp_seaman_cs.txt` |

## Chunking Strategy

**Chunk size:** 300 characters
**Overlap:** 50 characters

**Reasoning:** A character-based sliding window with overlap is ideal for this corpus. The documents consist primarily of short forum posts and professor reviews. A 300-character chunk is long enough to carry the semantic meaning of a single review or tip, but short enough to return highly targeted search results. A 50-character overlap ensures that if a key fact (like a course code and a professor's name) spans a chunk boundary, it remains intact for retrieval.

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` (via sentence-transformers)
**Top-k:** 5

**Production tradeoff reflection:**
If cost and resources weren't a constraint, I would weigh upgrading to a model with a larger context window (like OpenAI's `text-embedding-3-small` or a Voyage AI model). While `all-MiniLM-L6-v2` is fast and runs locally without API limits, it struggles with dense, highly technical domain jargon and has a limited token window. An API-hosted model might yield better accuracy for complex student questions, though it introduces latency and recurring API costs.

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Who should I take for Data Structures (CS 3358)? | Xiaomin Li or Lee Koh. Li has great slides and open-book tests, while Koh is difficult but will greatly improve programming skills. Avoid Hwang. |
| 2 | Is Dr. Mylene Farias a good choice for Computer Architecture (CS 3339)? | Yes, she is fairly new but takes feedback well, gives homework extensions, and offers extra credit. |
| 3 | Where are the best places to study near Derrick Hall? | Math Cats or Cal Central in Derrick Hall. The CLC on the 3rd floor of Ingram is also highly recommended. |
| 4 | How long does it take to walk from the stadium parking lot to Roy F. Mitte (RFM)? | It takes about 25-30 minutes, and students recommend bringing body wipes and deodorant due to the heat. |
| 5 | Does Professor Lee Koh use a modern version of MIPS in Assembly Language? | No, he uses an older version of MIPS so you have to follow the older syntax. |

## Anticipated Challenges

1. **Inconsistent Terminology:** Students might refer to courses interchangeably by name or code (e.g., "Data Structures" vs. "CS 3358"), or buildings by acronyms ("RFM" vs "Roy F. Mitte"). Semantic search should help, but heavy slang might fail retrieval.
2. **Contradictory Information:** Two chunks from different Reddit users might offer opposite advice on the same professor. The LLM might struggle to synthesize this without hallucinating or taking a definitive, biased stance.

## Architecture

```mermaid
graph TD
    A[Raw Documents: Reddit/RMP] -->|ingest.py| B(Chunking)
    B -->|300 char / 50 overlap| C[Embedding]
    C -->|sentence-transformers| D[(ChromaDB Vector Store)]
    E[User Query] --> F[Retriever]
    D <-->|Cosine Similarity| F
    F -->|Top-k Chunks| G[Generator]
    G -->|Groq / llama-3.3-70b| H[Grounded Response]