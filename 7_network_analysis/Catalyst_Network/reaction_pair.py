import pandas as pd

filename = "extracted_SMILES_reaxys.csv"
df = pd.read_csv(filename,dtype = str)
rea_list = []
pro_list = []

for row in df[["ID","reaction","Catalysts"]].iterrows():
    rea_list.append([row[1]['ID'], row[1]['reaction'].split(">>")[0]
                    ,row[1]['Catalysts']])
    pro_list.append([row[1]['ID'], row[1]['reaction'].split(">>")[1]
                    ,row[1]['Catalysts']])
## get two lists of reactant/product with id and catalyst imformation

rxn = []
catalysts = []
final = pd.DataFrame({"reaction":rxn, "catalysts":catalysts})
final.to_csv("transformed_reactions.csv")
## create an empty file

cnt = 0
for [rxn_id1, rea, cata1] in rea_list:
    for [rxn_id2, pro , cata2] in pro_list:
        if (cata2.find('Ni') != -1 or cata2.find('nickel') != -1 or
            cata1.find('Ni') != -1 or cata1.find('nickel') != -1):
            if rea == pro: ## if the reactant is a product
                rxn.append(rxn_id2 + ">>" + rxn_id1)
                catalysts.append(cata2 + ">>" + cata1)
                cnt += 1
                if (cnt % 100 == 0):
                    final = pd.DataFrame({"reaction":rxn, 
                                          "catalysts":catalysts})
                    final.to_csv("transformed_reactions.csv", 
                                 mode = 'a',header = False)
                    rxn = []
                    catalysts = []
                    ## write to file for every 100 lines
            
            
final = pd.DataFrame({"reaction":rxn, "catalysts":catalysts})
final.to_csv("transformed_reactions.csv", mode = 'a',header = False)
## write to file for the rest lines
