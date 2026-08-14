import time

# ==========================================
# 1. TOKEN BUCKET RATE LIMITER
# ==========================================
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity            # Max tokens bucket can hold
        self.refill_rate = refill_rate      # Tokens added per second
        self.tokens = capacity
        self.last_refill_timestamp = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_timestamp
        # Add tokens based on elapsed time
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill_timestamp = now

    def allow_request(self) -> bool:
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


# ==========================================
# 2. CIRCUIT BREAKER
# ==========================================
class CircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: float):
        self.failure_threshold = failure_threshold  # Consecutive errors before OPEN
        self.recovery_timeout = recovery_timeout    # Cooldown time in OPEN state
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()

    def execute(self, func, *args, **kwargs):
        now = time.time()

        # Check if recovery timeout has passed to attempt HALF-OPEN
        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_timeout:
                print("  [CIRCUIT BREAKER]: Cooldown expired -> Switching to HALF-OPEN")
                self.state = "HALF-OPEN"
            else:
                raise Exception("🚨 [CIRCUIT OPEN]: Fast-failing request! Service unavailable.")

        try:
            result = func(*args, **kwargs)
            # If successful in HALF-OPEN state, reset to CLOSED
            if self.state == "HALF-OPEN":
                print("  [CIRCUIT BREAKER]: Trial call succeeded -> Resetting to CLOSED")
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            print(f"  [CALL FAILED]: Error count = {self.failure_count}")

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_state_change = time.time()
                print("🚨 [CIRCUIT BREAKER]: Failure threshold reached -> TRIP TO OPEN!")
            raise e


# ==========================================
# 3. DEMONSTRATION EXECUTION
# ==========================================
def unstable_downstream_service(should_fail: bool):
    if should_fail:
        raise ConnectionError("503 Service Unavailable")
    return "200 OK: Data Payload"


if __name__ == "__main__":
    print("--- 1. Testing Rate Limiter (Capacity=2, Refill=1/sec) ---")
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=1.0)
    
    for i in range(1, 5):
        allowed = limiter.allow_request()
        print(f"Request #{i}: {'ACCEPTED' if allowed else 'THROTTLED (429)'}")

    print("\n--- 2. Testing Circuit Breaker (Threshold=2 failures, Timeout=2s) ---")
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=2.0)

    # Triggering failures to trip circuit
    for i in range(1, 4):
        print(f"\nAttempt #{i}:")
        try:
            cb.execute(unstable_downstream_service, should_fail=True)
        except Exception as e:
            print(f"Handled Exception: {e}")

    print("\nAttempt #4 (Immediate call while OPEN):")
    try:
        cb.execute(unstable_downstream_service, should_fail=False)
    except Exception as e:
        print(f"Handled Exception: {e}")

    print("\nWaiting 2.1 seconds for cooldown...")
    time.sleep(2.1)

    print("\nAttempt #5 (Call after cooldown during HALF-OPEN):")
    res = cb.execute(unstable_downstream_service, should_fail=False)
    print(f"Response: {res}")