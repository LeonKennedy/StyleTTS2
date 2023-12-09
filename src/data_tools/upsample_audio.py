import glob
import os
import soundfile as sf
import librosa


def up_wav_from_path(path):
    wave, sr = sf.read(path)

    if sr != 24000:
        wave = librosa.resample(wave, orig_sr=sr, target_sr=24000)
        print(path, sr)
        sf.write(path, wave, 24000)


def LJSpeech():
    root_dir = "/mnt/d4t/data/LJspeech/LJSpeech-1.1/wavs/"
    for i in glob.glob(os.path.join(root_dir, "*.wav")):
        up_wav_from_path(i)


if __name__ == "__main__":
    # up_wav_from_path("LJ023-0079.wav")
    LJSpeech()
