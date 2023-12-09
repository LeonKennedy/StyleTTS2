import glob
import os
from typing import List
import soundfile as sf
from shutil import copyfile
import phonemizer
from nltk.tokenize import word_tokenize
from text_utils import TextCleaner


class DataSetName:
    tc100 = "train-clean-100"
    tc360 = "train-clean-360"
    tc460 = "train-clean-460"
    dev_clean = "dev-clean"
    dev_all = "dev"


def run(path: str, dir_name: str, save_name: str):
    for p in glob.glob(os.path.join(root_path, path, "*")):
        role(p, os.path.join(root_path, dir_name), save_name)


def role(ori_path: str, des_path: str, save_name: str):
    pid = ori_path.split("/")[-1]
    des_path = os.path.join(des_path, pid)
    os.makedirs(des_path, exist_ok=True)

    for p in glob.glob(os.path.join(ori_path, "*")):
        data = chapter(p, des_path, pid)
        _write(data, save_name)


def _write(data: List, save_name: str):
    with open(save_name, "a+") as f:
        f.writelines(["|".join(record) + "\n" for record in data])


def chapter(ori_path: str, des_path: str, pid: str):
    global_phonemizer = phonemizer.backend.EspeakBackend(
        language="en-us",
        preserve_punctuation=True,
        with_stress=True,
        words_mismatch="ignore",
    )
    textclenaer = TextCleaner()
    chapter_id = ori_path.split("/")[-1]
    des_chapter_path = os.path.join(des_path, chapter_id)
    os.makedirs(des_chapter_path, exist_ok=True)

    out = []
    for p in glob.glob(os.path.join(ori_path, "*.wav")):
        save_path, txt = audio(p, des_chapter_path)
        if save_path:
            ps = global_phonemizer.phonemize([txt])
            ps2 = word_tokenize(ps[0])
            ps2 = " ".join(ps2)

            tokens = textclenaer(ps2)
            tokens.insert(0, 0)

            sub_path = "/".join(save_path.split("/")[-5:])
            out.append((sub_path, ps2, pid))
    return out


def audio(wav_path: str, des_path: str):
    wav_name = os.path.basename(wav_path)
    # text_original_path = wav_path.replace("wav", "original.txt")
    # assert os.path.exists(text_original_path)
    text_normal_path = wav_path.replace("wav", "normalized.txt")
    assert os.path.exists(text_normal_path)
    txt = _read_text(text_normal_path)

    save_path = _move_audio(wav_path, os.path.join(des_path, wav_name))
    if save_path:
        return (save_path, txt)
    return "", ""


def _read_text(path: str) -> str:
    with open(path, "r") as f:
        txt = f.read()
        return txt.strip()


def _move_audio(wav_path: str, des_path: str) -> str:
    if os.path.exists(des_path):
        return des_path
    wav, sr = sf.read(wav_path)
    flag = _check_duration(wav, sr)
    if not flag:
        print(wav_path, "less 1 second!!")
        return

    if sr != 24000:
        wave = librosa.resample(wave, orig_sr=sr, target_sr=24000)
        sf.write(des_path, wave, 24000)
        print("[resample]", wav_path, "to", des_path)
    else:
        copyfile(wav_path, des_path)
    return des_path


def _check_duration(wav, sr: int) -> bool:
    if wav.shape[0] / sr > 1:
        return True
    else:
        return False


def run_train():
    run(os.path.join(root_path, DataSetName.tc100))


def run_dev():
    run(DataSetName.dev_clean, DataSetName.dev_all, "dev.lst")


if __name__ == "__main__":
    root_path = "/mnt/d4t/data/LibriTTS/LibriTTS"
    run_dev()
    # run(os.path.join(root_path, "train-clean-360"))
