# Visionerds AI Engineering Internship

Weekly work from a 2-month AI/ML engineering internship at Visionerds, building up from LLM API basics to a full RAG-based agentic system with a production-style backend.

## What this covers, week by week

**Week 1 — Prompting, LLM APIs, and Git**
System vs. user prompts, few-shot prompting, forcing structured JSON output, calling LLMs via OpenRouter/Groq, and proper git workflow (branching, meaningful commits, resolving merge conflicts by hand, opening PRs, keeping API keys out of version control).

**Week 2 — Embeddings and Chunking**
Turning text into embeddings, chunking strategies for splitting documents into retrievable pieces, and the fundamentals of semantic search.

**Week 3 — RAG Memory Strategies**
Query rewriting for follow-up questions, buffer memory (raw conversation history) vs. summarization memory (compressed running summary), and fixing a chunking bug that let junk chunks into the vector store. Built with ChromaDB, Groq (primary) and OpenRouter (fallback) as LLM providers, and `sentence-transformers` for embeddings, using David C. Lay's *Linear Algebra* textbook as the RAG source.

**Week 4 — Agentic Tool-Use and MCP**
Function calling and tool-use loops, ReAct agents with step instrumentation and loop caps, MCP (Model Context Protocol) client/server integration using FastMCP, and a multi-agent router that classifies queries as document search, tool use, or conversational.

**Week 5 — FastAPI and SQL**
REST API theory, SQL with SQLite (a small shop database with users/products/orders), building CRUD endpoints with FastAPI, Pydantic validation, and wrapping the Week 4 router agent behind a `POST /chat` endpoint with per-session conversation memory.

**Week 6 — CI/CD and Capstone**
GitHub Actions for automated testing, and the final capstone project combining everything above into one deployable system.

## Capstone project

The final deliverable — an AI Document QA Reviewer that checks content drafts against product documentation and compliance policies — was built as a separate, standalone repository:

**[AI-Document-QA-Reviewer →](https://github.com/mahamazhar112/AI-Document-QA-Reviewer)**

It combines RAG retrieval (ChromaDB + sentence-transformers), a FastAPI backend, SQLite persistence, session-based memory, an intent router with query rewriting, and a full pytest + GitHub Actions CI pipeline — built and documented as a polished, demo-ready project.

## Repo structure

```
week1/   Prompting, LLM API calls, git workflow
week2/   Embeddings and chunking
week3/   RAG memory strategies (query rewriting, buffer/summarization memory)
week4/   Agentic tool-use, ReAct agents, MCP integration
week5/   FastAPI + SQL, REST endpoints
```
