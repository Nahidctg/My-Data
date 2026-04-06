# plugins/safety_shield.py
import __main__
import base64
import re

# --- 🔞 ১৮+ কিওয়ার্ড লিস্ট (আরও উন্নত করা হয়েছে) ---
ADULT_KEYWORDS = [
    "erotic", "porn", "sexy", "nudity", "adult", "18+", "uncut", "kink", 
    "sex", "brazzers", "web series", "hot scenes", "softcore", "nsfw"
]

# গুগল বটের জন্য একটি প্রফেশনাল সেফ ইমেজ
SAFE_PLACEHOLDER = "https://i.ibb.co/9TRmN8V/nsfw-placeholder.png"

def is_content_adult(data):
    if data.get('adult') is True or data.get('force_adult') is True:
        return True
    
    title = (data.get("title") or data.get("name") or "").lower()
    overview = (data.get("overview") or "").lower()
    
    for word in ADULT_KEYWORDS:
        if word in title or word in overview:
            return True
    return False

def encode_b64(text):
    return base64.b64encode(text.encode()).decode()

# --- 🛡️ MODERN SAFETY UI (Premium Glassmorphism) ---
def get_safety_shield_code(is_adult):
    if not is_adult:
        return "" 

    return f"""
    <style>
        /* মডার্ন ব্লার কন্টেইনার */
        .nsfw-masked {{
            position: relative !important;
            overflow: hidden !important;
            cursor: pointer !important;
            border-radius: 12px;
            background: #1a1a1a !important;
            min-height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }}

        .nsfw-masked:hover {{
            transform: scale(1.01);
        }}

        /* ইমেজ ব্লার এফেক্ট */
        .nsfw-masked img {{
            filter: blur(50px) grayscale(1) !important;
            opacity: 0.4 !important;
            transition: filter 0.8s ease, opacity 0.8s ease !important;
        }}

        /* ওপরের গ্লাস লেয়ার */
        .nsfw-overlay {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 10;
            color: #fff;
            transition: 0.5s ease;
            padding: 20px;
            text-align: center;
        }}

        .nsfw-icon {{
            font-size: 40px;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 10px #ff3b3b);
        }}

        .nsfw-text {{
            font-size: 18px;
            font-weight: 700;
            color: #ff4d4d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .nsfw-subtext {{
            font-size: 12px;
            color: #ccc;
            margin-top: 5px;
        }}

        /* আনমাস্ক হওয়ার পর */
        .nsfw-unmasked .nsfw-overlay {{
            opacity: 0 !important;
            visibility: hidden !important;
        }}

        .nsfw-unmasked img {{
            filter: blur(0px) grayscale(0) !important;
            opacity: 1 !important;
        }}

        /* DMCA Section */
        .dmca-footer {{
            margin-top: 40px;
            padding: 25px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            border: 1px dashed rgba(255, 255, 255, 0.1);
            font-size: 13px;
            color: #999;
            text-align: center;
            line-height: 1.6;
        }}
    </style>

    <script>
        function revealNSFW(el) {{
            const imgs = el.querySelectorAll('img');
            imgs.forEach(img => {{
                const encodedUrl = img.getAttribute('data-src');
                if (encodedUrl) {{
                    img.src = atob(encodedUrl);
                    img.removeAttribute('data-src');
                }}
            }});
            el.classList.add('nsfw-unmasked');
            // ৫ সেকেন্ড পর ওভারলে রিমুভ করে দেওয়া যাতে কন্টেন্ট দেখা যায়
            setTimeout(() => {{
                const overlay = el.querySelector('.nsfw-overlay');
                if(overlay) overlay.style.display = 'none';
            }}, 500);
            el.onclick = null;
        }}
    </script>
    
    <div class="dmca-footer">
        <b style="color:#eee;">⚖️ DMCA Disclaimer:</b> This portal only provides metadata and links. 
        We do not store files on our servers. Content is gathered from 3rd party APIs.
        <br><br>
        <a href="https://t.me/CineZoneBD1" style="background:#E50914; color:#fff; padding: 5px 15px; border-radius: 20px; text-decoration:none; font-size:11px;">REPORT CONTENT</a>
    </div>
    """

# ==========================================================
# 🔥 MONKEY PATCH & LOGIC REFINEMENT
# ==========================================================

if not hasattr(__main__, 'shield_old_html'):
    __main__.shield_old_html = __main__.generate_html_code

def safety_shield_generator(data, links, user_ads, owner_ads, share):
    is_adult = is_content_adult(data)
    html = __main__.shield_old_html(data, links, user_ads, owner_ads, share)
    
    if is_adult:
        # ইমেজ রিপ্লেসমেন্ট লজিক
        def secure_img_tags(match):
            full_tag = match.group(0)
            img_src = match.group(1)
            
            # লোগো বা টেলিগ্রাম বাটন বাদ দেওয়া
            if any(x in img_src for x in ["logo", "icon", "telegram", "button"]):
                return full_tag
            
            encoded_url = encode_b64(img_src)
            return f'src="{SAFE_PLACEHOLDER}" data-src="{encoded_url}"'

        html = re.sub(r'src="([^"]+)"', secure_img_tags, html)

        # সুন্দর ওভারলে লেয়ার যোগ করা
        nsfw_overlay_html = '''
        <div class="nsfw-overlay">
            <div class="nsfw-icon">🔞</div>
            <div class="nsfw-text">Adult Content</div>
            <div class="nsfw-subtext">Click to reveal the images</div>
        </div>
        '''

        # কন্টেইনার মডিফিকেশন
        if '<div class="info-poster">' in html:
            html = html.replace(
                '<div class="info-poster">', 
                f'<div class="info-poster nsfw-masked" onclick="revealNSFW(this)">{nsfw_overlay_html}'
            )
        
        if '<div class="screenshot-grid">' in html:
            html = html.replace(
                '<div class="screenshot-grid">', 
                f'<div class="screenshot-grid nsfw-masked" onclick="revealNSFW(this)">{nsfw_overlay_html}'
            )

    safety_code = get_safety_shield_code(is_adult)
    return f"{html}\n{safety_code}"

__main__.generate_html_code = safety_shield_generator

async def register(bot):
    print("🛡️ Premium Safety Shield (V2) Activated!")
