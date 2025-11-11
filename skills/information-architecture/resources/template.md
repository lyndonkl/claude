# Information Architecture Templates

Quick-start templates for content audits, card sorting, sitemaps, tree testing, and taxonomy design.

---

## Template 1: Content Audit

**When to use**: Before redesigning navigation, need inventory of existing content

### Content Audit Spreadsheet Template

| URL/ID | Title | Content Type | Category | Metadata | Last Updated | Owner | Status | Action | Notes |
|--------|-------|--------------|----------|----------|--------------|-------|--------|--------|-------|
| /about | About Us | Page | Company | meta-desc, img | 2024-01-15 | Marketing | Keep | Update copy | Outdated team bios |
| /api/auth | Authentication API | Docs | Developer | tags: auth, jwt | 2024-06-01 | Eng | Keep | None | Current |
| /blog/old-post | Old Post | Article | Blog | tags: news | 2020-03-10 | Marketing | **Remove** | Archive | 4 years old, irrelevant |
| /products/widget-a | Widget A | Product | Products | price, sku | 2024-05-20 | Sales | Keep | Recategorize | Should be in "Tools" not "Products" |
| /help/faq-duplicate | FAQ | Help | Support | tags: help | 2023-12-01 | Support | **Merge** | With /help/faq | Duplicate content |

### Audit Analysis Template

**Total Content Items**: [Count]

**By Type**:
- Pages: [Count] ([%])
- Docs: [Count] ([%])
- Articles: [Count] ([%])
- Products: [Count] ([%])
- Other: [Count] ([%])

**By Status**:
- Keep as-is: [Count] ([%])
- Update needed: [Count] ([%])
- Recategorize: [Count] ([%])
- Merge: [Count] ([%])
- Remove/Archive: [Count] ([%])

**Quality Issues**:
- Outdated (>2 years): [Count] items
- Missing metadata: [Count] items
- Duplicates: [Count] items
- Broken links: [Count] items
- Inconsistent labeling: [Count] items

**Current Performance** (from analytics):
- Most visited pages: [List top 5]
- Least visited pages: [List bottom 5]
- High bounce rate pages (>60%): [List]
- Search queries with no results: [List top 10]
- Common navigation paths: [List top 3]

**Key Findings**:
1. [Finding 1: e.g., "40% of content is outdated"]
2. [Finding 2: e.g., "Users search for 'pricing' but it's buried 4 levels deep"]
3. [Finding 3: e.g., "15% of content is duplicated across sections"]

**Recommendations**:
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

---

## Template 2: Card Sorting Study

**When to use**: Understanding user mental models for content organization

### Card Sorting Plan Template

**Study Type**: [Open / Closed / Hybrid]

**Research Question**: "How do [target users] naturally group and label [content type]?"

**Participants**:
- Target: [Number, e.g., "20 users"]
- Recruitment criteria: [e.g., "Active customers who use product 2+ times/week"]
- Incentive: [e.g., "$25 gift card"]

**Cards** ([Number] total):
1. [Card 1 name/title]
2. [Card 2 name/title]
3. [Card 3 name/title]
...
[List all cards — aim for 30-60 cards, representative sample of content]

**Pre-Defined Categories** (for Closed/Hybrid only):
1. [Category 1]
2. [Category 2]
3. [Category 3]
...

**Tool**: [e.g., "OptimalSort", "UserZoom", "Miro"]

**Instructions for Participants**:

```
You'll see [X] cards representing different [content/features/topics] on our [website/app].

Your task:
1. Read each card
2. Group cards that belong together
3. Name each group you create
4. You can create as many groups as you need (typically 5-10 groups work well)

There are no right or wrong answers. We want to understand how YOU think about organizing this content.

Time estimate: 15-20 minutes
```

### Card Sort Analysis Template

**Participation**:
- Completed: [X] / [Y] participants ([Z]% completion rate)
- Average time: [X minutes]

**Category Analysis**:

| Category Label | # Users Who Created It | % Agreement | Cards Most Often Included | Alternative Labels Used |
|----------------|------------------------|-------------|---------------------------|------------------------|
| Getting Started | 18 / 20 | 90% | "Sign Up", "First Login", "Quick Start" | "Onboarding", "Setup" |
| Reports | 16 / 20 | 80% | "Analytics", "Dashboard", "Metrics" | "Insights", "Data" |
| Settings | 19 / 20 | 95% | "Profile", "Preferences", "Account" | "Configuration", "Options" |

**Dendogram Insights** (hierarchical clustering):
- **Strong clusters** (>70% agreement): [List categories with high consensus]
- **Weak clusters** (<50% agreement): [List categories with low consensus — these need clarification]
- **Outlier cards**: [Cards that don't fit anywhere — may need reconsideration]

**Labeling Insights**:
- **Most common labels**: [e.g., "Help" (15 users), "Support" (12 users), "Assistance" (3 users)]
- **Terminology conflicts**: [e.g., "Users say 'Reports' but we call them 'Analytics'"]
- **Jargon to avoid**: [e.g., "Synergistic Solutions" — 0 users used this term]

**Key Findings**:
1. [Finding 1: e.g., "Users group by task, not by product feature"]
2. [Finding 2: e.g., "'Settings' is universally understood (95% agreement)"]
3. [Finding 3: e.g., "'Modules' label confuses users — split between 'Features' and 'Tools'"]

**Recommended Categories** (based on card sort):
1. [Category 1] — [Brief description]
2. [Category 2] — [Brief description]
3. [Category 3] — [Brief description]
...

---

## Template 3: Sitemap & Navigation Structure

**When to use**: Documenting information hierarchy after card sort analysis

### Sitemap Template

```
Homepage
├── [Category 1]
│   ├── [Subcategory 1.1]
│   │   ├── [Page 1.1.1]
│   │   └── [Page 1.1.2]
│   ├── [Subcategory 1.2]
│   │   ├── [Page 1.2.1]
│   │   └── [Page 1.2.2]
│   └── [Subcategory 1.3]
│
├── [Category 2]
│   ├── [Subcategory 2.1]
│   ├── [Subcategory 2.2]
│   └── [Subcategory 2.3]
│
├── [Category 3]
│   ├── [Page 3.1]
│   ├── [Page 3.2]
│   └── [Page 3.3]
│
└── [Category 4]
    ├── [Subcategory 4.1]
    │   ├── [Page 4.1.1]
    │   └── [Page 4.1.2]
    └── [Subcategory 4.2]
```

### Example: E-commerce Sitemap

```
Homepage
├── Shop by Category (Electronics, Clothing, Home & Garden)
├── Shop by Occasion (Daily Essentials, Special Occasions, Gifts)
├── Deals & Promotions (Today's Deals, Clearance, Bundles)
└── Support (Help Center, Track Order, Returns, Contact Us)
```

### Navigation Specification Template

**Primary Navigation** (Top-level categories):
- [Category 1]: [Description, user goal, target audience]
- [Category 2]: [Description, user goal, target audience]
- [Category 3]: [Description, user goal, target audience]

**Secondary Navigation** (Utility links):
- [Link 1]: [e.g., "Search", "Cart", "Account"]
- [Link 2]: [e.g., "Help", "Contact"]

**Faceted Filters** (for browse/search):
- **Facet 1**: [Name] — Options: [Option A, Option B, Option C]
- **Facet 2**: [Name] — Options: [Option A, Option B, Option C]
- **Facet 3**: [Name] — Options: [Option A, Option B, Option C]

**Breadcrumbs**: [Show path from homepage to current page]
- Example: `Home > [Category] > [Subcategory] > [Current Page]`

**Related Links**: [Contextual links on each page]
- "Related Articles"
- "You Might Also Like"
- "Next Steps"

**Search**:
- Placement: [e.g., "Global header, every page"]
- Features: [e.g., "Autocomplete, filters, recent searches"]
- Best bets: [Featured results for common queries]

---

## Template 4: Tree Testing Script

**When to use**: Validating navigation structure before building

### Tree Test Plan Template

**Research Question**: "Can users find [X] in our proposed navigation structure?"

**Participants**: [20-50 users matching target audience]

**Navigation Tree** (text-only structure):

```
Home
  Getting Started
    Sign Up
    First Login
    Quick Start Guide
  Features
    Reports
    Dashboards
    Alerts
  Settings
    Profile
    Preferences
    Billing
  Support
    Help Center
    Contact Us
    FAQ
```

**Tasks** (8-12 tasks typical):

1. **Task 1**: "You want to [user goal]. Where would you find [content]?"
   - **Correct destination**: [Path, e.g., "Features > Reports"]
   - **Why this task**: [e.g., "Most common user action"]

2. **Task 2**: "You need to [user goal]. Where would you look?"
   - **Correct destination**: [Path]
   - **Why this task**: [Rationale]

3. **Task 3**: [Task description]
   - **Correct destination**: [Path]
   - **Why this task**: [Rationale]

[Continue for 8-12 tasks covering key content/features]

### Tree Test Results Template

**Overall Performance**:
- **Success rate**: [X]% (Target: ≥70%)
- **Directness**: [X]× optimal path (Target: ≤1.5×)
- **Average time**: [X] seconds

**Task-Level Results**:

| Task | Success Rate | Directness | Avg Time | Top Incorrect Paths | Notes |
|------|--------------|------------|----------|---------------------|-------|
| Task 1 | 85% | 1.2× | 12 sec | None | Good |
| Task 2 | 45% | 2.5× | 35 sec | "Settings > Profile" (30%), "Support > Help" (25%) | **PROBLEM**: Users confused by label |
| Task 3 | 75% | 1.4× | 18 sec | "Features > Dashboards" (20%) | Minor issue |

**Problem Areas**:

| Issue | Evidence | Impact | Recommendation |
|-------|----------|--------|----------------|
| "Reports" label unclear | Task 2 only 45% success, users looked in "Dashboards" and "Settings" | High | Rename to "Analytics" or merge with "Dashboards" |
| "Settings" too broad | Tasks 4 & 5 both low success (50%, 55%) | Medium | Split into "Account Settings" and "App Preferences" |
| Deep nesting in "Support" | Task 7: 65% success, 2.8× directness | Medium | Flatten: move "FAQ" to top level |

**Recommended Changes**:
1. [Change 1: e.g., "Rename 'Reports' to 'Analytics'"]
2. [Change 2: e.g., "Split 'Settings' into 'Account' and 'Preferences'"]
3. [Change 3: e.g., "Move 'FAQ' from Support > Help Center > FAQ to top-level Support > FAQ"]

**Next Steps**:
- [ ] Implement recommended changes
- [ ] Re-run tree test on updated structure
- [ ] Proceed to wireframes once success rate ≥70% on all tasks

---

## Template 5: Taxonomy & Metadata Schema

**When to use**: Designing classification systems, tags, and content attributes

### Taxonomy Design Template

**Content Type**: [e.g., "Product", "Article", "Documentation Page"]

**Primary Taxonomy** (Hierarchical categories):
```
[Top-Level Category 1]
├── [Sub-category 1.1]
├── [Sub-category 1.2]
└── [Sub-category 1.3]

[Top-Level Category 2]
├── [Sub-category 2.1]
└── [Sub-category 2.2]

[Top-Level Category 3]
```

**Facets** (Orthogonal dimensions for filtering):
- **Facet 1**: [Name] — Values: [Value A, Value B, Value C]
- **Facet 2**: [Name] — Values: [Value A, Value B, Value C]
- **Facet 3**: [Name] — Values: [Value A, Value B, Value C]

**Tags** (Flexible, user-defined or preset):
- Preset tags: [List of controlled vocabulary tags]
- User-generated tags: [Yes/No]
- Tag moderation: [Yes/No, process]

**Metadata Schema**:

| Field | Type | Required | Values/Format | Purpose |
|-------|------|----------|---------------|---------|
| Title | Text | Yes | Plain text, max 60 chars | Display in nav, SEO |
| Description | Text | No | Plain text, max 160 chars | SEO meta description |
| Category | Select | Yes | [List of categories] | Primary classification |
| Tags | Multi-select | No | [Controlled vocabulary] | Cross-category findability |
| Author | Text | Yes | Name or ID | Attribution, filtering |
| Last Updated | Date | Yes | YYYY-MM-DD | Freshness indicator |
| Audience | Select | Yes | [e.g., "Beginner", "Advanced"] | Personalization |
| Content Type | Select | Yes | [e.g., "Tutorial", "Reference", "FAQ"] | Filtering, display |
| Status | Select | Yes | [e.g., "Draft", "Published", "Archived"] | Governance |

### Example: Documentation Taxonomy

**Primary Taxonomy**:
```
Getting Started
├── Installation
├── Configuration
└── First App

Guides
├── How-To Guides
├── Tutorials
└── Best Practices

Reference
├── API Documentation
├── CLI Reference
└── Configuration Files

Troubleshooting
├── Common Issues
├── Error Messages
└── FAQ
```

**Facets**:
- **Product Version**: v1.0, v2.0, v3.0
- **Difficulty Level**: Beginner, Intermediate, Advanced
- **Time to Complete**: <10 min, 10-30 min, >30 min

**Metadata** (for each doc page):
- Title, Description, Category, Tags, Author, Last Updated, Audience, Content Type, Product Version, Difficulty, Est. Time

---

## Quick Reference: When to Use Each Template

| Template | Use Case | Deliverable |
|----------|----------|-------------|
| **Content Audit** | Before redesign, need inventory | Spreadsheet with all content, status, recommendations |
| **Card Sorting** | Don't know how users categorize content | Category labels, groupings, terminology insights |
| **Sitemap** | After card sort, document structure | Visual hierarchy diagram |
| **Tree Testing** | Validate navigation before building | Success rates, problem areas, iteration recommendations |
| **Taxonomy & Metadata** | Design classification system | Taxonomy structure, metadata schema, controlled vocabulary |
