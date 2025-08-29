import requests
from bs4 import BeautifulSoup
import psycopg2

# Create connection to database
conn = psycopg2.connect(
    host="postgres_service",
    database="PythonBlog",
    user="postgres",
    password="admin"
)
cursor = conn.cursor()

cursor.execute("SELECT 1 FROM pg_database WHERE datname='PythonBlog'")
exists = cursor.fetchone()
if not exists:
    cursor.execute("CREATE DATABASE \"PythonBlog\"")
    print("✅ Database PythonBlog created!")
else:
    print("ℹ️ Database PythonBlog already exists.")


# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS qn_ans (
    title TEXT,
    content TEXT
);
""")

# Scrape blog
res = requests.get('https://blog.python.org/')
soup = BeautifulSoup(res.content, 'html.parser')
posts = soup.find_all("div", class_="date-outer")

qes_list, ans_list = [], []

for post in posts:
    # Title
    title_tag = post.find("h3", class_="post-title")
    qes_list.append(title_tag.text.strip() if title_tag else "No Title")

    # Content
    content_div = post.find("div", class_="post-body")
    if content_div:
        content_text = "\n".join(p.get_text(strip=True) for p in content_div.find_all("p"))
        ans_list.append(content_text)
    else:
        ans_list.append("No Content")

# Insert into DB
for title, content in zip(qes_list, ans_list):
    cursor.execute(
        "INSERT INTO qn_ans (title, content) VALUES (%s, %s)",
        (title, content)
    )

# Commit changes
conn.commit()
cursor.close()
conn.close()

print("✅ Data scraped and inserted into PostgreSQL successfully!")
