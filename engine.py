"""
TradePilot-AI-Pro - Core Engine
Asynchronous event loop managing strategies and exchange connection.
"""

import asyncio
import logging
import signal
from abc import ABC, abstractmethod
from typing import List, Optional, Set

from src.api.exchange_interface import (
    AbstractExchangeInterface,
    ExchangeError,
)

# Configure logger
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Strategy Base Class
# ----------------------------------------------------------------------
class BaseStrategy(ABC):
    """
    Abstract strategy that the engine runs periodically.
    """
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"strategy.{name}")

    @abstractmethod
    async def execute(self, exchange: AbstractExchangeInterface) -> None:
        ...

# ----------------------------------------------------------------------
# Core Engine
# ----------------------------------------------------------------------
class Engine:
    """
    Orchestrates the bot: connects to exchange, runs strategies, handles shutdown.
    """
    def __init__(self, exchange: AbstractExchangeInterface):
        self.exchange = exchange
        self.strategies: List[BaseStrategy] = []
        self._tasks: Set[asyncio.Task] = set()
        self._shutdown_event = asyncio.Event()

    def add_strategy(self, strategy: BaseStrategy) -> None:
        self.strategies.append(strategy)
        logger.info("Strategy '%s' added.", strategy.name)

    async def run(self) -> None:
        # Register signals for graceful shutdown
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: self._shutdown_event.set())

        try:
            await self.exchange.connect()
            logger.info("Exchange connected.")
        except ExchangeError as e:
            logger.critical("Connection failed: %s", e)
            return

        for strat in self.strategies:
            task = asyncio.create_task(self._run_strategy_safely(strat))
            self._tasks.add(task)

        await self._shutdown_event.wait()
        
        for task in self._tasks:
            task.cancel()
        
        await self.exchange.close()
        logger.info("Engine stopped.")

    async def _run_strategy_safely(self, strategy: BaseStrategy) -> None:
        while not self._shutdown_event.is_set():
            try:
                await strategy.execute(self.exchange)
            except Exception as e:
                logger.error("Error in strategy %s: %s", strategy.name, e)
                await asyncio.sleep(10)

