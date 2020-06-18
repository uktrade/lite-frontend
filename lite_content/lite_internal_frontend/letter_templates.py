from enum import Enum


class LetterTemplatesPage:
    class PickTemplate:
        TITLE = "Select a template"
        BUTTON = "Continue"

    class Preview:
        TITLE = "Preview"
        BUTTON = "Save"

    TITLE = "Letter templates"
    ERROR = "Template preview is not available at this time"
    ADD_PARAGRAPH = "Add a new paragraph"
    NONE_FOUND = "There aren't any letter templates"


class VariableHelpPage:
    TITLE = "Use variables to personalise the text"
    DETAIL_COLUMN = "To get"
    PATH_COLUMN = "Use"
    EXAMPLE_COLUMN = "Examples of how the variable will appear on the final document"
    # This defines the list of links on the left of the Variable help page
    # Each name must correspond to a table variable name
    CONTENTS = [
        "Addressee",
        "Organisation",
        "Case_and_licence_details",
        "Applications",
        "End_user_advisory_query",
        "Goods_query",
        "End_user",
        "Consignee",
        "Ultimate_recipient",
        "Third_parties",
        "Goods",
        "ECJU_query",
        "Notes",
        "Sites",
        "External_locations",
        "Documents",
    ]


class VariableHelpPageTables(Enum):
    # Following is a custom format for the variable help page
    # Each cell is split with a |
    # Each line corresponds to a row in the table
    # Each variable corresponds to a table
    # The name of the variable defines the name of the table

    Addressee = """
        Name|{{ addressee.name }}|Anthony Lord (default is the submitter)
        Email address|{{ addressee.email }}|anthony@testemail.co.uk
        Address (only if an addressee is selected)|{{ addressee.address }}|
        Phone number (only if an addressee is selected)|{{ addressee.phone_number }}|020 7946 0001
    """

    Organisation = """
        Name|{{ organisation.name }}|
        EORI number|{{ organisation.eori_number }}|
        SIC code|{{ organisation.sic_number }}|
        VAT registration number|{{ organisation.vat_number }}|
        Company registration number|{{ organisation.registration_number }}|
        Primary site name|{{ organisation.primary_site.name }}|
        Address|{{ organisation.primary_site.address_line_1 }} \\n {{ organisation.primary_site.address_line_2 }}|
        Postcode|{{ organisation.primary_site.postcode }}|
        City|{{ organisation.primary_site.city }}|
        Region|{{ organisation.primary_site.region }}|
        Country|{{ organisation.primary_site.country.name }}|United Kingdom
        Country code|{{ organisation.primary_site.country.code }}|
    """

    Case_and_licence_details = """
        Reference|{{ case_reference }}|GBSIEL/2020/0000001/P
        Type|{{ case_type.type }}|‘Application’ or ‘Query’
        Licence or clearance category|{{ case_type.sub_type }}|‘Standard’, ‘Open’, ‘HMRC’, or ‘Exhibition clearance’
        Licence or clearance type|{{ case_type.reference }}|‘OIEL’, ‘OGEL’, or ‘SIEL’
        Date document generated|{{ current_date }}|20 June 2020
        Time document generated|{{ current_time }}|‘10:30’ or ‘14:55’
        Start date|{{ licence.start_date }}|20 June 2020
        End date|{{ licence.end_date }}|20 June 2020
        Duration|{{ licence.duration }}|24
    """

    Applications = """
        End use details|{{ details.end_use_details }}|As entered by applicant 
        Informed by ECJU to apply for a licence|{{ details.military_end_use_controls }}|‘Yes’ or ‘No’
        Reference on ECJU letter|{{ details.military_end_use_controls_reference }}|
        Informed by ECJU that goods may be used in WMD|{{ details.informed_wmd }}|‘Yes’ or ‘No’
        Reference on ECJU letter|{{ details.informed_wmd_reference }}|
        Exporter suspects goods may be used in WMD|{{ details.suspected_wmd }}|‘Yes’ or ‘No’
        Details of suspected WMD goods|{{ details.suspected_wmd_reference }}|As entered by applicant 
        European military goods received under a transfer licence|{{ details.eu_military }}|‘Yes’ or ‘No’
        Exporter compliant with terms of export limitations or obtained consent|{{ details.compliant_limitations_eu }}|‘Yes’ or ‘No’
        Details of not compliant|{{ details.compliant_limitations_eu_reference }}|As entered by applicant 
    """  # noqa

    Standard_applications = """
        Export type|{{ details.export_type }}|‘Permanent’ or ‘Temporary’
        Informed by Border Force or HMRC to apply|{{ details.has_been_informed }}|‘Yes’ or ‘No’
        Reference number on letter from Border Force or HMRC|{{ details.reference_number_on_information_form }}|CRE/2020/1234567
        If firearms included on application|{{ details.contains_firearm_goods }}|‘Yes’ or ‘No’
        If goods shipped on an air waybill or bill of lading|{{ details.shipped_waybill_or_lading }}|‘Yes’ or ‘No’
        Details of the route of the goods|{{ details.non_waybill_or_lading_route_details }}|
        Proposed return date|{{ details.proposed_return_date }}|20 June 2020
        Trade control activity|{{ details.trade_control_activity }}|
        Other trade control activity|{{ details.trade_control_activity_other }}|
        Trade control product category|{{ details.trade_control_product_categories }}|
        Goods type category|{{ details.goodstype_category }}|
        Reason it’s a temporary export|{{ details.temporary_export_details.temp_export_details }}|As entered by applicant 
        Goods to remain under exporters direct control|{{ details.temporary_export_details.is_temp_direct_control }}|‘Yes’ or ‘No’
        Details of who will be in control of the products|{{ details.temporary_export_details.temp_direct_control_details }}|As entered by applicant
        Proposed date the goods to return to the UK|{{ details.temporary_export_details.proposed_return_date }}|20 June 2020
        Goods descriptions|{{ goods.all.description }}|As entered by applicant
        Control list entries|{{ goods.all.control_list_entries }}|‘ML1a’ or ‘1D101’
        Total value of the goods|{{ goods.all.applied_for_value }}|
        Quantity of goods|{{ goods.all.applied_for_quantity }}|
        If the goods are controlled|{{ goods.all.is_controlled }}|‘Yes’ or ‘No’
        If the goods are to be incorporated|{{ goods.all.is_incorporated }}|
        Part number|{{ goods.all.part_number }}|As entered by applicant
    """

    Open_applications = """
        Export type|{{ details.export_type }}|‘Permanent’ or ‘Temporary’
        Informed by Border Force or HMRC to apply|{{ details.has_been_informed }}|‘Yes’ or ‘No’
        Reference number on letter from Border Force or HMRC|{{ details.reference_number_on_information_form }}|
        If firearms included on application|{{ details.contains_firearm_goods }}|‘Yes’ or ‘No’
        If goods shipped on an air waybill or bill of lading|{{ details.shipped_waybill_or_lading }}|‘Yes’ or ‘No’
        Details of the route of the goods|{{ details.non_waybill_or_lading_route_details }}|As entered by applicant
        Proposed return date|{{ details.proposed_return_date }}|20 June 2020
        Trade control activity|{{ details.trade_control_activity }}|
        Other trade control activity|{{ details.trade_control_activity_other }}|
        Trade control product category|{{ details.trade_control_product_categories }}|
        Goods type category|{{ details.goodstype_category }}|
        Reason it’s a temporary export|{{ details.temporary_export_details.temp_export_details }}|As entered by applicant
        Goods to remain under exporters direct control|{{ details.temporary_export_details.is_temp_direct_control }}|‘Yes’ or ‘No’
        Details of who will be in control of the products|{{ details.temporary_export_details.temp_direct_control_details }}|As entered by applicant
        Proposed date the goods to return to the UK|{{ details.temporary_export_details.proposed_return_date }}|20 June 2020
        Goods descriptions|{{ goods.all.description }}|As entered by applicant
        Control list entries|{{ goods.all.control_list_entries }}|‘ML1a’ or ‘1D101’
        If the goods are controlled|{{ goods.all.is_controlled }}|‘Yes’ or ‘No’
        |{{ goods.countries.country_a.description }}|
        |{{ goods.countries.country_a.control_list_entries }}|
        Destination country|{{ destinations.country.name }}|‘Abu Dhabi’ or ‘Zimbabwe’
        Country code|{{ destinations.country.code }}|
        Sector and contract types|{{ destinations.contract_types }}|‘Nuclear-related (trigger list items)’ or ‘Army’
        Other sector and contract type|{{ destinations.other_contract_type }}|As entered by applicant
    """

    Customs_query = """
        Query details|{{ details.query_reason }}|As entered by applicant
        If goods have departed UK|{{ details.have_goods_departed }}|‘Yes’ or ‘No’
    """

    Exhibition_clearance = """
        Exhibition name|{{ details.exhibition_title }}|As entered by applicant
        Exhibition start date|{{ details.first_exhibition_date }}|20 June 2020
        Date the clearance is needed|{{ details.required_by_date }}|20 June 2020
        Details as to why clearance is needed by this date|{{ details.reason_for_clearance }}|As entered by applicant
        Goods type|{{ goods.item_type }}|
        Other goods type|{{ goods.other_item_type }}|
    """

    F680_clearance = """
        Clearance type|{{ details.clearance_types }}|‘Market survey’, ‘Initial discussions and promotions’, ‘Demonstration in the UK to overseas customers’, ‘Demonstration overseas’, ‘Training’ or ‘Through life support’
        Expedited|{{ details.expedited }}|‘Yes’ or ‘No’
        Date the clearance is needed|{{ details.expedited_date }}|20 June 2020
        If there’s any foreign technology or information involved|{{ details.foreign_technology }}|‘Yes’ or ‘No’
        Details of foreign technology or information|{{ details.foreign_technology_description }}|As entered by applicant
        If local assembly or manufacture is required|{{ details.locally_manufactured }}|‘Yes’ or ‘No’
        Details of local assembly or manufacture|{{ details.locally_manufactured_description }}|As entered by applicant
        Goods are rated under MTCR|{{ details.mtcr_type }}|‘Yes, Category 1’, Yes, Category 2’, ‘No’ or ‘I don’t know’
        If there’s a requirement to release UK MOD owned EW data or information|{{ details.electronic_warfare_requirement }}|‘Yes’ or ‘No’
        If the goods are due to enter service with the UK armed forces|{{ details.uk_service_equipment }}|‘Yes’ or ‘No’
        Details of goods entering service with the UK armed forces|{{ details.uk_service_equipment_description }}|As entered by applicant
        How the goods are funded|{{ details.uk_service_equipment_type }}|‘MOD funded’, ‘Part MOD funded / part private venture’ or ‘Private venture’
        Total value of prospect|{{ details.prospect_value }}|
        Clearance level|{{ details.clearance_level }}|‘UK TOP SECRET’, ‘NATO CONFIDENTIAL’ or ‘OCCAR UNCLASSIFIED’
        End user clearance level|{{ end_user.clearance_level }}|‘UK TOP SECRET’, ‘NATO CONFIDENTIAL’ or ‘OCCAR UNCLASSIFIED’
        Descriptors, caveats and codewords|{{ end_user.descriptors }}|As entered by applicant
    """

    End_user_advisory_query = """
        Notes|{{ details.note }}|
        Reason for the query|{{ details.query_reason }}|
        Nature of the business|{{ details.nature_of_business }}|
        Contact name|{{ details.contact_name }}|Anthony Lord
        Contact email|{{ details.contact_email }}|anthony@testemail.co.uk
        Contact job title|{{ details.contact_job_title }}|Product owner
        Contact phone number|{{ details.contact_telephone }}|020 7946 0001
    """

    Goods_query = """
        Proposed control list entry|{{ details.control_list_entry }}|‘ML1a’ or ‘1D101’
        Details for CLC query|{{ details.clc_raised_reasons }}|As entered by applicant
        Details for PV grading application|{{ details.pv_grading_raised_reasons }}|As entered by applicant
        Goods description|{{ details.good.description }}|As entered by applicant
        Control list entry|{{ details.good.control_list_entries }}|‘ML1a’ or ‘1D101’
        If good is controlled|{{ details.good.is_controlled }}|‘Yes’, ‘No’ or ‘Don’t know’
        Part number|{{ details.good.part_number }}|As entered by applicant
        If responded to CLC query|{{ details.clc_responded }}|‘Yes’ or ‘No’
        If responded to PV grading|{{ details.pv_grading_responded }}|‘Yes’ or ‘No’
    """

    End_user = """
        |{{ end_user.name }}|
        |{{ end_user.type }}|
        |{{ end_user.address }}|
        |{{ end_user.country.name }}|
        |{{ end_user.country.code }}|
        |{{ end_user.website }}|
    """

    Consignee = """
        |{{ consignee.name }}|
        |{{ consignee.type }}|
        |{{ consignee.address }}|
        |{{ consignee.country.name }}|
        |{{ consignee.country.code }}|
        |{{ consignee.website }}|
    """

    Ultimate_recipient = """
        |{{ ultimate_end_users.name }}|
        |{{ ultimate_end_users.type }}|
        |{{ ultimate_end_users.address }}|
        |{{ ultimate_end_users.country.name }}|
        |{{ ultimate_end_users.country.code }}|
        |{{ ultimate_end_users.website }}|
    """

    Third_parties = """
        |{% for third_party in third_parties.all %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.all %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.all %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.all %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.all %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.all %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.all %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_agent_and_broker = """
        |{% for third_party in third_parties.agent %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.agent %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.agent %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.agent %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.agent %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.agent %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.agent %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_intermediate_consignee = """
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.intermediate_consignee %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """  # noqa

    Third_party_additional_end_user = """
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.additional_end_user %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_authorised_submitter = """
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.submitter %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_consultant = """
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.consultant %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_contact = """
        |{% for third_party in third_parties.contact %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.contact %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.contact %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.contact %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.contact %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.contact %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.contact %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_exporter = """
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Third_party_other = """
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.type }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.address }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.country.name }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.country.code }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.website }} \\n {% endfor %}|
        |{% for third_party in third_parties.exporter %} \\n {{ third_party.descriptors }} \\n {% endfor %}|
    """

    Goods = """
        |{% for good in goods.all %} \\n {{ good.description }} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {% for clc in good.control_list_entries %} \\n {{ clc }} \\n {% endfor %} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {{ good.applied_for_value }} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {{ good.applied_for_quantity }} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {{ good.is_controlled }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.all %} \\n {{ good.is_incorporated }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.all %} \\n {{ good.part_number }} \\n {% endfor %}|
        (Exhibition clearance only)|{% for good in goods.all %} \\n {{ good.item_type }} \\n {% endfor %}|
        (Exhibition clearance only)|{% for good in goods.all %} \\n {{ good.other_item_type }} \\n {% endfor %}|
    """

    Approved_goods = """
        |{% for good in goods.approved %} \\n {{ good.description }} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {% for clc in good.control_list_entries %} \\n {{ clc }} \\n {% endfor %} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.applied_for_value }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.applied_for_quantity }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.value }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.quantity }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.is_controlled }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.approved %} \\n {{ good.is_incorporated }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.approved %} \\n {{ good.part_number }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.reason }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.note }} \\n {% endfor %}|
        |{% for good in goods.approved %} \\n {{ good.proviso_reason }} \\n {% endfor %}|
    """

    Refused_goods = """
        |{% for good in goods.refused %} \\n {{ good.description }} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {% for clc in good.control_list_entries %} \\n {{ clc }} \\n {% endfor %} \\n {% endfor %}|
        |{% for good in goods.refused %} \\n {{ good.applied_for_value }} \\n {% endfor %}|
        |{% for good in goods.refused %} \\n {{ good.applied_for_quantity }} \\n {% endfor %}|
        |{% for good in goods.refused %} \\n {{ good.is_controlled }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.refused %} \\n {{ good.is_incorporated }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.refused %} \\n {{ good.part_number }} \\n {% endfor %}|
        |{% for good in goods.refused %} \\n {{ good.reason }} \\n {% endfor %}|
        |{% for good in goods.refused %} \\n {{ good.note }} \\n {% endfor %}|
    """

    NLR_goods = """
        |{% for good in goods.nlr %} \\n {{ good.description }} \\n {% endfor %}|
        |{% for good in goods.all %} \\n {% for clc in good.control_list_entries %} \\n {{ clc }} \\n {% endfor %} \\n {% endfor %}|
        |{% for good in goods.nlr %} \\n {{ good.applied_for_value }} \\n {% endfor %}|
        |{% for good in goods.nlr %} \\n {{ good.applied_for_quantity }} \\n {% endfor %}|
        |{% for good in goods.nlr %} \\n {{ good.is_controlled }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.nlr %} \\n {{ good.is_incorporated }} \\n {% endfor %}|‘Yes’ or ‘No’
        |{% for good in goods.nlr %} \\n {{ good.part_number }} \\n {% endfor %}|
        |{% for good in goods.nlr %} \\n {{ good.reason }} \\n {% endfor %}|
        |{% for good in goods.nlr %} \\n {{ good.note }} \\n {% endfor %}|
    """

    ECJU_query = """
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.question.text }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.question.user }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.question.date }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.question.time }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.response.text }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.response.user }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.response.date }} \\n {% endfor %}|
        |{% for ecju_query in ecju_queries %} \\n {{ ecju_query.response.time }} \\n {% endfor %}|
    """

    Notes = """
        |{% for note in notes %} \\n {{ note.text }} \\n {% endfor %}|
        |{% for note in notes %} \\n {{ note.user }} \\n {% endfor %}|
        |{% for note in notes %} \\n {{ note.date }} \\n {% endfor %}|
        |{% for note in notes %} \\n {{ note.time }} \\n {% endfor %}|
    """

    Sites = """
        Name|{% for site in sites %} \\n {{ site.name }} \\n {% endfor %}|
        Address|{% for site in sites %} \\n {{ site.address_line_1 }} \\n {% endfor %}|{{ sites.address_line_2 }}
        {{ sites.address_line_1 }}|{% for site in sites %} \\n {{ site.address_line_2 }} \\n {% endfor %}|
        Postcode|{% for site in sites %} \\n {{ site.postcode }} \\n {% endfor %}|
        City|{% for site in sites %} \\n {{ site.city }} \\n {% endfor %}|
        |{% for site in sites %} \\n {{ site.region }} \\n {% endfor %}|
        |{% for site in sites %} \\n {{ site.country.name }} \\n {% endfor %}|
        |{% for site in sites %} \\n {{ site.country. }} \\n {% endfor %}|
        |{% for site in sites %} \\n {{ site.code }} \\n {% endfor %}|
    """

    External_locations = """
        |{% for external_location in external_locations %} \\n {{ external_location.name }} \\n {% endfor %}|
        |{% for external_location in external_locations %} \\n {{ external_location.address }} \\n {% endfor %}|
        |{% for external_location in external_locations %} \\n {{ external_location.country.name }} \\n {% endfor %}|
        |{% for external_location in external_locations %} \\n {{ external_location.country.code }} \\n {% endfor %}|
    """

    Documents = """
        |{% for document in documents %} \\n {{ document.name }} \\n {% endfor %}|
        |{% for document in documents %} \\n {{ document.description }} \\n {% endfor %}|
    """
