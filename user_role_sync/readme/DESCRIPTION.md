# User Role Sync from Excel

This module extends the functionality of `base_user_role` by providing a robust, user-friendly wizard to import, map, and batch-synchronize user access roles from Microsoft Excel spreadsheets (.xlsx).

### Key Features
* **Granular Row Selection:** Selectively sync specific users using inline toggle switches and bulk selection buttons.
* **2-Step Verification Preview:** Review matched accounts, missing users, and target roles in an interactive grid before live application.
* **Dynamic Template Generator:** Generates Excel templates with dropdown selectors dynamically mapped to installed Odoo apps.
* **Automatic Role Provisioning:** Automatically creates missing roles in `res.users.role` with base user permissions.
* **Multi-Strategy User Matching:** Matches users case-insensitively by Login, Email, or Full Name.
* **Instant Group Application:** Enforces menu visibility and record rules immediately via `set_groups_from_roles()`.
* **OCA base_user_role Compatible:** 100% compliant with OCA standard architecture.
