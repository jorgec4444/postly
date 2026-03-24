from backend.app.config import FREE_DAILY_LIMIT
from backend.app.rate_limit.serivce import _today
import logging

logger = logging.getLogger(__name__)

def get_stats(self) -> dict:
        """Return aggregated daily and all-time stats."""
        if not self._db:
            return {"error": "Database not connected"}

        today = _today()
        try:
            rate_rows = (
                self._db.table("rate_limits")
                .select("count")
                .eq("date", today)
                .execute()
            )
            rows = rate_rows.data or []
            total_ips = len(rows)
            total_requests = sum(r["count"] for r in rows)
            at_limit = sum(1 for r in rows if r["count"] >= FREE_DAILY_LIMIT)

            gen_resp = (
                self._db.table("generations")
                .select("id", count="exact")
                .execute()
            )
            total_generations = gen_resp.count or 0

            return {
                "today": {
                    "unique_ips": total_ips,
                    "total_requests": total_requests,
                    "ips_at_limit": at_limit,
                },
                "all_time": {"total_generations": total_generations},
                "free_limit": FREE_DAILY_LIMIT,
            }
        except Exception as exc:
            logger.error("get_stats error: %s", exc)
            return {"error": str(exc)}