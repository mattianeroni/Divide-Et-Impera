import reader

from dei import DivideEtImpera
from algorithms import Shuffler, RandomSearch, TwoOpt, Greedy, BiasedRandomised, HybridTabuAnnealing

problems = tuple(reader.read_benchmark(f) for f in reader.filenames)

DEI = DivideEtImpera(Shuffler(), problems[0], p=30, max_split=500, base_node_id = 1, goback=True)
sol = DEI.exe()
print(sol.value, sol.delay)

DEI = DivideEtImpera(RandomSearch(), problems[0], p=30, max_split=500, base_node_id = 1, goback=True)
sol = DEI.exe()
print(sol.value, sol.delay)


DEI = DivideEtImpera(TwoOpt(), problems[0], p=30, max_split=500, base_node_id = 1, goback=True)
sol = DEI.exe()
print(sol.value, sol.delay)


DEI = DivideEtImpera(Greedy(), problems[0], p=30, max_split=500, base_node_id = 1, goback=True)
sol = DEI.exe()
print(sol.value, sol.delay)


DEI = DivideEtImpera(BiasedRandomised(), problems[0], p=30, max_split=500, base_node_id = 1, goback=True)
sol = DEI.exe()
print(sol.value, sol.delay)


#DEI = DivideEtImpera(HybridTabuAnnealing(tabusize=80), problems[0], p=30, max_split=500, base_node_id = 1, goback=True)
#sol = DEI.exe()
#print(sol.value, sol.delay)
