import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "schemes.db")

SCHEMES = [
    {
        "id": "pm-kisan",
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "ministry": "Ministry of Agriculture & Farmers Welfare",
        "category": "farmers",
        "icon": "🌾",
        "description": "Direct income support of ₹6,000 per year to small and marginal farmer families, paid in three equal installments of ₹2,000 every four months directly to bank accounts via DBT.",
        "benefit": "₹6,000/year (3 installments of ₹2,000)",
        "link": "https://pmkisan.gov.in",
        "documents": json.dumps([
            "Aadhaar Card",
            "Land ownership records / Khasra-Khatauni",
            "Bank account passbook (Aadhaar-linked)",
            "Residential / domicile certificate"
        ]),
        "apply_steps": json.dumps([
            "Visit pmkisan.gov.in or nearest Common Service Centre (CSC)",
            "Click 'Farmers Corner' → 'New Farmer Registration'",
            "Enter Aadhaar number and complete OTP verification",
            "Fill in personal, land, and bank account details",
            "Submit — installments auto-credited every 4 months"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "occupation", "operator": "eq", "value": "farmer", "label": "Must be a farmer or agricultural worker", "required": True},
            {"field": "income", "operator": "lte", "value": 600000, "label": "Annual family income at or below ₹6 lakh", "required": True},
            {"field": "land", "operator": "gt", "value": 0, "label": "Must own agricultural land", "required": True},
            {"field": "extras", "operator": "contains", "value": "bank-account", "label": "Should have a valid bank account", "required": False}
        ])
    },
    {
        "id": "pm-awas-g",
        "name": "PMAY-G",
        "full_name": "Pradhan Mantri Awas Yojana – Gramin",
        "ministry": "Ministry of Rural Development",
        "category": "housing",
        "icon": "🏠",
        "description": "Provides financial assistance of ₹1.20–1.30 lakh (plains) or ₹1.30 lakh (hilly/NE/difficult areas) for construction of a pucca house with basic amenities to houseless or kutcha house dwellers.",
        "benefit": "₹1.20–1.30 lakh for pucca house construction",
        "link": "https://pmayg.nic.in",
        "documents": json.dumps([
            "Aadhaar Card",
            "MGNREGA Job Card",
            "Bank account passbook",
            "BPL / SECC certificate",
            "Caste certificate (if applicable)",
            "Self-declaration of not owning a pucca house"
        ]),
        "apply_steps": json.dumps([
            "Check your name in SECC / AwaasSoft beneficiary list at pmayg.nic.in",
            "If listed, approach Gram Panchayat or Block Development Office",
            "Gram Sabha approves the list of genuine beneficiaries",
            "Geo-tagged photographs taken at each construction stage",
            "Funds released in installments via DBT to your bank account"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "extras", "operator": "contains", "value": "no-house", "label": "Should not own a pucca house", "required": True},
            {"field": "income", "operator": "lte", "value": 300000, "label": "Annual income at or below ₹3 lakh", "required": True},
            {"field": "extras", "operator": "contains_any", "value": ["bpl", "ration-card"], "label": "BPL card or ration card holder preferred", "required": False},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "label": "SC/ST/OBC/EWS get priority allocation", "required": False}
        ])
    },
    {
        "id": "ayushman-bharat",
        "name": "Ayushman Bharat PM-JAY",
        "full_name": "Pradhan Mantri Jan Arogya Yojana",
        "ministry": "Ministry of Health & Family Welfare",
        "category": "health",
        "icon": "🏥",
        "description": "Health insurance cover of ₹5 lakh per family per year for secondary and tertiary hospitalization at over 24,000 empanelled government and private hospitals across India. Covers pre-existing conditions from day one.",
        "benefit": "₹5 lakh/year health insurance cover (cashless)",
        "link": "https://pmjay.gov.in",
        "documents": json.dumps([
            "Aadhaar Card",
            "Ration Card",
            "SECC-2011 database inclusion proof",
            "Income certificate (below ₹2 lakh)"
        ]),
        "apply_steps": json.dumps([
            "Check eligibility at mera.pmjay.gov.in or call 14555",
            "If eligible, visit any empanelled hospital or PMJAY Kendra",
            "Show Aadhaar for biometric verification",
            "Ayushman Card issued on the spot (also available via app)",
            "Present Ayushman Card at time of admission for cashless treatment"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "income", "operator": "lte", "value": 200000, "label": "Annual family income at or below ₹2 lakh", "required": True},
            {"field": "extras", "operator": "contains_any", "value": ["bpl", "ration-card"], "label": "BPL household or ration card holder (SECC-listed)", "required": True},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "label": "SC/ST/OBC/EWS categories get priority", "required": False}
        ])
    },
    {
        "id": "pmsby",
        "name": "PMSBY",
        "full_name": "Pradhan Mantri Suraksha Bima Yojana",
        "ministry": "Ministry of Finance",
        "category": "health",
        "icon": "🛡️",
        "description": "Accident insurance offering ₹2 lakh for accidental death or total disability and ₹1 lakh for partial disability. Renewable annual cover at a premium of just ₹20/year via auto-debit from your bank account.",
        "benefit": "₹2 lakh accident cover at only ₹20/year",
        "link": "https://www.myscheme.gov.in/schemes/pmsby",
        "documents": json.dumps([
            "Aadhaar Card",
            "Savings bank account (Aadhaar-linked)",
            "Mobile number linked to bank account"
        ]),
        "apply_steps": json.dumps([
            "Log in to your bank's internet banking or visit branch",
            "Enroll under PMSBY (most banks have one-click enrollment)",
            "Provide Aadhaar and mobile details for KYC",
            "₹20 auto-debited from account every June 1",
            "In case of accident, nominee claims at the bank branch"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "age", "operator": "lte", "value": 70, "label": "Must be 70 years or younger", "required": True},
            {"field": "extras", "operator": "contains", "value": "bank-account", "label": "Must have a savings bank account", "required": True}
        ])
    },
    {
        "id": "pmjjby",
        "name": "PMJJBY",
        "full_name": "Pradhan Mantri Jeevan Jyoti Bima Yojana",
        "ministry": "Ministry of Finance",
        "category": "health",
        "icon": "❤️",
        "description": "Life insurance offering ₹2 lakh cover for death from any cause — natural or accidental — at an annual premium of ₹436. One of the world's largest life insurance schemes by enrollment.",
        "benefit": "₹2 lakh life cover at ₹436/year",
        "link": "https://www.myscheme.gov.in/schemes/pmjjby",
        "documents": json.dumps([
            "Aadhaar Card",
            "Savings bank account (auto-debit consent)",
            "Mobile number linked to bank account",
            "Nominee details"
        ]),
        "apply_steps": json.dumps([
            "Enroll via bank branch, internet banking, or PMJJBY app",
            "Submit auto-debit consent form (₹436/year)",
            "Aadhaar-based KYC verification",
            "Policy certificate issued by bank / LIC",
            "Nominee submits claim to bank on death of policyholder"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "age", "operator": "lte", "value": 55, "label": "Must be 55 years or younger", "required": True},
            {"field": "extras", "operator": "contains", "value": "bank-account", "label": "Must have a savings bank account", "required": True}
        ])
    },
    {
        "id": "nsp",
        "name": "National Scholarship Portal",
        "full_name": "Central Post-Matric & Merit Scholarships",
        "ministry": "Ministry of Education / Social Justice & Empowerment",
        "category": "students",
        "icon": "🎓",
        "description": "Umbrella platform for 50+ central government scholarships for SC/ST/OBC/Minority and meritorious students at post-matric, UG, and PG levels. Covers tuition fees, maintenance allowance, and study materials via DBT.",
        "benefit": "₹3,000–₹12,000+/year + full tuition fee reimbursement",
        "link": "https://scholarships.gov.in",
        "documents": json.dumps([
            "Aadhaar Card",
            "Income certificate of parent/guardian",
            "Previous year mark sheets and admit card",
            "Bonafide certificate from current institution",
            "Student's bank account passbook",
            "Caste certificate (for category scholarships)"
        ]),
        "apply_steps": json.dumps([
            "Register at scholarships.gov.in with Aadhaar",
            "Select the relevant scholarship scheme from the list",
            "Fill academic and income details accurately",
            "Upload all required documents in prescribed format",
            "Institute verifies the application online",
            "Amount credited directly to student's bank via DBT"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "occupation", "operator": "eq", "value": "student", "label": "Must currently be a student", "required": True},
            {"field": "extras", "operator": "contains_any", "value": ["class-10", "class-12", "graduate"], "label": "Must have passed at least Class 10", "required": True},
            {"field": "income", "operator": "lte", "value": 250000, "label": "Annual family income at or below ₹2.5 lakh", "required": True},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "label": "SC/ST/OBC/EWS category for targeted scholarships", "required": False}
        ])
    },
    {
        "id": "pmegp",
        "name": "PMEGP",
        "full_name": "Prime Minister's Employment Generation Programme",
        "ministry": "Ministry of MSME",
        "category": "employment",
        "icon": "💼",
        "description": "Subsidy-linked loan scheme providing 15–35% subsidy on project cost for setting up new micro-enterprises in manufacturing (up to ₹50 lakh) and services/trade (up to ₹20 lakh). Higher subsidy for SC/ST/OBC, women, and rural applicants.",
        "benefit": "Subsidy 15–35% on project loan up to ₹50 lakh",
        "link": "https://kviconline.gov.in/pmegpeportal",
        "documents": json.dumps([
            "Aadhaar Card",
            "PAN Card",
            "Educational qualification certificates (Class 8 minimum for loans > ₹10L)",
            "Detailed Project Report (DPR)",
            "Bank account details",
            "Caste certificate / disability certificate (if applicable)",
            "EDP training completion certificate (post-approval)"
        ]),
        "apply_steps": json.dumps([
            "Apply online at kviconline.gov.in/pmegpeportal",
            "Application reviewed and shortlisted by KVIC / KVIB / DIC",
            "Interview and project assessment by Task Force Committee",
            "Mandatory EDP (Entrepreneurship Development Programme) training (10–15 days)",
            "Bank sanctions loan after training",
            "Subsidy deposited in Term Deposit — adjusted after 3 years"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "income", "operator": "lte", "value": 600000, "label": "Annual income at or below ₹6 lakh (for higher subsidy)", "required": False},
            {"field": "extras", "operator": "contains_any", "value": ["class-10", "class-12", "graduate"], "label": "Class 8 pass minimum (Class 10 preferred for large loans)", "required": False},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "label": "SC/ST/OBC/Women/PwD get 35% subsidy (vs 15–25%)", "required": False},
            {"field": "gender", "operator": "eq", "value": "female", "label": "Women entrepreneurs get 35% subsidy in urban areas", "required": False}
        ])
    },
    {
        "id": "mgnregs",
        "name": "MGNREGS",
        "full_name": "Mahatma Gandhi National Rural Employment Guarantee Scheme",
        "ministry": "Ministry of Rural Development",
        "category": "employment",
        "icon": "⛏️",
        "description": "Legal guarantee of 100 days of unskilled manual work per year to every rural household. Work must be provided within 15 days of application or unemployment allowance is paid. Current wage rates: ₹215–₹374/day depending on state.",
        "benefit": "100 days guaranteed work/year at ₹215–374/day",
        "link": "https://nrega.nic.in",
        "documents": json.dumps([
            "Aadhaar Card",
            "MGNREGA Job Card (issued by Gram Panchayat)",
            "Bank or Post Office account",
            "Residence proof (rural area)"
        ]),
        "apply_steps": json.dumps([
            "Apply for Job Card at Gram Panchayat (GP) — issued within 15 days",
            "Submit written demand for work to Gram Panchayat",
            "GP must provide work within 15 days — else unemployment allowance",
            "Work site within 5 km of residence; attendance via biometric",
            "Wages credited within 15 days of work completion"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "occupation", "operator": "in", "value": ["farmer", "daily-wage", "unemployed", "homemaker"], "label": "Willing to do unskilled manual labour (rural residents)", "required": False},
            {"field": "income", "operator": "lte", "value": 300000, "label": "Low income household (priority for allocation)", "required": False},
            {"field": "state", "operator": "not_in", "value": ["Delhi", "Goa"], "label": "Must reside in a rural area (scheme is rural-only)", "required": False}
        ])
    },
    {
        "id": "pm-mudra",
        "name": "PM MUDRA Yojana",
        "full_name": "Pradhan Mantri MUDRA Yojana",
        "ministry": "Ministry of Finance",
        "category": "employment",
        "icon": "🏪",
        "description": "Collateral-free loans to non-farm micro and small enterprises under three tiers: Shishu (up to ₹50,000), Kishore (₹50K–5 lakh), Tarun (₹5 lakh–10 lakh). Available through banks, MFIs, NBFCs, and Small Finance Banks.",
        "benefit": "Collateral-free loan up to ₹10 lakh",
        "link": "https://www.mudra.org.in",
        "documents": json.dumps([
            "Aadhaar Card",
            "PAN Card",
            "Proof of business existence / business plan",
            "Address proof of business premises",
            "Bank account statement (6 months)",
            "Two passport-size photographs"
        ]),
        "apply_steps": json.dumps([
            "Approach any PSU bank, private bank, NBFC, MFI, or RRB",
            "Fill MUDRA loan application form (Shishu/Kishore/Tarun)",
            "Submit business plan and identity/address documents",
            "Bank assesses business viability and creditworthiness",
            "Loan disbursed — MUDRA card issued for working capital",
            "Repayment tenure: 3–5 years"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "occupation", "operator": "in", "value": ["self-employed", "farmer", "unemployed", "daily-wage"], "label": "Must be self-employed or starting a business", "required": True},
            {"field": "income", "operator": "lte", "value": 600000, "label": "Annual income below ₹6 lakh (for better terms)", "required": False},
            {"field": "gender", "operator": "eq", "value": "female", "label": "Women entrepreneurs get priority and lower rates", "required": False}
        ])
    },
    {
        "id": "pmkvy",
        "name": "PMKVY 4.0",
        "full_name": "Pradhan Mantri Kaushal Vikas Yojana 4.0",
        "ministry": "Ministry of Skill Development & Entrepreneurship",
        "category": "employment",
        "icon": "🔧",
        "description": "Free short-term skill training (150–300 hours) across 300+ job roles in sectors like IT, healthcare, retail, construction, and agriculture. Trainees receive government-recognized certificates and monetary rewards on assessment.",
        "benefit": "Free training + ₹8,000 reward on certification",
        "link": "https://pmkvyofficial.org",
        "documents": json.dumps([
            "Aadhaar Card",
            "Educational qualification certificates",
            "Bank account details (for reward transfer)",
            "Passport-size photographs",
            "Mobile number (for OTP registration)"
        ]),
        "apply_steps": json.dumps([
            "Register at pmkvyofficial.org or visit nearest PMKVY Training Centre",
            "Select a job role / skill course from the sector catalogue",
            "Enroll at an NSDC-affiliated Training Partner",
            "Complete training (3 weeks–3 months depending on course)",
            "Appear for assessment by Sector Skill Council (SSC)",
            "Receive QP-NOS aligned certificate and ₹8,000 reward via DBT"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 15, "label": "Must be 15 years or older", "required": True},
            {"field": "age", "operator": "lte", "value": 45, "label": "Must be 45 years or younger", "required": True},
            {"field": "occupation", "operator": "in", "value": ["unemployed", "student", "daily-wage", "homemaker", "farmer"], "label": "Unemployed, school dropout, or seeking skill upgrade", "required": False},
            {"field": "income", "operator": "lte", "value": 300000, "label": "Annual income below ₹3 lakh (priority enrollment)", "required": False}
        ])
    },
    {
        "id": "bbbp-ssy",
        "name": "Sukanya Samriddhi Yojana",
        "full_name": "Sukanya Samriddhi Yojana (under Beti Bachao Beti Padhao)",
        "ministry": "Ministry of Women & Child Development / Finance",
        "category": "women",
        "icon": "👧",
        "description": "High-interest savings scheme for girl children with 8.2% annual interest (tax-free), under the Beti Bachao Beti Padhao initiative. Account matures when girl turns 21. Partial withdrawal allowed at 18 for education/marriage.",
        "benefit": "8.2% tax-free interest on savings up to ₹1.5 lakh/year",
        "link": "https://www.india.gov.in/sukanya-samriddhi-yojana",
        "documents": json.dumps([
            "Birth certificate of girl child",
            "Aadhaar Card of girl child",
            "Guardian's Aadhaar and PAN Card",
            "Address proof of guardian",
            "Passport-size photographs"
        ]),
        "apply_steps": json.dumps([
            "Visit any authorized bank or Post Office with documents",
            "Fill SSY account opening form",
            "Minimum deposit ₹250 (max ₹1.5 lakh/year)",
            "Account remains active for 21 years from date of opening",
            "Partial withdrawal (50%) allowed after girl turns 18",
            "Full maturity amount paid when girl turns 21"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "gender", "operator": "eq", "value": "female", "label": "Scheme is exclusively for girl children / women", "required": True},
            {"field": "age", "operator": "lte", "value": 10, "label": "SSY account can be opened only until age 10", "required": True},
            {"field": "category", "operator": "any", "value": None, "label": "Open to all categories — no income restriction", "required": False}
        ])
    },
    {
        "id": "ujjwala",
        "name": "PM Ujjwala Yojana 2.0",
        "full_name": "Pradhan Mantri Ujjwala Yojana",
        "ministry": "Ministry of Petroleum & Natural Gas",
        "category": "women",
        "icon": "🔥",
        "description": "Provides free LPG connections with stove and first refill subsidy to women from BPL/SC/ST/OBC/EWS households, replacing harmful solid fuel cooking. Over 10 crore connections given since launch.",
        "benefit": "Free LPG connection + stove + first refill",
        "link": "https://pmuy.gov.in",
        "documents": json.dumps([
            "Aadhaar Card (woman applicant's)",
            "BPL / SECC certificate or Ration Card",
            "Bank account passbook (woman's)",
            "Address proof",
            "Self-declaration of not having an LPG connection"
        ]),
        "apply_steps": json.dumps([
            "Visit nearest HP Gas / Indane / Bharat Gas distributor",
            "Fill PMUY application form",
            "Submit Aadhaar, ration card, and bank account details",
            "Distributor verifies details and submits to oil company",
            "Connection with stove and first refill delivered at home"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "gender", "operator": "eq", "value": "female", "label": "Applicant must be female (scheme is for women)", "required": True},
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "extras", "operator": "contains_any", "value": ["bpl", "ration-card"], "label": "Must hold BPL card or ration card", "required": True},
            {"field": "income", "operator": "lte", "value": 150000, "label": "Annual income below ₹1.5 lakh preferred", "required": False}
        ])
    },
    {
        "id": "atal-pension",
        "name": "Atal Pension Yojana",
        "full_name": "Atal Pension Yojana (APY)",
        "ministry": "Ministry of Finance / PFRDA",
        "category": "employment",
        "icon": "🏦",
        "description": "Government-backed pension scheme guaranteeing ₹1,000–₹5,000/month pension after age 60 for unorganised sector workers. Government co-contributes 50% of total contribution (up to ₹1,000/year) for eligible subscribers for 5 years.",
        "benefit": "₹1,000–₹5,000/month pension after age 60",
        "link": "https://npscra.nsdl.co.in/scheme-details.php",
        "documents": json.dumps([
            "Aadhaar Card",
            "Savings bank account",
            "Mobile number linked to bank",
            "KYC documents (via bank)"
        ]),
        "apply_steps": json.dumps([
            "Open account at any bank or via UPI apps (BHIM/Paytm/PhonePe)",
            "Choose pension amount (₹1K / ₹2K / ₹3K / ₹4K / ₹5K per month)",
            "Monthly contribution auto-debited based on age and pension chosen",
            "Government co-contributes 50% for first 5 years (for eligible subscribers)",
            "Pension starts at age 60; nominee gets corpus on subscriber's death"
        ]),
        "eligibility_rules": json.dumps([
            {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years or older", "required": True},
            {"field": "age", "operator": "lte", "value": 40, "label": "Must be 40 years or younger to join", "required": True},
            {"field": "extras", "operator": "contains", "value": "bank-account", "label": "Must have a savings bank account", "required": True},
            {"field": "occupation", "operator": "in", "value": ["farmer", "daily-wage", "self-employed", "homemaker", "unemployed"], "label": "Primarily for unorganised sector workers", "required": False}
        ])
    }
]


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS schemes")
    c.execute("DROP TABLE IF EXISTS eligibility_checks")

    c.execute("""
        CREATE TABLE schemes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            full_name TEXT NOT NULL,
            ministry TEXT NOT NULL,
            category TEXT NOT NULL,
            icon TEXT,
            description TEXT,
            benefit TEXT,
            link TEXT,
            documents TEXT,
            apply_steps TEXT,
            eligibility_rules TEXT
        )
    """)

    c.execute("""
        CREATE TABLE eligibility_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_hash TEXT NOT NULL,
            scheme_id TEXT NOT NULL,
            status TEXT NOT NULL,
            met_criteria INTEGER,
            total_criteria INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scheme_id) REFERENCES schemes(id)
        )
    """)

    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_checks_user ON eligibility_checks(user_hash)
    """)

    for s in SCHEMES:
        c.execute("""
            INSERT INTO schemes VALUES (
                :id, :name, :full_name, :ministry, :category, :icon,
                :description, :benefit, :link, :documents, :apply_steps, :eligibility_rules
            )
        """, s)

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH} with {len(SCHEMES)} schemes.")


if __name__ == "__main__":
    init_db()
