# Trigger Arc Travelling Salesman Problem (TATSP)

Ky projekt implementon **Trigger Arc TSP**, një variant i problemit klasik të Travelling Salesman Problem (TSP), i prezantuar në kuadër të **Metaheuristics Summer School Competition (MESS 2024)**.

## Përshkrimi i problemit

Jepet një graf i orientuar \( G = (N, A) \) me nyje dhe harkë me kosto pozitive. Për çdo hark mund të ekzistojnë **relacione trigger–target**:

- Nëse harku **trigger** përdoret, harku **target** merr një kosto të re.
- Vetëm **trigger-i i fundit** para përdorimit të target-it është aktiv.
- Qëllimi është të gjendet një **Hamiltonian cycle** (tur që viziton çdo nyje një herë dhe kthehet në depot 0) me **koston minimale**.

Ky problem është i frymëzuar nga optimizimi i fazës së mbledhjes së artikujve në magazina me rafte kompaktues, por mund të aplikohet edhe në skenarë më kompleksë.

## Formati i instancës

Instancat janë file tekst (UTF-8) me strukturë:

1. Rreshti i parë:  
|N| |A| |R|
ku N = numri i nyjeve, A = numri i harkëve, R = numri i relacioneve.

2. Pasojnë A rreshta:  
arc_index from to cost

3. Pasojnë R rreshta:  
rel_index trig_idx trig_from trig_to targ_idx targ_from targ_to new_cost


Kostot duhet të jenë **pozitive**. Parser-i hedh `ValueError` nëse gjendet ndonjë kosto negative.

## Struktura e projektit

- **cost_eval.py** – llogaritja e kostos së turit duke marrë parasysh trigger-at.
- **tsp_solver.py** – parser për instancat, heuristika konstruktive (greedy), local search (2-opt, relocate), dhe iterated local search (ILS).
- **visualization.py** – vizualizim grafik i turit (pa printime, vetëm vizatim).
- **trigger_arc_tsp.py** – skripti kryesor për ekzekutim.
- **instance_generator.py** – gjeneron instanca të reja në formatin zyrtar.

## Ekzekutimi

Për të ekzekutuar solverin mbi një instancë:

**python trigger_arc_tsp.py instances/example.txt --time 30 --seed 42**

Për të gjeneruar një instancë të re:
**python instance_generator.py**

## Output

Në terminal shfaqet kostoja totale dhe rendi i turit me kostot reale pas aktivizimit të trigger-ave. 
Vizualizohet edhe grafiku i turit.

## Metaheuristika të përdorura

Greedy constructive: tur fillestar me nearest-neighbor.
Local Search: 2-opt dhe relocate.
Iterated Local Search (ILS): perturbim me double-bridge dhe përmirësim me local search.
Pranim probabilistik: pranon ndonjëherë zgjidhje më të dobët për të shmangur ngecjen në minimum lokal.


