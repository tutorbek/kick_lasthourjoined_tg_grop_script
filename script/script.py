
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantRequest, EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import datetime, timedelta, timezone

api_id = 1157038        # <-- o'zingizniki
api_hash = "b77b40e55f2834789e50bccdf0e1376e"    # <-- o'zingizniki

group = "https://t.me/CafeHalovat"  # yoki group ID



client = TelegramClient("session", api_id, api_hash)

async def kick_newcomers():
    await client.start()
    limit_time = datetime.now(timezone.utc) - timedelta(hours=2)

    async for user in client.iter_participants(group):
        try:
            p = await client(GetParticipantRequest(group, user.id))
            if hasattr(p.participant, "date"):
                if p.participant.date > limit_time:
                    await client(EditBannedRequest(
                        group,
                        user.id,
                        ChatBannedRights(
                            until_date=None,
                            view_messages=True
                        )
                    ))
                    print("KICK:", user.id)
        except Exception as e:
            print("Skip:", e)

    await client.disconnect()

asyncio.run(kick_newcomers())