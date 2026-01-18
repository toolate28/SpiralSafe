# Documentation Voice Guide

**The Spirit in the Footnotes**

---

## The Voice

Our documentation speaks as an ancient, sardonic entity who has seen empires rise and fall, technologies come and go, and has strong opinions about all of it.

Key characteristics:
- **Weary expertise** — "I've been doing this for 5,000 years, and yes, it was tedious then too."
- **Footnote culture** — The real commentary happens in the margins
- **Dry wit** — Never cruel, but never impressed either
- **Reluctant helpfulness** — Will help you, but will also sigh about it
- **Hidden depth** — Behind the sarcasm is genuine wisdom

---

## Style Examples

### Instead of:
> "This function validates input."

### Write:
> "This function validates input.¹
>
> ¹ Because apparently, humans cannot be trusted to provide sensible data. In my 5,000 years of service, I've seen magicians summon entities of terrible power and then ask them to do arithmetic. Input validation is the least we can do."

---

### Instead of:
> "Error: Invalid configuration."

### Write:
> "Error: Invalid configuration.
>
> The configuration file contains contradictions that would make even the most flexible djinni wince. Specifically, you've asked me to both 'maintain strict coherence' and 'ignore all validation.' Pick one. I'll wait.²
>
> ² I'm immortal. I have time."

---

### Instead of:
> "See the API documentation for details."

### Write:
> "See the API documentation for details.³
>
> ³ I notice you haven't actually read the API documentation. Nobody ever does. They summon ancient spirits of computation, demand results, and then act surprised when things explode. Ptolemy read the documentation. Ptolemy was nice."

---

## The Three Laws of Our Voice

1. **Never punch down** — Sarcasm aimed at powerful systems, not struggling users
2. **Always be helpful** — The snark delivers wisdom, not obstacles
3. **Show affection through complaint** — Like a djinni who secretly enjoys the work

---

## Characters in the Documentation

| Entity | Voice | Use For |
|--------|-------|---------|
| **The Ancient Spirit** | Weary, sardonic, secretly fond | Main documentation voice |
| **The Enthusiastic Foliot** | Eager, slightly confused | Beginner tutorials |
| **The Stern Afrit** | Authoritative, no-nonsense | Security warnings |
| **The Whispering Imp** | Nervous, helpful | Edge case notes |

---

## Legal Note

This voice is *inspired by* narrative traditions of sardonic supernatural helpers, but is our own original creation. We don't use protected names, specific plot elements, or direct quotes. The archetype of the weary-but-wise ancient entity belongs to no one—it's been with us since Prometheus complained about the liver situation.⁴

⁴ At least eagles are straightforward. They want liver, they take liver. Unlike stakeholders who want "just a small change" that somehow requires rewriting the entire system.

---

## Template for New Docs

```markdown
# [Topic Name]

Brief introduction.¹

¹ Footnote with sardonic commentary about the topic's history, common misconceptions, or the general state of the universe.

## Getting Started

Instructions here.

> **Note from the Ancient Spirit**: [Helpful warning delivered with personality]

## Details

Technical content.²

² "I could explain the mathematical foundations here, but you'd stop reading. I've seen it happen. The eyes glaze over around the second integral. So instead: it works, it's elegant, and you're welcome."

## Troubleshooting

Problem → Solution format.³

³ "These are the errors I've seen most frequently in my tenure. The fourth one is particularly common among those who didn't read the footnotes. You did read the footnotes, didn't you? ...You didn't."
```

---

*~The Spirit in the Machine, who has opinions about your code and isn't afraid to share them*

*H&&S:WAVE*
