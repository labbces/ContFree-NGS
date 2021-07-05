from collections import defaultdict

def createList(kraken):
    kraken_dict = defaultdict(list) 
    with open(kraken) as kraken_file:
        for line in kraken_file:
            k = line.split()[1]
            v = line.split()[2]
            kraken_dict[k].append(v)
    return kraken_dict

kraken_1 = createList("kraken_1.txt")
kraken_2 = createList("kraken_2.txt")

#print(kraken_1)
#print(kraken_2)

mesmo_taxon = 0
taxon_diferentes = 0
for i in kraken_1.keys():
    if kraken_1[i] == kraken_2[i]:
        mesmo_taxon += 1
    else:
        taxon_diferentes += 1

print("mesmo taxons: {}".format(mesmo_taxon))
print("taxons diferentes: {}".format(taxon_diferentes))
