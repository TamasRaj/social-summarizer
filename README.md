---
title: Social Summarizer
emoji: 🐨
colorFrom: red
colorTo: purple
sdk: docker
pinned: false
license: apache-2.0
---

# Reddit Summarizer

This application fetches the latest posts from a specified subreddit and provides summaries using Hugging Face's transformers library.

## How to Use

1. Enter a subreddit name (with or without 'r/' prefix)
2. The app will fetch recent text posts from that subreddit
3. Each post will be summarized, and then a meta-summary will be generated

## Features

- Fetches latest text posts from any subreddit
- Uses transformer models to generate concise summaries
- Chat-like interface to track conversation history