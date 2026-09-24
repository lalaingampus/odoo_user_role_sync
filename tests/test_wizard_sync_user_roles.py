# Copyright 2026 CV. Anugerah Khair Arkananta
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

import base64
import io

from odoo.exceptions import UserError
from odoo.tests import common

try:
    import openpyxl
except ImportError:
    openpyxl = None


class TestWizardSyncUserRoles(common.TransactionCase):
    """Unit tests for WizardSyncUserRoles in user_role_sync module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Wizard = cls.env["wizard.sync.user.roles"]
        cls.WizardLine = cls.env["wizard.sync.user.roles.line"]
        cls.User = cls.env["res.users"]
        cls.Role = cls.env["res.users.role"]
        cls.RoleLine = cls.env["res.users.role.line"]

        # Sample test role
        cls.test_role_mgr = cls.Role.create({
            "name": "Test Manager Role",
        })
        cls.test_role_staff = cls.Role.create({
            "name": "Test Staff Role",
        })

        # Sample test user
        cls.test_user = cls.User.create({
            "name": "Alice Test User",
            "login": "alice.test@example.com",
            "email": "alice.test@example.com",
        })

    def _create_test_xlsx_base64(self, rows):
        """Helper to create an in-memory XLSX file encoded in base64."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "User Roles"
        for row in rows:
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return base64.b64encode(output.getvalue())

    def test_01_download_template_roles_list(self):
        """Test downloading template in roles_list mode."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        wizard = self.Wizard.create({
            "template_type": "roles_list",
        })
        action = wizard.action_download_template()
        self.assertIn("url", action)
        self.assertIn("/web/content/", action["url"])

    def test_02_download_template_app_matrix(self):
        """Test downloading template in app_matrix mode."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        wizard = self.Wizard.create({
            "template_type": "app_matrix",
        })
        action = wizard.action_download_template()
        self.assertIn("url", action)
        self.assertIn("/web/content/", action["url"])

    def test_03_load_preview_and_match_user(self):
        """Test preview loading and user matching by login and email."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        rows = [
            ["Nama User", "Email/Login", "Jabatan/Dept", "Roles (Pisahkan Koma Jika Banyak)", "Is Enabled"],
            ["Alice Test User", "alice.test@example.com", "Accounting", "Test Manager Role", "True"],
            ["Bob Nonexistent", "bob.missing@example.com", "Sales", "Test Staff Role", "True"],
        ]
        b64_file = self._create_test_xlsx_base64(rows)

        wizard = self.Wizard.create({
            "file_excel": b64_file,
            "filename": "test_roles.xlsx",
            "auto_create_user": False,
        })
        wizard.action_load_preview()

        self.assertEqual(wizard.state, "preview")
        self.assertEqual(len(wizard.line_ids), 2)

        # Alice should be matched
        alice_line = wizard.line_ids.filtered(lambda l: l.login_excel == "alice.test@example.com")
        self.assertTrue(alice_line)
        self.assertEqual(alice_line.user_status, "matched")
        self.assertEqual(alice_line.user_id, self.test_user)
        self.assertTrue(alice_line.is_selected)

        # Bob should be missing and not selected by default
        bob_line = wizard.line_ids.filtered(lambda l: l.login_excel == "bob.missing@example.com")
        self.assertTrue(bob_line)
        self.assertEqual(bob_line.user_status, "missing")
        self.assertFalse(bob_line.user_id)
        self.assertFalse(bob_line.is_selected)

    def test_04_apply_sync_role_assignment(self):
        """Test applying role synchronization to matched users."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        rows = [
            ["Nama User", "Email/Login", "Jabatan/Dept", "Roles (Pisahkan Koma Jika Banyak)", "Is Enabled"],
            ["Alice Test User", "alice.test@example.com", "Accounting", "Test Manager Role, Test Staff Role", "True"],
        ]
        b64_file = self._create_test_xlsx_base64(rows)

        wizard = self.Wizard.create({
            "file_excel": b64_file,
            "filename": "test_roles.xlsx",
        })
        wizard.action_load_preview()
        wizard.action_apply_sync()

        self.assertEqual(wizard.state, "done")
        self.assertIn("Role Synchronization Successfully Applied", wizard.result_summary)

        # Verify role line assignments on res.users
        role_lines = self.RoleLine.search([("user_id", "=", self.test_user.id)])
        assigned_role_names = role_lines.mapped("role_id.name")
        self.assertIn("Test Manager Role", assigned_role_names)
        self.assertIn("Test Staff Role", assigned_role_names)

    def test_05_auto_create_missing_role(self):
        """Test auto-creation of new roles when enabled."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        new_role_name = "Dynamic Custom Auto Role 2026"
        self.assertFalse(self.Role.search([("name", "=", new_role_name)]))

        rows = [
            ["Nama User", "Email/Login", "Jabatan/Dept", "Roles (Pisahkan Koma Jika Banyak)", "Is Enabled"],
            ["Alice Test User", "alice.test@example.com", "IT", new_role_name, "True"],
        ]
        b64_file = self._create_test_xlsx_base64(rows)

        wizard = self.Wizard.create({
            "file_excel": b64_file,
            "filename": "test_auto_role.xlsx",
            "auto_create_role": True,
        })
        wizard.action_load_preview()
        wizard.action_apply_sync()

        created_role = self.Role.search([("name", "=", new_role_name)])
        self.assertTrue(created_role)

    def test_06_auto_create_missing_user(self):
        """Test auto-creation of missing user accounts when enabled."""
        if not openpyxl:
            self.skipTest("openpyxl is not installed")

        new_login = "charlie.newuser@example.com"
        self.assertFalse(self.User.search([("login", "=", new_login)]))

        rows = [
            ["Nama User", "Email/Login", "Jabatan/Dept", "Roles (Pisahkan Koma Jika Banyak)", "Is Enabled"],
            ["Charlie New User", new_login, "Marketing", "Test Staff Role", "True"],
        ]
        b64_file = self._create_test_xlsx_base64(rows)

        wizard = self.Wizard.create({
            "file_excel": b64_file,
            "filename": "test_auto_user.xlsx",
            "auto_create_user": True,
        })
        wizard.action_load_preview()
        wizard.action_apply_sync()

        created_user = self.User.search([("login", "=", new_login)])
        self.assertTrue(created_user)
        self.assertEqual(created_user.name, "Charlie New User")

    def test_07_validation_errors(self):
        """Test wizard error handling on invalid operations."""
        wizard = self.Wizard.create({})

        # Loading preview without file must raise UserError
        with self.assertRaises(UserError):
            wizard.action_load_preview()

        # Applying sync without lines must raise UserError
        with self.assertRaises(UserError):
            wizard.action_apply_sync()
