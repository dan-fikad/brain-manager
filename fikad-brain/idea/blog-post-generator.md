
Yes. I’d solve this as a **compression problem**, not a “give the model the whole corpus” problem.

  

The mistake to avoid is this:

  

> **Do not** represent a writer by hundreds of raw posts at generation time.

> **Do** represent a writer by a small set of reusable artifacts that capture voice, structure, and habits.

  

## **1. Separate three kinds of memory**

  

Treat these as different systems:

  

**Content memory**

What the writer has written about: opinions, examples, frameworks, facts, recurring themes.

  

**Style memory**

How the writer writes: sentence rhythm, paragraph cadence, transitions, rhetorical devices, tone, hook patterns, formatting habits, CTA style, etc.

  

**Article state**

What this new post is trying to do right now: audience, thesis, outline, section goals, already-covered points, open loops.

  

If you mix these together in one big RAG index, style retrieval gets polluted by topic similarity, and topic retrieval gets polluted by surface writing quirks.

  

## **2. Build an offline “author package” for each user**

  

For each writer, preprocess their corpus once and store a compact package.

  

I’d build these artifacts:

  

### **A. Author card**

  

A structured summary, usually 300–800 tokens, such as:

- preferred opening styles
    
- sentence-length range
    
- paragraph length tendency
    
- degree of certainty / hedging
    
- humor / sarcasm level
    
- analogy frequency
    
- question usage
    
- favorite rhetorical moves
    
- formatting habits
    
- phrases to avoid
    
- phrases they overuse
    
- typical ending style
    

  

This is the main thing you pass into prompts.

  

### **B. Style exemplar bank**

  

Not full posts. Just 10–30 short, high-signal snippets tagged by **rhetorical role**, such as:

- hook
    
- personal anecdote
    
- explanation
    
- contrarian argument
    
- list section
    
- conclusion / CTA
    

  

At generation time, retrieve 2–4 exemplars by role, not by topic.

  

### **C. Semantic content index**

  

Chunk the writer’s posts for **meaning retrieval** only. This is where the system finds examples, arguments, and prior ideas relevant to the requested topic.

  

### **D. Hierarchical summaries**

  

Keep summaries at multiple levels:

- corpus summary
    
- theme summary
    
- post summary
    
- chunk-level evidence
    

  

That lets you retrieve the smallest useful level instead of raw text every time.

  

### **E. Style vector**

  

Train or infer a compact embedding representing style only. This should be topic-invariant as much as possible.

---

The important idea is that **style is much lower entropy than the full corpus**.

You usually do not need 500 posts in context to reproduce a voice. You need a style card, a few exemplars, and a few relevant content snippets.

  

## **3. Learn “style” separately from “content”**

  

This is the hardest part technically.

  

A good way to do it is to train a **style encoder** with contrastive learning or authorship-style classification.

  

### **Training setup**

  

Use pairs/triplets like:

- **positive**: same author, different topics
    
- **hard negative**: different authors, same topic
    
- **extra hard negative**: same platform / same niche / same structure
    

  

That forces the model to learn authorial style instead of just subject matter.

  

### **Input representation**

  

To reduce topic leakage, build style inputs from partially delexicalized text:

- mask named entities
    
- mask obvious topic nouns
    
- keep function words
    
- keep punctuation
    
- keep sentence boundaries
    
- optionally add POS or dependency features
    

  

This helps the style model care about **how** text is written, not just **what** it says.

  

### **Practical output**

  

Use the style encoder for three things:

1. retrieve the best style exemplars
    
2. generate/update the author card
    
3. optionally condition a self-hosted generator through prefix tuning / lightweight adapters
    

  

## **4. Do not fine-tune one full model per user**

  

At 1M users, per-user full fine-tunes are usually the wrong operating model.

  

A better progression is:

  

### **MVP**

  

Shared base model + author card + exemplar bank + semantic retrieval

  

### **V2**

  

Shared base model + learned style vector + better style retrieval

  

### **V3**

  

Cluster users into style archetypes, then add a **small per-user residual**

- one shared adapter per style cluster
    
- one lightweight per-user profile on top
    

  

That scales much better than 1M separate model variants.

  

The only user-specific learning signal I would definitely keep is **their edits**.

Accepted edits, rejected edits, and rewritten passages are the highest-value style data you’ll ever get.

  

## **5. Generate 4–5k words in stages, not in one shot**

  

For long blog posts, use a deterministic workflow:

  

### **Stage 1: Planner**

  

Input:

- user brief
    
- target audience
    
- author card
    
- relevant theme summaries
    

  

Output:

- thesis
    
- outline
    
- section intents
    
- tone target
    
- research gaps
    

  

### **Stage 2: Research / retrieval**

  

For each section, retrieve:

- relevant content snippets from the writer’s corpus
    
- external facts if needed
    
- 1–2 style exemplars matching that section role
    

  

### **Stage 3: Section writer**

  

Generate section by section, usually 500–900 words at a time.

  

Each section prompt contains only:

- author card
    
- small article-state summary
    
- section brief
    
- a few evidence snippets
    
- a few style exemplars
    

  

### **Stage 4: Continuity editor**

  

After all sections are drafted, run a pass for:

- transitions
    
- repetition removal
    
- argument consistency
    
- open-loop closure
    
- heading cleanup
    

  

### **Stage 5: Style polisher**

  

Final pass focused only on voice consistency and wording.

---

This is much cheaper and more controllable than one giant 5,000-word generation call.

  

A typical section prompt can stay in the low-thousands of input tokens instead of tens or hundreds of thousands.

  

## **6. Keep a rolling “article state” instead of the whole draft**

  

For long-form coherence, maintain a compact state object like:

- thesis
    
- outline
    
- claims already made
    
- examples already used
    
- terms already defined
    
- unresolved questions
    
- tone drift notes
    
- banned repetitions
    

  

That state should be updated after each section.

  

So instead of feeding the whole draft back to the model every time, you feed:

- current section target
    
- compact article state
    
- small relevant excerpt from prior sections if needed
    

  

That alone saves a lot of tokens.

  

## **7. At your scale, retrieval should be author-local**

  

This is a big architectural win.

  

Because each request already knows **which writer** it is generating for, you do **not** need a global ANN search across 1M authors at query time.

  

Route directly to that writer’s shard/package and search only inside that corpus.

  

That means your online problem is not “search the internet-scale corpus,” but “search a few hundred or few thousand chunks for one known author.”

  

That is much cheaper and simpler.

  

I’d use:

- **cold storage** for raw posts
    
- **warm storage** for semantic chunks and summaries
    
- **hot storage** for author card, style exemplars, style vector, and recent themes
    

  

Also deduplicate aggressively, because the same writer may cross-post similar text across Substack, Medium, personal blog, and newsletter archives.

  

## **8. Build two evaluators, not one**

  

You need both:

  

### **A. Style evaluator**

  

Train an internal classifier/scorer that estimates:

- “does this sound like author X?”
    
- “is this drifting toward generic AI style?”
    

  

### **B. Copying evaluator**

  

You also need a near-duplicate / overlap checker so the system does not accidentally reproduce source passages too closely.

  

That is especially important when style imitation is strong.

  

A good production metric set is:

- style similarity
    
- topic relevance
    
- factual support / citation coverage
    
- repetition score
    
- verbatim overlap score
    
- human preference score
    

  

## **9. If you implement this on OpenAI today**

  

For a current OpenAI-based build, I would use the **Responses API**, not Assistants. OpenAI recommends Responses for new projects, and the Assistants API is deprecated with a shutdown date of **August 26, 2026**. Responses also supports persistent chaining via previous_response_id / Conversations and has a compaction endpoint for shrinking long-running context. 

  

Current long-context models are large enough that they can be used as a safety net, but they should not be your default architecture. For example, GPT-5.4 currently has a **1,050,000-token context window** and **128,000 max output tokens**, but OpenAI notes that prompts above **272K input tokens** on GPT-5.4 / GPT-5.4 pro are priced at higher rates for the whole session. That means brute-force “stuff the whole corpus in context” is still economically wrong at scale. 

  

Prompt caching helps, but only for repeated prefixes. OpenAI’s docs say cache hits require an **exact repeated prefix** and kick in for prompts with **1024+ tokens**; they can reduce time-to-first-token by up to **80%** and input costs by up to **90%** for repeated content, and extended retention can keep cached prefixes active for up to **24 hours**. That is great for your fixed system prompt, tool schemas, and reusable templates. It does **not** solve the core cost of passing each writer’s unique corpus on every request. 

  

For embeddings, OpenAI’s current embedding models support dimensionality reduction: text-embedding-3-large creates embeddings up to **3072 dimensions**, and OpenAI notes it can be shortened via the dimensions parameter; their example says a **256-dimension** shortened embedding still outperformed unshortened text-embedding-ada-002 on MTEB. That makes compressed per-author retrieval much more realistic at your scale. 

  

If you use OpenAI-hosted file search, be aware of the current limits: for vector stores created starting in November 2025, file_search supports up to **100,000,000 files per vector store**, but you can attach at most **one vector store to an assistant and one to a thread**, and the default project file storage limit is **2.5 TB**. For 1M users with hundreds of posts each, that pushes most teams toward sharded external retrieval infrastructure or multiple store topologies rather than one giant hosted setup. 

  

A practical model split on the current OpenAI stack would be: use GPT-5.4 for planning and final editorial passes, use GPT-4.1 mini for high-volume drafting or fine-tuned writing tasks, and use GPT-4o mini for cheaper extraction / tagging / offline preprocessing. GPT-4.1 mini currently supports fine-tuning and has about a **1.047M-token context window**; GPT-4o mini is low-cost and also supports fine-tuning. 

  

## **10. What I would actually build first**

  

**Version 1**

- author card
    
- exemplar bank
    
- semantic retrieval
    
- section-by-section generator
    
- continuity editor
    
- copy checker
    

  

**Version 2**

- learned style encoder
    
- style-based exemplar retrieval
    
- time-weighted “recent voice” vs “all-time voice”
    

  

**Version 3**

- user-edit learning loop
    
- cluster adapters / prefix tuning
    
- stronger automated style evaluator
    

  

That sequence gets you something shippable early, while keeping a path to very strong personalization later.

  

The shortest summary is:

  

**Represent each author as a compact style package, not a pile of posts.**

**Retrieve content and style separately.**

**Generate long posts section-by-section with a rolling article state.**

  

That combination is the most scalable way to get both voice fidelity and token efficiency.

  

I can turn this into a concrete system design with data schema, pipeline stages, and model calls next.