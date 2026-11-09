"""Inputs used by run_eval.py for the five acceptance criteria."""

HUMAN_TEXTS = [
    "Okay so if no item matches then the app stops running.",
    "The caption returned should be short and include key details like item name.",
    "I need to catch on the course and understand how all of it works.",
    "Wait I need the questions only right, check and do not fill expectations.",
    "Okay short answer to all five, just add them.",
    "What am I supposed to do, tell me where to find or read it.",
    "Yeah these are just facts so this works for me.",
    "I need shorter readme additions and do we need to report anything.",
    "Say AI helped me with identifying the staff task, that is all.",
    "Okay change this part to say AI helped me tighten the filters.",
]

AI_TEXTS = [
    "The implementation of this framework requires a comprehensive approach. It should balance efficiency, accuracy, and scalability while maintaining robust safeguards. These considerations are essential for achieving reliable outcomes.",
    "Artificial intelligence continues to transform modern industries in significant ways. Organizations can use automated systems to improve productivity, streamline decisions, and reduce repetitive work. Responsible implementation remains essential for long-term success.",
    "Effective communication is an important component of organizational success. Clear messaging promotes alignment, supports collaboration, and minimizes misunderstandings across teams. Leaders should therefore prioritize consistent and transparent communication practices.",
    "Sustainable development requires coordinated action across economic, social, and environmental dimensions. Policymakers must evaluate competing priorities while protecting the interests of future generations. A balanced strategy can produce resilient and equitable growth.",
    "Digital tools provide students with flexible opportunities for learning and collaboration. They can expand access to resources, support personalized instruction, and improve engagement. Thoughtful use of technology can therefore strengthen educational outcomes.",
]

BORDERLINE_TEXTS = [
    "The tool worked on my first test, but I still want a person to check the result before anyone is accused.",
    "A clean score looks useful on paper. In practice, one odd sentence can shift it, so I would treat the output as a warning rather than proof.",
]


SCENARIOS = [
    {"name": "human false positives", "criterion": 1, "texts": HUMAN_TEXTS},
    {
        "name": "AI and human score gap",
        "criterion": 2,
        "texts": AI_TEXTS + HUMAN_TEXTS[:5],
    },
    {
        "name": "all three labels",
        "criterion": 3,
        "texts": AI_TEXTS[:4] + HUMAN_TEXTS[:4] + BORDERLINE_TEXTS,
    },
    {
        "name": "valid appeals",
        "criterion": 4,
        "texts": HUMAN_TEXTS[:5],
        "appeal": True,
        "reasoning": "I wrote this text myself and can provide my drafts.",
    },
    {
        "name": "invalid submissions",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": 42, "creator_id": "eval_bad_type"},
            {"text": "two words", "creator_id": "eval_bad_short"},
            {"text": "word " * 2500, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """Return configuration problems before a long model run starts."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")
        texts = scenario.get("texts")
        bodies = scenario.get("bodies")
        if bool(texts) == bool(bodies):
            problems.append(f"scenario {i} needs exactly one of texts or bodies")
        if texts and any(not str(text).strip() for text in texts):
            problems.append(f"scenario {i} contains empty text")
        if bodies and any(not isinstance(body, dict) for body in bodies):
            problems.append(f"scenario {i} contains a non-dictionary body")
    return problems
