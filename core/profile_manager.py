import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from utils.database import Database
from utils.logger import logger

class ProfileManager:
    def __init__(
        self,
        base_path: str = "profiles/profile_data",
        metadata_path: str = "profiles/metadata",
        db_path: str = "database/app.db"
    ):
        self.base_path = Path(base_path)
        self.metadata_path = Path(metadata_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        self.db = Database(db_path)

    def create_profile(
        self,
        profile_name: str,
        device_id: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            # Ensure directories exist
            self.base_path.mkdir(parents=True, exist_ok=True)
            self.metadata_path.mkdir(parents=True, exist_ok=True)

            profile_id = self._generate_profile_id()
            profile_dir = self.base_path / profile_id
            chrome_data_dir = profile_dir / "chrome_data"

            profile_dir.mkdir(parents=True, exist_ok=True)
            chrome_data_dir.mkdir(parents=True, exist_ok=True)

            created_at = datetime.now().isoformat()

            profile_data = {
                'profile_id': profile_id,
                'profile_name': profile_name,
                'profile_path': str(chrome_data_dir),
                'status': 'CREATING',
                'device_id': device_id,
                'created_at': created_at,
                'metadata': {}
            }

            self.db.insert_profile(profile_data)

            metadata = {
                'profile_id': profile_id,
                'name': profile_name,
                'status': 'CREATING',
                'device_type': None,
                'browser_type': 'chrome',
                'user_agent_id': device_id,
                'created_at': created_at,
                'last_used': None,
                'total_sessions': 0
            }

            metadata_file = self.metadata_path / f"{profile_id}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

            state_file = profile_dir / "state.json"
            state = {
                'profile_id': profile_id,
                'status': 'CREATING',
                'last_validation': None,
                'validation_attempts': 0,
                'last_error': None
            }
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)

            logger.info(f"Profile created: {profile_id} ({profile_name})")
            return profile_data

        except Exception as e:
            logger.error(f"Failed to create profile: {str(e)}")
            raise

    def update_profile_status(
        self,
        profile_id: str,
        status: str,
        error_message: Optional[str] = None
    ):
        try:
            updates = {
                'status': status,
                'last_validated': datetime.now().isoformat()
            }
            self.db.update_profile(profile_id, updates)

            metadata_file = self.metadata_path / f"{profile_id}_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                metadata['status'] = status
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)

            profile_dir = self.base_path / profile_id
            state_file = profile_dir / "state.json"
            if state_file.exists():
                with open(state_file, 'r') as f:
                    state = json.load(f)
                state['status'] = status
                state['last_validation'] = datetime.now().isoformat()
                if error_message:
                    state['last_error'] = error_message
                state['validation_attempts'] = state.get('validation_attempts', 0) + 1
                with open(state_file, 'w') as f:
                    json.dump(state, f, indent=2)

            logger.info(f"Profile {profile_id} status updated to: {status}", profile_id)

        except Exception as e:
            logger.error(f"Failed to update profile status: {str(e)}", profile_id)
            raise

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        return self.db.get_profile(profile_id)

    def get_all_profiles(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.db.get_all_profiles(status)

    def get_active_profiles(self) -> List[Dict[str, Any]]:
        return self.db.get_all_profiles(status='ACTIVE')

    def delete_profile(self, profile_id: str) -> bool:
        try:
            profile_dir = self.base_path / profile_id
            if profile_dir.exists():
                shutil.rmtree(profile_dir)

            metadata_file = self.metadata_path / f"{profile_id}_metadata.json"
            if metadata_file.exists():
                metadata_file.unlink()

            logger.info(f"Profile deleted: {profile_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete profile: {str(e)}", profile_id)
            return False

    def update_profile_last_used(self, profile_id: str):
        try:
            updates = {
                'last_used': datetime.now().isoformat(),
                'total_sessions': self.db.get_profile(profile_id).get('total_sessions', 0) + 1
            }
            self.db.update_profile(profile_id, updates)

        except Exception as e:
            logger.error(f"Failed to update last_used: {str(e)}", profile_id)

    def get_profile_path(self, profile_id: str) -> Optional[str]:
        profile = self.db.get_profile(profile_id)
        if profile:
            return profile['profile_path']
        return None

    def _generate_profile_id(self) -> str:
        existing_profiles = self.db.get_all_profiles()
        profile_numbers = []

        for profile in existing_profiles:
            pid = profile['profile_id']
            if pid.startswith('profile_'):
                try:
                    num = int(pid.split('_')[1])
                    profile_numbers.append(num)
                except:
                    pass

        next_number = max(profile_numbers) + 1 if profile_numbers else 1
        return f"profile_{next_number:03d}"

    def cleanup_profile(self, profile_id: str):
        try:
            profile_dir = self.base_path / profile_id / "chrome_data"

            cleanup_dirs = ['Cache', 'Code Cache', 'GPUCache', 'Service Worker']
            for dir_name in cleanup_dirs:
                dir_path = profile_dir / dir_name
                if dir_path.exists():
                    shutil.rmtree(dir_path, ignore_errors=True)

            logger.info(f"Profile cleanup completed: {profile_id}", profile_id)

        except Exception as e:
            logger.warning(f"Profile cleanup had issues: {str(e)}", profile_id)
