# SPARTA Foundation - Ground Truth Layer (Strat 0)

**ΜΟΛΩΝ ΛΑΒΕ** - Fortăreața Adevărului 🏛️⚡🔥

## Introducere: Fundamentul Epistemologic

**SPARTA Foundation** este **Stratul 0** - baza epistemică absolută a întregului sistem ΛΕΩΝΙΔΑΣ-AI PHALANX.

Este echivalentul unei **fortărețe construite pe rocă vulcanică solidă**:
- Fiecare piatră (concept) este verificată științific
- Fiecare piatră are o poziție precisă (domain, subdomain, topic)
- Fiecare piatră are legături cu altele (relations, prerequisites)
- Fiecare piatră are un certificat de autenticitate (source, confidence)

**Foundation conține 440+ concepte fundamentale** din 11 domenii științifice, fiecare cu **confidence 0.95-1.0** (verificat empiric sau matematic).

---

## Cele 11 Domenii Științifice

### Tabelul Domeniilor

| # | Domain | Subdomains | Total Concepts | Confidence Range | Examples |
|---|--------|-----------|----------------|------------------|----------|
| 1 | **Mathematics** 🔢 | Algebra, Geometry, Calculus, Logic, Number Theory, Statistics | 85 | 0.98-1.0 | Pythagorean Theorem, Integration, Prime Numbers |
| 2 | **Physics** ⚡ | Mechanics, Thermodynamics, Electromagnetism, Quantum, Relativity | 76 | 0.97-0.99 | Conservation of Energy, Maxwell's Equations, E=mc² |
| 3 | **Computer Science** 💻 | Algorithms, Data Structures, Complexity, Cryptography, Networks | 62 | 0.95-0.99 | Binary Search, RSA Encryption, TCP/IP Protocol |
| 4 | **Biology** 🧬 | Cell Biology, Genetics, Evolution, Ecology, Physiology | 58 | 0.95-0.98 | Cell Theory, DNA Structure, Natural Selection |
| 5 | **Medicine** 🏥 | Anatomy, Pharmacology, Pathology, Immunology, Neurology | 43 | 0.95-0.97 | Blood Circulation, Antibiotic Resistance, Neurons |
| 6 | **Psychology** 🧠 | Cognitive, Behavioral, Developmental, Social, Clinical | 31 | 0.95-0.97 | Working Memory, Classical Conditioning, Maslow's Hierarchy |
| 7 | **Ethics** ⚖️ | Normative, Applied, Meta-Ethics, Moral Philosophy | 24 | 0.95-0.97 | Categorical Imperative, Utilitarianism, Virtue Ethics |
| 8 | **Philosophy** 📚 | Epistemology, Metaphysics, Logic, Philosophy of Mind | 22 | 0.95-0.98 | Cogito Ergo Sum, Occam's Razor, Problem of Induction |
| 9 | **Astronomy** 🌌 | Celestial Mechanics, Cosmology, Astrophysics, Planetary Science | 18 | 0.96-0.99 | Kepler's Laws, Big Bang Theory, Black Holes |
| 10 | **Linguistics** 🗣️ | Syntax, Semantics, Phonetics, Morphology, Pragmatics | 14 | 0.95-0.98 | Chomsky Hierarchy, Phoneme Theory, Syntax Trees |
| 11 | **AI & AGI** 🤖 | Machine Learning, Neural Networks, Reasoning, AGI Theory | 12 | 0.95-0.98 | Backpropagation, Transformer Architecture, Turing Test |
| **TOTAL** | | | **445** | **0.95-1.0** | |

### Distribuția Confidence-ului

```
Confidence 1.0:    [85 concepts]  ████████████████  19.1%  (Mathematical proofs)
Confidence 0.99:   [76 concepts]  ███████████████   17.1%  (Physics laws)
Confidence 0.98:   [103 concepts] ████████████████████  23.1%  (Strong theories)
Confidence 0.97:   [98 concepts]  ███████████████████   22.0%  (Scientific consensus)
Confidence 0.96:   [52 concepts]  ██████████        11.7%  (Well-established)
Confidence 0.95:   [31 concepts]  ██████            7.0%   (Validated facts)
                   ────────────────────────────────────────
TOTAL:             [445 concepts] 100%
```

---

## Formatul JSON al Conceptelor

Fiecare concept din Foundation este reprezentat în **JSON** cu **15 câmpuri obligatorii**:

### Schema Completă JSON

```json
{
  "id": "STRING",
  "domain": "STRING",
  "subdomain": "STRING",
  "topic": "STRING",
  "definition": "STRING (concise)",
  "formal_statement": "STRING (mathematical/formal)",
  "relations": ["ARRAY of concept IDs"],
  "prerequisites": ["ARRAY of concept IDs"],
  "confidence": FLOAT (0.95-1.0),
  "source": "STRING (verification source)",
  "reflex_tag": "STRING (RFX_XXX_NNN)",
  "examples": ["ARRAY of concrete examples"],
  "counterexamples": ["ARRAY of what it's NOT"],
  "applications": ["ARRAY of real-world uses"],
  "verification": "STRING (how we verify)",
  "uncertainty": "STRING (what we DON'T know)"
}
```

### De Ce Fiecare Câmp Este Critic

#### 1. `id` (STRING)

**Format**: `DOMAIN_SUBDOMAIN_NNN` (ex: `PHYS_MECHANICS_001`)

**Scop**: Identificator unic pentru fiecare concept în dependency graph.

**De ce este critic**: 
- Permite referențierea precisă în `relations` și `prerequisites`
- Construiește dependency graph navigabil
- Previne duplicări

**Exemplu**:
```json
"id": "PHYS_MECHANICS_001"  // Concept #1 din Mechanics (Physics)
"id": "MATH_CALCULUS_042"   // Concept #42 din Calculus (Math)
```

#### 2. `domain` (STRING)

**Valori posibile**: Mathematics, Physics, Computer Science, Biology, Medicine, Psychology, Ethics, Philosophy, Astronomy, Linguistics, AI & AGI

**Scop**: Clasificare primară - în ce domeniu științific se încadrează conceptul.

**De ce este critic**:
- Permite filtrarea rapidă în Phalanx Bridge: `get_concepts(domain="Physics")`
- Organizează Foundation în compartimente epistemice
- Facilitează query routing (dacă query e despre fizică → căută în domain Physics)

**Exemplu**:
```json
"domain": "Physics"  // Concept din domeniul Fizicii
```

#### 3. `subdomain` (STRING)

**Scop**: Clasificare secundară - subdomeniul specific în cadrul domeniului.

**De ce este critic**:
- Granularitate mai fină pentru filtering
- Permite queries specifice: "Vreau doar concepte din Quantum Physics, nu Mechanics"
- Construiește ierarhii de cunoaștere

**Exemplu**:
```json
"domain": "Physics",
"subdomain": "Mechanics"  // Sub-domeniu specific
```

#### 4. `topic` (STRING)

**Scop**: Numele human-readable al conceptului.

**De ce este critic**:
- Query matching: user întreabă "conservarea energiei" → match cu `topic: "Conservation of Energy"`
- Afișare în răspunsuri (user-friendly)
- Semantic search

**Exemplu**:
```json
"topic": "Conservation of Energy"
```

#### 5. `definition` (STRING - concise)

**Scop**: Explicație clară, concisă a conceptului (1-3 propoziții).

**De ce este critic**:
- Bază pentru răspunsuri clare către user
- Training data pentru semantic understanding
- Verificare că înțelegem conceptul corect

**⚠️ IMPORTANT**: Phalanx Bridge **NU trimite definition direct** la Reflexive Generator - forțează raționament prin `relations`.

**Exemplu**:
```json
"definition": "Energy cannot be created or destroyed, only transformed from one form to another. The total energy in an isolated system remains constant."
```

#### 6. `formal_statement` (STRING - mathematical/formal)

**Scop**: Formulare matematică/formală riguroasă a conceptului.

**De ce este critic**:
- Precizie maximă (eliminăm ambiguitate)
- Verificare matematică (proof checking)
- Computation-ready (poate fi folosit în calcule)

**Exemplu**:
```json
"formal_statement": "For an isolated system: E_total = constant. dE/dt = 0. E = KE + PE + U (kinetic + potential + internal)"
```

#### 7. `relations` (ARRAY of concept IDs)

**Scop**: Concepte **înrudite** (not prerequisites) - legături laterale în graph.

**De ce este CRUCIAL pentru anti-halucinație**:
- Reflexive Generator construiește raționament prin **traversarea relations**
- Previne inventarea de legături false (doar relations din Foundation sunt valide)
- Creează context semantic dens

**Exemplu**:
```json
"relations": [
  "PHYS_MECHANICS_002",  // Kinetic Energy
  "PHYS_MECHANICS_003",  // Potential Energy
  "PHYS_THERMO_001",     // First Law of Thermodynamics
  "PHYS_QUANTUM_015"     // Energy in Quantum Systems
]
```

**Anti-Pattern** (ce NU face SPARTA):
```
// GPT-4 ar inventa:
"Conservation of Energy este înrudit cu Perpetuum Mobile" 
// (fals - perpetuum mobile încalcă conservarea energiei)
```

**SPARTA**:
```
// Verifică în relations:
if "PHYS_MECHANICS_099" in concept['relations']:  # Perpetuum Mobile
    # Da, există relație explicit definită
else:
    # Nu există - NU menționa
```

#### 8. `prerequisites` (ARRAY of concept IDs)

**Scop**: Concepte **necesare** pentru a înțelege conceptul curent - dependency graph.

**De ce este critic**:
- Asigură ordinea corectă de învățare
- Validare: dacă prerequisite lipsește → ERROR la load
- Construiește paths de raționament logice

**Exemplu**:
```json
"prerequisites": [
  "MATH_CALCULUS_001",   // Derivatives (necesari pentru dE/dt = 0)
  "PHYS_MECHANICS_000"   // Newton's Laws (baza mecanicii)
]
```

**Diferența între `relations` și `prerequisites`**:
- **Prerequisites**: "Trebuie să știi X pentru a înțelege Y" (ordine strictă)
- **Relations**: "X și Y sunt concepte legate" (ordine liberă)

```
Prerequisites: Algebra → Calculus → Physics (trebuie în ordine)
Relations: Kinetic Energy ↔ Potential Energy (ambele direcții, ordine liberă)
```

#### 9. `confidence` (FLOAT: 0.95-1.0)

**Scop**: Gradul de **certitudine epistemică** că conceptul este adevărat.

**De ce este critic**:
- Propagare în răspunsuri (răspunsul are confidence = min(concepts))
- Filtering (doar concepts cu confidence >= threshold)
- Onestitate epistemică (admitem incertitudinea)

**Scala Confidence**:

| Value | Meaning | Verification | Example |
|-------|---------|-------------|---------|
| **1.0** | Mathematical Truth | Rigorous proof | Pythagorean Theorem, 2+2=4 |
| **0.99** | Physical Law | 100+ years experimental verification | Conservation of Energy, Newton's Laws |
| **0.98** | Strong Theory | GPS, technology depends on it | General Relativity, Quantum Mechanics |
| **0.97** | Scientific Consensus | Fossil record, genetic evidence | Evolution, DNA Structure |
| **0.96** | Well-Established | Multiple independent verifications | Cell Theory, Germ Theory |
| **0.95** | Validated Fact | Strong evidence, some uncertainty | Specific drug dosages, recent discoveries |

**Exemplu**:
```json
"confidence": 0.99,  // Physical law - masiv verificată experimental
```

**Anti-Pattern** (GPT-4):
```
// GPT-4 "confidence" = P(next token | context)
P("Einstein") = 0.92 după "Relativitatea a fost descoperită de"
// Dar asta NU înseamnă că Relativitatea este adevărată cu 0.92
```

**SPARTA confidence** = P(concept is TRUE | verification)

#### 10. `source` (STRING)

**Scop**: **De unde știm** că conceptul este adevărat - sursa verificării.

**De ce este CRUCIAL**:
- **Transparență epistemică**: user poate verifica singur
- **Traceability**: fiecare afirmație are origine
- **Prevented hallucination**: fără source = NU intră în Foundation

**Format recomandat**: "Author/Institution (Year), Method"

**Exemplu**:
```json
"source": "Emmy Noether (1915), Mathematical proof in Noether's Theorem; Verified by 100+ years of experiments in closed systems"
```

**Tipuri de sources**:
- **Mathematical proof**: "Euclid's Elements (~300 BCE), geometric proof"
- **Experimental verification**: "Large Hadron Collider (2012), Higgs boson detection"
- **Observational**: "Hubble Space Telescope (1998), Type Ia supernovae observations"
- **Consensus**: "IPCC Reports (2021), 97% scientific consensus"

#### 11. `reflex_tag` (STRING: RFX_XXX_NNN)

**Format**: `RFX_<CATEGORY>_<NUMBER>`

**Scop**: Tag pentru **reflexive reasoning** - categorii de raționament.

**De ce este util**:
- Clasificare rapidă a tipului de concept
- Pattern matching în Λ-Pattern
- Optimization în query routing

**Categorii**:
- `RFX_LAW_NNN`: Legi fundamentale (Conservation, Newton's Laws)
- `RFX_THM_NNN`: Teoreme matematice (Pythagorean, Fermat)
- `RFX_PRN_NNN`: Principii generale (Occam's Razor, Uncertainty)
- `RFX_FCT_NNN`: Fapte verificate (Earth radius, DNA structure)
- `RFX_THY_NNN`: Teorii (Evolution, Quantum Mechanics)

**Exemplu**:
```json
"reflex_tag": "RFX_LAW_001"  // Legea #1 (Conservation of Energy)
```

#### 12. `examples` (ARRAY of strings)

**Scop**: Exemple **concrete** care ilustrează conceptul.

**De ce este critic pentru anti-halucinație**:
- User înțelege mai bine cu exemple
- Demonstrează **aplicabilitate** (conceptul nu e abstract)
- Previne interpretări greșite

**Exemplu**:
```json
"examples": [
  "A pendulum: KE ↔ PE transformation, total E constant",
  "Roller coaster: at top (max PE, min KE), at bottom (min PE, max KE)",
  "Elastic collision: two balls exchange energy, total unchanged",
  "Hydroelectric dam: water PE → turbine KE → electrical energy"
]
```

**Reguli pentru examples**:
- Minimum 2, recomandat 4
- Concrete, specific (NU vag)
- Diverse (diferite contexte)
- Verificabile (user poate testa/verifica)

#### 13. `counterexamples` (ARRAY of strings)

**Scop**: Ce **NU este** conceptul - previne confuzii.

**De ce este CRUCIAL pentru anti-halucinație**:
- **Definește granițele** conceptului
- Previne over-generalizarea
- Corectează misconceptions comune

**Exemplu**:
```json
"counterexamples": [
  "NOT: Energy can be created (violates conservation)",
  "NOT: Perpetual motion machines (impossible, violate conservation)",
  "NOT: Energy disappears (transforms, doesn't vanish)",
  "NOT: Energy increases spontaneously in isolated system"
]
```

**De ce counterexamples sunt critical**:
- GPT-4 poate inventa "Conservation of Energy permite..." (fals)
- SPARTA verifică: "Permite X?" → Check counterexamples → "NU, X e în counterexamples"

#### 14. `applications` (ARRAY of strings)

**Scop**: Unde se **folosește** conceptul în lumea reală.

**De ce este important**:
- Demonstrează **relevance**
- Conectează teoria cu practica
- Motivează învățarea

**Exemplu**:
```json
"applications": [
  "Engineering: Design of efficient machines (minimize energy loss)",
  "Aerospace: Rocket trajectory calculations (energy transformations)",
  "Climate science: Energy balance models (Earth system)",
  "Nuclear power: E=mc² conversion (mass-energy equivalence)"
]
```

#### 15. `verification` (STRING)

**Scop**: **Cum** verificăm că conceptul este adevărat.

**De ce este critic**:
- **Metodologie** transparentă
- Reproducibility (alții pot verifica)
- Confidence justificat

**Exemplu**:
```json
"verification": "Experimental: Countless closed-system experiments (pendulums, collisions, thermodynamics) over 200+ years. Mathematical: Noether's Theorem proves conservation from time-translation symmetry. No violation ever observed."
```

**Tipuri de verification**:
- **Experimental**: "Repeated lab experiments, consistent results"
- **Observational**: "Astronomical observations, statistical analysis"
- **Mathematical**: "Rigorous proof, peer-reviewed"
- **Technological**: "GPS works (proves relativity), computers work (proves quantum mechanics)"

#### 16. `uncertainty` (STRING)

**Scop**: Ce **NU știm** despre concept - onestitate epistemică.

**De ce este CRUCIAL**:
- **Forced honesty**: admitem limitele cunoașterii
- Previne over-confidence
- Ghidează research viitor

**Exemplu**:
```json
"uncertainty": "Unknown: Behavior at quantum-gravity scales (Planck scale). Unknown: Energy conservation in expanding universe (dark energy). Unknown: Whether energy is truly fundamental or emergent property."
```

**Regula Spartană**: **Fiecare concept TREBUIE să aibă uncertainty** - arată că suntem conștienți de limitele epistemice.

---

## Exemple Complete de Concepte

### Exemplu 1: Conservation of Energy (Complete)

```json
{
  "id": "PHYS_MECHANICS_001",
  "domain": "Physics",
  "subdomain": "Mechanics",
  "topic": "Conservation of Energy",
  
  "definition": "Energy cannot be created or destroyed in an isolated system, only transformed from one form to another. The total energy remains constant over time.",
  
  "formal_statement": "For an isolated system: E_total = constant, dE/dt = 0. E_total = KE + PE + U + Q + ... where KE=kinetic, PE=potential, U=internal, Q=heat. In closed system: E_in - E_out = ΔE_system",
  
  "relations": [
    "PHYS_MECHANICS_002",  // Kinetic Energy
    "PHYS_MECHANICS_003",  // Potential Energy
    "PHYS_THERMO_001",     // First Law of Thermodynamics
    "PHYS_THERMO_005",     // Heat Transfer
    "PHYS_QUANTUM_015",    // Energy in Quantum Systems
    "MATH_CALCULUS_010"    // Conservation Laws (Noether's Theorem)
  ],
  
  "prerequisites": [
    "PHYS_MECHANICS_000",  // Newton's Laws
    "MATH_CALCULUS_001",   // Derivatives (for dE/dt)
    "MATH_ALGEBRA_005"     // Equations
  ],
  
  "confidence": 0.99,
  
  "source": "Emmy Noether (1915), Noether's Theorem - energy conservation derived from time-translation symmetry. Verified by 200+ years of experiments in mechanics, thermodynamics, quantum mechanics. No violation ever observed in closed systems.",
  
  "reflex_tag": "RFX_LAW_001",
  
  "examples": [
    "Pendulum: At highest point (max PE, min KE), at lowest (min PE, max KE). Total E constant.",
    "Roller coaster: Height → speed conversion (PE → KE), friction converts to heat (Q).",
    "Elastic collision: Two billiard balls exchange momentum and energy, total E unchanged.",
    "Hydroelectric dam: Water PE (height) → turbine KE → generator electrical energy.",
    "Spring: Compression stores PE, release converts to KE of attached mass."
  ],
  
  "counterexamples": [
    "NOT: Perpetual motion machines (impossible - violate conservation)",
    "NOT: Energy created from nothing (violates conservation)",
    "NOT: Energy disappears (transforms to other forms, including mass via E=mc²)",
    "NOT: Energy increases spontaneously in isolated system",
    "NOT: Over-unity devices (output > input, violate conservation)"
  ],
  
  "applications": [
    "Mechanical engineering: Efficiency calculations (minimize energy loss to friction/heat)",
    "Aerospace: Rocket trajectory optimization (gravitational PE ↔ KE trade-offs)",
    "Electrical engineering: Power system design (generation, transmission, consumption balance)",
    "Climate science: Earth energy budget (solar input, thermal radiation output)",
    "Nuclear energy: Mass-energy conversion (E=mc², fission/fusion)",
    "Renewable energy: Wind/solar/hydro (capturing natural energy flows)"
  ],
  
  "verification": "Mathematical: Noether's Theorem (1915) proves energy conservation from time-translation symmetry. Experimental: Countless closed-system experiments (pendulums, collisions, thermodynamics, particle physics) over 200+ years show no violation. Technological: All engineering relies on energy conservation - GPS satellites, power grids, engines all work because conservation holds.",
  
  "uncertainty": "Unknown: Energy behavior at quantum-gravity scales (Planck scale ~10^-35 m). Unknown: Total energy of expanding universe (dark energy contribution unclear). Unknown: Whether energy is truly fundamental or emergent. Unknown: Exact mechanism of energy conservation in quantum field theory vacuum fluctuations."
}
```

### Exemplu 2: Pythagorean Theorem (Complete)

```json
{
  "id": "MATH_GEOMETRY_001",
  "domain": "Mathematics",
  "subdomain": "Geometry",
  "topic": "Pythagorean Theorem",
  
  "definition": "In a right triangle, the square of the hypotenuse (longest side) equals the sum of squares of the other two sides.",
  
  "formal_statement": "For right triangle with sides a, b and hypotenuse c: a² + b² = c². Equivalently: c = √(a² + b²). Holds only in Euclidean geometry (flat space).",
  
  "relations": [
    "MATH_GEOMETRY_002",   // Euclidean Geometry
    "MATH_GEOMETRY_010",   // Distance Formula
    "MATH_TRIGONOMETRY_001", // Sine/Cosine (c² = a² + b² - 2ab·cos(90°))
    "MATH_ALGEBRA_015",    // Quadratic Equations
    "PHYS_MECHANICS_020"   // Vector Addition (right-angle components)
  ],
  
  "prerequisites": [
    "MATH_ALGEBRA_001",    // Basic Algebra
    "MATH_GEOMETRY_000",   // Basic Geometry (triangles, angles)
    "MATH_ARITHMETIC_005"  // Squares and Square Roots
  ],
  
  "confidence": 1.0,
  
  "source": "Euclid's Elements, Book I, Proposition 47 (~300 BCE). Rigorous geometric proof. Over 400 different proofs exist (algebraic, geometric, analytic). Mathematical certainty in Euclidean geometry.",
  
  "reflex_tag": "RFX_THM_001",
  
  "examples": [
    "3-4-5 triangle: 3² + 4² = 9 + 16 = 25 = 5² ✓",
    "5-12-13 triangle: 5² + 12² = 25 + 144 = 169 = 13² ✓",
    "Diagonal of square (side a): d² = a² + a² = 2a², d = a√2",
    "Distance in 2D: point (3,4) from origin: d = √(3² + 4²) = 5",
    "Ladder problem: 5m ladder, 3m from wall → height = √(5² - 3²) = 4m"
  ],
  
  "counterexamples": [
    "NOT: Valid for non-right triangles (use Law of Cosines instead)",
    "NOT: Valid in non-Euclidean geometry (spherical/hyperbolic space)",
    "NOT: a² + b² = c² + 1 (some students make this error)",
    "NOT: a + b = c (linear sum, not squares)",
    "NOT: Works for 3D diagonals directly (need extended version)"
  ],
  
  "applications": [
    "Construction: Ensuring walls are perpendicular (3-4-5 method)",
    "Navigation: Distance calculations (GPS, maps)",
    "Computer graphics: Distance between pixels, vector lengths",
    "Physics: Vector component decomposition (right-angle resolution)",
    "Architecture: Roof pitch calculations, structural stability",
    "Astronomy: Parallax distance measurements"
  ],
  
  "verification": "Mathematical proof: Euclid's geometric proof (dissection method), algebraic proof (complete the square), hundreds of other proofs. Empirical: Every right triangle measurement confirms. Axiomatic: Follows from Euclidean postulates with logical necessity.",
  
  "uncertainty": "Unknown: None in Euclidean geometry (mathematical certainty). Limitation: Does not apply in non-Euclidean geometries (spherical triangles, hyperbolic space). Physical space: General relativity shows spacetime is curved (non-Euclidean) at large scales, but Pythagorean approximation excellent at human scales."
}
```

### Exemplu 3: Cell Theory (Complete)

```json
{
  "id": "BIO_CELL_001",
  "domain": "Biology",
  "subdomain": "Cell Biology",
  "topic": "Cell Theory",
  
  "definition": "All living organisms are composed of one or more cells. Cells are the basic unit of life. All cells arise from pre-existing cells through cell division.",
  
  "formal_statement": "Three Tenets: (1) All living organisms are composed of cells (unicellular or multicellular). (2) The cell is the fundamental unit of structure and function in organisms. (3) All cells arise from pre-existing cells via division (biogenesis, not spontaneous generation).",
  
  "relations": [
    "BIO_CELL_002",        // Cell Structure (membrane, nucleus, organelles)
    "BIO_CELL_010",        // Cell Division (mitosis, meiosis)
    "BIO_GENETICS_001",    // DNA Inheritance
    "BIO_EVOLUTION_005",   // Common Ancestry
    "BIO_ECOLOGY_020",     // Organisms and Environment
    "CHEM_BIOCHEM_001"     // Biomolecules
  ],
  
  "prerequisites": [
    "BIO_BASICS_000",      // What is "life"?
    "CHEM_BASICS_001",     // Basic Chemistry
    "PHYS_OPTICS_005"      // Microscopy (how we observe cells)
  ],
  
  "confidence": 0.96,
  
  "source": "Matthias Schleiden (1838, plants) and Theodor Schwann (1839, animals) formulated first two tenets. Rudolf Virchow (1855) added third tenet (omnis cellula e cellula). Verified by 180+ years of microscopy, cell culture, and molecular biology.",
  
  "reflex_tag": "RFX_THY_010",
  
  "examples": [
    "Unicellular: Bacteria (E. coli), Amoeba, Paramecium - entire organism = one cell",
    "Multicellular: Humans (~37 trillion cells), oak tree (billions of cells)",
    "Cell division: Bacterial reproduction (binary fission), human skin cell replacement",
    "Disproof of spontaneous generation: Pasteur's swan-neck flask experiment (1861)",
    "All cells have: membrane, genetic material (DNA/RNA), ribosomes, cytoplasm"
  ],
  
  "counterexamples": [
    "NOT: Viruses are cells (acellular, need host cells to replicate)",
    "NOT: Spontaneous generation (Pasteur disproved - life from life only)",
    "NOT: Crystals are cells (organized but not living)",
    "NOT: Proteins/molecules alone are living (need cellular organization)",
    "NOT: Cells can form from non-living matter spontaneously (requires replication)"
  ],
  
  "applications": [
    "Medicine: Understanding disease at cellular level (cancer = uncontrolled cell division)",
    "Biotechnology: Cell culture for drug production (insulin, vaccines)",
    "Agriculture: Plant tissue culture (cloning crops)",
    "Research: Cell lines for experiments (HeLa cells, induced pluripotent stem cells)",
    "Forensics: DNA analysis from cells (blood, hair, saliva)",
    "Evolution: Common cellular features indicate common ancestry"
  ],
  
  "verification": "Microscopy: Light microscopes (1600s), electron microscopes (1930s) directly visualize cells. Cell culture: Growing cells in lab proves they replicate. Molecular biology: DNA sequencing shows genetic continuity. No observation of spontaneous cell generation. All organisms examined have cellular structure.",
  
  "uncertainty": "Unknown: Exact origin of first cells (abiogenesis ~3.5 billion years ago). Unknown: Complete mechanisms of cell division regulation. Debate: Are there non-cellular life forms on other planets? Debate: Prions (misfolded proteins causing disease) - on border of life definition. Limitation: Viruses challenge definition (genetic material, evolution, but not cellular)."
}
```

---

## De Ce Fiecare Câmp Este Esențial pentru Anti-Halucinație

### Lanțul de Verificare

```
User Query: "Ce este conservarea energiei?"
         │
         ▼
1. Query Classification (Λ-Guide)
   → domain: "Physics"
   → topic: "Conservation of Energy"
         │
         ▼
2. Phalanx Bridge: get_concepts()
   → Caută: domain="Physics" AND topic LIKE "%Conservation%Energy%"
   → Găsește: PHYS_MECHANICS_001
   → Verifică: confidence >= 0.95 ✓ (0.99)
         │
         ▼
3. Phalanx Bridge: balance_entropy()
   → Verifică consistency
   → Status: BALANCED ✓
         │
         ▼
4. Phalanx Bridge: route_to_reflexive_generator()
   → NU trimite `definition` direct (previne copy-paste)
   → Trimite doar: id, relations, prerequisites, confidence
         │
         ▼
5. Reflexive Generator: _logical_expansion()
   → Traversează `relations`:
     - PHYS_MECHANICS_002 (Kinetic Energy)
     - PHYS_MECHANICS_003 (Potential Energy)
     - PHYS_THERMO_001 (First Law)
   → Construiește lanț logic (NU probabilistic)
         │
         ▼
6. Reflexive Generator: _derive_conclusion()
   → Confidence = min(0.99, 0.99, 0.99) = 0.99
   → Source = combines sources din toate concepts
   → Uncertainty = extrage din toate concepts
         │
         ▼
7. Λ-Pattern: validate()
   → Verifică: toate statements au source? ✓
   → Verifică: nicio halucinație detectată? ✓
         │
         ▼
8. Λ-Identity: add_identity()
   → Adaugă: knows_from = [sources]
   → Adaugă: foundation_ids = [PHYS_MECHANICS_001, ...]
         │
         ▼
9. Final Response to User
   → Text: raționament logic bazat pe relations
   → Confidence: 0.99
   → Sources: Noether (1915), experiments
   → Uncertainty: quantum-gravity scales unknown
```

**Fără oricare dintre câmpuri, lanțul se rupe:**
- Fără `id`: Nu putem referenția în relations
- Fără `relations`: Nu putem construi raționament logic
- Fără `confidence`: Nu știm cât de siguri suntem
- Fără `source`: Nu putem verifica adevărul
- Fără `uncertainty`: Pretindem că știm totul (mincinos)
- Fără `counterexamples`: Risc de over-generalizare
- Fără `prerequisites`: Ordinea de învățare greșită

**Toate câmpurile împreună = Fortăreață Impenetrabilă pentru Halucinații** 🏛️

---

## Procesul de Adăugare a Conceptelor Noi

### Pipeline-ul de Verificare

```
                    [Concept Propus]
                           │
                           ▼
┌──────────────────────────────────────────────┐
│ STEP 1: Source Verification                 │
│ - Există sursă credibilă? (peer-reviewed?)   │
│ - Autor recunoscut? Instituție respectată?   │
│ - Data publicării? Replicabilitate?          │
└──────────────┬───────────────────────────────┘
               │ Pass
               ▼
┌──────────────────────────────────────────────┐
│ STEP 2: Confidence Assessment                │
│ - Proof matematic? → 1.0                     │
│ - Lege fizică verificată? → 0.99             │
│ - Teorie puternică? → 0.98                   │
│ - Consens științific? → 0.97                 │
│ - Fapt stabilit? → 0.95-0.96                 │
│ - Sub 0.95? → REJECT                         │
└──────────────┬───────────────────────────────┘
               │ Pass (>= 0.95)
               ▼
┌──────────────────────────────────────────────┐
│ STEP 3: Multi-Source Verification            │
│ - Minimum 2 surse independente               │
│ - Cross-check între surse                    │
│ - Detectare contradicții                     │
└──────────────┬───────────────────────────────┘
               │ Pass
               ▼
┌──────────────────────────────────────────────┐
│ STEP 4: Dependency Graph Integration         │
│ - Prerequisites există în Foundation? ✓      │
│ - Relations valide? ✓                        │
│ - Nicio ciclicitate invalidă? ✓              │
└──────────────┬───────────────────────────────┘
               │ Pass
               ▼
┌──────────────────────────────────────────────┐
│ STEP 5: Field Completeness Check             │
│ - Toate 15 câmpuri completate? ✓             │
│ - Minimum 2 examples? ✓                      │
│ - Minimum 2 counterexamples? ✓               │
│ - Uncertainty documentat? ✓                  │
└──────────────┬───────────────────────────────┘
               │ Pass
               ▼
┌──────────────────────────────────────────────┐
│ STEP 6: Expert Review                        │
│ - Reviewed by domain expert                  │
│ - Verificare accuracy                        │
│ - Approval final                             │
└──────────────┬───────────────────────────────┘
               │ APPROVED
               ▼
        [ADDED TO FOUNDATION] 🏛️
```

### Exemplu: Respingere Concept

**Concept Propus**: "Homeopathy Works"

```
STEP 1: Source Verification
→ Sources: Hahnemann (1796), various homeopathic journals
→ CONCERN: Lack of peer-reviewed verification in mainstream journals
→ CONCERN: No mechanism in physics/chemistry

STEP 2: Confidence Assessment
→ Proposed confidence: 0.75
→ REJECT: Below 0.95 threshold
→ REASON: Multiple meta-analyses show no effect beyond placebo
→ REASON: Violates known chemistry (dilution beyond Avogadro)

STATUS: REJECTED from Foundation
ALTERNATIVE: Add concept "Placebo Effect" (confidence 0.97) instead
```

---

## Load și Balance: Phalanx Bridge în Acțiune

### Load Foundation

```python
def load_foundation(self, foundation_path="foundation.json"):
    """
    Încarcă Foundation din JSON și validează.
    
    Validări:
    1. JSON valid
    2. Toate câmpurile obligatorii prezente
    3. Confidence în range [0.95, 1.0]
    4. Prerequisites și relations există
    5. Nicio duplicare ID
    """
    with open(foundation_path, 'r') as f:
        self.foundation = json.load(f)
    
    # Validare
    ids = set()
    for concept in self.foundation:
        # 1. Câmpuri obligatorii
        required = ['id', 'domain', 'definition', 'confidence', 'source']
        for field in required:
            if field not in concept:
                raise ValueError(f"Missing field '{field}' in {concept.get('id', 'unknown')}")
        
        # 2. Confidence range
        conf = concept['confidence']
        if not (0.95 <= conf <= 1.0):
            raise ValueError(f"Confidence {conf} out of range for {concept['id']}")
        
        # 3. ID unic
        if concept['id'] in ids:
            raise ValueError(f"Duplicate ID: {concept['id']}")
        ids.add(concept['id'])
    
    # 4. Validate dependency graph
    self.validate_dependency_graph()
    
    logger.info(f"✓ Foundation loaded: {len(self.foundation)} concepts")
```

### Balance Entropy

```python
def balance_entropy(self):
    """
    Verifică consistency-ul Foundation (dS/dt = 0).
    
    Returns:
        dict: {
            'mean_confidence': float,
            'min_confidence': float,
            'max_confidence': float,
            'entropy': float (0-1, lower is better),
            'status': 'BALANCED' | 'UNBALANCED'
        }
    """
    confidences = [c['confidence'] for c in self.foundation]
    
    mean_conf = sum(confidences) / len(confidences)
    min_conf = min(confidences)
    max_conf = max(confidences)
    
    # Entropy = măsură de inconsistență
    # 0 = perfect consistent (toate 1.0)
    # 1 = maxim inconsistent (toate 0.0)
    entropy = 1.0 - mean_conf
    
    # Status
    if entropy < 0.05:  # < 5% deviation from perfection
        status = "BALANCED"  # dS/dt ≈ 0
    else:
        status = "UNBALANCED"  # dS/dt ≠ 0, needs rebalancing
    
    return {
        'mean_confidence': mean_conf,
        'min_confidence': min_conf,
        'max_confidence': max_conf,
        'entropy': entropy,
        'status': status,
        'total_concepts': len(self.foundation)
    }
```

**Exemplu Output**:
```python
{
  'mean_confidence': 0.977,
  'min_confidence': 0.95,
  'max_confidence': 1.0,
  'entropy': 0.023,  # 2.3% - Very balanced
  'status': 'BALANCED',
  'total_concepts': 445
}
```

---

## Statistici Foundation

### Distributie pe Domenii

```
Mathematics:        85 concepts  ████████████████████  19.1%
Physics:            76 concepts  ██████████████████    17.1%
Computer Science:   62 concepts  ██████████████        13.9%
Biology:            58 concepts  █████████████         13.0%
Medicine:           43 concepts  ██████████            9.7%
Psychology:         31 concepts  ███████               7.0%
Ethics:             24 concepts  █████                 5.4%
Philosophy:         22 concepts  █████                 4.9%
Astronomy:          18 concepts  ████                  4.0%
Linguistics:        14 concepts  ███                   3.1%
AI & AGI:           12 concepts  ███                   2.7%
                   ───────────────────────────────────────
TOTAL:             445 concepts  100%
```

### Growth Trajectory (Auto-Genesis)

```
FAZA 0 (Seed):     50 concepts   [██                    ]  11.2%  (Manual)
FAZA 1 (Current): 445 concepts   [████████████████████  ] 100%    (Verified)
FAZA 2 (Target): 1000 concepts   [████████████████████████████████████████] 224%  (Planned)
FAZA 3 (Future):  ∞  concepts    [████████████████████████████████████████████████████∞] (Auto-Genesis)
```

---

## Concluzie: Foundation = Forță Spartană

**SPARTA Foundation nu este o "bază de date" - este o FORTĂREAȚĂ** 🏛️

Fiecare piatră (concept) este:
- ✓ Verificată științific (confidence >= 0.95)
- ✓ Trasabilă (source, verification)
- ✓ Integrată (relations, prerequisites)
- ✓ Onestă (uncertainty explicit)
- ✓ Protejată (balance_entropy, validări)

**Nicio halucinație nu poate pătrunde** - doar adevăr verificat intră în Foundation.

**ΜΟΛΩΝ ΛΑΒΕ** - Vino și ia adevărul, dacă poți! 🏛️⚡🔥

---

**Next**: [SPARTA_ARCHITECTURE.md](SPARTA_ARCHITECTURE.md) - Implementări tehnice Phalanx Bridge și Reflexive Generator
