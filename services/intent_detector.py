"""
services/intent_detector.py

Detects what type of health topic the user is asking about.
100% Free - No AI API required.
"""

import re

INTENTS = {
    "mental_health": [
        "stress", "tension", "anxiety", "depression",
        "sad", "udaas", "dar", "panic",
        "gussa", "rona", "overthinking"
    ],

    "physical_health": [
        "fever", "bukhar", "cold", "cough",
        "pain", "headache", "pet dard",
        "vomit", "infection"
    ],

    "nutrition": [
        "diet", "food", "protein",
        "vitamin", "calcium", "iron",
        "fruit", "vegetable", "milk"
    ],

    "sleep": [
        "sleep", "neend",
        "insomnia", "late night"
    ],

    "exercise": [
        "gym", "exercise",
        "workout", "fitness",
        "running", "yoga"
    ],

    "water": [
        "water",
        "pani",
        "hydration"
    ],

    "puberty": [
        "puberty",
        "height",
        "voice",
        "beard",
        "body change"
    ],

    "period": [
        "period",
        "menstruation",
        "cramps"
    ],

    "medicine": [
        "medicine",
        "tablet",
        "capsule",
        "antibiotic"
    ],

    "emergency": [
        "bleeding",
        "blood",
        "accident",
        "emergency"
    ],

    "education": [
        "study",
        "exam",
        "career",
        "college",
        "school",
        "hackathon",
        "cpct"
    ]
}


def detect_intent(text: str) -> str:
    """
    Detect user's intent.

    Returns:
        mental_health
        physical_health
        nutrition
        sleep
        exercise
        water
        puberty
        period
        medicine
        emergency
        education
        general
    """

    if not text:
        return "general"

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    return "general"
