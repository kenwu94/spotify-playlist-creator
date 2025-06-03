import time
import threading
from collections import defaultdict, deque
from functools import wraps
from flask import request, jsonify
import logging

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(deque)
        self.lock = threading.Lock()
        
    def is_allowed(self, key, max_requests, window_seconds):
        """Check if request is allowed based on rate limits"""
        with self.lock:
            now = time.time()
            # Clean old requests outside the window
            while self.requests[key] and self.requests[key][0] <= now - window_seconds:
                self.requests[key].popleft()
            
            # Check if under limit
            if len(self.requests[key]) < max_requests:
                self.requests[key].append(now)
                return True
            return False
    
    def get_reset_time(self, key, window_seconds):
        """Get when the rate limit will reset"""
        with self.lock:
            if not self.requests[key]:
                return 0
            return int(self.requests[key][0] + window_seconds)

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(max_requests=10, window_seconds=60, per='ip', openai_calls_only=False):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        per: Rate limit per 'ip' or 'user' or 'global'
        openai_calls_only: If True, only limit OpenAI API calls
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get identifier based on 'per' parameter
            if per == 'ip':
                identifier = request.remote_addr
            elif per == 'user':
                # Use session or user ID if available
                identifier = request.headers.get('X-User-ID', request.remote_addr)
            else:  # global
                identifier = 'global'
            
            # Create unique key for this endpoint and identifier
            key = f"{f.__name__}:{identifier}"
            
            if not rate_limiter.is_allowed(key, max_requests, window_seconds):
                reset_time = rate_limiter.get_reset_time(key, window_seconds)
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Try again in {reset_time - int(time.time())} seconds.',
                    'retry_after': reset_time - int(time.time())
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Specific rate limiter for OpenAI calls
class OpenAIRateLimiter:
    def __init__(self):
        self.requests = defaultdict(deque)
        self.tokens_used = defaultdict(deque)
        self.lock = threading.Lock()        # Rate limits (adjust based on your OpenAI plan)
        self.REQUESTS_PER_MINUTE = 200  # Much higher for testing
        self.TOKENS_PER_MINUTE = 200000  # Much higher for testing
        self.REQUESTS_PER_DAY = 5000   # Much higher daily safety limit
        self.COST_LIMIT_PER_DAY = 20.0  # Much higher maximum daily cost in USD
        
        self.daily_cost = 0.0
        self.daily_reset_time = time.time() + 86400  # Reset daily limits
        
    def estimate_cost(self, prompt_tokens, completion_tokens=0, model="gpt-3.5-turbo"):
        """Estimate cost based on token usage"""
        # OpenAI pricing (update these based on current rates)
        pricing = {
            "gpt-4": {"input": 0.03/1000, "output": 0.06/1000},
            "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000},
            "gpt-3.5-turbo": {"input": 0.0015/1000, "output": 0.002/1000}
        }
        
        rates = pricing.get(model, pricing["gpt-3.5-turbo"])
        cost = (prompt_tokens * rates["input"]) + (completion_tokens * rates["output"])
        return cost
    
    def is_allowed(self, estimated_tokens=1000, model="gpt-3.5-turbo"):
        """Check if OpenAI request is allowed"""
        with self.lock:
            now = time.time()
            
            # Reset daily limits if needed
            if now > self.daily_reset_time:
                self.daily_cost = 0.0
                self.daily_reset_time = now + 86400
                # Clear daily request counters
                for key in list(self.requests.keys()):
                    if 'daily' in key:
                        del self.requests[key]
            
            # Clean old requests (1 minute window)
            minute_key = f"minute:{int(now // 60)}"
            day_key = f"daily:{int(now // 86400)}"
            
            # Check requests per minute
            current_minute_requests = len([r for r in self.requests[minute_key] if r > now - 60])
            if current_minute_requests >= self.REQUESTS_PER_MINUTE:
                return False, f"Rate limit: {self.REQUESTS_PER_MINUTE} requests/minute exceeded"
            
            # Check requests per day
            current_day_requests = len(self.requests[day_key])
            if current_day_requests >= self.REQUESTS_PER_DAY:
                return False, f"Daily limit: {self.REQUESTS_PER_DAY} requests/day exceeded"
            
            # Check estimated cost
            estimated_cost = self.estimate_cost(estimated_tokens, model=model)
            if self.daily_cost + estimated_cost > self.COST_LIMIT_PER_DAY:
                return False, f"Daily cost limit: ${self.COST_LIMIT_PER_DAY} exceeded"
            
            # All checks passed, record the request
            self.requests[minute_key].append(now)
            self.requests[day_key].append(now)
            self.daily_cost += estimated_cost
            
            return True, None
    
    def get_status(self):
        """Get current rate limit status"""
        now = time.time()
        minute_key = f"minute:{int(now // 60)}"
        day_key = f"daily:{int(now // 86400)}"
        
        current_minute_requests = len([r for r in self.requests[minute_key] if r > now - 60])
        current_day_requests = len(self.requests[day_key])
        
        return {
            "requests_this_minute": current_minute_requests,
            "requests_today": current_day_requests,
            "daily_cost": round(self.daily_cost, 4),
            "limits": {
                "requests_per_minute": self.REQUESTS_PER_MINUTE,
                "requests_per_day": self.REQUESTS_PER_DAY,
                "daily_cost_limit": self.COST_LIMIT_PER_DAY
            }
        }

# Global OpenAI rate limiter
openai_rate_limiter = OpenAIRateLimiter()

def openai_rate_limit(estimated_tokens=1000, model="gpt-3.5-turbo"):
    """Decorator specifically for OpenAI API calls"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            allowed, error_msg = openai_rate_limiter.is_allowed(estimated_tokens, model)
            
            if not allowed:
                logging.warning(f"OpenAI rate limit hit: {error_msg}")
                return jsonify({
                    'error': 'Service temporarily unavailable',
                    'message': 'Too many AI requests. Please try again later.',
                    'details': error_msg,
                    'status': openai_rate_limiter.get_status()
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator