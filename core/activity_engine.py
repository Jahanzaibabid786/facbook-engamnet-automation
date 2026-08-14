import time
import random
from typing import Dict, Any, List, Optional
from utils.logger import logger
from utils.database import Database

class ActivityEngine:
    def __init__(self, interaction_manager=None, config_path: str = "config/activity_config.json"):
        import json
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.db = Database()
        self.interaction = interaction_manager
        self.activities = self.config.get('activities', {})
        self.daily_limits = self.config.get('daily_limits', {})

    def execute_daily_activities(self, profile_id: str, session_id: int) -> Dict[str, Any]:
        """Execute configured daily activities for a profile"""
        logger.info(f"Starting daily activities for profile", profile_id)

        results = {
            'profile_id': profile_id,
            'session_id': session_id,
            'total_activities': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'activity_results': []
        }

        # Execute activities in order based on configuration
        if self.activities.get('feed_scrolling', False):
            result = self._execute_feed_browsing(profile_id)
            results['activity_results'].append(result)
            self._update_results_counter(results, result)

        if self.activities.get('reels', False):
            result = self._execute_reels(profile_id)
            results['activity_results'].append(result)
            self._update_results_counter(results, result)

        if self.activities.get('likes', False):
            result = self._execute_likes(profile_id)
            results['activity_results'].append(result)
            self._update_results_counter(results, result)

        if self.activities.get('comments', False):
            result = self._execute_comments(profile_id)
            results['activity_results'].append(result)
            self._update_results_counter(results, result)

        if self.activities.get('sharing', False):
            result = self._execute_sharing(profile_id)
            results['activity_results'].append(result)
            self._update_results_counter(results, result)

        if self.activities.get('stories', False):
            result = self._execute_stories(profile_id)
            results['activity_results'].append(result)
            self._update_results_counter(results, result)

        logger.info(f"Daily activities completed: {results['successful']} successful, {results['failed']} failed, {results['skipped']} skipped", profile_id)

        return results

    def _execute_feed_browsing(self, profile_id: str) -> Dict[str, Any]:
        """Execute feed scrolling activity"""
        try:
            logger.info("Starting feed browsing activity", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Browsing Facebook feed...")

            # Import here to avoid circular dependencies
            from facebook.feed import FeedBrowser
            feed_browser = FeedBrowser()

            result = feed_browser.browse_feed(profile_id, duration=30)

            self._log_activity(profile_id, 'feed_browsing', result)
            return result

        except Exception as e:
            logger.error(f"Feed browsing failed: {str(e)}", profile_id)
            result = {
                'activity_type': 'feed_browsing',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._log_activity(profile_id, 'feed_browsing', result)
            return result

    def _execute_reels(self, profile_id: str) -> Dict[str, Any]:
        """Execute reels watching activity"""
        try:
            logger.info("Starting reels activity", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Watching Reels...")

            from facebook.reels import ReelsWatcher
            reels_watcher = ReelsWatcher()

            limit = self.daily_limits.get('reels', 10)
            result = reels_watcher.watch_reels(profile_id, count=limit)

            self._log_activity(profile_id, 'reels', result)
            return result

        except Exception as e:
            logger.error(f"Reels activity failed: {str(e)}", profile_id)
            result = {
                'activity_type': 'reels',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._log_activity(profile_id, 'reels', result)
            return result

    def _execute_likes(self, profile_id: str) -> Dict[str, Any]:
        try:
            logger.info("Starting likes activity", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Liking posts...")

            from facebook.likes import LikeManager
            like_manager = LikeManager(self.interaction)

            limit = self.daily_limits.get('likes', 3)
            result = like_manager.like_posts(profile_id, count=limit)

            self._log_activity(profile_id, 'likes', result)
            return result

        except Exception as e:
            logger.error(f"Likes activity failed: {str(e)}", profile_id)
            result = {
                'activity_type': 'likes',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._log_activity(profile_id, 'likes', result)
            return result

    def _execute_comments(self, profile_id: str) -> Dict[str, Any]:
        try:
            logger.info("Starting comments activity", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Adding comments...")

            from facebook.comments import CommentManager
            comment_manager = CommentManager(self.interaction)

            limit = self.daily_limits.get('comments', 2)
            result = comment_manager.add_comments(profile_id, count=limit)

            self._log_activity(profile_id, 'comments', result)
            return result

        except Exception as e:
            logger.error(f"Comments activity failed: {str(e)}", profile_id)
            result = {
                'activity_type': 'comments',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._log_activity(profile_id, 'comments', result)
            return result

    def _execute_sharing(self, profile_id: str) -> Dict[str, Any]:
        """Execute sharing activity"""
        try:
            logger.info("Starting sharing activity", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Sharing content...")

            from facebook.sharing import ShareManager
            share_manager = ShareManager()

            limit = self.daily_limits.get('shares', 2)
            result = share_manager.share_content(profile_id, count=limit)

            self._log_activity(profile_id, 'sharing', result)
            return result

        except Exception as e:
            logger.error(f"Sharing activity failed: {str(e)}", profile_id)
            result = {
                'activity_type': 'sharing',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._log_activity(profile_id, 'sharing', result)
            return result

    def _execute_stories(self, profile_id: str) -> Dict[str, Any]:
        """Execute stories viewing activity"""
        try:
            logger.info("Starting stories activity", profile_id)
            print(f"[{time.strftime('%H:%M:%S')}] Viewing Stories...")

            from facebook.stories import StoriesViewer
            stories_viewer = StoriesViewer()

            result = stories_viewer.view_stories(profile_id)

            self._log_activity(profile_id, 'stories', result)
            return result

        except Exception as e:
            logger.error(f"Stories activity failed: {str(e)}", profile_id)
            result = {
                'activity_type': 'stories',
                'status': 'FAILED',
                'reason': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self._log_activity(profile_id, 'stories', result)
            return result

    def _log_activity(self, profile_id: str, activity_type: str, result: Dict[str, Any]):
        """Log activity result to database"""
        try:
            activity_data = {
                'profile_id': profile_id,
                'activity_type': activity_type,
                'status': result.get('status', 'UNKNOWN'),
                'timestamp': result.get('timestamp', time.strftime('%Y-%m-%d %H:%M:%S')),
                'duration': result.get('duration'),
                'details': result
            }
            self.db.insert_activity(activity_data)
        except Exception as e:
            logger.error(f"Failed to log activity: {str(e)}", profile_id)

    def _update_results_counter(self, results: Dict, activity_result: Dict):
        """Update activity results counters"""
        results['total_activities'] += 1
        status = activity_result.get('status', 'UNKNOWN')

        if status == 'SUCCESS':
            results['successful'] += 1
        elif status == 'SKIPPED':
            results['skipped'] += 1
        else:
            results['failed'] += 1
