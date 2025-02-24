import os
import feedparser
from datetime import datetime, timezone
import xml.etree.ElementTree as ET


def filter_and_save_rss(rss_url, output_folder):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Filter out entries with "Note" in the title
    filtered_entries = [entry for entry in feed.entries if "Note" not in entry.title]

    # Create the RSS feed structure
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    # Add channel elements with attribution
    ET.SubElement(channel, "title").text = f"Filtered: {feed.feed.title}"
    ET.SubElement(channel, "link").text = feed.feed.link
    ET.SubElement(channel, "description").text = (
        f"A filtered version of the feed from {feed.feed.link}. "
        "Original content is attributed to the respective authors."
    )
    ET.SubElement(channel, "language").text = "en-GB"
    ET.SubElement(channel, "pubDate").text = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Add a custom element for attribution
    attribution = ET.SubElement(channel, "attribution")
    attribution.text = (
        f"This feed is a filtered version of the original feed available at {feed.feed.link}. "
        "All content is attributed to the original author(s)."
    )

    # Add filtered entries to the channel
    for entry in filtered_entries:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = entry.title
        ET.SubElement(item, "link").text = entry.link
        ET.SubElement(item, "description").text = entry.description
        ET.SubElement(item, "pubDate").text = entry.published

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Define the output file path
    output_file = os.path.join(output_folder, 'harper_dot_blog_posts_only.xml')

    # Write the filtered feed to an XML file
    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    print(f"Filtered RSS feed saved to {output_file}.")

# URL of the RSS feed
rss_url = 'https://harper.blog/index.xml'

# Output folder path
output_folder = 'feeds'

# Filter and save the RSS feed
filter_and_save_rss(rss_url, output_folder)
