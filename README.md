# 46 — AI Study Assistant

An offline study helper for supplied notes. Despite the project name, it uses **no external generative AI, language model, network service, or model download**. Its extractive summary selects and returns sentences verbatim; quiz questions blank a term already present in a source sentence; Q&A quotes a matching source sentence or explicitly declines. Evidence fields make the source inspectable. It does not create paraphrased facts.

## Run

Requires Python 3.10+ and no third-party packages. Run `python -m unittest discover -s tests -v`. Use `summarize(notes)`, `generate_quiz(notes)`, and `answer_question(notes, question)` from `study_assistant.py`.
