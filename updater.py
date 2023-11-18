import glob, os, urllib.request, json, shutil, sys
import tkinter.messagebox
from version import VERSION

# 更新に関するクラス
class Updater(object):
    def __init__(self) -> None:
        self.latest_release_url = "https://api.github.com/repos/kottEy/osu_SkinTools/releases/latest"
        self.latest_version = ""
        self.zip_url = ""
        self.current_dir = os.getcwd()
        self.zip_name = os.path.join(self.current_dir, "update_program.zip")
        self.update_dir = os.path.join(self.current_dir, "update_program")
        self.now_version = VERSION

    # アップデートを確認する
    # アップデートがある -> True, アップデートがない -> False
    def check_update(self):
        body = self._get_latest_release()
        if body is None:
            return False
        json_body = json.loads(body)
        self.zip_url = json_body["assets"][0]["browser_download_url"]
        self.latest_version = json_body["tag_name"]
        if self.latest_version == self.now_version:
            return False
        return True

    # github rest apiをたたいてlatest releaseを取得
    def _get_latest_release(self):
        req: object = urllib.request.Request(self.latest_release_url)
        try:
            with urllib.request.urlopen(req) as res:
                return res.read()
        except:
            return None

    # アプリの更新
    def update_application(self):
        self._download_update()
        self._unpack_update()
        self._apply_update()

    # 更新プログラムのダウンロード
    def _download_update(self):
        print("[INFO] 更新プログラムのダウンロードを開始します。")
        urllib.request.urlretrieve(self.zip_url, self.zip_name)
        print("[SUCCESS] 更新プログラムのダウンロードが完了しました。")

    # 更新プログラムの解凍
    def _unpack_update(self):
        print("[INFO] 更新プログラムの解凍を開始します。")
        shutil.unpack_archive(self.zip_name, self.update_dir)
        print("[INFO] 更新プログラムの解凍が完了しました。")

    def _apply_update(self):
        print("[INFO] 更新プログラムの適用を開始します。")
        update_files = glob.glob(os.path.join(self.update_dir, "*"))
        for update_file in update_files:
            if os.path.basename(update_file) == 'images':
                pass
            elif os.path.basename(update_file) == 'updater.exe':
                pass
            else:
                shutil.move(update_file, os.path.join(self.current_dir, os.path.basename(update_file)))
                print(f"[INFO] Moved {update_file}")
        shutil.rmtree(self.update_dir)
        os.remove(self.zip_name)
        print(f"[INFO] Removed {self.zip_name}")
        os.rmdir(self.update_dir)
        print(f"[INFO] Removed {self.update_dir}")
        print("[INFO] 更新プログラムの適用が完了しました。")

# updater.exeはここが実行される
if __name__ == "__main__":
    print("[INFO] アップデートを開始します。")
    ud = Updater()
    if not ud.check_update():
        print("[ERROR] 更新プログラムが見つかりませんでした。")
        sys.exit()
    ud.update_application()
    print("[INFO] アップデートが終了しました。")
    tkinter.messagebox.showinfo("更新終了", "更新が終了しました。")