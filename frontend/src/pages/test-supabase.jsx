import React, { useEffect, useState } from 'react';

export default function TestSupabasePage() {
  const [status, setStatus] = useState('Testing...');
  const [error, setError] = useState(null);
  const [supabase, setSupabase] = useState(null);

  useEffect(() => {
    // Only import Supabase client on the client side
    if (typeof window !== 'undefined') {
      import('../lib/supabaseClient').then(({ supabase }) => {
        setSupabase(supabase);
      });
    }
  }, []);

  useEffect(() => {
    async function testConnection() {
      if (!supabase) return;
      
      try {
        // Test basic connection
        const { data, error } = await supabase.from('profiles').select('count').limit(1);
        
        if (error) {
          setError(error.message);
          setStatus('Connection failed');
        } else {
          setStatus('Connection successful!');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setStatus('Connection failed');
      }
    }

    if (supabase) {
      testConnection();
    }
  }, [supabase]);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Supabase Connection Test</h1>
      
      <div className="space-y-4">
        <div>
          <strong>Status:</strong> {status}
        </div>
        
        {error && (
          <div className="text-red-600">
            <strong>Error:</strong> {error}
          </div>
        )}
        
        <div className="text-sm text-gray-600">
          <p>URL: {process.env.NEXT_PUBLIC_SUPABASE_URL}</p>
          <p>Key: {process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? 'Set' : 'Not set'}</p>
        </div>
      </div>
    </div>
  );
} 