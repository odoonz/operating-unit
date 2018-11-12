# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Orders",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "version": "12.0.1.0.0",
    "author": "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Purchase Management",
    "depends": ["purchase", "stock_operating_unit"],
    "license": "LGPL-3",
    "data": [
        "security/purchase_security.xml",
        "views/purchase_order_view.xml",
        "views/purchase_order_line_view.xml",
        "views/product_supplierinfo_view.xml",
        "views/res_config_settings_views.xml",
    ],
    "demo": [
        "demo/purchase_order_demo.xml",
    ],
    "installable": True,
}
