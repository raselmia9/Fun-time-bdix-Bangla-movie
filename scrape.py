from bs4 import BeautifulSoup
import requests

url = "http://172.20.21.22/catagory.php?key=QmFuZ2xhX01vdmllcw=="

try:
  response = requests.get(url, timeout=10)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")
  mp4_links = []
  titles = []

  for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if ".mp4" in href.lower():
      if href.startswith("http"):
        full_url = href
      else:
        full_url = "http://172.20.21.22/" + href.lstrip("/")

      mp4_links.append(full_url)
      titles.append(a_tag.get_text(strip=True) or "Movie Item")

  # m3u ফাইল তৈরি
  with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for title, link in zip(titles, mp4_links):
      f.write(f"#EXTINF:-1,{title}\n")
      f.write(f"{link}\n")

  print(
      f"সফলভাবে {len(mp4_links)} টি লিংক দিয়ে 'playlist.m3u' আপডেট করা হয়েছে!"
  )

except Exception as e:
  print("ত্রুটি দেখা দিয়েছে:", e)
  
