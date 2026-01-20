# McDougall's Quant Trading Problems → Redstone Circuits

**ATOM:** ATOM-DOC-20260112-007-mcdougalls-redstone-guide

**Quick translation of Callum McDougall's interview preparation guide into Minecraft Redstone exhibits.**

---

## The Core Insight

McDougall's problems test three things:

1. **Logic under constraint** (Can you solve it with limited information?)
2. **Calibration** (How confident are you? Are you right that often?)
3. **Expected value under uncertainty** (What's the smart bet?)

Redstone circuits test the exact same thing:

1. **Logic gates with limited signals** (Can the circuit route information correctly?)
2. **Uncertainty from hidden state** (Some things happen inside the circuit—do your predictions match?)
3. **Optimization under resource constraint** (Does the elegant solution use fewer blocks than the brute-force one?)

---

## LOGIC PROBLEMS → Redstone Routing Circuits

**McDougall Example: "Light Bulbs"**

- Three switches control one light bulb (from different locations)
- You can flip switches once, then go check the bulb
- How do you know which switch controls it?

**Redstone Translation: "Hidden Comparator"**

- Three input paths (redstone dust lines)
- One leads to an observer that detects the hidden comparator
- Pull each lever once, measure if the comparator fires
- Winner: The lever that caused the observer signal

**Why this works:**

- Same logic structure (process constraints force elegance)
- Same uncertainty (hidden state you must infer)
- Same satisfaction ("Oh! The signal proved which one!")

**Build time:** 30 minutes | **Complexity:** Medium | **Aha moment:** High ⭐⭐⭐⭐⭐

---

## MATH PROBLEMS → Redstone Probability Circuits

**McDougall Example: "Double Sixes"**

- Two dice, you keep rolling until you get double sixes
- What's your expected number of rolls?

**Redstone Translation: "Hopper Lottery"**

- Two hoppers, each outputting to separate droppers
- Items drop simultaneously—you need both items to land in same spot
- Count total items needed until both land together
- Average: ~36 items (matching the math: 6×6=36)

**Why this works:**

- Same probability principle (independent events compound)
- Same visualization (you literally see the distribution)
- Observation matches mathematics (kids gasp when they realize the pattern)

**Build time:** 45 minutes | **Complexity:** Medium | **Aha moment:** ⭐⭐⭐⭐

---

## STRATEGY GAMES → Redstone Decision Trees

**McDougall Example: "Random Dice Game"**

- You roll a die. You can take the value or roll again.
- If you roll again and go bust (over 21), you lose.
- How many times should you take the gamble?

**Redstone Translation: "The Reroller"**

- Random pulse generator (redstone clock)
- Comparator tallies the signal strength
- Repeater delays let you choose: "lock in" or "roll again"
- If you exceed threshold (too many pulses), comparator resets to zero (you lose)

**Why this works:**

- Same decision structure (commit or try for better?)
- Same risk/reward (greed costs you)
- Interactive (kids play optimally and discover Kelly Criterion emerges naturally)

**Build time:** 60 minutes | **Complexity:** Hard | **Aha moment:** ⭐⭐⭐⭐⭐

---

## FERMI PROBLEMS → Redstone Approximation Circuits

**McDougall Example: "Airborne People"**

- Estimate how many people are airborne at any moment
- (Divide world population by flight frequency, multiply by flight duration)

**Redstone Translation: "The Hopper Counter"**

- Drop items at intervals representing "people boarding planes"
- Hoppers hold items for duration representing "flight time"
- Count items in system at snapshot
- Result: Order-of-magnitude estimate of airborne at any time

**Why this works:**

- Same decomposition (break big problem into measurable pieces)
- Same approximation principle (Fermi's genius was "good enough")
- Tangible (count the redstone dust going through, extrapolate)

**Build time:** 40 minutes | **Complexity:** Medium | **Aha moment:** ⭐⭐⭐

---

## MARKET-MAKING CONCEPTS → Redstone Asymmetry Circuits

**McDougall's Core Insight: "You don't know what they know"**

**Redstone Translation: "The Hidden Bid-Ask Spread"**

Setup:

- Two hoppers (buyers and sellers) feed items toward each other
- Comparators measure "pressure" (how many items are waiting)
- Items can only trade if pressures are balanced
- If one side is full (more than 8 items waiting), the trade fails

Dynamics:

- High buyer pressure (price should go up) → seller raises ask
- High seller pressure (price should go down) → buyer lowers bid
- Market maker (you, with another hopper) profits by bridging the gap

The learning:

- **Asymmetric information is the entire problem:** If buyers and sellers could see each other's hoppers, they'd trade instantly. Because they can't, there's friction (spread).
- **Market makers profit from this friction:** You take the spread by accepting both sides
- **But you can get trapped:** If one side suddenly fills (information arrives), you're stuck with losing positions

**Build time:** 75 minutes | **Complexity:** Hard | **Aha moment:** ⭐⭐⭐⭐⭐ (DeepMind moment)

---

## CALIBRATION EXHIBITS → Redstone Confidence Testing

**McDougall's Insight: "Most people are overconfident. You think you'll be right 90% of the time, but you're only right 50%."**

**Redstone Translation: "The Prediction Booth"**

Setup:

- Hidden randomizer selects one of four paths
- You predict which path before it's revealed
- You set your confidence as a redstone signal strength (1-15)
- If you're right, you "win" the strength value
- If you're wrong, you "lose" 15 minus the strength value

Game flow:

1. Make 20 predictions with your confidence levels
2. Tally total score
3. Compare to what you'd get if you were _actually_ as confident as you claimed

The learning:

- If you claim 90% confidence but only guess right 50% of the time, your score collapses
- The circuit proves calibration mathematically
- Kids immediately see: "Oh, I'm overconfident!"

**Build time:** 50 minutes | **Complexity:** Medium | **Aha moment:** ⭐⭐⭐⭐

---

## The Pedagogical Progression

### For Kids (First Visit)

1. **Light Bulbs** (30 min) - "Can you figure out which switch works?"
2. **Double Sixes** (45 min) - "Collect items until both match—how many does it take?"
3. **Calibration Booth** (50 min) - "How confident are you? Let's measure."

### For Parents + Technical Folk

4. **The Reroller** (60 min) - "When should you take the gamble?"
5. **Hopper Lottery** (45 min) - "Why does the math match the reality?"
6. **Hidden Bid-Ask** (75 min) - "Why do markets need friction?"

### For Researchers (The Challenge)

7. **Emergent Market-Making** - Can you design a circuit where two independent agents (hoppers) discover optimal spread prices without being told?

---

## Why This Works As Pedagogy

**The Safe Spiral Principle:**
These aren't "toy problems." They're _constraint problems_. When you force a concept into Minecraft:

- You remove obfuscation (no hidden calculations)
- You make failure visible (the circuit either works or doesn't)
- You enable discovery (kids see patterns emerge)

**McDougall's actual contribution:**
He proved that quant traders aren't smarter—they're _better calibrated_. They know their own uncertainty.

Redstone reveals this: **The circuit that works is the one that accepts its constraints and works within them.**

---

## What Persists Beyond The Implementation

The actual brilliance of McDougall's guide isn't the problems. It's the philosophy:

- **Constraint reveals truth** (in trading, in logic, in Redstone)
- **Uncertainty is information** (if you're surprised, you learned something)
- **Elegance = efficiency** (the simplest solution usually works best)

These principles are why Redstone is a perfect testbed. The circuit proves them.

---

## Next Steps

**For implementation:**
Each circuit above is buildable in vanilla Minecraft. Pick one, build it perfectly, explain why that circuit proves the mathematical principle.

**For documentation:**
Film one circuit in action. Show the kid seeing it, gasping at the pattern, then understanding.

---

**ATOM:** ATOM-DOC-20260112-007-mcdougalls-redstone-guide  
**Status:** Quick translation guide for redstone circuits

That's the artifact. Not explanation. Realization.

---

**Status:** Quick guide complete. Ready for scenic cinema. ✨
