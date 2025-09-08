from __future__ import annotations

import asyncio
import contextlib
import os
import tracemalloc
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

import psutil
import structlog

logger = structlog.stdlib.get_logger("DEVELOPER")


BYTES_IN_MB: int = 1024 * 1024
DEFAULT_THRESHOLD_PERCENT: float = 75.0
DEFAULT_CHECK_INTERVAL_SECONDS: int = 300
DEFAULT_TOP_N_STATS: int = 10


class SnapshotStat(Protocol):
    size: int
    count: int
    traceback: list  # minimal protocol for our logging


class Snapshot(Protocol):
    def statistics(self, key_type: str) -> Iterable[SnapshotStat]: ...


@dataclass(slots=True)
class MemoryUsage:
    rss_mb: float
    vms_mb: float
    percent: float


class MemoryMonitor:
    """
    Periodically logs process memory usage and (when above threshold) logs
    top allocation backtraces via tracemalloc.
    """

    def __init__(
        self,
        threshold_percent: float = DEFAULT_THRESHOLD_PERCENT,
        check_interval_seconds: int = DEFAULT_CHECK_INTERVAL_SECONDS,
    ) -> None:
        self.threshold_percent: float = threshold_percent
        self.check_interval_seconds: int = check_interval_seconds
        self._task: asyncio.Task[None] | None = None
        self._is_running: bool = False

    def start(self) -> asyncio.Task[None]:
        if self._is_running:
            return self._task
        tracemalloc.start()
        self._is_running = True
        self._task = asyncio.create_task(self._run_loop(), name="memory-monitor")
        return self._task

    async def stop(self) -> None:
        if not self._is_running:
            return
        self._is_running = False
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        self._task = None

    async def _run_loop(self) -> None:
        process = psutil.Process(os.getpid())
        while self._is_running:
            try:
                usage: MemoryUsage = self._gather_process_memory(process)
                logger.info(
                    "memory_usage",
                    rss_mb=f"{usage.rss_mb:.2f}",
                    vms_mb=f"{usage.vms_mb:.2f}",
                    percent=f"{usage.percent:.1f}",
                )
                if usage.percent > self.threshold_percent:
                    await self._log_threshold_exceeded()
            except Exception as exc:  # pragma: no cover (defensive)
                logger.exception("memory_monitor_error", error=str(exc))
            await asyncio.sleep(self.check_interval_seconds)

    def _gather_process_memory(self, process: psutil.Process) -> MemoryUsage:
        mem_info = process.memory_info()
        percent: float = process.memory_percent()
        return MemoryUsage(
            rss_mb=mem_info.rss / BYTES_IN_MB,
            vms_mb=mem_info.vms / BYTES_IN_MB,
            percent=percent,
        )

    async def _log_threshold_exceeded(self) -> None:
        stats = list(tracemalloc.take_snapshot.statistics("traceback"))
        logger.critical(
            "memory_threshold_exceeded",
            threshold_percent=self.threshold_percent,
            top_count=min(DEFAULT_TOP_N_STATS, len(stats)),
        )
        for stat in stats[:DEFAULT_TOP_N_STATS]:
            # Guard against zero division
            avg_kb: float = (stat.size / max(stat.count, 1)) / 1024
            first_frame = getattr(stat.traceback[0], "filename", "?"), getattr(stat.traceback[0], "lineno", "?")
            logger.critical(
                "memory_allocation_stat",
                objects=stat.count,
                total_mb=f"{stat.size / BYTES_IN_MB:.2f}",
                avg_kb=f"{avg_kb:.2f}",
                location=f"{first_frame[0]}:{first_frame[1]}",
            )
