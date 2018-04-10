'''
Copyright 2014-2017 EMBL - European Bioinformatics Institute, Wellcome
Trust Sanger Institute and GlaxoSmithKline

This software was developed as part of the Centre for Therapeutic
Target Validation (CTTV)  project. For more information please see:

        http://targetvalidation.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from __future__ import absolute_import, print_function
from nose.tools.nontrivial import with_setup
import sys
import json
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
import datetime
import opentargets.model.core as opentargets
import opentargets.model.bioentity as bioentity
import opentargets.model.evidence.core as evidence_core
import opentargets.model.evidence.genetics as evidence_genetics
import opentargets.model.evidence.association_score as evidence_score
import opentargets.model.evidence.phenotype as evidence_phenotype
import opentargets.model.evidence.linkout as evidence_linkout

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2017, The Centre for Therapeutic Target Validation (CTTV)"
__credits__ = ["Gautier Koscielny", "Samiul Hasan", "Michael Maguire"]
__license__ = "Apache 2.0"
__version__ = "1.2.8"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"

def setup_module(module):
    print ("") # this is to get a newline after the dots
    print ("setup_module before anything in this file")
 
def teardown_module(module):
    print ("teardown_module after everything in this file")
 
def my_setup_function():
    print ("my_setup_function")
 
def my_teardown_function():
    print ("my_teardown_function")
 
@with_setup(my_setup_function, my_teardown_function)
def test_base_exists():
    obj = opentargets.Base()
    assert not obj == None
    
@with_setup(my_setup_function, my_teardown_function)
def test_genetics_exists():
    obj = opentargets.Genetics()
    assert not obj == None
    
@with_setup(my_setup_function, my_teardown_function)
def test_animal_models_exists():
    obj = opentargets.Animal_Models()
    assert not obj == None

@with_setup(my_setup_function, my_teardown_function)
def test_expression_exists():
    obj = opentargets.Expression()
    assert not obj == None
    
@with_setup(my_setup_function, my_teardown_function)
def test_drug_exists():
    obj = opentargets.Drug()
    assert not obj == None

@with_setup(my_setup_function, my_teardown_function)
def test_literature_curated_exists():
    obj = opentargets.Literature_Curated()
    assert not obj == None

@with_setup(my_setup_function, my_teardown_function)
def test_literature_mining_exists():
    obj = opentargets.Literature_Mining()
    assert not obj == None

@with_setup(my_setup_function, my_teardown_function)
def test_base_create_and_clone():
    obj = opentargets.Base()
    obj.access_level = "public"
    obj.sourceID = "opentargets"
    obj.validated_against_schema_version = "1.2.8"
    # create a target
    obj.target = bioentity.Target(
        id="http://identifiers.org/ensembl/ENSG00000213724",
        activity="http://identifiers.org/cttv.activity/predicted_damaging",
        target_type="http://identifiers.org/cttv.target/gene_evidence")
    obj.disease = bioentity.Disease(id="http://www.ebi.ac.uk/efo/EFO_0003767")
    errors = obj.validate(logger)
    assert obj is not None and errors == 0

    # try to serialize
    obj.serialize()
    str = obj.to_JSON(indentation=None)


@with_setup(my_setup_function, my_teardown_function)
def test_genomics_englad_create_and_clone():
    print("test_genomics_englad_create_and_clone")
    obj = opentargets.Literature_Curated(type='genetic_literature')
    obj.access_level = "public"
    obj.sourceID = "genomics_england"
    obj.validated_against_schema_version = "1.2.8"
    obj.unique_association_fields = dict(
        target="http://identifiers.org/ensembl/ENSG00000213724",
        object="http://www.ebi.ac.uk/efo/EFO_0003767",
        variant="http://identifiers.org/dbsnp/rs11010067",
        study_name="cttv009_gwas_catalog",
        pvalue="2.000000039082963e-25",
        pubmed_refs="http://europepmc.org/abstract/MED/23128233")

    # create target, disease and variant
    obj.target = bioentity.Target(
        id="http://identifiers.org/ensembl/ENSG00000213724",
        activity="http://identifiers.org/cttv.activity/predicted_damaging",
        target_type="http://identifiers.org/cttv.target/gene_evidence")
    obj.disease = bioentity.Disease(id="http://www.ebi.ac.uk/efo/EFO_0003767")

    publications = None
    single_lit_ref_list = list()
    if publications is not None:
        publications = re.findall(r"\'(.+?)\'", str(publications))
        if len(publications) > 0:
            for paper_set in publications:
                paper_set = re.findall(r"\d{7,12}", paper_set)
                for paper in paper_set:
                    lit_url = "http://europepmc.org/abstract/MED/" + paper
                    single_lit_ref_list.append(evidence_core.Single_Lit_Reference(lit_id=lit_url))
        else:
            print("no publication found for %s %s %s" % (panel_name, panel_id, publications))
            lit_url = "http://europepmc.org/abstract/MED/00000000"
            single_lit_ref_list.append(evidence_core.Single_Lit_Reference(lit_id=lit_url))

    provenance_type = evidence_core.BaseProvenance_Type(
        database=evidence_core.BaseDatabase(
            id="Genomics England PanelApp",
            version='v4.1',
            dbxref=evidence_core.BaseDbxref(
                url="https://panelapp.genomicsengland.co.uk/",
                id="Genomics England PanelApp", version="v5.7")),
        literature=evidence_core.BaseLiterature(
            references=single_lit_ref_list
        )
    )

    d = provenance_type.serialize()
    print(json.dumps(d, indent=2))

    level_of_confidence = 'HighEvidence'
    resource_score = evidence_score.Probability(
        type="probability",
        method=evidence_score.Method(
            description="Further details in the Genomics England PanelApp.",
            reference="NA",
            url="https://panelapp.genomicsengland.co.uk"),
        value=0.5)

    now = datetime.datetime.now()

    obj.evidence = evidence_core.Literature_Curated()
    obj.evidence.is_associated = True
    obj.evidence.evidence_codes = ["http://purl.obolibrary.org/obo/ECO_0000205"]
    obj.evidence.provenance_type = provenance_type
    obj.evidence.date_asserted = now.isoformat()
    obj.evidence.provenance_type = provenance_type
    obj.evidence.resource_score = resource_score
    # specific
    linkout = evidence_linkout.Linkout(
        url="http://www.genomicsengland.co.uk/dummy",
        nice_name='Further details in the Genomics England PanelApp')

    d = linkout.serialize()
    print(json.dumps(d, indent=2))

    obj.evidence.urls = [linkout]
    d = obj.serialize()
    print(json.dumps(d, indent=2))
    errors = obj.validate(logger)

    assert not obj == None and errors == 0

    tojson = obj.to_JSON()


@with_setup(my_setup_function, my_teardown_function)
def test_genetics_create_and_clone():
    obj = opentargets.Genetics(type="genetic_association")
    obj.access_level = "public"
    obj.sourceID = "opentargets"
    obj.validated_against_schema_version = "1.2.8"
    obj.unique_association_fields = {
        "target": "http://identifiers.org/ensembl/ENSG00000213724",
        "object": "http://www.ebi.ac.uk/efo/EFO_0003767",
        "variant": "http://identifiers.org/dbsnp/rs11010067",
        "study_name": "cttv009_gwas_catalog",
        "pvalue": "2.000000039082963e-25",
        "pubmed_refs": "http://europepmc.org/abstract/MED/23128233" }

    # create target, disease and variant
    obj.target = bioentity.Target(
        id="http://identifiers.org/ensembl/ENSG00000213724",
        activity="http://identifiers.org/cttv.activity/predicted_damaging",
        target_type="http://identifiers.org/cttv.target/gene_evidence")
    obj.disease = bioentity.Disease(id="http://www.ebi.ac.uk/efo/EFO_0003767")
    obj.variant = bioentity.Variant(id="http://identifiers.org/dbsnp/rs11010067", type="snp single")
    obj.evidence = opentargets.GeneticsEvidence(
        variant2disease = evidence_genetics.Variant2Disease(  
            evidence_codes = ["http://purl.obolibrary.org/obo/ECO_0000205"], 
            unique_experiment_reference = "http://europepmc.org/abstract/MED/23128233", 
            provenance_type = evidence_core.BaseProvenance_Type(),
            date_asserted = "2015-05-11T11:46:09+00:00",
            resource_score = evidence_score.Pvalue(value = 2.000000039082963e-25),
            gwas_panel_resolution = 100000,
            gwas_sample_size = 200),
        gene2variant = evidence_genetics.Gene2Variant( 
            evidence_codes = [ "http://purl.obolibrary.org/obo/ECO_0000205", "http://identifiers.org/eco/cttv_mapping_pipeline" ],
            functional_consequence = "http://purl.obolibrary.org/obo/SO_0001631",
            provenance_type = evidence_core.BaseProvenance_Type(),
            date_asserted = "2015-05-11T11:46:09+00:00",
            resource_score = evidence_score.Pvalue(value = 2.000000039082963e-25)
        )
        )
                                                                                        
    logger.info(obj.evidence.variant2disease.unique_experiment_reference)
    obj.evidence.resource_score = evidence_score.Probability(method=evidence_score.Method(url = "http://en.wikipedia.org/wiki/Genome-wide_association_study",
                        description = "The P value we get from the curated paper for the given variant to disease association."), value=2.000000039082963e-25)
    errors = obj.validate(logger)
    assert not obj == None and errors == 0
    
@with_setup(my_setup_function, my_teardown_function)
def test_animal_models_create_and_clone():

    now = datetime.datetime.now()
    obj = opentargets.Animal_Models()
    obj.validated_against_schema_version = '1.2.8'
    obj.access_level = 'public'
    obj.type = 'animal_model'
    obj.sourceID = 'phenodigm'
    obj.target = bioentity.Target(
        id = "http://www.identifier.org/ensembl/ENSG00000105810",
        target_type="http://identifiers.org/cttv.target/gene_evidence", 
        activity="http://identifiers.org/cttv.activity/predicted_damaging"
        )
    obj.disease = bioentity.Disease(
        id = "http://www.orpha.net/ORDO/Orphanet_137631",
        name="Lung fibrosis - immunodeficiency - 46,XX gonadal dysgenesis"
        )

    obj.unique_association_fields = {}
    obj.unique_association_fields['predictionModel'] = 'mgi_predicted'

    obj.evidence = opentargets.Animal_ModelsEvidence()
    #obj.evidence.evidence_codes.append("http://identifiers.org/eco/ECO:0000057")
    obj.evidence.orthologs = evidence_phenotype.Orthologs(
        evidence_codes = ["http://identifiers.org/eco/ECO:0000265"],
        provenance_type= evidence_core.BaseProvenance_Type(database=evidence_core.BaseDatabase(id="MGI", version="2015")),
        resource_score= evidence_score.Pvalue(type="pvalue", method= evidence_score.Method(description ="Orthology from MGI"), value=0.0),
        date_asserted= now.isoformat(),
        human_gene_id = 'http://identifiers.org/ensembl/ENSG00000105810',
        model_gene_id = 'http://identifiers.org/ensembl/ENSMUSG00000040274',
        species = "mouse"
        ) 
    obj.evidence.biological_model = evidence_phenotype.Biological_Model(
        evidence_codes = ["http://identifiers.org/eco/ECO:0000179"],
        provenance_type= evidence_core.BaseProvenance_Type(database=evidence_core.BaseDatabase(id="MGI", version="2015")),
        resource_score= evidence_score.Pvalue(type="pvalue", method= evidence_score.Method(description =""), value=0),
        date_asserted= now.isoformat(),
        model_id = "23150",
        species = "mouse",
        allele_ids = 'MGI:5141514|MGI:5141514',
        zygosity = 'hom',
        genetic_background ='involves: 129 * C57BL/6 * FVB/N',
        allelic_composition = 'Cdk6<tm2.1Phin>/Cdk6<tm2.1Phin>',
        model_gene_id = 'http://identifiers.org/ensembl/ENSMUSG00000040274',
        #evidence_codes = 
        phenotypes = 
            [
            bioentity.Phenotype(id = "MP:0000706", term_id = "http://purl.obolibrary.org/obo/MP:0000706", label = "small thymus"),
            bioentity.Phenotype(id = "MP:0000715", term_id = "http://purl.obolibrary.org/obo/MP:0000715", label = "decreased thymocyte number"),
            bioentity.Phenotype(id = "MP:0002145", term_id = "http://purl.obolibrary.org/obo/MP:0002145", label = "abnormal T cell differentiation"),
            bioentity.Phenotype(id = "MP:0004810", term_id = "http://purl.obolibrary.org/obo/MP:0004810", label = "decreased hematopoietic stem cell number"),
            bioentity.Phenotype(id = "MP:0005090", term_id = "http://purl.obolibrary.org/obo/MP:0005090", label = "increased double-negative T cell number"),
            bioentity.Phenotype(id = "MP:0005092", term_id = "http://purl.obolibrary.org/obo/MP:0005092", label = "decreased double-positive T cell number"),
            bioentity.Phenotype(id = "MP:0008074", term_id = "http://purl.obolibrary.org/obo/MP:0008074", label = "increased CD4-positive, alpha beta T cell number"),
            bioentity.Phenotype(id = "MP:0008078", term_id = "http://purl.obolibrary.org/obo/MP:0008078", label = "increased CD8-positive, alpha-beta T cell number"),
            bioentity.Phenotype(id = "MP:0010130", term_id = "http://purl.obolibrary.org/obo/MP:0010130", label = "decreased DN1 thymic pro-T cell number"),
            bioentity.Phenotype(id = "MP:0010132", term_id = "http://purl.obolibrary.org/obo/MP:0010132", label = "decreased DN2 thymocyte number"),
            bioentity.Phenotype(id = "MP:0010133", term_id = "http://purl.obolibrary.org/obo/MP:0010133", label = "increased DN3 thymocyte number"),
            bioentity.Phenotype(id = "MP:0010136", term_id = "http://purl.obolibrary.org/obo/MP:0010136", label = "decreased DN4 thymocyte number"),
            bioentity.Phenotype(id = "MP:0010763", term_id = "http://purl.obolibrary.org/obo/MP:0010763", label = "abnormal hematopoietic stem cell physiology")
            ]
        )

    obj.evidence.disease_model_association = evidence_phenotype.Disease_Model_Association(
        disease_id = "http://www.orpha.net/ORDO/Orphanet_137631",
        model_id = "23150",    
        provenance_type= evidence_core.BaseProvenance_Type(database=evidence_core.BaseDatabase(id="PhenoDigm", version="2015")),
        evidence_codes = ["http://identifiers.org/eco/ECO:0000057"],    
        resource_score= evidence_score.Summed_Total(type="summed_total", method= evidence_score.Method(description ="PhenoDigm Score"), value=91.57),
        date_asserted= now.isoformat(), 
        model_phenotypes = 
            [
            bioentity.Phenotype(id = "MP:0008074", term_id = "http://purl.obolibrary.org/obo/MP:0008074", label = "increased CD4-positive, alpha beta T cell number"),
            bioentity.Phenotype(id = "MP:0010133", term_id = "http://purl.obolibrary.org/obo/MP:0010133", label = "increased DN3 thymocyte number"),
            bioentity.Phenotype(id = "MP:0005092", term_id = "http://purl.obolibrary.org/obo/MP:0005092", label = "decreased double-positive T cell number"), 
            bioentity.Phenotype(id = "MP:0010763", term_id = "http://purl.obolibrary.org/obo/MP:0010763", label = "abnormal hematopoietic stem cell physiology"),        
            bioentity.Phenotype(id = "MP:0000715", term_id = "http://purl.obolibrary.org/obo/MP:0000715", label = "decreased thymocyte number"),
            bioentity.Phenotype(id = "MP:0010132", term_id = "http://purl.obolibrary.org/obo/MP:0010132", label = "decreased DN2 thymocyte number"),
            bioentity.Phenotype(id = "MP:0010136", term_id = "http://purl.obolibrary.org/obo/MP:0010136", label = "decreased DN4 thymocyte number"),
            bioentity.Phenotype(id = "MP:0004810", term_id = "http://purl.obolibrary.org/obo/MP:0004810", label = "decreased hematopoietic stem cell number"),
            bioentity.Phenotype(id = "MP:0010130", term_id = "http://purl.obolibrary.org/obo/MP:0010130", label = "decreased DN1 thymic pro-T cell number"),
            bioentity.Phenotype(id = "MP:0002145", term_id = "http://purl.obolibrary.org/obo/MP:0002145", label = "abnormal T cell differentiation"),
            bioentity.Phenotype(id = "MP:0000706", term_id = "http://purl.obolibrary.org/obo/MP:0000706", label = "small thymus"),
            bioentity.Phenotype(id = "MP:0008078", term_id = "http://purl.obolibrary.org/obo/MP:0008078", label = "increased CD8-positive, alpha-beta T cell number")        
            ],
        human_phenotypes = 
            [
            bioentity.Phenotype(id = "HP:0004315", term_id = "http://purl.obolibrary.org/obo/MP:0008074", label = "IgG deficiency"),
            bioentity.Phenotype(id = "HP:0002850", term_id = "http://purl.obolibrary.org/obo/MP:0010133", label = "IgM deficiency"),
            bioentity.Phenotype(id = "HP:0000777", term_id = "http://purl.obolibrary.org/obo/MP:0005092", label = "Abnormality of the thymus"), 
            bioentity.Phenotype(id = "HP:0005415", term_id = "http://purl.obolibrary.org/obo/MP:0010763", label = "Decreased number of CD8+ T cells"),        
            bioentity.Phenotype(id = "HP:0100765", term_id = "http://purl.obolibrary.org/obo/MP:0000715", label = "Abnormality of the tonsils"),
            bioentity.Phenotype(id = "HP:0002720", term_id = "http://purl.obolibrary.org/obo/MP:0010132", label = "IgA deficiency"),
            bioentity.Phenotype(id = "HP:0005407", term_id = "http://purl.obolibrary.org/obo/MP:0010136", label = "Decreased number of CD4+ T cells")
            ]
        )
        
        
    obj.evidence.date_asserted = now.isoformat()
    obj.evidence.is_associated = True

    errors = obj.validate(logger)
    assert not obj == None and errors == 0

@with_setup(my_setup_function, my_teardown_function)
def test_expression_create_and_clone():
    obj = opentargets.Expression()
    obj.access_level = "public"
    obj.sourceID = "opentargets"
    obj.validated_against_schema_version = "1.2.8"
    # create a target
    obj.target = bioentity.Target(
        id=["http://identifiers.org/ensembl/ENSG00000213724"], 
        activity="http://identifiers.org/cttv.activity/predicted_damaging", 
        target_type="http://identifiers.org/cttv.target/gene_evidence"
        )
    obj.disease = bioentity.Disease(id=["http://www.ebi.ac.uk/efo/EFO_0003767"]) 
    
    assert not obj == None
    
@with_setup(my_setup_function, my_teardown_function)
def test_drug_create_and_clone():
    obj = opentargets.Drug()
    assert not obj == None

@with_setup(my_setup_function, my_teardown_function)
def test_literature_curated_create_and_clone():
    obj = opentargets.Literature_Curated()
    assert not obj == None

@with_setup(my_setup_function, my_teardown_function)
def test_literature_mining_create_and_clone():
    lit_id_ = '12345678'
    target = "http://identifiers.org/ensembl/ENSG00000213724"
    disease = "http://www.ebi.ac.uk/efo/EFO_0003767"
    score = 0.5
    obj = opentargets.Literature_Mining(type='literature')
    obj.access_level = "public"
    obj.sourceID = "disgenet"
    obj.validated_against_schema_version = "1.2.8"
    obj.unique_association_fields = {"target": target,
            "publicationIDs": lit_id_,
            "disease_uri": disease}
    obj.target = bioentity.Target(id=target, activity="http://identifiers.org/cttv.activity/up_or_down", target_type="http://identifiers.org/cttv.target/gene_or_protein_or_transcript")
    obj.disease = bioentity.Disease(id=disease)
    obj.evidence = evidence_core.Literature_Mining()
    obj.evidence.unique_experiment_reference = lit_id_
    obj.evidence.provenance_type = evidence_core.BaseProvenance_Type()
    obj.evidence.date_asserted = '2015-05-15'
    obj.evidence.resource_score = evidence_score.Summed_Total(method=evidence_score.Method(url = "http://disgenet.org/web/DisGeNET/menu/dbinfo#score",
                            description = "DisGeNET gene-disease score takes into account the number and type of sources (level of curation, organisms), and the number of publications supporting the association"), value=score)
    obj.evidence.literature_ref = evidence_core.Single_Lit_Reference(lit_id= lit_id_)
    obj.evidence.literature_ref.mined_sentences = [];
    mined_sentences=["Our aim was to evaluate possible differences in glucocorticoid receptor (GR) density in peripheral leukocytes and effects of low-dose GCS treatment on GR density and on the hypothalamic-pituitary-adrenal axis in UC patients who had received high-dose GCS treatment due to a moderate or severe attack.","Up to 30% of patients with severe-to-moderate attacks of ulcerative colitis (UC) respond poorly to glucocorticosteroid (GCS) treatment.","Differences in GR mRNA levels per se thus may not be important for the ability of patients with UC to respond to GCS treatment."]
    for sentence in mined_sentences:
        obj.evidence.literature_ref.mined_sentences.append(evidence_core.Base_Mined_Sentences_Item(text = sentence, section = "abstract"))
    obj.evidence.evidence_codes = []
    obj.evidence.evidence_codes.append("http://www.targetvalidation.org/evidence/literature_mining")
    obj.evidence.evidence_codes.append("http://purl.obolibrary.org/obo/ECO_0000213")
    
    errors = obj.validate(logger)
    logger.info(errors)
    assert not obj == None and errors == 0

