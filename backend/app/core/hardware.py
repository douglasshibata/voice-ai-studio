import torch
import psutil
import logging

logger = logging.getLogger("voice_ai_studio.hardware")

class HardwareDetector:
    @staticmethod
    def detect():
        cuda_available = torch.cuda.is_available()
        cuda_device_name = None
        cuda_vram_gb = 0.0

        if cuda_available:
            try:
                cuda_device_name = torch.cuda.get_device_name(0)
                cuda_vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
            except Exception as e:
                logger.warning(f"Error getting CUDA properties: {e}")

        mps_available = hasattr(torch.backends, "mps") and torch.backends.mps.is_available()

        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)

        recommended_device = "cpu"
        if cuda_available:
            recommended_device = "cuda"
        elif mps_available:
            recommended_device = "mps"

        return {
            "device": recommended_device,
            "cuda": {
                "available": cuda_available,
                "device_name": cuda_device_name,
                "vram_gb": cuda_vram_gb
            },
            "mps": {
                "available": mps_available
            },
            "system": {
                "ram_gb": ram_gb,
                "cpu_cores": psutil.cpu_count(logical=True)
            }
        }
