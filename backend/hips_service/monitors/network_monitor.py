"""Network connection monitoring using psutil."""

import asyncio
import psutil
import logging
from typing import Set, Tuple, List

from hips_service.monitors.base_monitor import BaseMonitor
from hips_service.core.event_bus import EventBus, MonitorEvent
from hips_service.core.platform_detector import PlatformDetector
from hips_service.utils.time import get_local_time

logger = logging.getLogger(__name__)


class NetworkMonitor(BaseMonitor):
    """Monitor outbound network connections using psutil."""

    def __init__(self, event_bus: EventBus, interval: float = 5.0,
                 suspicious_ports: List[int] = None, max_events_per_batch: int = 100):
        super().__init__(event_bus, "NetworkMonitor")
        self.interval = interval
        self.suspicious_ports: Set[int] = set(suspicious_ports or [])
        self.max_events_per_batch = max_events_per_batch
        self._seen: Set[Tuple] = set()

    def get_capabilities(self) -> List[str]:
        return ["network_connection"]

    def _conn_key(self, conn) -> Tuple:
        raddr = (conn.raddr.ip, conn.raddr.port) if conn.raddr else ('', 0)
        return (conn.pid or 0, raddr)

    def _initialize(self):
        """Snapshot existing connections so we only alert on NEW ones."""
        try:
            conns = psutil.net_connections(kind='inet')
            self._seen = {self._conn_key(c) for c in conns if c.raddr}
            logger.info(f"NetworkMonitor: {len(self._seen)} existing connections snapshotted")
        except Exception as e:
            logger.warning(f"NetworkMonitor: could not snapshot existing connections: {e}")

    async def _monitoring_loop(self):
        logger.info("NetworkMonitor loop started")
        while self.running:
            try:
                await self._check()
            except Exception as e:
                logger.error(f"NetworkMonitor error: {e}", exc_info=True)
            await asyncio.sleep(self.interval)
        logger.info("NetworkMonitor loop stopped")

    async def _check(self):
        try:
            # Get a snapshot of all active TCP/UDP connections on the system
            conns = psutil.net_connections(kind='inet')
        except Exception as e:
            logger.warning(f"NetworkMonitor: net_connections failed: {e}")
            return

        # Only track connections that have a remote address (outbound connections)
        current: dict[Tuple, psutil._common.sconn] = {}
        for c in conns:
            if c.raddr:
                current[self._conn_key(c)] = c

        # Find connections that appeared since the last poll
        new_keys = set(current.keys()) - self._seen
        self._seen = set(current.keys())

        emitted = 0
        for key in new_keys:
            if emitted >= self.max_events_per_batch:
                break

            conn = current[key]
            dst_ip = conn.raddr.ip
            dst_port = conn.raddr.port
            pid = conn.pid or 0

            # Look up which process owns this connection so we can include it in the event
            process_name = None
            process_path = None
            try:
                if pid:
                    proc = psutil.Process(pid)
                    process_name = proc.name()
                    process_path = proc.exe()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

            # Mark as high severity if destination port is in the known suspicious ports list
            severity = 'high' if dst_port in self.suspicious_ports else 'low'

            event = MonitorEvent(
                timestamp=get_local_time(),
                event_type='network_connection',
                platform=PlatformDetector.get_platform_name(),
                severity=severity,
                data={
                    'dst_ip': dst_ip,
                    'dst_port': dst_port,
                    'src_ip': conn.laddr.ip if conn.laddr else None,
                    'src_port': conn.laddr.port if conn.laddr else None,
                    'protocol': 'tcp' if conn.type and 'SOCK_STREAM' in str(conn.type) else 'udp',
                    'process_pid': pid,
                    'process_name': process_name or 'unknown',
                    'process_path': process_path or '',
                    'status': conn.status or '',
                }
            )
            await self.event_bus.publish(event)
            emitted += 1

    async def start(self):
        if self.running:
            logger.warning(f"{self.name} already running")
            return

        self.running = True
        logger.info(f"{self.name} starting")
        self._initialize()

        if not self.running:
            return

        self._monitor_task = asyncio.create_task(self._monitoring_loop())

    async def stop(self):
        if not self.running:
            return
        self.running = False
        logger.info(f"{self.name} stopping")
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
