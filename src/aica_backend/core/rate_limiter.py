from datetime import datetime, timedelta
from typing import Dict, List, Optional
from .config import settings


class RateLimiter:
    def __init__(self):
        self._failed_attempts: Dict[str, List[datetime]] = {}
        self._lockout_duration = timedelta(minutes=settings.LOCKOUT_DURATION_MINUTES)
        self._max_attempts = settings.MAX_LOGIN_ATTEMPTS
    
    def check_rate_limit(self, identifier: str) -> bool:
        now = datetime.utcnow()
        self._cleanup_old_attempts(identifier, now)
        
        attempts = self._failed_attempts.get(identifier, [])
        return len(attempts) < self._max_attempts
    
    def record_failed_attempt(self, identifier: str) -> None:
        now = datetime.utcnow()
        
        if identifier not in self._failed_attempts:
            self._failed_attempts[identifier] = []
        
        self._failed_attempts[identifier].append(now)
    
    def clear_failed_attempts(self, identifier: str) -> None:
        """Clear failed attempts for identifier."""
        if identifier in self._failed_attempts:
            del self._failed_attempts[identifier]
    
    def get_lockout_time_remaining(self, identifier: str) -> Optional[int]:
        """Get remaining lockout time in seconds."""
        if not self.check_rate_limit(identifier):
            attempts = self._failed_attempts.get(identifier, [])
            if attempts:
                oldest_relevant_attempt = attempts[0]
                unlock_time = oldest_relevant_attempt + self._lockout_duration
                remaining = (unlock_time - datetime.utcnow()).total_seconds()
                return max(0, int(remaining))
        
        return None
    
    def _cleanup_old_attempts(self, identifier: str, current_time: datetime) -> None:
        """Remove attempts older than lockout duration."""
        if identifier in self._failed_attempts:
            cutoff_time = current_time - self._lockout_duration
            self._failed_attempts[identifier] = [
                attempt for attempt in self._failed_attempts[identifier]
                if attempt > cutoff_time
            ]

            if not self._failed_attempts[identifier]:
                del self._failed_attempts[identifier]


rate_limiter = RateLimiter()
