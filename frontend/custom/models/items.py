#!/usr/bin/env python3
import re
from typing import Union, List, Optional, Any, Dict

from fastapi import APIRouter
from pydantic import Field, field_validator, model_validator, ConfigDict

import frontend.lib.utils as utils
import frontend.models.base_query_params as CoreModel
from frontend.custom.config import DEFAULT_ROWS, facet_query, facets

router = APIRouter()

class ItemsQueryParams(CoreModel.CoreQueryParams):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    expand: Optional[str] = None
    text: Optional[Union[str, List[str]]] = Field(default=None)
    sectionType: Optional[str] = Field(default=None)
    querent: Optional[str] = Field(default=None)
    patient: Optional[str] = Field(default=None)
    question_asked: Optional[Union[str, List[str]]] = Field(default=None, alias="question-asked")
    querent_is_asking_about: Optional[str] = Field(default=None, alias="querent-is-asking-about")
    age: Optional[str] = Field(default=None)
    age_search_type: Optional[str] = Field(default=None, alias="age-search-type")
    age_max: Optional[str] = Field(default=None, alias="age-max")
    age_role: Optional[str] = Field(default=None, alias="age-role")
    year: Optional[Union[int, str]] = None
    month: Optional[Union[int, str]] = None
    day: Optional[Union[int, str]] = None
    year_max: Optional[Union[int, str]] = Field(default=None, alias="year-max")
    month_max: Optional[Union[int, str]] = Field(default=None, alias="month-max")
    day_max: Optional[Union[int, str]] = Field(default=None, alias="day-max")
    search_date_type: Optional[str] = Field(default="on", alias="search-date-type")
    name: Optional[str] = Field(default=None)
    surname: Optional[str] = Field(default=None)
    name_type: Optional[str] = Field(default="on", alias="name-type")
    identifier: Optional[Union[int, str]] = None
    # Canonical facets

    f1_astrologer_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-astrologer-0")
    f1_astrologer_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-astrologer-1")
    f1_astrologer_identified: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-astrologer-identified")
    f1_damaged: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-damaged")
    f1_date_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-date-0")
    f1_date_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-date-1")
    f1_date_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-date-2")
    f1_date_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-date-3")
    f1_death: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-death")
    f1_death_cert: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-death-cert")
    f1_deleted: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-deleted")
    f1_dob: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-dob")
    f1_dob_cert: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-dob-cert")
    f1_document_type_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-document-type-0")
    f1_document_type_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-document-type-1")
    f1_document_type_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-document-type-2")
    f1_document_type_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-document-type-3")
    f1_entity_age_band_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-entity-age-band-0")
    f1_entity_age_band_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-entity-age-band-1")
    f1_entity_question_asked_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-entity-question-asked-0")
    f1_entity_question_asked_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-entity-question-asked-1")
    f1_entity_question_asked_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-entity-question-asked-2")
    f1_entity_question_asked_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-entity-question-asked-3")
    f1_event_mentioned: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-event-mentioned")
    f1_extent_of_transcription: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-extent-of-transcription")
    f1_gentry: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-gentry")
    f1_hands: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-hands")
    f1_has_astro_chart: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-has-astro-chart")
    f1_has_geo_chart: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-has-geo-chart")
    f1_how_did_it_take_place_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-how-did-it-take-place-0")
    f1_how_did_it_take_place_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-how-did-it-take-place-1")
    f1_identified_entity_is_asking_about: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-is-asking-about")
    f1_identified_entity_practice: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-practice")
    f1_identified_entity_role_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-role-0")
    f1_identified_entity_role_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-role-1")
    f1_identified_entity_role_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-role-2")
    f1_identified_entity_role_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-role-3")
    f1_identified_entity_was_never: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-identified-entity-was-never")
    f1_info_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-info-0")
    f1_info_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-info-1")
    f1_info_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-info-2")
    f1_info_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-info-3")
    f1_judgment: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-judgment")
    f1_language: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-language")
    f1_number_of_astrologers: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-number-of-astrologers")
    f1_number_of_patients: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-number-of-patients")
    f1_number_of_practitioners: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-number-of-practitioners")
    f1_number_of_querents: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-number-of-querents")
    f1_occupation_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-occupation-0")
    f1_occupation_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-occupation-1")
    f1_occupation_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-occupation-2")
    f1_occupation_mentioned: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-occupation-mentioned")
    f1_participant: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-participant")
    f1_patient: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient")
    f1_patient_age_band_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-age-band-0")
    f1_patient_age_band_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-age-band-1")
    f1_patient_assumed: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-assumed")
    f1_patient_consent: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-consent")
    f1_patient_identified: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-identified")
    f1_patient_knowledge: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-knowledge")
    f1_patient_present: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-present")
    f1_patient_sex: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-patient-sex")
    f1_person_sex: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-person-sex")
    f1_practice: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practice")
    f1_practitioner_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practitioner-0")
    f1_practitioner_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practitioner-1")
    f1_practitioner_identified: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practitioner-identified")
    f1_practitioner_is_astrologer: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practitioner-is-astrologer")
    f1_practitioner_is_patient: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practitioner-is-patient")
    f1_practitioner_is_querent: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-practitioner-is-querent")
    f1_querent: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent")
    f1_querent_age_band_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent-age-band-0")
    f1_querent_age_band_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent-age-band-1")
    f1_querent_identified: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent-identified")
    f1_querent_is_asking_about: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent-is-asking-about")
    f1_querent_present: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent-present")
    f1_querent_sex: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-querent-sex")
    f1_question_asked_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-question-asked-0")
    f1_question_asked_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-question-asked-1")
    f1_question_asked_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-question-asked-2")
    f1_question_asked_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-question-asked-3")
    f1_recipe: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-recipe")
    f1_residence_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-residence-0")
    f1_residence_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-residence-1")
    f1_residence_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-residence-2")
    f1_residence_3: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-residence-3")
    f1_residence_4: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-residence-4")
    f1_residence_mentioned: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-residence-mentioned")
    f1_shelfmark: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-shelfmark")
    f1_social_network_recorded: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-social-network-recorded")
    f1_time_of_day_0: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-time-of-day-0")
    f1_time_of_day_1: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-time-of-day-1")
    f1_time_of_day_2: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-time-of-day-2")
    f1_treatment: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-treatment")
    f1_volume_name: Optional[Union[str, List[str]]] = Field(default=None, alias="f1-volume-name")

    @model_validator(mode="before")
    def filter_and_extract_dynamic_facets(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get('age'):
            values.pop('age_role', None)

        # Pattern matches keys starting with 'f', followed by digits, and then one or more hyphen-separated alphanumeric segments.
        facet_pattern = re.compile(r"^f[0-9]+((-[a-zA-Z0-9]+)+)$")
        defined_fields = set(cls.model_fields.keys())
        defined_aliases = {field.alias for field in cls.model_fields.values() if field.alias}
        #print(f"DUMP {values}")
        for key in list(values.keys()):
            if key not in defined_fields and key not in defined_aliases:
                match = facet_pattern.match(key)
                if match:
                    facet_value = values.pop(key)
                    facet_value = facet_value if isinstance(facet_value, list) else [facet_value]
                    new_key = f"f1{match.group(1)}"
                    if new_key in values:
                        existing = values[new_key]
                        if not isinstance(existing, list):
                            existing = [existing]
                        existing.extend(facet_value)
                        values[new_key] = existing
                    else:
                        values[new_key] = facet_value
                else:
                    values.pop(key)
        return values

    @field_validator("rows", mode="after")
    def validate_rows_items(cls, value):
        return DEFAULT_ROWS if value not in (10, 20) else value

    def is_facet(self, key: str, value: Any) -> bool:
        return re.match(r"^f[0-9]+-.+?$", key) is not None

    def generate_datestring(self, year, month, day):
        if year:
            # Only form a date string if month is provided when day is provided
            if day and not month:
                return None
            parts = [str(x).zfill(2) for x in [year, month, day] if x is not None]
            return "-".join(parts)
        return None

    def generate_age_query(self, age, age_type, age_max):
        result = ''
        if not age_type:
            result = age
        elif age_type == 'lessThan':
            result = f"[* TO {age}}}"
        elif age_type == 'moreThan':
            result = f"{{{age} TO *]"
        elif age_type == 'between':
            age_clean = age if age else '*'
            age_max_clean = age_max if age_max else '*'
            result = f"[{age_clean} TO {age_max_clean}]"
        return result

    def get_solr_params(self) -> dict:
        query_params2, facet_params2 = self.separate_parameters()
        url_params = {**query_params2, **facet_params2}

        # Mapping for text translations
        translation_key = {
            "metadata": "metadata",
            "text": "text",
        }
        # These fields will be removed later.
        solr_delete = ["text", "keyword", "sectionType", "search-date-type", "age-role", "age-max", "age-search-type", "name-type", "rows"]
        solr_fields = ["_text_", "content_textual-content", "content_footnotes", "content_summary"]
        remap_fields = [
            "exclude-widedate",
            "search-correspondent",
            "search-addressee",
            "search-author",
            "search-repository",
            "day",
            "month",
            "dateRange",
            "text",
            "_text_"
        ]
        solr_params = {}

        set_params = url_params
        q = []
        fq = []
        filters = {}
        expand_clauses = {}

        # Remove exclusionary boolean params that only make sense in the affirmative.
        for p in ["exclude-widedate"]:
            if set_params.get(p, "").lower() == "no":
                set_params.pop(p, None)

        # Remap text field based on sectionType
        if set_params.get("text") and set_params.get("sectionType") in translation_key:
            key = translation_key[set_params["sectionType"]]
            set_params[key] = set_params.pop("text")
            set_params.pop("sectionType", None)
        elif set_params.get("text") and not set_params.get("sectionType") in translation_key:
            set_params['_text_']=set_params.pop("text")
            set_params.pop("text", None)
        if set_params.get("sectionType") and not set_params.get("text"):
            set_params.pop("sectionType", None)

        if set_params.get("age") and set_params.get("age-role") in ['querent','patient']:
            key = set_params["age-role"]+"-age"
            set_params[key] = self.generate_age_query(set_params.get("age"), set_params.get("age-search-type"), set_params.get("age-max"))
            set_params.pop("age-role", None)
            set_params.pop("age", None)
        elif set_params.get("age") and (not set_params.get("age-role") or set_params.get("age-role") == "any"):
            age_param = set_params.get("age")
            set_params['age'] = self.generate_age_query(age_param, set_params.get("age-search-type"), set_params.get("age-max"))
            set_params.pop("age-role", None)

        if set_params.get("question-asked"):
            ' OR '.join(['"' + item.strip('"') + '"' for item in '"Personal Affairs" "Worldly Affairs"'.split('" "')])
            questions_asked_param = ' OR '.join(
                '"' + item.strip('"') + '"'
                for group in set_params.get("question-asked")
                for item in group.split('" "')
            )
            set_params['question-asked'] = questions_asked_param

        # Date processing
        date_min = self.generate_datestring(set_params.get("year"), set_params.get("month"), set_params.get("day"))
        date_max = self.generate_datestring(set_params.get("year-max"), set_params.get("month-max"), set_params.get("day-max"))
        search_date_type = set_params.get("search-date-type")
        if date_min or search_date_type == "between":
            for k in ["year", "month", "day", "year-max", "month-max", "day-max", "search-date-type"]:
                set_params.pop(k, None)
            predicate_type = "Within"
            if date_max or search_date_type == "between":
                date_max_final = date_max if date_max else "2009-02-12"
                date_min_final = date_min if date_min else "1510-01-01"
                predicate_type = "Intersects"
                date_range = f"[{date_min_final} TO {date_max_final}]"
            else:
                if search_date_type == "after":
                    predicate_type = "Intersects"
                    date_range = f"[{date_min} TO 2009-02-12]"
                elif search_date_type == "before":
                    predicate_type = "Intersects"
                    date_range = f"[1510-01-01 TO {date_min}]"
                else:
                    date_range = date_min
            if date_range:
                fq.append(f'{{!field f=dateRange op={predicate_type}}}{date_range}')
        else:
            set_params.pop("search-date-type", None)

        for name, value in set_params.items():
            #print('Checking %s' % name)
            if value:
                if name in remap_fields:
                    q.append(f'{name}:({utils.stringify(value)})')
                elif name in ["keyword"]:
                    q.append(f'({utils.stringify(value)})')
                elif re.match(r"^f[0-9]+-.+?$", name) and facets.get(name, {}).get("nested") is True:
                    field_name = facets.get(name).get("field")
                    val_list = utils.listify(value)
                    fields = [f"{field_name}-{i}" for i in range(facets.get(name, {}).get("max_depth") + 1)]
                    for val in sorted(val_list):
                        val_clean = re.sub(r'^"(.+?)"$', r'\1', val)
                        val_parts = val_clean.split("::")
                        num_parts = len(val_parts)
                        solr_name = fields[min(num_parts - 1, len(fields) - 1)]
                        for i in range(len(val_parts)+2):
                            filters[f"f.{field_name}-{str(i)}.facet.contains"] = "::".join(val_parts[: i + 1])
                            filters[f"f.{field_name}-{str(i)}.facet.limit"]=-1
                        fq.append(f'{solr_name}:"{val_clean}"')
                elif re.match(r"^f[0-9]+-.+?$", name):
                    solr_name = re.sub(r"^f[0-9]+-(.+?)$", r"facet-\1", name)
                    for x in utils.listify(value):
                        x_clean = re.sub(r'^"(.+?)"$', r'\1', x)
                        fq.append(f'{solr_name}:"{x_clean}"')
                elif re.match(r"^facet-.+?$", name):
                    value_clean = re.sub(r'^"(.+?)"$', r'\1', value)
                    fq.append(f'{name}:"{value_clean}"')
                elif name == "page":
                    page_val = int(value)
                    solr_params["start"] = (page_val - 1) * DEFAULT_ROWS
                elif name == "sort":
                    sort_val = value if value in ['sort-date', 'sort-date-desc', 'sort-shelfmark', 'sort-volume-name', 'sort-title'] else "score"
                    sort_order = "desc" if sort_val in ["score", "sort-date-desc"] else "asc"
                    solr_params["sort"] = f"{re.sub(r'-desc','',sort_val)} {sort_order}"
                elif name == "expand":
                    if value in ["volume-name", "shelfmark", "hands"]:
                        expand_clauses[f"f.facet-{value}.facet.limit"] = "-1"
                        expand_clauses[f"f.facet-{value}.facet.sort"] = "-1"
                elif not name in solr_delete + solr_fields:
                    q.append(f'{name}:({utils.stringify(value)})')

        final_q = " ".join(q)
        if final_q in ["['*']", "['']"]:
            final_q = "*"
        if not solr_params.get('sort'):
            solr_params['sort']= "score desc"
        solr_params["q"] = final_q if final_q not in ["['*']", "['']"] else "*"
        solr_params["fq"] = fq
        solr_params = {**solr_params, **filters, **expand_clauses}
        #print(solr_params)
        return solr_params
