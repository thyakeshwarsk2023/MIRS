PHRASE_EXPLANATIONS = {
    "wake up": "Urgency framing — pressures immediate belief change without evidence",
    "act now": "Scarcity/urgency cue — classic persuasion tactic to bypass critical thinking",
    "before it's too late": "Fear-based deadline framing — amplifies perceived threat",
    "emergency": "Crisis language — elevates emotional arousal over factual context",
    "crisis": "Crisis framing — positions narrative as existential or urgent",
    "catastrophe": "Catastrophizing — exaggerates scale of harm or danger",
    "terrifying": "Fear amplification — intensifies emotional response",
    "panic": "Panic induction — encourages reactive rather than analytical reading",
    "threat": "Threat framing — positions actors or events as hostile or dangerous",
    "they don't want you to know": "Conspiracy framing — implies hidden suppression of truth",
    "hidden truth": "Secrecy narrative — suggests exclusive access to suppressed facts",
    "secret agenda": "Malintent attribution — assigns covert motives without substantiation",
    "cover-up": "Institutional distrust cue — implies deliberate concealment",
    "mainstream media lies": "Source delegitimization — undermines institutional journalism",
    "deep state": "Shadow-actor framing — attributes events to unaccountable forces",
    "globalist agenda": "Out-group conspiracy framing — vague hostile collective attribution",
    "media won't show you": "Exclusive-truth claim — positions source as bypassing censorship",
    "suppressed information": "Censorship narrative — implies knowledge is being withheld",
    "shocking": "Sensationalism — prioritizes surprise over verification",
    "unbelievable": "Disbelief hook — encourages sharing before scrutiny",
    "must watch": "Engagement bait — demands attention without substantive claim",
    "explosive": "Hyperbolic intensifier — inflates significance of claims",
    "massive scandal": "Scandal framing — implies wrongdoing at scale without proof",
    "bombshell": "Revelation rhetoric — suggests game-changing undisclosed facts",
    "outrageous": "Moral outrage cue — triggers anger-based engagement",
    "mind-blowing": "Awe/surprise manipulation — reduces analytical skepticism",
    "disturbing": "Disgust/fear cue — primes negative emotional reaction",
    "everyone knows": "False consensus — implies widespread agreement without evidence",
    "undeniable proof": "Certainty overclaim — asserts proof where verification may be lacking",
    "this proves": "Causal overreach — links weak evidence to strong conclusions",
    "without a doubt": "Absolute certainty language — closes room for nuance",
    "guaranteed truth": "Unfalsifiable claim — discourages skepticism or correction",
    "enemy of the people": "Dehumanizing out-group label — polarizes audience against targets",
    "traitors": "Loyalty violation framing — assigns moral betrayal without due process",
    "corrupt elites": "Power-structure villain framing — consolidates blame on elites",
    "rigged system": "System delegitimization — undermines institutional trust broadly",
    "they are coming for you": "Personal threat framing — directs fear toward the reader",
}

propaganda_keywords = [

    "wake up",
    "act now",
    "before it's too late",
    "emergency",
    "crisis",
    "catastrophe",
    "terrifying",
    "panic",
    "threat",

    "they don't want you to know",
    "hidden truth",
    "secret agenda",
    "cover-up",
    "mainstream media lies",
    "deep state",
    "globalist agenda",
    "media won't show you",
    "suppressed information",

    "shocking",
    "unbelievable",
    "must watch",
    "explosive",
    "massive scandal",
    "bombshell",
    "outrageous",
    "mind-blowing",
    "disturbing",

    "everyone knows",
    "undeniable proof",
    "this proves",
    "without a doubt",
    "guaranteed truth",

    "enemy of the people",
    "traitors",
    "corrupt elites",
    "rigged system",
    "they are coming for you"
]


def detect_propaganda(text):

    text_lower = text.lower()

    found_phrases = []

    for phrase in propaganda_keywords:

        if phrase in text_lower:
            found_phrases.append(phrase)

    return found_phrases


def propaganda_score(matches):

    score = min(len(matches) * 15, 100)

    return score


def get_phrase_explanation(phrase: str) -> str:
    """Return analyst-style explanation for a detected rhetorical phrase."""
    return PHRASE_EXPLANATIONS.get(
        phrase.lower(),
        "Persuasive or emotionally charged rhetoric detected in narrative framing.",
    )