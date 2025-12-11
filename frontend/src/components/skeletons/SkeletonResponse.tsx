// src/components/skeletons/SkeletonResponse.tsx
import SkeletonBlock from './SkeletonBlock';

export default function SkeletonResponse() {
  return (
    <div className="mt-6 border-t pt-4">
      <SkeletonBlock className="h-5 w-1/4 mb-4" />
      <SkeletonBlock className="h-32 w-full mb-4" />
      <div className="flex items-center gap-3 text-sm">
        <SkeletonBlock className="h-4 w-20" />
        <SkeletonBlock className="h-4 w-10" />
      </div>
    </div>
  );
}
