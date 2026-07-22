from bs4 import BeautifulSoup
import requests

# আপনার কাঙ্ক্ষিত মুভি বা ওয়াচ পেজের লিংক এখানে দিন
url = "https://web.rogplay.app/watch/movie/1368337"

# ব্রাউজার হিসেবে রিকোয়েস্ট পাঠানোর জন্য হেডার্স
headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-US,en;q=0.9',
}

try:
  print('ওয়েবসাইট থেকে ডেটা ফেচ করা হচ্ছে...')
  response = requests.get(url, headers=headers, timeout=15)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, 'html.parser')
  found_links = []

  # ১. সকল <a> ট্যাগ থেকে .mp4, .m3u8, .mkv বা স্ট্রিম লিংক খোঁজা
  for a in soup.find_all('a', href=True):
    href = a['href']
    if any(ext in href.lower() for ext in ['.mp4', '.m3u8', '.mkv', 'stream']):
      found_links.append(href)

  # ২. যদি কোনো <video> বা <source> ট্যাগ থাকে
  for source in soup.find_all(['video', 'source'], src=True):
    src = source['src']
    if src not in found_links:
      found_links.append(src)

  # playlist.m3u ফাইল তৈরি করা
  with open('playlist.m3u', 'w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    if found_links:
      for i, link in enumerate(found_links, start=1):
        f.write(f'#EXTINF:-1,Movie Stream {i}\n')
        f.write(f'{link}\n')
      print(
          f'সফলভাবে {len(found_links)} টি ভিডিও লিংক দিয়ে "playlist.m3u" ফাইল'
          ' তৈরি হয়েছে!'
      )
    else:
      # যদি সরাসরি স্ট্যাটিক ট্যাগে লিংক না পাওয়া যায়, তবে ইনফো সেভ করবে
      f.write('#EXTINF:-1,No direct static stream found (Dynamic/API site)\n')
      f.write('# Note: Use Browser Network Inspector or IDM to capture link.\n')
      print(
          'সরাসরি স্ট্যাটিক লিংক পাওয়া যায়নি (সাইটটি ডাইনামিক)। প্লেলিস্ট ফাইলে'
          ' নোটিশ সেভ করা হয়েছে।'
      )

except Exception as e:
  print('ত্রুটি দেখা দিয়েছে:', e)
      
