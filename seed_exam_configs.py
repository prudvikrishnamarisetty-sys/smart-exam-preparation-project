"""
Seed all official exam configurations.
Run: python seed_exam_configs.py
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from database import engine, SessionLocal, Base
from models import ExamConfig
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Delete existing configs to re-seed cleanly
db.query(ExamConfig).delete()
db.commit()

def cfg(key, name, cat, total_q, total_marks, duration, neg, marks_per_q, sections, icon, desc):
    db.add(ExamConfig(
        exam_key=key, display_name=name, category=cat,
        total_questions=total_q, total_marks=total_marks,
        duration_minutes=duration, negative_marking=neg,
        marks_per_question=marks_per_q,
        sections_json=json.dumps(sections),
        pattern_summary=f"{total_q} Qs | {total_marks} Marks | {duration} min | Neg: {'-' + str(neg) if neg > 0 else 'None'}",
        icon=icon, description=desc
    ))

# ── GOVT IT JOBS ─────────────────────────────────────────────────────────────
cfg("SSC_SELECTION_POST_MATRIC", "SSC Selection Post Phase-14 (Matric)", "GOVT_IT",
    100, 200, 60, 0.50, 2.0,
    [{"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"General Awareness","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"Quantitative Aptitude","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"English Language","questions":25,"marks_per_q":2,"negative":0.5}],
    "🏛️", "SSC Selection Post Phase-14 Matric Level — 100 Qs, 200 Marks, 60 min, -0.50 per wrong")

cfg("SSC_SELECTION_POST_12", "SSC Selection Post Phase-14 (10+2)", "GOVT_IT",
    100, 200, 60, 0.50, 2.0,
    [{"name":"General Intelligence","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"General Awareness","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"Quantitative Aptitude","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"English Comprehension","questions":25,"marks_per_q":2,"negative":0.5}],
    "🏛️", "SSC Selection Post Phase-14 10+2 Level — 100 Qs, 200 Marks, 60 min, -0.50 per wrong")

cfg("SSC_SELECTION_POST_GRAD", "SSC Selection Post Phase-14 (Graduate)", "GOVT_IT",
    100, 200, 60, 0.50, 2.0,
    [{"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"General Awareness","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"Quantitative Aptitude","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"English Comprehension","questions":25,"marks_per_q":2,"negative":0.5}],
    "🏛️", "SSC Selection Post Phase-14 Graduate Level — 100 Qs, 200 Marks, 60 min, -0.50 per wrong")

cfg("SSC_CGL_TIER1", "SSC CGL Tier-1", "GOVT_IT",
    100, 200, 60, 0.50, 2.0,
    [{"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"General Awareness","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"Quantitative Aptitude","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"English Comprehension","questions":25,"marks_per_q":2,"negative":0.5}],
    "📋", "SSC Combined Graduate Level Tier-1 — 100 Qs, 200 Marks, 60 min, -0.50 per wrong")

cfg("SSC_CGL_TIER2", "SSC CGL Tier-2 (Paper-I)", "GOVT_IT",
    180, 540, 180, 1.0, 3.0,
    [{"name":"Session-1: Mathematical Abilities","questions":30,"marks_per_q":3,"negative":1.0},
     {"name":"Session-1: Reasoning & General Intelligence","questions":30,"marks_per_q":3,"negative":1.0},
     {"name":"Session-2: English Lang & Comprehension","questions":45,"marks_per_q":3,"negative":1.0},
     {"name":"Session-2: General Awareness","questions":25,"marks_per_q":3,"negative":1.0},
     {"name":"Session-3: Computer Knowledge","questions":20,"marks_per_q":3,"negative":1.0},
     {"name":"Session-3: Data Entry Speed","questions":30,"marks_per_q":3,"negative":1.0}],
    "📋", "SSC CGL Tier-2 Paper-I — 180 Qs, 540 Marks, 180 min, -1.00 per wrong")

cfg("SSC_CHSL_TIER1", "SSC CHSL Tier-1", "GOVT_IT",
    100, 200, 60, 0.50, 2.0,
    [{"name":"General Intelligence","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"General Awareness","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"Quantitative Aptitude","questions":25,"marks_per_q":2,"negative":0.5},
     {"name":"English Language","questions":25,"marks_per_q":2,"negative":0.5}],
    "📝", "SSC Combined Higher Secondary Level Tier-1 — 100 Qs, 200 Marks, 60 min, -0.50 per wrong")

cfg("SSC_JE_IT", "SSC JE IT Paper-1", "GOVT_IT",
    200, 200, 120, 0.25, 1.0,
    [{"name":"General Intelligence & Reasoning","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"General Awareness","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"IT & Computer Science","questions":100,"marks_per_q":1,"negative":0.25}],
    "💻", "SSC Junior Engineer IT Paper-1 — 200 Qs, 200 Marks, 120 min, -0.25 per wrong")

cfg("GATE_CSE", "GATE Computer Science", "GOVT_IT",
    65, 100, 180, 0.33, 1.5,
    [{"name":"General Aptitude","questions":10,"marks_per_q":1.5,"negative":0.5},
     {"name":"Core CS — 1 mark Qs","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"Core CS — 2 mark Qs","questions":30,"marks_per_q":2,"negative":0.67}],
    "🖥️", "GATE CS — 65 Qs, 100 Marks, 3 hrs, Variable negative marking")

cfg("NIC_SCI_OFFICER", "NIC Scientific Officer", "GOVT_IT",
    120, 120, 120, 0.25, 1.0,
    [{"name":"Quantitative Aptitude","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"Reasoning","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"English","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"General Awareness","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"IT & Computer Science","questions":40,"marks_per_q":1,"negative":0.25}],
    "🏢", "NIC Scientific Officer — 120 Qs, 120 Marks, 120 min, -0.25 per wrong")

cfg("IBPS_SO_IT", "IBPS SO IT Officer", "GOVT_IT",
    75, 75, 45, 0.25, 1.0,
    [{"name":"Reasoning","questions":25,"marks_per_q":1,"negative":0.25},
     {"name":"English Language","questions":25,"marks_per_q":1,"negative":0.25},
     {"name":"IT Knowledge","questions":25,"marks_per_q":1,"negative":0.25}],
    "🏦", "IBPS SO IT Officer Prelims — 75 Qs, 75 Marks, 45 min, -0.25 per wrong")

cfg("RRB_JE_IT", "RRB JE IT", "GOVT_IT",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":15,"marks_per_q":1,"negative":0.33},
     {"name":"IT & Computer Science","questions":30,"marks_per_q":1,"negative":0.33}],
    "🚂", "RRB Junior Engineer IT — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("ISRO_CS", "ISRO Scientist/Engineer CS", "GOVT_IT",
    80, 240, 90, 1.0, 3.0,
    [{"name":"Computer Science & Engineering","questions":80,"marks_per_q":3,"negative":1.0}],
    "🚀", "ISRO CS — 80 Qs, 240 Marks, 90 min, -1.00 per wrong")

cfg("DRDO_CEPTAM", "DRDO CEPTAM Tech-A IT", "GOVT_IT",
    150, 150, 150, 0.50, 1.0,
    [{"name":"General Intelligence & Reasoning","questions":50,"marks_per_q":1,"negative":0.5},
     {"name":"General Awareness","questions":25,"marks_per_q":1,"negative":0.5},
     {"name":"Quantitative Aptitude","questions":25,"marks_per_q":1,"negative":0.5},
     {"name":"IT & Computer Science","questions":50,"marks_per_q":1,"negative":0.5}],
    "🛡️", "DRDO CEPTAM Tech-A IT — 150 Qs, 150 Marks, 150 min, -0.50 per wrong")

# ── B.TECH LANGUAGE / TECH EXAMS ─────────────────────────────────────────────
cfg("JAVA_OCJP", "Java OCJP/OCP", "BTECH_LANG",
    60, 60, 75, 0.0, 1.0,
    [{"name":"Java Basics & OOP","questions":20,"marks_per_q":1,"negative":0},
     {"name":"Collections & Generics","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Exception Handling & I/O","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Concurrency & Lambdas","questions":10,"marks_per_q":1,"negative":0}],
    "☕", "Java OCJP — 60 Qs, 60 Marks, 75 min, No negative marking")

cfg("PYTHON_PCEP", "Python PCEP", "BTECH_LANG",
    30, 30, 45, 0.0, 1.0,
    [{"name":"Basics & Control Flow","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Functions & Modules","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Data Structures","questions":10,"marks_per_q":1,"negative":0}],
    "🐍", "Python PCEP Entry — 30 Qs, 30 Marks, 45 min, No negative marking")

cfg("PYTHON_PCAP", "Python PCAP", "BTECH_LANG",
    40, 40, 65, 0.0, 1.0,
    [{"name":"Modules & Packages","questions":10,"marks_per_q":1,"negative":0},
     {"name":"OOP in Python","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Exceptions & File I/O","questions":15,"marks_per_q":1,"negative":0}],
    "🐍", "Python PCAP Associate — 40 Qs, 40 Marks, 65 min, No negative marking")

cfg("DSA_PRACTICE", "DSA (Data Structures & Algorithms)", "CORE_CS",
    60, 60, 90, 0.0, 1.0,
    [{"name":"Arrays & Strings","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Linked List, Stack, Queue","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Trees & Graphs","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Sorting, Searching & DP","questions":15,"marks_per_q":1,"negative":0}],
    "🔢", "DSA Practice — 60 Qs, 60 Marks, 90 min, No negative marking")

# ── CORE CS ───────────────────────────────────────────────────────────────────
cfg("DBMS_GATE", "DBMS (GATE Pattern)", "CORE_CS",
    65, 100, 180, 0.33, 1.5,
    [{"name":"General Aptitude","questions":10,"marks_per_q":1,"negative":0.33},
     {"name":"DBMS — 1 Mark","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"DBMS — 2 Marks","questions":25,"marks_per_q":2,"negative":0.67}],
    "🗄️", "DBMS GATE Pattern — 65 Qs, 100 Marks, 180 min, -0.33/-0.67 per wrong")

cfg("OS_GATE", "Operating Systems (GATE Pattern)", "CORE_CS",
    65, 100, 180, 0.33, 1.5,
    [{"name":"General Aptitude","questions":10,"marks_per_q":1,"negative":0.33},
     {"name":"OS — 1 Mark","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"OS — 2 Marks","questions":25,"marks_per_q":2,"negative":0.67}],
    "⚙️", "OS GATE Pattern — 65 Qs, 100 Marks, 180 min, -0.33/-0.67 per wrong")

cfg("CN_GATE", "Computer Networks (GATE Pattern)", "CORE_CS",
    65, 100, 180, 0.33, 1.5,
    [{"name":"General Aptitude","questions":10,"marks_per_q":1,"negative":0.33},
     {"name":"CN — 1 Mark","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"CN — 2 Marks","questions":25,"marks_per_q":2,"negative":0.67}],
    "🌐", "Computer Networks GATE Pattern — 65 Qs, 100 Marks, 180 min, -0.33/-0.67 per wrong")

# ── CLOUD / DEVOPS ────────────────────────────────────────────────────────────
cfg("AWS_SAA_C03", "AWS Solutions Architect SAA-C03", "CLOUD_DEVOPS",
    65, 65, 130, 0.0, 1.0,
    [{"name":"Cloud Concepts","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Security & Identity","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Resilient Architectures","questions":20,"marks_per_q":1,"negative":0},
     {"name":"High-Performance Architectures","questions":20,"marks_per_q":1,"negative":0}],
    "☁️", "AWS SAA-C03 — 65 Qs, 130 min, No negative marking")

cfg("AZURE_AZ104", "Azure Administrator AZ-104", "CLOUD_DEVOPS",
    50, 50, 120, 0.0, 1.0,
    [{"name":"Identity & Governance","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Storage","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Compute & Networking","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Monitoring & Backup","questions":10,"marks_per_q":1,"negative":0}],
    "🔷", "Azure AZ-104 — 50 Qs, 120 min, No negative marking")

cfg("DOCKER_DCA", "Docker Certified Associate", "CLOUD_DEVOPS",
    55, 55, 90, 0.0, 1.0,
    [{"name":"Orchestration","questions":20,"marks_per_q":1,"negative":0},
     {"name":"Image Creation & Management","questions":20,"marks_per_q":1,"negative":0},
     {"name":"Networking & Security","questions":15,"marks_per_q":1,"negative":0}],
    "🐳", "Docker DCA — 55 Qs, 90 min, No negative marking")

cfg("GCP_ACE", "Google Cloud Associate Cloud Engineer (GCP ACE)", "CLOUD_DEVOPS",
    50, 50, 120, 0.0, 1.0,
    [{"name":"Setting Up a Cloud Solution Environment","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Planning & Configuring Cloud Solution","questions":12,"marks_per_q":1,"negative":0},
     {"name":"Deploying & Implementing Cloud Solution","questions":12,"marks_per_q":1,"negative":0},
     {"name":"Ensuring Successful Operation","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Configuring Access & Security","questions":6,"marks_per_q":1,"negative":0}],
    "🌐", "GCP ACE — 50 Qs, 120 min, No negative marking")

cfg("K8S_CKA", "Kubernetes Certified Kubernetes Administrator (CKA)", "CLOUD_DEVOPS",
    66, 66, 120, 0.0, 1.0,
    [{"name":"Cluster Architecture, Installation & Configuration","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Workloads & Scheduling","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Services & Networking","questions":13,"marks_per_q":1,"negative":0},
     {"name":"Storage","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Troubleshooting","questions":13,"marks_per_q":1,"negative":0}],
    "⎈", "Kubernetes CKA — 66 Qs, 120 min, No negative marking")

# ── COMPANY HIRING TESTS ──────────────────────────────────────────────────────
cfg("TCS_NQT_IT", "TCS NQT IT", "COMPANY",
    90, 90, 90, 0.0, 1.0,
    [{"name":"Verbal Ability","questions":24,"marks_per_q":1,"negative":0},
     {"name":"Reasoning Ability","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Numerical Ability","questions":26,"marks_per_q":1,"negative":0},
     {"name":"Programming Logic","questions":10,"marks_per_q":1,"negative":0}],
    "🏢", "TCS NQT IT — 90 Qs, 90 Marks, 90 min, No negative marking")

cfg("INFOSYS_SP", "Infosys Systems Engineer SP", "COMPANY",
    65, 65, 95, 0.0, 1.0,
    [{"name":"Logical Reasoning","questions":15,"marks_per_q":1,"negative":0},
     {"name":"Mathematical Thinking","questions":10,"marks_per_q":1,"negative":0},
     {"name":"Verbal Ability","questions":20,"marks_per_q":1,"negative":0},
     {"name":"Pseudo Code & Programming","questions":20,"marks_per_q":1,"negative":0}],
    "🔵", "Infosys SP — 65 Qs, 95 min, No negative marking")

cfg("WIPRO_NLTH", "Wipro Elite NLTH", "COMPANY",
    75, 75, 75, 0.25, 1.0,
    [{"name":"Verbal Ability","questions":18,"marks_per_q":1,"negative":0.25},
     {"name":"Analytical & Logical Reasoning","questions":18,"marks_per_q":1,"negative":0.25},
     {"name":"Quantitative Aptitude","questions":18,"marks_per_q":1,"negative":0.25},
     {"name":"Programming Concepts","questions":21,"marks_per_q":1,"negative":0.25}],
    "⚡", "Wipro Elite NLTH — 75 Qs, 75 Marks, 75 min, -0.25 per wrong")

cfg("COGNIZANT_GENC", "Cognizant GenC", "COMPANY",
    70, 70, 70, 0.0, 1.0,
    [{"name":"Reasoning Ability","questions":25,"marks_per_q":1,"negative":0},
     {"name":"Verbal Ability","questions":25,"marks_per_q":1,"negative":0},
     {"name":"Quantitative Aptitude","questions":20,"marks_per_q":1,"negative":0}],
    "🎯", "Cognizant GenC — 70 Qs, 70 Marks, 70 min, No negative marking")

# ── BANKING EXAMS ─────────────────────────────────────────────────────────────
cfg("IBPS_PO_PRELIMS", "IBPS PO Prelims", "BANKING",
    100, 100, 60, 1.0, 1.0,
    [{"name":"English Language","questions":30,"marks_per_q":1,"negative":1.0},
     {"name":"Quantitative Aptitude","questions":35,"marks_per_q":1,"negative":1.0},
     {"name":"Reasoning Ability","questions":35,"marks_per_q":1,"negative":1.0}],
    "🏦", "IBPS PO Prelims — 100 Qs, 100 Marks, 60 min, -1.00 per wrong")

cfg("IBPS_PO_MAINS", "IBPS PO Mains", "BANKING",
    155, 200, 180, 0.25, 1.0,
    [{"name":"Reasoning & Computer Aptitude","questions":45,"marks_per_q":1,"negative":0.25},
     {"name":"English Language","questions":35,"marks_per_q":1,"negative":0.25},
     {"name":"Data Analysis & Interpretation","questions":35,"marks_per_q":1,"negative":0.25},
     {"name":"General Economy & Banking Awareness","questions":40,"marks_per_q":1,"negative":0.25}],
    "🏦", "IBPS PO Mains — 155 Qs, 200 Marks, 180 min, -0.25 per wrong")

cfg("IBPS_CLERK_PRELIMS", "IBPS Clerk Prelims", "BANKING",
    100, 100, 60, 1.0, 1.0,
    [{"name":"English Language","questions":30,"marks_per_q":1,"negative":1.0},
     {"name":"Numerical Ability","questions":35,"marks_per_q":1,"negative":1.0},
     {"name":"Reasoning Ability","questions":35,"marks_per_q":1,"negative":1.0}],
    "🏦", "IBPS Clerk Prelims — 100 Qs, 100 Marks, 60 min, -1.00 per wrong")

cfg("SBI_PO_PRELIMS", "SBI PO Prelims", "BANKING",
    100, 100, 60, 0.25, 1.0,
    [{"name":"English Language","questions":30,"marks_per_q":1,"negative":0.25},
     {"name":"Quantitative Aptitude","questions":35,"marks_per_q":1,"negative":0.25},
     {"name":"Reasoning Ability","questions":35,"marks_per_q":1,"negative":0.25}],
    "🏛️", "SBI PO Prelims — 100 Qs, 100 Marks, 60 min, -0.25 per wrong")

cfg("SBI_CLERK_PRELIMS", "SBI Clerk Prelims (Junior Associate)", "BANKING",
    100, 100, 60, 0.25, 1.0,
    [{"name":"English Language","questions":30,"marks_per_q":1,"negative":0.25},
     {"name":"Numerical Ability","questions":35,"marks_per_q":1,"negative":0.25},
     {"name":"Reasoning Ability","questions":35,"marks_per_q":1,"negative":0.25}],
    "🏛️", "SBI Clerk Prelims — 100 Qs, 100 Marks, 60 min, -0.25 per wrong")

cfg("RBI_GRADE_B", "RBI Grade B Officer Phase-1", "BANKING",
    200, 200, 120, 0.25, 1.0,
    [{"name":"General Awareness","questions":80,"marks_per_q":1,"negative":0.25},
     {"name":"English Language","questions":30,"marks_per_q":1,"negative":0.25},
     {"name":"Quantitative Aptitude","questions":30,"marks_per_q":1,"negative":0.25},
     {"name":"Reasoning","questions":60,"marks_per_q":1,"negative":0.25}],
    "💰", "RBI Grade B Phase-1 — 200 Qs, 200 Marks, 120 min, -0.25 per wrong")

cfg("NABARD_GRADE_A", "NABARD Grade A Prelims", "BANKING",
    200, 200, 120, 0.25, 1.0,
    [{"name":"Reasoning","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"English Language","questions":40,"marks_per_q":1,"negative":0.25},
     {"name":"Computer Knowledge","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"General Awareness","questions":40,"marks_per_q":1,"negative":0.25},
     {"name":"Quantitative Aptitude","questions":40,"marks_per_q":1,"negative":0.25},
     {"name":"Economic & Social Issues","questions":40,"marks_per_q":1,"negative":0.25}],
    "🌾", "NABARD Grade A Prelims — 200 Qs, 200 Marks, 120 min, -0.25 per wrong")

# ── RAILWAY EXAMS ─────────────────────────────────────────────────────────────
cfg("RRB_NTPC_CBT1", "RRB NTPC CBT-1", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":40,"marks_per_q":1,"negative":0.33}],
    "🚂", "RRB NTPC CBT-1 — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_NTPC_CBT2", "RRB NTPC CBT-2", "RAILWAY",
    120, 120, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":35,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":35,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":50,"marks_per_q":1,"negative":0.33}],
    "🚂", "RRB NTPC CBT-2 — 120 Qs, 120 Marks, 90 min, -0.33 per wrong")

cfg("RRB_GROUP_D", "RRB Group D (ALP/Technician)", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Science","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness & Current Affairs","questions":20,"marks_per_q":1,"negative":0.33}],
    "🚃", "RRB Group D — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_ALP_STAGE1", "RRB ALP Stage-1", "RAILWAY",
    75, 75, 60, 0.33, 1.0,
    [{"name":"Mathematics","questions":20,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Science","questions":20,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness on Current Affairs","questions":10,"marks_per_q":1,"negative":0.33}],
    "🚄", "RRB ALP Stage-1 — 75 Qs, 75 Marks, 60 min, -0.33 per wrong")

cfg("RRB_ALP_STAGE2_PARTA", "RRB ALP Stage-2 Part-A (CBT)", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"Basic Science & Engineering","questions":40,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness on Current Affairs","questions":10,"marks_per_q":1,"negative":0.33}],
    "🚄", "RRB ALP Stage-2 Part-A — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_ALP_STAGE2_PARTB", "RRB ALP Stage-2 Part-B (Trade Syllabus)", "RAILWAY",
    75, 75, 60, 0.0, 1.0,
    [{"name":"Trade-Specific Technical Questions","questions":75,"marks_per_q":1,"negative":0}],
    "🚄", "RRB ALP Stage-2 Part-B — 75 Qs, 75 Marks, 60 min, No negative marking")

cfg("RRB_JE_CIVIL", "RRB JE Civil Engineering", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":15,"marks_per_q":1,"negative":0.33},
     {"name":"Civil Engineering","questions":30,"marks_per_q":1,"negative":0.33}],
    "🏗️", "RRB JE Civil — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_JE_MECH", "RRB JE Mechanical Engineering", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":15,"marks_per_q":1,"negative":0.33},
     {"name":"Mechanical Engineering","questions":30,"marks_per_q":1,"negative":0.33}],
    "⚙️", "RRB JE Mechanical — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_JE_EEE", "RRB JE Electrical Engineering (EEE)", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":15,"marks_per_q":1,"negative":0.33},
     {"name":"Electrical Engineering","questions":30,"marks_per_q":1,"negative":0.33}],
    "⚡", "RRB JE EEE — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_JE_ECE", "RRB JE Electronics & Communication (ECE)", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":25,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":15,"marks_per_q":1,"negative":0.33},
     {"name":"Electronics & Communication","questions":30,"marks_per_q":1,"negative":0.33}],
    "📡", "RRB JE ECE — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_CONSTABLE_RPF", "RRB RPF Constable", "RAILWAY",
    120, 120, 90, 0.25, 1.0,
    [{"name":"General Awareness / Current Affairs","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"Arithmetic","questions":35,"marks_per_q":1,"negative":0.25},
     {"name":"General Intelligence & Reasoning","questions":35,"marks_per_q":1,"negative":0.25}],
    "🚔", "RRB RPF Constable — 120 Qs, 120 Marks, 90 min, -0.25 per wrong")

cfg("RRB_SI_RPF", "RRB RPF Sub-Inspector (SI)", "RAILWAY",
    120, 120, 90, 0.25, 1.0,
    [{"name":"General Awareness / Current Affairs","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"Arithmetic","questions":35,"marks_per_q":1,"negative":0.25},
     {"name":"General Intelligence & Reasoning","questions":35,"marks_per_q":1,"negative":0.25}],
    "🚔", "RRB RPF SI — 120 Qs, 120 Marks, 90 min, -0.25 per wrong")

cfg("RRB_PARAMEDICAL", "RRB Paramedical Staff", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"General Awareness","questions":20,"marks_per_q":1,"negative":0.33},
     {"name":"Mathematics","questions":20,"marks_per_q":1,"negative":0.33},
     {"name":"General Intelligence & Reasoning","questions":10,"marks_per_q":1,"negative":0.33},
     {"name":"Professional Knowledge (Medical/Health)","questions":50,"marks_per_q":1,"negative":0.33}],
    "🏥", "RRB Paramedical — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

cfg("RRB_MINISTERIAL_ISOLATED", "RRB Ministerial & Isolated Categories", "RAILWAY",
    100, 100, 90, 0.33, 1.0,
    [{"name":"General Intelligence & Reasoning","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"General Awareness","questions":30,"marks_per_q":1,"negative":0.33},
     {"name":"Arithmetic","questions":20,"marks_per_q":1,"negative":0.33},
     {"name":"English Language","questions":20,"marks_per_q":1,"negative":0.33}],
    "📋", "RRB Ministerial/Isolated — 100 Qs, 100 Marks, 90 min, -0.33 per wrong")

# ── DEFENCE EXAMS ─────────────────────────────────────────────────────────────
cfg("NDA_MATHS", "NDA Mathematics Paper", "DEFENCE",
    120, 300, 150, 1.33, 2.5,
    [{"name":"Algebra","questions":30,"marks_per_q":2.5,"negative":0.83},
     {"name":"Matrices & Determinants","questions":15,"marks_per_q":2.5,"negative":0.83},
     {"name":"Calculus","questions":20,"marks_per_q":2.5,"negative":0.83},
     {"name":"Trigonometry","questions":20,"marks_per_q":2.5,"negative":0.83},
     {"name":"Statistics & Probability","questions":15,"marks_per_q":2.5,"negative":0.83},
     {"name":"Vector Algebra","questions":20,"marks_per_q":2.5,"negative":0.83}],
    "⚔️", "NDA Mathematics — 120 Qs, 300 Marks, 150 min, -0.83 per wrong")

cfg("NDA_GAT", "NDA General Ability Test (GAT)", "DEFENCE",
    150, 600, 150, 2.0, 4.0,
    [{"name":"English","questions":50,"marks_per_q":4,"negative":1.33},
     {"name":"Physics","questions":25,"marks_per_q":4,"negative":1.33},
     {"name":"Chemistry","questions":15,"marks_per_q":4,"negative":1.33},
     {"name":"General Science","questions":10,"marks_per_q":4,"negative":1.33},
     {"name":"History & Geography","questions":30,"marks_per_q":4,"negative":1.33},
     {"name":"Current Events","questions":20,"marks_per_q":4,"negative":1.33}],
    "⚔️", "NDA GAT — 150 Qs, 600 Marks, 150 min, -1.33 per wrong")

cfg("CDS_GENERAL_KNOWLEDGE", "CDS General Knowledge", "DEFENCE",
    120, 100, 120, 0.33, 0.83,
    [{"name":"Current Events","questions":30,"marks_per_q":0.83,"negative":0.27},
     {"name":"History","questions":30,"marks_per_q":0.83,"negative":0.27},
     {"name":"Geography","questions":30,"marks_per_q":0.83,"negative":0.27},
     {"name":"Science & Technology","questions":30,"marks_per_q":0.83,"negative":0.27}],
    "🎖️", "CDS General Knowledge — 120 Qs, 100 Marks, 120 min, -0.33 per wrong")

cfg("AFCAT", "AFCAT (Air Force Common Admission Test)", "DEFENCE",
    100, 300, 120, 1.0, 3.0,
    [{"name":"General Awareness","questions":30,"marks_per_q":3,"negative":1.0},
     {"name":"Verbal Ability in English","questions":30,"marks_per_q":3,"negative":1.0},
     {"name":"Numerical Ability","questions":15,"marks_per_q":3,"negative":1.0},
     {"name":"Reasoning & Military Aptitude","questions":25,"marks_per_q":3,"negative":1.0}],
    "✈️", "AFCAT — 100 Qs, 300 Marks, 120 min, -1.00 per wrong")

# ── UPSC EXAMS ────────────────────────────────────────────────────────────────
cfg("UPSC_PRELIMS_GS1", "UPSC CSE Prelims GS Paper-1", "UPSC",
    100, 200, 120, 0.67, 2.0,
    [{"name":"Current Events of National & International Importance","questions":20,"marks_per_q":2,"negative":0.67},
     {"name":"Indian Polity & Governance","questions":20,"marks_per_q":2,"negative":0.67},
     {"name":"Indian History & Art Culture","questions":15,"marks_per_q":2,"negative":0.67},
     {"name":"Indian & World Geography","questions":20,"marks_per_q":2,"negative":0.67},
     {"name":"Economic & Social Development","questions":15,"marks_per_q":2,"negative":0.67},
     {"name":"Environmental Ecology & Science","questions":10,"marks_per_q":2,"negative":0.67}],
    "🏛️", "UPSC CSE Prelims GS-1 — 100 Qs, 200 Marks, 120 min, -0.67 per wrong")

cfg("UPSC_CAPF", "UPSC CAPF AC Paper-1", "UPSC",
    125, 250, 150, 0.83, 2.0,
    [{"name":"General Mental Ability & Reasoning","questions":25,"marks_per_q":2,"negative":0.67},
     {"name":"General Science & Environment","questions":25,"marks_per_q":2,"negative":0.67},
     {"name":"Indian Polity & Economy","questions":25,"marks_per_q":2,"negative":0.67},
     {"name":"History","questions":25,"marks_per_q":2,"negative":0.67},
     {"name":"Geography","questions":25,"marks_per_q":2,"negative":0.67}],
    "🚔", "UPSC CAPF Paper-1 — 125 Qs, 250 Marks, 150 min, -0.67 per wrong")

# ── TEACHING EXAMS ────────────────────────────────────────────────────────────
cfg("CTET_PAPER1", "CTET Paper-1 (Classes 1–5)", "TEACHING",
    150, 150, 150, 0.0, 1.0,
    [{"name":"Child Development & Pedagogy","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Language-1 (Hindi/English)","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Language-2 (Hindi/English)","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Mathematics","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Environmental Studies","questions":30,"marks_per_q":1,"negative":0}],
    "📚", "CTET Paper-1 — 150 Qs, 150 Marks, 150 min, No negative marking")

cfg("CTET_PAPER2", "CTET Paper-2 (Classes 6–8)", "TEACHING",
    150, 150, 150, 0.0, 1.0,
    [{"name":"Child Development & Pedagogy","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Language-1","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Language-2","questions":30,"marks_per_q":1,"negative":0},
     {"name":"Mathematics & Science OR Social Studies","questions":60,"marks_per_q":1,"negative":0}],
    "📚", "CTET Paper-2 — 150 Qs, 150 Marks, 150 min, No negative marking")

cfg("KVS_PGT", "KVS PGT (Post Graduate Teacher)", "TEACHING",
    180, 180, 180, 0.25, 1.0,
    [{"name":"General English","questions":10,"marks_per_q":1,"negative":0.25},
     {"name":"General Hindi","questions":10,"marks_per_q":1,"negative":0.25},
     {"name":"General Knowledge & Current Affairs","questions":40,"marks_per_q":1,"negative":0.25},
     {"name":"Reasoning Ability","questions":40,"marks_per_q":1,"negative":0.25},
     {"name":"Computer Literacy","questions":10,"marks_per_q":1,"negative":0.25},
     {"name":"Pedagogy","questions":20,"marks_per_q":1,"negative":0.25},
     {"name":"Subject Specific","questions":100,"marks_per_q":1,"negative":0.25}],
    "🏫", "KVS PGT — 180 Qs, 180 Marks, 180 min, -0.25 per wrong")

# ── STATE PSC / OTHER ─────────────────────────────────────────────────────────
cfg("APPSC_GROUP1_PRELIMS", "APPSC Group-1 Prelims", "STATE_PSC",
    150, 150, 150, 0.0, 1.0,
    [{"name":"General Studies & Mental Ability","questions":150,"marks_per_q":1,"negative":0}],
    "🏢", "APPSC Group-1 Prelims — 150 Qs, 150 Marks, 150 min, No negative marking")

cfg("TSPSC_GROUP1", "TSPSC Group-1 Prelims", "STATE_PSC",
    150, 150, 150, 0.0, 1.0,
    [{"name":"General Studies","questions":75,"marks_per_q":1,"negative":0},
     {"name":"Mental Ability & Reasoning","questions":75,"marks_per_q":1,"negative":0}],
    "🏢", "TSPSC Group-1 Prelims — 150 Qs, 150 Marks, 150 min, No negative marking")

cfg("MPPSC_PRELIMS", "MPPSC State Service Prelims", "STATE_PSC",
    100, 200, 120, 0.67, 2.0,
    [{"name":"General Studies","questions":100,"marks_per_q":2,"negative":0.67}],
    "🏢", "MPPSC Prelims — 100 Qs, 200 Marks, 120 min, -0.67 per wrong")

cfg("SSC_MTS", "SSC MTS (Multi-Tasking Staff)", "GOVT_NON_IT",
    90, 90, 90, 0.0, 1.0,
    [{"name":"Numerical & Mathematical Ability","questions":20,"marks_per_q":1,"negative":0},
     {"name":"Reasoning Ability & Problem Solving","questions":20,"marks_per_q":1,"negative":0},
     {"name":"General Awareness","questions":25,"marks_per_q":1,"negative":0},
     {"name":"English Language & Comprehension","questions":25,"marks_per_q":1,"negative":0}],
    "📝", "SSC MTS — 90 Qs, 90 Marks, 90 min, No negative marking")

cfg("SSC_GD_CONSTABLE", "SSC GD Constable", "GOVT_NON_IT",
    80, 160, 60, 0.50, 2.0,
    [{"name":"General Intelligence & Reasoning","questions":20,"marks_per_q":2,"negative":0.5},
     {"name":"General Knowledge & General Awareness","questions":20,"marks_per_q":2,"negative":0.5},
     {"name":"Elementary Mathematics","questions":20,"marks_per_q":2,"negative":0.5},
     {"name":"English / Hindi","questions":20,"marks_per_q":2,"negative":0.5}],
    "👮", "SSC GD Constable — 80 Qs, 160 Marks, 60 min, -0.50 per wrong")

cfg("SSC_CPO_TIER1", "SSC CPO (Central Police Organisations) Tier-1", "GOVT_NON_IT",
    200, 200, 120, 0.25, 1.0,
    [{"name":"General Intelligence & Reasoning","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"General Knowledge & General Awareness","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"Quantitative Aptitude","questions":50,"marks_per_q":1,"negative":0.25},
     {"name":"English Comprehension","questions":50,"marks_per_q":1,"negative":0.25}],
    "🚓", "SSC CPO Tier-1 — 200 Qs, 200 Marks, 120 min, -0.25 per wrong")

db.commit()
total = db.query(ExamConfig).count()
print(f"[OK] Seeded {total} exam configs successfully!")
print("\nExam List:")
for e in db.query(ExamConfig).all():
    print(f"  [{e.category}] {e.exam_key}: {e.pattern_summary}")
db.close()
