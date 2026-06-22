import os
import json
import urllib.request
import xml.etree.ElementTree as ET

# Kullanıcı ilgi alanları / User interests for filtering
USER_INTERESTS = "Python, Artificial Intelligence, Machine Learning, LLM, Web Development"

# RSS Feed URL (Hacker News)
HN_RSS_URL = "https://news.ycombinator.com/rss"

# GitHub API URL (Trending Python Repositories)
GITHUB_API_URL = "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=10"

def fetch_tech_news(url):
    """Fetches and parses tech news from an RSS feed using standard library."""
    print("[*] Haber akışı çekiliyor (Hacker News)... ")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        news_items = []
        for item in root.findall('.//item')[:10]:  # Get top 10 items
            title = item.find('title').text
            link = item.find('link').text
            news_items.append({"title": title, "link": link})
        return news_items
    except Exception as e:
        print(f"[!] Haberler alınamadı: {e}")
        return []

def fetch_github_repos(url):
    """Fetches trending GitHub repositories using GitHub API."""
    print("[*] Trend GitHub projeleri çekiliyor...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            repos = []
            for item in data.get('items', [])[:10]:
                repos.append({
                    "name": item['full_name'],
                    "description": item['description'] or "Açıklama yok.",
                    "stars": item['stargazers_count'],
                    "url": item['html_url']
                })
            return repos
    except Exception as e:
        print(f"[!] GitHub projeleri alınamadı: {e}")
        return []

def generate_ai_digest(news, repos, interests):
    """Uses OpenAI-compatible API to filter and summarize content based on user interests."""
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")

    if not api_key:
        print("\n[!] UYARI: 'OPENAI_API_KEY' bulunamadı. Kural tabanlı basit filtreleme yapılıyor.")
        return fallback_rule_based_filter(news, repos, interests)

    print("[*] Yapay zeka asistanı verileri analiz ediyor ve özetliyor...")
    
    prompt = f"""
    Aşağıda teknoloji haberleri ve popüler GitHub projeleri listelenmiştir.
    Kullanıcının ilgi alanlarına göre ({interests}) bu listeyi filtrele ve Türkçe olarak kişiselleştirilmiş bir günlük bülten hazırla.
    Gereksiz gürültüyü (ilgisiz konuları) ele.
    
    Haberler:
    {json.dumps(news, indent=2)}
    
    GitHub Projeleri:
    {json.dumps(repos, indent=2)}
    
    Format:
    - **[Önemli Gelişmeler]** (Seçtiğin haberlerin kısa özeti ve neden önemli olduğu)
    - **[İncelemen Gereken Projeler]** (Seçtiğin GitHub projeleri ve kısa açıklamaları)
    """

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Sen profesyonel bir teknoloji editörü ve kişisel asistansın."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        req = urllib.request.Request(
            f"{api_base}/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode())
            return res_data['choices'][0]['message']['content']
    except Exception as e:
        print(f"[!] Yapay zeka analizi başarısız oldu: {e}")
        return fallback_rule_based_filter(news, repos, interests)

def fallback_rule_based_filter(news, repos, interests):
    """Fallback filter using simple keyword matching if no API key is provided."""
    keywords = [kw.strip().lower() for kw in interests.split(",")]
    filtered_news = []
    filtered_repos = []

    for item in news:
        if any(kw in item['title'].lower() for kw in keywords):
            filtered_news.append(item)
            
    for repo in repos:
        if any(kw in repo['name'].lower() or kw in repo['description'].lower() for kw in keywords):
            filtered_repos.append(repo)

    output = "\n=== KİŞİSELLEŞTİRİLMİŞ BÜLTEN (Kural Tabanlı Filtreleme) ===\n\n"
    output += "**[Önemli Gelişmeler]**\n"
    if filtered_news:
        for item in filtered_news:
            output += f"- {item['title']}\n  Link: {item['link']}\n"
    else:
        output += "İlgi alanlarınıza uygun yeni haber bulunamadı.\n"

    output += "\n**[İncelemen Gereken Projeler]**\n"
    if filtered_repos:
        for repo in filtered_repos:
            output += f"- {repo['name']} (★ {repo['stars']})\n  Açıklama: {repo['description']}\n  Link: {repo['url']}\n"
    else:
        output += "İlgi alanlarınıza uygun popüler GitHub projesi bulunamadı.\n"
        
    return output

if __name__ == "__main__":
    print("=== Kişisel Yapay Zeka Asistanı Başlatılıyor ===")
    print(f"İlgi Alanları: {USER_INTERESTS}\n")
    
    # 1. Verileri Topla
    news = fetch_tech_news(HN_RSS_URL)
    repos = fetch_github_repos(GITHUB_API_URL)
    
    # 2. İşle ve Özetle
    digest = generate_ai_digest(news, repos, USER_INTERESTS)
    
    # 3. Sonucu Yazdır
    print("\n" + "="*50)
    print(digest)
    print("="*50)
