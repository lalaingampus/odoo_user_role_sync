# User Role Sync from Excel (`user_role_sync`)

<div align="center">

<img src="static/description/banner.png" alt="User Role Sync from Excel Banner" width="100%"/>

<br/><br/>

[![License: LGPL-3](https://img.shields.io/badge/licence-LGPL--3-blue.svg)](LICENSE)
[![Odoo Version](https://img.shields.io/badge/odoo-17.0-brightgreen.svg)](https://www.odoo.com)
[![Translation: i18n](https://img.shields.io/badge/i18n-ID%20%7C%20EN-purple.svg)](i18n/)

<br/>

[![Bahasa Indonesia](https://img.shields.io/badge/🇮🇩%20Bahasa%20Indonesia-Ganti%20ke%20ID-lightgrey?style=for-the-badge)](README.md)
[![English](https://img.shields.io/badge/🇬🇧%20English-Active-blue?style=for-the-badge)](README.en.md)

</div>

---

**User Role Sync from Excel** is an enterprise-grade Odoo 17 module that extends the OCA [`base_user_role`](https://github.com/OCA/server-auth) application. It provides an interactive 2-step verification wizard to import, map, verify, and batch-synchronize user access roles directly from Microsoft Excel spreadsheets (`.xlsx`).

---

## 🌟 Key Features

- 📊 **Dynamic Template Generator**: Automatically generates `.xlsx` spreadsheets tailored dynamically to all installed applications and security groups in your active Odoo database.
- 👁️ **2-Step Verification & Preview Table**: Review matched users, unregistered users, and resolved role matrices before committing changes to the database.
- 🔘 **Granular Row-by-Row Selection**: Selective synchronization with toggles per user row and bulk actions (*Select All Matched* / *Deselect All*).
- 🔍 **Multi-Strategy User Matching**: Resolves users automatically via login/username, email address, full name, or login prefix (before `@`).
- ➕ **Auto-create Missing Roles**: Automatically creates missing `res.users.role` records with assigned group access rights.
- 👤 **Auto-create Missing Users**: Optionally create new active `res.users` accounts directly from Excel spreadsheet rows.
- ⚡ **Instant Security Recalculation**: Immediately triggers `set_groups_from_roles(force=True)` to recalculate menus, ACL rules, and permissions.
- 🌐 **Multi-Language (i18n)**: Full native translations for English and Bahasa Indonesia via standard GNU gettext (`.po` / `.pot`).
- 🧩 **OCA Compliant**: Fully compatible with OCA `base_user_role` standard architecture.

---

## 📋 Requirements & Dependencies

### Odoo Modules:
- `base`
- `base_user_role` (OCA)

### Python Libraries:
- `openpyxl` (for reading and writing `.xlsx` files)

Install openpyxl via pip:
```bash
pip install openpyxl
```

---

## ⚙️ Configuration & Access Rights

Ensure the user accessing the wizard has:
- **Administration / Access Rights** or **Administration / Settings** permission.

---

## 🚀 Usage Guide

### 1. Open the Wizard
Navigate to **Settings** > **Users & Companies** > **Sync Roles from Excel**.

### 2. Step 1: Upload & Options (Draft Step)
- *(Optional)* Choose the template format (*Application Permission Matrix* or *Role Assignment Matrix*) and click **Download Excel Template**.
- Fill in user details and permission levels in the downloaded `.xlsx` template.
- Upload your completed file in the **Excel File (.xlsx)** field.
- Configure options:
  - **Auto-create Missing Roles**: Enable to create missing roles automatically.
  - **Auto-create Missing Users**: Enable to auto-create user login accounts for unregistered users.
  - **Auto Role Prefix**: Prefix for generated role names (default: `Role -`).
- Click **Load & Preview Data**.

### 3. Step 2: Verification & Review (Preview Step)
- Review the interactive dashboard cards (**Total Rows**, **Selected**, **Ready to Process**, **Unregistered**).
- Verify user matching statuses:
  - 🟢 **Found in Odoo**: User matched and ready to sync.
  - 🟡 **To Be Created**: User will be created automatically.
  - 🔴 **Not in Odoo**: User not found (can be manually selected in the dropdown).
- Select/deselect specific rows or use bulk buttons.
- Click **Confirm & Apply Roles**.

### 4. Step 3: Result Summary (Done Step)
- Review the execution summary with the count of updated users and created accounts.
- Click **View Synchronized Users** to inspect the updated roles directly on user forms.

---

## 📁 Excel Template Formats

### Format 1: Application Permission Matrix (Recommended)
| Name | Email / Login | Job / Dept | Role Name (Optional) | Sales | Purchase | Inventory | Accounting |
|------|---------------|------------|----------------------|-------|----------|-----------|------------|
| John Doe | john@company.com | Sales Lead | Role - Sales Lead | Create, Read, Edit | Read Only | - | - |
| Jane Smith | jane@company.com | Admin Staff | Role - Admin Staff | Read Only | Create, Read, Edit | Read Only | - |

*Supported Permission Values:*
- `Create, Read, Edit` / `Manager` / `Admin` / `Full`: Manager/full rights to the module.
- `Read Only` / `User` / `View`: Standard user read-only/view access.
- `-` / `None` / Blank: No access granted.

### Format 2: Role Assignment Matrix (Direct Role Mapping)
| Name | Email / Login | Job / Dept | Target Roles (Comma-separated) | Is Enabled (True/False) |
|------|---------------|------------|--------------------------------|-------------------------|
| John Doe | john@company.com | Sales Lead | Role Sales Lead, Role Inventory | True |
| Jane Smith | jane@company.com | Admin Staff | Role Admin Staff | True |

---

## 👥 Contributors & Maintainers

* **CV. Anugerah Khair Arkananta** (<info@arkananta.id>)
* Repository: [https://github.com/lalaingampus/odoo_user_role_sync](https://github.com/lalaingampus/odoo_user_role_sync)

---

## 📄 License

This module is licensed under **LGPL-3.0** or later.  
See [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.html) for details.
