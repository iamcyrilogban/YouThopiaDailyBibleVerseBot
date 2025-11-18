def send_reply(message, touched_message_id):
    try:
        # Send the reply to the touched message in the group chat
        if message.content_type == "text":
            sent_message = bot.send_message(GROUP_CHAT_ID, message.text, reply_to_message_id=touched_message_id)
        elif message.content_type == "photo": 
            sent_message = bot.send_photo(GROUP_CHAT_ID, message.photo[-1].file_id, caption=message.caption, reply_to_message_id=touched_message_id)
        elif message.content_type == "video":
            sent_message = bot.send_video(GROUP_CHAT_ID, message.video.file_id, caption=message.caption, reply_to_message_id=touched_message_id)
        elif message.content_type == "voice":
            sent_message = bot.send_voice(GROUP_CHAT_ID, message.voice.file_id, caption=message.caption, reply_to_message_id=touched_message_id)
        elif message.content_type == "audio":
            sent_message = bot.send_audio(GROUP_CHAT_ID, message.audio.file_id, caption=message.caption, reply_to_message_id=touched_message_id)
        else: 
            bot.send_message(message.chat.id, "Unsupported message type. Please try again.")
            return

        # Create an inline keyboard for "Reply Anonymously" button using sent_message_id
        markup = InlineKeyboardMarkup()
        reply_url = f"https://t.me/{bot.get_me().username}?start=reply_{sent_message.message_id}"
        markup.add(InlineKeyboardButton("Reply Anonymously", url=reply_url))

        # Edit the sent message to include the reply button
        bot.edit_message_reply_markup(GROUP_CHAT_ID, sent_message.message_id, reply_markup=markup)

        # Notify the user that their reply was sent
        bot.send_message(
            message.chat.id,
            f'Your reply has been posted anonymously. <a href="https://t.me/c/2248181172/{sent_message.message_id}">See here</a>',
            parse_mode='HTML'
        )

    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to send reply: {e}")  