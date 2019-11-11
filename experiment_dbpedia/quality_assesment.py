import json
from SPARQLWrapper import SPARQLWrapper, JSON
from experiment_dbpedia import util

# sparql query to get properties type [(dbo:) || (dbp:) || (foaf:) || (schema:)] of persons selected in @param query2
query3 = """
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dbr:<http://dbpedia.org/resource/>
    PREFIX dbo:<http://dbpedia.org/ontology/>
    PREFIX dbp:<http://dbpedia.org/property/>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX schema:<http://schema.org/>
    SELECT
     # COUNT(*) 
     ?person ?predicate ?object 
     # COUNT (DISTINCT ?predicate) 
     # DISTINCT
      WHERE 
    { 
        ?person ?predicate ?object. 
        FILTER( STRSTARTS(STR(?predicate),str(dbo:)) || STRSTARTS(STR(?predicate),str(dbp:)) || STRSTARTS(STR(?predicate),str(foaf:)) || STRSTARTS(STR(?predicate),str(schema:)) ) 
        FILTER (?person IN (dbr:Alice_Walker,dbr:Duduka_da_Fonseca,dbr:Zack_Addy, dbr:Paulie_Pennino , dbr:Cornelia_\(wife_of_Caesar\) , dbr:Aloysius_Lilius, dbr:Julius_Caesar, dbr:James_Gosling, dbr:Lionel_Messi ))
    }
"""

query4 = """
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dbr:<http://dbpedia.org/resource/>
    PREFIX dbo:<http://dbpedia.org/ontology/>
    PREFIX dbp:<http://dbpedia.org/property/>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX schema:<http://schema.org/>
    SELECT
     # COUNT(*) 
     ?person ?predicate ?object 
     # COUNT (DISTINCT ?predicate) 
     # DISTINCT
      WHERE 
    { 
        ?person ?predicate ?object. 
         FILTER( STRSTARTS(STR(?predicate),str(dbo:)) || STRSTARTS(STR(?predicate),str(dbp:)) || STRSTARTS(STR(?predicate),str(foaf:)) || STRSTARTS(STR(?predicate),str(schema:)) ) 
        FILTER (?person IN (dbr:Abdelkader_Ghezzal,dbr:Riyad_Mahrez,dbr:Scott_Stevens, dbr:Scott_Stevens_\(footballer\) , dbr:George_W._Bush , dbr:Mohamed_Morsi, dbr:Bassem_Youssef, dbr:Tarek_El_Kazzaz, dbr:Enrique_Iglesias ))
    }
"""

synonyms_triples = {}

with open('result.json') as json_file:
    data = json.load(json_file)
    for key in data:
        # print(key, data[key])
        synonyms_triples[key] = list()


def triple_has_synonyms(pred_string):
    prd_str = pred_string.lower()
    for item in data:
        if (prd_str == item) or (prd_str in data[item]):
            return [True, item]
    return [False, '']


def compare_triple_get_case(triple1, triple2):
    subject_1 = triple1[0]
    predicate_1 = triple1[1]
    object_1 = triple1[2]

    subject_2 = triple2[0]
    predicate_2 = triple2[1]
    object_2 = triple2[2]

    # CASE_01 same subject same object => Duplicate triple
    if subject_1 == subject_2 and object_1 == object_2:
        return 'CASE_01'

    # CASE_02 same subject different object => Duplicate predicate | inaccurate value
    if subject_1 == subject_2 and object_1 != object_2:
        return 'CASE_02'

    if predicate_1 != predicate_2:
        # CASE_03 different subject same object => Duplicate predicate | possible inaccurate value (exp: unique ID)
        if subject_1 != subject_2 and object_1 == object_2:
            return 'CASE_03'

        # CASE_04 different subject different object => Duplicate predicate
        if subject_1 != subject_2 and object_1 != object_2:
            return 'CASE_04'
    return 'NOT_DEFINED'


sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(query3)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# processing results type [Triple]
# fetch the results
results_vars = results['head']['vars']
for result in results['results']['bindings']:
    subject_ = util.replace_uri_by_prefix(result[results_vars[0]]['value'])
    predicate_ = util.replace_uri_by_prefix(result[results_vars[1]]['value'])
    object_ = util.replace_uri_by_prefix(result[results_vars[2]]['value'])
    predicate_string = predicate_.split(':')[1]
    THS = triple_has_synonyms(predicate_string)
    if THS[0]:
        synonyms_triples[THS[1]].append([subject_, predicate_, object_])
# ./ end processing results type [Triple]
VALID_CASES = ['CASE_03']
ERRORS_CASE_01 = 0
ERRORS_CASE_02 = 0
ERRORS_CASE_03 = 0
ERRORS_CASE_04 = 0
for e in synonyms_triples:
    print(e)
    ST = synonyms_triples[e]
    ST_len = len(ST)
    predicates_case_04 = []
    triples_case_02 = {}
    triples_case_01 = {}
    # print(ST_len)
    # print(ST)
    if ST_len > 1:
        i = 0
        while i < ST_len - 1:
            for j in range(1, ST_len):
                if j > i:
                    CASE = compare_triple_get_case(ST[i], ST[j])
                    if CASE in VALID_CASES:
                        print(ST[i], ' <---> ', ST[j], '  [', CASE, '] ')
                    elif CASE == 'CASE_04':
                        case_04_prd_01 = ST[i][1]
                        case_04_prd_02 = ST[j][1]

                        if case_04_prd_01 not in predicates_case_04 and case_04_prd_02 not in predicates_case_04:
                            predicates_case_04.append(case_04_prd_01)
                            predicates_case_04.append(case_04_prd_02)
                            # print('PRD_CASE_04', predicates_case_04)
                            ERRORS_CASE_04 += 1
                            print(ST[i], ' <---> ', ST[j], '  [', CASE, '] ')

                        if case_04_prd_01 not in predicates_case_04 and case_04_prd_02 in predicates_case_04:
                            predicates_case_04.append(case_04_prd_01)
                            # predicates_case_04.append(case_04_prd_02)
                            ERRORS_CASE_04 += 1
                            print(ST[i], ' <---> ', ST[j], '  [', CASE, '] ')

                        if case_04_prd_01 in predicates_case_04 and case_04_prd_02 not in predicates_case_04:
                            # predicates_case_04.append(case_04_prd_01)
                            predicates_case_04.append(case_04_prd_02)
                            ERRORS_CASE_04 += 1
                            print(ST[i], ' <---> ', ST[j], '  [', CASE, '] ')
                    elif CASE == 'CASE_02':
                        subject__ = ST[i][0]
                        if subject__ in triples_case_02:
                            if ST[i] not in triples_case_02[subject__]:
                                triples_case_02[subject__].append(ST[i])
                            if ST[j] not in triples_case_02[subject__]:
                                triples_case_02[subject__].append(ST[j])
                        else:
                            triples_case_02[subject__] = []
                            triples_case_02[subject__].append(ST[i])
                            triples_case_02[subject__].append(ST[j])
                    elif CASE == 'CASE_01':
                        subject__ = ST[i][0]
                        if subject__ in triples_case_01:
                            if ST[i] not in triples_case_01[subject__]:
                                triples_case_01[subject__].append(ST[i])
                            if ST[j] not in triples_case_01[subject__]:
                                triples_case_01[subject__].append(ST[j])
                        else:
                            triples_case_01[subject__] = []
                            triples_case_01[subject__].append(ST[i])
                            triples_case_01[subject__].append(ST[j])

            i += 1

    for sbj in triples_case_01:
        print('[CASE_01]', sbj)
        ERRORS_CASE_01 += len(triples_case_01[sbj]) - 1
        print(len(triples_case_01[sbj]) - 1, triples_case_01[sbj])

    for sbj in triples_case_02:
        print('[CASE_02]', sbj)
        ERRORS_CASE_02 += len(triples_case_02[sbj]) - 1
        print(len(triples_case_02[sbj]) - 1, triples_case_02[sbj])

print('CASE_04_ERRORS:', ERRORS_CASE_04)
print('CASE_02_ERRORS:', ERRORS_CASE_02)
print('CASE_01_ERRORS:', ERRORS_CASE_01)
