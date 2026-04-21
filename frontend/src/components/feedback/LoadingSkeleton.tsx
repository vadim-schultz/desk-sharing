import type { ReactNode } from 'react';
import {
  Box,
  Skeleton,
  SkeletonCircle,
  SkeletonText,
  VStack,
} from '@chakra-ui/react';

interface LoadingSkeletonProps {
  isOverlay?: boolean;
  isFullPage?: boolean;
  minHeight?: string | number;
  lines?: number;
  showAvatar?: boolean;
  label?: string;
  children?: ReactNode;
}

const LoadingSkeleton = ({
  isOverlay = false,
  isFullPage = false,
  minHeight = '120px',
  lines = 3,
  showAvatar = false,
  label = 'Loading content',
  children,
}: LoadingSkeletonProps) => {
  const content = (
    <Box role="status" aria-live="polite" aria-label={label} width="full">
      {children ?? (
        <VStack align="stretch" gap={4} width="full">
          {showAvatar && <SkeletonCircle size="12" />}
          <Skeleton height="20px" borderRadius="md" />
          <SkeletonText noOfLines={lines} gap="3" height="16px" width="full" />
        </VStack>
      )}
    </Box>
  );

  if (isOverlay) {
    return (
      <Box
        position="absolute"
        inset={0}
        bg="blackAlpha.200"
        display="flex"
        alignItems="center"
        justifyContent="center"
        pointerEvents="none"
        px={6}
      >
        {content}
      </Box>
    );
  }

  if (isFullPage) {
    return (
      <Box
        minH="60vh"
        display="flex"
        alignItems="center"
        justifyContent="center"
        px={6}
        py={12}
      >
        {content}
      </Box>
    );
  }

  return (
    <Box minH={minHeight} px={2} py={4}>
      {content}
    </Box>
  );
};

export default LoadingSkeleton;
