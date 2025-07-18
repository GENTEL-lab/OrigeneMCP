import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ChemblAPI:
    BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/json'})

    def get_activity(self):
        """Retrieve activity object list."""

        result = self.session.get(self.BASE_URL + "/activity/?limit=5&offset=0")
        return result.text

    def get_activity_by_id(self, activity_id):
        """Retrieve single activity object details by ID."""
        result = self.session.get(self.BASE_URL + f"/activity/{activity_id}")
        return result.text

    def get_activity_by_ids(self, activity_ids:list):
        """Retrieve multiple activity objects by IDs."""
        ids_str = ";".join([str(id) for id in activity_ids])
        result = self.session.get(self.BASE_URL + f"/activity?set/{ids_str}")
        return result.text

    def search_activity(self, query_str):
        """Search activity using query string"""
        result = self.session.get(self.BASE_URL + f"/activity/search?q={query_str}&limit=1&offset=0")
        return result.text

    def get_activity_supplementary_data_by_activity(self):
        """Retrieve activitysupplementarydatabyactivity object list."""
        result = self.session.get(self.BASE_URL + "/activity_supplementary_data_by_activity/?limit=5&offset=0")
        return result.text

    def get_activity_supplementary_data_by_activity_by_id(self, activity_id):
        """Retrieve single activitysupplementarydatabyactivity object details by ID."""
        result = self.session.get(self.BASE_URL + f"/activity_supplementary_data_by_activity/{activity_id}")
        return result.text

    def get_activity_supplementary_data_by_activity_by_ids(self, activity_ids:list[int]):
        """Retrieve multiple activitysupplementarydatabyactivity objects by IDs."""
        ids_str = ";".join([str(id) for id in activity_ids])
        result = self.session.get(self.BASE_URL + f"/activity_supplementary_data_by_activity/set/{ids_str}")
        return result.text

    def get_assay(self):
        """Retrieve assay object list."""
        result = self.session.get(self.BASE_URL + "/assay/?limit=5&offset=0")
        return result.text

    def get_assay_by_id(self, assay_chembl_id):
        """Retrieve single assay object details by ID."""
        result = self.session.get(self.BASE_URL + f"/assay/{assay_chembl_id}")
        return result.text

    def get_assay_by_ids(self, assay_chembl_ids:list[str]):
        """Retrieve multiple assay objects by IDs."""
        ids_str = ";".join(assay_chembl_ids)
        result = self.session.get(self.BASE_URL + f"/assay/set/{ids_str}")
        return result.text

    def search_assay(self, query_str):
        """Search assay using query string."""
        result = self.session.get(self.BASE_URL + f"/assay/search?q={query_str}&limit=5&offset=0")
        return result.text

    def get_assay_class(self):
        """Retrieve assay_class object list."""
        result = self.session.get(self.BASE_URL + "/assay_class/?limit=5&offset=0")
        return result.text

    def get_assay_class_by_id(self, assay_class_id):
        """Retrieve single assay_class object details by ID."""
        result = self.session.get(self.BASE_URL + f"/assay_class/{assay_class_id}")
        return result.text

    def get_assay_class_by_ids(self, assay_class_ids:list):
        """Retrieve multiple assay_class objects by IDs."""
        ids_str = ";".join([str(id) for id in assay_class_ids])
        result = self.session.get(self.BASE_URL + f"/assay_class/set/{ids_str}")
        return result.text

    def get_atc_class(self):
        """Retrieve atc_class object list."""
        return self.session.get(self.BASE_URL + "/atc_class/").text

    def get_atc_class_by_id(self, level5):
        """Retrieve single atc_class object details by ID."""
        return self.session.get(self.BASE_URL + f"/atc_class/{level5}").text

    def get_atc_class_by_ids(self, level5s:list[str]):
        """Retrieve multiple atc_class objects by IDs."""
        ids_str = ";".join(level5s)
        return self.session.get(self.BASE_URL + f"/atc_class/set/{ids_str}").text

    def get_binding_site(self):
        """Retrieve binding_site object list."""
        return self.session.get(self.BASE_URL + "/binding_site/?limit=5&offset=0").text

    def get_binding_site_by_id(self, site_id):
        """Retrieve single binding_site object details by ID."""
        return self.session.get(self.BASE_URL + f"/binding_site/{site_id}").text

    def get_binding_site_by_ids(self, site_ids:list):
        """Retrieve multiple binding_site objects by IDs."""
        ids_str = ";".join([str(id) for id in site_ids])
        return self.session.get(self.BASE_URL + f"/binding_site/set/{ids_str}").text

    def get_biotherapeutic(self):
        """Retrieve biotherapeutic object list."""
        return self.session.get(self.BASE_URL + "/biotherapeutic/?limit=5&offset=0").text

    def get_biotherapeutic_by_id(self, molecule_chembl_id):
        """Retrieve single biotherapeutic object details by ID."""
        return self.session.get(self.BASE_URL + f"/biotherapeutic/{molecule_chembl_id}").text

    def get_biotherapeutic_by_ids(self, molecule_chembl_ids:list[str]):
        """Retrieve multiple biotherapeutic objects by IDs."""
        ids_str = ";".join(molecule_chembl_ids)
        return self.session.get(self.BASE_URL + f"/biotherapeutic/set/{ids_str}").text

    def get_cell_line(self):
        """Retrieve cell line object list."""
        return self.session.get(self.BASE_URL + "/cell_line/?limit=5&offset=0").text

    def get_cell_line_by_id(self, cell_id):
        """Retrieve single cell line object details by ID."""
        return self.session.get(self.BASE_URL + f"/cell_line/{cell_id}").text

    def get_cell_line_by_ids(self, cell_ids:list):
        """Retrieve multiple cell line objects by IDs."""
        ids_str = ";".join([str(id) for id in cell_ids])
        return self.session.get(self.BASE_URL + f"/cell_line/set/{ids_str}").text

    def get_chembl_id_lookup(self):
        """Retrieve chembl_id_lookup object list."""
        return self.session.get(self.BASE_URL + "/chembl_id_lookup/?limit=5&offset=0").text

    def get_chembl_id_lookup_by_id(self, chembl_id):
        """Retrieve single chembl_id_lookup object details by ID."""
        return self.session.get(self.BASE_URL + f"/chembl_id_lookup/{chembl_id}").text

    def get_chembl_id_lookup_by_ids(self, chembl_ids:list[str]):
        """Retrieve multiple chembl_id_lookup objects by IDs."""
        ids_str = ";".join(chembl_ids)
        return self.session.get(self.BASE_URL + f"/chembl_id_lookup/set/{ids_str}").text

    def search_chembl_id_lookup(self, query_str):
        """Search chemblidlookup using query string."""
        return self.session.get(self.BASE_URL + f"/chembl_id_lookup/search?q={query_str}&limit=1&offset=0").text

    def get_chembl_release(self):
        """Retrieve chembl_release object list."""
        return self.session.get(self.BASE_URL + "/chembl_release/?limit=5&offset=0").text

    def get_chembl_release_by_id(self, chembl_release):
        """Retrieve single chembl_release object details by ID."""
        if isinstance(chembl_release, str) and "CHEMBL_" in chembl_release:
            chembl_release = chembl_release.split("_")[1]
        return self.session.get(self.BASE_URL + f"/chembl_release/{chembl_release}").text

    def get_chembl_release_by_ids(self, chembl_releases:list):
        """Retrieve multiple chembl_release objects by IDs."""
        try:
            ids_str = ";".join([id.split("_")[1] if isinstance(id, str) and "CHEMBL_" in str(id) else id for id in chembl_releases])
        except Exception:
            ids_str = ";".join([str(id) for id in chembl_releases])
        return self.session.get(self.BASE_URL + f"/chembl_release/set/{ids_str}").text

    def get_compound_record(self):
        """Retrieve compound_record object list."""
        return self.session.get(self.BASE_URL + "/compound_record/?limit=5&offset=0").text

    def get_compound_record_by_id(self, record_id):
        """Retrieve single compound_record object details by ID."""
        return self.session.get(self.BASE_URL + f"/compound_record/{record_id}").text

    def get_compound_record_by_ids(self, record_ids:list):
        """Retrieve multiple compound_record objects by IDs."""
        ids_str = ";".join([str(id) for id in record_ids])
        return self.session.get(self.BASE_URL + f"/compound_record/set/{ids_str}").text

    def get_compound_structural_alert(self):
        """Retrieve compound_structural_alert object list."""
        return self.session.get(self.BASE_URL + "/compound_structural_alert/").text

    def get_compound_structural_alert_by_id(self, cpd_str_alert_id):
        """Retrieve single compound_structural_alert object details by ID."""
        return self.session.get(self.BASE_URL + f"/compound_structural_alert/{cpd_str_alert_id}").text

    def get_compound_structural_alert_by_ids(self, cpd_str_alert_ids:list):
        """Retrieve multiple compound_structural_alert objects by IDs."""
        ids_str = ";".join([str(id) for id in cpd_str_alert_ids])
        return self.session.get(self.BASE_URL + f"/compound_structural_alert/set/{ids_str}").text

    def get_document(self):
        """Retrieve document object list."""
        return self.session.get(self.BASE_URL + "/document/?limit=5&offset=0").text

    def get_document_by_id(self, document_chembl_id):
        """Retrieve single document object details by ID."""
        return self.session.get(self.BASE_URL + f"/document/{document_chembl_id}").text

    def get_document_by_ids(self, document_chembl_ids:list[str]):
        """Retrieve multiple document objects by IDs."""
        ids_str = ";".join(document_chembl_ids)
        return self.session.get(self.BASE_URL + f"/document/set/{ids_str}").text

    def search_document(self, query_str):
        """Search document using query string."""
        return self.session.get(self.BASE_URL + f"/document/search?q={query_str}&limit=1&offset=0").text

    def get_document_similarity(self):
        """Retrieve document similarity object list."""
        return self.session.get(self.BASE_URL + "/document_similarity/?limit=5&offset=0").text

    def get_document_similarity_by_id(self, document_1_chembl_id):
        """Retrieve single document similarity object details by ID."""
        return self.session.get(self.BASE_URL + f"/document_similarity/{document_1_chembl_id}").text

    def get_document_similarity_by_ids(self, document_1_chembl_ids:list[str]):
        """Retrieve multiple document similarity objects by IDs."""
        ids_str = ";".join(document_1_chembl_ids)
        return self.session.get(self.BASE_URL + f"/document_similarity/set/{ids_str}").text

    def get_drug(self):
        """Retrieve drug object list."""
        return self.session.get(self.BASE_URL + "/drug/?limit=5&offset=0").text

    def get_drug_by_id(self, molecule_chembl_id:str):
        """Retrieve single drug object details by ID."""
        return self.session.get(self.BASE_URL + f"/drug/{molecule_chembl_id}").text

    def get_drug_by_ids(self, molecule_chembl_ids:list[str]):
        """Retrieve multiple drus objects by IDs."""
        ids_str = ";".join(molecule_chembl_ids)
        return self.session.get(self.BASE_URL + f"/drug/set/{ids_str}").text

    def get_drug_indication(self):
        """Retrieve drug indication object list."""
        return self.session.get(self.BASE_URL + "/drug_indication/?limit=5&offset=0").text

    def get_drug_indication_by_id(self, drugind_id):
        """Retrieve drug indication object details by ID."""
        return self.session.get(self.BASE_URL + f"/drug_indication/{drugind_id}").text

    def get_drug_indication_by_ids(self, drugind_ids:list):
        """Retrieve multiple drug indication objects by IDs."""
        ids_str = ";".join([str(id) for id in drugind_ids])
        return self.session.get(self.BASE_URL + f"/drug_indication/set/{ids_str}").text

    def get_drug_warning(self):
        """Retrieve drug_warning object list."""
        return self.session.get(self.BASE_URL + "/drug_warning/?limit=5&offset=0").text

    def get_drug_warning_id(self, warning_id):
        """Retrieve single drug_warning object details by ID."""
        return self.session.get(self.BASE_URL + f"/drug_warning/{warning_id}").text

    def get_drug_warning_ids(self, warning_ids:list):
        """Retrieve multiple drug_warning objects by IDs."""
        ids_str = ";".join([str(id) for id in warning_ids])
        return self.session.get(self.BASE_URL + f"/drug_warning/set/{ids_str}").text

    def get_go_slim(self):
        """Retrieve go_slim object list."""
        return self.session.get(self.BASE_URL + "/go_slim/?limit=5&offset=0").text

    def get_go_slim_id(self, go_id):
        """Retrieve single go_slim object details by ID."""
        return self.session.get(self.BASE_URL + f"/go_slim/{go_id}").text

    def get_go_slim_ids(self, go_ids:list[str]):
        """Retrieve multiple go_slim objects by IDs."""
        ids_str = ";".join(go_ids)
        return self.session.get(self.BASE_URL + f"/go_slim/set/{ids_str}").text

    def get_mechanism(self):
        """Retrieve mechanism object list."""
        return self.session.get(self.BASE_URL + "/mechanism/?limit=5&offset=0").text

    def get_mechanism_id(self, mec_id):
        """Retrieve single mechanism object details by ID."""
        return self.session.get(self.BASE_URL + f"/mechanism/{mec_id}").text

    def get_mechanism_ids(self, mec_ids:list):
        """Retrieve multiple mechanism objects by IDs."""
        ids_str = ";".join([f"{id}" for id in mec_ids])
        return self.session.get(self.BASE_URL + f"/mechanism/set/{ids_str}").text

    def get_metabolism(self):
        """Retrieve metabolism object list."""
        return self.session.get(self.BASE_URL + "/metabolism/?limit=5&offset=0").text

    def get_metabolism_id(self, met_id):
        """Retrieve single metabolism object details by ID."""
        return self.session.get(self.BASE_URL + f"/metabolism/{met_id}").text

    def get_metabolism_ids(self, met_ids:list):
        """Retrieve multiple metabolism objects by IDs."""
        ids_str = ";".join([f"{id}" for id in met_ids])
        return self.session.get(self.BASE_URL + f"/metabolism/set/{ids_str}").text

    def get_molecule(self):
        """
            Retrieve list of molecules. Apart from the standard set of relation types, there is one specific operator:

            flexmatch - matches SMILES with the same structure, as opposed to exact match, for example: COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC (C)(C)[C@H]6COc7cc(OC)ccc7[C@@H]56 will match two molecules with:

            COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC (C)(C)[C@H]6COc7cc(OC)ccc7[C@@H]56 and

            COc1ccc2[C@@H]3[C@H](COc2c1)C(C)(C)OC4=C3C(=O)C(=O)C5=C4OC (C)(C)[C@@H]6COc7cc(OC)ccc7[C@H]56
            SMILES.
        """
        return self.session.get(self.BASE_URL + "/molecule/?limit=1&offset=0").text

    def get_molecule_id(self, molecule_chembl_id):
        """Retrieve single molecule object details by ID."""
        return self.session.get(self.BASE_URL + f"/molecule/{molecule_chembl_id}").text

    def get_molecule_ids(self, molecule_chembl_ids:list):
        """Retrieve multiple molecule objects by IDs."""
        ids_str = ";".join([f"{id}" for id in molecule_chembl_ids])
        return self.session.get(self.BASE_URL + f"/molecule/set/{ids_str}").text

    def search_molecule(self, query_str):
        """Search molecule using query string."""
        return self.session.get(self.BASE_URL + f"/molecule/search?q={query_str}&limit=1&offset=0").text

    def get_molecule_form(self):
        """Retrieve molecule_form object list."""
        return self.session.get(self.BASE_URL + "/molecule_form/?limit=5&offset=0").text

    def get_molecule_form_id(self, molecule_chembl_id):
        """Retrieve single metabolism object details by ID."""
        return self.session.get(self.BASE_URL + f"/molecule_form/{molecule_chembl_id}").text

    def get_molecule_form_ids(self, molecule_chembl_ids:list):
        """Retrieve multiple molecule_form objects by IDs."""
        ids_str = ";".join(molecule_chembl_ids)
        return self.session.get(self.BASE_URL + f"/molecule_form/set/{ids_str}").text

    def get_organism(self):
        """Retrieve organism object list."""
        return self.session.get(self.BASE_URL + "/organism/?limit=5&offset=0").text

    def get_organism_id(self, oc_id):
        """Retrieve single organism object details by ID."""
        return self.session.get(self.BASE_URL + f"/organism/{oc_id}").text

    def get_organism_ids(self, oc_ids:list):
        """Retrieve multiple organism objects by IDs."""
        ids_str = ";".join([str(id) for id in oc_ids])
        return self.session.get(self.BASE_URL + f"/organism/set/{ids_str}").text

    def get_protein_classification(self):
        """Retrieve protein_classification object list."""
        return self.session.get(self.BASE_URL + "/protein_classification/?limit=5&offset=0").text

    def get_protein_classification_id(self, protein_class_id):
        """Retrieve single protein_classification object details by ID."""
        return self.session.get(self.BASE_URL + f"/protein_classification/{protein_class_id}").text

    def get_protein_classification_ids(self, protein_class_ids:list):
        """Retrieve multiple protein_classification objects by IDs."""
        ids_str = ";".join([str(id) for id in protein_class_ids])
        return self.session.get(self.BASE_URL + f"/protein_classification/set/{ids_str}").text

    def search_protein_classification(self, query_str):
        """Search protein_classification using query string."""
        return self.session.get(self.BASE_URL + f"/protein_classification/search?q={query_str}&limit=1&offset=0").text

    def get_similarity_smiles(self,standard_inchi_key, similarity):
        """Retrieve single similarity object details by ID."""
        return self.session.get(self.BASE_URL + f"/similarity/{standard_inchi_key}/85").text

    def get_source(self):
        """Retrieve source object list."""
        return self.session.get(self.BASE_URL + "/source/?limit=5&offset=0").text

    def get_source_id(self, src_id):
        """Retrieve single source object details by ID."""
        return self.session.get(self.BASE_URL + f"/source/{src_id}").text

    def get_source_ids(self, src_ids:list):
        """Retrieve multiple source objects by IDs."""
        ids_str = ";".join([str(id) for id in src_ids])
        return self.session.get(self.BASE_URL + f"/source/set/{ids_str}").text

    def get_status(self):
        """Retrieve status object list."""
        return self.session.get(self.BASE_URL + "/status/?limit=5&offset=0").text

    def substructure_info(self, molecule_chembl_id):
        """Retrieve single substructure object details by ID."""
        return self.session.get(self.BASE_URL + f"/substructure/{molecule_chembl_id}").text

    def get_target(self):
        """Retrieve target object list."""
        return self.session.get(self.BASE_URL + "/target/?limit=5&offset=0").text

    def get_target_id(self, target_chembl_id):
        """Retrieve single target object details by ID."""
        return self.session.get(self.BASE_URL + f"/target/{target_chembl_id}").text

    def get_target_ids(self, target_chembl_ids:list):
        """Retrieve multiple target objects by IDs."""
        ids_str = ";".join(target_chembl_ids)
        return self.session.get(self.BASE_URL + f"/target/set/{ids_str}").text

    def search_target(self, query_str):
        """Search target using query string."""
        return self.session.get(self.BASE_URL + f"/target/search?q={query_str}&limit=1&offset=0").text

    def get_target_component(self):
        """Retrieve target_component object list."""
        return self.session.get(self.BASE_URL + "/target_component/?limit=5&offset=0").text

    def get_target_component_id(self, component_id):
        """Retrieve single target_component object details by ID."""
        return self.session.get(self.BASE_URL + f"/target_component/{component_id}").text

    def get_target_component_ids(self, component_ids: list):
        """Retrieve multiple target_component objects by IDs."""
        ids_str = ";".join([str(id) for id in component_ids])
        return self.session.get(self.BASE_URL + f"/target_component/set/{ids_str}").text

    def get_target_relation(self):
        """Retrieve target object list."""
        return self.session.get(self.BASE_URL + "/target_relation/?limit=5&offset=0").text

    def get_target_relation_id(self, related_target_chembl_id):
        """Retrieve single target_relation object details by ID."""
        return self.session.get(self.BASE_URL + f"/target_relation/{related_target_chembl_id}").text

    def get_target_relation_ids(self, related_target_chembl_ids: list):
        """Retrieve multiple target_relation objects by IDs."""
        ids_str = ";".join(related_target_chembl_ids)
        return self.session.get(self.BASE_URL + f"/target_relation/set/{ids_str}").text

    def get_tissue(self):
        """Retrieve tissue object list."""
        return self.session.get(self.BASE_URL + "/tissue/?limit=5&offset=0").text

    def get_tissue_id(self, tissue_chembl_id):
        """Retrieve single tissue object details by ID."""
        return self.session.get(self.BASE_URL + f"/tissue/{tissue_chembl_id}").text

    def get_tissue_ids(self, tissue_chembl_ids: list):
        """Retrieve multiple tissue objects by IDs."""
        ids_str = ";".join(tissue_chembl_ids)
        return self.session.get(self.BASE_URL + f"/tissue/set/{ids_str}").text

    def get_xref_source(self):
        """Retrieve xref_source object list."""
        return self.session.get(self.BASE_URL + "/xref_source/?limit=5&offset=0").text

    def get_xref_source_id(self, xref_src_db):
        """Retrieve single xref_source object details by ID."""
        return self.session.get(self.BASE_URL + f"/xref_source/{xref_src_db}").text

    def get_xref_source_ids(self, xref_src_dbs: list):
        """Retrieve multiple xref_source objects by IDs."""
        ids_str = ";".join(xref_src_dbs)
        return self.session.get(self.BASE_URL + f"/xref_source/set/{ids_str}").text

    def get_image(self, chembl_id):
        """Get image of the compound, specified by

            ChEMBL ID or
            Standard InChI Key
            You can specify optional parameters:

            engine - chemistry toolkit used for rendering, can be rdkit only, default: rdkit.
            dimensions - size of the image (the length of the square image side). Can't be more than 500, default: 500.
            ignoreCoords - Ignore 2D coordinates encoded in the molfile and let the chemistry toolkit to recompute them.
        """
        # self.session.headers.update({'Accept': 'application/svg'})
        return self.session.get(self.BASE_URL + f"/image/{chembl_id}").text


# if __name__ == '__main__':
#     ca = ChemblAPI()
    # res = ca.get_activity()

    # res = ca.get_activity_by_id(31863)
    # res = ca.get_activity_by_ids([31863, 31864])
    # loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(asyncio.wait([fetch_data("/activity")]))
    # res = asyncio.run(fetch_data("/activity"))
    # res = asyncio.run(ca.async_get_activity_by_id(31863))
    # res = ca.search_activity("CHEMBL1806")
    # res = ca.get_activity_supplementary_data_by_activity()

    # res = ca.get_activity_supplementary_data_by_activity_by_ids([17126237,17126238])
    # res = ca.get_assay()
    # res = ca.get_assay_id("CHEMBL615117")
    # res = ca.get_assay_ids(["CHEMBL615117","CHEMBL615118"])
    # res = ca.search_assay("CHEMBL615117")

    # res = ca.get_assay_class()
    # res = ca.get_assay_class_id(1)
    # res = ca.get_assay_class_ids([1, 2])

    # res = ca.get_atc_class()
    # res = ca.get_atc_class_id("A01AA04")
    # res = ca.get_atc_class_ids(["A01AA04", "A01AA30"])

    # res = ca.get_binding_site()
    # res = ca.get_binding_site_id(2)
    # res = ca.get_binding_site_ids(["1","2","3","4","5","6"])

    # res = ca.get_biotherapeutic()
    # res = ca.get_biotherapeutic_id("CHEMBL448105")
    # res = ca.get_biotherapeutic_ids(["CHEMBL448105", "CHEMBL268600"])

    # res = ca.get_cell_line()
    # res = ca.get_cell_line_id(1)
    # res = ca.get_cell_line_ids([1, 2, 3])

    # res = ca.get_chembl_id_lookup()
    # res = ca.get_chembl_id_lookup_id("CHEMBL1")
    # res = ca.get_chembl_id_lookup_ids(["CHEMBL1"])
    # res = ca.search_chembl_id_lookup("CHEMBL1123123")

    # res = ca.get_chembl_release()
    # res = ca.get_chembl_release_id(1)
    # res = ca.get_chembl_release_id("CHEMBL_1")
    # res = ca.get_chembl_release_ids([2])
    # res = ca.get_chembl_release_ids(["CHEMBL_2"])

    # res = ca.get_compound_record()
    # res = ca.get_compound_record_id(1)
    # res = ca.get_compound_record_ids([2])

    # res = ca.get_compound_structural_alert()
    # res = ca.get_compound_structural_alert_id(79048021)
    # res = ca.get_compound_structural_alert_ids([79048021])

    # res = ca.get_document()
    # res = ca.get_document_by_id("CHEMBL1158643")
    # res = ca.get_document_by_ids(["CHEMBL1158643"])
    # res = ca.search_document("Unpublished")

    # res = ca.get_document_similarity()
    # res = ca.get_document_similarity_by_id('CHEMBL1148466')
    # res = ca.get_document_similarity_by_ids(['CHEMBL1148466'])

    # res = ca.get_drug()
    # res = ca.get_drug_by_id("CHEMBL3")
    # res = ca.get_drug_by_ids(['CHEMBL3'])

    # res = ca.get_drug_indication()
    # res = ca.get_drug_indication_by_id(22606)
    # res = ca.get_drug_indication_by_ids([22606])

    # res = ca.get_drug_warning()
    # res = ca.get_drug_warning_id(1)
    # res = ca.get_drug_warning_ids([1])

    # res = ca.get_go_slim()
    # res = ca.get_go_slim_id("GO:0000003")
    # res = ca.get_go_slim_ids(["GO:0000003"])

    # res = ca.get_mechanism()
    # res = ca.get_mechanism_id(13)
    # res = ca.get_mechanism_ids([13])
    # res = ca.get_molecule()
    # res = ca.get_molecule_id("CHEMBL6329")
    # res = ca.get_molecule_ids(["CHEMBL6329"])
    # res = ca.search_molecule("Small")

    # res = ca.get_molecule_form()
    # res = ca.get_molecule_form_id("CHEMBL6329")
    # res = ca.get_molecule_form_ids(["CHEMBL6329"])

    # res = ca.get_organism()
    # res = ca.get_organism_id(1)
    # res = ca.get_organism_ids([1])

    # res = ca.get_protein_classification()
    # res = ca.get_protein_classification_id(1)
    # res = ca.get_protein_classification_ids([1])
    # res = ca.search_protein_classification("enzyme")

    # res = ca.get_source()
    # res = ca.get_source_id(1)
    # res = ca.get_source_ids([1])
    # res = ca.get_status()

    # res = ca.get_target()
    # res = ca.get_target_id("CHEMBL2074")
    # res = ca.get_target_ids(["CHEMBL2074"])
    # res = ca.search_target("glucoamylase")

    # res = ca.get_target_component()
    # res = ca.get_target_component_id(1)
    # res = ca.get_target_component_ids([2])

    # res = ca.get_target_relation()
    # res = ca.get_target_relation_id('CHEMBL2096619')
    # res = ca.get_target_relation_ids(['CHEMBL2096619'])

    # res = ca.get_tissue()
    # res = ca.get_tissue_id('CHEMBL3988026')
    # res = ca.get_tissue_ids(['CHEMBL3988026'])

    # res = ca.get_xref_source()
    # res = ca.get_xref_source_id('AlphaFoldDB')
    # res = ca.get_xref_source_ids(['AlphaFoldDB'])
    # res = ca.get_similarity_smiles('OWRSAHYFSSNENM-UHFFFAOYSA-N', 85)

    # res = ca.get_image("CHEMBL3508141")
    # print(res)



