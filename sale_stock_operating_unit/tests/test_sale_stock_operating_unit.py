# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.sale_operating_unit.tests import test_sale_operating_unit


class TestSaleStockOperatingUnit(test_sale_operating_unit.
                                 TestSaleOperatingUnit):

    def setUp(self):
        super(TestSaleStockOperatingUnit, self).setUp()

    def test_security(self):
        """Test Sale Operating Unit"""
        # Confirm Sale1
        self.sale1.action_confirm()
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(self.sale1.operating_unit_id,
                         self.sale1.picking_ids.operating_unit_id,
                         'OU in Sale Order and Picking should be same')
        # Confirm Sale2
        self.sale2.action_confirm()
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(self.sale2.operating_unit_id,
                         self.sale2.picking_ids.operating_unit_id,
                         'OU in Sale Order and Picking should be same')
