import os
from PIL import Image, ImageDraw, ImageFont

# Canvas Configuration
WIDTH = 1000
HEIGHT = 580
BG_COLOR = (248, 250, 252) # Slate-50
HEADER_BG = (113, 75, 103) # Odoo Primary #714B67
HEADER_TEAL = (0, 135, 132) # Secondary #008784

FONT_DIR = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
FONT_REGULAR = os.path.join(FONT_DIR, 'segoeui.ttf')
FONT_BOLD = os.path.join(FONT_DIR, 'segoeuib.ttf')
FONT_MONO = os.path.join(FONT_DIR, 'consola.ttf')

font_title = ImageFont.truetype(FONT_BOLD, 20)
font_subtitle = ImageFont.truetype(FONT_REGULAR, 13)
font_tab = ImageFont.truetype(FONT_BOLD, 13)
font_h2 = ImageFont.truetype(FONT_BOLD, 16)
font_body = ImageFont.truetype(FONT_REGULAR, 13)
font_body_bold = ImageFont.truetype(FONT_BOLD, 13)
font_small = ImageFont.truetype(FONT_REGULAR, 11)
font_small_bold = ImageFont.truetype(FONT_BOLD, 11)
font_badge = ImageFont.truetype(FONT_BOLD, 10)
font_counter = ImageFont.truetype(FONT_BOLD, 22)
font_counter_lbl = ImageFont.truetype(FONT_BOLD, 10)

def draw_window_base(draw, active_tab_idx=0):
    # Background
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=(241, 245, 249))
    
    # Outer Window Card
    draw.rounded_rectangle([15, 15, WIDTH - 15, HEIGHT - 15], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Window Title Bar
    draw.rounded_rectangle([15, 15, WIDTH - 15, 65], radius=16, fill=(248, 250, 252))
    draw.rectangle([15, 50, WIDTH - 15, 65], fill=(248, 250, 252))
    draw.line([15, 65, WIDTH - 15, 65], fill=(226, 232, 240), width=1)
    
    # Traffic lights (macOS style window buttons)
    draw.ellipse([32, 35, 44, 47], fill=(239, 68, 68))
    draw.ellipse([52, 35, 64, 47], fill=(245, 158, 11))
    draw.ellipse([72, 35, 84, 47], fill=(16, 185, 129))
    
    # App Header Title
    draw.text((105, 33), "Odoo ERP  •  User Role Sync from Excel (.xlsx)  •  Interactive Workflow Demo", fill=(51, 65, 85), font=font_subtitle)
    
    # Tabs / Workflow Stepper Header
    tabs = [
        ("1. Excel Role Matrix", (16, 185, 129)),
        ("2. Wizard Upload", (113, 75, 103)),
        ("3. Preview & Select", (245, 158, 11)),
        ("4. Instant Recalculation", (0, 135, 132))
    ]
    
    tab_x = 30
    tab_y = 80
    for i, (tab_name, color) in enumerate(tabs):
        is_active = (i == active_tab_idx)
        w = 215
        h = 36
        if is_active:
            draw.rounded_rectangle([tab_x, tab_y, tab_x + w, tab_y + h], radius=8, fill=color)
            draw.text((tab_x + 15, tab_y + 9), tab_name, fill=(255, 255, 255), font=font_tab)
            # Active indicator
            draw.polygon([(tab_x + w//2 - 6, tab_y + h), (tab_x + w//2 + 6, tab_y + h), (tab_x + w//2, tab_y + h + 6)], fill=color)
        else:
            draw.rounded_rectangle([tab_x, tab_y, tab_x + w, tab_y + h], radius=8, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
            draw.text((tab_x + 15, tab_y + 9), tab_name, fill=(100, 116, 139), font=font_tab)
        tab_x += w + 20
        
    draw.line([30, 128, WIDTH - 30, 128], fill=(226, 232, 240), width=1)

def draw_cursor(draw, x, y, clicking=False):
    # Mouse cursor arrow
    pts = [(x, y), (x + 14, y + 14), (x + 8, y + 14), (x + 12, y + 23), (x + 9, y + 24), (x + 5, y + 15), (x, y + 18)]
    if clicking:
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], outline=(113, 75, 103), width=2)
    draw.polygon(pts, fill=(30, 41, 59), outline=(255, 255, 255))

def create_scene_1(cursor_pos=None, is_click=False):
    # SCENE 1: Excel Spreadsheet Role Matrix
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_window_base(draw, active_tab_idx=0)
    
    # Subheader Banner in Excel Style
    draw.rounded_rectangle([30, 142, WIDTH - 30, 185], radius=8, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((45, 154), "[XLSX]  user_roles_matrix.xlsx", fill=(6, 95, 70), font=font_body_bold)
    draw.text((290, 155), "Standard Role Assignment Matrix - Edit directly in MS Excel / Google Sheets", fill=(4, 120, 87), font=font_small)
    
    # Excel Table Container
    table_x = 30
    table_y = 195
    table_w = WIDTH - 60
    
    # Table Header (Excel Green Theme)
    draw.rectangle([table_x, table_y, table_x + table_w, table_y + 32], fill=(16, 149, 93))
    
    cols = [
        ("No", 45),
        ("Nama User (Name)", 180),
        ("Email / Login (Account Match)", 240),
        ("Jabatan (Job Position)", 160),
        ("Roles to Assign (Comma-separated)", 315)
    ]
    
    cur_x = table_x
    for title, w in cols:
        draw.text((cur_x + 10, table_y + 8), title, fill=(255, 255, 255), font=font_small_bold)
        cur_x += w
        if cur_x < table_x + table_w:
            draw.line([cur_x, table_y, cur_x, table_y + 32], fill=(14, 120, 75), width=1)
            
    rows = [
        ("1", "Ahmad Faisal", "ahmad.faisal@company.com", "Operational Manager", "Role Manager Operasional"),
        ("2", "Dewi Lestari", "dewi.lestari@company.com", "HR Specialist", "Role Staff HR, Role Internal"),
        ("3", "Budi Santoso", "budi.santoso@company.com", "Warehouse Lead", "Role Staff Gudang"),
        ("4", "Siti Rahma", "siti.rahma@company.com", "Finance Supervisor", "Role Supervisor Keuangan"),
        ("5", "Eko Prasetyo", "eko.prasetyo@company.com", "Sales Executive", "Role Staff Penjualan"),
        ("6", "Rian Hidayat", "rian.hidayat@company.com", "New Employee (Unregistered)", "Role Staff Operasional")
    ]
    
    row_y = table_y + 32
    for r_idx, row in enumerate(rows):
        bg = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252)
        if r_idx == 5:
            bg = (254, 242, 242) # highlight missing
            
        draw.rectangle([table_x, row_y, table_x + table_w, row_y + 32], fill=bg)
        draw.line([table_x, row_y + 32, table_x + table_w, row_y + 32], fill=(226, 232, 240), width=1)
        
        cur_x = table_x
        # Col 0: No
        draw.text((cur_x + 12, row_y + 8), row[0], fill=(100, 116, 139), font=font_small)
        cur_x += cols[0][1]
        
        # Col 1: Name
        draw.text((cur_x + 10, row_y + 8), row[1], fill=(15, 23, 42), font=font_small_bold)
        cur_x += cols[1][1]
        
        # Col 2: Email
        draw.text((cur_x + 10, row_y + 8), row[2], fill=(71, 85, 105), font=font_small)
        cur_x += cols[2][1]
        
        # Col 3: Job
        draw.text((cur_x + 10, row_y + 8), row[3], fill=(71, 85, 105), font=font_small)
        cur_x += cols[3][1]
        
        # Col 4: Roles Badge
        roles_text = row[4]
        # pill badges
        rx = cur_x + 8
        for role_item in roles_text.split(','):
            role_item = role_item.strip()
            badge_w = draw.textlength(role_item, font=font_badge) + 14
            draw.rounded_rectangle([rx, row_y + 6, rx + badge_w, row_y + 25], radius=4, fill=(237, 233, 254), outline=(196, 181, 253), width=1)
            draw.text((rx + 7, row_y + 8), role_item, fill=(109, 40, 217), font=font_badge)
            rx += badge_w + 6
            
        row_y += 32
        
    draw.rectangle([table_x, table_y, table_x + table_w, row_y], outline=(226, 232, 240), width=1)
    
    # Bottom Note Banner
    draw.rounded_rectangle([30, 440, WIDTH - 30, 545], radius=10, fill=(240, 249, 255), outline=(186, 230, 253), width=1)
    draw.text((50, 455), "💡 Multi-Strategy Matching Engine:", fill=(3, 105, 161), font=font_body_bold)
    draw.text((50, 480), "• Automatically matches Odoo users by Exact Login, Email Address, Contact Name, or Email Prefix.", fill=(14, 116, 144), font=font_small)
    draw.text((50, 500), "• Supports multi-role assignment in single cells with auto-creation of missing roles in Odoo.", fill=(14, 116, 144), font=font_small)
    draw.text((50, 520), "• Step 1: Upload this spreadsheet into Odoo to inspect the Verification Preview Grid.", fill=(14, 116, 144), font=font_small)

    if cursor_pos:
        draw_cursor(draw, cursor_pos[0], cursor_pos[1], is_click)
        
    return img

def create_scene_2(cursor_pos=None, is_click=False, btn_hover=False):
    # SCENE 2: Wizard Step 1 - Upload & Options
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_window_base(draw, active_tab_idx=1)
    
    # Wizard Modal Box
    wiz_x = 30
    wiz_y = 142
    wiz_w = WIDTH - 60
    
    # Wizard Header & Status Bar
    draw.rounded_rectangle([wiz_x, wiz_y, wiz_x + wiz_w, wiz_y + 46], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((wiz_x + 18, wiz_y + 13), "Step 1 / 3 : Upload Role Matrix File", fill=(30, 41, 59), font=font_h2)
    
    # Status bar indicator pills on right
    sb_x = wiz_x + wiz_w - 360
    draw.rounded_rectangle([sb_x, wiz_y + 10, sb_x + 90, wiz_y + 35], radius=6, fill=(113, 75, 103))
    draw.text((sb_x + 15, wiz_y + 15), "1. Draft", fill=(255, 255, 255), font=font_small_bold)
    
    draw.rounded_rectangle([sb_x + 100, wiz_y + 10, sb_x + 200, wiz_y + 35], radius=6, fill=(241, 245, 249))
    draw.text((sb_x + 115, wiz_y + 15), "2. Preview", fill=(148, 163, 184), font=font_small)
    
    draw.rounded_rectangle([sb_x + 210, wiz_y + 10, sb_x + 295, wiz_y + 35], radius=6, fill=(241, 245, 249))
    draw.text((sb_x + 225, wiz_y + 15), "3. Done", fill=(148, 163, 184), font=font_small)
    
    # Left Card: File Upload
    card1_x = wiz_x
    card1_y = 200
    card1_w = 420
    draw.rounded_rectangle([card1_x, card1_y, card1_x + card1_w, card1_y + 270], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((card1_x + 20, card1_y + 16), "Excel Spreadsheet File", fill=(51, 65, 85), font=font_body_bold)
    
    # File Dropzone Box
    draw.rounded_rectangle([card1_x + 20, card1_y + 48, card1_x + card1_w - 20, card1_y + 150], radius=8, fill=(240, 253, 244), outline=(134, 239, 172), width=1)
    draw.text((card1_x + 40, card1_y + 68), "📁 user_roles_matrix.xlsx", fill=(22, 101, 52), font=font_body_bold)
    draw.text((card1_x + 40, card1_y + 95), "Size: 24.8 KB  •  Format: Office Open XML", fill=(21, 128, 61), font=font_small)
    draw.text((card1_x + 40, card1_y + 118), "✓ File ready for structural verification", fill=(16, 185, 129), font=font_small_bold)
    
    # Download template helper
    draw.rounded_rectangle([card1_x + 20, card1_y + 165, card1_x + card1_w - 20, card1_y + 245], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((card1_x + 35, card1_y + 180), "Need a pre-filled blank spreadsheet?", fill=(71, 85, 105), font=font_small)
    draw.rounded_rectangle([card1_x + 35, card1_y + 204, card1_x + 230, card1_y + 232], radius=4, fill=(255, 255, 255), outline=(113, 75, 103), width=1)
    draw.text((card1_x + 48, card1_y + 210), "📥 Download Template (.xlsx)", fill=(113, 75, 103), font=font_small_bold)
    
    # Right Card: Sync Options & Config
    card2_x = wiz_x + 440
    card2_y = 200
    card2_w = wiz_w - 440
    draw.rounded_rectangle([card2_x, card2_y, card2_x + card2_w, card2_y + 270], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((card2_x + 20, card2_y + 16), "Synchronization Settings", fill=(51, 65, 85), font=font_body_bold)
    
    # Options list
    opts = [
        ("Template Type", "● Role Assignment Matrix    ○ App Permission Matrix"),
        ("Auto-Create Missing Roles", "☑ Enabled (Creates role in res.users.role automatically)"),
        ("Auto-Create Missing Users", "☐ Disabled (Safety mode: prevents creating phantom users)"),
        ("Default Role Prefix", "[ Role -                                               ]")
    ]
    
    opt_y = card2_y + 50
    for label, val in opts:
        draw.text((card2_x + 20, opt_y), label, fill=(100, 116, 139), font=font_small_bold)
        draw.text((card2_x + 20, opt_y + 18), val, fill=(30, 41, 59), font=font_small)
        opt_y += 48
        
    # Wizard Footer Action Bar
    draw.rounded_rectangle([wiz_x, 485, wiz_x + wiz_w, 545], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    # Button: Preview & Verify (Primary)
    btn_col = (86, 57, 78) if btn_hover else (113, 75, 103)
    draw.rounded_rectangle([wiz_x + 20, 496, wiz_x + 200, 534], radius=6, fill=btn_col)
    draw.text((wiz_x + 38, 506), "🔍  Preview & Verify", fill=(255, 255, 255), font=font_body_bold)
    
    # Cancel Button
    draw.rounded_rectangle([wiz_x + 215, 496, wiz_x + 305, 534], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((wiz_x + 235, 506), "Cancel", fill=(100, 116, 139), font=font_body)
    
    draw.text((wiz_x + 330, 507), "⚡ Instant preview without modifying any live user records.", fill=(100, 116, 139), font=font_small)

    if cursor_pos:
        draw_cursor(draw, cursor_pos[0], cursor_pos[1], is_click)
        
    return img

def create_scene_3(cursor_pos=None, is_click=False, btn_hover=False, uncheck_item=False):
    # SCENE 3: Wizard Step 2 - Verification Grid & Selective User Selection
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_window_base(draw, active_tab_idx=2)
    
    wiz_x = 30
    wiz_y = 142
    wiz_w = WIDTH - 60
    
    # Wizard Header & Status Bar
    draw.rounded_rectangle([wiz_x, wiz_y, wiz_x + wiz_w, wiz_y + 46], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((wiz_x + 18, wiz_y + 13), "Step 2 / 3 : Verification Grid & User Selection", fill=(30, 41, 59), font=font_h2)
    
    # Status bar indicator pills on right
    sb_x = wiz_x + wiz_w - 360
    draw.rounded_rectangle([sb_x, wiz_y + 10, sb_x + 90, wiz_y + 35], radius=6, fill=(241, 245, 249))
    draw.text((sb_x + 15, wiz_y + 15), "1. Draft", fill=(148, 163, 184), font=font_small)
    
    draw.rounded_rectangle([sb_x + 100, wiz_y + 10, sb_x + 200, wiz_y + 35], radius=6, fill=(245, 158, 11))
    draw.text((sb_x + 115, wiz_y + 15), "2. Preview", fill=(255, 255, 255), font=font_small_bold)
    
    draw.rounded_rectangle([sb_x + 210, wiz_y + 10, sb_x + 295, wiz_y + 35], radius=6, fill=(241, 245, 249))
    draw.text((sb_x + 225, wiz_y + 15), "3. Done", fill=(148, 163, 184), font=font_small)
    
    # Stat summary cards
    stat_cards = [
        ("TOTAL ROWS", "6", (241, 245, 249), (51, 65, 85)),
        ("SELECTED USERS", "5", (239, 246, 255), (29, 78, 216)),
        ("MATCHED IN ODOO", "5", (240, 253, 244), (22, 101, 52)),
        ("MISSING IN ODOO", "1", (254, 242, 242), (185, 28, 28))
    ]
    
    cx = wiz_x
    card_w = (wiz_w - 30) // 4
    for title, val, cbg, cfg in stat_cards:
        draw.rounded_rectangle([cx, 198, cx + card_w, 245], radius=8, fill=cbg, outline=(226, 232, 240), width=1)
        draw.text((cx + 12, 204), title, fill=cfg, font=font_counter_lbl)
        draw.text((cx + 12, 218), val, fill=cfg, font=font_counter)
        cx += card_w + 10
        
    # Table Header & Rows
    tbl_y = 255
    tbl_h = 220
    draw.rectangle([wiz_x, tbl_y, wiz_x + wiz_w, tbl_y + 28], fill=(248, 250, 252))
    draw.line([wiz_x, tbl_y + 28, wiz_x + wiz_w, tbl_y + 28], fill=(226, 232, 240), width=1)
    
    tcols = [
        ("SYNC", 50),
        ("EXCEL USER / EMAIL", 220),
        ("MATCH STATUS", 140),
        ("MATCHED ODOO USER", 190),
        ("ASSIGNED ROLES", 280)
    ]
    
    cur_x = wiz_x
    for title, w in tcols:
        draw.text((cur_x + 10, tbl_y + 7), title, fill=(100, 116, 139), font=font_small_bold)
        cur_x += w
        
    p_rows = [
        (True, "Ahmad Faisal (ahmad.faisal@co...)", "MATCHED", "Ahmad Faisal [Admin]", "Role Manager Operasional"),
        (True, "Dewi Lestari (dewi.lestari@co...)", "MATCHED", "Dewi Lestari [Internal]", "Role Staff HR, Role Internal"),
        (True, "Budi Santoso (budi.santoso@co...)", "MATCHED", "Budi Santoso [Internal]", "Role Staff Gudang"),
        (True, "Siti Rahma (siti.rahma@company...)", "MATCHED", "Siti Rahma [Internal]", "Role Supervisor Keuangan"),
        (True, "Eko Prasetyo (eko.prasetyo@co...)", "MATCHED", "Eko Prasetyo [Internal]", "Role Staff Penjualan"),
        (False, "Rian Hidayat (rian.hidayat@co...)", "MISSING", "None (Auto-Unchecked)", "Role Staff Operasional")
    ]
    
    ry = tbl_y + 28
    for r_idx, (checked, u_excel, status, u_match, roles) in enumerate(p_rows):
        bg = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252)
        if status == "MISSING":
            bg = (254, 242, 242)
            
        draw.rectangle([wiz_x, ry, wiz_x + wiz_w, ry + 27], fill=bg)
        draw.line([wiz_x, ry + 27, wiz_x + wiz_w, ry + 27], fill=(241, 245, 249), width=1)
        
        cur_x = wiz_x
        # Col 0: Checkbox toggle
        chk_box = [cur_x + 16, ry + 6, cur_x + 30, ry + 20]
        if checked:
            draw.rounded_rectangle(chk_box, radius=3, fill=(113, 75, 103))
            draw.text((cur_x + 19, ry + 6), "✓", fill=(255, 255, 255), font=font_badge)
        else:
            draw.rounded_rectangle(chk_box, radius=3, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
        cur_x += tcols[0][1]
        
        # Col 1: Excel User
        draw.text((cur_x + 10, ry + 6), u_excel, fill=(51, 65, 85), font=font_small)
        cur_x += tcols[1][1]
        
        # Col 2: Match Status Badge
        if status == "MATCHED":
            draw.rounded_rectangle([cur_x + 8, ry + 4, cur_x + 115, ry + 22], radius=4, fill=(220, 252, 231), outline=(134, 239, 172), width=1)
            draw.text((cur_x + 15, ry + 6), "✓ Found in Odoo", fill=(22, 101, 52), font=font_badge)
        else:
            draw.rounded_rectangle([cur_x + 8, ry + 4, cur_x + 125, ry + 22], radius=4, fill=(254, 226, 226), outline=(252, 165, 165), width=1)
            draw.text((cur_x + 14, ry + 6), "✕ Belum Ada di Odoo", fill=(185, 28, 28), font=font_badge)
        cur_x += tcols[2][1]
        
        # Col 3: Matched User
        draw.text((cur_x + 10, ry + 6), u_match, fill=(30, 41, 59) if status=="MATCHED" else (148, 163, 184), font=font_small_bold if status=="MATCHED" else font_small)
        cur_x += tcols[3][1]
        
        # Col 4: Roles
        rx = cur_x + 8
        for role_item in roles.split(','):
            role_item = role_item.strip()
            bw = draw.textlength(role_item, font=font_badge) + 12
            draw.rounded_rectangle([rx, ry + 4, rx + bw, ry + 22], radius=4, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
            draw.text((rx + 6, ry + 6), role_item, fill=(51, 65, 85), font=font_badge)
            rx += bw + 5
            
        ry += 27
        
    draw.rectangle([wiz_x, tbl_y, wiz_x + wiz_w, ry], outline=(226, 232, 240), width=1)
    
    # Wizard Footer Action Bar
    draw.rounded_rectangle([wiz_x, 485, wiz_x + wiz_w, 545], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    # Button: Confirm & Apply Roles (Primary Green/Teal)
    btn_col = (0, 99, 97) if btn_hover else (0, 135, 132)
    draw.rounded_rectangle([wiz_x + 20, 496, wiz_x + 235, 534], radius=6, fill=btn_col)
    draw.text((wiz_x + 36, 506), "⚡  Confirm & Apply Roles", fill=(255, 255, 255), font=font_body_bold)
    
    # Back to Options Button
    draw.rounded_rectangle([wiz_x + 250, 496, wiz_x + 365, 534], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((wiz_x + 265, 506), "Back to Upload", fill=(100, 116, 139), font=font_body)
    
    # Select / Deselect quick actions
    draw.text((wiz_x + 390, 507), "Select All  |  Deselect All  |  5 users ready to sync", fill=(71, 85, 105), font=font_small_bold)

    if cursor_pos:
        draw_cursor(draw, cursor_pos[0], cursor_pos[1], is_click)
        
    return img

def create_scene_processing(pulse_pct=0.5):
    # Transition Toast / Loading animation
    img = create_scene_3()
    draw = ImageDraw.Draw(img)
    
    # Darkened Backdrop Overlay
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (15, 23, 42, 100))
    img.paste(Image.blend(img.convert('RGBA'), overlay, 0.45).convert('RGB'), (0, 0))
    draw = ImageDraw.Draw(img)
    
    # Center Modal Box
    mw = 520
    mh = 160
    mx = (WIDTH - mw) // 2
    my = (HEIGHT - mh) // 2
    
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    
    # Spinner ring simulation
    draw.ellipse([mx + 30, my + 45, mx + 85, my + 100], fill=(241, 245, 249), outline=(226, 232, 240), width=4)
    draw.arc([mx + 30, my + 45, mx + 85, my + 100], start=int(pulse_pct * 360), end=int(pulse_pct * 360 + 160), fill=(113, 75, 103), width=5)
    
    draw.text((mx + 105, my + 40), "Synchronizing User Roles...", fill=(15, 23, 42), font=font_h2)
    draw.text((mx + 105, my + 68), "1. Writing res.users.role.line records...", fill=(100, 116, 139), font=font_small)
    draw.text((mx + 105, my + 88), "2. Executing user.set_groups_from_roles(force=True)...", fill=(0, 135, 132), font=font_small_bold)
    
    # Progress Bar
    bar_w = mw - 140
    draw.rounded_rectangle([mx + 105, my + 115, mx + 105 + bar_w, my + 125], radius=5, fill=(241, 245, 249))
    prog_w = int(bar_w * pulse_pct)
    draw.rounded_rectangle([mx + 105, my + 115, mx + 105 + prog_w, my + 125], radius=5, fill=(0, 135, 132))
    
    return img

def create_scene_4(cursor_pos=None, is_click=False, btn_hover=False):
    # SCENE 4: Wizard Step 3 - Done & Success Confirmation
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_window_base(draw, active_tab_idx=3)
    
    wiz_x = 30
    wiz_y = 142
    wiz_w = WIDTH - 60
    
    # Wizard Header & Status Bar
    draw.rounded_rectangle([wiz_x, wiz_y, wiz_x + wiz_w, wiz_y + 46], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((wiz_x + 18, wiz_y + 13), "Step 3 / 3 : Synchronization Completed Successfully", fill=(30, 41, 59), font=font_h2)
    
    # Status bar indicator pills on right
    sb_x = wiz_x + wiz_w - 360
    draw.rounded_rectangle([sb_x, wiz_y + 10, sb_x + 90, wiz_y + 35], radius=6, fill=(241, 245, 249))
    draw.text((sb_x + 15, wiz_y + 15), "1. Draft", fill=(148, 163, 184), font=font_small)
    
    draw.rounded_rectangle([sb_x + 100, wiz_y + 10, sb_x + 200, wiz_y + 35], radius=6, fill=(241, 245, 249))
    draw.text((sb_x + 115, wiz_y + 15), "2. Preview", fill=(148, 163, 184), font=font_small)
    
    draw.rounded_rectangle([sb_x + 210, wiz_y + 10, sb_x + 295, wiz_y + 35], radius=6, fill=(16, 185, 129))
    draw.text((sb_x + 225, wiz_y + 15), "3. Done", fill=(255, 255, 255), font=font_small_bold)
    
    # Big Success Banner Box
    draw.rounded_rectangle([wiz_x, 202, wiz_x + wiz_w, 310], radius=12, fill=(240, 253, 244), outline=(134, 239, 172), width=1)
    
    # Green Check Circle Icon
    draw.ellipse([wiz_x + 30, 226, wiz_x + 90, 286], fill=(16, 185, 129))
    draw.text((wiz_x + 46, 236), "✓", fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 34))
    
    draw.text((wiz_x + 110, 222), "5 Users Successfully Synchronized & Recalculated!", fill=(22, 101, 52), font=font_title)
    draw.text((wiz_x + 110, 252), "All role assignments have been committed to Odoo. Base security groups and implied permissions", fill=(21, 128, 61), font=font_body)
    draw.text((wiz_x + 110, 274), "were instantly updated across active sessions with force recalculation enabled.", fill=(21, 128, 61), font=font_body)
    
    # 3 Summary Cards
    cards = [
        ("👥 Active Users Updated", "5 Odoo Accounts", "Ahmad, Dewi, Budi, Siti, Eko", (239, 246, 255), (30, 64, 175)),
        ("🛡️ Roles Assigned", "7 Role Lines Added", "res.users.role.line synced", (245, 243, 255), (109, 40, 217)),
        ("⚡ Security Recalculation", "Instant Execution", "set_groups_from_roles (OK)", (236, 253, 245), (6, 95, 70))
    ]
    
    cx = wiz_x
    cw = (wiz_w - 20) // 3
    for title, h_txt, s_txt, cbg, cfg in cards:
        draw.rounded_rectangle([cx, 325, cx + cw, 465], radius=10, fill=cbg, outline=(226, 232, 240), width=1)
        draw.text((cx + 18, 340), title, fill=cfg, font=font_body_bold)
        draw.text((cx + 18, 375), h_txt, fill=(15, 23, 42), font=font_h2)
        draw.text((cx + 18, 410), s_txt, fill=(100, 116, 139), font=font_small)
        cx += cw + 10
        
    # Wizard Footer Action Bar
    draw.rounded_rectangle([wiz_x, 485, wiz_x + wiz_w, 545], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    # Button: View Synchronized Users (Primary)
    btn_col = (86, 57, 78) if btn_hover else (113, 75, 103)
    draw.rounded_rectangle([wiz_x + 20, 496, wiz_x + 245, 534], radius=6, fill=btn_col)
    draw.text((wiz_x + 36, 506), "👥  View Synchronized Users", fill=(255, 255, 255), font=font_body_bold)
    
    # Close Button
    draw.rounded_rectangle([wiz_x + 260, 496, wiz_x + 340, 534], radius=6, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((wiz_x + 280, 506), "Close", fill=(100, 116, 139), font=font_body)
    
    draw.text((wiz_x + 365, 507), "✓ Zero downtime • No user logout or restart required", fill=(16, 185, 129), font=font_small_bold)

    if cursor_pos:
        draw_cursor(draw, cursor_pos[0], cursor_pos[1], is_click)
        
    return img

def generate_gif(output_path):
    frames = []
    durations = []
    
    # --- SCENE 1: Excel Matrix (3.0 sec) ---
    # Static view
    frames.append(create_scene_1((500, 300), is_click=False))
    durations.append(1800)
    # Cursor moves to top right
    frames.append(create_scene_1((680, 220), is_click=False))
    durations.append(800)
    # Switch tab transition
    frames.append(create_scene_1((350, 95), is_click=True))
    durations.append(400)
    
    # --- SCENE 2: Wizard Upload (3.0 sec) ---
    # Static view
    frames.append(create_scene_2((400, 300), is_click=False, btn_hover=False))
    durations.append(1400)
    # Move to button
    frames.append(create_scene_2((140, 515), is_click=False, btn_hover=True))
    durations.append(800)
    # Click button
    frames.append(create_scene_2((140, 515), is_click=True, btn_hover=True))
    durations.append(600)
    
    # --- SCENE 3: Wizard Preview & Select (3.5 sec) ---
    # Static view of preview table
    frames.append(create_scene_3((500, 300), is_click=False, btn_hover=False))
    durations.append(1500)
    # Inspection on uncheck / row
    frames.append(create_scene_3((60, 422), is_click=False, btn_hover=False))
    durations.append(700)
    # Move to Confirm button
    frames.append(create_scene_3((140, 515), is_click=False, btn_hover=True))
    durations.append(800)
    # Click Confirm button
    frames.append(create_scene_3((140, 515), is_click=True, btn_hover=True))
    durations.append(500)
    
    # --- SCENE TRANSITION: Processing Pulse (1.2 sec) ---
    frames.append(create_scene_processing(pulse_pct=0.25))
    durations.append(300)
    frames.append(create_scene_processing(pulse_pct=0.60))
    durations.append(300)
    frames.append(create_scene_processing(pulse_pct=0.90))
    durations.append(300)
    frames.append(create_scene_processing(pulse_pct=1.0))
    durations.append(300)
    
    # --- SCENE 4: Wizard Done (3.5 sec) ---
    frames.append(create_scene_4((500, 300), is_click=False, btn_hover=False))
    durations.append(1800)
    frames.append(create_scene_4((140, 515), is_click=False, btn_hover=True))
    durations.append(900)
    frames.append(create_scene_4((140, 515), is_click=True, btn_hover=True))
    durations.append(800)
    
    print(f"Total frames: {len(frames)}, generating GIF...")
    
    # Optimize palette and save
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Successfully generated: {output_path} (Size: {os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    target = r"C:\Users\bottl\Documents\Custom Modul Odoo\user_role_sync\user_role_sync\static\description\demo.gif"
    generate_gif(target)
