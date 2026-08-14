import shutil
from pathlib import Path
from typing import List
from utils.logger import logger
from utils.database import Database

class ProfileCleaner:
    def __init__(self):
        self.db = Database()
        self.profiles_base = Path("profiles/profile_data")
        self.metadata_base = Path("profiles/metadata")

    def clean_all_profiles(self) -> bool:
        try:
            logger.info("Starting complete profile cleanup")

            if self.profiles_base.exists():
                shutil.rmtree(self.profiles_base)
                logger.info("Removed all profile data directories")

            if self.metadata_base.exists():
                shutil.rmtree(self.metadata_base)
                logger.info("Removed all profile metadata")

            self.profiles_base.mkdir(parents=True, exist_ok=True)
            self.metadata_base.mkdir(parents=True, exist_ok=True)

            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles")
            cursor.execute("DELETE FROM activities")
            cursor.execute("DELETE FROM sessions")
            conn.commit()
            conn.close()

            logger.info("Cleared all profile database records")
            return True

        except Exception as e:
            logger.error(f"Failed to clean profiles: {str(e)}")
            return False

    def clean_profile(self, profile_id: str) -> bool:
        try:
            logger.info(f"Cleaning profile: {profile_id}")

            profile = self.db.get_profile(profile_id)
            if not profile:
                logger.warning(f"Profile not found: {profile_id}")
                return False

            profile_path = Path(profile['profile_path']).parent
            if profile_path.exists():
                shutil.rmtree(profile_path)
                logger.info(f"Removed profile directory: {profile_path}")

            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE profile_id = ?", (profile_id,))
            cursor.execute("DELETE FROM activities WHERE profile_id = ?", (profile_id,))
            cursor.execute("DELETE FROM sessions WHERE profile_id = ?", (profile_id,))
            conn.commit()
            conn.close()

            logger.info(f"Profile cleaned successfully: {profile_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to clean profile {profile_id}: {str(e)}")
            return False

    def list_orphaned_profiles(self) -> List[str]:
        orphaned = []

        if not self.profiles_base.exists():
            return orphaned

        for profile_dir in self.profiles_base.iterdir():
            if profile_dir.is_dir():
                profile_id = profile_dir.name
                profile = self.db.get_profile(profile_id)
                if not profile:
                    orphaned.append(profile_id)

        return orphaned

    def clean_orphaned_profiles(self) -> int:
        orphaned = self.list_orphaned_profiles()
        cleaned = 0

        for profile_id in orphaned:
            try:
                profile_path = self.profiles_base / profile_id
                if profile_path.exists():
                    shutil.rmtree(profile_path)
                    logger.info(f"Removed orphaned profile: {profile_id}")
                    cleaned += 1
            except Exception as e:
                logger.error(f"Failed to clean orphaned profile {profile_id}: {str(e)}")

        return cleaned
