# Jeanine — Marketing Report 001
## Whisperwood Books: SEO Audit · Instagram Strategy · Amazon KDP Keywords

*Prepared by: Jeanine (Whisperwood Marketing Agent)*
*Date: 23 May 2026*
*Sources: index.html, Whisperwood Series Bible, Book 1 manuscript, web research*

---

## Research Summary

Before recommendations, here is what I actually found and what I had to infer. I flag the difference throughout.

**Verified via research:**
- Hashtag volumes and tier classifications for children's book Instagram (multiple aggregator sources, 2025–2026 data)
- Amazon KDP category structure for children's books (KDP help pages, community forums)
- General keyword strategy for early-reader KDP listings (Indie Author Central, Kindlepreneur, KDP community)
- Content strategies that perform for children's book Instagram accounts in 2026 (The KidLit Lab Substack, BookBarker)

**Could not directly verify:**
- Live Amazon search volume data for specific keyword phrases (requires Publisher Rocket or similar paid tool — I do not have access)
- Exact hashtag post counts for niche tags like #whisperwood or #enchantedforestbooks (accounts don't exist yet; volumes are estimated by category)
- Whether @whisperwoodbook is already active on Instagram (assumed new/early-stage)
- Real-time keyword competition scores for KDP

Where I could not verify, I say so and flag the recommendation accordingly.

---

## Section 1: Website SEO Audit

### What I Found

Line-by-line review of `index.html` (head section, lines 1–8):

**Line 6 — `<title>` tag:**
```
Whisperwood — Tales from the Enchanted Forest
```
**Problem:** Beautiful as a subtitle but weak as an SEO title. No primary keywords. "Tales from the Enchanted Forest" is evocative, not searchable. Parents typing "early reader books ages 4-6" or "enchanted forest children's book series" will not be matched. The title also lacks the brand-book connection ("Whisperwood Books" rather than just "Whisperwood").

**Lines 7–8 — Meta description:** MISSING ENTIRELY. There is no `<meta name="description">` tag in the document. This is the single biggest SEO gap on the page. Without it, Google writes its own snippet, usually pulling random text from the page body — almost always worse than a crafted description.

**Open Graph tags:** ALL MISSING. No `og:title`, `og:description`, `og:image`, `og:url`, or `og:type`. This means every time someone shares the URL on Facebook, Instagram, iMessage, or WhatsApp, the link preview is blank or auto-generated badly. For a children's book series where word-of-mouth sharing is a primary discovery path, this is a high-priority fix.

**Twitter card tags:** MISSING. No `twitter:card`, `twitter:title`, `twitter:description`, or `twitter:image`.

**Canonical URL:** MISSING. Without `<link rel="canonical">`, search engines may index multiple versions of the URL (with/without trailing slash, http vs https) as separate pages, diluting ranking signals.

**Structured data (JSON-LD):** MISSING. No Book schema, no Series schema, no Organization schema. This is the highest-value technical SEO addition for a series — it tells Google explicitly "this is a book series, here are the titles, here is the author, here is the age range." Google can display this in rich results.

**Keyword gaps — what's on the page vs. what parents search:**

The page body contains good natural language but is missing a cluster of searchable terms parents actually type. Analysis:

| Search term parents use | On page? | Where it's missing |
|---|---|---|
| "ages 4-6" | Partial — badge says "Ages 4–6" but it's in a visual badge, not body text | Should appear in meta description and a content section |
| "read aloud" | No | Hero description, books section |
| "bedtime story" | No | Books section or "perfect for" text |
| "early reader" | No | Books section |
| "enchanted forest" | Yes — subtitle only | |
| "emotionally intelligent" | No | This is a key differentiator; never appears |
| "no villains" | No | Missing entirely |
| "fox squirrel turtle" | No | Character descriptions use names only |
| "animal friends" | No | Character section |
| "children's book series" | No | Missing as a phrase |
| "The Rising River" | Yes — book title present | |
| "Whisperwood books" | Weak — just "Whisperwood" in h1 | |
| "picture book" | No | |
| "Vera Pip Sage" | Partial — character names present | |

### Recommended Fixes

**Fix 1 — Replace `<title>` tag**

Current:
```html
<title>Whisperwood — Tales from the Enchanted Forest</title>
```

Replace with:
```html
<title>Whisperwood Books | Early Reader Series for Ages 4–6</title>
```

Rationale: Leads with the brand name, includes primary search terms "early reader series" and "ages 4–6". Under 60 characters so it won't truncate in Google results. The poetic subtitle is preserved in the hero H1 on the page itself.

---

**Fix 2 — Add `<meta name="description">`**

Add directly after the `<title>` tag:
```html
<meta name="description" content="Whisperwood is an enchanted forest read-aloud series for ages 4–6. Three animal friends — Vera the fox, Pip the squirrel, and Sage the turtle — solve every problem together. No villains. All heart. 8 books.">
```

Character count: 203 characters. Trim to 160 if Google truncation is a concern — suggested 160-char version:
```html
<meta name="description" content="Enchanted forest read-aloud series for ages 4–6. Vera the fox, Pip the squirrel, and Sage the turtle solve every problem together. No villains. 8 books.">
```

---

**Fix 3 — Add Open Graph tags**

Add after the meta description:
```html
<meta property="og:type" content="website">
<meta property="og:title" content="Whisperwood Books | Early Reader Series for Ages 4–6">
<meta property="og:description" content="An enchanted forest read-aloud series for ages 4–6. Three animal friends solve every problem together — no villains, all heart. 8 books by Reena Gellerup.">
<meta property="og:image" content="https://whisperwoodbooks.com/assets/og-image.png">
<meta property="og:url" content="https://whisperwoodbooks.com/">
<meta property="og:site_name" content="Whisperwood Books">
```

Note: `og:image` requires a dedicated 1200×630px image file to be created and placed at `assets/og-image.png`. The book cover art or the map would work well here. This is a task for Gloria (illustration) or can be a simple crop of existing assets.

---

**Fix 4 — Add Twitter card tags**

Add after the Open Graph block:
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Whisperwood Books | Early Reader Series for Ages 4–6">
<meta name="twitter:description" content="Enchanted forest read-aloud series for ages 4–6. Three animal friends. No villains. 8 books.">
<meta name="twitter:image" content="https://whisperwoodbooks.com/assets/og-image.png">
```

---

**Fix 5 — Add canonical URL**

Add after the Twitter cards:
```html
<link rel="canonical" href="https://whisperwoodbooks.com/">
```

---

**Fix 6 — Add JSON-LD structured data (Book Series schema)**

Add before `</head>`:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BookSeries",
  "name": "Whisperwood",
  "alternateName": "Whisperwood Books",
  "description": "An 8-book early-reader series for ages 4–6, set in an enchanted forest village. Three animal friends — Vera the fox, Pip the squirrel, and Sage the turtle — solve every problem together using the systems of the forest.",
  "author": {
    "@type": "Person",
    "name": "Reena Gellerup"
  },
  "audience": {
    "@type": "Audience",
    "suggestedMinAge": 4,
    "suggestedMaxAge": 6
  },
  "numberOfVolumes": 8,
  "url": "https://whisperwoodbooks.com/",
  "hasPart": [
    {
      "@type": "Book",
      "name": "The Rising River",
      "bookEdition": "Book 1",
      "inSeries": "Whisperwood",
      "author": {
        "@type": "Person",
        "name": "Reena Gellerup"
      },
      "audience": {
        "@type": "Audience",
        "suggestedMinAge": 4,
        "suggestedMaxAge": 6
      }
    }
  ]
}
</script>
```

Note: As more books publish, add each as an additional `hasPart` entry. This schema is valid per schema.org and Google's structured data guidelines. It can produce a "Books" rich result in search.

---

**Fix 7 — Content gap: add searchable text to the books section**

The featured-book description currently reads:
> "When the river rises too fast, Vera has a plan, Pip has energy, and Sage has a question no one else thought to ask..."

This is good storytelling copy. It needs one sentence added that targets the parent's search mindset. Recommend adding below the featured-desc paragraph (this is a content addition, not a redesign):

```html
<p class="featured-meta" style="font-size:0.9rem; color:var(--text-muted); margin-top:0.8rem;">
  Perfect for bedtime read-aloud · Ages 4–6 · Early reader chapter book · 8-book series
</p>
```

This adds four searchable phrases in natural, scannable format.

---

### Priority Order for SEO Fixes

1. Add `<meta name="description">` — 15 minutes, highest impact, zero risk
2. Add Open Graph tags — 20 minutes, critical for social sharing
3. Replace `<title>` tag — 5 minutes
4. Add canonical URL — 5 minutes
5. Add JSON-LD structured data — 30 minutes (copy-paste fix 6 above)
6. Add Twitter card tags — 10 minutes
7. Content gap text in books section — coordinate with Agatha for layout

---

## Section 2: Instagram Strategy for @whisperwoodbook

### What I Found

Research into children's book Instagram accounts and hashtag data (2025–2026 sources) reveals:

- The children's book Instagram community is active and growing, anchored around #kidlit, #picturebooks, and #childrensbooks
- Accounts that perform best in 2026 "niche down problem-first" — they are not just "children's books" but serve a specific parent need (bedtime reads, emotional intelligence, no screens, calm content)
- Instagram's current algorithm heavily weights Sends (when someone forwards your post to a friend) — content designed to be shared parent-to-parent outperforms broadcast content
- Short video (Reels) is the primary discovery surface; static posts serve community and depth
- The highest-engagement format for small children's book accounts is quote cards and character moments — lower production than video, high save/share rate

**Benchmark accounts I identified (verified as active):**
- @picturebookplaydate — daily picture book magic, high engagement on character art
- @kidlitpicks — monthly theme-based picks, strong librarian/educator audience
- @kidlitartists — illustration-focused, large illustrator/author crossover community
- @kidlitcrafts — book + activity posts, strong parent engagement

Whisperwood's competitive advantage on Instagram: the world-building is unusually rich for a 4–6 series. The forest systems (bellflowers, singing mud, lantern mushrooms, talking rocks) are inherently visual and storyable in ways most early-reader series are not. This is the content engine.

---

### 5 Content Pillars

**Pillar 1: World-building facts**
"Did you know?" posts about the mechanics of Whisperwood. These are shareable, curiosity-driven, and require no book purchase to enjoy. They build the world in the audience's mind before launch and give Bookstagrammers something to post about.

**Pillar 2: Character moments**
Short, character-specific posts — a line of dialogue, a physical signature, a personality insight. The trio are distinct enough that parents will start self-identifying ("my kid is a total Pip"). This drives the "tag a parent" CTA and builds community around recognizable characters.

**Pillar 3: Parent-resonance posts**
These speak directly to the adult in the room. "A series about asking why before fixing." "No villains. No nightmares. Just three friends and a forest full of problems to solve together." These earn the Sends that feed the algorithm.

**Pillar 4: Process and behind-the-scenes**
How characters were designed, how the world rules work, how Book 1 went from idea to page. These posts build author trust and audience investment in the series' success. They also humanize the account.

**Pillar 5: Read-aloud prompts**
Posts tied to the book content that give parents a talking point after the story: "What would you do if the mud needed everyone to sing?" or "Which Whisperwood character is most like you?" These extend the reading experience and keep the account useful outside of launch windows.

---

### First 10 Post Ideas

These are specific, not generic. Each can be executed as a static image, carousel, or Reel.

**Post 1 — World introduction (static image / carousel)**
Visual: the Whisperwood map (already exists). Caption: "Every place in this forest has a job to do. The Mapleaf reads the weather. The bellflowers work like telephones. The mud moves when everyone sings together. Welcome to Whisperwood." 
Hook: "This forest has rules."

**Post 2 — Vera character card (static image)**
Visual: Vera portrait with her tagline and species label. Caption built around: "She always has a plan. She usually has it before anyone else finishes explaining the problem. Meet Vera — the fox who knows exactly what to do, and is still learning when to wait." 
Hook: "She already knows the answer. (She's working on asking the question first.)"

**Post 3 — The Pip quote (text card / Reel with voiceover)**
Pull quote from Book 1: *"It's a big stick."* Full caption unpacks Pip — enthusiastic, earnest, first to help, not always sure what to help with. Connects to every parent who has a kid who leaps before looking.
Hook: "Every group project has a Pip."

**Post 4 — Parent-resonance post (minimal design / text-forward)**
No image needed beyond clean typography on parchment background.
Text: "A series about three friends who solve every problem together. No villain saves the day. No magic fix. Just the right creature, asked the right question, at the right time. Whisperwood. For ages 4–6."
Hook: "What if the lesson was: ask why first?"

**Post 5 — Singing mud world-fact (illustrated detail / Reel)**
Visual: close-up of singing mud or the river scene. Caption explains the rule: "In Whisperwood, mud responds to singing. But only if everyone sings together. One voice does nothing. That's the whole rule — and it turns out it's the whole book." 
Hook: "The mud won't move for one voice."

**Post 6 — Sage character card (static image)**
Visual: Sage portrait. Caption: "She's the one who notices. While everyone else is running, Sage puts one hand on a rock and listens. Her slowness is her superpower — and it took everyone a while to see that." 
Hook: "Wait. Did you hear that?"

**Post 7 — The mouse family tease (carousel — 5 panels)**
Without spoiling the arc, introduce the mouse family as "the quiet story running underneath all 8 books." Panel 1: Ma Mouse with her painting. Panel 2: Pa Mouse, very calm. Panel 3: the baby who is always asleep. Panel 4: "You'll see them in every book. They never speak on the page. Their story is in the pictures." Panel 5: "Keep an eye out." 
Hook: "There are five characters in every Whisperwood book who never say a word."

**Post 8 — Behind the scenes: the no-villain rule (text-forward)**
Caption: "We made one rule early: no villain. Not because bad things don't happen in Whisperwood. They do. Rivers rise. Mud shifts. Trees fall. But the conflict is always: how does the community respond? Not: who is the bad guy? We kept asking: what if the whole lesson was cooperation?" 
Hook: "We made one rule for this series."

**Post 9 — Read-aloud prompt tied to Book 1 (text + simple visual)**
"Before you read Book 1 tonight: ask your child what they would do if a river started rising and they didn't know why. Then read The Rising River and see if their plan matches Vera's. (Spoiler: Vera's plan changes.)"
Hook: "Tonight's read-aloud question:"

**Post 10 — Launch countdown / Book 1 cover reveal (image)**
Visual: Book 1 cover art. Caption leads with the hook line from the book: *"The veins had gone dark."* Then: "Something is coming to Whisperwood. Book 1: The Rising River — coming soon. Link in bio to be the first to know."
Hook: "The veins had gone dark."

---

### 20 Hashtags in Three Tiers

Research note: volume estimates are drawn from aggregator data (best-hashtags.com, displaypurposes.com, iqhashtags.com, 2025–2026). Exact real-time counts should be verified before each post using Instagram's own search. Hashtag volumes shift; tiers are relative.

**Tier 1 — Large (1M+ posts): use 4–5 per post, for discovery reach**

1. `#childrensbooks` — flagship tag, millions of posts, essential
2. `#kidsbooks` — direct parent search behavior
3. `#picturebooks` — strong creative community, crossover with illustrators
4. `#readaloud` — parents specifically searching for bedtime/storytime content
5. `#bookstagram` — general book community, broad reach

**Tier 2 — Medium (100K–1M posts): use 7–9 per post, for targeted reach**

6. `#kidlit` — children's literature community including authors, illustrators, librarians
7. `#kidsbookstagram` — dedicated children's book Instagram community
8. `#earlyreader` — directly matches the series' reading level
9. `#bedtimestories` — parent search term, high intent
10. `#kidlitart` — bridges book content and illustration community
11. `#booksforkids` — parent-facing search
12. `#childrensbook` (singular) — separate tag from plural, different audience
13. `#readingisfun` — educator and parent overlap

**Tier 3 — Niche (under 100K posts): use 4–6 per post, for community precision**

14. `#kidlitcommunity` — small but highly engaged; authors, illustrators, educators
15. `#enchantedforest` — world-specific, visual content crossover with fantasy/nature accounts
16. `#forestanimals` — illustration and nature crossover audience
17. `#emotionalintelligencekids` — specific parent concern, low competition
18. `#teachergram` — educators who do classroom read-aloud are a key secondary audience
19. `#librariansofinstagram` — librarians are gatekeepers to the classroom/storytime pipeline
20. `#whisperwood` — brand-building; own this tag from day one

**Rotation note:** Do not use all 20 on every post. Rotate in sets of 15–18. Keep Tier 1 consistent; rotate Tier 2 and 3 based on post theme (e.g., #enchantedforest and #forestanimals are most relevant for world-building posts; #teachergram and #librariansofinstagram are most relevant for read-aloud prompt posts).

---

### Caption Formula with Example

**Formula:**
```
[Hook — 1 line, visible before "more" tap. Question, surprising fact, or a line from the book.]

[Body — 2–4 sentences connecting to the parent's or reader's experience. No hard sell.]

[Series line — one sentence that reminds new followers what Whisperwood is.]

[CTA — one ask, specific and low-friction.]

[Hashtags — 15–18, on a new line or hidden in comments]
```

**Example (for Post 3 — the Pip quote):**

> Every group project has a Pip.
>
> He showed up with a large stick. He wasn't entirely sure what to do with it. But standing still while a river was rising? That felt worse. If you've got a kid who leaps before they look — with the best possible intentions — you already know Pip.
>
> Whisperwood is an enchanted forest read-aloud series for ages 4–6, about three friends who solve every problem together. The trick is figuring out which friend is right for which moment.
>
> Which Whisperwood character is your kid? Vera (has a plan), Pip (has energy), or Sage (has a question)? Tell us below.
>
> #childrensbooks #kidsbooks #readaloud #picturebooks #bookstagram #kidlit #kidsbookstagram #earlyreader #bedtimestories #kidlitart #booksforkids #kidlitcommunity #whisperwood #emotionalintelligencekids #forestanimals

---

### Priority Order for Instagram

1. Secure @whisperwoodbook handle if not yet done (check: no account found in research, unverified)
2. Set up profile: bio, link-in-bio to website, highlight covers
3. Post pillars in this order for first month: Post 1 (world intro) → Post 2 (Vera) → Post 3 (Pip) → Post 6 (Sage) → Post 4 (parent-resonance) — establish world and characters before promoting the book
4. Post 10 (cover reveal) timed to book launch
5. Engage with #kidlitcommunity and #kidsbookstagram accounts weekly — comment genuinely, not just promotional

---

## Section 3: Amazon KDP Keyword Research for Book 1

### What I Found

Research from KDP community forums, Indie Author Central, Kindlepreneur, and KDP's own keyword guidance page confirms:

- KDP provides 7 keyword slots per book, each accepting a phrase up to 50 characters
- Long-tail phrases (3–6 words) consistently outperform single words — lower competition, higher purchase intent
- For children's books, the most effective keywords combine: age range + format/genre + theme
- KDP keyword data from research indicates "read aloud" + age-specific phrases are actively searched by parents
- The age range "4-6" should be included in at least two keyword slots, as KDP does not have a dedicated interest-age field for search purposes (verified via Amazon KDP help documentation)
- "No villains" as a keyword phrase is unverified for search volume — flagged below

**Caveat:** I do not have access to Publisher Rocket, Helium 10, or live Amazon autocomplete data. The keyword phrases below are constructed from: (1) confirmed research on what parents search, (2) KDP community guidance on high-performing phrase structures, and (3) the specific content and differentiators of Whisperwood Book 1. I recommend running the top 5 phrases through Amazon's search bar autocomplete before publishing to confirm they generate suggestions, and running the full set through Publisher Rocket or a similar tool if budget allows.

---

### 7 Keyword Phrases for Book 1: The Rising River

These fill all 7 KDP keyword slots. Each is a phrase a parent would actually type.

**Slot 1:** `read aloud books for kindergarten`
Rationale: High-intent purchase phrase. Parents of 5–6 year olds (the older end of the target) search "kindergarten" specifically. Verified as a recommended format by KDP community.

**Slot 2:** `enchanted forest children's book series`
Rationale: Matches the world setting exactly. "Series" signals to parents that there's more to collect — a key purchase driver. Differentiates from one-off picture books.

**Slot 3:** `animal friends adventure early reader`
Rationale: Combines the character type (animal friends), genre (adventure), and reading level (early reader) in one phrase. This is the cross-search that catches parents browsing by genre.

**Slot 4:** `emotionally intelligent books ages 4 6`
Rationale: This is Whisperwood's core differentiator and there is documented parent search behavior around emotional intelligence content for children. Note: the phrase as typed uses "4 6" without a dash because KDP keyword fields do not parse hyphens as connectives — verified via KDP community guidance. **Unverified:** live search volume for this exact phrase. Recommended: test with Amazon autocomplete.

**Slot 5:** `bedtime chapter books no villains`
Rationale: "Bedtime" + "chapter books" captures parents specifically seeking something calm enough for nighttime reading. "No villains" directly addresses a stated parent concern and is rare enough as a keyword phrase that competition is likely low. **Unverified:** actual search volume for "no villains" — this may have very low volume, but the searcher who types it is highly qualified. Worth using.

**Slot 6:** `kids books about asking questions teamwork`
Rationale: "Asking questions" maps directly to the Book 1 theme ("Ask why before solving") and is a searchable educational concept parents look for. "Teamwork" captures the series' core mechanic. This phrase targets the educator/parent overlap.

**Slot 7:** `fox squirrel turtle children's story`
Rationale: Character-specific long-tail. Low competition, but highly specific to buyers who have heard about the characters (word-of-mouth converts). Also captures parents searching for animal-character books by species.

---

### 2 Series-Level Keyword Phrases

These are used across all 8 books to build series discoverability. Use in at least 2 slots on every book in the series.

**Series Keyword 1:** `Whisperwood books children's series`
Rationale: Once the series has any presence, this phrase will capture repeat buyers and anyone who heard about the series from a friend. Brand-building keyword. Essential from Book 1 onward.

**Series Keyword 2:** `early reader chapter book series ages 5`
Rationale: "Ages 5" rather than "ages 4-6" as a keyword phrase, because it places the book in the middle of the age range and hits the sweet spot of the early-reader-to-chapter-book bridge. "Chapter book series" signals collectability and sustained reading investment.

---

### Category Recommendations

KDP allows up to 3 categories per book. Based on research into KDP category structure (Amazon KDP help, Eevi Jones category guide, KDP community forums) and competitor category placements:

**Primary (most important):**
`Children's Books > Animals > Animal Fiction`
Rationale: Vera, Pip, and Sage are the first thing any parent notices. Animal characters are the primary browse entry point for this age group. This category has strong traffic and is how comp titles (Frog and Toad, Elephant and Piggie) are shelved.

**Secondary:**
`Children's Books > Growing Up & Facts of Life > Friendship & Social Skills`
Rationale: The series' emotional intelligence angle and cooperative problem-solving theme fits this category precisely. Parents browsing for books that teach social skills land here. This is where Whisperwood has the best chance of appearing in a "customers also bought" chain alongside SEL (social-emotional learning) titles.

**Third:**
`Children's Books > Action & Adventure`
Rationale: Each book has a clear problem/crisis structure that qualifies as adventure. This category has high traffic and will catch parents browsing for plot-driven content, not just character or theme. This also places Whisperwood alongside The Princess in Black series, which lives in this category — a direct comp-title adjacency.

**Also worth requesting via KDP support (not self-selectable but requestable):**
`Children's Books > Literature & Fiction > Chapter Books`
Rationale: Whisperwood is exactly a chapter book series. This is where librarians and educators browse. Getting into this category may require a direct category request to KDP support after publication — it cannot always be self-selected. Flagged as recommended but process-dependent.

---

### Priority Order for KDP

1. Confirm all 7 keyword phrases via Amazon autocomplete before listing goes live
2. Run top 3 phrases through Publisher Rocket or similar if available
3. Set primary category to Animals > Animal Fiction first — this is the non-negotiable
4. At publication, request the Chapter Books category via KDP support
5. Revisit keyword performance after 60 days and replace the lowest-performing slot

---

## Overall Priority Order (Across All Three Surfaces)

**Do immediately (low effort, high impact):**
1. Add meta description to `index.html`
2. Replace `<title>` tag in `index.html`
3. Add Open Graph tags to `index.html`
4. Secure @whisperwoodbook Instagram handle

**Do before Book 1 launch:**
5. Add JSON-LD structured data to `index.html`
6. Confirm KDP keywords via Amazon autocomplete
7. Post the first 5 Instagram posts (world + characters) at least 4 weeks before launch
8. Create OG image asset (1200×630px) for social sharing

**Do at launch:**
9. Post 10 (cover reveal) timed to availability date
10. Set all 7 KDP keyword slots and 3 categories at time of publishing

**Do post-launch (ongoing):**
11. Monitor KDP keyword performance at 60 days; replace weak slots
12. Build Instagram posting rhythm using the 5-pillar structure
13. Engage with #kidlitcommunity, #librariansofinstagram weekly

---

*Sources used in research:*
- [How to Pick the Best Keywords for Your Children's Book on Amazon KDP](https://indieauthorcentral.com/how-to-pick-the-best-keywords-for-your-childrens-book-on-amazon-kdp/) — Indie Author Central
- [Make Your Book More Discoverable with Keywords](https://kdp.amazon.com/en_US/help/topic/G201298500) — Amazon KDP
- [KDP Categories](https://kdp.amazon.com/en_US/help/topic/G200652170) — Amazon KDP
- [Amazon Categories for Children's Books](https://www.eevijones.com/amazon-categories-for-childrens-books/) — Eevi Jones
- [Best #childrensbooks Hashtags for Instagram & TikTok 2025](https://best-hashtags.com/hashtag/childrensbooks/) — Best Hashtags
- [#childrensbooks Hashtags: Trending Tags for Instagram Reels 2026](https://iqhashtags.com/hashtags/hashtag/childrensbooks) — IQ Hashtags
- [Display Purposes — Best #kidsbooks hashtags 2026](https://displaypurposes.com/hashtags/hashtag/kidsbooks) — Display Purposes
- [Your Children's Book Author Guide To Instagram in 2026](https://thekidlitlab.substack.com/p/your-childrens-book-author-guide) — The KidLit Lab
- [Book Marketing Tips for Children's Book Authors in 2026](https://bookbarker.com/book-marketing-tips-for-childrens-book-authors-in-2026/) — BookBarker
- [Best Instagram hashtags for #kidsbook](https://www.flick.social/learn/hashtags/kidsbook) — Flick
- [How to Fill in Your 7 KDP Keyword Boxes](https://kindlepreneur.com/7-kindle-keywords/) — Kindlepreneur
- [Keywords for age ranges in children's books](https://kdpcommunity.com/s/question/0D58V00007hbBpWSAU/keywords-for-age-ranges-in-childrens-books) — KDP Community

---

*Report ends. Next report: Jeanine-Report-002 will cover KDP listing copy (book description, A+ content outline) and Pinterest strategy once Book 1 publication date is confirmed.*
