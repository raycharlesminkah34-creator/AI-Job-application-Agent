from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from tools.apply import save_to_pdf
import time

def detect_captcha(page):
    """Detects captcha on a particular page and returns a bool"""
    captcha_signals = [
    "iframe[src*='recaptcha']",
    "iframe[src*='hcaptcha']",
    ".g-recaptcha",
    ".h-captcha",
    "#captcha",
    "[class*='captcha']",
    "[id*='captcha']",
]

    for selector in captcha_signals:
        try:
            if page.query_selector(selector):
                return True
        except Exception:
            continue

    return False


def fill_fields(page, field_map):
    field_selectors = {
        "name":  ["input[name*='name']", "input[placeholder*='name']", "input[id*='name']"],
        "email": ["input[type='email']", "input[name*='email']", "input[placeholder*='email']"],
        "phone": ["input[type='tel']", "input[name*='phone']", "input[placeholder*='phone']"],
    }

    for field, selectors in field_selectors.items():
        value = field_map.get(field)
        if not value:
            continue
        
        for selector in selectors:
            try:
                el = page.query_selector(selector)
                if el:
                    el.fill(value)
                    print(f"  ✓ Filled: {field}")
                    break
            except Exception:
                continue


def click_submit(page):

    submit_selectors = [
        "button[type='submit']",
        "input[type='submit']",
        "button:has-text('Apply')",
        "button:has-text('Submit')",
        "button:has-text('Send Application')",
    ]

    for selector in submit_selectors:
        try:
            el = page.query_selector(selector)
            if el:
                el.click()
                print("Submitted successfully")
                return True
        except Exception:
            print("COuldn't submit application. User should do it manually")

        
    return False


def upload_cv(page, cv_pdf):

     upload_selectors = [
        "input[type='file']",
        "input[name*='resume']",
        "input[name*='cv']",
        "input[accept*='pdf']",
    ]
     for selector in upload_selectors:
        try:
            el = page.query_selector(selector)
            if el:
                el.set_input_file(cv_pdf)
                print("Cv uploaded")
                return True
        except Exception:
            continue
        print("CV not found")
        return False
     

def auto_apply(job_url: str, tailored_cv: str, user_info: dict):
    print(f"Opening browser for {job_url}....")
    cv_pdf = save_to_pdf(tailored_cv)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        try:
            page.go_to(job_url, timeout=30000)
            print("Page loaded.")
            time.sleep(2)

            page.fill_field(page, user_info)
            print("Filling fields...")

            page.upload_cv(page, cv_pdf)
            print("Uploading cv...")
            time.sleep(1)

            if detect_captcha(page):
                print("\n⚠️  CAPTCHA detected!")
                print("👉 Solve the CAPTCHA in the browser window.")
                input("   Press Enter here when done to continue...")
            else:
                print("\n  ✓ No CAPTCHA detected")

            submitted = click_submit(page)
            if submitted:
                results = f"Application submitted successfully to {job_url}"
            else:
                input("Submit button not found. Submitmanually and press Enter")
                results = f"Application manually submitted to {job_url}"

        except PlaywrightTimeoutError:
            results = f"Timed out loading {job_url}"
        except Exception as e:
            results = f"Error during application: str(e)"

        finally:
            input("Press Enter to close browser")
            browser.close()





    
