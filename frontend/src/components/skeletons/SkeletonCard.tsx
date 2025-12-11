// src/components/skeletons/SkeletonCard.tsx
import SkeletonBlock from './SkeletonBlock';

export default function SkeletonCard() {
  return (
    <div className="p-4 border border-gray-200 rounded-md bg-white space-y-3">
      <SkeletonBlock className="h-4 w-1/3" />
      <SkeletonBlock className="h-4 w-2/3" />
      <SkeletonBlock className="h-4 w-1/2" />
    </div>
  );
}
