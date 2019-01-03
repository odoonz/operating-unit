# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in MRP",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "version": "12.0.1.0.0",
    "author": "Graeme Gellatly",
    "license": "LGPL-3",
    "website": "https://github.com/odoonz/operating-unit",
    "category": "Sales Management",
    "depends": [
        "mrp",
        "operating_unit",
        "stock_operating_unit",
    ],
    "data": [
        'views/mrp_production.xml'
    ],
    'installable': True,
}
