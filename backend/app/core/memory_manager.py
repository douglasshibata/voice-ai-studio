import gc
import logging

logger = logging.getLogger("voice_ai_studio.memory")

class ModelMemoryManager:
    def __init__(self, max_vram_gb: float = 8.0):
        self.max_vram_gb = max_vram_gb
        self.loaded_models = {} # model_id -> dict(instance, vram_gb, loaded_at)

    def load_model(self, model_id: str, load_fn, vram_gb: float = 1.0):
        if model_id in self.loaded_models:
            logger.info(f"Model {model_id} is already loaded.")
            return self.loaded_models[model_id]["instance"]

        total_allocated = sum(item["vram_gb"] for item in self.loaded_models.values())
        if total_allocated + vram_gb > self.max_vram_gb:
            logger.info("VRAM limit exceeded. Unloading oldest idle models...")
            self.unload_oldest()

        logger.info(f"Loading model {model_id} (~{vram_gb} GB VRAM)...")
        instance = load_fn()
        self.loaded_models[model_id] = {
            "instance": instance,
            "vram_gb": vram_gb
        }
        return instance

    def unload_model(self, model_id: str):
        if model_id in self.loaded_models:
            logger.info(f"Unloading model {model_id}...")
            del self.loaded_models[model_id]
            gc.collect()
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except ImportError:
                pass

    def unload_oldest(self):
        if self.loaded_models:
            first_key = next(iter(self.loaded_models))
            self.unload_model(first_key)

    def flush_all(self):
        keys = list(self.loaded_models.keys())
        for model_id in keys:
            self.unload_model(model_id)

    def get_loaded_info(self):
        return {
            model_id: {"vram_gb": info["vram_gb"]}
            for model_id, info in self.loaded_models.items()
        }

memory_manager = ModelMemoryManager()
