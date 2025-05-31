# ollama-ttrpg-query
Example use of Ollama to query TTRPG notes stored in a vector database

The text file I used is formated in a particular way, so I defined a function to help me parse that. This is in `read_file.py`

The main process is to run `prepare_rag.py` which will take the file and create one document per session to store the notes. 
This is prepared with Chroma using an Ollama embedding model for future lookups.

The core of the application, once the RAG is prepared, is to run `query_rag.py`. This takes in an input and answers it. 
It fetches 3 session notes that are relevant to the input question, and includes the prior/next session notes from the first match. 
All of this information is passed to Ollama, which by default is running gemma3:12b and should have a 128k context window to store all this.

Testing has shown moderate accuracy. It clearly would need more information to be fully accurate, but it does get the gist of it.

## Examples
Some example prompts and answers:

### When did Soren get the most scrolls?
Response:

Based on the provided session notes, the period when Soren acquired the most scrolls was between **August 8th and August 15th, 2024**.

Here’s a breakdown:

*   **August 2nd, 2024:** Soren bought a scroll of Detect Thoughts (2nd level) for 200g.
*   **August 15th, 2024:** While examining the tower with Alor, several scrolls were discovered, including: Arcane Lock, Glyph of Warding, Conjure Elementals, and a Spell Scroll of Demiplane. This implies a significant influx of scrolls during this session.

Therefore, the window between August 8th and August 15th saw the most scrolls acquired by Soren.

### Who is Queen Tesselia and what is her role in the campaign?
Response:

Okay, let's delve into Queen Tesselia and her role in the campaign, based on the provided session notes.

**Who is Queen Tesselia?**

Queen Tesselia is the reigning monarch of Tesselia, the capital city of the kingdom of Andor. However, she is only five years old, which fundamentally shapes the entire political landscape of the region. Because of her youth, she's under the regency of her father, a man who is described as a "bastard" and "abusing his position."  This situation creates instability and makes her a pawn in a larger political game.

**What is her role in the campaign?**

Based on the information gathered, here’s a breakdown of her role:

*   **Political Pawn:** She's essentially a figurehead. Her father, the regent, is the one wielding actual power.  He’s actively trying to maintain control, and his dislike for the adventurer's guild suggests he sees them as a potential threat to his authority. This makes her the focal point for those who want to challenge his rule.
*   **Target for Manipulation:** Nevermore's plan to overthrow the regent involves positioning herself as a temporary ruler until Tesselia is old enough to abdicate. This suggests a potential future where Tesselia’s abdication, or at least the *idea* of it, becomes a key plot point.
*   **Symbol of Legitimacy:** Even though she's just a child, Tesselia represents the rightful rule of Andor. This makes her a valuable asset for anyone trying to claim legitimacy. Nevermore knows this and intends to leverage it.
*   **Future Focus:** The fact that the regent is likely to kill her before she can inherit the throne adds a ticking clock element to the campaign. The party might be compelled to protect her or intervene in the political power struggle.
*   **Hidden Information:** The notes highlight that there was a meeting between Queen Tesselia and Queen Elnasha. This strongly suggests a connection and potential intrigue beyond the local politics of Tesselia. This is especially interesting when considering the mention of a guild branch being established in Southern Andor.



**Gaps in Information:**

*   **Queen Tesselia’s personality:** We know nothing about her as an individual. Is she aware of the power struggles around her? Does she have any desires or opinions?
*   **Her relationship with her father:**  Is she aware of his abuse of power? Does she resent him?
*   **Her relationship with Nevermore:**  Are they in contact? Does she know Nevermore’s intentions?
*   **Elansha’s role:** We are aware of the meeting, but have no information about why she was there.

Overall, Queen Tesselia’s role seems destined to become increasingly significant as the campaign progresses, with her future potentially intertwined with the larger political intrigue surrounding Andor and possibly involving connections to Southern Andor and beyond.

### How and when did Tririn die?
Response:

Tririn died during the final confrontation with Athena in the high-tech facility (referenced in the 2025-01-16 session notes). Specifically, after a period of sustained attrition against Polythemis and his cultists (2024-12-05 session notes) and facing a significant influx of robot adds and Athena’s defenses (2025-01-09 session notes), Tririn succumbed after failing a Dexterity saving throw at disadvantage following a Time Stop spell cast during a desperate attempt to escape the collapsing facility.



There's no additional information provided to determine the precise cause of death beyond that.


### How did the party invent Christmas?
Response:

**The Invention of Cherish Eve (or "Nova's Big Show")**

The story of how the party “invented” Cherish Eve (essentially, their version of Christmas) is a bit chaotic and born from a series of unusual events and Nova's penchant for spectacle. Here's how it unfolded:

**The Seeds of an Idea:** The journey towards this festive occasion began with the discovery of a strange tower, seemingly ripped from time and space. Within it, the party uncovered clues to a wizard obsessed with time travel and a portal circle leading to a mysterious place – the Technocrafts island. This place, and the wizard’s experiments, sparked a connection to a desire for wonder and celebration. 

**Nova’s Vision:** Nova, always seeking opportunities for grand displays, saw potential for a spectacular holiday. Inspired by the wizard's tales and the party's growing fame, she proposed a festive event for the town, drawing a loose parallel to something akin to the winter holidays.

**The Santa Inspiration:** Nova, seemingly having some awareness of the concept of "Santa," decided to incorporate this figure into their celebration. Tririn, always eager to participate, was transformed into a helper elf. June was polymorphed into a reindeer, while Soren conjured a floating disk for transportation. 

**The Grand Performance:**  The day itself was a deliberate spectacle. Nova, with Shar’s assistance, led the "parade," tossing presents (likely scavenged from the tower or acquired elsewhere) while riding the floating disk. The show involved music, light, and a general sense of joyous chaos. This effectively created the visual foundation for the holiday.

**A Touch of Magic:** Soren’s conjurations and June's transformation further enhanced the event’s magical ambiance, reinforcing the feeling of a uniquely festive occasion.

**The Legacy:** The sheer success and uniqueness of the event, as described, cemented its place in the town's memory. The citizens of the town would speak of the event for years to come, further solidifying the party’s role as the "inventors" of Cherish Eve.



**What’s Missing:** 

*   **The Origin of “Cherish”**: The exact inspiration behind the name "Cherish Eve" remains unclear.
*   **Detailed Traditions**: Beyond the initial show, few details are given about recurring customs or rituals associated with this invented holiday.

