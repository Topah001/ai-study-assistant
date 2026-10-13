"""Offline, source-grounded study helpers; no AI model or network calls."""

from collections import Counter
from dataclasses import dataclass
import re

_SENTENCE = re.compile(r"(?<=[.!?])\s+|\n+")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
_STOP = set("a an and are as at be been by for from has have in is it its of on or that the their this to was were which with".split())


def _sentences(text: str) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("Notes must be text")
    return [part.strip() for part in _SENTENCE.split(text.strip()) if part.strip()]


def _terms(sentence: str) -> list[str]:
    return [word.lower() for word in _WORD.findall(sentence) if word.lower() not in _STOP]


def summarize(notes: str, max_sentences: int = 3) -> list[str]:
    """Return the most informative source sentences verbatim, in source order."""
    sentences = _sentences(notes)
    if not isinstance(max_sentences, int) or isinstance(max_sentences, bool) or max_sentences < 0:
        raise ValueError("max_sentences must be a non-negative integer")
    if not sentences or max_sentences == 0:
        return []
    frequencies = Counter(term for sentence in sentences for term in _terms(sentence))
    ranked = sorted(
        enumerate(sentences),
        key=lambda item: (
            -sum(frequencies[t] for t in _terms(item[1])) / max(1, len(_terms(item[1]))),
            item[0],
        ),
    )
    selected = {index for index, _ in ranked[:max_sentences]}
    return [sentence for index, sentence in enumerate(sentences) if index in selected]


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    answer: str
    evidence: str


def generate_quiz(notes: str, limit: int = 5) -> list[QuizQuestion]:
    """Create answerable cloze questions whose answer/evidence are source spans."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise ValueError("limit must be a non-negative integer")
    if limit == 0:
        return []
    result = []
    for sentence in _sentences(notes):
        words = _WORD.findall(sentence)
        candidates = [word for word in words if word.lower() not in _STOP and len(word) >= 4]
        if not candidates:
            continue
        answer = max(candidates, key=lambda word: (len(word), word.lower()))
        question = re.sub(re.escape(answer), "____", sentence, count=1, flags=re.IGNORECASE)
        if question != sentence:
            result.append(QuizQuestion(question, answer, sentence))
        if len(result) >= limit:
            break
    return result


@dataclass(frozen=True)
class Answer:
    text: str
    evidence: str | None


def answer_question(notes: str, question: str) -> Answer:
    """Select matching source evidence; never infer beyond a directly quoted sentence."""
    sentences = _sentences(notes)
    question_terms = set(_terms(question))
    if not question_terms:
        return Answer("I can't answer from the supplied notes.", None)
    candidates = [
        (len(question_terms & set(_terms(sentence))), index, sentence)
        for index, sentence in enumerate(sentences)
    ]
    score, _, evidence = max(candidates, default=(0, 0, ""))
    if score == 0:
        return Answer("I can't answer from the supplied notes.", None)
    return Answer(f'According to the notes: "{evidence}"', evidence)

