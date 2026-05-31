import re

CONTENT_MODERATION_REGEX = re.compile(
    r"""
    \b(
        fuck|fucking|fucker|motherfucker|
        shit|bullshit|shitty|
        bitch|bitches|
        asshole|ass|bastard|
        dick|dickhead|cock|
        pussy|cunt|
        slut|whore|
        retard|idiot|moron|
        loser|stupid|dumbass|
        nigga|nigger|
        faggot|gaylord|
        kill\s+yourself|kys|
        suicide|self[- ]?harm|
        nazi|hitler|
        terrorist|terrorism|
        rape|rapist|
        pedophile|pedo|
        porn|pornography|
        sexcam|onlyfans|
        scam|fraud|
        hack|hacker|crack|
        malware|spyware|ransomware|
        phishing
    )\b
    |
    https?://\S+                           # URLs
    |
    www\.\S+                              # URLs without protocol
    |
    [A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,} # Emails
    |
    \b\d{10,}\b                           # Long numbers
    |
    (.)\1{5,}                             # Repeated characters
    """,
    re.IGNORECASE | re.VERBOSE
)

def moderate(text: str) -> bool:
    return not bool(CONTENT_MODERATION_REGEX.search(text))