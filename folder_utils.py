import os
import re


def remove_watermark(folder_path: str, watermark_pattern: [str | re.Pattern], walk: bool = False):
    """
    Функция для удаления вотемарок из названий файлов и папок

    :param folder_path: абсолютный путь к папке с непотребными названиями
    :param watermark_pattern: шаблон вотемарки, которую необходимо удалить
    :param walk: использовать обход всех подпапок
    """

    if isinstance(watermark_pattern, str):
        watermark_pattern = re.compile(watermark_pattern)

    if walk:
        for dp, ds, fs in os.walk(folder_path):
            for file_name in fs:
                if re.search(watermark_pattern, file_name):
                    src = f'{dp}\\{file_name}'
                    dst = f'{dp}\\{re.sub(watermark_pattern, "", file_name)}'
                    os.rename(src, dst)

            if re.search(watermark_pattern, dp):
                dst = re.sub(watermark_pattern, '', dp)
                os.rename(dp, dst)
    else:
        for name in os.listdir(folder_path):
            if re.search(watermark_pattern, name):
                src = f'{folder_path}\\{name}'
                dst = f'{folder_path}\\{re.sub(watermark_pattern, "", name)}'
                os.rename(src, dst)


if __name__ == '__main__':
    path = r'D:\Obsidian\Саморазвитие\Курсы\Backend на FastAPI\3. Вперед в production!'
    watermark = r'(?i) ?\[(?:openssource|supersliv)\.(?:org|bz|biz)\] ?'
    remove_watermark(path, watermark, walk=True)
