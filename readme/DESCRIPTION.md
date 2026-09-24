# User Role Sync from Excel

This module extends the functionality of `base_user_role` by providing a user-friendly wizard to import and synchronize user roles in batch from an Excel spreadsheet (.xlsx).

### Key Features
* Batch assignment of user roles from Excel.
* Automatic role creation if not already present in the system.
* Flexible matching by User Login, Email, or Full Name (case-insensitive).
* Instant application of security groups (`set_groups_from_roles`).
* Built-in template generator to download ready-to-use Excel templates.
* Interactive summary report detailing processed, updated, and missing users.
