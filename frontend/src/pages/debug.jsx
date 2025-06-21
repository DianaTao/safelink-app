import React from 'react';

export default function DebugPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Environment Variables Debug</h1>
      
      <div className="space-y-4">
        <div>
          <strong>NEXT_PUBLIC_SUPABASE_URL:</strong>
          <p className="text-sm text-gray-600 break-all">
            {process.env.NEXT_PUBLIC_SUPABASE_URL || 'NOT SET'}
          </p>
        </div>
        
        <div>
          <strong>NEXT_PUBLIC_SUPABASE_ANON_KEY:</strong>
          <p className="text-sm text-gray-600 break-all">
            {process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? 
              `${process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.substring(0, 20)}...` : 
              'NOT SET'
            }
          </p>
        </div>
        
        <div>
          <strong>NEXT_PUBLIC_MAPBOX_TOKEN:</strong>
          <p className="text-sm text-gray-600 break-all">
            {process.env.NEXT_PUBLIC_MAPBOX_TOKEN ? 
              `${process.env.NEXT_PUBLIC_MAPBOX_TOKEN.substring(0, 20)}...` : 
              'NOT SET'
            }
          </p>
        </div>
      </div>
    </div>
  );
} 