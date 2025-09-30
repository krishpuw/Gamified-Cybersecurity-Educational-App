# agents/management_agent.py
from typing import Dict, Any, Tuple, List
from model import db, User, EngagementLog, Badge, UserBadge

DIFF_XP = {"easy": 10, "medium": 20, "hard": 30}
DIFF_SCORE = {"easy": 1, "medium": 2, "hard": 3}

LEVEL_CURVE = [0, 100, 250, 450, 700, 1000, 1350, 1750]  # XP thresholds for levels 1..n

BADGE_RULES = [
    {"name": "First Blood", "desc": "First correct answer!", "predicate": lambda stats: stats["correct_count"] >= 1},
    {"name": "Fast Thinker", "desc": "Answer under 2s", "predicate": lambda stats: stats["last_rt_ms"] is not None and stats["last_rt_ms"] < 2000 and stats["last_correct"]},
    {"name": "Level 5", "desc": "Reached Level 5", "predicate": lambda stats: stats["new_level"] >= 5},
]

def _level_from_xp(total_xp: int) -> int:
    lvl = 1
    for i, thresh in enumerate(LEVEL_CURVE, start=1):
        if total_xp >= thresh:
            lvl = i
    return max(1, lvl)

class ManagementAgent:
    def _ensure_badges(self):
        # idempotent: create default badges if missing
        existing = {b.name for b in Badge.query.all()}
        for rule in BADGE_RULES:
            if rule["name"] not in existing:
                db.session.add(Badge(name=rule["name"], description=rule["desc"]))
        db.session.commit()

    def _award_badges(self, user: User, stats: Dict[str, Any]) -> List[str]:
        self._ensure_badges()
        new_badges = []
        owned = {ub.badge.name for ub in user.user_badges}
        for rule in BADGE_RULES:
            if rule["predicate"](stats) and rule["name"] not in owned:
                badge = Badge.query.filter_by(name=rule["name"]).first()
                db.session.add(UserBadge(user_id=user.id, badge_id=badge.id))
                new_badges.append(rule["name"])
        return new_badges

    def process_event(self, *, user_id: int, operation_id: str | None, question_id: str | None,
                      is_correct: bool, response_time_ms: int | None, difficulty: str | None) -> Dict[str, Any]:
        difficulty = (difficulty or "easy").lower()
        base_xp = DIFF_XP.get(difficulty, 10)
        base_score = DIFF_SCORE.get(difficulty, 1)

        xp_gain = base_xp if is_correct else 0
        score_gain = base_score if is_correct else 0

        # small speed bonus (optional)
        if is_correct and response_time_ms is not None:
            if response_time_ms < 2000:   # <2s
                xp_gain += 5
                score_gain += 1
            elif response_time_ms < 5000: # <5s
                xp_gain += 2

        user = User.query.get(user_id)
        if not user:
            return {"error": f"User {user_id} not found"}

        # Update aggregates
        before_level = user.level or 1
        user.xp = int(user.xp or 0) + xp_gain
        user.score = int(getattr(user, "score", 0)) + score_gain
        user.level = _level_from_xp(user.xp)

        # Log event
        log = EngagementLog(
            user_id=user.id,
            operation_id=operation_id,
            question_id=question_id,
            is_correct=is_correct,
            response_time_ms=response_time_ms,
            difficulty=difficulty,
            xp_delta=xp_gain,
            score_delta=score_gain,
        )
        db.session.add(log)

        # compute quick stats for badge predicates
        correct_count = EngagementLog.query.filter_by(user_id=user.id, is_correct=True).count()
        stats = {
            "correct_count": correct_count,
            "last_rt_ms": response_time_ms,
            "last_correct": is_correct,
            "new_level": user.level,
        }
        new_badges = self._award_badges(user, stats)

        db.session.commit()

        return {
            "xp_gain": xp_gain,
            "new_xp": int(user.xp),
            "new_level": int(user.level),
            "score": int(user.score),
            "leaderboard_rank": None,  # can compute in GET /leaderboard
            "new_badges": new_badges,
        }
