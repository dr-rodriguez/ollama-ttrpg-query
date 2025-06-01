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

## Running

Once you have the dependencies installed (`pip install -r requirements.txt`) and have ollama running with the various models pulled, 
you can run queries through the command line.

Run `python .\query.py --help` and you'll get the following output:   
```
usage: query.py [-h] [-n NUM_NOTES] [-d] prompt

Query the DnD notes for relevant information.

positional arguments:
  prompt                A required string prompt for the program.

options:
  -h, --help            show this help message and exit
  -n NUM_NOTES, --num-notes NUM_NOTES
                        An optional integer specifying the number of notes (default: 2).
  -d, --disable-extra   An optional flag to disable fetching extra notes from prior/future sessions (default: False).
```

For example: `python .\query.py -n 8 -d "Which boss fights did Soren participate in? Did he go down in any of them?"`
Returns:
```
Prompt: Which boss fights did Soren participate in? Did he go down in any of them?
Number of notes: 8
Disable feching extra notes: True
Session notes to consider: ['2024-12-12', '2025-01-09', '2025-01-16', '2024-06-06', '2024-05-15', '2024-04-04', '2024-10-31', '2024-03-28']
Database indices: [48, 49, 50, 27, 24, 18, 45, 17]
Vector distances: [0.6727909445762634, 0.7138648629188538, 0.7525293231010437, 0.7797321081161499, 0.8304133415222168, 0.8320909738540649, 0.8401113748550415, 0.8490421772003174]
Here's a breakdown of Soren's boss fight participation based on the provided notes:

**Boss Fights Soren Participated In:**

*   **Fight with Ashton & Gnash (2024-04-04):** Soren was present and played a key role in defeating Ashton, ultimately killing him with magic missiles.
*   **Fight with Magnolia (2024-03-28):** Soren was present during this fight.
*   **Fight with Athena (2025-01-09 & 2025-01-16):** Soren was a central target and participant in the multi-session fight against Athena and her robot forces.

**Did Soren Go Down?**

Yes, Soren went down in multiple fights:

*   **Fight with Magnolia (2024-03-28):** Notes indicate he was "at 2/2/2 in spell slots" suggesting he's taken significant damage.
*   **Fight with Athena (2025-01-09):** Soren went down twice.
*   **Fight with Athena (2025-01-16):** Soren went down multiple times, notably being targeted and focused down by Athena.

It's unclear if Soren went down during the fight with Ashton, but he did appear to be taking some damage in general.
```
This isn't entirely accurate, but it's a suprisingly good approximation. It's essentially the big fights prior to the end of Chapters 1 and 2, though I would have counted two or three more.

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


### What is Queen Tesselia's connection to Lady Nevermore?
Response:

Based on the session notes, Queen Tesselia and Lady Nevermore have a complex and developing connection, hinting at a deeper history and shared purpose. Here’s what we know:

*   **Acquaintance:** Nevermore is familiar with Tesselia's mother ("She knows the 'being' in the device that held Tesselia. Knows 'secret codes'"). This suggests Nevermore knew Tesselia's mother before Tesselia’s current age.
*   **Shared Secret:** Their joint exploration of the ancient facility beneath the castle, facilitated by Tesselia using a code (“TESSELIA”), implies a shared understanding and mission related to the site and its technology.
*   **Potential Protector/Advisor:** Nevermore has taken on the role of “Regent Advisor” to Tesselia, indicating a protective and guiding role.
*   **Unclear Depth:** While there’s a clear connection and shared knowledge, the *exact* nature of their relationship (whether it's mentorship, familial, or something else entirely) remains unclear. The "secret codes" Nevermore knows about Tesselia's mother are a major hint, but we don's know what that implies.

It's possible their relationship is significantly deeper than we currently understand, but the notes do not provide sufficient information to definitively state their connection.


### How and when did Tririn die?
Response:

Tririn died during the final confrontation with Athena in the high-tech facility (referenced in the 2025-01-16 session notes). Specifically, after a period of sustained attrition against Polythemis and his cultists (2024-12-05 session notes) and facing a significant influx of robot adds and Athena’s defenses (2025-01-09 session notes), Tririn succumbed after failing a Dexterity saving throw at disadvantage following a Time Stop spell cast during a desperate attempt to escape the collapsing facility.

There's no additional information provided to determine the precise cause of death beyond that.


### How did the party invent Christmas?
Response:

The party essentially *invented* Christmas for the town, leveraging Nova’s innate showmanship and their accumulated magical abilities. Here's how, based on the notes:

1. **Nova's Idea:** Nova, known for his spectacle, proposed a Christmas celebration, likely inspired by the concept of "Santa" (which he shared with the town, suggesting a prior knowledge of this tradition).
2. **The Spectacle:** They combined Nova's performance (wrestling a Brown Bear pulled from a Rust Bag of Tricks – a chaotic but entertaining start) with Soren’s lute playing and Shar and June’s collecting money, effectively turning the event into a festival.
3. **Magical Transformation:**  Soten dressed the party (and themselves!) as elves, and June was polymorphed into a reindeer. Soren conjured a Floating Disk for transportation, creating a whimsical, magical parade.
4. **The Presentation:** Nova, with Shar's help, told the story, completing the festive atmosphere.  The successful, memorable nature of the performance ensured the town would “speak about this for years.”

While the notes don't specify a pre-existing holiday tradition, the party clearly crafted a unique and impactful celebration, which the townspeople likely adopted as their own version of Christmas.

**Missing Information:** The notes don’t explain where Nova learned about “Santa”, nor what the original Christmas tradition looked like.


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

