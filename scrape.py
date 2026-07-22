from bs4 import BeautifulSoup
import requests

# আপনার নতুন ওয়েবসাইট ইউআরএল
url = "https://web.rogplay.app/movie"

# মোবাইল ব্রাউজার হিসেবে রিকোয়েস্ট পাঠানোর জন্য Headers
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like'
        ' Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
    )
}

try:
  print("সার্ভারের সাথে কানেক্ট করা হচ্ছে...")
  response = requests.get(url, headers=headers, timeout=15)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")
  mp4_links = []
  titles = []

  # HTML এর সব <a> ট্যাগ থেকে লিঙ্ক সংগ্রহ করা
  for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]

    # .mp4 বা .m3u8 ভিডিও ফাইল খোঁজা
    if ".mp4" in href.lower() or ".m3u8" in href.lower():
      if href.startswith("http"):
        full_url = href
      else:
        full_url = "https://web.rogplay.app" + href

      if full_url not in mp4_links:
        mp4_links.append(full_url)
        titles.append(a_tag.get_text(strip=True) or "Movie Item")

  # playlist.m3u ফাইল তৈরি করা
  with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for title, link in zip(titles, mp4_links):
      f.write(f"#EXTINF:-1,{title}\n")
      f.write(f"{link}\n")

  print(
      f"সফলভাবে {len(mp4_links)} টি লিঙ্ক নিয়ে 'playlist.m3u' তৈরি করা হয়েছে!"
  )

except Exception as e:
  print("ত্রুটি দেখা দিয়েছে:", e)
    
