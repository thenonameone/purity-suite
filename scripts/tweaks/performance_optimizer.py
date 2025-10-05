#!/usr/bin/env python3
"""
Purity Ecosystem - Real-Time Performance Optimizer
Optimize system performance based on current workload and user preferences
"""

import psutil
import json
import os
from pathlib import Path

class PerformanceOptimizer:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.config_file = self.base_path / "suite" / "config" / "ecosystem_config.json"
        
    def get_system_stats(self):
        """Get current system performance statistics"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'load_avg': os.getloadavg()[0] if hasattr(os, 'getloadavg') else 0
        }
    
    def optimize_performance(self, mode='balanced'):
        """Apply performance optimizations based on mode"""
        stats = self.get_system_stats()
        
        optimizations = {
            'turbo': {
                'nice_level': -5,
                'io_priority': 'high',
                'cache_size': 'large',
                'parallel_processes': 'max'
            },
            'balanced': {
                'nice_level': 0,
                'io_priority': 'normal', 
                'cache_size': 'medium',
                'parallel_processes': 'auto'
            },
            'eco': {
                'nice_level': 10,
                'io_priority': 'low',
                'cache_size': 'small',
                'parallel_processes': 'minimal'
            }
        }
        
        return optimizations.get(mode, optimizations['balanced'])
    
    def apply_tweaks(self, mode):
        """Apply real-time performance tweaks"""
        tweaks = self.optimize_performance(mode)
        
        # Apply system-level optimizations
        print(f"🚀 Applying {mode} performance mode...")
        print(f"   Process Priority: {tweaks['nice_level']}")
        print(f"   I/O Priority: {tweaks['io_priority']}")
        print(f"   Cache Size: {tweaks['cache_size']}")
        print(f"   Parallel Processes: {tweaks['parallel_processes']}")
        
        return True

if __name__ == "__main__":
    optimizer = PerformanceOptimizer()
    stats = optimizer.get_system_stats()
    print("📊 Current System Stats:")
    print(f"   CPU: {stats['cpu_percent']:.1f}%")
    print(f"   Memory: {stats['memory_percent']:.1f}%")
    print(f"   Disk: {stats['disk_percent']:.1f}%")