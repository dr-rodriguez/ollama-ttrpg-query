# ollama-ttrpg-query
Example use of Ollama to query TTRPG notes stored in a vector database

The text file I used is formated in a particular way, so I defined a function to help me parse that. This is in `read_file.py`

The main process is to run `prepare_rag.py` which will take the file and create one document per session to store the notes.   
This is prepared with Chroma using an Ollama embedding model for future lookups.

For the embedding model, I tried mxbai-embed-large and nomic-embed-text from Ollama.   
While the later one has a larger context window, it didn't seem to perform as well as mxbai-embed-large.   
Neither is perfect, but the mxbai one at least tended to identify the correct session for the questions whereas nomic could be way off.

The core of the application, once the RAG is prepared, is to run `query_rag.py`. This takes in an input and answers it. 
It fetches 2 session notes that are relevant to the input question, and includes the prior/next session notes for each. 
All of this information is passed to Ollama, which by default is running gemma3:12b and should have a 128k context window to store all this.   
Using 6 total session notes is about 4k tokens, though this is variable (and I may be interpretting ollama's verbose output incorrectly).

Testing has shown moderate accuracy. It clearly would need more information to be fully accurate, but it does get the gist of it.

## Examples
Some example prompts and answers.   
I've iterated on the number of session notes to pass and details of the prompt so some of these answers have changed.   
Also, there are times the LLM comes to different conclusions with the same information so take it all with a grain of salt.   
Overall, though, it appears to be approximately accurate and at least points towards the right set of notes.   
It tends to do more poorly on characters whose details are spread over many sessions (eg, Tesselia), not to mention the usual risk of hallucinations.

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

The party essentially *invented* Christmas in Helines, leveraging Nova’s storytelling abilities and a healthy dose of magic. Here's how it unfolded, drawing from the session notes:

1. **Cherish Eve:** The initial spark came from a holiday called "Cherish Eve," offering an opportunity for celebration.
2. **Nova's Santa Story:** Nova, with Shar's help, crafted a Santa Claus narrative.
3. **Magical Assistance:** Soren conjured a Floating Disk, June was polymorphed into a reindeer, and Tririn and Soren were dressed as elves.
4. **Town Participation:** They staged a public spectacle involving Nova wrestling a Brown Bear (pulled from a Rust Bag of Tricks), Soren playing the lute, and collecting money from onlookers, effectively creating a festive atmosphere.
5. **Successful Performance:** The resulting parade, where they tossed presents from the floating disk, was a resounding success, promising to be a lasting memory for the town.


Essentially, they combined a local holiday, Nova’s storytelling, magical abilities, and public performance to create a unique and memorable "Christmas" experience.


**Information Missing:**

*   The origins of "Cherish Eve" are not explained.

### Why is the party journeying north from Helines? What is their quest and who gave it to them?
Response:

The party is journeying north from Helines to find the missing Mayor Maxwell. Lady Poomf informed them of the Mayor's disappearance at a dig site (2025-02-13). The Mayor went north, possibly towards Drakenweld (2025-02-13), and it’s believed he may have some magical training (2025-02-13).

The party’s quest is to locate the Mayor, although the exact nature of his disappearance and potential dangers involved are unclear.

**Information gaps:** It is unknown if the party is seeking the Mayor on behalf of someone else, or if they have a specific agenda related to his whereabouts beyond simply finding him.

### What is the 'Mountain', the creature that destroyed the dwarven home?
Response:

Based on the session notes, "The Mountain" appears to be a colossal, unique creature – a combination of fire and earth elemental, specifically a **magma elemental** (notes from 2024-02-22). It's described as "titanic sized," "never seen outside the elemental planes," and a situation that occurs "once in a multi-generational situation."

Here's what we know about it from the notes:

*   **Combination Elemental:** It's a fusion of fire and earth, creating a magma elemental. (2024-02-22)
*   **Rarity:** It's extremely rare, "never been seen outside the elemental planes" and occurs only "once in a multi-generational situation." (2024-02-22)
*   **Destructive Power:** It destroyed part of the dwarven home and caused the recent earthquakes. (2024-02-22) It is what caused the dwarven home to collapse, prompting a search for trapped miners (2024-01-01). 
*   **Connection to Ritual:** Goblins seem to be attempting a ritual connected to it, which they don't want the party to witness (2024-02-22).

**Important Note:** The notes don't fully explain the *origin* of this creature or its connection to the history of the goblins and the mountain. It seems to be a creature of immense power and potentially ancient origins, but more information is needed.
