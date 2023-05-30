# ╭─────────────────────────── Import ───────────────────────────╮ #
import os
import json

try:from lxml import etree
except:
    os.system('pip install lxml')
    from lxml import etree

try:import requests
except:
    os.system('pip install requests')
    import requests

try:from bs4 import BeautifulSoup
except:
    os.system('pip install bs4')
    from bs4 import BeautifulSoup


# ╭─────────────────────────── Version ───────────────────────────╮ #
VERSIONID = '1.0.0'


# ╭─────────────────────────── Colors ───────────────────────────╮ #
red = "\033[0;31m"
green = "\033[0;32m"
reset = "\033[0m"


# ╭─────────────────────────── Pattern ───────────────────────────╮ #
pattern = r"https://v\.redd\.it/([^/,\"]+)"



# ╭─────────────────────────── Config ───────────────────────────╮ #


# ╭─── Default config data ───╮ #
default_config = """{
    "log": true,
    "version": true
}"""


# ╭─── Create config.json ───╮ #
if not os.path.exists('config.json'):open('config.json', 'w', encoding='utf-8').write(default_config)


# ╭─── Load Config ───╮ #
config_data = json.loads(open('config.json', 'r', encoding='utf-8').read())
try:log_statut = config_data["log"]  # Read log data
except:log_statut = True
try:version = config_data["version"]  # Read version data
except:version = True




# ╭─────────────────────────── Def DownloadRedditVideo ───────────────────────────╮ #
def RedditVideoDownloader(url, path, filename=None):
    try:
        # ╭─── Author ───╮ #
        if log_statut == True:print(f'{reset}[{green}-{reset}] Reddit Video Downloader by TheGrayDream, need help or report a bug? https://dsc.gg/tgdgithub')


        # ╭─── Check Version ───╮ #
        if version == True:
            try:
                if not requests.get('https://raw.githubusercontent.com/thegraydream/Reddit-Video-Downloader/master/version').text.strip() == VERSIONID:
                    if log_statut == True:print(f'{red}You are not using the latset version of Reddit Video Downloader, please update it on "https://github.com/thegraydream/Reddit-Video-Downloader".{reset}')
                    r = input('Would you like to download the latest version? (y/n) > ').strip()
                    if r == "y":
                        for dow in json.loads(requests.get(f'https://raw.githubusercontent.com/thegraydream/Reddit-Video-Downloader/master/update.json').text)["update"]:
                            print(f'{reset}[{green}>{reset}] {green}Downloading {dow}{reset}')
                            try:
                                content = requests.get(f'https://raw.githubusercontent.com/thegraydream/Reddit-Video-Downloader/master/{dow}').text
                                if content == "404: Not Found":print(f'{reset}[{red}>{reset}] {red} We cannot find the file {dow}')
                                else:
                                    open(dow, 'w', encoding='utf-8').write(content)
                            except:
                                print(f'{reset}[{red}<{reset}] {red} An error occurred while downloading the latest version of {dow}')
                                return False, f'Update download error ({dow})'
                        return True, 'Update completed successfully, please restart program'
            except:return False, f'Update download error'

        # ╭─── Send a request to url ───╮ #
        if log_statut == True:print(f'{reset}[{green}>{reset}] {green}A request has been sent to https://rapidsave.com/info?url={url}{reset}')
        response = requests.get(f'https://rapidsave.com/info?url={url}')
        if log_statut == True:print(f'{reset}[{green}<{reset}] {green}The request has been received, statut code: {response.status_code}{reset}')
        if not "Invalid reddit post" in response.text:


            # ╭─── Get Data ───╮ #
            html_data = BeautifulSoup(response.text, 'html.parser')
            html_tree = etree.HTML(str(html_data))

            try:
                downloadlinkxml = html_tree.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/table[2]/tbody/tr/td[1]/div/a') # Get Download Link
                downloadlink = str(downloadlinkxml[0].get('href')).strip()
            except:downloadlink = None

            try:
                subredditxml = html_tree.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/table[1]/tbody/tr[3]/td[2]') # Get SubReddit
                subreddit = str(subredditxml[0].text).strip()
            except:subreddit = None

            try:
                downloadsizexml = html_tree.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/table[1]/tbody/tr[5]/td[2]') # Get Download Size
                downloadsize = str(downloadsizexml[0].text).strip()
            except:downloadsize = None

            try:
                titlexml = html_tree.xpath('/html/body/div[3]/div[2]/div[2]/h2') # Get Title
                title = str(titlexml[0].text).strip()
            except:title = None

            if log_statut == True:print(f'{reset}[{green}+{reset}] {green}The video has been found! title: {title}, subreddit: {subreddit}')       


            # ╭─── Create Folder ───╮ #
            try:
                if not os.path.exists(path):
                    os.makedirs(path, exist_ok=True)
                    if log_statut == True:print(f'{reset}[{green}+{reset}] {green}create a new directory "{path}"{reset}')
            except:
                if log_statut == True:print(f"{reset}[{red}-{reset}] {red}Unable to create folder {path}")
                path = ""
            

            # ╭─── Downloading Data ───╮ #
            try:
                if log_statut == True:print(f'{reset}[{green}>{reset}] {green}A request has been sent to {downloadlink}{reset}')
                get_video = requests.get(downloadlink)
                if log_statut == True:print(f'{reset}[{green}<{reset}] {green}The request has been received, statut code: {get_video.status_code}{reset}')

                if log_statut == True:print(f'{reset}[{green}>{reset}] {green}Download video, {downloadsize}{reset}')
                if filename == None:filename = title

                with open(f'{path}/{filename}.mp4', "wb") as file:
                    file.write(get_video.content)
                if log_statut == True:print(f'{reset}[{green}<{reset}] {green}The video has been successfully downloaded ({path}/{filename}){reset}')

                return True, 'The video has been successfully downloaded', f'{path}/{filename}', title, subreddit
            except:
                print(f"{reset}[{red}-{reset}] {red}An error occurred while creating the video {path}{reset}")
                return False, 'An error occurred while creating the video'


        else:
            print(f"{reset}[{red}-{reset}] {red}Invalid link, please provide a link of this type: https://www.reddit.com/r/ThisLooksFun/comments/ID/SubReddit{reset}")
            return False, 'Invalid link'
    except:
        print(f"{reset}[{red}-{reset}] {red}An error occurred{reset}")
        return False, 'An error occurred'


# ╭───── USAGE ─────╮  ╭─────────────────────────── VIDEO LINK ───────────────────────────╮    ╭── PATH ──╮   ╭── VIDEO NAME ──╮ #
RedditVideoDownloader('https://www.reddit.com/r/ThisLooksFun/comments/13vlcjw/thislooksfun/', 'Best/Video/', 'myredditvideo.mp4')

# You can use this function with "from downloadredditvideo import downloadredditvideo"