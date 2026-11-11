import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import VoiceProfile

logger = logging.getLogger("voice_ai_studio.services.design")

class VoiceDesignService:
    @staticmethod
    def design_voice(
        db: Session,
        name: str,
        prompt_description: str,
        gender: str = "female",
        age_group: str = "adult",
        emotion: str = "calm",
        style: str = "professional",
        accent: str = "neutral",
        language: str = "pt-BR"
    ) -> VoiceProfile:
        """Parses natural text descriptions into acoustic parameter features."""
        pitch = 1.0
        rate = 1.0
        energy = 1.0

        if gender.lower() == "female":
            pitch = 1.2
        elif gender.lower() == "male":
            pitch = 0.8

        if "enthusiastic" in prompt_description.lower() or emotion == "excited":
            energy = 1.3
            rate = 1.1

        acoustic_features = {
            "gender": gender,
            "age_group": age_group,
            "emotion": emotion,
            "style": style,
            "accent": accent,
            "pitch": pitch,
            "rate": rate,
            "energy": energy,
            "description": prompt_description
        }

        profile = VoiceProfile(
            name=name,
            description=prompt_description,
            gender=gender,
            language=language,
            is_cloned=False,
            quality_score=95.0,
            acoustic_features=acoustic_features
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        logger.info(f"Designed voice profile {profile.id} ({name}) from prompt description.")
        return profile
