// src/components/skeletons/SkeletonList.tsx
import SkeletonBlock from './SkeletonBlock';

export default function SkeletonList({ count = 4 }: { count?: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="p-3 border border-gray-200 rounded-md bg-white">
          <SkeletonBlock className="h-4 w-1/3 mb-2" />
          <SkeletonBlock className="h-4 w-2/3" />
        </div>
      ))}
    </div>
  );
}
