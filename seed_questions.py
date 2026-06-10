"""
Seed question bank — provides fallback/sample questions.
AI generates questions dynamically; these serve as a baseline.
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
add("Find odd one out: 2,5,10,17,24,37","10","17","24","37","C","Pattern:+3,+5,+7,+9,+11 → 26 not 24",S,"General Intelligence & Reasoning","General Intelligence & Reasoning","Number Series","medium",2019,2,0.5)
add("Who is 'Father of Economics'?","Karl Marx","Adam Smith","J.M.Keynes","David Ricardo","B","Adam Smith wrote Wealth of Nations 1776",S,"General Awareness","General Awareness","Economics","easy",2020,2,0.5)
add("Parliament of India has how many houses?","1","2","3","4","B","Lok Sabha and Rajya Sabha",S,"General Awareness","General Awareness","Polity","easy",2018,2,0.5)

# ── SSC CHSL TIER-1 ───────────────────────────────────────────────────────────
S="SSC_CHSL_TIER1"
add("LCM of 12,15,20?","30","60","120","180","B","LCM=2²×3×5=60",S,"Quantitative Aptitude","Quantitative Aptitude","LCM & HCF","easy",2019,2,0.5)
add("Fill blank: She has been working here ___ 2015.","from","since","for","by","B","'since' with specific point in time",S,"English Language","English Comprehension","Grammar","easy",2018,2,0.5)
add("A does work in 10 days, B in 15 days. Together?","5 days","6 days","7 days","8 days","B","Rate=1/10+1/15=1/6 → 6 days",S,"Quantitative Aptitude","Quantitative Aptitude","Time & Work","medium",2019,2,0.5)
add("Find missing: 3,9,27,81,?","162","243","324","189","B","Geometric ×3: 81×3=243",S,"General Intelligence","General Intelligence","Number Series","easy",2018,2,0.5)
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

# ── JAVA OCJP ─────────────────────────────────────────────────────────────────
S="JAVA_OCJP"
add("What is output of: System.out.println(10/3);","3.33","3","4","Error","B","Integer division: 10/3=3 in Java",S,"Java Basics & OOP","Java Basics & OOP","Data Types","easy",2022,1,0)
add("Which keyword is used to inherit a class in Java?","implements","extends","inherits","super","B","'extends' used for class inheritance",S,"Java Basics & OOP","Java Basics & OOP","OOP Concepts","easy",2022,1,0)
add("Which of these is NOT a Java primitive type?","int","String","boolean","char","B","String is a class, not a primitive",S,"Java Basics & OOP","Java Basics & OOP","Data Types","easy",2021,1,0)
add("What does the 'final' keyword do to a variable?","Makes it static","Makes it constant","Makes it global","Makes it private","B","final variable cannot be reassigned",S,"Java Basics & OOP","Java Basics & OOP","Keywords","easy",2022,1,0)
add("Which interface must be implemented for sorting with Collections.sort()?","Serializable","Comparable","Cloneable","Iterable","B","Comparable interface with compareTo()",S,"Collections & Generics","Collections & Generics","Collections API","medium",2021,1,0)
add("Which exception is thrown for array out of bounds?","NullPointerException","ArrayIndexOutOfBoundsException","ClassCastException","StackOverflowError","B","ArrayIndexOutOfBoundsException for invalid index",S,"Exception Handling & I/O","Exception Handling & I/O","Exceptions","easy",2021,1,0)
add("What is the default value of int in Java?","null","1","0","-1","C","Default value of int is 0",S,"Java Basics & OOP","Java Basics & OOP","Data Types","easy",2020,1,0)

# ── JAVA BASICS ───────────────────────────────────────────────────────────────
S="JAVA_BASICS"
add("Which method is the entry point of a Java program?","start()","main()","run()","init()","B","public static void main(String[] args) is entry point",S,"Syntax & Data Types","Syntax & Data Types","Methods","easy",2022,1,0)
add("What is the size of int in Java?","2 bytes","4 bytes","8 bytes","Depends on platform","B","int is always 4 bytes (32-bit) in Java",S,"Syntax & Data Types","Syntax & Data Types","Data Types","easy",2021,1,0)
add("Which keyword prevents a method from being overridden?","static","private","final","abstract","C","final method cannot be overridden",S,"OOP Concepts","OOP Concepts","Inheritance","medium",2022,1,0)
add("What is the output of: System.out.println(\"Hello\" + 1 + 2);","Hello12","Hello3","3Hello","Error","A","String concatenation happens left to right: Hello12",S,"Syntax & Data Types","Syntax & Data Types","Operators","medium",2021,1,0)

# ── JAVA OOP ADVANCED ─────────────────────────────────────────────────────────
S="JAVA_OOP_ADVANCED"
add("Which concept allows one class to have multiple forms?","Encapsulation","Polymorphism","Inheritance","Abstraction","B","Polymorphism means many forms",S,"Abstract Classes & Polymorphism","Abstract Classes & Polymorphism","Polymorphism","easy",2022,1,0)
add("An interface in Java can have?","Only abstract methods","Abstract and default methods","Only concrete methods","Static methods only","B","Since Java 8, interfaces can have default methods",S,"Inheritance & Interfaces","Inheritance & Interfaces","Interfaces","medium",2022,1,0)
add("Which keyword is used to call a parent class constructor?","this()","super()","parent()","base()","B","super() calls the parent class constructor",S,"Inheritance & Interfaces","Inheritance & Interfaces","Inheritance","easy",2021,1,0)

# ── JAVA COLLECTIONS ─────────────────────────────────────────────────────────
S="JAVA_COLLECTIONS"
add("Which Java collection does NOT allow duplicates?","ArrayList","LinkedList","HashSet","Vector","C","HashSet stores only unique elements",S,"List, Set & Map","List, Set & Map","Set","easy",2022,1,0)
add("What does HashMap.get(key) return if key not found?","0","''","null","Exception","C","Returns null if key is not present",S,"List, Set & Map","List, Set & Map","Map","easy",2021,1,0)
add("Which stream method is used to filter elements?","map()","filter()","reduce()","collect()","B","filter() selects elements matching a predicate",S,"Java 8 Streams & Lambda","Java 8 Streams & Lambda","Streams","easy",2022,1,0)
add("What is the difference between ArrayList and LinkedList?","No difference","ArrayList uses array; LinkedList uses doubly linked list","LinkedList is faster for get()","ArrayList uses linked list","B","ArrayList backed by array, LinkedList by doubly linked list",S,"List, Set & Map","List, Set & Map","List","medium",2021,1,0)

# ── JAVA SPRING BOOT ─────────────────────────────────────────────────────────
S="JAVA_SPRING_BOOT"
add("Which annotation marks a class as a Spring REST controller?","@Component","@Service","@RestController","@Repository","C","@RestController combines @Controller and @ResponseBody",S,"REST APIs & Controllers","REST APIs & Controllers","Annotations","easy",2023,1,0)
add("What does @Autowired do in Spring?","Creates a new object","Injects a dependency automatically","Marks a class as singleton","Enables transactions","B","@Autowired performs dependency injection",S,"Spring Core & IoC","Spring Core & IoC","DI","easy",2023,1,0)
add("Which Spring Boot annotation enables auto-configuration?","@EnableAutoConfiguration","@SpringBootApplication","@Configuration","@ComponentScan","B","@SpringBootApplication includes auto-configuration",S,"Spring Boot Basics","Spring Boot Basics","Configuration","medium",2022,1,0)

# ── PYTHON PCEP ───────────────────────────────────────────────────────────────
S="PYTHON_PCEP"
add("What is output of: print(type(5/2))?","int","float","str","complex","B","5/2=2.5, type is float in Python 3",S,"Basics & Control Flow","Basics & Control Flow","Data Types","easy",2022,1,0)
add("Which keyword defines a function in Python?","func","def","function","define","B","'def' keyword defines a function",S,"Functions & Modules","Functions & Modules","Functions","easy",2022,1,0)
add("What does len([1,2,3]) return?","2","3","4","Error","B","len() returns number of elements: 3",S,"Data Structures","Data Structures","Lists","easy",2021,1,0)
add("Output of: print(2**3)?","6","8","9","5","B","** is power operator: 2³=8",S,"Basics & Control Flow","Basics & Control Flow","Operators","easy",2022,1,0)
add("Which is mutable in Python?","tuple","string","list","int","C","Lists are mutable; tuples/strings are not",S,"Data Structures","Data Structures","Data Types","easy",2021,1,0)

# ── PYTHON PCAP ───────────────────────────────────────────────────────────────
S="PYTHON_PCAP"
add("What is a Python decorator?","A design pattern","A function that wraps another function","A type of class","A built-in module","B","Decorators wrap functions to modify their behavior",S,"OOP in Python","OOP in Python","Decorators","medium",2022,1,0)
add("Which method is called when an object is created?","__new__","__init__","__create__","__start__","B","__init__ is the constructor/initializer",S,"OOP in Python","OOP in Python","Classes","easy",2021,1,0)
add("What does 'with open()' ensure in Python?","Faster file reading","Automatic file closing","No exceptions","Binary mode only","B","Context manager ensures file is closed automatically",S,"Exceptions & File I/O","Exceptions & File I/O","File I/O","easy",2022,1,0)
add("How do you catch a specific exception in Python?","try/finally","try/except ExceptionType","try/catch","raise/handle","B","except ExceptionType catches specific exceptions",S,"Exceptions & File I/O","Exceptions & File I/O","Exceptions","easy",2021,1,0)

# ── PYTHON BASICS ─────────────────────────────────────────────────────────────
S="PYTHON_BASICS"
add("What is the output of: print('Hello'[::-1])?","olleH","Hello","Helo","Error","A","[::-1] reverses the string",S,"Syntax & Data Types","Syntax & Data Types","Strings","easy",2022,1,0)
add("Which data type is immutable in Python?","list","dict","tuple","set","C","Tuples cannot be modified after creation",S,"Lists, Tuples & Dicts","Lists, Tuples & Dicts","Data Types","easy",2021,1,0)
add("What is a lambda function?","A class method","An anonymous function","A module","A built-in","B","lambda creates an anonymous function inline",S,"Functions & Lambda","Functions & Lambda","Lambda","easy",2022,1,0)
add("Output of: print(bool(0))?","True","False","0","None","B","0 is falsy in Python",S,"Syntax & Data Types","Syntax & Data Types","Boolean","easy",2021,1,0)
add("How do you add an element to the end of a list?","list.add()","list.append()","list.insert()","list.push()","B","append() adds to the end of a list",S,"Lists, Tuples & Dicts","Lists, Tuples & Dicts","Lists","easy",2022,1,0)

# ── PYTHON OOP ────────────────────────────────────────────────────────────────
S="PYTHON_OOP"
add("What is inheritance in Python OOP?","Sharing data between modules","A class deriving properties from another","Object creation","Function overloading","B","Inheritance lets a class reuse parent class code",S,"Inheritance & Polymorphism","Inheritance & Polymorphism","Inheritance","easy",2022,1,0)
add("Which Python keyword is used for multiple inheritance?","extends","implements","class MyClass(A, B):","inherit","C","Python supports multiple inheritance via class definition",S,"Inheritance & Polymorphism","Inheritance & Polymorphism","Multiple Inheritance","medium",2021,1,0)
add("What is a generator in Python?","A random number tool","A function that yields values lazily","A type of list","A class decorator","B","Generators use yield and return values lazily",S,"Decorators & Generators","Decorators & Generators","Generators","medium",2022,1,0)
add("What does __str__ method do in Python?","Returns object type","Returns string representation of object","Converts to bytes","Compares objects","B","__str__ is called by str() and print()",S,"Classes & Objects","Classes & Objects","Magic Methods","easy",2021,1,0)

# ── PYTHON DATA SCIENCE ───────────────────────────────────────────────────────
S="PYTHON_DATA_SCIENCE"
add("Which NumPy function creates an array of zeros?","np.zeros()","np.empty()","np.null()","np.blank()","A","np.zeros(shape) creates array filled with zeros",S,"NumPy & Arrays","NumPy & Arrays","NumPy","easy",2023,1,0)
add("Which pandas method displays the first 5 rows?","df.first()","df.top()","df.head()","df.show()","C","df.head() returns first 5 rows by default",S,"Pandas & DataFrames","Pandas & DataFrames","Pandas","easy",2023,1,0)
add("Which library is used for data visualization in Python?","NumPy","Pandas","Matplotlib","Scikit-learn","C","Matplotlib is the primary plotting library",S,"Matplotlib & Visualization","Matplotlib & Visualization","Visualization","easy",2022,1,0)
add("Which algorithm is used for classification in ML?","K-Means","Linear Regression","Decision Tree","PCA","C","Decision Tree is a classification algorithm",S,"Statistics & ML Basics","Statistics & ML Basics","Machine Learning","medium",2023,1,0)

# ── C BASICS ─────────────────────────────────────────────────────────────────
S="C_BASICS"
add("What is a pointer in C?","A variable that stores an address","A variable that stores a value","A function type","A data structure","A","Pointers store memory addresses of variables",S,"Pointers & Memory","Pointers & Memory","Pointers","easy",2022,1,0)
add("What does malloc() do in C?","Frees memory","Allocates memory dynamically","Declares a variable","Initializes memory to zero","B","malloc allocates a specified number of bytes dynamically",S,"Pointers & Memory","Pointers & Memory","Memory Allocation","easy",2021,1,0)
add("What is the size of char in C?","1 byte","2 bytes","4 bytes","8 bytes","A","char is 1 byte in C",S,"Syntax & Data Types","Syntax & Data Types","Data Types","easy",2022,1,0)
add("Which header file is needed for printf in C?","stdlib.h","string.h","stdio.h","math.h","C","stdio.h contains printf declaration",S,"Syntax & Data Types","Syntax & Data Types","Header Files","easy",2021,1,0)
add("What is the output of: printf('%d', sizeof(int));","2","4","8","Depends on system","D","sizeof(int) is platform-dependent (usually 4)",S,"Syntax & Data Types","Syntax & Data Types","Operators","medium",2022,1,0)

# ── C++ BASICS ────────────────────────────────────────────────────────────────
S="CPP_BASICS"
add("What is a class in C++?","A function","A user-defined data type with data & functions","A header file","A pointer type","B","Class is a blueprint combining data and methods",S,"OOP in C++","OOP in C++","Classes","easy",2022,1,0)
add("Which operator is used to access members via pointer?",".","::","->"," *","C","-> dereferences pointer and accesses member",S,"OOP in C++","OOP in C++","Pointers","easy",2021,1,0)
add("What is a constructor in C++?","A destructor","A function with return type","A special method called on object creation","A static method","C","Constructor initializes an object, same name as class",S,"OOP in C++","OOP in C++","Constructor","easy",2022,1,0)
add("What does 'virtual' keyword do in C++?","Makes function static","Enables runtime polymorphism","Makes class abstract","Prevents inheritance","B","virtual enables dynamic dispatch (runtime polymorphism)",S,"OOP in C++","OOP in C++","Polymorphism","medium",2021,1,0)
add("Which C++ STL container provides O(1) access by index?","list","deque","vector","set","C","vector provides O(1) random access",S,"Templates & STL","Templates & STL","STL Containers","easy",2022,1,0)

# ── C++ STL ───────────────────────────────────────────────────────────────────
S="CPP_STL"
add("Which STL container stores key-value pairs sorted by key?","unordered_map","vector","map","set","C","map keeps elements sorted by key",S,"Maps & Sets","Maps & Sets","Map","easy",2022,1,0)
add("What is the time complexity of std::sort?","O(n)","O(n log n)","O(n²)","O(log n)","B","std::sort uses introsort: O(n log n) average",S,"Algorithms & Iterators","Algorithms & Iterators","Sorting","easy",2021,1,0)
add("Which smart pointer has unique ownership?","shared_ptr","weak_ptr","unique_ptr","auto_ptr","C","unique_ptr cannot be copied, only moved",S,"Smart Pointers & Move Semantics","Smart Pointers & Move Semantics","Smart Pointers","medium",2022,1,0)
add("What does begin() return for a vector?","Last element","Pointer to first element","Size","End iterator","B","begin() returns iterator to first element",S,"Algorithms & Iterators","Algorithms & Iterators","Iterators","easy",2021,1,0)

# ── JS BASICS ─────────────────────────────────────────────────────────────────
S="JS_BASICS"
add("What is the output of: typeof null?","null","object","undefined","string","B","typeof null returns 'object' (historical JS quirk)",S,"Syntax & Data Types","Syntax & Data Types","Data Types","medium",2022,1,0)
add("Which keyword declares a block-scoped variable?","var","let","const","function","B","let is block-scoped unlike var",S,"Syntax & Data Types","Syntax & Data Types","Variables","easy",2021,1,0)
add("What does === check in JavaScript?","Value only","Type only","Value and type","Reference","C","=== is strict equality: checks value AND type",S,"Syntax & Data Types","Syntax & Data Types","Operators","easy",2022,1,0)
add("Which method adds an element to the end of an array?","push()","pop()","shift()","unshift()","A","push() appends to end of array",S,"Syntax & Data Types","Syntax & Data Types","Arrays","easy",2021,1,0)
add("What is a closure in JavaScript?","A loop","A function that remembers its outer scope","A class method","An async function","B","Closure: inner function accessing outer function's variables",S,"Functions & Closures","Functions & Closures","Closures","medium",2022,1,0)
add("Which event fires when a button is clicked?","onload","onchange","onclick","onkeyup","C","onclick fires when an element is clicked",S,"DOM & Events","DOM & Events","Events","easy",2021,1,0)

# ── JS ADVANCED ───────────────────────────────────────────────────────────────
S="JS_ADVANCED"
add("What does async/await do?","Runs code synchronously","Makes asynchronous code look synchronous","Creates new threads","Cancels promises","B","async/await simplifies working with promises",S,"Promises & Async/Await","Promises & Async/Await","Async","easy",2022,1,0)
add("What is a Promise in JavaScript?","A synchronous function","An object representing future value","A type of array","A class","B","Promise represents an async operation's eventual result",S,"Promises & Async/Await","Promises & Async/Await","Promises","easy",2021,1,0)
add("What is the prototype chain?","A CSS concept","How JS looks up properties on objects via prototypes","An array method","A module system","B","JS walks up the prototype chain for property lookup",S,"Prototype & Inheritance","Prototype & Inheritance","Prototype","medium",2022,1,0)

# ── REACT JS ─────────────────────────────────────────────────────────────────
S="REACT_JS"
add("What is JSX in React?","A JavaScript library","A syntax extension for writing HTML-like code in JS","A styling framework","A build tool","B","JSX is syntactic sugar for React.createElement()",S,"React Basics & JSX","React Basics & JSX","JSX","easy",2023,1,0)
add("Which hook is used for state in React functional components?","useEffect","useState","useRef","useContext","B","useState manages state in functional components",S,"Hooks & State Management","Hooks & State Management","Hooks","easy",2023,1,0)
add("What does useEffect hook do?","Manages state","Handles side effects like API calls","Creates context","Manages refs","B","useEffect runs side effects after render",S,"Hooks & State Management","Hooks & State Management","Hooks","easy",2022,1,0)
add("What are props in React?","State variables","Read-only data passed from parent to child","Internal component state","CSS styles","B","Props are immutable data passed to components",S,"Components & Props","Components & Props","Props","easy",2023,1,0)

# ── SQL BASICS ────────────────────────────────────────────────────────────────
S="SQL_BASICS"
add("Which SQL clause filters rows after grouping?","WHERE","HAVING","GROUP BY","ORDER BY","B","HAVING filters grouped results, WHERE filters rows before grouping",S,"Aggregations & Grouping","Aggregations & Grouping","Aggregations","easy",2022,1,0)
add("What does SELECT DISTINCT do?","Selects all rows","Returns only unique rows","Sorts results","Joins tables","B","DISTINCT removes duplicate rows from result",S,"SELECT & Filtering","SELECT & Filtering","SELECT","easy",2021,1,0)
add("Which join returns only matching rows from both tables?","Left Join","Full Outer Join","Inner Join","Cross Join","C","Inner Join returns rows with matching keys in both tables",S,"Joins & Subqueries","Joins & Subqueries","Joins","easy",2022,1,0)
add("Which SQL command creates a new table?","INSERT","ALTER","CREATE","UPDATE","C","CREATE TABLE creates a new table",S,"DDL & DML Commands","DDL & DML Commands","DDL","easy",2021,1,0)
add("What does COUNT(*) return?","Sum of all values","Number of rows","Average","Maximum value","B","COUNT(*) counts all rows including NULLs",S,"Aggregations & Grouping","Aggregations & Grouping","Aggregations","easy",2022,1,0)

# ── SQL ADVANCED ──────────────────────────────────────────────────────────────
S="SQL_ADVANCED"
add("What is an index in SQL?","A table column","A data structure to speed up queries","A stored procedure","A constraint","B","Index improves query performance but uses extra storage",S,"Indexes & Views","Indexes & Views","Indexes","easy",2022,1,0)
add("What does ACID stand for in databases?","Auto, Commit, Index, Delete","Atomicity, Consistency, Isolation, Durability","Array, Class, Integer, Data","None of the above","B","ACID ensures reliable database transactions",S,"Transactions & ACID","Transactions & ACID","ACID","medium",2021,1,0)
add("Which command rolls back a transaction?","COMMIT","ROLLBACK","SAVEPOINT","BEGIN","B","ROLLBACK undoes all changes in a transaction",S,"Transactions & ACID","Transactions & ACID","Transactions","easy",2022,1,0)
add("What is a stored procedure?","A view","A precompiled set of SQL statements","An index","A trigger","B","Stored procedures are saved executable SQL code blocks",S,"Stored Procedures & Triggers","Stored Procedures & Triggers","Stored Procedures","easy",2021,1,0)

# ── DSA ───────────────────────────────────────────────────────────────────────
S="DSA_PRACTICE"
add("Which sorting algorithm is best for nearly sorted arrays?","QuickSort","MergeSort","Insertion Sort","Bubble Sort","C","Insertion sort O(n) for nearly sorted",S,"Sorting, Searching & DP","Sorting, Searching & DP","Sorting","medium",2022,1,0)
add("What is time complexity of accessing element in array by index?","O(n)","O(log n)","O(1)","O(n²)","C","Direct index access is O(1)",S,"Arrays & Strings","Arrays & Strings","Arrays","easy",2022,1,0)
add("Which data structure is used in BFS?","Stack","Queue","Heap","Tree","B","BFS uses Queue (FIFO)",S,"Trees & Graphs","Trees & Graphs","Graph Traversal","easy",2021,1,0)
add("What is the best case time complexity of QuickSort?","O(n²)","O(n log n)","O(n)","O(log n)","B","Best case with balanced partitions: O(n log n)",S,"Sorting, Searching & DP","Sorting, Searching & DP","Sorting","medium",2021,1,0)
add("Time complexity of searching in a balanced BST?","O(1)","O(n)","O(log n)","O(n log n)","C","BST search: O(log n) when balanced",S,"Trees & Graphs","Trees & Graphs","Trees","medium",2022,1,0)

# ── AWS SAA-C03 ───────────────────────────────────────────────────────────────
S="AWS_SAA_C03"
add("Which AWS service provides scalable object storage?","EBS","EFS","S3","Glacier","C","S3 = Simple Storage Service for object storage",S,"Storage","Resilient Architectures","Storage","easy",2023,1,0)
add("Which service provides managed relational database?","DynamoDB","ElastiCache","RDS","Redshift","C","RDS = Relational Database Service",S,"Databases","Resilient Architectures","Databases","easy",2023,1,0)
add("Which AWS service is used for CDN?","Route 53","CloudFront","API Gateway","ALB","B","CloudFront is AWS CDN service",S,"Networking","High-Performance Architectures","CDN","easy",2022,1,0)
add("IAM stands for?","Internet Access Management","Identity and Access Management","Internal Access Manager","Integrated Auth Module","B","IAM = Identity and Access Management",S,"Security","Security & Identity","IAM","easy",2022,1,0)

# ── TCS NQT IT ────────────────────────────────────────────────────────────────
S="TCS_NQT_IT"
add("A man walks 5km East then 3km North. Distance from start?","√34 km","8 km","4 km","√28 km","A","√(5²+3²)=√34 km",S,"Numerical Ability","Numerical Ability","Distance","medium",2022,1,0)
add("If 6 workers build a wall in 15 days, how long for 10?","7 days","8 days","9 days","10 days","C","6×15=10×x → x=9 days",S,"Numerical Ability","Numerical Ability","Time & Work","easy",2022,1,0)
add("Which is NOT a valid identifier in most languages?","_variable","2variable","variable2","my_var","B","Identifiers cannot start with digits",S,"Programming Logic","Programming Logic","Basics","easy",2021,1,0)
add("Output of: for i in range(3): print(i) in Python?","0 1 2","1 2 3","0 1 2 3","1 2","A","range(3) gives 0,1,2",S,"Programming Logic","Programming Logic","Loops","easy",2022,1,0)
add("Which is the correct logical expression for 'a OR NOT b'?","a && !b","a || !b","!a || b","a && b","B","OR=||, NOT=! so 'a OR NOT b' = a||!b",S,"Reasoning Ability","Reasoning Ability","Boolean Logic","medium",2022,1,0)

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

# ── COGNIZANT GENC ────────────────────────────────────────────────────────────
S="COGNIZANT_GENC"
add("All roses are flowers. Some flowers are red. Conclusion?","All roses are red","Some roses are red","No conclusion about roses being red","All flowers are roses","C","No direct conclusion from given premises",S,"Reasoning Ability","Reasoning Ability","Syllogism","medium",2022,1,0)
add("A and B invest 3:4. Profit Rs.8400. B's share?","Rs.3600","Rs.4800","Rs.4200","Rs.5400","B","B's share=4/7×8400=Rs.4800",S,"Quantitative Aptitude","Quantitative Aptitude","Partnership","easy",2021,1,0)
add("Find next: 2,6,12,20,30,?","40","42","44","48","B","Differences 4,6,8,10,12 → 30+12=42",S,"Reasoning Ability","Reasoning Ability","Number Series","medium",2022,1,0)

# ── APTITUDE: NUMBER SYSTEM ───────────────────────────────────────────────────
S="APT_NUMBER_SYSTEM"
add("LCM of 12, 18, and 24?","36","72","48","60","B","LCM=2³×3²=72",S,"Number System & Divisibility","Number System & Divisibility","LCM","easy",2022,1,0)
add("HCF of 48 and 64?","8","16","12","24","B","48=2⁴×3, 64=2⁶, HCF=2⁴=16",S,"Number System & Divisibility","Number System & Divisibility","HCF","easy",2021,1,0)
add("What is the remainder when 17 is divided by 5?","1","2","3","4","B","17=5×3+2, remainder=2",S,"Number System & Divisibility","Number System & Divisibility","Remainders","easy",2022,1,0)
add("Which of the following is a prime number?","15","21","37","49","C","37 is prime; others have factors",S,"Number System & Divisibility","Number System & Divisibility","Primes","easy",2021,1,0)
add("The product of two numbers is 120. If one is 8, the other is?","14","15","16","18","B","120/8=15",S,"Number System & Divisibility","Number System & Divisibility","Basic Operations","easy",2022,1,0)

# ── APTITUDE: PERCENTAGE ──────────────────────────────────────────────────────
S="APT_PERCENTAGE"
add("What is 15% of 200?","25","30","35","40","B","15/100×200=30",S,"Percentage & Applications","Percentage & Applications","Percentage","easy",2022,1,0)
add("A price increases from Rs.500 to Rs.600. % increase?","15%","20%","25%","10%","B","(100/500)×100=20%",S,"Percentage & Applications","Percentage & Applications","Percentage Change","easy",2021,1,0)
add("If 40% of x = 120, then x = ?","200","250","300","350","C","x=120×100/40=300",S,"Percentage & Applications","Percentage & Applications","Finding X","easy",2022,1,0)
add("A shopkeeper gives 20% discount on Rs.1000. Selling price?","700","750","800","850","C","SP=1000×(1-0.20)=800",S,"Percentage & Applications","Percentage & Applications","Discount","easy",2021,1,0)

# ── APTITUDE: PROFIT & LOSS ───────────────────────────────────────────────────
S="APT_PROFIT_LOSS"
add("A book is bought for Rs.200, sold for Rs.250. Profit%?","20%","25%","30%","15%","B","Profit%=(50/200)×100=25%",S,"Profit, Loss & Discount","Profit, Loss & Discount","Profit","easy",2022,1,0)
add("SP=Rs.360, loss 10%. CP=?","Rs.400","Rs.380","Rs.420","Rs.450","A","CP=360/0.90=400",S,"Profit, Loss & Discount","Profit, Loss & Discount","Loss","medium",2021,1,0)
add("CP=Rs.500, profit 20%. SP=?","Rs.580","Rs.590","Rs.600","Rs.620","C","SP=500×1.20=600",S,"Profit, Loss & Discount","Profit, Loss & Discount","Profit","easy",2022,1,0)

# ── APTITUDE: TIME & WORK ─────────────────────────────────────────────────────
S="APT_TIME_WORK"
add("A can do a work in 10 days, B in 20 days. Together?","5 days","6 days","7 days","8 days","C","1/10+1/20=3/20 → 20/3≈6.67≈7 days",S,"Time, Work & Pipes","Time, Work & Pipes","Time & Work","medium",2022,1,0)
add("A pipe fills a tank in 6 hrs, another empties in 12 hrs. Net time?","12 hrs","10 hrs","8 hrs","6 hrs","A","Net rate=1/6-1/12=1/12 → 12 hrs",S,"Time, Work & Pipes","Time, Work & Pipes","Pipes & Cisterns","medium",2021,1,0)
add("If 5 workers finish a job in 8 days, 8 workers finish in?","4 days","5 days","6 days","7 days","B","5×8=8×x → x=5 days",S,"Time, Work & Pipes","Time, Work & Pipes","Time & Work","easy",2022,1,0)

# ── APTITUDE: SPEED & DISTANCE ────────────────────────────────────────────────
S="APT_SPEED_DISTANCE"
add("A train 200m long passes a pole in 20s. Speed in km/h?","30","36","40","45","B","Speed=200/20=10m/s=36km/h",S,"Speed, Distance & Trains","Speed, Distance & Trains","Trains","easy",2022,1,0)
add("Distance=240km, Speed=60km/h. Time taken?","3 hrs","4 hrs","5 hrs","6 hrs","B","Time=240/60=4 hrs",S,"Speed, Distance & Trains","Speed, Distance & Trains","Speed & Time","easy",2021,1,0)
add("Boat goes 15km upstream in 3hrs, 15km downstream in 1.5hrs. Speed of stream?","2.5 km/h","5 km/h","3 km/h","4 km/h","A","Downstream=10, Upstream=5; Stream=(10-5)/2=2.5",S,"Speed, Distance & Trains","Speed, Distance & Trains","Boats & Streams","medium",2022,1,0)

# ── APTITUDE: INTEREST ────────────────────────────────────────────────────────
S="APT_INTEREST"
add("SI on Rs.5000 at 8% per year for 3 years?","Rs.1000","Rs.1200","Rs.1500","Rs.2000","B","SI=5000×8×3/100=1200",S,"Simple & Compound Interest","Simple & Compound Interest","Simple Interest","easy",2022,1,0)
add("CI on Rs.10000 at 10% for 2 years?","Rs.2000","Rs.2100","Rs.2200","Rs.1900","B","CI=10000×(1.1²-1)=2100",S,"Simple & Compound Interest","Simple & Compound Interest","Compound Interest","medium",2021,1,0)
add("At what rate SI, Rs.2000 becomes Rs.2500 in 5 years?","4%","5%","6%","3%","B","SI=500, Rate=500×100/(2000×5)=5%",S,"Simple & Compound Interest","Simple & Compound Interest","Simple Interest","easy",2022,1,0)

# ── APTITUDE: RATIO & PROPORTION ─────────────────────────────────────────────
S="APT_RATIO_PROPORTION"
add("Ratio of A:B=3:4. If B=120, A=?","80","90","100","110","B","A=3/4×120=90",S,"Ratio, Proportion & Mixtures","Ratio, Proportion & Mixtures","Ratio","easy",2022,1,0)
add("In what ratio milk:water gives 40L if milk:water=3:2?","24L milk, 16L water","20L milk, 20L water","30L milk, 10L water","15L milk, 25L water","A","Milk=3/5×40=24, Water=2/5×40=16",S,"Ratio, Proportion & Mixtures","Ratio, Proportion & Mixtures","Mixtures","easy",2021,1,0)

# ── APTITUDE: ALGEBRA ────────────────────────────────────────────────────────
S="APT_ALGEBRA"
add("Solve: 2x+5=13. x=?","3","4","5","6","B","2x=8, x=4",S,"Algebra, Equations & Inequalities","Algebra, Equations & Inequalities","Linear Equations","easy",2022,1,0)
add("If x²-5x+6=0, the roots are?","2,3","1,6","3,4","2,4","A","(x-2)(x-3)=0 → x=2,3",S,"Algebra, Equations & Inequalities","Algebra, Equations & Inequalities","Quadratic Equations","medium",2021,1,0)
add("Simplify: (a+b)²","a²+b²","a²+2ab+b²","a²-2ab+b²","2a+2b","B","(a+b)²=a²+2ab+b²",S,"Algebra, Equations & Inequalities","Algebra, Equations & Inequalities","Identities","easy",2022,1,0)

# ── APTITUDE: GEOMETRY ────────────────────────────────────────────────────────
S="APT_GEOMETRY"
add("Area of circle with radius 7cm?","132 cm²","147 cm²","154 cm²","160 cm²","C","A=π×7²=22/7×49=154",S,"Geometry, Triangles & Mensuration","Geometry, Triangles & Mensuration","Circle","easy",2022,1,0)
add("Perimeter of rectangle: length=12, breadth=8?","40","38","42","36","A","P=2(12+8)=40",S,"Geometry, Triangles & Mensuration","Geometry, Triangles & Mensuration","Rectangle","easy",2021,1,0)
add("Volume of cube with side 5cm?","100 cm³","115 cm³","125 cm³","130 cm³","C","V=5³=125 cm³",S,"Geometry, Triangles & Mensuration","Geometry, Triangles & Mensuration","Cube","easy",2022,1,0)

# ── REASONING: VERBAL ────────────────────────────────────────────────────────
S="REASONING_VERBAL"
add("Doctor : Hospital :: Teacher : ?","School","Office","Court","Market","A","Teacher works in a School",S,"Analogy & Classification","Analogy & Classification","Analogy","easy",2022,1,0)
add("If APPLE is coded as BQQMF, how is MANGO coded?","NBNHP","NBOHP","NCOIP","NANHP","B","Each letter shifted +1: M→N, A→B, N→O, G→H, O→P",S,"Series & Coding-Decoding","Series & Coding-Decoding","Coding-Decoding","medium",2021,1,0)
add("A is B's mother. C is B's brother. How is A related to C?","Sister","Daughter","Mother","Aunt","C","If A is B's mother and C is B's brother, A is C's mother",S,"Syllogism & Blood Relations","Syllogism & Blood Relations","Blood Relations","easy",2022,1,0)
add("Pointing north, you turn right. Turn right again. Which direction?","North","South","East","West","B","North→Right=East→Right=South",S,"Direction & Ranking","Direction & Ranking","Directions","easy",2021,1,0)
add("Find odd one out: Dog, Cat, Cow, Rose","Dog","Cat","Cow","Rose","D","Rose is a flower; others are animals",S,"Analogy & Classification","Analogy & Classification","Classification","easy",2022,1,0)

# ── REASONING: NON-VERBAL ────────────────────────────────────────────────────
S="REASONING_NON_VERBAL"
add("A figure rotated 180° and then reflected. Which transformation results?","Same as original","Mirror of original","Upside down","None","A","180° rotation + reflection = original for symmetric figures",S,"Pattern Recognition","Pattern Recognition","Rotation","medium",2022,1,0)
add("Mirror image of 'EXAM' in a vertical mirror?","MAXE","EXAM","MXAE","AXEM","A","Vertical mirror reverses left-right: EXAM → MAXE",S,"Mirror & Water Images","Mirror & Water Images","Mirror Images","easy",2021,1,0)
add("How many triangles are in a triangle divided by 3 lines from vertices?","4","6","7","9","B","3 lines from vertices create 6 small triangles",S,"Embedded & Counting Figures","Embedded & Counting Figures","Counting Figures","medium",2022,1,0)

# ── REASONING: LOGICAL ───────────────────────────────────────────────────────
S="REASONING_LOGICAL"
add("All birds can fly. Penguin is a bird. Conclusion?","Penguin can fly","Penguin cannot fly","No conclusion","Penguins are not birds","A","Based on the given premises, penguin can fly (logical deduction)",S,"Statements & Conclusions","Statements & Conclusions","Syllogism","medium",2022,1,0)
add("Statement: Students who study hard pass. Ram passed. Assumption?","Ram studied hard","Ram is a student","Passing is easy","Teachers help","A","The most reasonable assumption is that Ram studied hard",S,"Assumptions & Arguments","Assumptions & Arguments","Assumptions","medium",2021,1,0)
add("Which is a valid argument form? P→Q, P, therefore?","Not Q","Q","Not P","P and Q","B","Modus Ponens: if P→Q and P, then Q",S,"Logical Deduction","Logical Deduction","Logic","medium",2022,1,0)
add("Problem: Crime is rising. Best course of action?","Ignore it","Increase police patrols","Close all roads","Reduce jobs","B","Increasing police presence is a direct course of action",S,"Course of Action","Course of Action","Course of Action","easy",2021,1,0)

# ── REASONING: PUZZLES ───────────────────────────────────────────────────────
S="REASONING_PUZZLES"
add("5 people sit in a row. A is to the left of B, C is to the right of B. Who is in the middle?","A","B","C","D","B","B has A on left and C on right, so B is in middle",S,"Linear & Circular Seating","Linear & Circular Seating","Linear Seating","medium",2022,1,0)
add("In a circular arrangement of 6 people, how many arrangements are possible?","720","120","6","24","B","Circular arrangements = (n-1)! = 5! = 120",S,"Linear & Circular Seating","Linear & Circular Seating","Circular Seating","medium",2021,1,0)
add("Box A is above Box B. Box C is below Box B. Which box is at top?","Box B","Box A","Box C","Cannot determine","B","A is above B, so A is at the top",S,"Box, Floor & Complex Puzzles","Box, Floor & Complex Puzzles","Box Puzzles","easy",2022,1,0)

# ── REASONING: FULL MOCK ─────────────────────────────────────────────────────
S="REASONING_FULL_MOCK"
add("If 'MOON' = 57, 'STAR' = 58, what is 'SUN'?","54","55","56","57","C","S=19,U=21,N=14 → sum=54? Use positional values",S,"Verbal Reasoning","Verbal Reasoning","Coding","medium",2022,1,0)
add("Complete: 2, 4, 8, 16, ?","24","28","32","36","C","Geometric ×2: 16×2=32",S,"Verbal Reasoning","Verbal Reasoning","Number Series","easy",2021,1,0)
add("A person is 7th from left and 8th from right in a row. How many people?","14","15","16","13","A","Total=7+8-1=14",S,"Verbal Reasoning","Verbal Reasoning","Ranking","easy",2022,1,0)

# ── APTITUDE: DATA INTERPRETATION ────────────────────────────────────────────
S="APT_DATA_INTERPRETATION"
add("A bar graph shows sales: Jan=200, Feb=250, Mar=300. Average sales?","225","233","250","275","C","Average=(200+250+300)/3=250",S,"Bar Graph & Line Chart","Bar Graph & Line Chart","Bar Graph","easy",2022,1,0)
add("A pie chart: 25% is 50 units. Total units?","150","175","200","225","C","Total=50×100/25=200",S,"Pie Chart & Table","Pie Chart & Table","Pie Chart","easy",2021,1,0)
add("In a table, 2022 profit is Rs.1200, 2021 profit is Rs.1000. % growth?","10%","15%","20%","25%","C","Growth=(200/1000)×100=20%",S,"Pie Chart & Table","Pie Chart & Table","Table DI","easy",2022,1,0)

# ── APTITUDE: FULL MOCK ───────────────────────────────────────────────────────
S="APT_FULL_MOCK"
add("Train travels 300km at 60km/h. Time taken?","4 hrs","5 hrs","6 hrs","7 hrs","B","T=300/60=5 hrs",S,"Arithmetic & Number System","Arithmetic & Number System","Speed & Time","easy",2022,1,0)
add("What is 35% of 500?","150","165","175","180","C","35/100×500=175",S,"Arithmetic & Number System","Arithmetic & Number System","Percentage","easy",2021,1,0)
add("If 2x+3=11, x=?","3","4","5","6","B","2x=8, x=4",S,"Algebra & Geometry","Algebra & Geometry","Equations","easy",2022,1,0)

db.commit()
count = db.query(Question).count()
print(f"[OK] Seeded {count} questions across all exam categories!")
db.close()
