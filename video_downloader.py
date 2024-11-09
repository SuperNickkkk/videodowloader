import yt_dlp

def download_video():
    print("请输入视频链接地址：")
    url = input().strip()
    
    ydl_opts = {
        'format': 'bv*+ba/b',  # 使用更好的格式选择器
        'outtmpl': '%(title)s-%(id)s.%(ext)s',  # 添加视频ID避免重名
        'progress_hooks': [show_progress],
        'writesubtitles': True,  # 下载字幕
        'writethumbnail': True,  # 下载缩略图
        'postprocessors': [{
            'key': 'FFmpegMetadata',  # 添加元数据
            'add_metadata': True,
        }],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("开始下载视频...")
            info = ydl.extract_info(url, download=True)
            print(f"\n成功下载: {info.get('title')}")
            
    except Exception as e:
        print(f"下载出错: {str(e)}")
        
def show_progress(d):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        print(f"\r下载进度: {percent} 速度: {speed} 剩余时间: {eta}", end='')
    elif d['status'] == 'finished':
        print("\n下载完成,正在处理...")

if __name__ == "__main__":
    download_video()