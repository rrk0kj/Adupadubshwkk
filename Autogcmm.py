from telethon import TelegramClient, events
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    InviteToChannelRequest,
    EditAdminRequest,
    EditPhotoRequest
)
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import (
    ChatAdminRights,
    InputChatUploadedPhoto,
    MessageActionChatAddUser,
    MessageActionChatJoinedByLink,
    MessageActionChatEditPhoto,
    MessageActionChatEditTitle,
    MessageActionChatDeletePhoto
)

# API
api_id = 30071429
api_hash = "1e2942cf8ca2ddd5a86acf7bb33ae75c"

# Admin usernames
CREATEGROUP_ADMIN = "hupke"
CREATEADU_ADMIN = "abtiee"

# AWS-compatible PFP paths (files must exist in same folder as script)
PFP1 = "pfp.jpg"
PFP2 = "pfp2.jpg"

# Admin rights
admin_rights = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=True,
    invite_users=True,
    pin_messages=True,
    add_admins=False,
    anonymous=False,
    manage_call=True
)

client = TelegramClient("session", api_id, api_hash)


async def create_mm_group(event, title, pfp, admin_id):
    try:
        # Create group
        result = await client(CreateChannelRequest(
            title=title,
            about="Always confirm that you are dealing with me and not with an impersonator!",
            megagroup=True
        ))

        chat = result.chats[0]

        # Entities
        admin = await client.get_input_entity(admin_id)  # works with username
        creator = await client.get_me()

        # Invite admin
        await client(InviteToChannelRequest(chat, [admin]))

        # Admin tag
        await client(EditAdminRequest(
            channel=chat,
            user_id=admin,
            admin_rights=admin_rights,
            rank="Middlemem"
        ))

        # Creator tag
        await client(EditAdminRequest(
            channel=chat,
            user_id=creator,
            admin_rights=admin_rights,
            rank="Middlemem Group"
        ))

        # Upload PFP
        file = await client.upload_file(pfp)

        await client(EditPhotoRequest(
            channel=chat,
            photo=InputChatUploadedPhoto(file)
        ))

        # Invite link
        invite = await client(ExportChatInviteRequest(chat))

        await event.reply(f"✅ Group Created\n\n{invite.link}")

    except Exception as e:
        await event.reply(f"❌ Error:\n{e}")


# tents MM group → /ziox
@client.on(events.NewMessage(pattern="/ziox"))
async def tents_group(event):
    await create_mm_group(
        event,
        "tents MM | @middlemem",
        PFP1,
        CREATEGROUP_ADMIN
    )


# Adu MM group → /adu
@client.on(events.NewMessage(pattern="/adu"))
async def adu_group(event):
    await create_mm_group(
        event,
        "Adu MM | @middlemem",
        PFP2,
        CREATEADU_ADMIN
    )


# Auto delete ALL service messages
@client.on(events.NewMessage)
async def delete_service_messages(event):
    try:
        if isinstance(event.message.action, (
            MessageActionChatAddUser,
            MessageActionChatJoinedByLink,
            MessageActionChatEditPhoto,
            MessageActionChatEditTitle,
            MessageActionChatDeletePhoto
        )):
            await event.delete()
    except:
        pass


print("🔥 Auto MM Group Creator Running...")

client.start()
client.run_until_disconnected()