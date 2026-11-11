import os
import unittest
from app.services.studio_workflows import StudioAudioWorkflows

class TestStudioWorkflows(unittest.TestCase):
    def test_tts_workflow(self):
        res = StudioAudioWorkflows.tts_synthesize("Texto de teste para TTS.", speed=1.1)
        self.assertIn("audio_path", res)
        self.assertTrue(os.path.exists(res["audio_path"]))

    def test_stt_workflow(self):
        res = StudioAudioWorkflows.stt_transcribe("dummy.wav", diarize=True)
        self.assertIn("segments", res)
        self.assertIn("text", res)

    def test_dubbing_workflow(self):
        res = StudioAudioWorkflows.video_dubbing_pipeline(
            video_path="sample.mp4",
            target_language="en-US",
            voice_mapping={"Speaker 1": "piper-pt-br-faber-medium"}
        )
        self.assertIn("dubbed_video_path", res)
        self.assertEqual(res["target_language"], "en-US")
        self.assertGreater(len(res["segments"]), 0)

    def test_audiobook_workflow(self):
        chapters = [
            {"title": "Capítulo 1", "content": "Era uma vez um sistema de IA de voz local."},
            {"title": "Capítulo 2", "content": "Ele processava áudio com total privacidade e velocidade."}
        ]
        voice_map = {"Narrator": "piper-pt-br-faber-medium"}
        res = StudioAudioWorkflows.audiobook_studio_process("Doc Full Text", chapters, voice_map)
        self.assertEqual(res["total_chapters"], 2)
        self.assertIn("audiobook_path", res)

if __name__ == "__main__":
    unittest.main()
