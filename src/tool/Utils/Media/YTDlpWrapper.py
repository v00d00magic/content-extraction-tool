from Plugins.App.Storage.Storage import app
import yt_dlp

class YTDlpWrapper:
    def download_hook(self, d):
        if d['status'] == 'downloading':
           percent_str_clear = d['_percent_str'].replace('[0;94m', '')
           percent_str = percent_str_clear
           percent_str = ''.join(chr for chr in percent_str if chr.isprintable())
           percent = percent_str.split('%')[0].strip()

           app.logger.log(kind="progress",message=f"Downloaded {percent}%",section="YtDlp")
        elif d['status'] == 'finished':
           app.logger.log(kind="success",message=f"Successfully downloaded",section="YtDlp")
    
    def __init__(self, opts):
        # 'outtmpl': 'downloads/%(title)s.mp4',
        self.ydl_opts = {'quiet': True, 'progress_hooks': [self.download_hook], "ratelimit": float(app.config.get("net.max_speed")) * 1024}
        #self.ydl_opts["quiet"] = False
        self.ydl_opts.update(opts)

        self.ydl = yt_dlp.YoutubeDL(self.ydl_opts)
