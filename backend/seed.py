"""
Seed script: creates tables, inserts articles/resources, seeds users, and indexes into ChromaDB.

Credentials:
  Admin : admin@startupnav.com  / StartupNav#2026Admin
  User  : user@startupnav.com   / TestUser#2026

Run:
  cd backend
  python seed.py
"""
import os
import sys

# Load .env before importing app modules
from dotenv import load_dotenv
load_dotenv()

from app.database import Base, engine, SessionLocal
from app.models.user import User, UserRole
from app.models.article import Article
from app.models.resource import Resource
from app.services.auth_service import hash_password

ARTICLES = [
    {
        "title": "How to Register a Private Limited Company in India",
        "category": "Registration",
        "summary": "Step-by-step guide to incorporating a Pvt Ltd company with MCA, covering DSC, DIN, name approval, MOA/AOA, and Certificate of Incorporation.",
        "tags": ["pvt ltd", "MCA", "incorporation", "india"],
        "content": """Registering a Private Limited Company (Pvt Ltd) in India is governed by the Companies Act, 2013 and administered by the Ministry of Corporate Affairs (MCA). It is the most popular business structure for startups due to limited liability, ability to raise equity funding, and perpetual succession.

## Step 1: Obtain Digital Signature Certificate (DSC)
All directors must obtain a Class 3 DSC from a government-authorised certifying authority (e.g., eMudhra, Sify, NSDL). This typically takes 1–2 business days and costs ₹1,000–₹2,000 per DSC.

## Step 2: Apply for Director Identification Number (DIN)
DIN is a unique identifier for each director. For new companies, DIN can be applied through the SPICe+ form directly during incorporation. Existing directors use DIR-3.

## Step 3: Name Reservation via RUN (Reserve Unique Name)
Apply for a unique company name on the MCA portal using the RUN service. The name must end with "Private Limited" and should not be identical or similar to existing companies or trademarks. MCA typically responds within 1–2 working days.

## Step 4: Draft Memorandum and Articles of Association (MOA & AOA)
MOA defines the company's constitution and objectives. AOA defines the internal rules governing the company. Both documents must be carefully drafted as they are difficult to change later.

## Step 5: File SPICe+ (Simplified Proforma for Incorporating a Company Electronically)
SPICe+ is a single integrated form that handles: company incorporation, DIN allotment, PAN, TAN, GST (optional), EPFO registration, ESIC registration, and Professional Tax (Maharashtra). Upload notarised copies of MOA, AOA, directors' identity proofs, address proof of registered office, and utility bills.

## Step 6: Certificate of Incorporation (COI)
After approval, MCA issues the Certificate of Incorporation (COI) along with the Company Identification Number (CIN). This typically takes 3–7 working days from filing.

## Post-Incorporation Compliance
After incorporation, you must: open a current bank account, deposit minimum paid-up capital, issue share certificates within 60 days, hold the first Board meeting within 30 days, and appoint a statutory auditor within 30 days.

## Costs Overview
Government fees range from ₹0–₹2,000 depending on authorized capital. Professional fees for a CA/CS range from ₹5,000–₹15,000. Total cost is typically ₹7,000–₹20,000 for a basic incorporation.

## Key Advantages of Pvt Ltd
- Limited liability protection for shareholders
- Ability to raise equity funding from angel investors and VCs
- Separate legal entity with perpetual succession
- Better credibility with banks, clients, and partners
- Easier to add co-founders through equity allocation
""",
    },
    {
        "title": "Understanding Startup India Registration and Tax Benefits",
        "category": "Registration",
        "summary": "How to register under the Startup India initiative for DPIIT recognition, tax exemptions under Sections 80-IAC and 56(2)(viib), and self-certification for labour and environmental laws.",
        "tags": ["startup india", "DPIIT", "tax exemption", "80-IAC"],
        "content": """The Startup India initiative, launched by the Government of India in January 2016, provides a supportive ecosystem for startups including tax benefits, regulatory relaxations, and funding support.

## Eligibility for DPIIT Recognition
To be recognised as a Startup by the Department for Promotion of Industry and Internal Trade (DPIIT), your company must:
1. Be incorporated as a Pvt Ltd, LLP, or Partnership firm
2. Be less than 10 years old from the date of incorporation
3. Have annual turnover not exceeding ₹100 crore in any financial year
4. Be working towards innovation, development, or improvement of products/services
5. Not be formed by splitting up or reconstructing an existing business

## How to Apply for DPIIT Recognition
1. Visit the Startup India portal (startupindia.gov.in)
2. Create an account and fill the recognition form
3. Upload Certificate of Incorporation, PAN, and a brief description of the innovative nature of your business
4. Recognition is typically granted within 2 business days

## Tax Benefits Available

### Income Tax Exemption under Section 80-IAC
Eligible startups can claim 100% deduction on profits for any 3 consecutive years out of the first 10 years since incorporation. Eligibility requires DPIIT recognition and approval from the Inter-Ministerial Board (IMB).

### Angel Tax Exemption under Section 56(2)(viib)
DPIIT-recognised startups are exempt from angel tax — the provision that treats investment received above fair market value as income. This is critical for early-stage fundraising.

### Capital Gains Exemption under Section 54EE
Investors who sell assets and reinvest the proceeds in DPIIT-recognised startup funds are exempt from long-term capital gains tax, subject to a lock-in of 3 years.

## Labour Law Self-Certification
DPIIT-recognised startups can self-certify compliance with 6 labour laws for 3–5 years, including: Building and Other Construction Workers Act, Inter-State Migrant Workmen Act, Payment of Gratuity Act, Contract Labour Act, Employees' Provident Fund Act, and Employees' State Insurance Act.

## Faster Winding Up
Startups can wind up operations within 90 days under the Insolvency and Bankruptcy Code (IBC), compared to years for traditional companies.

## Public Procurement
Central government ministries and PSUs must allow DPIIT-recognised startups to participate in procurement without prior turnover experience requirements.
""",
    },
    {
        "title": "Pre-Seed and Seed Funding: What Founders Need to Know",
        "category": "Funding",
        "summary": "A practical guide to pre-seed and seed funding stages — typical check sizes, investor types, what they look for, and how to prepare your pitch.",
        "tags": ["seed funding", "pre-seed", "angel investors", "pitch deck"],
        "content": """Early-stage funding is the lifeblood of a startup before it achieves revenue or product-market fit. Understanding the distinctions between pre-seed and seed stages will help you target the right investors at the right time.

## Pre-Seed Stage

### What It Is
Pre-seed funding typically ranges from ₹25 lakhs to ₹2 crore (or $30K–$250K USD). At this stage, you have an idea, early prototype, or MVP. Revenue is zero or very minimal.

### Who Invests at Pre-Seed
- Founder's own savings (bootstrapping)
- Friends and family
- Angel investors (individual HNIs)
- Pre-seed focused micro-VCs
- Incubators and accelerators (e.g., Y Combinator, T-Hub, NSRCEL, 91springboard)

### What Investors Look for
At pre-seed, investors are primarily betting on the team. They want to see:
- A founder with deep domain expertise or a history of building things
- Evidence of the problem being real (customer conversations, surveys)
- Early prototype or proof of concept
- A large addressable market

### Typical Terms
Pre-seed is often structured as a SAFE (Simple Agreement for Future Equity) or convertible note to avoid complex equity valuation at an early stage.

## Seed Stage

### What It Is
Seed funding typically ranges from ₹2 crore to ₹10 crore (or $500K–$2M USD). By this stage, you have a working product, early users, and some initial traction metrics (MoM growth, retention, NPS scores).

### Who Invests at Seed
- Institutional seed funds (Blume Ventures, Kae Capital, 3one4 Capital, Stellaris in India)
- Super angel investors
- Corporate venture arms
- Family offices

### What Investors Look for at Seed
- Product-market fit signals: retention curves, weekly active users, NPS > 50
- Revenue or clear path to monetisation
- Team completeness (tech + business + domain)
- Competitive moat or defensibility

## Preparing Your Pitch Deck
A seed-stage pitch deck typically has 10–12 slides:
1. Problem — What pain are you solving? For whom?
2. Solution — Your product, how it uniquely solves the problem
3. Market Size — TAM, SAM, SOM with credible bottom-up sizing
4. Traction — Key metrics, growth rate, testimonials
5. Business Model — How do you make money?
6. Competition — Honest competitive landscape
7. Go-to-Market — How will you acquire the next 1,000 customers?
8. Team — Why are YOU the team to solve this?
9. Financials — 18-month forecast, key assumptions
10. Ask — How much are you raising and what will you use it for?

## Due Diligence Checklist
Investors will ask for: incorporation documents, cap table, IP assignment agreements, co-founder agreements, financial statements, customer contracts, and any pending litigation.
""",
    },
    {
        "title": "Series A Funding: Scaling Beyond Product-Market Fit",
        "category": "Funding",
        "summary": "How to approach Series A — typical raise size, metrics VCs expect, term sheet basics, and how to run a structured fundraising process.",
        "tags": ["series A", "VC funding", "term sheet", "growth metrics"],
        "content": """Series A is the first significant institutional round of funding, typically raised after a startup has demonstrated clear product-market fit and is ready to scale its go-to-market.

## Typical Series A Profile
- Raise size: ₹15 crore to ₹60 crore ($2M–$8M USD) in India; $5M–$15M in US
- Company age: 2–4 years post-incorporation
- Valuation: 5x–10x the seed round valuation
- Equity dilution: 15%–25% of the company

## Metrics VCs Expect Before Leading a Series A

### For SaaS Startups
- Annual Recurring Revenue (ARR): ₹3 crore–₹10 crore ($500K–$1.5M)
- Month-over-Month growth: 10%–15% consistently
- Net Revenue Retention (NRR): > 110%
- Gross margin: > 60%
- Customer Acquisition Cost (CAC) payback: < 18 months

### For Consumer/Marketplace Startups
- Monthly Active Users (MAU): 50K–500K with strong retention (D7 > 30%, D30 > 15%)
- Gross Merchandise Value (GMV) or transaction volume showing 3x–5x YoY growth
- Unit economics positive on a per-transaction basis

## Understanding Term Sheets
Key term sheet provisions to understand:

### Valuation and Dilution
Pre-money valuation determines how much equity VCs receive. If you raise ₹20 crore at a ₹80 crore pre-money valuation, VCs receive 20% (₹20cr / ₹100cr post-money).

### Liquidation Preference
Most Series A deals include a 1x non-participating liquidation preference, meaning VCs get their money back first in an exit. Avoid 2x+ preferences and participating liquidation.

### Anti-Dilution
Broad-based weighted average anti-dilution is standard and reasonable. Avoid full-ratchet anti-dilution as it heavily penalises founders in down rounds.

### Board Composition
A typical Series A board is 5 seats: 2 founders, 1 lead investor, 2 independent directors. Maintain founder majority on the board as long as possible.

### Pro-Rata Rights
Investors want the right to participate in future rounds to maintain their ownership percentage. This is reasonable; grant it.

## Running a Structured Fundraising Process
1. Build your data room: deck, financials, MIS, cap table, legal docs
2. Identify 20–30 target investors and tier them (A-list, B-list, intros)
3. Get warm introductions from your network, existing investors, or portfolio founders
4. Run meetings in parallel over 6–8 weeks to create competitive tension
5. Aim to have multiple term sheets to negotiate better terms
6. Close within 90 days of receiving your first term sheet
""",
    },
    {
        "title": "Startup Equity and Cap Table Management",
        "category": "Legal",
        "summary": "How to structure founder equity, create an ESOP pool, manage a cap table, and avoid common equity mistakes that complicate future fundraising.",
        "tags": ["equity", "cap table", "ESOP", "vesting", "co-founders"],
        "content": """A well-structured equity foundation is critical for long-term startup success. Poor cap table decisions made early are notoriously difficult and expensive to fix later.

## Founder Equity Split
The most important decision at inception. Common approaches:

### Equal Split (50/50 or 33/33/33)
Simple and feels fair but can lead to deadlocks in decision-making. Works well when co-founders have truly equal contributions.

### Contribution-Based Split
Assess contributions across: idea origin, technical capability, domain expertise, capital contribution, network and business development ability. A common framework: start with 100% split equally, then adjust +/- based on differentiated contributions.

### The Vesting Schedule
All founder equity must vest over 4 years with a 1-year cliff. This means:
- Nothing vests in the first year (the cliff)
- 25% vests at the end of Year 1
- Remaining 75% vests monthly over Years 2–4

Without vesting, a departing co-founder keeps all their equity, which is catastrophic for the remaining team and future investors.

## ESOP (Employee Stock Option Pool)

### Why It Matters
ESOPs allow you to attract and retain talent by giving them ownership in the company. A typical ESOP pool is 10%–15% of the fully diluted share capital.

### Setting Up ESOP
1. Reserve an ESOP pool at incorporation (before the first external funding round)
2. Define the ESOP plan with vesting schedules, exercise price, and eligible employees
3. File with MCA and update the cap table
4. Issue options — not shares — to employees; shares are issued upon exercise after vesting

### ESOP Vesting for Employees
Standard: 4-year vest with 1-year cliff. Vest monthly or quarterly after the cliff. Consider acceleration provisions: single-trigger (change of control) or double-trigger (change of control + termination).

## Managing Your Cap Table

### Cap Table Structure
Track: shareholder name, share class, number of shares, % ownership (fully diluted), issue price, and date. Tools: Carta, Pulley, LetsVenture in India, or a simple Excel sheet initially.

### Fully Diluted Share Count
Always calculate ownership on a fully diluted basis: common shares + preferred shares + ESOP pool (including unissued options) + warrants + convertible notes.

### Common Mistakes to Avoid
1. Giving equity to early contractors without vesting → fix it immediately
2. Having a co-founder who left but holds 20%+ equity → negotiate a buyback
3. Not creating an ESOP pool before fundraising → VCs will require it and it dilutes existing shareholders
4. Issuing shares at par value without proper valuation → creates tax issues for employees
5. Not having a shareholders' agreement → leads to disputes on voting, drag-along, tag-along rights
""",
    },
    {
        "title": "GST Registration and Compliance for Startups",
        "category": "Taxation",
        "summary": "When and how to register for GST, HSN/SAC codes, filing returns (GSTR-1, GSTR-3B), input tax credit, and managing GST for SaaS and e-commerce startups.",
        "tags": ["GST", "taxation", "GSTR", "input tax credit", "compliance"],
        "content": """Goods and Services Tax (GST) is India's unified indirect tax applicable to the supply of goods and services. Understanding GST is essential for startup compliance and cash flow management.

## When to Register for GST

### Mandatory Registration Triggers
- Aggregate turnover exceeds ₹20 lakh per year (₹10 lakh for special category states)
- Supply of goods across state borders (inter-state supply), regardless of turnover
- e-Commerce operators and sellers on platforms like Amazon, Flipkart (mandatory, no threshold)
- Import/export of services
- Receipt of foreign remittance for services exported

### Voluntary Registration
Even if below the threshold, voluntary GST registration is advisable for B2B startups as it enables Input Tax Credit (ITC) claims and signals professionalism to corporate clients.

## GST Rates for Startups

### SaaS and Software Services
Most software services (including SaaS, cloud computing, app development) attract 18% GST under SAC code 998314 or 998315.

### Professional Services
Consulting, legal, and professional services: 18% GST.

### E-Commerce Products
Rate depends on the product category:
- Electronics: 18%
- Apparel (< ₹1,000): 5%; Apparel (> ₹1,000): 12%
- Books: 0%
- Restaurant food (non-AC): 5%

## GST Registration Process
1. Visit the GST portal (gst.gov.in)
2. Apply using Form REG-01 with: PAN, Aadhaar, COI, bank account details, address proof
3. GST number (GSTIN) is allotted within 3–7 working days
4. GSTIN format: 2-digit state code + PAN + 3 alphanumeric characters

## Filing GST Returns

### GSTR-1 (Monthly/Quarterly)
Reports all outward supplies (sales). Due: 11th of next month (monthly) or end of month following quarter.

### GSTR-3B (Monthly Summary Return)
Monthly self-assessment of tax liability and payment. Due: 20th of next month. Must be filed even with zero transactions.

### GSTR-9 (Annual Return)
Annual reconciliation of all monthly returns. Due: December 31st of the following financial year.

## Input Tax Credit (ITC)
ITC allows you to offset GST paid on purchases against GST collected on sales.
- Eligible: purchases used for business purposes with a valid GST invoice
- Not eligible: personal expenses, blocked credits (motor vehicles, food, insurance)
- ITC is claimed in GSTR-3B based on invoices reflected in GSTR-2B

## For Exported Services (Zero-Rated Supply)
SaaS and services exported to clients outside India are zero-rated — no GST is charged to the foreign client. You can either: claim a refund of ITC, or export under a Letter of Undertaking (LUT) to avoid paying GST upfront.
""",
    },
    {
        "title": "Income Tax for Startups: Section 80-IAC and Advance Tax",
        "category": "Taxation",
        "summary": "Overview of corporate income tax for startups, advance tax obligations, deductions available, and how to claim the 80-IAC exemption.",
        "tags": ["income tax", "80-IAC", "advance tax", "corporate tax", "deductions"],
        "content": """Indian startups are subject to the Income Tax Act, 1961. Understanding your tax obligations early prevents costly penalties and helps in financial planning.

## Corporate Tax Rates
- Domestic companies with turnover ≤ ₹400 crore (previous year): 25% + 7% surcharge + 4% cess = ~26% effective
- New manufacturing companies incorporated after Oct 2019 opting for concessional regime: 22% + surcharge + cess = ~25.17% effective
- Companies with turnover > ₹400 crore: 30% + surcharge + cess = ~34.94% effective

Note: Most early-stage startups will not have taxable profits for the first 2–4 years due to accumulated losses.

## Advance Tax
Companies whose estimated tax liability exceeds ₹10,000 in a financial year must pay advance tax in four instalments:
- 15% by June 15
- 45% by September 15
- 75% by December 15
- 100% by March 15

Failure to pay advance tax results in interest under Sections 234B and 234C.

## Section 80-IAC: Tax Holiday for Startups
DPIIT-recognised startups can claim 100% income tax deduction on profits for any 3 consecutive years out of the first 10 years of incorporation.

### Eligibility
- Must be incorporated between April 1, 2016 and March 31, 2025
- DPIIT recognition required
- Approval from the Inter-Ministerial Board (IMB) required
- Must be a Pvt Ltd company or LLP

### How to Claim
File Form 80-IAC with the IMB after DPIIT recognition. IMB reviews and approves. Once approved, claim the deduction in your income tax return (Form ITR-6 for companies).

## Key Deductions Available

### Section 35(1)(iv) — R&D Capital Expenditure
150% deduction on capital expenditure incurred on in-house scientific research and development.

### Section 80JJAA — New Employment Deduction
30% additional deduction on new employee salaries for 3 years, for companies with audited books and new employees earning < ₹25,000/month.

### Section 10(23FB) — Exemption for Venture Capital Funds
Income of SEBI-registered venture capital funds from investing in startups is exempt from tax — an incentive for VC investment.

## Transfer Pricing for Startups with Foreign Transactions
If your startup has transactions with related foreign entities (e.g., a US parent, offshore employees, royalty payments), transfer pricing rules under Section 92 apply. You must maintain documentation and file Form 3CEB annually.

## Filing Deadlines
- Advance tax: quarterly as above
- TDS returns: quarterly (due 31st of month following quarter)
- Annual IT Return (ITR-6): September 30th for companies with statutory audit; October 31st if transfer pricing applicable
- Tax audit (if turnover > ₹1 crore for business or ₹50 lakh for professionals): September 30th
""",
    },
    {
        "title": "Hiring Your First 10 Employees: Legal and Cultural Foundations",
        "category": "Hiring",
        "summary": "Employment contracts, PF/ESI obligations, offer letters, background checks, and how to build culture during the critical first 10 hires.",
        "tags": ["hiring", "employment", "PF", "ESI", "offer letter", "culture"],
        "content": """The first 10 employees define your startup's culture, technical foundation, and go-to-market capability. Getting hiring right early prevents legal headaches and cultural misfits that can sink a company.

## Legal Framework for Hiring

### Employment Contracts
Every employee must receive a signed employment agreement before starting. Key clauses:
- Designation, compensation (CTC breakdown), joining date
- Probation period (typically 3–6 months)
- Notice period (typically 30–90 days depending on seniority)
- Non-disclosure agreement (NDA)
- Intellectual Property (IP) assignment clause — all work created during employment belongs to the company
- Non-solicitation clause (employees cannot poach your team/clients for 1–2 years after leaving)
- Avoid non-compete clauses as they are largely unenforceable in India

### Offer Letter vs Employment Agreement
Issue an offer letter first (conditional on background check), then a full employment agreement on Day 1.

## Statutory Compliance

### EPF (Employees' Provident Fund)
Mandatory once you have 20+ employees. Both employer (12% of basic) and employee (12% of basic) contribute to the EPF. Register on the EPFO portal. Even before mandatory threshold, voluntary registration signals employer professionalism.

### ESI (Employees' State Insurance)
Mandatory once you have 10+ employees (20+ in some states). Applicable to employees earning ≤ ₹21,000/month. Employee contributes 0.75%, employer contributes 3.25% of gross wages.

### Professional Tax
State-specific. Applicable in states like Maharashtra, Karnataka, West Bengal. Deducted from employee salary (₹200/month typically) and paid to the state government.

### Gratuity
Employees who complete 5+ years of continuous service are entitled to gratuity: (last drawn salary × 15 × years of service) / 26. Most startups provision for this from Year 3.

## Compensation Structuring
CTC breakdown for tax efficiency:
- Basic (40–50% of CTC): taxable, forms base for PF
- HRA (40–50% of basic): exempt under Section 10(13A) for rented accommodation
- Special Allowance: fully taxable, used to fill up CTC
- LTA (Leave Travel Allowance): exempt for actual travel twice in 4 years
- Meal vouchers (Sodexo): ₹2,600/month tax-free
- NPS employer contribution: 10% of basic, tax-free for employer and employee

## Background Verification
For engineering and senior hires: education verification, previous employment verification, criminal record check, and reference calls. Use platforms like AuthBridge, SpringVerify, or IDfy.

## Building Culture in the First 10 Hires

### Define your values early
Write down 3–5 core values and their operational meaning (not platitudes like "integrity"). Examples: "We ship every week — incremental progress beats perfection"; "We give direct feedback without politics."

### Diversity from Day 1
Homogeneous early teams are a competitive disadvantage. Actively recruit across gender, educational background, and socioeconomic diversity.

### One-on-Ones from Week 1
Start weekly 30-minute 1:1s with every employee from their first week. Create psychological safety from the start.
""",
    },
    {
        "title": "Building a Startup Brand from Scratch",
        "category": "Branding",
        "summary": "Brand strategy fundamentals for startups — defining brand identity, positioning, visual design, naming, and building brand consistency across channels.",
        "tags": ["branding", "brand identity", "logo", "positioning", "visual design"],
        "content": """Brand is not your logo. Brand is the sum of every impression a person has of your company. Done well, it becomes your most durable competitive advantage.

## The Brand Strategy Foundation

### Define Your Brand Purpose (The "Why")
Start with Simon Sinek's Golden Circle: Why does your company exist beyond making money? For example: "We exist to make financial services accessible to India's 100 million first-generation entrepreneurs."

### Identify Your Target Audience
Be ruthlessly specific. Not "SMEs in India" but "First-generation entrepreneurs aged 28–45 running manufacturing businesses in Tier 2 cities with annual revenue of ₹1–20 crore."

### Brand Positioning Statement
Template: "For [target audience] who [have this problem], [Brand Name] is the [category] that [key benefit] because [reason to believe]."

Example: "For early-stage founders in India who struggle to navigate regulatory compliance, Startup Navigator is the knowledge platform that simplifies every step because it combines government-sourced information with expert guidance."

## Naming Your Startup

### Criteria for a Good Name
- Memorable and easy to pronounce in target markets
- Available as a .com domain and across social handles
- No trademark conflicts (search on IP India portal and USPTO)
- Ideally, the name itself conveys meaning or emotion
- Avoid generic names ("Tech Solutions Pvt Ltd") and overly literal names

### Name Generation Approaches
- Compound words: Snapdeal, Practo, Razorpay
- Invented words: Ola (meaning "hello" in Spanish), Meesho
- Metaphors: Swiggy (swift + piggy), Dunzo
- Founder names: Tata, Mahindra, Byju's

## Visual Identity

### Logo Design
Invest in a professional logo. Brief your designer with: brand personality (3 adjectives), target audience, color preferences, and examples of brands you admire and why. Expect 3–5 rounds of revisions. Cost: ₹15,000–₹1,00,000 from a professional designer.

### Color Palette
Primary color: creates immediate recognition (think Ola yellow, Zomato red). Secondary palette: 2–3 complementary colors. Test for accessibility (WCAG AA contrast ratios).

### Typography
Choose a primary typeface for headings (distinctive, brand personality) and a secondary typeface for body (readable, neutral). Stick to Google Fonts or licensed fonts.

### Brand Guidelines Document
Document: logo usage (do's and don'ts), color codes (Hex, RGB, CMYK, Pantone), typography hierarchy, photography style, tone of voice. Share with every freelancer, agency, and employee.

## Tone of Voice

### Define Your Brand Personality
Choose 3–5 personality traits: Professional but approachable? Bold and disruptive? Warm and empowering? Your tone of voice should reflect these in every piece of copy.

### Consistency Across Touchpoints
Website, social media, pitch decks, customer support emails, and product UI copy must all feel like they come from the same brand. Create a simple tone of voice guide with examples.
""",
    },
    {
        "title": "Digital Marketing Strategy for Early-Stage Startups",
        "category": "Marketing",
        "summary": "A practical digital marketing playbook for pre-revenue startups — content marketing, SEO basics, paid acquisition, social media, and measuring what matters.",
        "tags": ["digital marketing", "SEO", "content marketing", "growth", "paid ads"],
        "content": """Marketing before product-market fit is expensive and ineffective. But once you have early traction, a structured digital marketing strategy accelerates growth without burning all your seed money.

## The Funnel Framework
Think in terms of: Awareness → Interest → Consideration → Intent → Purchase → Retention → Advocacy.

Early-stage startups often over-invest in Awareness (ads) while neglecting Retention (onboarding, email). Focus budget on the stage where you have the highest dropout.

## Content Marketing: The Long Game

### Why Content Marketing Works for Startups
It builds compounding organic traffic, establishes authority, and costs primarily time rather than cash — critical when budget is tight.

### Content Strategy
1. Identify 10–15 "pillar" topics that your target audience searches for
2. Create one long-form (1,500–3,000 word) guide per topic per month
3. Repurpose each guide into: 3 LinkedIn posts, 1 Twitter thread, 1 email newsletter, 1 infographic
4. Target long-tail keywords with search volume 100–1,000/month and low competition

### SEO Basics for Startups
- On-page: keyword in H1, meta description, URL slug; internal linking between related articles
- Technical: mobile-first, page speed > 90 on Lighthouse, proper sitemap.xml, structured data
- Off-page: earn backlinks through HARO (Help a Reporter Out), guest posts, startup directories
- Tools: Google Search Console (free), Ahrefs or Semrush (paid), Screaming Frog (free tier)

## Paid Acquisition

### When to Start Paid Ads
Only after: you have a landing page that converts > 3%, you understand your CAC target, and you have at least ₹2–3 lakh to spend meaningfully.

### Channels by Stage
- Pre-PMF: Meta ads for consumer apps (lowest CPM, great targeting), Google Search for high-intent B2B
- Post-PMF scaling: LinkedIn for B2B SaaS (expensive but high quality), Google Display, YouTube for brand

### Key Metrics to Track
- Click-Through Rate (CTR): > 2% is healthy for search, > 1% for display
- Cost Per Click (CPC): varies by industry; aim for 30–50% below your industry benchmark
- Conversion Rate (CVR): landing page conversion; > 5% for a lead gen form is strong
- Customer Acquisition Cost (CAC): total marketing spend / new customers acquired
- CAC Payback Period: months to recover CAC from gross margin; target < 12 months

## Social Media Strategy

### Choose 1–2 Channels, Not 5
B2B: LinkedIn + Twitter (X). Consumer: Instagram + YouTube. Don't try to be everywhere.

### Content Calendar
Post 3x per week on your primary channel. Mix: 60% educational/value content, 20% company updates, 20% personal founder stories (highest engagement).

### Community Building
Join and contribute to communities before promoting. For tech startups: IndieHackers, Product Hunt, Reddit communities. For B2B: LinkedIn industry groups, Slack communities.

## Email Marketing

### Build Your List from Day 1
Collect emails via: website waitlist, lead magnets (free templates, guides), webinars, and product sign-ups. Email has the highest ROI of any digital channel (average 42x).

### Email Sequences for Startups
1. Welcome sequence (5 emails over 2 weeks): introduce your brand, deliver promised value, introduce your product
2. Activation sequence: guide new users to their first "aha moment"
3. Re-engagement: win back inactive users with a special offer or product update
""",
    },
    {
        "title": "Venture Capital Fundraising Process: A Founder's Playbook",
        "category": "Fundraising",
        "summary": "End-to-end guide to the VC fundraising process — targeting the right investors, warm introductions, data rooms, due diligence, and closing.",
        "tags": ["venture capital", "fundraising", "VC", "due diligence", "data room"],
        "content": """Fundraising from venture capital is a sales process. Like any sales process, it succeeds with preparation, pipeline management, and relentless follow-through.

## Preparing to Fundraise

### Know Your Numbers Cold
You will be asked these in every meeting:
- Monthly recurring revenue (MRR) and MoM growth rate
- Churn rate (monthly and annual)
- CAC and payback period
- LTV:CAC ratio (> 3:1 is healthy)
- Burn rate and runway
- Gross margin
- Number of paying customers / active users

### Build Your Data Room
Organise a shared folder (Google Drive, Notion, or Docsend) with:
- Pitch deck (investor version, not the public version)
- Company financials: P&L, balance sheet, cash flow statement (3 years if available)
- MIS/metrics dashboard: monthly cohort data, funnel metrics, unit economics
- Cap table (as of today, fully diluted)
- Incorporation documents and corporate structure chart
- Key contracts: customer contracts, vendor agreements, employment agreements
- IP documentation: patents filed, trademark registrations
- Team overview: LinkedIn profiles, org chart

## Targeting the Right VCs

### Research Before Reaching Out
Check: portfolio companies (do they have a direct competitor?), stage focus (seed vs. Series A vs. growth), sector focus (SaaS vs. consumer vs. fintech), check size, and whether they actively invest in your geography.

### Building Your Target List
Tier A: Your top 5 dream investors (best fit, most value-add). Tier B: 15 strong fits. Tier C: 30 adequate fits. Start with Tier B first to refine your pitch before hitting Tier A.

## Getting Warm Introductions

### The Gold Standard
Warm introductions from a VC's portfolio founders are the most effective. Second best: introductions from other investors, lawyers, bankers, or advisors. Cold emails have a < 3% response rate.

### How to Ask for Introductions
Be specific: "I'm fundraising for [Company]. [Investor X] invests in [sector]. I know you've worked with them on [portfolio company]. Would you be willing to forward a brief email introduction?" Make it easy with a forwardable email they can send on your behalf.

## Running the Process

### Create FOMO through Parallelism
Run meetings with all investors simultaneously over a 4–6 week window. Avoid sequential processes where you wait for one VC's decision before approaching the next — it kills momentum.

### The Investor Meeting Arc
Meeting 1 (30–45 min): Pitch and gauge interest. Follow up with deck and data room. Meeting 2 (60 min): Deep dive on product, metrics, and market. Reference check period. Partner meeting/IC: present to the full partnership. Term sheet → Negotiation → Due diligence → Close.

### Negotiation Principles
- Always negotiate; VCs expect it
- The most important terms: valuation, board composition, pro-rata rights, information rights
- Secondary concerns: anti-dilution mechanism, drag-along threshold
- Engage a startup-experienced lawyer for term sheet review (cost: ₹50,000–₹2,00,000)

## Post-Close Investor Relations
Send monthly investor updates: metrics dashboard, key wins, key challenges, asks (introductions, hires, advice). Investors who feel informed are more likely to help proactively.
""",
    },
    {
        "title": "Using AI Tools to 10x Startup Productivity",
        "category": "AI Tools",
        "summary": "Practical guide to integrating AI tools — LLMs, coding assistants, design AI, and automation — into a startup's workflows to do more with fewer people.",
        "tags": ["AI tools", "LLM", "productivity", "automation", "ChatGPT", "Cursor"],
        "content": """AI tools are now a legitimate competitive advantage for startups. A 5-person team that uses AI well can outproduce a 15-person team that doesn't.

## AI for Engineering and Development

### Coding Assistants
- Cursor: AI-native code editor; the most powerful tool for full-stack development. Its Composer feature can generate entire features from a prompt.
- GitHub Copilot: integrates into VS Code, JetBrains. Strong autocomplete and function generation.
- Codeium: free alternative to Copilot; strong for Python and JavaScript.

### Practical Tips
- Write detailed comments/docstrings before a function; AI generates better code with more context
- Use AI for: writing tests, documenting code, refactoring, SQL queries, regex, data transformations
- Don't trust AI for: security-critical code, cryptography, HIPAA/financial compliance without careful review

### AI for Infrastructure
- AWS Bedrock, Google Vertex AI: managed AI services for embedding, generation, and classification
- Pulumi AI: generates infrastructure-as-code from natural language
- Warp terminal: AI-native terminal with command suggestions and debugging

## AI for Content and Marketing

### Writing and Copywriting
- Claude (Anthropic): best for long-form content, analysis, and nuanced writing
- ChatGPT (OpenAI): strong for brainstorming, outlines, and marketing copy
- Jasper, Copy.ai: purpose-built for marketing teams with templates

### Workflow for AI-Assisted Content
1. Brief: write a 200-word brief with target audience, tone, key points, and SEO keyword
2. Generate: create a first draft using Claude or GPT-4
3. Edit: human editor refines, adds proprietary data, personalises voice
4. Fact-check: verify all statistics and claims — AI hallucinates
5. Publish: AI-assisted content still benefits from human editorial judgment

### Visual and Design AI
- Midjourney: best image generation for marketing assets
- Adobe Firefly: integrated into Adobe Creative Cloud; commercially safe images
- Canva AI: drag-and-drop design with AI-generated elements; ideal for non-designers
- Framer AI: generates website designs from text prompts

## AI for Customer Support

### AI Chatbots
Deploy an AI chatbot (Intercom, Crisp, or a custom LangChain-based bot) on your website and in-app. Train it on your documentation, FAQs, and common support tickets. Can deflect 40–60% of support queries.

### Sentiment Analysis
Use AI to automatically tag and prioritise support tickets by: sentiment, urgency, and topic. Tools: Zendesk AI, Freshdesk AI, or a simple OpenAI API integration.

## AI for Sales and Outreach

### Lead Research and Personalisation
- Clay: enriches contact data and auto-generates personalised outreach copy
- Apollo.io AI: suggests optimal outreach timing and messaging
- Lemlist: AI-personalises cold email sequences at scale

### CRM Intelligence
- Salesforce Einstein: next best action recommendations
- HubSpot AI: email writing assistant, call transcription and summarisation

## Building Responsible AI Practices
- Establish a clear AI usage policy for your team: what data can and cannot be shared with AI tools (never share customer PII, proprietary source code, or confidential contracts with public AI tools)
- Audit AI outputs for bias before deploying customer-facing features
- Disclose AI-generated content to users where legally required (EU AI Act)
""",
    },
    {
        "title": "Product-Market Fit: How to Know When You Have It",
        "category": "Growth",
        "summary": "Frameworks and metrics for identifying product-market fit — Sean Ellis test, retention curves, NPS, and what to do before and after you find it.",
        "tags": ["PMF", "product-market fit", "retention", "NPS", "growth"],
        "content": """Product-market fit (PMF) is the degree to which a product satisfies a strong market demand. It's the single most important milestone for an early-stage startup — everything else (marketing, hiring, fundraising) becomes easier after you have it.

## How to Know If You Have PMF

### The Sean Ellis Test
Survey your users: "How would you feel if you could no longer use [Product]?" If > 40% say "Very disappointed," you likely have PMF. Benchmarks from Superhuman research show that reaching 40%+ correlates strongly with successful growth.

### Retention Curves
Plot Day 1, Day 7, Day 30, Day 90 retention (percentage of users who return after their first use). A flattening retention curve (even at 10–20% for consumer, 70%+ for SaaS) indicates PMF. A curve that hits zero by Day 30 means you don't have PMF.

### Net Promoter Score (NPS)
Ask users: "How likely are you to recommend [Product] to a friend? (0–10)" NPS > 50 is excellent; NPS > 30 indicates healthy PMF. B2B benchmarks are typically lower than consumer.

### Organic Growth and Word of Mouth
If > 25% of your new users are coming from referrals or word-of-mouth (measured by asking "How did you hear about us?"), that's a strong PMF signal.

### Revenue Retention
For B2B SaaS: Net Revenue Retention (NRR) > 100% means existing customers are expanding faster than they're churning — a clear PMF signal.

## Before PMF: Searching Mode

### What to Focus On
Talk to users daily. Build the minimum features required to solve the core problem. Kill features that users don't use. Measure retention, not acquisition.

### Avoiding Premature Scaling
Scaling before PMF is the #1 startup killer. Hiring a marketing team, running paid ads, or hiring 20 engineers before PMF just burns cash faster. Stay lean until the signals are clear.

### How Long It Takes
Median time to PMF is 2–3 years. Some find it in 6 months; others pivot 3 times before finding it. Don't rush; don't give up without trying at least 2–3 distinct customer segments.

## After PMF: Growth Mode

### Scaling Distribution
Once you have PMF, the bottleneck shifts from product to distribution. Invest in: content marketing and SEO, paid acquisition, partnerships and integrations, inside sales for B2B.

### Maintaining PMF at Scale
PMF can break as you expand to new customer segments, geographies, or price points. Run the Sean Ellis survey quarterly. Monitor NPS and retention curves by cohort. Stay close to your fastest-growing customer segment.

### The Transition to Series A
Investors fund the scaling of PMF, not the search for it. The clearest signal for Series A readiness: consistent MoM growth in revenue/users, flattening (not declining) retention curves, and emerging word-of-mouth growth.
""",
    },
    {
        "title": "Intellectual Property Protection for Startups",
        "category": "Legal",
        "summary": "How to protect your startup's IP — trademarks, patents, copyrights, trade secrets, and IP assignment from founders and employees.",
        "tags": ["IP", "trademark", "patent", "copyright", "trade secrets"],
        "content": """Intellectual property (IP) is often a startup's most valuable asset. Protecting it early — before raising money, before hiring employees, and before going public — is critical.

## Types of IP Relevant to Startups

### Trademarks
Protects your brand name, logo, tagline, and distinctive signs that identify your business. In India, registered under the Trade Marks Act, 1999 by the Controller General of Patents, Designs and Trade Marks (CGPDTM).

**Process:**
1. Search the trademark registry (ipindia.gov.in) for conflicts
2. File application Form TM-A with applicable class (Nice Classification)
3. Examination: 3–4 months; the examiner may raise objections
4. Publication in the Trademark Journal: if no opposition within 4 months, proceed
5. Registration certificate issued: valid for 10 years, renewable indefinitely

**Cost:** Government fee ₹4,500–₹9,000 per class; total with lawyer ₹10,000–₹30,000.

### Patents
Protects novel inventions (products or processes). Requirements: novelty (not previously known anywhere), non-obviousness (not obvious to a person skilled in the art), industrial applicability.

**India Patent Process:**
1. Conduct a prior art search (Google Patents, Espacenet)
2. File a provisional application to establish a priority date (₹1,750 for startups)
3. File complete specification within 12 months
4. Examination and prosecution: 3–5 years
5. Grant: valid for 20 years from filing

**Patentable in Software Context:** Business methods and pure software are not patentable in India. However, software that produces a technical effect or is part of a technical process may qualify.

### Copyrights
Automatically protects original works of authorship — code, content, design, artwork. In India, registration under the Copyright Act, 1957 is not mandatory but provides evidence of ownership.

### Trade Secrets
Information that has commercial value because it is not publicly known and you take reasonable steps to keep it secret. Protect by: NDAs, access controls, restricting access to source code, and documenting confidentiality obligations.

## IP Assignment: The Critical Clause

### From Founders
All IP created by founders before and during the company's operation must be formally assigned to the company. Use an IP Assignment Agreement signed at incorporation. VCs will specifically check for this.

### From Employees
Every employment agreement must include an IP assignment clause: "Any invention, design, software, or work product created by the employee during the course of employment, or using company resources, is the exclusive property of the company."

### From Contractors and Freelancers
Work created by contractors is not automatically owned by you in India. You must have a written contract with an IP assignment clause. "Work for hire" is a US legal concept; it does not automatically apply in India.

## IP Due Diligence
Investors will check: Are all IP rights assigned to the company? Are there any third-party IP claims? Are all software licenses compliant? Are there any open-source licenses with copyleft terms that could contaminate proprietary code?
""",
    },
    {
        "title": "Financial Modelling for Startups: Building a 3-Year Forecast",
        "category": "Fundraising",
        "summary": "How to build a startup financial model — revenue drivers, unit economics, burn rate, runway, and presenting financials to investors.",
        "tags": ["financial model", "forecasting", "burn rate", "runway", "unit economics"],
        "content": """A credible financial model is not about predicting the future accurately — it's about demonstrating that you understand your business drivers and can think rigorously about growth. Investors use it to stress-test your assumptions.

## The Three Core Statements

### Income Statement (P&L)
Revenue - Cost of Goods Sold = Gross Profit
Gross Profit - Operating Expenses = EBITDA
EBITDA - Depreciation - Interest - Taxes = Net Profit / Loss

For startups, the key metrics are: Revenue growth rate, Gross margin %, and EBITDA burn.

### Cash Flow Statement
Tracks actual cash in and out. Startups often confuse profit with cash — you can be profitable on paper but run out of cash due to payment timing. Cash flow = Net income + Non-cash items (depreciation) ± Working capital changes.

### Balance Sheet
Assets = Liabilities + Equity. Key for startups: cash position, deferred revenue (a liability), and shareholder equity (paid-up capital + accumulated losses).

## Building Your Revenue Model

### Bottom-Up Approach (Preferred by Investors)
Start from operational drivers, not a top-down "we'll capture 1% of a ₹10,000 crore market" projection.

**For SaaS:**
New MRR = (Leads × Conversion Rate to Trial × Conversion Rate to Paid × ACV) / 12
Net MRR = Previous MRR + New MRR - Churned MRR + Expansion MRR

**For Marketplace/E-commerce:**
GMV = (Monthly active buyers × Average order frequency × Average order value)
Revenue = GMV × Take Rate

**For Services/Consulting:**
Revenue = (Number of consultants × Billable hours per month × Billing rate) × Utilisation rate

## Unit Economics: The Foundation

### Customer Acquisition Cost (CAC)
CAC = Total Sales & Marketing Spend / New Customers Acquired (in same period)
Industry benchmark: CAC should be recoverable within 12–18 months.

### Customer Lifetime Value (LTV)
LTV = (Average Monthly Revenue per Customer × Gross Margin %) / Monthly Churn Rate
A healthy LTV:CAC ratio is 3:1 or higher.

### Payback Period
Payback Period = CAC / (Monthly Revenue per Customer × Gross Margin %)

## Modeling Burn Rate and Runway
Monthly Burn Rate = Total Cash Outflows - Total Cash Inflows
Runway (months) = Current Cash Balance / Net Monthly Burn

Maintain at least 12–18 months of runway at all times. Start your next fundraise when you have 9 months of runway left.

## Key Assumptions to Document
Every number in your model should trace back to an assumption. Document: conversion rates (source: your own data or industry benchmarks), churn rate, average contract value, headcount plan with salary grades, and infrastructure costs.

## Presenting Financials to Investors
Focus on: Year 1 actuals vs. plan (shows execution ability), Year 2–3 projections driven by the fundraise (what will you do with the money?), key inflection points (when do you hit profitability? When do you need the next raise?). Show a base case, bear case, and bull case.
""",
    },
    {
        "title": "Growth Hacking for Startups: Viral Loops and Retention Engines",
        "category": "Growth",
        "summary": "Proven growth hacking techniques — referral programs, viral loops, activation optimisation, and cohort analysis for sustainable startup growth.",
        "tags": ["growth hacking", "viral loop", "referral", "retention", "activation"],
        "content": """Growth hacking is not about tricks. It's about building systematic processes to discover and exploit growth channels faster than traditional marketing.

## The AARRR Framework (Pirate Metrics)

### Acquisition
How do users first find you? Track by channel: organic search, paid ads, referral, direct, social. Identify your highest-converting acquisition channel and double down.

### Activation
Does the user have a great first experience? The "aha moment" is the specific action that correlates with long-term retention. For Slack: sending your first message. For Dropbox: sharing a folder. Find your aha moment by analysing what actions your retained users took in their first session.

### Retention
Do users come back? This is the most important metric. Improve retention before investing in acquisition. A leaky bucket: spending ₹10 lakh/month acquiring users who churn in 30 days is negative ROI.

### Revenue
How do you convert free users to paying users? Test pricing models: freemium with a feature paywall, free trial with credit card, usage-based pricing.

### Referral
How do you get users to tell others? Build referral into the product itself — not as an afterthought.

## Building a Viral Loop

### Inherent Virality (Built into the Product)
Examples: Calendly (sharing a scheduling link), Zoom (inviting someone to a meeting), Canva (sharing a design). Every use of the product naturally introduces a new potential user.

### How to Design Viral Loops
1. Identify a core user action that involves sharing or inviting others
2. Make sharing frictionless (1-click share, pre-populated message)
3. Give the recipient a reason to try the product (the invite is also a value proposition)
4. Measure Viral Coefficient (K-factor): K = (Average invitations sent per user) × (Conversion rate of invitations)
5. K > 1 = exponential growth; K < 1 = growth dependent on other channels

### Referral Programs
Dropbox's referral program (give 500MB, get 500MB) grew signups by 60% permanently. Design: reward both referrer and referee; make the reward valuable enough to motivate but not so valuable it attracts fraudsters; track by unique referral links.

## Activation Optimisation

### Onboarding is Activation
The first 5 minutes determine whether a user stays. Map your current onboarding flow and identify every point where users drop off.

### Tactics to Improve Activation
- Progressive disclosure: show only what's needed at each step; don't overwhelm new users
- Empty state design: when a user has no data, show them what the product looks like with data
- Personalization: ask 3–5 questions at signup and customise the experience
- Success milestones: celebrate the user's first achievement in the product
- Email/SMS nudges: trigger automated messages when users don't complete key activation steps

## Cohort Analysis: The Growth Hacker's Microscope
Group users by the week or month they first used your product. Track retention, revenue, and activation by cohort. Look for: cohorts improving over time (your product is getting better), or specific cohort drops (a bad release or bad campaign).
""",
    },
    {
        "title": "LLP vs Private Limited: Choosing the Right Business Structure",
        "category": "Registration",
        "summary": "Detailed comparison of LLP and Private Limited Company for Indian startups — taxation, compliance, fundraising ability, and when to choose each.",
        "tags": ["LLP", "pvt ltd", "business structure", "registration", "comparison"],
        "content": """Choosing the right legal structure at the start is a critical decision. The two most popular structures for Indian startups are the Limited Liability Partnership (LLP) and the Private Limited Company (Pvt Ltd). Each has distinct advantages and limitations.

## Limited Liability Partnership (LLP)

### Structure
Governed by the Limited Liability Partnership Act, 2008. Partners have limited liability (like shareholders), but management is flexible without the rigid corporate structure. Regulated by the Ministry of Corporate Affairs (MCA).

### Key Advantages of LLP
- Lower compliance burden: no mandatory board meetings, fewer MCA filings
- No mandatory statutory audit if turnover < ₹40 lakh and capital contribution < ₹25 lakh
- Tax pass-through: LLP income is taxed at partner level, no dividend distribution tax
- LLP Agreement is more flexible than MOA/AOA for profit-sharing arrangements
- Lower government fees for registration and annual filings

### Key Disadvantages of LLP
- Cannot raise equity funding from angel investors or VCs — investors cannot hold "shares" in an LLP; they can only become partners
- ESOP is not possible — cannot issue stock options to employees
- Foreign Direct Investment (FDI) is allowed only in certain sectors under the approval route
- Conversion from LLP to Pvt Ltd later is complex and involves tax implications

### When to Choose LLP
- Professional services firms (law, consulting, accounting) where partners are central to service delivery
- Businesses that will never seek external equity funding
- Businesses owned by NRIs or foreign nationals (simpler compliance)
- Real estate and investment holding structures

## Private Limited Company (Pvt Ltd)

### Structure
Governed by Companies Act, 2013. Separate legal entity with shareholders and directors. Maximum 200 shareholders. Cannot publicly list shares.

### Key Advantages of Pvt Ltd
- Can raise equity funding from angel investors, VCs, and private equity
- ESOP is well-defined and straightforward — critical for hiring top talent
- Limited liability for shareholders
- Easier to transfer shares, bring in new investors, and structure buyouts
- Better brand credibility for enterprise B2B clients and in regulatory contexts
- FDI is allowed under automatic route for most sectors

### Key Disadvantages of Pvt Ltd
- Higher compliance burden: mandatory board meetings, annual filings, statutory audit regardless of size
- Dividend distribution: profits distributed to shareholders are first taxed at corporate level, then at shareholder level (double taxation mitigation: salary to founder-directors)
- More expensive to set up and maintain (auditor fees, professional fees)

### When to Choose Pvt Ltd
- Any startup intending to raise external equity funding
- Technology companies that need to offer ESOPs to attract talent
- Businesses with multiple co-founders and complex equity arrangements
- B2B companies selling to enterprise clients who require contractual counterparties

## The Decision Framework
Choose LLP if: bootstrapped professional services firm, no plans for external equity, founders prefer flexibility. Choose Pvt Ltd if: seeking investor funding, need ESOPs, building a scalable technology product.

## Converting LLP to Pvt Ltd
Possible under Section 366 of Companies Act, 2013, but involves: revaluation of assets, capital gains tax on appreciation, stamp duty, and complex restructuring. Always better to start as Pvt Ltd if funding is the plan.
""",
    },
    {
        "title": "Startup Legal Agreements: The 5 Contracts Every Founder Must Have",
        "category": "Legal",
        "summary": "The five essential legal agreements for startups — co-founder agreement, NDA, term sheet, shareholder agreement, and employment contract — with key clauses explained.",
        "tags": ["legal", "contracts", "co-founder agreement", "NDA", "shareholder agreement"],
        "content": """Legal agreements are the foundation of startup governance. Getting them right early prevents expensive disputes and makes fundraising smoother.

## 1. Co-Founder Agreement

The most important early document. Governs the relationship between co-founders before external investors arrive.

### Key Clauses
- **Equity split and vesting:** Define each founder's percentage and the vesting schedule (4-year with 1-year cliff is standard)
- **Roles and responsibilities:** Who is CEO, CTO, etc.; decision-making authority
- **IP assignment:** All pre-existing and future IP is assigned to the company
- **Buy-sell provisions:** What happens when a co-founder wants to leave or is asked to leave — right of first refusal at agreed valuation
- **Non-compete and non-solicitation:** Typically 1–2 years post-departure
- **Dispute resolution:** Arbitration clause specifying seat, rules (SIAC, LCIA, or domestic arbitration)
- **Deadlock resolution:** When founders disagree, who has the casting vote? Is it the CEO? Do you use a Russian Roulette clause?

## 2. Non-Disclosure Agreement (NDA)

Use before sharing confidential information with: potential co-founders, advisors, vendors, or potential partners (NOT investors — most investors refuse to sign NDAs).

### Key Clauses
- Definition of Confidential Information (be specific — "all information shared" is better than listing categories)
- Exclusions: publicly available information, independently developed information
- Term: typically 2–3 years
- Recipient's obligations: not to use or disclose; restrict access within their organisation
- Return or destruction of information on termination
- Injunctive relief: breach of NDA justifies immediate injunction without bond

## 3. Term Sheet

A non-binding document (except for exclusivity and confidentiality provisions) that outlines the key terms of an investment before drafting the full set of transaction documents.

### Key Terms to Negotiate
- **Pre-money valuation:** Directly determines your dilution
- **Investment amount and tranche structure:** Is the full amount invested upfront or in tranches tied to milestones?
- **Liquidation preference:** 1x non-participating preferred is fair; resist 2x or participating preferred
- **Anti-dilution:** Broad-based weighted average is fair; resist full ratchet
- **Board composition:** Maintain founder-majority board as long as possible
- **Drag-along rights:** Investors can force founders to vote for an acquisition — negotiate the threshold (e.g., 75%+ approval required)
- **Tag-along rights:** Minority shareholders can join when majority sells — standard and reasonable
- **Information rights:** Quarterly financials, annual audited statements, monthly MIS — reasonable
- **ROFR (Right of First Refusal):** Investors get to buy shares before founders can sell to third parties

## 4. Shareholders' Agreement (SHA)

The binding agreement between all shareholders that governs the company's operation. Executed after the term sheet is agreed and before funds are transferred.

### Additional Provisions in SHA vs. Term Sheet
- Reserved matters: specific decisions (raising > ₹X crore debt, acquisitions, key hires) require investor approval
- Restrictive covenants on founders: founders cannot start competing businesses during employment
- Exit provisions: drag-along, tag-along, right of first refusal on founder shares
- Representation and warranties: founders represent that the company's information provided is accurate

## 5. Employment Contract

Covered in detail in the hiring article. For senior hires and early employees, additionally include: equity grant letters (options from ESOP pool), specific termination provisions (for-cause vs. without-cause), and any specific KPIs tied to the role.
""",
    },
    {
        "title": "Building a Marketing Funnel for B2B SaaS Startups",
        "category": "Marketing",
        "summary": "How to build a B2B SaaS marketing funnel — ICP definition, inbound vs outbound, lead scoring, SDR/AE model, and measuring pipeline coverage.",
        "tags": ["B2B SaaS", "marketing funnel", "ICP", "inbound", "outbound", "SDR"],
        "content": """B2B SaaS growth requires a systematic marketing and sales engine. Unlike consumer products, every stage of the funnel must be deliberately designed and measured.

## Step 1: Define Your Ideal Customer Profile (ICP)

Your ICP is the specific type of company that derives the most value from your product, converts fastest, retains longest, and expands most reliably.

### ICP Attributes
- **Firmographic:** Industry, company size (employees/revenue), geography, tech stack
- **Situational:** Specific trigger events (new funding, new leadership, regulatory change, rapid growth)
- **Behavioural:** How they currently solve the problem you address

### How to Find Your ICP
Analyse your 10 best existing customers: What do they have in common? What triggered them to buy? Why do they stay? This becomes your ICP hypothesis. Test it with targeted outreach.

## Step 2: Build Your Funnel Stages

For B2B SaaS, a typical funnel is:
**Awareness → Education → Consideration → Evaluation → Decision → Onboarding → Expansion → Advocacy**

### Metrics for Each Stage
- Awareness: Website traffic, branded search volume
- Education: Content downloads, webinar registrations, email list growth
- Consideration: Free trial signups, demo requests, MQL (Marketing Qualified Leads)
- Evaluation: SQL (Sales Qualified Leads), active pilots
- Decision: Proposals sent, proposals won/lost
- Expansion: NRR, upsell rate, seats added

## Inbound Marketing for B2B SaaS

### Content Strategy
Create content that maps to each funnel stage:
- Top of funnel (TOFU): Blog posts, infographics, LinkedIn posts answering "what is X" questions
- Middle of funnel (MOFU): Comparison guides, ROI calculators, case studies, webinars
- Bottom of funnel (BOFU): Demos, free trials, proposals, security questionnaires, customer references

### SEO for B2B
Focus on: commercial intent keywords ("best [category] software", "[competitor] alternative"), problem-aware keywords ("how to reduce [pain point]"), and integration keywords ("[your product] + [popular tool] integration").

## Outbound Sales for B2B

### Building the Outbound Motion
- Source leads: LinkedIn Sales Navigator, Apollo.io, Lusha, or industry-specific databases
- Personalise at scale: Use Clay or Lemlist to research each prospect and personalise the first line
- Sequence: 3–5 touch sequence over 2 weeks: email → LinkedIn → email → phone → email
- Subject lines: curiosity-gap ("Quick question about your [specific challenge]") outperform generic ones

### SDR/AE Model
At scale: Sales Development Reps (SDRs) handle outbound prospecting and qualifying inbound; Account Executives (AEs) run demos, negotiations, and closings.

## Lead Scoring
Assign points to prospect actions: email open (+1), email click (+3), visited pricing page (+10), watched demo video (+15), requested a demo (+30). Route leads above a score threshold to sales immediately.

## Pipeline Coverage
Pipeline coverage = Total pipeline value / Revenue target for the period
A healthy B2B pipeline has 3x–4x coverage: if your quarterly target is ₹1 crore, you should have ₹3–4 crore in qualified pipeline.

## Marketing Attribution
Track which channels contribute to revenue: first-touch attribution (which channel first brought the prospect), last-touch (which channel closed them), and multi-touch (credit distributed across all channels). Use a CRM like HubSpot or Salesforce to track the full journey.
""",
    },
]

RESOURCES = [
    {"title": "MCA Company Registration Portal", "category": "Registration", "url": "https://www.mca.gov.in/", "description": "Official Ministry of Corporate Affairs portal for company registration, filings, and compliance.", "resource_type": "link", "tags": ["MCA", "registration", "government"]},
    {"title": "Startup India Recognition Portal", "category": "Registration", "url": "https://www.startupindia.gov.in/", "description": "Official portal to apply for DPIIT recognition and access Startup India benefits.", "resource_type": "link", "tags": ["DPIIT", "startup india", "recognition"]},
    {"title": "GST Portal", "category": "Taxation", "url": "https://www.gst.gov.in/", "description": "Official GST registration, return filing, and payment portal.", "resource_type": "link", "tags": ["GST", "tax", "government"]},
    {"title": "IP India Trademark Search", "category": "Legal", "url": "https://ipindiaonline.gov.in/", "description": "Search existing trademarks and file trademark applications in India.", "resource_type": "link", "tags": ["trademark", "IP", "legal"]},
    {"title": "Y Combinator SAFE Documents", "category": "Fundraising", "url": "https://www.ycombinator.com/documents/", "description": "Free, standardised SAFE (Simple Agreement for Future Equity) and other legal templates from Y Combinator.", "resource_type": "template", "tags": ["SAFE", "legal templates", "fundraising"]},
    {"title": "EPFO Employer Registration", "category": "Hiring", "url": "https://unifiedportal-emp.epfindia.gov.in/", "description": "Employees' Provident Fund Organisation — register as an employer and manage PF contributions.", "resource_type": "link", "tags": ["EPF", "PF", "hiring", "compliance"]},
    {"title": "Blume Ventures Portfolio", "category": "Funding", "url": "https://blume.vc/", "description": "One of India's top seed-stage VCs — research their portfolio and investment thesis.", "resource_type": "link", "tags": ["VC", "India", "seed funding"]},
    {"title": "ProductHunt", "category": "Marketing", "url": "https://www.producthunt.com/", "description": "Launch your product and get early adopters from a community of tech enthusiasts.", "resource_type": "link", "tags": ["launch", "marketing", "community"]},
    {"title": "Google AI Studio (Gemini API)", "category": "AI Tools", "url": "https://aistudio.google.com/", "description": "Access Gemini models for your startup's AI features — free tier available.", "resource_type": "tool", "tags": ["Gemini", "AI", "API", "Google"]},
    {"title": "Carta Cap Table Management", "category": "Legal", "url": "https://carta.com/", "description": "Industry-standard cap table management, ESOP administration, and 409A valuations.", "resource_type": "tool", "tags": ["cap table", "equity", "ESOP"]},
]


def seed_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # --- Users ---
        if not db.query(User).filter(User.email == "admin@startupnav.com").first():
            admin = User(
                email="admin@startupnav.com",
                hashed_password=hash_password("StartupNav#2026Admin"),
                full_name="Admin User",
                role=UserRole.admin,
            )
            db.add(admin)
            print("  Created admin user")

        if not db.query(User).filter(User.email == "user@startupnav.com").first():
            regular = User(
                email="user@startupnav.com",
                hashed_password=hash_password("TestUser#2026"),
                full_name="Test User",
                role=UserRole.user,
            )
            db.add(regular)
            print("  Created regular user")

        # --- Articles ---
        existing_titles = {a.title for a in db.query(Article.title).all()}
        new_articles = []
        for data in ARTICLES:
            if data["title"] not in existing_titles:
                article = Article(**data)
                db.add(article)
                new_articles.append(article)
        print(f"  Inserted {len(new_articles)} new articles")

        # --- Resources ---
        existing_resource_titles = {r.title for r in db.query(Resource.title).all()}
        new_resources = 0
        for data in RESOURCES:
            if data["title"] not in existing_resource_titles:
                db.add(Resource(**data))
                new_resources += 1
        print(f"  Inserted {new_resources} new resources")

        db.commit()

        # --- ChromaDB Indexing ---
        print("\nIndexing articles into ChromaDB...")
        try:
            from app.services.rag_service import get_rag_service
            rag = get_rag_service()
            rag.reset_collection()
            all_articles = db.query(Article).filter(Article.is_published == 1).all()
            for article in all_articles:
                rag.upsert_article(article)
                print(f"  Indexed: {article.title[:60]}...")
            print(f"\n✓ Indexed {len(all_articles)} articles into ChromaDB")
        except Exception as e:
            print(f"\n⚠ ChromaDB indexing failed: {e}")
            print("  Run POST /admin/reindex after starting the server to index articles.")

    finally:
        db.close()

    print("\n✓ Seed complete!")
    print("  Admin:   admin@startupnav.com  / StartupNav#2026Admin")
    print("  User:    user@startupnav.com   / TestUser#2026")


if __name__ == "__main__":
    seed_db()
