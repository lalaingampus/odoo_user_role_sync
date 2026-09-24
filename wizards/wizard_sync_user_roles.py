# Copyright 2026 CV. Anugerah Khair Arkananta
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

import base64
import io
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    _logger.debug("Cannot import 'openpyxl'. Please install it via pip.")
    openpyxl = None
    Font = None
    PatternFill = None
    Alignment = None
    Border = None
    Side = None
    get_column_letter = None
    DataValidation = None


class WizardSyncUserRoles(models.TransientModel):
    _name = "wizard.sync.user.roles"
    _description = "Wizard Synchronize User Roles from Excel"

    file_excel = fields.Binary(
        string="Excel File (.xlsx)",
        required=False,
    )
    filename = fields.Char(string="File Name")

    template_type = fields.Selection(
        selection=[
            ("roles_list", "Role Assignment Matrix (Standard User-to-Roles)"),
            ("app_matrix", "Application Permission Matrix (Auto-detect Installed Apps)"),
        ],
        string="Template Format",
        default="app_matrix",
        help="Choose whether to generate template based on existing Roles or dynamically discovered installed Applications.",
    )

    auto_create_role = fields.Boolean(
        string="Auto-create Missing Roles",
        default=True,
        help="If enabled, roles found in the spreadsheet that do not exist yet in Odoo will be automatically created.",
    )

    default_role_prefix = fields.Char(
        string="Auto Role Prefix",
        default="Role -",
        help="Prefix used when creating dynamic roles based on job/department or permissions.",
    )

    role_logistic_id = fields.Many2one(
        comodel_name="res.users.role",
        string="Role Logistic (Optional)",
    )
    role_staff_pc_id = fields.Many2one(
        comodel_name="res.users.role",
        string="Role Staff & PC (Optional)",
    )

    line_ids = fields.One2many(
        comodel_name="wizard.sync.user.roles.line",
        inverse_name="wizard_id",
        string="Preview Baris Data",
    )

    total_rows = fields.Integer(
        string="Total Baris",
        compute="_compute_counts",
    )
    matched_rows = fields.Integer(
        string="User Ditemukan",
        compute="_compute_counts",
    )
    missing_rows = fields.Integer(
        string="User Belum Ada",
        compute="_compute_counts",
    )
    selected_rows = fields.Integer(
        string="Dipilih",
        compute="_compute_counts",
    )

    result_summary = fields.Html(
        string="Ringkasan Hasil Sinkronisasi",
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Upload File"),
            ("preview", "Pengecekan & Verifikasi"),
            ("done", "Selesai"),
        ],
        string="Status",
        default="draft",
    )

    @api.depends("line_ids", "line_ids.user_status", "line_ids.is_selected")
    def _compute_counts(self):
        for rec in self:
            rec.total_rows = len(rec.line_ids)
            rec.matched_rows = len(rec.line_ids.filtered(lambda l: l.user_status == "matched"))
            rec.missing_rows = len(rec.line_ids.filtered(lambda l: l.user_status == "missing"))
            rec.selected_rows = len(rec.line_ids.filtered(lambda l: l.is_selected and l.user_status == "matched"))

    def _get_active_app_categories(self):
        """Mendeteksi seluruh kategori aplikasi/modul yang aktif di database ini secara dinamis."""
        Category = self.env["ir.module.category"].sudo()
        Group = self.env["res.groups"].sudo()

        categories = Category.search([
            ("visible", "=", True),
        ], order="sequence, name")

        valid_categories = []
        seen_names = set()
        for cat in categories:
            grps = Group.search([("category_id", "=", cat.id)])
            if grps and cat.name and cat.name.strip() not in seen_names:
                valid_categories.append(cat)
                seen_names.add(cat.name.strip())

        return valid_categories

    def _parse_permission_level(self, text_val):
        """Menganalisis teks izin pada kolom Excel secara universal."""
        if not text_val:
            return {"is_none": True, "is_manager": False, "is_user": False}

        t = str(text_val).strip().lower()
        if t in ["-", "none", "no access", "tidak ada", "0", "false", "n/a", "no", ""]:
            return {"is_none": True, "is_manager": False, "is_user": False}

        is_manager = any(w in t for w in ["manager", "admin", "full", "creat", "edit", "write", "ubah", "tambah", "semua", "all"])
        is_user = any(w in t for w in ["user", "read", "view", "lihat", "baca", "own", "sendiri"]) or not is_manager

        return {
            "is_none": False,
            "is_manager": is_manager,
            "is_user": is_user,
        }

    def _find_groups_for_category(self, category_record, perm):
        """Mencari security group Odoo dari ir.module.category berdasarkan level izin."""
        Group = self.env["res.groups"].sudo()
        grps = Group.search([("category_id", "=", category_record.id)], order="sequence asc, id asc")
        if not grps:
            return []

        if perm.get("is_none"):
            return []

        if len(grps) == 1:
            return [grps[0].id]

        if perm.get("is_manager"):
            return [grps[-1].id]
        else:
            return [grps[0].id]

    def action_download_template(self):
        """Menghasilkan file template Excel secara 100% DINAMIS berdasarkan aplikasi/role di database Odoo saat ini."""
        if not openpyxl:
            raise UserError(
                _("The 'openpyxl' Python library is required to generate templates.")
            )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "User Roles"

        thin_border = Border(
            left=Side(style="thin", color="D3D3D3"),
            right=Side(style="thin", color="D3D3D3"),
            top=Side(style="thin", color="D3D3D3"),
            bottom=Side(style="thin", color="D3D3D3"),
        )
        header_fill = PatternFill(start_color="714B67", end_color="714B67", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

        if self.template_type == "roles_list":
            headers = [
                "Nama User",
                "Email/Login",
                "Jabatan/Dept",
                "Roles (Pisahkan Koma Jika Banyak)",
                "Is Enabled (True/False)",
            ]
            ws.append(headers)

            existing_roles = self.env["res.users.role"].sudo().search([], limit=5)
            role_example = ", ".join(r.name for r in existing_roles[:2]) if existing_roles else "Role Manager, Role Staff"

            ws.append(["Contoh User A", "user.a@example.com", "Manager", role_example, "True"])
            ws.append(["Contoh User B", "user.b@example.com", "Staff", "Role Staff Standard", "True"])

            for _ in range(15):
                ws.append(["", "", "", "", "True"])

        else:
            base_headers = ["Nama User", "Email/Login", "Jabatan/Dept", "Role Name (Opsional)"]
            active_cats = self._get_active_app_categories()
            app_headers = [cat.name for cat in active_cats]

            if not app_headers:
                app_headers = ["Sales", "Purchase", "Inventory", "Accounting", "Employees", "Project"]

            headers = base_headers + app_headers
            ws.append(headers)

            sample_row_manager = ["Contoh Manager / Lead", "manager@example.com", "Manager", "Role Manager Operasional"]
            sample_row_staff = ["Contoh Staff Standard", "staff@example.com", "Staff", "Role Staff Standard"]

            for _ in app_headers:
                sample_row_manager.append("Create, Read, Edit")
                sample_row_staff.append("Read Only")

            ws.append(sample_row_manager)
            ws.append(sample_row_staff)

            for _ in range(15):
                ws.append(["", "", "", ""] + [""] * len(app_headers))

            if DataValidation and len(headers) > 4:
                start_col = get_column_letter(5)
                end_col = get_column_letter(len(headers))
                dv = DataValidation(
                    type="list",
                    formula1='"Create, Read, Edit,Read Only,-"',
                    allow_blank=True,
                    showDropDown=True,
                    showErrorMessage=True,
                    errorTitle="Nilai Tidak Valid",
                    error="Pilih salah satu dari: 'Create, Read, Edit', 'Read Only', atau '-'"
                )
                ws.add_data_validation(dv)
                dv.add(f"{start_col}2:{end_col}100")

        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_align
            cell.border = thin_border
        ws.row_dimensions[1].height = 28

        for row in ws.iter_rows(min_row=2, max_row=20, min_col=1, max_col=len(headers)):
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(vertical="center")

        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 16)

        # Sheet 2: Petunjuk
        ws_info = wb.create_sheet(title="Petunjuk Pengisian")
        ws_info.append(["PANDUAN PENGISIAN TEMPLATE AKSES USER ROLE"])
        ws_info.append([])
        ws_info.append(["Kolom", "Keterangan", "Pilihan Nilai"])
        ws_info.append(["Nama User", "Nama lengkap user di Odoo", "Teks Bebas"])
        ws_info.append(["Email/Login", "Username login atau email user", "user@company.com / username"])
        ws_info.append(["Jabatan/Dept", "Posisi atau divisi user", "Staff, Manager, Supervisor, dll."])
        ws_info.append(["Role Name (Opsional)", "Nama Role yang ingin dipasangkan/dibuat", "Bisa dikosongkan untuk auto-generate"])
        ws_info.append(["Kolom Aplikasi/Modul", "Izin akses per aplikasi Odoo yang terpasang:", ""])
        ws_info.append(["", "• Create, Read, Edit (atau Manager / Full)", "Hak akses penuh (buat, ubah, lihat)"])
        ws_info.append(["", "• Read Only (atau User / View)", "Hak akses melihat saja"])
        ws_info.append(["", "• - (atau kosong / None)", "Tidak memiliki akses ke modul tersebut"])

        ws_info.cell(row=1, column=1).font = Font(size=13, bold=True, color="714B67")
        ws_info.row_dimensions[1].height = 25
        info_header_fill = PatternFill(start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")
        for col_idx in range(1, 4):
            c = ws_info.cell(row=3, column=col_idx)
            c.fill = info_header_fill
            c.font = Font(bold=True)
            c.border = thin_border

        for col in ws_info.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws_info.column_dimensions[col_letter].width = max(max_len + 4, 20)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        file_base64 = base64.b64encode(output.getvalue())

        attachment = self.env["ir.attachment"].create(
            {
                "name": "Template_User_Role_Sync.xlsx",
                "type": "binary",
                "datas": file_base64,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "res_model": self._name,
                "res_id": self.id,
            }
        )

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }

    # =========================================================================
    # STEP 1: PARSE & LOAD DATA TO PREVIEW TABLE
    # =========================================================================
    def action_load_preview(self):
        """Membaca file Excel dan menampilkan tabel preview untuk diverifikasi user terlebih dahulu."""
        self.ensure_one()
        if not self.file_excel:
            raise UserError(_("Harap pilih file Excel terlebih dahulu."))

        if not openpyxl:
            raise UserError(_("Library 'openpyxl' dibutuhkan untuk membaca file Excel."))

        try:
            file_data = base64.b64decode(self.file_excel)
            wb = openpyxl.load_workbook(io.BytesIO(file_data), data_only=True)
            ws = wb.active
        except Exception as e:
            raise UserError(_("Gagal membaca file Excel. Pastikan format file .xlsx valid.\nError: %s") % str(e))

        # Bersihkan baris preview sebelumnya jika ada
        self.line_ids.unlink()

        User = self.env["res.users"].sudo()
        Role = self.env["res.users.role"].sudo()
        Category = self.env["ir.module.category"].sudo()
        Group = self.env["res.groups"].sudo()

        headers = [
            str(cell.value).strip() if cell.value is not None else ""
            for cell in ws[1]
        ]

        col_map = {}
        dynamic_app_cols = {}
        all_categories = Category.search([])
        cat_by_name = {c.name.lower().strip(): c for c in all_categories}

        for idx, h in enumerate(headers):
            if not h:
                continue
            h_clean = h.lower().replace(" ", "").replace("/", "").replace("_", "")
            
            # Map standard base columns without allowing app category columns to overwrite them
            if "name" not in col_map and ("nama" in h_clean or "name" in h_clean) and not any(k in h_clean for k in ["role", "email", "login", "marketing", "type", "app", "category", "akses"]):
                col_map["name"] = idx
            elif "login" not in col_map and ("login" in h_clean or "email" in h_clean or "username" in h_clean) and not any(k in h_clean for k in ["marketing", "role", "app"]):
                col_map["login"] = idx
            elif "role" not in col_map and any(k in h_clean for k in ["role", "roles", "peran", "hakakses"]):
                col_map["role"] = idx
            elif "job" not in col_map and any(k in h_clean for k in ["jabatan", "dept", "depart", "job", "posisi", "divisi", "position", "title"]):
                col_map["job"] = idx
            elif "enabled" not in col_map and any(k in h_clean for k in ["enabled", "active", "aktif", "statusaktif", "isactive", "isenabled"]):
                col_map["enabled"] = idx
            else:
                matched_cat = None
                h_original_lower = h.lower().strip()
                if h_original_lower in cat_by_name:
                    matched_cat = cat_by_name[h_original_lower]
                else:
                    for c_name, cat in cat_by_name.items():
                        if c_name in h_original_lower or h_original_lower in c_name:
                            matched_cat = cat
                            break

                dynamic_app_cols[idx] = {
                    "header": h,
                    "category": matched_cat,
                }

        name_idx = col_map.get("name", 0)
        login_idx = col_map.get("login", 1)
        role_col_idx = col_map.get("role", None)
        job_idx = col_map.get("job", None)
        enabled_idx = col_map.get("enabled", None)

        lines_to_create = []

        for row_idx, row in enumerate(
            ws.iter_rows(min_row=2, values_only=True), start=2
        ):
            if not row or all(v is None or str(v).strip() == "" for v in row):
                continue

            user_name = (
                str(row[name_idx]).strip()
                if name_idx is not None and len(row) > name_idx and row[name_idx] is not None
                else ""
            )
            user_login = (
                str(row[login_idx]).strip()
                if login_idx is not None and len(row) > login_idx and row[login_idx] is not None
                else ""
            )
            user_job = (
                str(row[job_idx]).strip()
                if job_idx is not None and len(row) > job_idx and row[job_idx] is not None
                else ""
            )
            is_enabled = True
            if enabled_idx is not None and len(row) > enabled_idx and row[enabled_idx] is not None:
                is_enabled = str(row[enabled_idx]).strip().lower() not in ["false", "0", "no", "disabled", "nonaktif", "tidak"]

            if not user_name and not user_login:
                continue

            # Target Role String
            detected_roles = []
            if role_col_idx is not None and len(row) > role_col_idx and row[role_col_idx]:
                roles_str = str(row[role_col_idx]).strip()
                detected_roles = [r.strip() for r in roles_str.split(",") if r.strip()]

            perm_snippets = []
            for col_idx, app_info in dynamic_app_cols.items():
                if len(row) > col_idx and row[col_idx] is not None:
                    val_str = str(row[col_idx]).strip()
                    perm = self._parse_permission_level(val_str)
                    if not perm.get("is_none"):
                        h_title = app_info.get("header")
                        level_title = "Full" if perm.get("is_manager") else "Read"
                        perm_snippets.append(f"{h_title}: {level_title}")

            if not detected_roles:
                if user_job:
                    detected_roles = [f"{self.default_role_prefix} {user_job}".strip()]
                else:
                    detected_roles = [f"{self.default_role_prefix} Standard User".strip()]

            # Cari user di Odoo dengan multi-strategi pencarian
            user = False
            UserCtx = User.with_context(active_test=False)

            # 1. Exact match Login, Email, atau Name
            domain = []
            if user_login:
                domain.extend([("login", "=ilike", user_login), ("email", "=ilike", user_login)])
            if user_name:
                domain.append(("name", "=ilike", user_name))
            
            if domain:
                if len(domain) > 1:
                    full_domain = ["|"] * (len(domain) - 1) + domain
                else:
                    full_domain = domain
                user = UserCtx.search(full_domain, limit=1)

            # 2. Match short login (bagian sebelum @ pada email)
            if not user and user_login and "@" in user_login:
                short_login = user_login.split("@")[0].strip()
                user = UserCtx.search([
                    "|",
                    "|",
                    ("login", "=ilike", short_login),
                    ("email", "=ilike", short_login),
                    ("name", "=ilike", short_login),
                ], limit=1)

            # 3. Match login berdasarkan nama atau sebaliknya
            if not user and user_name:
                user = UserCtx.search([("login", "=ilike", user_name)], limit=1)
            if not user and user_login:
                user = UserCtx.search([("name", "=ilike", user_login)], limit=1)

            user_status = "matched" if user else "missing"

            lines_to_create.append({
                "wizard_id": self.id,
                "row_index": row_idx,
                "is_selected": True if user_status == "matched" else False,
                "name_excel": user_name or "-",
                "login_excel": user_login or "-",
                "job_excel": user_job or "-",
                "user_id": user.id if user else False,
                "user_status": user_status,
                "role_names": ", ".join(detected_roles),
                "permissions_summary": " | ".join(perm_snippets[:5]) + (" ..." if len(perm_snippets) > 5 else ""),
                "is_enabled": is_enabled,
            })

        if not lines_to_create:
            raise UserError(_("Tidak ada data baris user yang valid di dalam file Excel."))

        self.env["wizard.sync.user.roles.line"].create(lines_to_create)
        self.write({"state": "preview"})
        return self._reopen_wizard()

    def _reopen_wizard(self):
        self.ensure_one()
        self.invalidate_recordset()
        view = self.env.ref("user_role_sync.view_wizard_sync_user_roles_form", raise_if_not_found=False)
        return {
            "name": _("Sync Roles from Excel"),
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "view_id": view.id if view else False,
            "views": [(view.id if view else False, "form")],
            "target": "new",
            "context": dict(self.env.context),
        }

    def action_select_all(self):
        """Memilih seluruh baris user yang cocok di Odoo."""
        self.ensure_one()
        matched_lines = self.line_ids.filtered(lambda l: l.user_status == "matched" or bool(l.user_id))
        if matched_lines:
            matched_lines.write({"is_selected": True})
        else:
            self.line_ids.write({"is_selected": True})
        return self._reopen_wizard()

    def action_deselect_all(self):
        """Membatalkan pilihan seluruh baris."""
        self.ensure_one()
        self.line_ids.write({"is_selected": False})
        return self._reopen_wizard()

    def action_back_to_upload(self):
        """Kembali ke mode upload untuk mengganti file jika preview belum sesuai."""
        self.ensure_one()
        self.line_ids.unlink()
        self.write({"state": "draft"})
        return self._reopen_wizard()

    # =========================================================================
    # STEP 2: CONFIRM & APPLY ROLES TO RES.USERS
    # =========================================================================
    def action_apply_sync(self):
        """Menerapkan role yang sudah diverifikasi ke database dan tab User Roles pada res.users."""
        self.ensure_one()
        if not self.line_ids:
            raise UserError(_("Tidak ada data yang dapat disinkronkan. Silakan muat file Excel terlebih dahulu."))

        selected_lines = self.line_ids.filtered(lambda l: l.is_selected and l.user_id)
        if not selected_lines:
            raise UserError(_("Tidak ada baris user yang dipilih untuk disinkronkan. Silakan centang minimal satu user yang berstatus 'Ditemukan di Odoo'."))

        Role = self.env["res.users.role"].sudo()
        RoleLine = self.env["res.users.role.line"].sudo()
        Group = self.env["res.groups"].sudo()
        Category = self.env["ir.module.category"].sudo()

        base_user_group = self.env.ref("base.group_user", raise_if_not_found=False)

        updated_users = []
        assigned_count = 0

        for line in selected_lines:
            user = line.user_id
            target_role_names = [r.strip() for r in (line.role_names or "").split(",") if r.strip()]
            
            user_target_roles = []
            for r_name in target_role_names:
                r_rec = Role.search([("name", "=ilike", r_name)], limit=1)
                if not r_rec and self.auto_create_role:
                    r_rec = Role.create({"name": r_name})
                    if base_user_group:
                        r_rec.write({"implied_ids": [(4, base_user_group.id)]})
                if r_rec:
                    user_target_roles.append(r_rec)

            for t_role in user_target_roles:
                role_line = RoleLine.search(
                    [
                        ("user_id", "=", user.id),
                        ("role_id", "=", t_role.id),
                    ],
                    limit=1,
                )

                if not role_line:
                    RoleLine.create(
                        {
                            "user_id": user.id,
                            "role_id": t_role.id,
                            "is_enabled": line.is_enabled,
                        }
                    )
                    assigned_count += 1
                else:
                    if role_line.is_enabled != line.is_enabled:
                        role_line.write({"is_enabled": line.is_enabled})
                        assigned_count += 1

            # Terapkan perubahan ke grup security Odoo
            user.set_groups_from_roles(force=True)
            if user.id not in [u.id for u in updated_users]:
                updated_users.append(user)

        # HTML Summary
        summary_html = f"""
        <div style="font-family: sans-serif; font-size: 13px;">
            <div style="padding: 15px; background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; border-radius: 6px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; margin-bottom: 8px;">✓ Sinkronisasi Role Berhasil Diterapkan!</h4>
                <p style="margin: 0; font-size: 14px;">
                    Total <strong>{len(updated_users)} User</strong> berhasil disinkronkan dan hak aksesnya telah aktif pada tab <strong>User Roles</strong>.
                </p>
            </div>
            <p class="text-muted">
                Anda dapat melihat hasil pembaruan langsung pada menu <strong>Settings &gt; Users &amp; Companies &gt; Users</strong> (Tab <em>User Roles</em>).
            </p>
        </div>
        """

        self.write({
            "result_summary": summary_html,
            "state": "done",
        })
        return self._reopen_wizard()

    def action_view_updated_users(self):
        """Membuka view res.users untuk mengecek langsung tab User Roles pada user-user yang di-update."""
        self.ensure_one()
        matched_user_ids = self.line_ids.mapped("user_id").ids
        return {
            "name": _("User yang Berhasil Disinkronkan"),
            "type": "ir.actions.act_window",
            "res_model": "res.users",
            "view_mode": "tree,form",
            "domain": [("id", "in", matched_user_ids)],
            "target": "current",
        }


class WizardSyncUserRolesLine(models.TransientModel):
    _name = "wizard.sync.user.roles.line"
    _description = "Preview Baris Sinkronisasi User Role"
    _order = "row_index asc"

    wizard_id = fields.Many2one(
        comodel_name="wizard.sync.user.roles",
        string="Wizard Parent",
        ondelete="cascade",
    )
    row_index = fields.Integer(string="Baris")
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User Cocok di Odoo",
    )
    name_excel = fields.Char(string="Nama (Excel)")
    login_excel = fields.Char(string="Email / Login (Excel)")
    job_excel = fields.Char(string="Jabatan / Dept")
    user_status = fields.Selection(
        selection=[
            ("matched", "Ditemukan di Odoo"),
            ("missing", "Belum Ada di Odoo"),
        ],
        string="Status User",
        default="matched",
    )
    is_selected = fields.Boolean(
        string="Pilih",
        default=True,
        help="Centang untuk menyinkronkan user ini ke Odoo.",
    )
    role_names = fields.Char(string="Target Role(s)")
    permissions_summary = fields.Char(string="Izin Modul Dinamis")
    is_enabled = fields.Boolean(string="Role Aktif", default=True)
