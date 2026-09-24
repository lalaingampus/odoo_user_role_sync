# Copyright 2026 CV. Anugerah Khair Arkananta
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

{
    "name": "User Role Sync from Excel",
    "summary": "Import and synchronize user roles from Excel spreadsheet",
    "version": "18.0.1.0.0",
    "category": "Administration",
    "website": "https://github.com/lalaingampus/odoo_user_role_sync",
    "author": "CV. Anugerah Khair Arkananta",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "auto_install": False,
    "depends": [
        "base",
        "base_user_role",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/wizard_sync_user_roles_views.xml",
    ],
    "external_dependencies": {
        "python": [
            "openpyxl",
        ],
    },
}
