from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import wordnet as wn
import enchant
import json

# Processing options
options = {
    'Predicate': True,
    'Triple': False
}
# Virtuoso SPARQL query namespace prefixes
npDic = {
    "a": "http://www.w3.org/2005/Atom",
    "address": "http://schemas.talis.com/2005/address/schema#",
    "admin": "http://webns.net/mvcb/",
    "as": "http://www.w3.org/ns/activitystreams#",
    "atom": "http://atomowl.org/ontologies/atomrdf#",
    "aws": "http://soap.amazon.com/",
    "b3s": "http://b3s.openlinksw.com/",
    "batch": "http://schemas.google.com/gdata/batch",
    "bibo": "http://purl.org/ontology/bibo/",
    "bif": "bif:",
    "bugzilla": "http://www.openlinksw.com/schemas/bugzilla#",
    "c": "http://www.w3.org/2002/12/cal/icaltzd#",
    "campsite": "http://www.openlinksw.com/campsites/schema#",
    "cb": "http://www.crunchbase.com/",
    "cc": "http://web.resource.org/cc/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "cv": "http://purl.org/captsolo/resume-rdf/0.2/cv#",
    "cvbase": "http://purl.org/captsolo/resume-rdf/0.2/base#",
    "dawgt": "http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#",
    "dbc": "http://dbpedia.org/resource/Category:",
    "dbo": "http://dbpedia.org/ontology/",
    "dbp": "http://dbpedia.org/property/",
    "dbpedia-af": "http://af.dbpedia.org/resource/",
    "dbpedia-als": "http://als.dbpedia.org/resource/",
    "dbpedia-an": "http://an.dbpedia.org/resource/",
    "dbpedia-ar": "http://ar.dbpedia.org/resource/",
    "dbpedia-az": "http://az.dbpedia.org/resource/",
    "dbpedia-bar": "http://bar.dbpedia.org/resource/",
    "dbpedia-be": "http://be.dbpedia.org/resource/",
    "dbpedia-be-x-old": "http://be-x-old.dbpedia.org/resource/",
    "dbpedia-bg": "http://bg.dbpedia.org/resource/",
    "dbpedia-br": "http://br.dbpedia.org/resource/",
    "dbpedia-ca": "http://ca.dbpedia.org/resource/",
    "dbpedia-commons": "http://commons.dbpedia.org/resource/",
    "dbpedia-cs": "http://cs.dbpedia.org/resource/",
    "dbpedia-cy": "http://cy.dbpedia.org/resource/",
    "dbpedia-da": "http://da.dbpedia.org/resource/",
    "dbpedia-de": "http://de.dbpedia.org/resource/",
    "dbpedia-dsb": "http://dsb.dbpedia.org/resource/",
    "dbpedia-el": "http://el.dbpedia.org/resource/",
    "dbpedia-eo": "http://eo.dbpedia.org/resource/",
    "dbpedia-es": "http://es.dbpedia.org/resource/",
    "dbpedia-et": "http://et.dbpedia.org/resource/",
    "dbpedia-eu": "http://eu.dbpedia.org/resource/",
    "dbpedia-fa": "http://fa.dbpedia.org/resource/",
    "dbpedia-fi": "http://fi.dbpedia.org/resource/",
    "dbpedia-fr": "http://fr.dbpedia.org/resource/",
    "dbpedia-frr": "http://frr.dbpedia.org/resource/",
    "dbpedia-fy": "http://fy.dbpedia.org/resource/",
    "dbpedia-ga": "http://ga.dbpedia.org/resource/",
    "dbpedia-gd": "http://gd.dbpedia.org/resource/",
    "dbpedia-gl": "http://gl.dbpedia.org/resource/",
    "dbpedia-he": "http://he.dbpedia.org/resource/",
    "dbpedia-hr": "http://hr.dbpedia.org/resource/",
    "dbpedia-hsb": "http://hsb.dbpedia.org/resource/",
    "dbpedia-hu": "http://hu.dbpedia.org/resource/",
    "dbpedia-id": "http://id.dbpedia.org/resource/",
    "dbpedia-ie": "http://ie.dbpedia.org/resource/",
    "dbpedia-io": "http://io.dbpedia.org/resource/",
    "dbpedia-is": "http://is.dbpedia.org/resource/",
    "dbpedia-it": "http://it.dbpedia.org/resource/",
    "dbpedia-ja": "http://ja.dbpedia.org/resource/",
    "dbpedia-ka": "http://ka.dbpedia.org/resource/",
    "dbpedia-kk": "http://kk.dbpedia.org/resource/",
    "dbpedia-ko": "http://ko.dbpedia.org/resource/",
    "dbpedia-ku": "http://ku.dbpedia.org/resource/",
    "dbpedia-la": "http://la.dbpedia.org/resource/",
    "dbpedia-lb": "http://lb.dbpedia.org/resource/",
    "dbpedia-lmo": "http://lmo.dbpedia.org/resource/",
    "dbpedia-lt": "http://lt.dbpedia.org/resource/as",
    "dbpedia-lv": "http://lv.dbpedia.org/resource/a",
    "dbpedia-mk": "http://mk.dbpedia.org/resource/",
    "dbpedia-mr": "http://mr.dbpedia.org/resource/",
    "dbpedia-ms": "http://ms.dbpedia.org/resource/",
    "dbpedia-nah": "http://nah.dbpedia.org/resource/",
    "dbpedia-nds": "http://nds.dbpedia.org/resource/",
    "dbpedia-nl": "http://nl.dbpedia.org/resource/",
    "dbpedia-nn": "http://nn.dbpedia.org/resource/",
    "dbpedia-no": "http://no.dbpedia.org/resource/",
    "dbpedia-nov": "http://nov.dbpedia.org/resource/",
    "dbpedia-oc": "http://oc.dbpedia.org/resource/",
    "dbpedia-os": "http://os.dbpedia.org/resource/",
    "dbpedia-pam": "http://pam.dbpedia.org/resource/",
    "dbpedia-pl": "http://pl.dbpedia.org/resource/",
    "dbpedia-pms": "http://pms.dbpedia.org/resource/",
    "dbpedia-pnb": "http://pnb.dbpedia.org/resource/",
    "dbpedia-pt": "http://pt.dbpedia.org/resource/",
    "dbpedia-ro": "http://ro.dbpedia.org/resource/",
    "dbpedia-ru": "http://ru.dbpedia.org/resource/",
    "dbpedia-sh": "http://sh.dbpedia.org/resource/",
    "dbpedia-simple": "http://simple.dbpedia.org/resource/",
    "dbpedia-sk": "http://sk.dbpedia.org/resource/",
    "dbpedia-sl": "http://sl.dbpedia.org/resource/",
    "dbpedia-sq": "http://sq.dbpedia.org/resource/",
    "dbpedia-sr": "http://sr.dbpedia.org/resource/",
    "dbpedia-sv": "http://sv.dbpedia.org/resource/",
    "dbpedia-sw": "http://sw.dbpedia.org/resource/",
    "dbpedia-th": "http://th.dbpedia.org/resource/",
    "dbpedia-tr": "http://tr.dbpedia.org/resource/",
    "dbpedia-ug": "http://ug.dbpedia.org/resource/",
    "dbpedia-uk": "http://uk.dbpedia.org/resource/",
    "dbpedia-vi": "http://vi.dbpedia.org/resource/",
    "dbpedia-vo": "http://vo.dbpedia.org/resource/",
    "dbpedia-war": "http://war.dbpedia.org/resource/",
    "dbpedia-wikicompany": "http://dbpedia.openlinksw.com/wikicompany/",
    "dbpedia-wikidata": "http://wikidata.dbpedia.org/resource/",
    "dbpedia-yo": "http://yo.dbpedia.org/resource/",
    "dbpedia-zh": "http://zh.dbpedia.org/resource/",
    "dbpedia-zh-min-nan": "http://zh-min-nan.dbpedia.org/resource/",
    "dbr": "http://dbpedia.org/resource/",
    "dbt": "http://dbpedia.org/resource/Template:",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dct": "http://purl.org/dc/terms/",
    "digg": "http://digg.com/docs/diggrss/",
    "dul": "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl",
    "ebay": "urn:ebay:apis:eBLBaseComponents",
    "enc": "http://purl.oclc.org/net/rss_2.0/enc#",
    "exif": "http://www.w3.org/2003/12/exif/ns/",
    "fb": "http://api.facebook.com/1.0/",
    "ff": "http://api.friendfeed.com/2008/03",
    "fn": "http://www.w3.org/2005/xpath-functions/#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "freebase": "http://rdf.freebase.com/ns/",
    "g": "http://base.google.com/ns/1.0",
    "gb": "http://www.openlinksw.com/schemas/google-base#",
    "gd": "http://schemas.google.com/g/2005",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "geodata": "http://sws.geonames.org/",
    "geonames": "http://www.geonames.org/ontology#",
    "georss": "http://www.georss.org/georss/",
    "gml": "http://www.opengis.net/gml",
    "go": "http://purl.org/obo/owl/GO#",
    "hlisting": "http://www.openlinksw.com/schemas/hlisting/",
    "hoovers": "http://wwww.hoovers.com/",
    "hrev": "http:/www.purl.org/stuff/hrev#",
    "ical": "http://www.w3.org/2002/12/cal/ical#",
    "ir": "http://web-semantics.org/ns/image-regions",
    "itunes": "http://www.itunes.com/DTDs/Podcast-1.0.dtd",
    "ldp": "http://www.w3.org/ns/ldp#",
    "lgdt": "http://linkedgeodata.org/triplify/",
    "lgv": "http://linkedgeodata.org/vocabulary#",
    "link": "http://www.xbrl.org/2003/linkbase",
    "lod": "http://lod.openlinksw.com/",
    "math": "http://www.w3.org/2000/10/swap/math#",
    "media": "http://search.yahoo.com/mrss/",
    "mesh": "http://purl.org/commons/record/mesh/",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    "mf": "http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#",
    "mmd": "http://musicbrainz.org/ns/mmd-1.0#",
    "mo": "http://purl.org/ontology/mo/",
    "mql": "http://www.freebase.com/",
    "nci": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#",
    "nfo": "http://www.semanticdesktop.org/ontologies/nfo/#",
    "ng": "http://www.openlinksw.com/schemas/ning#",
    "nyt": "http://data.nytimes.com/",
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "obo": "http://www.geneontology.org/formats/oboInOwl#",
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "ogc": "http://www.opengis.net/",
    "ogcgml": "http://www.opengis.net/ont/gml#",
    "ogcgs": "http://www.opengis.net/ont/geosparql#",
    "ogcgsf": "http://www.opengis.net/def/function/geosparql/",
    "ogcgsr": "http://www.opengis.net/def/rule/geosparql/",
    "ogcsf": "http://www.opengis.net/ont/sf#",
    "oo": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0:",
    "openSearch": "http://a9.com/-/spec/opensearchrss/1.0/",
    "opencyc": "http://sw.opencyc.org/concept/",
    "opl": "http://www.openlinksw.com/schema/attribution#",
    "opl-gs": "http://www.openlinksw.com/schemas/getsatisfaction/",
    "opl-meetup": "http://www.openlinksw.com/schemas/meetup/",
    "opl-xbrl": "http://www.openlinksw.com/schemas/xbrl/",
    "oplweb": "http://www.openlinksw.com/schemas/oplweb#",
    "ore": "http://www.openarchives.org/ore/terms/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "product": "http://www.buy.com/rss/module/productV2/",
    "protseq": "http://purl.org/science/protein/bysequence/",
    "prov": "http://www.w3.org/ns/prov#",
    "r": "http://backend.userland.com/rss2",
    "radio": "http://www.radiopop.co.uk/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfa": "http://www.w3.org/ns/rdfa#",
    "rdfdf": "http://www.openlinksw.com/virtrdf-data-formats#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "rev": "http://purl.org/stuff/rev#",
    "review": "http:/www.purl.org/stuff/rev#",
    "rss": "http://purl.org/rss/1.0/",
    "sc": "http://purl.org/science/owl/sciencecommons/",
    "schema": "http://schema.org/",
    "scovo": "http://purl.org/NET/scovo#",
    "sd": "http://www.w3.org/ns/sparql-service-description#",
    "sf": "urn:sobject.enterprise.soap.sforce.com",
    "sioc": "http://rdfs.org/sioc/ns#",
    "sioct": "http://rdfs.org/sioc/types#",
    "skiresort": "http://www.openlinksw.com/ski_resorts/schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "slash": "http://purl.org/rss/1.0/modules/slash/",
    "sql": "sql:",
    "stock": "http://xbrlontology.com/ontology/finance/stock_market#",
    "twfy": "http://www.openlinksw.com/schemas/twfy#",
    "umbel": "http://umbel.org/umbel#",
    "umbel-ac": "http://umbel.org/umbel/ac/",
    "umbel-rc": "http://umbel.org/umbel/rc/",
    "umbel-sc": "http://umbel.org/umbel/sc/",
    "uniprot": "http://purl.uniprot.org/",
    "units": "http://dbpedia.org/units/",
    "usc": "http://www.rdfabout.com/rdf/schema/uscensus/details/100pct/",
    "v": "http://www.openlinksw.com/xsltext/",
    "vcard": "http://www.w3.org/2001/vcard-rdf/3.0#",
    "vcard2006": "http://www.w3.org/2006/vcard/ns#",
    "vi": "http://www.openlinksw.com/virtuoso/xslt/",
    "virt": "http://www.openlinksw.com/virtuoso/xslt",
    "virtcxml": "http://www.openlinksw.com/schemas/virtcxml#",
    "virtpivot": "http://www.openlinksw.com/schemas/virtpivot#",
    "virtrdf": "http://www.openlinksw.com/schemas/virtrdf#",
    "void": "http://rdfs.org/ns/void#",
    "wb": "http://www.worldbank.org/",
    "wdrs": "http://www.w3.org/2007/05/powder-s#",
    "wf": "http://www.w3.org/2005/01/wf/flow#",
    "wfw": "http://wellformedweb.org/CommentAPI/",
    "wiki-commons": "http://commons.wikimedia.org/wiki/",
    "wikidata": "http://www.wikidata.org/entity/",
    "wikipedia-en": "http://en.wikipedia.org/wiki/",
    "xf": "http://www.w3.org/2004/07/xpath-functions",
    "xfn": "http://gmpg.org/xfn/11#",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "xhv": "http://www.w3.org/1999/xhtml/vocab#",
    "xi": "http://www.xbrl.org/2003/instance",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xn": "http://www.ning.com/atom/1.0",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "xsl10": "http://www.w3.org/XSL/Transform/1.0",
    "xsl1999": "http://www.w3.org/1999/XSL/Transform",
    "xslwd": "http://www.w3.org/TR/WD-xsl",
    "y": "urn:yahoo:maps",
    "yago": "http://dbpedia.org/class/yago/",
    "yago-res": "http://yago-knowledge.org/resource/",
    "yt": "http://gdata.youtube.com/schemas/2007",
    "zem": "http://s.zemanta.com/ns#",
}

mini_np_dic = {
    "dbp:": "http://dbpedia.org/property/",
    "rdf:": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs:": "http://www.w3.org/2000/01/rdf-schema#",
    "owl:": "http://www.w3.org/2002/07/owl#",
    "dbo:": "http://dbpedia.org/ontology/",
    "foaf:": "http://xmlns.com/foaf/0.1/",
    "geo:": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "dct:": "http://purl.org/dc/terms/",
    "prov:": "http://www.w3.org/ns/prov#",
    "dc:": "http://purl.org/dc/elements/1.1/",
    "gold:": "http://purl.org/linguistics/gold/",
    "vrank:": "http://purl.org/voc/vrank#",
    "georss:": "http://www.georss.org/georss/",
    "/": "http://rdvocab.info/RDARelationshipsWEMI/",
    "dbr:": "http://dbpedia.org/resource/",
    "nodeid:": "nodeID://",
    "instances:": "http://www.w3.org/2006/03/wn/wn20/instances/",
    "docview:": "http://search.proquest.com/docview/",
    "en-wiki:": "http://en.wikipedia.org/wiki/",
    "wikimedia-file:": "http://commons.wikimedia.org/wiki/Special:FilePath/",
    "wikidata-entity:": "http://www.wikidata.org/entity/",
    "yago-res:": "http://yago-knowledge.org/resource/",
    "freebase:": "http://rdf.freebase.com/ns/",
    "dbr-es:": "http://es.dbpedia.org/resource/",
    "dbr-it:": "http://it.dbpedia.org/resource/",
    "dbr-fr:": "http://fr.dbpedia.org/resource/",
    "dbr-pt:": "http://pt.dbpedia.org/resource/",
    "dbr-nl:": "http://nl.dbpedia.org/resource/",
    "dbr-de:": "http://de.dbpedia.org/resource/",
    "dbr-ja:": "http://ja.dbpedia.org/resource/",
    "dbr-ko:": "http://ko.dbpedia.org/resource/",
    "dbr-eu:": "http://eu.dbpedia.org/resource/",
    "dbr-el:": "http://el.dbpedia.org/resource/",
    "dbr-cs:": "http://cs.dbpedia.org/resource/",
    "dbr-pl:": "http://pl.dbpedia.org/resource/",
    "dbr-id:": "http://id.dbpedia.org/resource/",
    "wikidata-dbr:": "http://wikidata.dbpedia.org/resource/",
    "d-nb:": "http://d-nb.info/gnd/",
    "viaf:": "http://viaf.org/viaf/",
    "sw:": "http://sw.cyc.com/concept/",
    "europe-names:": "http://data.europa.eu/euodp/jrc-names/",
    "bbc-things:": "http://www.bbc.co.uk/things/",
    "wiwiss-gut-people:": "http://www4.wiwiss.fu-berlin.de/gutendata/resource/people/",
    "wiwiss-res-people:": "http://www4.wiwiss.fu-berlin.de/dblp/resource/person/",
    "zitgist-artist:": "http://zitgist.com/music/artist/",
    "nytimes:": "http://data.nytimes.com/",
    "dbc-yago:": "http://dbpedia.org/class/yago/",
    "schema:": "http://schema.org/",
    "ont-owl:": "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#",
    "umbel-rc:": "http://umbel.org/umbel/rc/"
}

# Replace namespace URI by PREFIX
# Pending predicates []
predicates = []
uri_predicate_list = []


def replace_uri_by_prefix(uri_predicate, is_predicate=False):
    for prefix in mini_np_dic:
        if mini_np_dic[prefix] in uri_predicate:
            prefix_predicate = uri_predicate.replace(mini_np_dic[prefix], prefix)
            if is_predicate:
                uri_predicate_list.append(prefix_predicate)
                predicates.append(prefix_predicate.replace(prefix, '').lower())
            return prefix_predicate

    return uri_predicate


def union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


def is_matched_syn_sets(list1, list2):
    list1x2 = set(list1) & set(list2)
    if len(list1x2) > 0:
        return True
    return False


def char_list_to_int(list_char):
    for idx, item in enumerate(list_char):
        list_char[idx] = int(item)
    return list_char


sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# sparql query to get all properties related to the subject type PREFIX:Person
query1 = """
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo:<http://dbpedia.org/ontology/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX schema:<http://schema.org/>
    PREFIX dbr:<http://dbpedia.org/resource/>
    PREFIX xml:<http://www.w3.org/XML/1998/namespace>
    PREFIX dbp:<http://dbpedia.org/property/>
    SELECT
    DISTINCT ?predicate
    WHERE {
    ?person a ?o .
    ?person ?predicate ?object .
    FILTER (?o IN (foaf:Person, dbo:Person, schema:Person, wikidata:Q5 ) )
    }
    LIMIT 10100
"""

# sparql query to get properties of specific persons
# (dbr:Alice_Walker,    dbr:Duduka_da_Fonseca,  dbr:Zack_Addy,  dbr:Paulie_Pennino , dbr:Cornelia_\(wife_of_Caesar\),
# dbr:Aloysius_Lilius,  dbr:Julius_Caesar,      dbr:James_Gosling, dbr:Lionel_Messi )
query2 = """
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dbr:<http://dbpedia.org/resource/>
    SELECT 
     ?person ?predicate ?object
    WHERE  
    { 
        ?person ?predicate ?object. 
        FILTER (?person IN (dbr:Alice_Walker,dbr:Duduka_da_Fonseca,dbr:Zack_Addy, dbr:Paulie_Pennino , dbr:Cornelia_\(wife_of_Caesar\) , dbr:Aloysius_Lilius, dbr:Julius_Caesar, dbr:James_Gosling, dbr:Lionel_Messi ))
    }
"""

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
      ?predicate WHERE 
    { 
        ?person ?predicate ?object. 
        FILTER( STRSTARTS(STR(?predicate),str(dbo:)) || STRSTARTS(STR(?predicate),str(dbp:)) || STRSTARTS(STR(?predicate),str(foaf:)) || STRSTARTS(STR(?predicate),str(schema:)) ) 
        FILTER (?person IN (dbr:Alice_Walker,dbr:Duduka_da_Fonseca,dbr:Zack_Addy, dbr:Paulie_Pennino , dbr:Cornelia_\(wife_of_Caesar\) , dbr:Aloysius_Lilius, dbr:Julius_Caesar, dbr:James_Gosling, dbr:Lionel_Messi ))
    }
"""

# get distinct properties in @param query 3
query4 = """
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dbr:<http://dbpedia.org/resource/>
    PREFIX dbo:<http://dbpedia.org/ontology/>
    PREFIX dbp:<http://dbpedia.org/property/>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX schema:<http://schema.org/>
    SELECT
     # COUNT(*) 
     # ?person ?predicate ?object 
     # COUNT (DISTINCT ?predicate) 
      DISTINCT ?predicate 
     WHERE 
    { 
        ?person ?predicate ?object. 
        FILTER( STRSTARTS(STR(?predicate),str(dbo:)) || STRSTARTS(STR(?predicate),str(dbp:)) || STRSTARTS(STR(?predicate),str(foaf:)) || STRSTARTS(STR(?predicate),str(schema:)) ) 
        FILTER (?person IN (dbr:Alice_Walker,dbr:Duduka_da_Fonseca,dbr:Zack_Addy, dbr:Paulie_Pennino , dbr:Cornelia_\(wife_of_Caesar\) , dbr:Aloysius_Lilius, dbr:Julius_Caesar, dbr:James_Gosling, dbr:Lionel_Messi ))
    }
"""

sparql.setQuery(query4)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# processing results type [Predicate]
# fetch the results and replace each uri with specific prefix
# append a list of diff predicates labels @String values
# if options allow to process this type of dataset
suggestions_dictionary = enchant.Dict("en_US")
predicates_suggestions = []
candidate_synonyms = {}
candidate_synonyms_ = []
delete_from_candidate_synonyms = []
if options['Predicate']:
    for result in results["results"]["bindings"]:
        replace_uri_by_prefix(result["predicate"]["value"], True)

    print('size of predicates LIST: ', len(predicates), ' predicates')
    print('size of uri_predicate LIST: ', len(uri_predicate_list), ' uri_predicates')

    for index, predicate in enumerate(predicates):
        possible_predicate_synonyms = []
        predicate_suggested_corrections = []
        for syn in wn.synsets(predicate):
            for l in syn.lemmas():
                possible_predicate_synonyms.append(l.name())
        predicate_suggested_corrections = suggestions_dictionary.suggest(predicate)
        predicates_suggestions.append([predicate, union(possible_predicate_synonyms, predicate_suggested_corrections)])
        # count = predicates.count(predicate)
        # if count > 1:
        #     print('[ ', uri_predicate_list[index], index, ' <:::> ', count, ' ]')

    # for index, uri_pre in enumerate(uri_predicate_list):
    #     print(index, type(index))
    #     print(index, uri_pre, predicates_suggestions[index])

    # print(predicates_suggestions[0])
    predicates_suggestions_legnth = len(predicates_suggestions)
    # print('predicates_suggestions_legnth>>', predicates_suggestions_legnth, type(predicates_suggestions))
    # predicates_suggestions = enumerate(predicates_suggestions)
    # print('after enumarate, ', type(predicates_suggestions))

    comparison_possibilities = 0
    if predicates_suggestions_legnth > 1:
        # for index, pre_sugg in enumerate(predicates_suggestions):
        #     print(pre_sugg)
        i = 0
        # print(predicates_suggestions_legnth[0])
        while i < predicates_suggestions_legnth - 1:
            # print(predicates_suggestions[i])
            for j in range(1, predicates_suggestions_legnth):
                if j > i:
                    # print(predicates_suggestions[j])
                    matching = is_matched_syn_sets(predicates_suggestions[i][1], predicates_suggestions[j][1])
                    if matching:
                        candidate_synonyms_.append([predicates_suggestions[i][0], predicates_suggestions[j][0]])
                        if predicates_suggestions[i][0] in candidate_synonyms:
                            if predicates_suggestions[j][0] not in candidate_synonyms[predicates_suggestions[i][0]]:
                                candidate_synonyms[predicates_suggestions[i][0]].append(predicates_suggestions[j][0])
                        else:
                            candidate_synonyms[predicates_suggestions[i][0]] = list()
                            candidate_synonyms[predicates_suggestions[i][0]].append(predicates_suggestions[j][0])
                        comparison_possibilities += 1
            i += 1
    print('number of comparison possibilities', comparison_possibilities)
    print('synonyms tuples list', len(candidate_synonyms))

    # for item in candidate_synonyms_:
    #     print(item)

    for index, cand_syn in enumerate(candidate_synonyms):
        print(cand_syn)
        indexes = []
        for index_, syn in enumerate(candidate_synonyms[cand_syn]):
            indexes.append(index_)
            print(index_, syn)
        SELECTED = input("select the valid synonyms  by number, separated by a comma [1,2] , put [-1] for None of them:")
        SELECTED = char_list_to_int(SELECTED.split(','))
        # print(set(char_list_to_int(SELECTED.split(','))) & set(indexes))
        remove_indices = [e for e in indexes if e not in SELECTED]
        print(remove_indices)
        selected_syn = [i for j, i in enumerate(candidate_synonyms[cand_syn]) if j not in remove_indices]
        if len(selected_syn) == 0:
            delete_from_candidate_synonyms.append(cand_syn)
            # del candidate_synonyms[cand_syn]
        else:
            candidate_synonyms[cand_syn] = selected_syn
        # print(candidate_synonyms[cand_syn])
    # Remove multiple keys from dictionary
    [candidate_synonyms.pop(key) for key in delete_from_candidate_synonyms]

    with open('result.json', 'w') as json_file:
        json.dump(candidate_synonyms, json_file)

    for idx_, cand_syn_ in enumerate(candidate_synonyms):
        print(cand_syn_)
        print(candidate_synonyms[cand_syn_])
# ./end processing results type [Predicate]
# processing results type [Triple]
# fetch the results
if options['Triple']:
    results_vars = results['head']['vars']
    for result in results['results']['bindings']:
        print('( ', replace_uri_by_prefix(result[results_vars[0]]['value']), ' , ',
              replace_uri_by_prefix(result[results_vars[1]]['value'], True), ' , ',
              replace_uri_by_prefix(result[results_vars[2]]['value']), ' )')
# ./ end processing results type [Triple]
