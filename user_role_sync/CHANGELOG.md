# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [17.0.1.0.0] - 2026-09-24

### Added
- **Dynamic Excel Template Generator**:
  - Auto-detection of all active application categories (`ir.module.category`) installed in the Odoo database.
  - Generates Excel templates dynamically with styled headers, guidance notes, and dropdown validations (`openpyxl`).
  - Supports two template formats: *Role Assignment Matrix* and *Application Permission Matrix*.
- **Intelligent User & Role Parser**:
  - Fuzzy and multi-strategy matching for user detection (Login, Email, Name, and short usernames).
  - Universal permission level parsing (Manager/Admin, User/Read, and No Access).
  - Dynamic mapping from application permission columns to standard Odoo security groups (`res.groups`).
- **Preview & Verification Wizard**:
  - Interactive verification table with state indicators (`Matched`, `To Be Created`, `Missing`).
  - Option to manually select/deselect rows and assign Odoo users inline.
  - Option `auto_create_role` to automatically create non-existing roles.
  - Option `auto_create_user` to automatically create new user accounts in Odoo.
- **Role Synchronization Engine**:
  - Automated role assignment and updates on `res.users.role.line`.
  - Immediate trigger of `set_groups_from_roles(force=True)` to recalculate user security groups.
  - Detailed summary screen with visual status and direct navigation to updated user records.
- **Multilingual Support**:
  - Comprehensive translations in English (`pot`), Indonesian (`id.po`, `id_ID.po`).
- **Comprehensive Unit Tests**:
  - Full test suite covering template generation, file parsing, user matching, and role synchronization.
