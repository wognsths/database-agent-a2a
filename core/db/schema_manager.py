import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

USER_DESCRIPTION_DIR = "data/user_descriptions"
USER_DESCRIPTION_PATH = os.path.join(USER_DESCRIPTION_DIR, "user_description.json")

os.makedirs(USER_DESCRIPTION_DIR, exist_ok=True)

class UserDescriptionManager:
    def __init__(self):
        self.user_description: Optional[Dict[str, Any]] = None
        self._load_user_description()

    def _load_user_description(self):
        if os.path.exists(USER_DESCRIPTION_PATH):
            try:
                with open(USER_DESCRIPTION_PATH, "r", encoding="utf-8") as f:
                    self.user_description = json.load(f)
                    logger.info("Loaded user-defined description")
            except Exception as e:
                logger.error(f"Error loading description: {e}")

    def get_user_description(self) -> Optional[Dict[str, Any]]:
        return self.user_description

    def upload_user_description(self, description_data: Dict[str, Any]) -> bool:
        enriched = {
            **description_data,
            "_metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "is_user_defined": True,
            },
        }
        self.user_description = enriched
        return self._save_description("uploaded")

    def _save_description(self, log_prefix: str) -> bool:
        try:
            with open(USER_DESCRIPTION_PATH, "w", encoding="utf-8") as f:
                json.dump(self.user_description, f, ensure_ascii=False, indent=2)
            logger.info(f"User description {log_prefix}")
            return True
        except Exception as e:
            logger.error(f"Failed to save description: {e}")
            return False


user_description_manager = UserDescriptionManager()
