#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import json
import math
import os
import time
from PIL import Image
# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.display_progress import humanbytes
from helper_funcs.help_uploadbot import DownLoadFile

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
vid=['https://www.youtube.com/watch?v=NPqFtxK1nFA', 'https://www.youtube.com/watch?v=-gh0FYNET4o', 'https://www.youtube.com/watch?v=6vBqTpbbpIY', 'https://www.youtube.com/watch?v=fBzXx2IvvEc', 'https://www.youtube.com/watch?v=Wj0lXQRXiOY', 'https://www.youtube.com/watch?v=-PKo0Pq-JQ8', 'https://www.youtube.com/watch?v=up8EmXRkiFM', 'https://www.youtube.com/watch?v=TTgxUz4OGtE', 'https://www.youtube.com/watch?v=S4_Z-Mpv1EU', 'https://www.youtube.com/watch?v=ZaHIcNSZgXY', 'https://www.youtube.com/watch?v=66i1kLZO-lc', 'https://www.youtube.com/watch?v=4JRX1-1-kJc', 'https://www.youtube.com/watch?v=EiByVHXT_hc', 'https://www.youtube.com/watch?v=_pL1g4mLQUM', 'https://www.youtube.com/watch?v=Q2HXdoLjmM4', 'https://www.youtube.com/watch?v=NwymkRkD2mE', 'https://www.youtube.com/watch?v=8I-QHfG6Ffk', 'https://www.youtube.com/watch?v=O3zocb7ZHkM', 'https://www.youtube.com/watch?v=3UDDXuwmPVc', 'https://www.youtube.com/watch?v=drrawYmxVgo', 'https://www.youtube.com/watch?v=R4Y5Vl-BcOE', 'https://www.youtube.com/watch?v=bMZAIEhCgfY', 'https://www.youtube.com/watch?v=Lt7sJOsZvls', 'https://www.youtube.com/watch?v=PWf1E8kqVZA', 'https://www.youtube.com/watch?v=OS4ZG6eEHp8', 'https://www.youtube.com/watch?v=GenqU32RkAI', 'https://www.youtube.com/watch?v=Ej_lee7riBM', 'https://www.youtube.com/watch?v=DPnwWJ31qNM', 'https://www.youtube.com/watch?v=jAgjYBfRQs0', 'https://www.youtube.com/watch?v=ei90-5ezNTk', 'https://www.youtube.com/watch?v=7F9QmFVeKD8', 'https://www.youtube.com/watch?v=CCDXLStOWtk', 'https://www.youtube.com/watch?v=qkN1ktD-hRM', 'https://www.youtube.com/watch?v=zPkKiMo5ZfQ', 'https://www.youtube.com/watch?v=5P4BJi95uuU', 'https://www.youtube.com/watch?v=rEpOKZeqo0c', 'https://www.youtube.com/watch?v=4m7jKNNyI_8', 'https://www.youtube.com/watch?v=hSDFinrGYVU', 'https://www.youtube.com/watch?v=QBC2isMalYY', 'https://www.youtube.com/watch?v=n4XOVlBrDLc', 'https://www.youtube.com/watch?v=ltmKxmUyZBg', 'https://www.youtube.com/watch?v=V1IMVocd65I', 'https://www.youtube.com/watch?v=ePNPJuFEJ7k', 'https://www.youtube.com/watch?v=zObqBR82ocA', 'https://www.youtube.com/watch?v=kUFtaSyQR6c', 'https://www.youtube.com/watch?v=PpcYEd0JpyM', 'https://www.youtube.com/watch?v=YhGxbrsu8PE', 'https://www.youtube.com/watch?v=uaegLGOHyJY', 'https://www.youtube.com/watch?v=-31K92bxJnw', 'https://www.youtube.com/watch?v=WBAU5pqODGw', 'https://www.youtube.com/watch?v=cXUaH5ataj4', 'https://www.youtube.com/watch?v=YV7Pm4mSIN8', 'https://www.youtube.com/watch?v=YRuC1PhiSZ8', 'https://www.youtube.com/watch?v=ZdlCnr5jkJE', 'https://www.youtube.com/watch?v=uvaGQVh4lXg', 'https://www.youtube.com/watch?v=95G9-kdHw6I', 'https://www.youtube.com/watch?v=pRrlBTQrWEE', 'https://www.youtube.com/watch?v=YOs7QMNX7s8', 'https://www.youtube.com/watch?v=Q5gloSE8eW4', 'https://www.youtube.com/watch?v=fNKCI7Pnu94', 'https://www.youtube.com/watch?v=LfcrAgY25jM', 'https://www.youtube.com/watch?v=vkrquiHOEeg', 'https://www.youtube.com/watch?v=xeqRz7Syizs', 'https://www.youtube.com/watch?v=_n6pjA5aFQ4', 'https://www.youtube.com/watch?v=2PFnPzi9kws', 'https://www.youtube.com/watch?v=UFLgrC-hZl0', 'https://www.youtube.com/watch?v=iny4GenrNkk', 'https://www.youtube.com/watch?v=m1NOb2RSvMs', 'https://www.youtube.com/watch?v=LlulKIWFlvw', 'https://www.youtube.com/watch?v=Xs5os29NhTs', 'https://www.youtube.com/watch?v=JOBg9lIluW4', 'https://www.youtube.com/watch?v=MB1lMSYrHdY', 'https://www.youtube.com/watch?v=HKeft1mGUXw', 'https://www.youtube.com/watch?v=QsxymWG26S0', 'https://www.youtube.com/watch?v=4EIDsNUl4dk', 'https://www.youtube.com/watch?v=_IQQTWIRdJs', 'https://www.youtube.com/watch?v=KVrZu9kt3qw', 'https://www.youtube.com/watch?v=06pyHUP7sSs', 'https://www.youtube.com/watch?v=SDvlzD9_3Ck', 'https://www.youtube.com/watch?v=bfylXs4L-a0', 'https://www.youtube.com/watch?v=f_lgPOH5nOk', 'https://www.youtube.com/watch?v=HYPvJKihhX8', 'https://www.youtube.com/watch?v=aPt5D6NcQB4', 'https://www.youtube.com/watch?v=jxGm2R0zD7s', 'https://www.youtube.com/watch?v=7ozXEc2NmPE', 'https://www.youtube.com/watch?v=YGyQgNldRoU', 'https://www.youtube.com/watch?v=WbRD-trxPNI', 'https://www.youtube.com/watch?v=7MxXhPaDAMg', 'https://www.youtube.com/watch?v=UgSFpEndLnc', 'https://www.youtube.com/watch?v=WCvqN51E0f0', 'https://www.youtube.com/watch?v=it-PM93ihTc', 'https://www.youtube.com/watch?v=Gk6YBGl0mmg', 'https://www.youtube.com/watch?v=pdCMxreTK1s', 'https://www.youtube.com/watch?v=PC57cNMyKTc', 'https://www.youtube.com/watch?v=mKg6IBlIGdY', 'https://www.youtube.com/watch?v=9YlJCz_aZFg', 'https://www.youtube.com/watch?v=A4enHz-ExsE', 'https://www.youtube.com/watch?v=n_8qAfTqJ8U', 'https://www.youtube.com/watch?v=W9rKdg0VUT4', 'https://www.youtube.com/watch?v=UXIb9BieA80', 'https://www.youtube.com/watch?v=1l3M3xWSH5U', 'https://www.youtube.com/watch?v=uOHsyBycJko', 'https://www.youtube.com/watch?v=67apyJAfPTQ', 'https://www.youtube.com/watch?v=O5otExIW9xE', 'https://www.youtube.com/watch?v=VaOdtzdp72k', 'https://www.youtube.com/watch?v=0ac-631SIdQ', 'https://www.youtube.com/watch?v=0YnFbW7Oaac', 'https://www.youtube.com/watch?v=rCpXr2nSaoQ', 'https://www.youtube.com/watch?v=5OnnTzTdtew', 'https://www.youtube.com/watch?v=AhELSLi_aNM', 'https://www.youtube.com/watch?v=d7bfDUrIFPw', 'https://www.youtube.com/watch?v=e6v_SpPzdUE', 'https://www.youtube.com/watch?v=OpVb3m-e9JM', 'https://www.youtube.com/watch?v=ety62-Lp2Z8', 'https://www.youtube.com/watch?v=npCjhuxoqUE', 'https://www.youtube.com/watch?v=ErnGuG8HVFk', 'https://www.youtube.com/watch?v=TFDyjkJWi_E', 'https://www.youtube.com/watch?v=0NcDAIq8Spo', 'https://www.youtube.com/watch?v=tmdEyEmthYA', 'https://www.youtube.com/watch?v=o3dSfzvMEAQ', 'https://www.youtube.com/watch?v=NB-fNw1QaZ4', 'https://www.youtube.com/watch?v=SwtoJKKpaU4', 'https://www.youtube.com/watch?v=vq9jNap5Gu0', 'https://www.youtube.com/watch?v=3PVV3VIcChA', 'https://www.youtube.com/watch?v=wgonC6xNLuk', 'https://www.youtube.com/watch?v=cls5FujvW34', 'https://www.youtube.com/watch?v=2tstLDiQiIU', 'https://www.youtube.com/watch?v=wVKoKHI6xlw', 'https://www.youtube.com/watch?v=Dg_oA5ZWy4A', 'https://www.youtube.com/watch?v=6xupvus1vQQ', 'https://www.youtube.com/watch?v=wc5miYdGce4', 'https://www.youtube.com/watch?v=IveIR1HpK5k', 'https://www.youtube.com/watch?v=dGpyVZLXdTY', 'https://www.youtube.com/watch?v=lRqZGxhXz2M', 'https://www.youtube.com/watch?v=LrvXiJyCWKA', 'https://www.youtube.com/watch?v=zKCcglCO9Tk', 'https://www.youtube.com/watch?v=1Amze_D20Io', 'https://www.youtube.com/watch?v=dq1gMoZdazE', 'https://www.youtube.com/watch?v=EZ2G6oBUlfM', 'https://www.youtube.com/watch?v=j1XAptAU6Fo', 'https://www.youtube.com/watch?v=brOZkM26QLQ', 'https://www.youtube.com/watch?v=KyQwdA7FhEY', 'https://www.youtube.com/watch?v=sTlTGugpX-s', 'https://www.youtube.com/watch?v=Z816F9gkSIU', 'https://www.youtube.com/watch?v=a_fpY6ADncU', 'https://www.youtube.com/watch?v=wABb-gUhBKE', 'https://www.youtube.com/watch?v=f1WlyETkL1I', 'https://www.youtube.com/watch?v=i5RVOeNWJNc', 'https://www.youtube.com/watch?v=LcSJVbLEpp8', 'https://www.youtube.com/watch?v=wxcom0uirPQ', 'https://www.youtube.com/watch?v=9HJbV8hM2HI', 'https://www.youtube.com/watch?v=sHNiEVPrDf4', 'https://www.youtube.com/watch?v=nJshMBph9k0', 'https://www.youtube.com/watch?v=_brIOL4ygBo', 'https://www.youtube.com/watch?v=o4Brptbv310', 'https://www.youtube.com/watch?v=vXFcqk7EJOs', 'https://www.youtube.com/watch?v=zdFeU6S2kBU', 'https://www.youtube.com/watch?v=Y1HVT__2kZA', 'https://www.youtube.com/watch?v=zZeHC6lA0zE', 'https://www.youtube.com/watch?v=842EG49_Qug', 'https://www.youtube.com/watch?v=XJ8OeFI9TQU', 'https://www.youtube.com/watch?v=eRwy-23w4ZM', 'https://www.youtube.com/watch?v=gLMTUCaUSd0', 'https://www.youtube.com/watch?v=cyd2395ux1I', 'https://www.youtube.com/watch?v=5yp4bETMPEw', 'https://www.youtube.com/watch?v=vMF-QIs-IbM', 'https://www.youtube.com/watch?v=yAMFQ7JyFd4', 'https://www.youtube.com/watch?v=o9RLV8gjugw', 'https://www.youtube.com/watch?v=pW7_i1vpwa0', 'https://www.youtube.com/watch?v=Bm2ZI1ZQEI4', 'https://www.youtube.com/watch?v=6dqE3sdDPyo', 'https://www.youtube.com/watch?v=qyUUnxXd_Kg', 'https://www.youtube.com/watch?v=Ork74WaVf7k', 'https://www.youtube.com/watch?v=r6F117vbhOY', 'https://www.youtube.com/watch?v=AvASZsUIcaU']

@pyrogram.Client.on_message(pyrogram.filters.regex(pattern=".*http.*"))
async def echo(bot, update):
    if update.from_user.id in Config.AUTH_USERS:
        logger.info(update.from_user)
        #url = update.text
        #forlopp----------------
        for i in vid:
            url=i
            youtube_dl_username = None
            youtube_dl_password = None
            file_name = None
            if "|" in url:
                url_parts = url.split("|")
                if len(url_parts) == 2:
                    url = url_parts[0]
                    file_name = url_parts[1]
                elif len(url_parts) == 4:
                    url = url_parts[0]
                    file_name = url_parts[1]
                    youtube_dl_username = url_parts[2]
                    youtube_dl_password = url_parts[3]
                else:
                    for entity in update.entities:
                        if entity.type == "text_link":
                            url = entity.url
                        elif entity.type == "url":
                            o = entity.offset
                            l = entity.length
                            url = url[o:o + l]
                if url is not None:
                    url = url.strip()
                if file_name is not None:
                    file_name = file_name.strip()
                # https://stackoverflow.com/a/761825/4723940
                if youtube_dl_username is not None:
                    youtube_dl_username = youtube_dl_username.strip()
                if youtube_dl_password is not None:
                    youtube_dl_password = youtube_dl_password.strip()
                logger.info(url)
                logger.info(file_name)
            else:
                for entity in update.entities:
                    if entity.type == "text_link":
                        url = entity.url
                    elif entity.type == "url":
                        o = entity.offset
                        l = entity.length
                        url = url[o:o + l]
            if Config.HTTP_PROXY != "":
                command_to_exec = [
                    "youtube-dl",
                    "--no-warnings",
                    "--youtube-skip-dash-manifest",
                    "-j",
                    url,
                    "--proxy", Config.HTTP_PROXY
                ]
            else:
                command_to_exec = [
                    "youtube-dl",
                    "--no-warnings",
                    "--youtube-skip-dash-manifest",
                    "-j",
                    url
                ]
            if youtube_dl_username is not None:
                command_to_exec.append("--username")
                command_to_exec.append(youtube_dl_username)
            if youtube_dl_password is not None:
                command_to_exec.append("--password")
                command_to_exec.append(youtube_dl_password)
            # logger.info(command_to_exec)
            process = await asyncio.create_subprocess_exec(
                *command_to_exec,
                # stdout must a pipe to be accessible as process.stdout
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Wait for the subprocess to finish
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            # logger.info(e_response)
            t_response = stdout.decode().strip()
            # logger.info(t_response)
            # https://github.com/rg3/youtube-dl/issues/2630#issuecomment-38635239
            if e_response and "nonnumeric port" not in e_response:
                # logger.warn("Status : FAIL", exc.returncode, exc.output)
                error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
                if "This video is only available for registered users." in error_message:
                    error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
                    reply_to_message_id=update.message_id,
                    parse_mode="html",
                    disable_web_page_preview=True
                )
                return False
            if t_response:
                # logger.info(t_response)
                x_reponse = t_response
                if "\n" in x_reponse:
                    x_reponse, _ = x_reponse.split("\n")
                response_json = json.loads(x_reponse)
                save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
                    "/" + str(update.from_user.id) + ".json"
                with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
                    json.dump(response_json, outfile, ensure_ascii=False)
                # logger.info(response_json)
                inline_keyboard = []
                duration = None
                if "duration" in response_json:
                    duration = response_json["duration"]
                if "formats" in response_json:
                    for formats in response_json["formats"]:
                        format_id = formats.get("format_id")
                        format_string = formats.get("format_note")
                        if format_string is None:
                            format_string = formats.get("format")
                        format_ext = formats.get("ext")
                        approx_file_size = ""
                        if "filesize" in formats:
                            approx_file_size = humanbytes(formats["filesize"])
                        cb_string_video = "{}|{}|{}".format(
                            "video", format_id, format_ext)
                        cb_string_file = "{}|{}|{}".format(
                            "file", format_id, format_ext)
                        if format_string is not None and not "audio only" in format_string:
                            ikeyboard = [
                                InlineKeyboardButton(
                                    "S " + format_string + " video " + approx_file_size + " ",
                                    callback_data=(cb_string_video).encode("UTF-8")
                                ),
                                InlineKeyboardButton(
                                    "D " + format_ext + " " + approx_file_size + " ",
                                    callback_data=(cb_string_file).encode("UTF-8")
                                )
                            ]
                            """if duration is not None:
                                cb_string_video_message = "{}|{}|{}".format(
                                    "vm", format_id, format_ext)
                                ikeyboard.append(
                                    InlineKeyboardButton(
                                        "VM",
                                        callback_data=(
                                            cb_string_video_message).encode("UTF-8")
                                    )
                                )"""
                        else:
                            # special weird case :\
                            ikeyboard = [
                                InlineKeyboardButton(
                                    "SVideo [" +
                                    "] ( " +
                                    approx_file_size + " )",
                                    callback_data=(cb_string_video).encode("UTF-8")
                                ),
                                InlineKeyboardButton(
                                    "DFile [" +
                                    "] ( " +
                                    approx_file_size + " )",
                                    callback_data=(cb_string_file).encode("UTF-8")
                                )
                            ]
                        inline_keyboard.append(ikeyboard)
                    if duration is not None:
                        cb_string_64 = "{}|{}|{}".format("audio", "64k", "mp3")
                        cb_string_128 = "{}|{}|{}".format("audio", "128k", "mp3")
                        cb_string = "{}|{}|{}".format("audio", "320k", "mp3")
                        inline_keyboard.append([
                            InlineKeyboardButton(
                                "MP3 " + "(" + "64 kbps" + ")", callback_data=cb_string_64.encode("UTF-8")),
                            InlineKeyboardButton(
                                "MP3 " + "(" + "128 kbps" + ")", callback_data=cb_string_128.encode("UTF-8"))
                        ])
                        inline_keyboard.append([
                            InlineKeyboardButton(
                                "MP3 " + "(" + "320 kbps" + ")", callback_data=cb_string.encode("UTF-8"))
                        ])
                else:
                    format_id = response_json["format_id"]
                    format_ext = response_json["ext"]
                    cb_string_file = "{}|{}|{}".format(
                        "file", format_id, format_ext)
                    cb_string_video = "{}|{}|{}".format(
                        "video", format_id, format_ext)
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "SVideo",
                            callback_data=(cb_string_video).encode("UTF-8")
                        ),
                        InlineKeyboardButton(
                            "DFile",
                            callback_data=(cb_string_file).encode("UTF-8")
                        )
                    ])
                    cb_string_file = "{}={}={}".format(
                        "file", format_id, format_ext)
                    cb_string_video = "{}={}={}".format(
                        "video", format_id, format_ext)
                    inline_keyboard.append([
                        InlineKeyboardButton(
                            "video",
                            callback_data=(cb_string_video).encode("UTF-8")
                        ),
                        InlineKeyboardButton(
                            "file",
                            callback_data=(cb_string_file).encode("UTF-8")
                        )
                    ])
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                # logger.info(reply_markup)
                thumbnail = Config.DEF_THUMB_NAIL_VID_S
                thumbnail_image = Config.DEF_THUMB_NAIL_VID_S
                if "thumbnail" in response_json:
                    if response_json["thumbnail"] is not None:
                        thumbnail = response_json["thumbnail"]
                        thumbnail_image = response_json["thumbnail"]
                thumb_image_path = DownLoadFile(
                    thumbnail_image,
                    Config.DOWNLOAD_LOCATION + "/" +
                    str(update.from_user.id) + ".webp",
                    Config.CHUNK_SIZE,
                    None,  # bot,
                    Translation.DOWNLOAD_START,
                    update.message_id,
                    update.chat.id
                )
                if os.path.exists(thumb_image_path):
                    im = Image.open(thumb_image_path).convert("RGB")
                    im.save(thumb_image_path.replace(".webp", ".jpg"), "jpeg")
                else:
                    thumb_image_path = None
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.FORMAT_SELECTION.format(thumbnail) + "\n" + Translation.SET_CUSTOM_USERNAME_PASSWORD,
                    reply_markup=reply_markup,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )
            else:
                # fallback for nonnumeric port a.k.a seedbox.io
                inline_keyboard = []
                cb_string_file = "{}={}={}".format(
                    "file", "LFO", "NONE")
                cb_string_video = "{}={}={}".format(
                    "video", "OFL", "ENON")
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "SVideo",
                        callback_data=(cb_string_video).encode("UTF-8")
                    ),
                    InlineKeyboardButton(
                        "DFile",
                        callback_data=(cb_string_file).encode("UTF-8")
                    )
                ])
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                await bot.send_message(
                    chat_id=update.chat.id,
                    text=Translation.FORMAT_SELECTION.format(""),
                    reply_markup=reply_markup,
                    parse_mode="html",
                    reply_to_message_id=update.message_id
                )
