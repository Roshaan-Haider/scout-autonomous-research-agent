# Scout — Autonomous Research Agent

A multi-step agent built with LangGraph that plans, retrieves, and 
synthesizes information across multiple tool calls, rather than 
answering in a single shot.

## What it does
Given a research goal, Scout autonomously decides which tools to use 
(web search, document retrieval via RAG), gathers information across 
multiple steps, and synthesizes a structured output — with bounded 
autonomy (limits on tool calls, timeouts, and failure handling) rather 
than running unchecked.

## Stack
- LangChain / LangGraph
- Local LLM (Llama 3.1 8B Instruct) via LM Studio
- Python 3.11

## Status
🚧 In development