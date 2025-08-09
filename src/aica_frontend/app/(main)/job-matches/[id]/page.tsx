'use client';

import { useParams } from 'next/navigation';

export default function JobMatchDetailPage() {
  const params = useParams();
  const jobId = params.id;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Job Match Details</h1>
      <p className="text-gray-600">Viewing details for job match: {jobId}</p>
    </div>
  );
}
