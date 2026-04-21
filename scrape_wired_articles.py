import json
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

urls = [
    "https://www.wired.com/sponsored/story/ai-is-set-to-revolutionise-corporate-hr/",
    "https://www.wired.com/sponsored/story/medicines-ai-evolution/",
    "https://www.wired.com/story/book-excerpt-a-world-appears-michael-pollan/",
    "https://www.wired.com/sponsored/story/omidyar-the-big-interview/",
    "https://www.wired.com/sponsored/story/the-ai-gap-is-widening/",
    "https://www.wired.com/sponsored/story/the-rise-of-rogue-ai/",
    "https://www.wired.com/sponsored/story/banking-gets-more-personal-with-ai/",
    "https://www.wired.com/sponsored/story/employment-hero-why-ai-is-now-hrs-business/",
    "https://www.wired.com/sponsored/story/flexera/",
    "https://www.wired.com/sponsored/story/sports-brands-and-ai-a-winning-combination/",
    "https://www.wired.com/sponsored/story/the-new-ai-marketing-playbook-tremendous/",
    "https://www.wired.com/sponsored/story/how-ai-assistants-are-transforming-the-workforce/",
    "https://www.wired.com/sponsored/story/the-geopolitics-of-ai/",
    "https://www.wired.com/sponsored/story/sponsored/story/small-businesses-ai-to-work-sage/",
    "https://www.wired.com/sponsored/story/future-of-compliance-policy-as-code-kyndryl/",
    "https://www.wired.com/sponsored/story/jetbrains/",
    "https://www.wired.com/sponsored/story/esker/",
    "https://www.wired.com/sponsored/story/ai-and-the-human-side-of-health-innovation/",
    "https://www.wired.com/sponsored/story/ai-is-reinventing-the-way-creative-teams-work-dropbox/",
    "https://www.wired.com/sponsored/story/agentic-ai-businesses-thoughtworks/",
    "https://www.wired.com/contributor-content/story/how-ai-is-helping-pet-owners-monitor-health-changes/",
    "https://www.wired.com/sponsored/story/ai-is-booming-but-the-debates-are-just-beginning-ibm/",
    "https://www.wired.com/sponsored/story/three-milestones-that-will-make-ai-agents-ubiquitous/",
    "https://www.wired.com/sponsored/story/keyrus/",
    "https://www.wired.com/sponsored/story/the-10x-challenge-how-ai-factories-are-redefining-energy-infrastructure/",
    "https://www.wired.com/contributor-content/story/why-customer-service-operations-are-turning-to-modern-ai-tools/",
    "https://www.wired.com/sponsored/story/ai-is-making-our-volatile-planet-more-predictable/",
    "https://www.wired.com/contributor-content/story/ai-and-machine-learning-for-personalization-in-ecommerce/",
    "https://www.wired.com/sponsored/story/the-real-reason-ai-isnt-working-for-your-company/",
    "https://www.wired.com/sponsored/story/adobe-just-supercharged-generative-ai-for-creators/",
    "https://www.wired.com/sponsored/story/ces-is-loud-the-future-of-ai-will-be-quiet/",
    "https://www.wired.com/sponsored/story/how-neuro-symbolic-ai-breaks-the-limits-of-llms/",
    "https://www.wired.com/sponsored/story/propylon/",
    "https://www.wired.com/sponsored/story/opening-the-office-door-to-ai/",
    "https://www.wired.com/sponsored/story/kaiko/",
    "https://www.wired.com/sponsored/story/trackforce/",
    "https://www.wired.com/sponsored/story/apryse/",
    "https://www.wired.com/sponsored/story/csg/",
    "https://www.wired.com/sponsored/story/conversations-with-pioneers-of-enterprise-ai-hcltech/",
    "https://www.wired.com/sponsored/story/ai-is-set-to-revolutionise-corporate-hr/",
    "https://www.wired.com/sponsored/story/kpler/",
    "https://www.wired.com/contributor-content/story/how-biomechanical-ai-could-change-strength-training-for-the-future/",
    "https://www.wired.com/contributor-content/story/why-design-not-scale-will-decide-the-future-of-ai/",
    "https://www.wired.com/contributor-content/story/how-ai-digital-twins-are-reshaping-the-future-of-fan-interactions/",
    "https://www.wired.com/sponsored/story/quantumsystems/",
    "https://www.wired.com/sponsored/story/trackforce/",
    "https://www.wired.com/sponsored/story/comfort-connected-the-evolution-of-home-climate-technology/",
    "https://www.wired.com/contributor-content/story/ai-has-learned-to-write-space-aye-wants-it-to-see/",
    "https://www.wired.com/contributor-content/story/why-customer-service-operations-are-turning-to-modern-ai-tools/",
    "https://www.wired.com/contributor-content/story/how-ai-is-reshaping-online-orders-can-it-really-deliver/"
]

def scrape_wired_articles(url_list):
    # setup selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    # Explicit Wait (15 detik max)
    wait = WebDriverWait(driver, 15)

    scraped_data = []

    for idx, url in enumerate(url_list):
        print(f"[{idx+1}/{len(url_list)}] Scraping: {url}")
        try:
            driver.get(url)

            # handling wait : tunggu hingga tag <h1> (Judul Artikel) termuat di DOM
            wait.until(EC.presence_of_element_located((By. TAG_NAME, "h1")))

            # ekstrak judul
            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
            except NoSuchElementException:
                title = driver.title

            try:
                desc_element = driver.find_element(By.XPATH, "//meta[@name='description']")
                description = desc_element.get_attribute("content")
            except NoSuchElementException:
                description = "No desc"
            
            try:
                article_header = driver.find_element(By.TAG_NAME, "header")
                
                author_element = article_header.find_element(By.CSS_SELECTOR, ".byline__name, a[rel='author']")
                author_text = author_element.text
            except NoSuchElementException:
                author_text = "Unknown"

            # formatting author agar selalu ada kata "By" di depannya
            if not author_text.startswith("By"):
                author_final = f"By {author_text}"
            else:
                author_final = author_text
            
            # ekstrak timestamp saat ini
            scraped_at = datetime.datetime.now().isoformat()

            # masukkan ke dalam dictionary
            scraped_data.append({
                "title": title,
                "url": url,
                "description": description,
                "author": author_final,
                "scraped_at": scraped_at,
                "source": "Wired.com"
            })

        except TimeoutException:
            print(f" -> [TIMEOUT] Halaman terlalu lama memuat atau elemen tidak ditemukan.")
        except Exception as e:
            print(f" -> [ERROR] Terjadi kesalahan: {str(e)}")
        
        time.sleep(2) # jeda ringan agar tidak terblokir anti-scraping wired

    driver.quit()
    return scraped_data

if __name__ == "__main__":
    print("memulai scraping...")

    articles = scrape_wired_articles(urls)

    # format JSON Session Wraper
    session_id = f"wired_session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    timestamp = datetime.datetime.now().isoformat()

    final_output = {
        'session_id': session_id,
        'session_id': timestamp,
        'articles_count': len(articles),
        'articles':articles
    }

    # menyimpan ke JSON
    output_filename = "wired_scraped_data.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print(f"\nScraping selesai. Berhasil mengambil {len(articles)} artikel.")
    print(f"Data telah disimpan ke dalam : {output_filename}")

