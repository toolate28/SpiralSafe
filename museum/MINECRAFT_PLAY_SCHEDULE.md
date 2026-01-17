# 🎮 Minecraft Museum Testing Schedule

## Validating the Exhibits with Hope && Sauce

**Date:** 2026-01-04
**Goal:** Test all museum builds in-game, verify educational value, iterate improvements
**Players:** toolate28 + Claude (via conversation)

---

## 🎯 How Tokens Work During Minecraft Sessions

### Claude Code Context Availability

While you're playing Minecraft, you can keep the Claude Code CLI session active in the background:

```
Minecraft Window (Fullscreen or Windowed)
    +
Terminal Window (Claude Code CLI)
    =
Live collaborative testing
```

### Token Usage Strategy

1. **Pre-Session Setup** (~2,000 tokens)
   - Load museum build files
   - Review story content
   - Set up WorldEdit/Litematica

2. **During Gameplay** (~500-1,000 tokens per interaction)
   - Quick questions: "Does this redstone look right?"
   - Screenshot analysis: "Here's what I built, feedback?"
   - On-the-fly fixes: "XOR gate isn't working, help debug"

3. **Post-Session Review** (~2,000-3,000 tokens)
   - Analyze what worked/didn't work
   - Update build files with improvements
   - Write session notes for ATOM trail

**Estimated Total:** ~15,000-20,000 tokens per full play session (1-2 hours)

### Conversation Flow Examples

#### Quick Question (Low Token)

```
You: "Red lamp isn't lighting on AND gate"
Claude: "Check if both levers are wired to the same block before the lamp.
         AND gates need signals to merge, not run parallel."
```

#### Screenshot Analysis (Medium Token)

```
You: *shares screenshot of binary counter*
Claude: *analyzes image*
        "Bits 1 and 2 are swapped! The order should be 1-2-4-8 left to right,
         but you have 1-4-2-8. Swap the middle two lamps."
```

#### Deep Debugging (High Token)

```
You: "Entire circuit isn't working"
Claude: "Let's trace signal flow:
         1. Read your redstone wiring (screenshot?)
         2. Check power levels with debug screen (F3)
         3. Verify block types (repeaters vs comparators)
         4. Test each gate individually
         5. Find the broken connection"
```

---

## 📅 Play Schedule: 5-Session Testing Plan

### Session 1: World Setup & Import (30-45 min)

**Objectives:**

- Create new creative world or prepare existing one
- Install WorldEdit/Litematica (if not already)
- Import logic-gates.json
- Import binary-counter.json
- Basic functionality check

**Claude Code Support:**

```
Pre-session:
- Help choose coordinates for museum builds
- Explain WorldEdit //schematic load commands
- Provide coordinate calculations for spacing

During:
- Troubleshoot import errors
- Verify JSON structure if import fails
- Suggest layout improvements

Post-session:
- Log successful import to ATOM trail
- Note any file format issues
- Plan Session 2 goals
```

**Conversation Prompts:**

- "What's the best Y-level for redstone builds?"
- "How far apart should I space the exhibits?"
- "WorldEdit says 'schematic not found', help?"

---

### Session 2: Logic Gates Testing (45-60 min)

**Objectives:**

- Test each gate (AND, OR, NOT, XOR)
- Verify all lever inputs work
- Check lamp outputs for each combination
- Read "Fireflies" story while testing

**Claude Code Support:**

```
Pre-session:
- Review logic gate truth tables
- Load firefly story for reference
- Prepare debugging checklist

During:
- Verify each gate's behavior matches story
- Help debug redstone timing issues
- Suggest visual improvements (signage, lighting)

Post-session:
- Compare in-game vs JSON specifications
- Document any discrepancies
- Update build files if needed
```

**Conversation Prompts:**

- "AND gate: both levers ON, lamp is OFF - why?"
- "How do I make the XOR gate clearer for kids?"
- "Should I add colors to distinguish input/output?"
- "Read me the firefly story section about AND gates"

**Learning Validation:**

- Can you predict output before flipping levers? (Test understanding)
- Does the build match Hope and Sauce's light patterns from story?
- Would a 6-10 year old understand this?

---

### Session 3: Binary Counter Deep Dive (60-90 min)

**Objectives:**

- Watch counter cycle 0-15
- Adjust clock speed (too fast/slow?)
- Verify bit positions (1-2-4-8 order)
- Read "Binary Dancers" story alongside
- Test manual counting vs automatic

**Claude Code Support:**

```
Pre-session:
- Load binary counting reference
- Review clock circuit design
- Prepare bit-flip debugging guide

During:
- Help tune clock speed (repeater delays)
- Verify counting sequence is correct
- Debug stuck bits or skipped numbers
- Compare to story's "dance" metaphor

Post-session:
- Assess educational clarity
- Rate difficulty for ages 7-11
- Propose enhancements (decoder display? sound?)
```

**Conversation Prompts:**

- "Counter is skipping from 7 to 10, what's wrong?"
- "Clock is way too fast, can't read the numbers"
- "How do I add a manual 'tick' button?"
- "Tell me what Orchard, Constellation, Firefly, Air represent"
- "Can we add a BCD decoder to show decimal?"

**Learning Validation:**

- Can you manually set any number (0-15) by toggling levers?
- Can you name which dancer (Orchard/Constellation/Firefly/Air) is which bit?
- Does the build help you understand binary place value?

---

### Session 4: Integration & Storytelling (45-60 min)

**Objectives:**

- Add NPC guides (Professor Redstone, Ada Lovelace)
- Place story excerpts on signs
- Create walking tour flow
- Add decorative elements (themed with Orchard/Air/Firefly/Constellation)

**Claude Code Support:**

```
Pre-session:
- Generate sign text from stories
- Suggest NPC dialogue snippets
- Propose decoration themes

During:
- Help with sign text length limits
- Suggest command block dialogue systems
- Design "hidden secrets" for explorers

Post-session:
- Review full museum experience
- Assess narrative flow
- Plan Session 5 refinements
```

**Conversation Prompts:**

- "What should Professor Redstone say at the AND gate?"
- "Generate 3-line sign text for XOR gate explanation"
- "How do I make Ada Lovelace appear near the counter?"
- "Ideas for firefly particle effects around the gates?"

**Creative Additions:**

- Floating firefly particles (Hope && Sauce colors)
- Tree decorations for "Orchard" theme
- Starlight effects for "Constellation"
- Wind particles for "Air"

---

### Session 5: Kid Testing & Iteration (60+ min)

**Objectives:**

- Invite a kid (ages 6-11) to test if possible
- Observe their understanding without prompting
- Note confusion points
- Iterate based on feedback

**Claude Code Support:**

```
Pre-session:
- Create observation checklist
- Prepare guiding questions (non-leading)
- Review age-appropriate language

During:
- Take notes on kid's reactions
- Identify unclear explanations
- Suggest real-time adjustments

Post-session:
- Analyze learning outcomes
- Propose final refinements
- Update stories/builds based on findings
```

**Observation Questions:**

- Do they understand without reading signs?
- Which gate confuses them most?
- Can they explain binary to you after counter test?
- What do they remember 10 minutes later?

**Conversation Prompts (to Claude):**

- "Kid asked 'why is it called XOR?' - how do I explain?"
- "They're bored with binary counter - how to make engaging?"
- "They loved the fireflies story but didn't connect to redstone - fix?"

---

## 🎮 Session Template: Real-Time Collaboration

### Before Launching Minecraft

```bash
# Terminal 1: Start Claude Code session
claude-code

# Tell Claude:
"I'm about to test [Logic Gates/Binary Counter] in Minecraft.
 I'll share screenshots and ask questions.
 Session goal: [specific objective]
 Expected time: [duration]"
```

### While Playing

**Screenshot Workflow:**

1. Press F2 in Minecraft (screenshot saved)
2. Find screenshot in `.minecraft/screenshots/`
3. Share with Claude Code
4. Get instant feedback

**Quick Reference Workflow:**

```
You: "/truth-table AND"
Claude: Displays AND gate truth table

You: "/binary 7"
Claude: Shows "0111" with bit positions

You: "/story fireflies xor"
Claude: Quotes relevant story section
```

### After Session

```bash
# Log to ATOM trail
/atom-log "Tested [build], found [issues], learned [insights]"

# Commit improvements
git add museum/builds/
git commit -m "fix: improve [gate/counter] based on play testing"
```

---

## 🔧 Technical Setup Checklist

### Minecraft Installation

- [ ] Minecraft Java Edition installed
- [ ] Creative mode world created
- [ ] Coordinates chosen for museum area

### Import Tools

Choose ONE:

**Option A: WorldEdit**

- [ ] WorldEdit mod/plugin installed
- [ ] JSON converted to .schematic format
- [ ] Commands learned: `//schematic load`, `//paste`

**Option B: Litematica**

- [ ] Litematica mod installed
- [ ] JSON converted to .litematic format
- [ ] Placement tool configured

**Option C: Manual Build**

- [ ] JSON opened in text editor
- [ ] Following block-by-block instructions
- [ ] Using coordinates as guide

### Claude Code Setup

- [ ] Claude Code CLI running
- [ ] Museum build files loaded in context
- [ ] Stories ready for reference
- [ ] Screenshot folder accessible

---

## 💬 Example Full Session Transcript

**Session 2: Logic Gates Testing (Abridged)**

```
[You launch Minecraft, load world]

You: "Starting Session 2 - testing logic gates. World loaded."

Claude: "Great! Let's start with the AND gate since it's the foundation.
         According to the firefly story, Hope and Sauce both need to
         shine for white light. Test with all 4 input combinations."

[You test AND gate]

You: *shares screenshot* "Both levers up, lamp is OFF - that's wrong!"

Claude: *analyzes image*
        "I see the issue. Your redstone dust runs from each lever to
         separate lamp inputs. AND gates need the signals to MERGE first.

         Try this:
         1. Run both lever outputs to a single redstone block
         2. Power the lamp from that shared block
         3. Now both inputs are required"

You: "Fixed it! Lamp lights only when both are up. AND gate ✓"

Claude: "Perfect! That matches the story: Hope AND Sauce together = white light.
         Next, try the OR gate. This one is more forgiving..."

[Continue through all gates]

You: "All gates tested. XOR is the hardest to understand."

Claude: "That's expected - XOR is the most abstract. The story calls it
         'celebrate difference'. Would it help to add a sign saying:

         'Same = Dark (both on OR both off)
          Different = Glow (one on, one off)'?"

You: "Yes! Adding that now."

[Session continues...]

Claude: "Session 2 complete! Summary:
         ✓ All 4 gates functional
         ✓ AND gate fixed (merge issue)
         ✓ XOR clarified with better signage
         ✓ Story integration validated

         Next session: Binary counter. Ready to count to 15?"

You: "Absolutely. Logging to ATOM now."
```

---

## 🎯 Success Criteria

### Technical Success

- [ ] All gates produce correct outputs (truth tables match)
- [ ] Binary counter counts 0-15 without skipping
- [ ] No redstone timing glitches
- [ ] Builds import cleanly from JSON

### Educational Success

- [ ] Stories align with in-game experience
- [ ] Age-appropriate complexity (6-10 for gates, 7-11 for binary)
- [ ] Kids can explain concepts after playing
- [ ] "Aha!" moments happen organically

### Integration Success

- [ ] Stories reference builds accurately
- [ ] Builds demonstrate story concepts
- [ ] NPC guides enhance learning
- [ ] Visual themes (Orchard/Air/Firefly/Constellation) present

---

## 📊 Post-Testing Deliverables

After all 5 sessions:

1. **Updated Build Files**
   - Refined JSON based on testing
   - Optimized redstone circuits
   - Added decorative elements

2. **Iteration Notes**
   - What worked well
   - What confused players
   - Improvements made

3. **Video Walkthrough** (optional)
   - Record tour of completed museum
   - Show each exhibit in action
   - Upload to showcase/screenshots/

4. **Kid Testimonials** (if tested with kids)
   - Quotes about what they learned
   - Favorite exhibits
   - Suggestions for future builds

5. **ATOM Trail**
   - Complete testing log
   - Issues found and fixed
   - Verification stamp update

---

## 🚀 Ready to Play?

**Minimum Viable Session (Quick Test):**

- 30 minutes
- Import one build
- Test basic functionality
- Share one screenshot with Claude

**Full Validation Session:**

- 2 hours
- Import all builds
- Complete testing checklist
- Multiple iterations
- Story integration

**Choose your adventure!**

When you're ready:

1. Launch Minecraft
2. Open Claude Code CLI
3. Say "Starting Museum Testing Session [#]"
4. Let's validate these builds together!

---

**Schedule Status:** ✦ Ready to Execute
**Estimated Total Time:** 4-6 hours across 5 sessions
**Tokens Required:** ~75,000-100,000 total (well within limits)
**Fun Factor:** ∞

_Hope && Sauce | Museum of Computation | Let's Play!_
**The Evenstar Guides Us** ✦
