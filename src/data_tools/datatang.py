#!/usr/bin/env python
# encoding: utf-8
"""
@author: coffee
@license: (C) Copyright 2022-2032, Node Supply Chain Manager Corporation Limited.
@contact: leonhe0119@gmail.com
@file: datatang.py.py
@time: 2023/12/9 15:19
@desc:
"""
import os
import glob
from shutil import copyfile

import librosa
import phonemizer
import soundfile as sf


def run():
    origin_path = "/mnt/d4t/xudonglong/dataset"
    global_phonemizer = phonemizer.backend.EspeakBackend(
        language="en-us",
        preserve_punctuation=True,
        with_stress=True,
        words_mismatch="ignore",
    )
    for p in glob.glob(os.path.join(origin_path, "G0*")):
        data = role(p)
        _save_data(data, global_phonemizer)


def _save_data(data, global_phonemizer):
    with open("tang.lst", "a+") as f:
        for record in data:
            path = "/".join(record[0].split("/")[-2:])
            phoneme = global_phonemizer.phonemize([record[1]])[0]
            row = "|".join([path, phoneme, str(record[2])])
            f.write(row + "\n")


def role(ori_path: str):
    pid = int(os.path.basename(ori_path)[1:])
    out = []
    for p in glob.glob(os.path.join(ori_path, "*.wav")):
        path = audio(p)
        if path:
            txt_path = p.replace(".wav", ".txt")
            text = _read_text(txt_path)
            out.append((path, text, pid))
    return out


def _read_text(path: str) -> str:
    with open(path, "r") as f:
        txt = f.read()
        return txt.strip()


def audio(wav_path: str) -> str:
    path = os.path.join(des_path, os.path.basename(wav_path))
    if os.path.exists(path):
        return path

    wav, sr = sf.read(wav_path)
    flag = _check_duration(wav, sr)
    if not flag:
        print(wav_path, "less 1 second!!")
        return

    if sr != 24000:
        wave = librosa.resample(wav, orig_sr=sr, target_sr=24000)
        sf.write(path, wave, 24000)
        print("[resample]", wav_path, "to", des_path)
    else:
        copyfile(wav_path, path)
    return path


def _check_duration(wav, sr: int) -> bool:
    if wav.shape[0] / sr > 1:
        return True
    else:
        return False


if __name__ == '__main__':
    des_path = "/mnt/d4t/data/datatang"
    run()
