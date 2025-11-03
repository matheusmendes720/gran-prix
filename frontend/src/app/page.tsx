'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  
  useEffect(() => {
    // Redirect to main dashboard
    router.push('/main');
  }, [router]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Nova Corrente
        </h1>
        <p className="text-xl text-gray-600">
          Carregando Dashboard...
        </p>
      </div>
    </main>
  );
}

