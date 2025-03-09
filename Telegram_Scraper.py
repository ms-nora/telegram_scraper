pip install telethon pandas


import asyncio
import time
import os
import pandas as pd
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, MessageEntityUrl

#telegram api details
API_ID = 'your api id'
API_HASH = 'your api hash'

#define the output csv file
csv_filename = "telegram_scrape_results.csv"

async def fetch_links(client, chat, limit=100):
    #fetches all links from messages in the given chat
    links = []
    async for msg in client.iter_messages(chat, limit=limit):
        if msg.entities:
            for entity in msg.entities:
                if isinstance(entity, MessageEntityUrl):
                    links.append(msg.text[entity.offset: entity.offset + entity.length])
    return links

async def fetch_members(client, chat, limit=100):
    #fetches members from a given chat
    members = []
    offset = 0

    while True:
        try:
            participants = await client(GetParticipantsRequest(
                channel=chat,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            members.extend(participants.users)
            if len(participants.users) < limit:
                break
            offset += len(participants.users)
        except FloodWaitError as e:
            print(f"rate limit reached, waiting {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)

    return [{
        "user_id": member.id,
        "username": member.username or "N/A",
        "first_name": member.first_name or "",
        "last_name": member.last_name or "",
        "access_hash": member.access_hash
    } for member in members]

async def search_telegram_channels_and_scrape(client, keywords):
    #searches telegram for channels and groups based on keywords
    results = []
    
    for keyword in keywords:
        print(f"searching for keyword: {keyword}")
        try:
            response = await client(SearchRequest(
                q=keyword,
                limit=10,
                from_id=None,
                offset_date=None,
                offset_id=0,
                hash=0
            ))

            for chat in response.chats:
                invite_link = f"https://t.me/{chat.username}" if chat.username else None

                #fetch members if it's a group
                members = await fetch_members(client, chat) if chat.megagroup else []

                #fetch links from messages
                links = await fetch_links(client, chat)

                results.append({
                    "keyword": keyword,
                    "platform": "telegram",
                    "username": chat.username or "N/A",
                    "user_id": chat.id,
                    "group_name": chat.title if chat.megagroup else None,
                    "group_link": invite_link if chat.megagroup else None,
                    "channel_name": chat.title if not chat.megagroup else None,
                    "channel_link": invite_link if not chat.megagroup else None,
                    "invite_link": invite_link,
                    "members": len(members),
                    "links": ', '.join(links)  #merges links into a single string
                })
        except FloodWaitError as e:
            print(f"rate limit reached, waiting {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)

    return results

def save_to_csv(results, filename=csv_filename):
    #saves the scraping results to a csv file
    df = pd.DataFrame(results)

    #save csv with utf-8 encoding and proper formatting
    df.to_csv(filename, index=False, sep=",", encoding="utf-8")

    print(f"results saved to {filename}")

async def main():
    #loads keywords from a file or defines them manually
    keyword_file = "keywords.txt"

    if os.path.exists(keyword_file):
        with open(keyword_file, "r", encoding="utf-8") as f:
            keywords = [line.strip() for line in f.readlines()]
    else:
        keywords = ["example_keyword_1", "example_keyword_2"]  #define keywords manually

    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        results = await search_telegram_channels_and_scrape(client, keywords)
        save_to_csv(results)

#run the asynchronous main function
asyncio.run(main())

