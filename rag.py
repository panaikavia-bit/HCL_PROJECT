
import os
import hashlib
import ipaddress
import socket
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
import chromadb

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai
from google.genai import types


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

EMBEDDING_MODEL = "gemini-embedding-001"

ALLOWED_DOMAINS = [
    "w3schools.com",
    "javatpoint.com",
    "learn.microsoft.com"
]

USER_AGENT = "AIInterviewEducator/1.0"


# --------------------------------------------------
# 2. CONNECT TO CHROMADB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name="csharp_dotnet_knowledge"
)


# --------------------------------------------------
# 3. CHECK WEBSITE URL
# --------------------------------------------------

def validate_url(url):

    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise ValueError("Please enter a secure HTTPS URL.")

    if not parsed.hostname:
        raise ValueError("Invalid website URL.")

    hostname = parsed.hostname.lower()

    allowed = any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in ALLOWED_DOMAINS
    )

    if not allowed:
        raise ValueError(
            "Only W3Schools, JavaTpoint and Microsoft Learn URLs are allowed."
        )

    # Block local and private network addresses.
    try:
        addresses = socket.getaddrinfo(hostname, None)
        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global:
                raise ValueError("Private or local addresses are not allowed.")
    except socket.gaierror:
        raise ValueError("Could not resolve the website address.")

    return parsed


# --------------------------------------------------
# 4. CHECK ROBOTS.TXT PERMISSION
# --------------------------------------------------

def check_robots_permission(url):

    parsed = urlparse(url)

    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=10
        )

        if response.status_code == 404:
            return True

        response.raise_for_status()

        parser.parse(response.text.splitlines())

        return parser.can_fetch(USER_AGENT, url)

    except requests.RequestException:
        raise ValueError(
            "Could not check robots.txt. Please try again later."
        )


# --------------------------------------------------
# 5. EXTRACT WEBSITE TEXT
# --------------------------------------------------

def extract_website_text(url):

    validate_url(url)

    if not check_robots_permission(url):
        raise ValueError(
            "This page does not allow automated access. "
            "Please choose another permitted tutorial page."
        )

    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=20
    )

    response.raise_for_status()

    if "text/html" not in response.headers.get("Content-Type", ""):
        raise ValueError("The URL does not point to an HTML page.")

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.get_text(strip=True) if soup.title else url

    for unwanted in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "noscript",
        "svg"
    ]):
        unwanted.decompose()

    main_content = (
        soup.find("main")
        or soup.find("article")
        or soup.body
        or soup
    )

    text = main_content.get_text(
        separator=" ",
        strip=True
    )

    if len(text) < 200:
        raise ValueError(
            "Not enough readable tutorial content was found."
        )

    return title, text


# --------------------------------------------------
# 6. SPLIT TEXT INTO CHUNKS
# --------------------------------------------------

def split_into_chunks(text, chunk_size=1000, overlap=150):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if len(chunk.strip()) > 50:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# --------------------------------------------------
# 7. GENERATE GEMINI EMBEDDINGS
# --------------------------------------------------

def generate_embeddings(texts, task_type):

    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768
        )
    )

    return [
        embedding.values
        for embedding in result.embeddings
    ]


# --------------------------------------------------
# 8. SAVE WEBSITE CONTENT TO CHROMADB
# --------------------------------------------------

def add_website(url):

    title, website_text = extract_website_text(url)

    chunks = split_into_chunks(website_text)

    if not chunks:
        raise ValueError("No useful text chunks were found.")

    saved_count = 0

    # Process small batches to avoid large API requests.
    for batch_start in range(0, len(chunks), 10):

        batch = chunks[batch_start:batch_start + 10]

        embeddings = generate_embeddings(
            batch,
            "RETRIEVAL_DOCUMENT"
        )

        ids = []
        metadatas = []

        for index, chunk in enumerate(batch):

            chunk_number = batch_start + index

            unique_text = f"{url}-{chunk_number}-{chunk}"

            chunk_id = hashlib.sha256(
                unique_text.encode("utf-8")
            ).hexdigest()

            ids.append(chunk_id)

            metadatas.append({
                "source": url,
                "title": title,
                "chunk": chunk_number
            })

        collection.upsert(
            ids=ids,
            documents=batch,
            embeddings=embeddings,
            metadatas=metadatas
        )

        saved_count += len(batch)

    return {
        "title": title,
        "chunks": saved_count,
        "url": url
    }


# --------------------------------------------------
# 9. SEARCH STORED KNOWLEDGE
# --------------------------------------------------

def search_knowledge(question, top_k=4):

    if collection.count() == 0:
        return []

    question_embedding = generate_embeddings(
        [question],
        "RETRIEVAL_QUERY"
    )[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matches = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        matches.append({
            "content": document,
            "source": metadata.get("source", ""),
            "title": metadata.get("title", ""),
            "distance": distance
        })

    return matches


# --------------------------------------------------
# 10. CHECK KNOWLEDGE BASE
# --------------------------------------------------

def get_knowledge_count():

    return collection.count()
