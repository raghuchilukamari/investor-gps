'use client';

import { useEffect, useState } from 'react';
import { api, HealthStatus } from '@/services/api';

export default function BackendStatus() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [welcome, setWelcome] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthData, welcomeData] = await Promise.all([
          api.getHealth(),
          api.getWelcome()
        ]);
        setHealth(healthData);
        setWelcome(welcomeData.message);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="p-4">Loading backend status...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-4 space-y-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Backend Status</h2>
        {health && (
          <div className="space-y-2">
            <p>Status: <span className="font-medium">{health.status}</span></p>
            <p>Last Check: <span className="font-medium">{new Date(health.timestamp).toLocaleString()}</span></p>
          </div>
        )}
        {welcome && (
          <div className="mt-4">
            <p className="text-gray-600 dark:text-gray-300">{welcome}</p>
          </div>
        )}
      </div>
    </div>
  );
} 