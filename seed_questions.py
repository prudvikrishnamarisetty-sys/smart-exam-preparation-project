"""
Comprehensive question bank for all 26+ exams.
Run: python seed_questions.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from database import engine, SessionLocal, Base
from models import Question
Base.metadata.create_all(bind=engine)
db = SessionLocal()

def add(text, a, b, c, d, ans, expl, exam, subj, section, topic, diff="medium", year=None, marks=1.0, neg=0.0):
    db.add(Question(text=text, option_a=a, option_b=b, option_c=c, option_d=d,
        correct_option=ans, explanation=expl, exam_type=exam, subject=subj,
        section=section, topic=topic, difficulty=diff, year=year,
        marks_per_question=marks, negative_marks=neg, source="Seed"))

# ── SSC CGL TIER-1 ────────────────────────────────────────────────────────────
S="SSC_CGL_TIER1"
add("If a+b=10 and ab=21, find a²+b².", "58","52","48","62","A","(a+b)²=a²+2ab+b²→100=a²+42+b²→58",S,"Quantitative Aptitude","Quantitative Aptitude","Algebra","medium",2019,2,0.5)
add("A train 150m long passes a pole in 15s. Speed in km/h?","36","40","32","45","A","Speed=150/15=10m/s=36km/h",S,"Quantitative Aptitude","Quantitative Aptitude","Speed & Distance","easy",2018,2,0.5)
add("Average of 5 numbers is 20. One excluded, avg=18. Excluded number?","24","28","26","30","B","Sum=100, rem=72, excluded=28",S,"Quantitative Aptitude","Quantitative Aptitude","Average","medium",2018,2,0.5)
add("Compound interest on Rs.10000 at 10% for 2 years?","Rs.2000","Rs.2100","Rs.2200","Rs.2500","B","CI=10000((1.1)²-1)=2100",S,"Quantitative Aptitude","Quantitative Aptitude","Interest","medium",2018,2,0.5)
add("25% of 400=?","50","75","100","125","C","25/100×400=100",S,"Quantitative Aptitude","Quantitative Aptitude","Percentage","easy",2020,2,0.5)
add("Select correctly spelled word.","Accomodate","Accommodate","Acommodate","Acomodate","B","Accommodate: double c and double m",S,"English Language","English Comprehension","Spelling","easy",2020,2,0.5)
add("Choose synonym of 'Abundant'.","Scarce","Plentiful","Meager","Rare","B","Abundant means plentiful",S,"English Language","English Comprehension","Synonyms","easy",2019,2,0.5)
add("Choose antonym of 'Benevolent'.","Kind","Malevolent","Generous","Helpful","B","Malevolent = wishing harm",S,"English Language","English Comprehension","Antonyms","easy",2020,2,0.5)
add("Correct passive of 'She writes a letter.'","A letter was written by her","A letter is written by her","A letter is being written","A letter has been written","B","Present simple passive: is+past participle",S,"English Language","English Comprehension","Grammar","easy",2020,2,0.5)
add("Find odd one out: 2,5,10,17,24,37","10","17","24","37","C","Pattern:+3,+5,+7,+9,+11 → 26 not 24",S,"General Intelligence & Reasoning","General Intelligence & Reasoning","Number Series","medium",2019,2,0.5)
add("If ROSE=6821, how is FORE coded?","4261","4821","4216","4126","A","R=6,O=8,S=2,E=1→F=4,O=8→FORE=4261",S,"General Intelligence & Reasoning","General Intelligence & Reasoning","Coding-Decoding","medium",2019,2,0.5)
add("Who is 'Father of Economics'?","Karl Marx","Adam Smith","J.M.Keynes","David Ricardo","B","Adam Smith wrote Wealth of Nations 1776",S,"General Awareness","General Awareness","Economics","easy",2020,2,0.5)
add("Parliament of India has how many houses?","1","2","3","4","B","Lok Sabha and Rajya Sabha",S,"General Awareness","General Awareness","Polity","easy",2018,2,0.5)
add("Which vitamin is produced by sunlight?","Vitamin A","Vitamin B","Vitamin C","Vitamin D","D","UV rays trigger Vitamin D synthesis",S,"General Awareness","General Awareness","Science","easy",2019,2,0.5)
add("Who invented the telephone?","Thomas Edison","Alexander Graham Bell","Nikola Tesla","Marconi","B","Bell patented telephone in 1876",S,"General Awareness","General Awareness","Inventions","easy",2019,2,0.5)

# ── SSC CHSL TIER-1 ───────────────────────────────────────────────────────────
S="SSC_CHSL_TIER1"
add("LCM of 12,15,20?","30","60","120","180","B","LCM=2²×3×5=60",S,"Quantitative Aptitude","Quantitative Aptitude","LCM & HCF","easy",2019,2,0.5)
add("Fill blank: She has been working here ___ 2015.","from","since","for","by","B","'since' with specific point in time",S,"English Language","English Comprehension","Grammar","easy",2018,2,0.5)
add("A does work in 10 days, B in 15 days. Together?","5 days","6 days","7 days","8 days","B","Rate=1/10+1/15=1/6 → 6 days",S,"Quantitative Aptitude","Quantitative Aptitude","Time & Work","medium",2019,2,0.5)
add("Find missing: 3,9,27,81,?","162","243","324","189","B","Geometric ×3: 81×3=243",S,"General Intelligence","General Intelligence","Number Series","easy",2018,2,0.5)
add("HCF of 12 and 18?","4","6","8","12","B","12=2²×3, 18=2×3². HCF=6",S,"Quantitative Aptitude","Quantitative Aptitude","LCM & HCF","easy",2020,2,0.5)
add("Which Indian state has maximum coastline?","Kerala","Tamil Nadu","Gujarat","Maharashtra","C","Gujarat has ~1600km coastline",S,"General Awareness","General Awareness","Geography","medium",2020,2,0.5)

# ── GATE CSE ──────────────────────────────────────────────────────────────────
S="GATE_CSE"
add("Time complexity of binary search?","O(n)","O(log n)","O(n log n)","O(1)","B","Halves search space each step",S,"Data Structures","Core CS — 1 mark Qs","Searching","easy",2019,1,0.33)
add("Which data structure uses LIFO?","Queue","Stack","Array","Linked List","B","Stack: Last In First Out",S,"Data Structures","Core CS — 1 mark Qs","Stack","easy",2018,1,0.33)
add("Number of edges in complete graph with n vertices?","n(n-1)","n(n-1)/2","n²","2n","B","Each vertex connects to n-1 others, /2",S,"Discrete Math","Core CS — 2 mark Qs","Graph Theory","medium",2018,2,0.67)
add("Which normal form removes transitive dependency?","1NF","2NF","3NF","BCNF","C","3NF eliminates transitive dependencies",S,"DBMS","Core CS — 1 mark Qs","Normalization","medium",2019,1,0.33)
add("Worst-case time of QuickSort?","O(n log n)","O(n²)","O(n)","O(log n)","B","Worst case O(n²) with bad pivot",S,"Algorithms","Core CS — 1 mark Qs","Sorting","easy",2020,1,0.33)
add("Which scheduling has minimum average waiting time?","FCFS","SJF","Round Robin","Priority","B","Shortest Job First minimizes avg wait",S,"Operating Systems","Core CS — 2 mark Qs","Scheduling","medium",2019,2,0.67)
add("TCP three-way handshake uses which flags?","SYN,ACK,FIN","SYN,SYN-ACK,ACK","SYN,FIN,RST","ACK,FIN,RST","B","SYN→SYN-ACK→ACK establishes TCP",S,"Computer Networks","Core CS — 1 mark Qs","TCP","medium",2018,1,0.33)
add("DFS uses which data structure?","Queue","Stack","Heap","Hash Table","B","DFS uses stack (or recursion)",S,"Algorithms","Core CS — 1 mark Qs","Graph Traversal","easy",2019,1,0.33)
add("Which join returns all rows from both tables?","Inner Join","Left Join","Right Join","Full Outer Join","D","Full outer join returns all rows from both",S,"DBMS","Core CS — 2 mark Qs","SQL Joins","medium",2020,2,0.67)
add("Page fault occurs when?","Page is in memory","Page is not in memory","CPU is idle","Disk is full","B","Page fault when page not in RAM",S,"Operating Systems","Core CS — 1 mark Qs","Virtual Memory","easy",2018,1,0.33)
add("Which memory management has external fragmentation?","Paging","Segmentation","Virtual Memory","Caching","B","Segmentation causes external fragmentation",S,"Operating Systems","Core CS — 2 mark Qs","Memory","medium",2019,2,0.67)
add("If log₁₀2=0.301, find log₁₀8.","0.603","0.903","2.408","0.801","B","log8=log2³=3×0.301=0.903",S,"Mathematics","Core CS — 1 mark Qs","Logarithms","easy",2019,1,0.33)
add("Which protocol is at transport layer?","HTTP","IP","TCP","ARP","C","TCP at transport layer (Layer 4)",S,"Computer Networks","Core CS — 1 mark Qs","OSI Model","easy",2020,1,0.33)

# ── JAVA OCJP ─────────────────────────────────────────────────────────────────
S="JAVA_OCJP"
add("What is output of: System.out.println(10/3);","3.33","3","4","Error","B","Integer division: 10/3=3 in Java",S,"Java Basics & OOP","Java Basics & OOP","Data Types","easy",2022,1,0)
add("Which keyword is used to inherit a class in Java?","implements","extends","inherits","super","B","'extends' used for class inheritance",S,"Java Basics & OOP","Java Basics & OOP","OOP Concepts","easy",2022,1,0)
add("Which of these is NOT a Java primitive type?","int","String","boolean","char","B","String is a class, not a primitive",S,"Java Basics & OOP","Java Basics & OOP","Data Types","easy",2021,1,0)
add("What does the 'final' keyword do to a variable?","Makes it static","Makes it constant","Makes it global","Makes it private","B","final variable cannot be reassigned",S,"Java Basics & OOP","Java Basics & OOP","Keywords","easy",2022,1,0)
add("Which interface must be implemented for sorting with Collections.sort()?","Serializable","Comparable","Cloneable","Iterable","B","Comparable interface with compareTo()",S,"Collections & Generics","Collections & Generics","Collections API","medium",2021,1,0)
add("What is autoboxing in Java?","Manual type casting","Auto conversion int↔Integer","Method overloading","Array resizing","B","Auto wrapping primitives to wrapper classes",S,"Java Basics & OOP","Java Basics & OOP","Autoboxing","medium",2022,1,0)
add("Which exception is thrown for array out of bounds?","NullPointerException","ArrayIndexOutOfBoundsException","ClassCastException","StackOverflowError","B","ArrayIndexOutOfBoundsException for invalid index",S,"Exception Handling & I/O","Exception Handling & I/O","Exceptions","easy",2021,1,0)
add("What is the default value of int in Java?","null","1","0","-1","C","Default value of int is 0",S,"Java Basics & OOP","Java Basics & OOP","Data Types","easy",2020,1,0)

# ── PYTHON PCEP ───────────────────────────────────────────────────────────────
S="PYTHON_PCEP"
add("What is output of: print(type(5/2))?","int","float","str","complex","B","5/2=2.5, type is float in Python 3",S,"Basics & Control Flow","Basics & Control Flow","Data Types","easy",2022,1,0)
add("Which keyword defines a function in Python?","func","def","function","define","B","'def' keyword defines a function",S,"Functions & Modules","Functions & Modules","Functions","easy",2022,1,0)
add("What does len([1,2,3]) return?","2","3","4","Error","B","len() returns number of elements: 3",S,"Data Structures","Data Structures","Lists","easy",2021,1,0)
add("Output of: print(2**3)?","6","8","9","5","B","** is power operator: 2³=8",S,"Basics & Control Flow","Basics & Control Flow","Operators","easy",2022,1,0)
add("Which is mutable in Python?","tuple","string","list","int","C","Lists are mutable; tuples/strings are not",S,"Data Structures","Data Structures","Data Types","easy",2021,1,0)
add("What is output of: print('Python'[0:3])?","Pyt","Pyt","yt","Py","A","Slicing [0:3] gives first 3 chars: 'Pyt'",S,"Basics & Control Flow","Basics & Control Flow","Strings","easy",2020,1,0)

# ── DSA ───────────────────────────────────────────────────────────────────────
S="DSA_PRACTICE"
add("Which sorting algorithm is best for nearly sorted arrays?","QuickSort","MergeSort","Insertion Sort","Bubble Sort","C","Insertion sort O(n) for nearly sorted",S,"Sorting, Searching & DP","Sorting, Searching & DP","Sorting","medium",2022,1,0)
add("What is time complexity of accessing element in array by index?","O(n)","O(log n)","O(1)","O(n²)","C","Direct index access is O(1)",S,"Arrays & Strings","Arrays & Strings","Arrays","easy",2022,1,0)
add("Which data structure is used in BFS?","Stack","Queue","Heap","Tree","B","BFS uses Queue (FIFO)",S,"Trees & Graphs","Trees & Graphs","Graph Traversal","easy",2021,1,0)
add("Maximum number of nodes at level k in binary tree?","k","2^k","2^(k-1)","k²","B","Level k has max 2^k nodes",S,"Trees & Graphs","Trees & Graphs","Trees","medium",2022,1,0)
add("What is the best case time complexity of QuickSort?","O(n²)","O(n log n)","O(n)","O(log n)","B","Best case with balanced partitions: O(n log n)",S,"Sorting, Searching & DP","Sorting, Searching & DP","Sorting","medium",2021,1,0)
add("Which data structure is suitable for implementing recursion?","Queue","Array","Stack","Linked List","C","Function call stack uses Stack",S,"Linked List, Stack, Queue","Linked List, Stack, Queue","Stack","easy",2020,1,0)
add("Time complexity of searching in a balanced BST?","O(1)","O(n)","O(log n)","O(n log n)","C","BST search: O(log n) when balanced",S,"Trees & Graphs","Trees & Graphs","Trees","medium",2022,1,0)

# ── AWS SAA-C03 ───────────────────────────────────────────────────────────────
S="AWS_SAA_C03"
add("Which AWS service provides scalable object storage?","EBS","EFS","S3","Glacier","C","S3 = Simple Storage Service for object storage",S,"Storage","Resilient Architectures","Storage","easy",2023,1,0)
add("Which service provides managed relational database?","DynamoDB","ElastiCache","RDS","Redshift","C","RDS = Relational Database Service",S,"Databases","Resilient Architectures","Databases","easy",2023,1,0)
add("Which AWS service is used for CDN?","Route 53","CloudFront","API Gateway","ALB","B","CloudFront is AWS CDN service",S,"Networking","High-Performance Architectures","CDN","easy",2022,1,0)
add("What is the maximum size of a single S3 object?","5GB","5TB","1TB","100GB","B","S3 single object max size is 5TB",S,"Storage","Resilient Architectures","S3","medium",2022,1,0)
add("Which EC2 pricing model is cheapest for steady, predictable workloads?","On-Demand","Spot","Reserved","Dedicated","C","Reserved instances give up to 75% savings",S,"Compute","Cloud Concepts","EC2","medium",2023,1,0)
add("IAM stands for?","Internet Access Management","Identity and Access Management","Internal Access Manager","Integrated Auth Module","B","IAM = Identity and Access Management",S,"Security","Security & Identity","IAM","easy",2022,1,0)

# ── TCS NQT IT ────────────────────────────────────────────────────────────────
S="TCS_NQT_IT"
add("A man walks 5km East then 3km North. Distance from start?","√34 km","8 km","4 km","√28 km","A","√(5²+3²)=√34 km",S,"Numerical Ability","Numerical Ability","Distance","medium",2022,1,0)
add("If 6 workers build a wall in 15 days, how long for 10?","7 days","8 days","9 days","10 days","C","6×15=10×x → x=9 days",S,"Numerical Ability","Numerical Ability","Time & Work","easy",2022,1,0)
add("Which is NOT a valid identifier in most languages?","_variable","2variable","variable2","my_var","B","Identifiers cannot start with digits",S,"Programming Logic","Programming Logic","Basics","easy",2021,1,0)
add("Output of: for i in range(3): print(i) in Python?","0 1 2","1 2 3","0 1 2 3","1 2","A","range(3) gives 0,1,2",S,"Programming Logic","Programming Logic","Loops","easy",2022,1,0)
add("She completed the project ___ time.","at","in","on","by","B","'in time' = before deadline",S,"Verbal Ability","Verbal Ability","Grammar","easy",2021,1,0)
add("Which is the correct logical expression for 'a OR NOT b'?","a && !b","a || !b","!a || b","a && b","B","OR=||, NOT=! so 'a OR NOT b' = a||!b",S,"Reasoning Ability","Reasoning Ability","Boolean Logic","medium",2022,1,0)

# ── NIC SCIENTIFIC OFFICER ────────────────────────────────────────────────────
S="NIC_SCI_OFFICER"
add("Which sorting algorithm is stable?","QuickSort","Heap Sort","Merge Sort","Selection Sort","C","Merge sort is stable: equal elements maintain order",S,"IT & Computer Science","IT & Computer Science","Sorting","medium",2021,1,0.25)
add("Which layer of OSI model handles routing?","Data Link","Network","Transport","Session","B","Network layer (Layer 3) handles routing",S,"IT & Computer Science","IT & Computer Science","Networking","easy",2020,1,0.25)
add("Which is NOT a NoSQL database?","MongoDB","Cassandra","Oracle","CouchDB","C","Oracle is a relational (SQL) database",S,"IT & Computer Science","IT & Computer Science","Databases","easy",2021,1,0.25)
add("RAID 1 provides?","Striping","Mirroring","Striping+Parity","Striping+Mirroring","B","RAID 1 = disk mirroring for redundancy",S,"IT & Computer Science","IT & Computer Science","Storage","medium",2020,1,0.25)

# ── RRB JE IT ─────────────────────────────────────────────────────────────────
S="RRB_JE_IT"
add("Which IP address range is private?","10.0.0.0/8","8.8.8.8","172.32.0.0","200.0.0.0","A","10.0.0.0/8 is private (RFC1918)",S,"IT & Computer Science","IT & Computer Science","Networking","medium",2021,1,0.33)
add("Which is fastest memory in memory hierarchy?","RAM","Cache","Register","HDD","C","Registers are fastest, closest to CPU",S,"IT & Computer Science","IT & Computer Science","Computer Organisation","easy",2020,1,0.33)
add("What does HTTP stand for?","HyperText Transfer Protocol","High Transfer Text Protocol","HyperText Transmission Protocol","High Text Transfer Protocol","A","HTTP=HyperText Transfer Protocol",S,"IT & Computer Science","IT & Computer Science","Networking","easy",2021,1,0.33)
add("Which number system uses base 16?","Binary","Octal","Decimal","Hexadecimal","D","Hexadecimal uses digits 0-9 and A-F",S,"Mathematics","Mathematics","Number Systems","easy",2020,1,0.33)

# ── ISRO CS ───────────────────────────────────────────────────────────────────
S="ISRO_CS"
add("Which algorithm is used in Dijkstra's shortest path?","DFS","Greedy","Dynamic Programming","Backtracking","B","Dijkstra uses greedy approach",S,"Computer Science & Engineering","Computer Science & Engineering","Algorithms","hard",2020,3,1.0)
add("The number of 1's in binary representation of 255?","4","6","8","7","C","255=11111111 in binary, eight 1's",S,"Computer Science & Engineering","Computer Science & Engineering","Number Systems","medium",2021,3,1.0)
add("Which protocol is used for email retrieval?","SMTP","FTP","POP3","HTTP","C","POP3 = Post Office Protocol for email retrieval",S,"Computer Science & Engineering","Computer Science & Engineering","Networking","medium",2020,3,1.0)
add("Context switching is done by?","Compiler","Loader","OS Scheduler","Hardware alone","C","OS scheduler performs context switching",S,"Computer Science & Engineering","Computer Science & Engineering","Operating Systems","medium",2021,3,1.0)

# ── DRDO CEPTAM ───────────────────────────────────────────────────────────────
S="DRDO_CEPTAM"
add("What is the full form of ALU?","Arithmetic Logic Unit","Array Logic Unit","Arithmetic Linear Unit","Automated Logic Unit","A","ALU performs arithmetic and logical operations",S,"IT & Computer Science","IT & Computer Science","Computer Architecture","easy",2021,1,0.5)
add("Which generation of computer used transistors?","First","Second","Third","Fourth","B","Second generation (1956-1963) used transistors",S,"IT & Computer Science","IT & Computer Science","Computer History","easy",2020,1,0.5)
add("What does RAM stand for?","Read Access Memory","Random Access Memory","Read All Memory","Rapid Access Memory","B","RAM=Random Access Memory, volatile",S,"IT & Computer Science","IT & Computer Science","Computer Basics","easy",2021,1,0.5)
add("Boiling point of water is?","90°C","95°C","100°C","110°C","C","Water boils at 100°C at standard pressure",S,"General Awareness","General Awareness","Science","easy",2020,1,0.5)

# ── COGNIZANT GENC ────────────────────────────────────────────────────────────
S="COGNIZANT_GENC"
add("All roses are flowers. Some flowers are red. Conclusion?","All roses are red","Some roses are red","No conclusion about roses being red","All flowers are roses","C","No direct conclusion from given premises",S,"Reasoning Ability","Reasoning Ability","Syllogism","medium",2022,1,0)
add("A and B invest 3:4. Profit Rs.8400. B's share?","Rs.3600","Rs.4800","Rs.4200","Rs.5400","B","B's share=4/7×8400=Rs.4800",S,"Quantitative Aptitude","Quantitative Aptitude","Partnership","easy",2021,1,0)
add("Find next: 2,6,12,20,30,?","40","42","44","48","B","Differences 4,6,8,10,12 → 30+12=42",S,"Reasoning Ability","Reasoning Ability","Number Series","medium",2022,1,0)

db.commit()
count = db.query(Question).count()
print(f"[OK] Seeded {count} questions across all exam categories!")
db.close()
