import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_banner(output_path):
    # Render at 2x scale for ultra-crisp antialiasing, then downsample to 1200x630
    SCALE = 2
    W = 1200 * SCALE
    H = 630 * SCALE
    
    # 1. Base Canvas
    img = Image.new('RGBA', (W, H), (15, 23, 42, 255))
    
    # Create background gradient & ambient glows
    bg = Image.new('RGBA', (W, H), (15, 23, 42, 255))
    
    # Draw ambient color circles for glowing mesh gradient effect
    # Glow 1: Top-Left Purple (#714B67)
    glow1 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g1_draw = ImageDraw.Draw(glow1)
    g1_draw.ellipse([-200 * SCALE, -200 * SCALE, 700 * SCALE, 600 * SCALE], fill=(113, 75, 103, 190))
    glow1 = glow1.filter(ImageFilter.GaussianBlur(radius=160 * SCALE))
    
    # Glow 2: Bottom-Right Teal (#008784)
    glow2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g2_draw = ImageDraw.Draw(glow2)
    g2_draw.ellipse([600 * SCALE, 150 * SCALE, 1400 * SCALE, 800 * SCALE], fill=(0, 135, 132, 180))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=180 * SCALE))
    
    # Glow 3: Top-Right Violet Accent (#4F46E5)
    glow3 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g3_draw = ImageDraw.Draw(glow3)
    g3_draw.ellipse([800 * SCALE, -250 * SCALE, 1450 * SCALE, 350 * SCALE], fill=(79, 70, 229, 130))
    glow3 = glow3.filter(ImageFilter.GaussianBlur(radius=150 * SCALE))

    # Glow 4: Bottom-Left Emerald Accent (#10B981)
    glow4 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g4_draw = ImageDraw.Draw(glow4)
    g4_draw.ellipse([-100 * SCALE, 380 * SCALE, 450 * SCALE, 750 * SCALE], fill=(16, 185, 129, 110))
    glow4 = glow4.filter(ImageFilter.GaussianBlur(radius=140 * SCALE))

    # Composite glows onto background
    bg = Image.alpha_composite(bg, glow1)
    bg = Image.alpha_composite(bg, glow2)
    bg = Image.alpha_composite(bg, glow3)
    bg = Image.alpha_composite(bg, glow4)
    
    # Fonts
    FONT_DIR = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    font_bold = os.path.join(FONT_DIR, 'segoeuib.ttf')
    font_regular = os.path.join(FONT_DIR, 'segoeui.ttf')
    font_semibold = os.path.join(FONT_DIR, 'seguisb.ttf')
    if not os.path.exists(font_semibold):
        font_semibold = font_bold
        
    f_title = ImageFont.truetype(font_bold, 44 * SCALE)
    f_subtitle = ImageFont.truetype(font_regular, 21 * SCALE)
    f_badge_v = ImageFont.truetype(font_bold, 15 * SCALE)
    f_badge_feat = ImageFont.truetype(font_semibold, 16 * SCALE)
    f_footer = ImageFont.truetype(font_regular, 16 * SCALE)
    f_footer_bold = ImageFont.truetype(font_semibold, 16 * SCALE)
    
    # 2. Glassmorphic Card Container
    card_margin_x = 55 * SCALE
    card_margin_y = 45 * SCALE
    card_x1 = card_margin_x
    card_y1 = card_margin_y
    card_x2 = W - card_margin_x
    card_y2 = H - card_margin_y
    
    # Drop shadow behind card
    shadow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    shadow_draw.rounded_rectangle([card_x1, card_y1 + 10*SCALE, card_x2, card_y2 + 10*SCALE], radius=24*SCALE, fill=(0, 0, 0, 95))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=20*SCALE))
    bg = Image.alpha_composite(bg, shadow_layer)
    
    # Card surface with subtle border
    card_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    card_draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=24*SCALE, fill=(15, 23, 42, 150), outline=(255, 255, 255, 55), width=2*SCALE)
    
    bg = Image.alpha_composite(bg, card_layer)
    draw = ImageDraw.Draw(bg)
    
    # 3. App Icon
    icon_path = os.path.join(os.path.dirname(output_path), 'icon.png')
    if not os.path.exists(icon_path):
        icon_path = r"C:\Users\bottl\Documents\Custom Modul Odoo\user_role_sync\user_role_sync\static\description\icon.png"
        
    icon_size = 175 * SCALE
    icon_x = card_x1 + 45 * SCALE
    icon_y = card_y1 + 48 * SCALE
    
    if os.path.exists(icon_path):
        icon_img = Image.open(icon_path).convert('RGBA')
        icon_img = icon_img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        # Icon rounded card backdrop with shadow
        icon_bg = Image.new('RGBA', (icon_size + 24*SCALE, icon_size + 24*SCALE), (0, 0, 0, 0))
        ib_draw = ImageDraw.Draw(icon_bg)
        ib_draw.rounded_rectangle([0, 0, icon_size + 24*SCALE, icon_size + 24*SCALE], radius=28*SCALE, fill=(255, 255, 255, 245), outline=(255, 255, 255, 140), width=2*SCALE)
        
        # Paste icon inside
        icon_bg.paste(icon_img, (12*SCALE, 12*SCALE), icon_img)
        bg.paste(icon_bg, (int(icon_x - 12*SCALE), int(icon_y - 12*SCALE)), icon_bg)
    
    # 4. Header Content (Right of Icon)
    content_x = icon_x + icon_size + 40 * SCALE
    content_y = icon_y - 5 * SCALE
    
    # Version Pill Badges
    v_badges = [
        ("ODOO 16.0 • 17.0 • 18.0", (113, 75, 103), (255, 255, 255), (216, 180, 254)),
        ("COMMUNITY & ENTERPRISE", (16, 185, 129), (255, 255, 255), (110, 231, 183)),
    ]
    
    bx = content_x
    by = content_y
    for text, bg_color, text_color, border_color in v_badges:
        txt_len = draw.textlength(text, font=f_badge_v)
        pw = int(txt_len + 28 * SCALE)
        ph = 32 * SCALE
        # Draw pill with background and clear visible border
        draw.rounded_rectangle([bx, by, bx + pw, by + ph], radius=16*SCALE, fill=(*bg_color, 230), outline=border_color, width=int(1.5*SCALE))
        draw.text((bx + 14*SCALE, by + 6*SCALE), text, fill=text_color, font=f_badge_v)
        bx += pw + 14 * SCALE
        
    # Title
    title_y = by + 44 * SCALE
    draw.text((content_x, title_y), "User Role Sync from Excel", fill=(255, 255, 255), font=f_title)
    
    # Subtitle
    sub_y = title_y + 60 * SCALE
    draw.text((content_x, sub_y), "Bulk Import, Dynamic Matrix, & Intelligent Permission Recalculation", fill=(203, 213, 225), font=f_subtitle)
    
    # 5. Divider Line
    div_y = card_y1 + 250 * SCALE
    draw.line([card_x1 + 45*SCALE, div_y, card_x2 - 45*SCALE, div_y], fill=(255, 255, 255, 45), width=int(1.5*SCALE))
    
    # 6. Feature Chips / Badges Grid (High Contrast & Sharp)
    features = [
        # (Title, Accent Color)
        ("Dynamic App Matrix", (56, 189, 248)),
        ("Fuzzy User Matching", (167, 139, 250)),
        ("Auto-Create Roles", (52, 211, 153)),
        ("Interactive Preview Grid", (251, 191, 36)),
        ("Instant Group Recalculation", (56, 189, 248)),
        ("Bilingual ID / EN", (167, 139, 250)),
        ("Multi-Role Assignment", (52, 211, 153)),
        ("Openpyxl Direct Import", (251, 191, 36)),
    ]
    
    grid_start_x = card_x1 + 45 * SCALE
    grid_start_y = div_y + 30 * SCALE
    col_w = (card_x2 - card_x1 - 90 * SCALE - 3 * 18 * SCALE) // 4
    chip_h = 46 * SCALE
    
    for idx, (label, accent_col) in enumerate(features):
        row = idx // 4
        col = idx % 4
        cx1 = grid_start_x + col * (col_w + 18 * SCALE)
        cy1 = grid_start_y + row * (chip_h + 16 * SCALE)
        cx2 = cx1 + col_w
        cy2 = cy1 + chip_h
        
        # Draw pill card with dark glass fill + subtle colored border
        draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=10*SCALE, fill=(30, 41, 59, 220), outline=(*accent_col[:3], 100), width=int(1.5*SCALE))
        
        # Dot indicator
        dot_r = 4 * SCALE
        dot_cy = cy1 + chip_h // 2
        draw.ellipse([cx1 + 16*SCALE - dot_r, dot_cy - dot_r, cx1 + 16*SCALE + dot_r, dot_cy + dot_r], fill=accent_col)
        
        # Text
        draw.text((cx1 + 28*SCALE, cy1 + 11*SCALE), label, fill=(241, 245, 249), font=f_badge_feat)
        
    # 7. Footer Bar inside card
    footer_y = card_y2 - 45 * SCALE
    draw.line([card_x1 + 45*SCALE, footer_y - 15*SCALE, card_x2 - 45*SCALE, footer_y - 15*SCALE], fill=(255, 255, 255, 30), width=1*SCALE)
    
    # Left Footer: Company / Author
    draw.text((card_x1 + 45*SCALE, footer_y), "By CV. Anugerah Khair Arkananta", fill=(148, 163, 184), font=f_footer_bold)
    
    # Right Footer: License & Compatibility Info
    right_txt = "License: LGPL-3.0   •   Odoo 16.0 / 17.0 / 18.0"
    r_len = draw.textlength(right_txt, font=f_footer)
    draw.text((card_x2 - 45*SCALE - r_len, footer_y), right_txt, fill=(148, 163, 184), font=f_footer)
    
    # 8. Downsample to target 1200x630 using high quality Lanczos resampling
    final_banner = bg.resize((1200, 630), Image.Resampling.LANCZOS)
    
    # Save as optimized PNG
    final_banner.save(output_path, "PNG", optimize=True)
    print(f"Banner generated successfully at {output_path} (Size: {os.path.getsize(output_path)} bytes)")

if __name__ == '__main__':
    target = r"C:\Users\bottl\Documents\Custom Modul Odoo\user_role_sync\user_role_sync\static\description\banner.png"
    create_banner(target)
