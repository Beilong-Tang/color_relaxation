"""
This class is used to support online inferencing for server deployment
"""
import torch
import soundfile as sf
import librosa
import numpy as np
from funcodec.bin.text2audio_inference import Text2Audio
from funcodec.bin.text2audio_inference import save_audio
import nltk


class Text2AudioWrapper(Text2Audio):

    def __init__(self, config_file = None, model_file = None, device = "cuda", dtype = "float32", **kwargs):
        super().__init__(config_file, model_file, device, dtype, **kwargs)
        self.prompt_audio = None
        self.prompt_text = None
        self.continual = True # Allow continual

        self.change_prompt_audio_and_text("/DKUdata/tangbl/FunCodec/FunCodec/egs/LibriTTS/text2speech_laura/demo/8230_279154_000013_000003.wav", "one of these is context")
    
    def change_prompt_audio_and_text(self, prompt_audio_path, text):
        """
        This function should be triggered whenever users change the prompt audio 

        [1,1,T]
        """
        def read_audio(filename, force_1ch=True, fs=16000):
            audio, fs_ = sf.read(filename, always_2d=True)
            audio = audio[:, :1].T if force_1ch else audio.T
            if fs is not None and fs != fs_:
                audio = librosa.resample(audio, orig_sr=fs_, target_sr=fs, res_type="soxr_hq")
                return audio, fs
            return audio, fs_

        audio, fs_ = read_audio(prompt_audio_path)
        self.prompt_audio = torch.from_numpy(audio).unsqueeze(0).cuda().float() # [1,1,T]
        self.prompt_text = text
    
    @torch.no_grad()
    def __call__(self, text, output_path:str):
        """
        This method will call the model to infer on texts, and saves the audio to output_path
        """
        sentences = nltk.tokenize.sent_tokenize(text)
        res = []
        for _sent in sentences:
            _r = self._generate_split(_sent)
            res.append(_r.squeeze(0)) # [T]
        res = torch.cat(res, dim = 0).unsqueeze(0) # [1,T]
        torch.cuda.empty_cache()
        save_audio(res, output_path, 16000, True)
    
    @torch.no_grad()
    def _generate_split(self, text:str):
        """Inference

        Args:
            text: Input text data
            prompt_text: Prompt text for zero-shot adaption
            prompt_audio: Prompt audio for zero-shot adaption
        Returns:
            generation audios: [1,T]
        """
        prompt_text = self.prompt_text
        prompt_audio = self.prompt_audio
        self.model.eval()
        continual_mode = self.continual 
        if continual_mode:
            text = " ".join([prompt_text, text]).strip()
            codec = self.codec_model(prompt_audio, run_mod="encode")[0][0].squeeze(1).transpose(0,1)
            continual = codec[:, :self.model.predict_nq].tolist()
            continual_length = len(continual) if self.exclude_prompt else 0
        else:
            continual = None
            continual_length = None

        # 0. extract text embeddings
        text_emb, text_emb_lens = self.text_emb_model(text)

        # 1. encode text
        text_outs, text_out_lens = self.model.encode(text_emb, text_emb_lens)

        # 2. decode first codec group
        decoded_codec = self.model.decode_codec(
            text_outs,
            text_out_lens,
            max_length=30 * 25,
            sampling=self.sampling,
            beam_size=self.beam_size,
            continual=continual
        )

        # _, _, gen_speech_only_lm, _ = self.codec_model(
        #     decoded_codec[:, continual_length:],
        #     bit_width=None,
        #     run_mod="decode"
        # )

        # 3. predict embeddings
        gen_speech = self.model.syn_audio(
            decoded_codec, text_outs, text_out_lens, self.codec_model,
            continual_length=continual_length,
        )

        ret_val = dict(
            gen=gen_speech,
            # gen_only_lm=gen_speech_only_lm,
        )

        return ret_val['gen'][0] # [1,T]
