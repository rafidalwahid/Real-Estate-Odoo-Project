{
    "name": "Real Estate Ads",
    "version": "1.0",
    "author": "Rafid",
    "description": """
        Real Estate module to show available properties.
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/model_access.xml',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_offer_view.xml',
        'views/property_tag_view.xml',
        'views/menu_items.xml',

        # Data Files
        # 'data/property_type.xml'
        'data/estates.property.type.csv'
    ],
    'demo': [
        'demo/property_tag.xml'
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
